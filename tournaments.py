# tournaments.py - Tournament & Match Management module
# Functions: create_tournament, view_tournaments, schedule_match,
#            declare_winner, delete_match, tournaments_menu
# Owner: Priyanshu
# tournaments.py - Tournament & Match Management module
# Functions: create_tournament, view_tournaments, schedule_match,
#            declare_match_winner, delete_match, tournaments_menu

import mysql.connector

#create tournament
def create_tournament(conn):
    name = input("Tournament name: ").strip()
    game = input("Game: ").strip()
    date = input("Date (YYYY-MM-DD): ").strip()
    if not name or not game or not date:
        print("All fields are required.")
        return

    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO tournaments (tournament_name, game, tournament_date) VALUES (%s, %s, %s)",
            (name, game, date),
        )
        conn.commit()
        print("Tournament created.")
    except mysql.connector.Error as e:
        print("Error:", e)
    finally:
        cur.close()


#view tournaments
def view_tournaments(conn):
    cur = conn.cursor()
    cur.execute(
        "SELECT tournament_id, tournament_name, game, tournament_date FROM tournaments ORDER BY tournament_id"
    )
    rows = cur.fetchall()
    cur.close()
    if not rows:
        print("No tournaments yet.")
        return False
    print(f"\n{'ID':<5}{'Tournament':<25}{'Game':<15}{'Date':<12}")
    for tid, name, game, date in rows:
        print(f"{tid:<5}{name:<25}{game:<15}{str(date):<12}")
    return True


#view matches
def _view_matches(conn, tournament_id=None):
    """Internal helper: list matches, optionally filtered to one tournament."""
    cur = conn.cursor()
    query = """
        SELECT m.match_id, t1.team_name, t2.team_name, w.team_name, tr.tournament_name
        FROM matches m
        JOIN teams t1 ON m.team1_id = t1.team_id
        JOIN teams t2 ON m.team2_id = t2.team_id
        LEFT JOIN teams w ON m.winner_id = w.team_id
        JOIN tournaments tr ON m.tournament_id = tr.tournament_id
    """
    params = ()
    if tournament_id is not None:
        query += " WHERE m.tournament_id = %s"
        params = (tournament_id,)
    query += " ORDER BY m.match_id"

    cur.execute(query, params)
    rows = cur.fetchall()
    cur.close()
    if not rows:
        print("No matches yet.")
        return False
    print(f"\n{'ID':<5}{'Team 1':<20}{'Team 2':<20}{'Winner':<20}{'Tournament':<20}")
    for mid, t1, t2, winner, tname in rows:
        print(f"{mid:<5}{t1:<20}{t2:<20}{(winner or '-'):<20}{tname:<20}")
    return True


#schedule matches
def schedule_match(conn):
    if not view_tournaments(conn):
        return
    tournament_id = input("Tournament ID: ").strip()
    if not tournament_id.isdigit():
        print("Enter a valid number.")
        return

    cur = conn.cursor()
    cur.execute("SELECT tournament_id FROM tournaments WHERE tournament_id = %s", (tournament_id,))
    if cur.fetchone() is None:
        print("No tournament with that ID.")
        cur.close()
        return

    cur.execute("SELECT team_id, team_name, game FROM teams ORDER BY team_id")
    teams = cur.fetchall()
    cur.close()
    if len(teams) < 2:
        print("Need at least two teams to schedule a match.")
        return
    print(f"\n{'ID':<5}{'Team':<25}{'Game':<20}")
    for tid, tname, tgame in teams:
        print(f"{tid:<5}{tname:<25}{tgame:<20}")

    team1_id = input("Team 1 ID: ").strip()
    team2_id = input("Team 2 ID: ").strip()
    if not team1_id.isdigit() or not team2_id.isdigit():
        print("Enter valid numbers.")
        return
    if team1_id == team2_id:
        print("A team cannot play itself.")
        return

    valid_ids = {str(t[0]) for t in teams}
    if team1_id not in valid_ids or team2_id not in valid_ids:
        print("One or both team IDs don't exist.")
        return

    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO matches (tournament_id, team1_id, team2_id) VALUES (%s, %s, %s)",
            (tournament_id, team1_id, team2_id),
        )
        conn.commit()
        print("Match scheduled.")
    except mysql.connector.Error as e:
        print("Error:", e)
    finally:
        cur.close()


#declare match winner
def declare_match_winner(conn):
    if not _view_matches(conn):
        return
    match_id = input("Match ID: ").strip()
    if not match_id.isdigit():
        print("Enter a valid number.")
        return

    cur = conn.cursor()
    cur.execute("SELECT team1_id, team2_id FROM matches WHERE match_id = %s", (match_id,))
    row = cur.fetchone()
    if row is None:
        print("No match with that ID.")
        cur.close()
        return
    team1_id, team2_id = row

    winner_id = input(f"Winner team ID ({team1_id} or {team2_id}): ").strip()
    if winner_id not in (str(team1_id), str(team2_id)):
        print("Winner must be one of the two teams in this match.")
        cur.close()
        return

    cur.execute("UPDATE matches SET winner_id = %s WHERE match_id = %s", (winner_id, match_id))
    conn.commit()
    print("Winner declared.")
    cur.close()


#delete match
def delete_match(conn):
    if not _view_matches(conn):
        return
    match_id = input("Match ID to delete: ").strip()
    if not match_id.isdigit():
        print("Enter a valid number.")
        return
    if input("Are you sure? (y/n): ").lower() != "y":
        return
    cur = conn.cursor()
    cur.execute("DELETE FROM matches WHERE match_id = %s", (match_id,))
    conn.commit()
    print("Match deleted." if cur.rowcount else "No match with that ID.")
    cur.close()


#tournament menu 
def tournaments_menu(conn):
    while True:
        print("\n--- Tournament & Match Management ---")
        print("1. Create Tournament")
        print("2. View All Tournaments")
        print("3. Schedule Match")
        print("4. Declare Match Winner")
        print("5. Delete Match")
        print("0. Back")
        choice = input("Choose: ").strip()
        if choice == "1":
            create_tournament(conn)
        elif choice == "2":
            view_tournaments(conn)
        elif choice == "3":
            schedule_match(conn)
        elif choice == "4":
            declare_match_winner(conn)
        elif choice == "5":
            delete_match(conn)
        elif choice == "0":
            break
        else:
            print("Invalid choice.")