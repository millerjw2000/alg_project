import requests
import sqlite3
from urllib.parse import urlparse

# need access to more defensive stats.

STAT_MAPPING = {
    "blocks": "blocks",
    "steals": "steals",
    "defensiveRebounds": "d_rebounds",
    "turnoverPoints": "turnover_points",
    "defReboundRate": "d_rebound_rate",
    "fouls": "fouls",
    "reboundRate": "rebound_rate",
    "rebounds": "rebounds",
    "gamesPlayed": "games_played",
    "assists": "assists",
    "effectiveFGPct": "effective_fg_pct",
    "fieldGoalsMade": "field_goals_made",
    "fieldGoalsAttempted": "field_goals_attempted",
    "fieldGoalPct": "field_goal_pct",
    "freeThrowPct": "free_throw_pct",
    "freeThrowsAttempted": "free_throw_attempts",
    "freeThrowsMade": "free_throws_made",
    "offensiveRebounds": "offensive_rebounds",
    "points": "points",
    "turnovers": "turnovers",
    "threePointPct": "three_point_pct",
    "threePointFieldGoalsAttempted": "three_point_attempts",
    "threePointFieldGoalsMade": "three_points_made",
    "trueShootingPct": "true_shooting_pct",
    "teamTurnovers": "team_turnovers",
    "assistRatio": "assist_ratio",
    "pointsInPaint": "points_in_paint",
    "offReboundRate": "offensive_rebound_rate",
    "possessions": "possessions",
    "paceFactor": "pace_factor",
    "offensiveReboundPct": "offensive_rebound_pct",
    "twoPointFieldGoalsMade": "two_points_made",
    "twoPointFieldGoalsAttempted": "two_point_attempts",
    "twoPointFieldGoalPct": "two_point_pct",
    "shootingEfficiency": "shooting_efficiency",
    "scoringEfficiency": "scoring_efficiency"
}

def initialize_database():
    conn = get_connection()

    with open("evaluator/schema.sql", "r") as file:
        schema = file.read()

    try:
        conn.executescript(schema)
        conn.commit()
    finally:
        conn.close()

def enter_team(info, team_id, team_name):

    team_data = {
        column: None
        for column in STAT_MAPPING.values()
    }

    categories = info["splits"]["categories"]

    for category in categories:

        for stat in category["stats"]:

            stat_name = stat["name"]

            if stat_name in STAT_MAPPING:

                database_column = STAT_MAPPING[stat_name]

                team_data[database_column] = stat.get("value")

    columns = ["id", "team_name"] + list(team_data.keys())

    values = [team_id, team_name] + list(team_data.values())

    placeholders = ", ".join(["?"] * len(columns))

    column_names = ", ".join(columns)

    update_clause = ", ".join(
        f"{column} = excluded.{column}"
        for column in columns
        if column != "id"
    )

    sql = f"""
        INSERT INTO teams ({column_names})
        VALUES ({placeholders})

        ON CONFLICT(id) DO UPDATE SET
        {update_clause}
    """

    conn = get_connection()

    try:
        conn.execute(sql, values)
        conn.commit()

    finally:
        conn.close()

def get_connection():
    conn = sqlite3.connect('evaluator/stats.db')
    return conn

def main():

    initialize_database()
    
    for i in range(1,31):

        url = 'https://sports.core.api.espn.com/v2/sports/basketball/leagues/nba/seasons/2027/teams/' + str(i) + '?lang=en&region=us'
        response = requests.get(url)
        data = response.json()

        team_id = data['id']
        team_name = data['displayName']

        stat_url = data['statistics']['$ref']
        response = requests.get(stat_url)
        data = response.json()
        #print(data)

        enter_team(data,team_id,team_name)

    conn = get_connection()
    try:
        cursor = conn.cursor()

        cursor.execute("SELECT games_played FROM teams WHERE id='1'")

        results = cursor.fetchall()

        for row in results:
            print(row)

    finally:
        conn.close()

if __name__ == '__main__':

    main()