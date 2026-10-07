import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "1234"  # MySQL password
}

def init_db():
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    cur.execute("CREATE DATABASE IF NOT EXISTS esportshub;")
    cur.execute("USE esportshub;")
    
    try:
        with open("schema.sql", "r") as f:
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
    init_db()
    
    config = DB_CONFIG.copy()
    config["database"] = "esportshub"
    return mysql.connector.connect(**config)

if __name__ == "__main__":
    conn = get_connection()
    print("Connected successfully:", conn.is_connected())
    conn.close()
