# leaderboard.py - Leaderboard module
# Functions: show_leaderboard (ranks teams by total match wins)
# Owner: Priyanshu

import mysql.connector


def show_leaderboard(conn):
    cur = conn.cursor()
    cur.execute(
        """
        SELECT t.team_id, t.team_name, t.game,
        SUM(CASE WHEN m.winner_id = t.team_id THEN 1 ELSE 0 END) AS wins,
        SUM(CASE WHEN m.winner_id IS NOT NULL AND m.winner_id != t.team_id THEN 1 ELSE 0 END) AS losses
        FROM teams t
        LEFT JOIN matches m
        ON (m.team1_id = t.team_id OR m.team2_id = t.team_id) AND m.winner_id IS NOT NULL
        GROUP BY t.team_id, t.team_name, t.game
        ORDER BY wins DESC, losses ASC, t.team_name ASC
        """
    )
    rows = cur.fetchall()
    cur.close()
    if not rows:
        print("No teams yet.")
        return

    print(f"\n{'Rank':<6}{'Team':<22}{'Game':<15}{'P':<5}{'W':<5}{'L':<5}{'Win%':<8}")
    for rank, (team_id, team_name, game, wins, losses) in enumerate(rows, start=1):
        played = wins + losses
        win_pct = (wins / played * 100) if played else 0.0
        print(f"{rank:<6}{team_name:<22}{game:<15}{played:<5}{wins:<5}{losses:<5}{win_pct:<8.1f}")