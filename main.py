# main.py - EsportsHub main menu
# Connects to the database and routes the user to each module's menu.
# Built together by both developers.

# main.py - EsportsHub main menu
# main.py - EsportsHub main menu

from db import get_connection
from teams import teams_menu
from players import players_menu


def main():
    conn = get_connection()
    while True:
        print("\n=== EsportsHub ===")
        print("1. Team Management")
        print("2. Player Management")
        print("0. Exit")
        choice = input("Choose: ").strip()
        if choice == "1":
            teams_menu(conn)
        elif choice == "2":
            players_menu(conn)
        elif choice == "0":
            break
        else:
            print("Invalid choice.")
    conn.close()


if __name__ == "__main__":
    main()