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