# teams.py - Team Management module
# Functions: create_team, view_teams, delete_team, teams_menu
# Owner: Ayushmaan

import mysql.connector


def create_team(conn):
    name = input("Team name: ").strip()
    game = input("Game: ").strip()
    if not name or not game:
        print("Name and game cannot be empty.")
        return
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO teams (team_name, game) VALUES (%s, %s)", (name, game))
        conn.commit()
        print("Team created.")
    except mysql.connector.Error as e:
        print("Error:", e)
    finally:
        cur.close()


def view_teams(conn):
    cur = conn.cursor()
    cur.execute("SELECT team_id, team_name, game FROM teams ORDER BY team_id")
    rows = cur.fetchall()
    cur.close()
    if not rows:
        print("No teams yet.")
        return False
    print(f"\n{'ID':<5}{'Team':<25}{'Game':<20}")
    for team_id, team_name, game in rows:
        print(f"{team_id:<5}{team_name:<25}{game:<20}")
    return True


def assign_player_to_team(conn):
    cur = conn.cursor()
    cur.execute("SELECT player_id, player_name, game, team_id FROM players ORDER BY player_id")
    players = cur.fetchall()
    if not players:
        print("No players registered yet.")
        cur.close()
        return
    print(f"\n{'ID':<5}{'Player':<25}{'Game':<20}{'Team ID':<8}")
    for pid, pname, game, tid in players:
        print(f"{pid:<5}{pname:<25}{game:<20}{str(tid) if tid else '-':<8}")

    player_id = input("Player ID: ").strip()
    if not player_id.isdigit():
        print("Enter a valid number.")
        cur.close()
        return

    if not view_teams(conn):
        cur.close()
        return
    team_id = input("Team ID to assign to: ").strip()
    if not team_id.isdigit():
        print("Enter a valid number.")
        cur.close()
        return

    cur.execute("SELECT team_id FROM teams WHERE team_id = %s", (team_id,))
    if cur.fetchone() is None:
        print("No team with that ID.")
        cur.close()
        return

    cur.execute("UPDATE players SET team_id = %s WHERE player_id = %s", (team_id, player_id))
    conn.commit()
    print("Player assigned." if cur.rowcount else "No player with that ID.")
    cur.close()


def delete_team(conn):
    if not view_teams(conn):
        return
    team_id = input("Team ID to delete: ").strip()
    if not team_id.isdigit():
        print("Enter a valid number.")
        return
    if input("This also deletes the team's matches. Sure? (y/n): ").lower() != "y":
        return
    cur = conn.cursor()
    cur.execute("DELETE FROM teams WHERE team_id = %s", (team_id,))
    conn.commit()
    print("Team deleted." if cur.rowcount else "No team with that ID.")
    cur.close()

def view_teams(conn):
    cur = conn.cursor()
    cur.execute(
        """
        SELECT t.team_id, t.team_name, t.game, COUNT(p.player_id) AS player_count
        FROM teams t
        LEFT JOIN players p ON p.team_id = t.team_id
        GROUP BY t.team_id, t.team_name, t.game
        ORDER BY t.team_id
        """
    )
    rows = cur.fetchall()
    cur.close()
    if not rows:
        print("No teams yet.")
        return False
    print(f"\n{'ID':<5}{'Team':<25}{'Game':<20}{'Players':<8}")
    for team_id, team_name, game, player_count in rows:
        print(f"{team_id:<5}{team_name:<25}{game:<20}{player_count:<8}")
    return True

def view_team_roster(conn):
    if not view_teams(conn):
        return
    team_id = input("Team ID to view roster: ").strip()
    if not team_id.isdigit():
        print("Enter a valid number.")
        return

    cur = conn.cursor()
    cur.execute("SELECT team_name FROM teams WHERE team_id = %s", (team_id,))
    row = cur.fetchone()
    if row is None:
        print("No team with that ID.")
        cur.close()
        return
    team_name = row[0]

    cur.execute(
        "SELECT player_id, player_name, game FROM players WHERE team_id = %s ORDER BY player_id",
        (team_id,),
    )
    players = cur.fetchall()
    cur.close()

    print(f"\nRoster for {team_name}:")
    if not players:
        print("No players on this team yet.")
        return
    print(f"{'ID':<5}{'Player':<25}{'Game':<20}")
    for pid, pname, game in players:
        print(f"{pid:<5}{pname:<25}{game:<20}")

def teams_menu(conn):
    while True:
        print("\n--- Team Management ---")
        print("1. Create Team")
        print("2. View All Teams")
        print("3. View Team Roster")
        print("4. Assign Player to Team")
        print("5. Delete Team")
        print("0. Back")
        choice = input("Choose: ").strip()
        if choice == "1":
            create_team(conn)
        elif choice == "2":
            view_teams(conn)
        elif choice == "3":
            view_team_roster(conn)
        elif choice == "4":
            assign_player_to_team(conn)
        elif choice == "5":
            delete_team(conn)
        elif choice == "0":
            break
        else:
            print("Invalid choice.")