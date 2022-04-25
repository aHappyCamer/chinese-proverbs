"""
reference : https://www.dataquest.io/blog/loading-data-into-postgres/

Connect to the database to create table and copy csv data into table
"""

import csv
import psycopg2
import os


def csv_to_db():
    # conn = psycopg2.connect(database="dbname", user="username", password="password", host="host", port="####")
    conn = psycopg2.connect(
        "host={} dbname={} user={} password={} port={}".format(
            os.getenv("POSTGRES_HOST"),
            os.getenv("POSTGRES_DB"),
            os.getenv("POSTGRES_USER"),
            os.getenv("POSTGRES_PASS"),
            os.getenv("POSTGRES_PORT"),
        )
    )

    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS proverbs(
        id integer PRIMARY KEY,
        chinese text,
        pinyin text,
        p_translation text
        )
    """
    )

    with open("Chinese_proverbs.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row.
        for row in reader:
            cur.execute(
                "INSERT INTO proverbs VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING",
                row,
            )
    conn.commit()
