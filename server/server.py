from flask import Flask, request, jsonify
import sqlite3
import time

app = Flask(__name__)

# Database connection function
def connect_db():
    return sqlite3.connect("inventory.db")

# Function to set up the database and create the table if it doesn't exist
def setup_database():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            name TEXT PRIMARY KEY,
            quantity INTEGER
        )
    """)
    conn.commit()
    conn.close()

@app.route('/transform', methods=['POST'])
def transform():
    if request.is_json:
        data = request.get_json()  # Get the JSON data
        print(f"Received data: {data}")  # Debugging line to check the data
        if data:
            return jsonify({"message": "Transform data received successfully!", "data": data}), 200
        else:
            return jsonify({"error": "Empty data received"}), 400
    else:
        return jsonify({"error": "Expected JSON data"}), 415


# Route to add an item to the inventory
@app.route("/add-item", methods=["POST"])
def add_item():
    data = request.json
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO inventory (name, quantity) VALUES (?, ?)", (data["name"], data["quantity"]))
    conn.commit()
    conn.close()
    return jsonify({"message": "Item added"}), 200

# Route to get all items from the inventory
@app.route("/get-items", methods=["GET"])
def get_items():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventory")
    items = [{"name": row[0], "quantity": row[1]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(items), 200

# Call the setup_database function to create the table before the app starts
setup_database()

if __name__ == "__main__":
    app.run(debug=True)
