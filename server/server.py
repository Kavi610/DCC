import time
import sqlite3
from flask import Flask, request, jsonify, abort
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
DATABASE = "inventory.db"

def init_db():
    """Initializes the SQLite database if it doesn't exist."""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS inventory
                 (name TEXT PRIMARY KEY, quantity INTEGER)''')
    conn.commit()
    conn.close()

init_db()

def delay_response():
    """Introduce a 10-second delay."""
    time.sleep(10)

@app.before_request
def log_request():
    app.logger.info("Received %s request for %s with data: %s",
                    request.method, request.path, request.get_json() or request.args)

# Helper: update inventory database
def update_inventory(query, params):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    try:
        c.execute(query, params)
        conn.commit()
    except sqlite3.IntegrityError as e:
        conn.close()
        return False, str(e)
    conn.close()
    return True, ""

@app.route('/transform', methods=['POST'])
def transform():
    delay_response()
    data = request.get_json()
    if not data:
        abort(400, description="No JSON data provided")
    # Expecting location, rotation_euler, and scale
    if not all(key in data for key in ['location', 'rotation_euler', 'scale']):
        abort(400, description="Missing transform data")
    return jsonify({"status": "Transform data received", "data": data}), 200

@app.route('/translation', methods=['POST'])
def translation():
    delay_response()
    data = request.get_json()
    if not data or 'location' not in data:
         abort(400, description="Missing translation data")
    return jsonify({"status": "Translation data received", "location": data['location']}), 200

@app.route('/rotation', methods=['POST'])
def rotation():
    delay_response()
    data = request.get_json()
    if not data or 'rotation_euler' not in data:
        abort(400, description="Missing rotation data")
    return jsonify({"status": "Rotation data received", "rotation": data['rotation_euler']}), 200

@app.route('/scale', methods=['POST'])
def scale():
    delay_response()
    data = request.get_json()
    if not data or 'scale' not in data:
        abort(400, description="Missing scale data")
    return jsonify({"status": "Scale data received", "scale": data['scale']}), 200

@app.route('/file-path', methods=['GET'])
def file_path():
    delay_response()
    # For demonstration, we simulate a file path.
    base_file_path = "/path/to/dcc/file.blend"
    project_folder = "/path/to/dcc/project"
    if request.args.get('projectpath', 'false').lower() == 'true':
        return jsonify({"file_path": project_folder}), 200
    return jsonify({"file_path": base_file_path}), 200

@app.route('/add-item', methods=['POST'])
def add_item():
    delay_response()
    data = request.get_json()
    if not data or 'name' not in data or 'quantity' not in data:
        abort(400, description="Missing item data")
    success, error = update_inventory("INSERT INTO inventory (name, quantity) VALUES (?, ?)",
                                      (data['name'], data['quantity']))
    if not success:
        abort(400, description=f"Error adding item: {error}")
    return jsonify({"status": "Item added", "item": data}), 200

@app.route('/remove-item', methods=['POST'])
def remove_item():
    delay_response()
    data = request.get_json()
    if not data or 'name' not in data:
        abort(400, description="Missing item name")
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("DELETE FROM inventory WHERE name = ?", (data['name'],))
    conn.commit()
    if c.rowcount == 0:
        conn.close()
        abort(404, description="Item not found")
    conn.close()
    return jsonify({"status": "Item removed", "name": data['name']}), 200

@app.route('/update-quantity', methods=['POST'])
def update_quantity():
    delay_response()
    data = request.get_json()
    if not data or 'name' not in data or 'quantity' not in data:
        abort(400, description="Missing data")
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("UPDATE inventory SET quantity = ? WHERE name = ?", (data['quantity'], data['name']))
    conn.commit()
    if c.rowcount == 0:
        conn.close()
        abort(404, description="Item not found")
    conn.close()
    return jsonify({"status": "Item quantity updated", "item": data}), 200

if __name__ == '__main__':
    app.run(debug=True)
