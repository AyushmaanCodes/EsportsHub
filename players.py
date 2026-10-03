# players.py - Player Management module
# Functions: register_player, view_players, search_player, delete_player, players_menu
# Owner: Ayushmaan

import mysql.connector


def register_player(conn):
    name = input("Player name: ").strip()
    game = input("Game: ").strip()
    if not name or not game:
        print("Name and game cannot be empty.")
        return

    cur = conn.cursor()
    cur.execute("SELECT team_id, team_name, game FROM teams ORDER BY team_id")
    teams = cur.fetchall()

    team_id = None
    if teams:
        print(f"\n{'ID':<5}{'Team':<25}{'Game':<20}")
        for tid, tname, tgame in teams:
            print(f"{tid:<5}{tname:<25}{tgame:<20}")
        choice = input("Team ID (leave blank for no team): ").strip()
        if choice:
            if not choice.isdigit():
                print("Enter a valid number. Registering without a team.")
            else:
                cur.execute("SELECT team_id FROM teams WHERE team_id = %s", (choice,))
                if cur.fetchone():
                    team_id = choice
                else:
                    print("No team with that ID. Registering without a team.")
    else:
        print("No teams yet, registering without a team.")

    try:
        cur.execute(
            "INSERT INTO players (player_name, game, team_id) VALUES (%s, %s, %s)",
            (name, game, team_id),
        )
        conn.commit()
        print("Player registered.")
    except mysql.connector.Error as e:
        print("Error:", e)
    finally:
        cur.close()


def view_players(conn):
    cur = conn.cursor()
    cur.execute(
        """
        SELECT p.player_id, p.player_name, p.game, t.team_name
        FROM players p
        LEFT JOIN teams t ON p.team_id = t.team_id
        ORDER BY p.player_id
        """
    )
    rows = cur.fetchall()
    cur.close()
    if not rows:
        print("No players yet.")
        return False
    print(f"\n{'ID':<5}{'Player':<25}{'Game':<20}{'Team':<20}")
    for pid, pname, game, team in rows:
        print(f"{pid:<5}{pname:<25}{game:<20}{team or '-':<20}")
    return True


def search_player(conn):
    term = input("Search by name or game: ").strip()
    if not term:
        print("Enter something to search for.")
        return
    cur = conn.cursor()
    cur.execute(
        """
        SELECT p.player_id, p.player_name, p.game, t.team_name
        FROM players p
        LEFT JOIN teams t ON p.team_id = t.team_id
        WHERE p.player_name LIKE %s OR p.game LIKE %s
        ORDER BY p.player_id
        """,
        (f"%{term}%", f"%{term}%"),
    )
    rows = cur.fetchall()
    cur.close()
    if not rows:
        print("No matching players.")
        return
    print(f"\n{'ID':<5}{'Player':<25}{'Game':<20}{'Team':<20}")
    for pid, pname, game, team in rows:
        print(f"{pid:<5}{pname:<25}{game:<20}{team or '-':<20}")


def delete_player(conn):
    if not view_players(conn):
        return
    player_id = input("Player ID to delete: ").strip()
    if not player_id.isdigit():
        print("Enter a valid number.")
        return
    if input("Are you sure? (y/n): ").lower() != "y":
        return
    cur = conn.cursor()
    cur.execute("DELETE FROM players WHERE player_id = %s", (player_id,))
    conn.commit()
    print("Player deleted." if cur.rowcount else "No player with that ID.")
    cur.close()


def players_menu(conn):
    while True:
        print("\n--- Player Management ---")
        print("1. Register New Player")
        print("2. View All Players")
        print("3. Search Player")
        print("4. Delete Player")
        print("0. Back")
        choice = input("Choose: ").strip()
        if choice == "1":
            register_player(conn)
        elif choice == "2":
            view_players(conn)
        elif choice == "3":
            search_player(conn)
        elif choice == "4":
            delete_player(conn)
        elif choice == "0":
            break
        else:
            print("Invalid choice.")