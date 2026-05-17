import sqlite3

# Flight Management System
# Manages flights, pilots, and destinations for an airline company
# Uses SQLite3 for database operations via a command-line interface


class DBOperations:

    # SQL statement to create tables if they don't already exist
    sql_create_pilot_table = """CREATE TABLE IF NOT EXISTS PILOT (
                                pilot_id    INTEGER PRIMARY KEY,
                                first_name  TEXT NOT NULL,
                                last_name   TEXT NOT NULL,
                                licence_no  TEXT NOT NULL,
                                rank        TEXT NOT NULL)"""

    sql_create_destination_table = """CREATE TABLE IF NOT EXISTS DESTINATION (
                                airport_code TEXT PRIMARY KEY,
                                airport_name TEXT NOT NULL,