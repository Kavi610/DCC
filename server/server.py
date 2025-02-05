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
    c.execute('''CREATE TABLE IF NOT EXISTS inventory (name TEXT PRIMARY KEY, quantity INTEGER)''')
    conn.commit()
    conn.close()

init_db()

def delay_response():
    """Introduce a 10-second delay."""
    time.sleep(10)

@app.before_request
def log_request():
    app.logger.info("Received %s request for %s with data: %s", request.method, request.path, request.get_json() or request.args)

@app.route('/transform', methods=['POST'])
def transform():
    delay_response()
    data = request.get_json()
    if not data:
        abort(400, description="No JSON data provided")
    return jsonify({"status": "Transform data received", "data": data}), 200

if __name__ == '__main__':
    app.run(debug=True)
