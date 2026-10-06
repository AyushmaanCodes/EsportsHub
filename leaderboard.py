# leaderboard.py - Leaderboard module
# Functions: show_leaderboard (ranks teams by total match wins)
# Owner: Priyanshu
# leaderboard.py - Leaderboard module
# Functions: show_leaderboard

import mysql.connector


def show_leaderboard(conn):
    cur = conn.cursor()
    cur.execute(
        """
        SELECT t.team_id, t.team_name, t.game, COUNT(m.match_id) AS wins
        FROM teams t
        LEFT JOIN matches m ON m.winner_id = t.team_id
        GROUP BY t.team_id, t.team_name, t.game
        ORDER BY wins DESC, t.team_name ASC
        """
    )
    rows = cur.fetchall()
    cur.close()
    if not rows:
        print("No teams yet.")
        return
    print(f"\n{'Rank':<6}{'Team':<25}{'Game':<20}{'Wins':<6}")
    for rank, (team_id, team_name, game, wins) in enumerate(rows, start=1):
        print(f"{rank:<6}{team_name:<25}{game:<20}{wins:<6}")