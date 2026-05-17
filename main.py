import sqlite3

# Flight Management System
#-------------------------
# Manages flights, pilots and destinations for an airline company
# This uses SQLite3 for database operations via a command-line interface

#step 1 - creates the tables
#step 2 - adds sample data to the tables
#step 3 - provides functions to add, update, delete and query the data




class DBOperations:

    # SQL statement to create tables , it skips this step if the table already exists
    sql_create_pilot_table = """CREATE TABLE IF NOT EXISTS PILOT (
                                pilot_id    INTEGER PRIMARY KEY,
                                first_name  TEXT NOT NULL,
                                last_name   TEXT NOT NULL,
                                licence_no  TEXT NOT NULL,
                                rank        TEXT NOT NULL)"""

    sql_create_destination_table = """CREATE TABLE IF NOT EXISTS DESTINATION (
                                airport_code TEXT PRIMARY KEY,
                                airport_name TEXT NOT NULL,
                                city         TEXT NOT NULL,
                                country      TEXT NOT NULL,
                                timezone     TEXT NOT NULL)"""

    sql_create_flight_table = """CREATE TABLE IF NOT EXISTS FLIGHT (
                                flight_number        TEXT NOT NULL,
                                departure_date       DATE NOT NULL,
                                departure_time       TIME,
                                updated_departure_time TIME,
                                arrival_time         TIME,
                                status               TEXT,
                                pilot_id             INTEGER,
                                airport_code         TEXT,
                                PRIMARY KEY (flight_number, departure_date),
                                FOREIGN KEY (pilot_id) REFERENCES PILOT(pilot_id),
                                FOREIGN KEY (airport_code) REFERENCES DESTINATION(airport_code))"""
                                
    
                                