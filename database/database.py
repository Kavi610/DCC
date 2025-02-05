import sqlite3

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

if __name__ == "__main__":
    setup_database()
