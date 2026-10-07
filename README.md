# EsportsHub

A console application for managing an esports competition — teams, players, tournaments, and matches, built with Python and MySQL.

## Features
--**Team Management** : create teams, view all teams, assign players, delete teams
--**Player Management** : register players, view all players, search by name or game, delete players
--**Tournament & Match Management** : create tournaments, schedule matches, declare match winners, delete matches or tournaments
--**Leaderboard** : ranks all teams by total match wins

## Tech Stack
--Python 3.14
--MySQL 8.0, via `mysql-connector-python`

## Setup
1. Install Python 3.x and MySQL Server.
2. Install the required library: pip install mysql-connector-python
3. In `db.py`, set `DB_CONFIG["password"]` to your own MySQL root password.
4. Run the program.

The database and tables are created automatically on first run.

## File Structure

| File              | Purpose                               |
| `db.py`           | Database connection and auto-setup    |
| `schema.sql`      | Table definitions                     |
| `teams.py`        | Team Management                       |
| `players.py`      | Player Management                     |
| `tournaments.py`  | Tournament & Match Management         |
| `leaderboard.py`  | Leaderboard                           |
| `main.py`         | Main menu, ties all modules together  |

## Authors
Ayushmaan Singh and Priyanshu