import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "qwertyuiop[]"  # Your MySQL password
}

def init_db():
    """Creates database and tables automatically if they don't exist."""
    # 1. Connect to MySQL server (without specifying a database yet)
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    # 2. Create and select database
    cur.execute("CREATE DATABASE IF NOT EXISTS esportshub;")
    cur.execute("USE esportshub;")
    
    # 3. Execute schema queries from schema.sql
    try:
        with open("schema.sql", "r") as f:
            # Read whole file and split into individual SQL statements
            sql_commands = f.read().split(";")
            for command in sql_commands:
                cmd = command.strip()
                if cmd:
                    cur.execute(cmd)
        conn.commit()
    except Exception as e:
        print("Database initialization note/error:", e)
    finally:
        cur.close()
        conn.close()

def get_connection():
    """Ensures database exists, then returns connection to esportshub."""
    init_db()  # Runs the auto-setup check every time
    
    config = DB_CONFIG.copy()
    config["database"] = "esportshub"
    return mysql.connector.connect(**config)

if __name__ == "__main__":
    conn = get_connection()
    print("Connected successfully:", conn.is_connected())
    conn.close()

# db.py - Database connection
# get_connection() returns a MySQL connection used by every module.
# Keep your real password out of the GitHub copy of this file.