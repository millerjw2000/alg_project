import sqlite3
import requests
from urllib.parse import urlparse

def get_connection():
    conn = sqlite3.connect('evaluator/stats.db')
    return conn

def get_data_from_db(pref,team_id):

    result_dict = {}

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM teams
            WHERE id = ?
        """, (team_id,))

        row = cursor.fetchone()

        if row is None:
            print(f"No team found with ID {team_id}")
            return

        column_names = [description[0] for description in cursor.description]

        for name, value in zip(column_names, row):

            result_dict[(pref + '_'+ name).upper()] = value

        return result_dict

    finally:
        conn.close()
        