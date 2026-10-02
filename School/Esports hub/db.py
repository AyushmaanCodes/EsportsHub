import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="esportshub",
    )

if __name__ == "__main__":
    conn = get_connection()
    print("Connected:", conn.is_connected())
    conn.close()

# db.py - Database connection
# get_connection() returns a MySQL connection used by every module.
# Keep your real password out of the GitHub copy of this file.