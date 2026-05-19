import sqlite3

# Flight Management System
#-------------------------
# Manages flights, pilots and destinations for an airline company
# This uses SQLite3 for database operations via a command-line interface

#step 1 - creates the tables
#step 2 - initialises the database connection
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
                                PRIMARY KEY (flight_number + departure_date),
                                FOREIGN KEY (pilot_id) REFERENCES PILOT(pilot_id),
                                FOREIGN KEY (airport_code) REFERENCES DESTINATION(airport_code))"""

    
# Initalisation and connection

def __init__(self):
        try:
            self.conn = sqlite3.connect("FlightManagement.db")
            self.cur  = self.conn.cursor()
            self.cur.execute(self.sql_create_pilot_table)
            self.cur.execute(self.sql_create_destination_table)
            self.cur.execute(self.sql_create_flight_table)
            self.conn.commit()
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

def get_connection(self):
    self.conn = sqlite3.connect("FlightManagement.db")
    self.cur  = self.conn.cursor()

# Function to importing data from file [placeholder]


# Insert SQL [placeholder]
    
    # Insert SQL
    sql_insert_pilot       = "INSERT INTO PILOT VALUES (?, ?, ?, ?, ?)"
    sql_insert_destination = "INSERT INTO DESTINATION VALUES (?, ?, ?, ?, ?)"
    sql_insert_flight      = "INSERT INTO FLIGHT VALUES (?, ?, ?, ?, ?, ?, ?, ?)"


# Select SQL [placeholder]

    # Select SQL
    sql_select_all_flights      = "SELECT * FROM FLIGHT"
    sql_select_all_pilots       = "SELECT * FROM PILOT"
    sql_select_all_destinations = "SELECT * FROM DESTINATION"





                                

# Insert data     
def insert_pilot(self):
        try:
            self.get_connection()
            pilot = Pilot()
            pilot.pilot_id   = int(input("Enter pilot ID: "))
            pilot.first_name = input("Enter first name: ")
            pilot.last_name  = input("Enter last name: ")
            pilot.licence_no = input("Enter licence number: ")
            pilot.rank       = input("Enter rank (Captain/First Officer): ")
            self.cur.execute(self.sql_insert_pilot, (
                pilot.pilot_id,
                pilot.first_name,
                pilot.last_name,
                pilot.licence_no,
                pilot.rank))
            self.conn.commit()
            print("Pilot added successfully")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()  

 def insert_destination(self):
        try:
            self.get_connection()
            dest = Destination()
            dest.airport_code = input("Enter airport code (e.g. LHR): ").upper()
            dest.airport_name = input("Enter airport name: ")
            dest.city         = input("Enter city: ")
            dest.country      = input("Enter country: ")
            dest.timezone     = input("Enter timezone (e.g. UTC+0): ")
            self.cur.execute(self.sql_insert_destination, (
                dest.airport_code,
                dest.airport_name,
                dest.city,
                dest.country,
                dest.timezone))
            self.conn.commit()
            print("Destination added successfully")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

def insert_flight(self):
        try:
            self.get_connection()
            flight = Flight()
            flight.flight_number = input("Enter flight number (e.g. BA201): ").upper()
            flight.departure_date = input("Enter departure date (YYYY-MM-DD): ")
            flight.departure_time = input("Enter departure time (HH:MM): ")
            flight.updated_departure_time = None
            flight.arrival_time = input("Enter arrival time (HH:MM): ")
            flight.status = input("Enter status (On Time/Delayed/Cancelled): ")
            flight.pilot_id = int(input("Enter pilot ID: "))
            flight.airport_code = input("Enter destination airport code (e.g. LHR): ").upper()
            self.cur.execute(self.sql_insert_flight, (
                flight.flight_number,
                flight.departure_date,
                flight.departure_time,
                flight.updated_departure_time,
                flight.arrival_time,
                flight.status,
                flight.pilot_id,
                flight.airport_code))
            self.conn.commit()
            print("Flight added successfully")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

