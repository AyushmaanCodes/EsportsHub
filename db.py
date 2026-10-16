import mysql.connector
import os

#Returns True if this password actually connects to MySQL, False otherwise.
def try_password(pwd):
    try:
        conn = mysql.connector.connect(host="localhost", user="root", password=pwd)
        conn.close()
        return True
    except mysql.connector.Error:
        return False

#Reads a saved MySQL password, or keeps asking until one actually works, then saves it
def get_password():
    if os.path.exists("db_password.txt"):
        with open("db_password.txt", "r") as f:
            saved = f.read().strip()
        if try_password(saved):
            return saved
        print("Saved password no longer works.")

    while True:
        pwd = input("Enter your MySQL root password: ").strip()
        if try_password(pwd):
            with open("db_password.txt", "w") as f:
                f.write(pwd)
            return pwd
        print("Wrong password. Try again.")


def get_db_config():
    return {
        "host": "localhost",
        "user": "root",
        "password": get_password(),
    }


#Creates database and tables automatically if they don't exist
def init_db():
    conn = mysql.connector.connect(**get_db_config())
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

#Ensures database exists, then returns connection to esportshub
def get_connection():
    init_db()
    config = get_db_config()
    config["database"] = "esportshub"
    return mysql.connector.connect(**config)


if __name__ == "__main__":
    conn = get_connection()
    print("Connected successfully:", conn.is_connected())
    conn.close()