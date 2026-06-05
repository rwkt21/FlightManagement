import sqlite3
from datetime import datetime

# Flight Management System
#-------------------------
# Manages flights, pilots and destinations for an airline company
# This uses SQLite3 for database operations via a command-line interface

#step 1 - creates the tables
#step 2 - initialises the database connection
#step 3 - adds sample data to the tables
#step 4 - provides functions to add, update, delete and query the data
#step 5 - adds the menu for user to execute functions



class DBOperations:

    # skips table creation if tables exist
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
                                PRIMARY KEY (flight_number , departure_date),
                                FOREIGN KEY (pilot_id) REFERENCES PILOT(pilot_id),
                                FOREIGN KEY (airport_code) REFERENCES DESTINATION(airport_code))"""

    # Insert SQL variables
    
    sql_insert_pilot       = "INSERT INTO PILOT VALUES (?, ?, ?, ?, ?)"
    sql_insert_destination = "INSERT INTO DESTINATION VALUES (?, ?, ?, ?, ?)"
    sql_insert_flight      = "INSERT INTO FLIGHT VALUES (?, ?, ?, ?, ?, ?, ?, ?)"

    
    # Initalise and connection

     
    def __init__(self):
        try:
            self.conn = sqlite3.connect("FlightManagement.db")
            self.cur = self.conn.cursor()
            self.cur.execute(self.sql_create_pilot_table)
            self.cur.execute(self.sql_create_destination_table)
            self.cur.execute(self.sql_create_flight_table)
            self.conn.commit()

            # load data on first run only
            self.cur.execute("SELECT COUNT(*) FROM DESTINATION")
            count = self.cur.fetchone()[0]
            if count == 0:
                with open("seed_data.sql", "r") as f:
                    sql = f.read()
                self.cur.executescript(sql)
                self.conn.commit()
                print("Sample data loaded.")

        except Exception as e:
            print(e)

        finally:
            try:
                self.conn.close()
            except Exception:
                pass

    def get_connection(self):
        self.conn = sqlite3.connect("FlightManagement.db")
        self.cur  = self.conn.cursor()

    
    # SQL queries
    sql_database_summary = """SELECT
                                (SELECT COUNT(*) FROM PILOT) as total_pilots,
                                (SELECT COUNT(*) FROM DESTINATION) as total_destinations,
                                (SELECT COUNT(*) FROM FLIGHT) as total_flights"""

    sql_select_all_flights      = "SELECT * FROM FLIGHT"
    sql_select_all_pilots       = "SELECT * FROM PILOT"
    sql_select_all_destinations = "SELECT * FROM DESTINATION"

    sql_search_flight = """SELECT * FROM FLIGHT
                           WHERE flight_number = ?
                           AND departure_date = ?"""

    sql_search_pilot  = "SELECT * FROM PILOT WHERE pilot_id = ?"

    sql_update_flight = """UPDATE FLIGHT
                           SET updated_departure_time = ?, status = ?
                           WHERE flight_number = ? AND departure_date = ?"""

    sql_assign_pilot  = """UPDATE FLIGHT
                           SET pilot_id = ?
                           WHERE flight_number = ? AND departure_date = ?"""

    sql_delete_flight = """DELETE FROM FLIGHT
                           WHERE flight_number = ? AND departure_date = ?"""

    sql_flights_with_pilots = """SELECT f.flight_number, f.departure_date,
                                        f.departure_time, f.status,
                                        p.first_name, p.last_name, p.rank
                                 FROM FLIGHT f
                                 JOIN PILOT p ON f.pilot_id = p.pilot_id
                                 ORDER BY f.departure_date"""
    
    sql_flights_by_destination = """SELECT f.flight_number, f.departure_date,
                                           f.departure_time, f.arrival_time,
                                           f.status, p.first_name, p.last_name
                                    FROM FLIGHT f
                                    JOIN PILOT p ON f.pilot_id = p.pilot_id
                                    WHERE f.airport_code = ?
                                    ORDER BY f.departure_date"""
    sql_unassigned_flights = """SELECT flight_number, departure_date,
                                       departure_time, arrival_time,
                                       status, airport_code
                                FROM FLIGHT
                                WHERE pilot_id IS NULL
                                ORDER BY departure_date"""
    
    #  function to show all flights and assigned pilots
    def flights_with_pilots(self):
        try:
            self.get_connection()
            self.cur.execute(self.sql_flights_with_pilots)
            results = self.cur.fetchall()
            if results:
                print("\nFlights and Assigned Pilots")
                print("\n-----------------------------------------------------------------------------")
                print(f"{'Flight No':<12}{'Date':<14}{'Dep Time':<12}{'Status':<12}{'First Name':<15}{'Last Name':<15}{'Rank'}")
                print("-" * 90)
                for row in results:
                    print(f"{str(row[0]):<12}{str(row[1]):<14}{str(row[2]):<12}{str(row[3]):<12}{str(row[4]):<15}{str(row[5]):<15}{str(row[6])}")
            else:
                print("No flights found")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()


    # Function to importing data from file   
    def insert_pilot(self):
        try:
            self.get_connection()
            pilot = Pilot()
            while True:
                try:
                    pilot.pilot_id = int(input("Enter pilot ID: "))
                    break
                except ValueError:
                    print("Pilot ID must be a number. Please try again.")
                self.cur.execute("SELECT COUNT(*) FROM PILOT WHERE pilot_id = ?", (pilot.pilot_id,))
                if self.cur.fetchone()[0] > 0:
                    print(f"Pilot ID {pilot.pilot_id} already exists. Please use a different ID.")
                    return        
            
            pilot.first_name = input("Enter first name: ")
            pilot.last_name = input("Enter last name: ")
            pilot.licence_no = input("Enter licence number: ")
            while True:
                rank_input = input("Enter rank - C (Captain), F (First Officer): ").upper()
                if rank_input == "C":
                    pilot.rank = "Captain"
                    break
                elif rank_input == "F":
                    pilot.rank = "First Officer"
                    break
                else:
                    print("Invalid input. Please enter C or F")
            self.cur.execute(self.sql_insert_pilot, (
                pilot.pilot_id,
                pilot.first_name,
                pilot.last_name,
                pilot.licence_no,
                pilot.rank))
            self.conn.commit()
            print("Pilot added successfully")
        except sqlite3.Error as err:
            print("Database error:", err)

        self.conn.close()

    def insert_destination(self):
        try:
            self.get_connection()
            dest = Destination()
            while True:
                dest.airport_code = input("Enter airport code (e.g. LHR): ").upper()
                if len(dest.airport_code) == 3 and dest.airport_code.isalpha():
                    self.cur.execute("SELECT COUNT(*) FROM DESTINATION WHERE airport_code = ?", (dest.airport_code,))
                    if self.cur.fetchone()[0] > 0:
                        print(f"{dest.airport_code} already exists. Please use a different code.")
                    else:
                        break
                else:
                    print("Airport code must be exactly 3 letters e.g. LHR")
            
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
            print("Destination saved successfully")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def insert_flight(self):
        try:
            self.get_connection()
            flight = Flight()
            flight.flight_number = input("Enter flight number (e.g. BA201): ").upper()
            while True:
                flight.departure_date = input("Enter departure date (YYYY-MM-DD): ")
                try:
                    datetime.strptime(flight.departure_date, "%Y-%m-%d")
                    break
                except ValueError:
                    print("Invalid date. Please use YYYY-MM-DD e.g. 2025-06-01")
            self.cur.execute("SELECT COUNT(*) FROM FLIGHT WHERE flight_number = ? AND departure_date = ?", (flight.flight_number, flight.departure_date))
            if self.cur.fetchone()[0] > 0:
                print(f"Flight {flight.flight_number} on {flight.departure_date} already exists.")
                return         
            
            while True:
                flight.departure_time = input("Enter departure time (HH:MM): ")
                try:
                    datetime.strptime(flight.departure_time, "%H:%M")
                    break
                except ValueError:
                    print("Invalid time. Please use HH:MM e.g. 09:30")
            flight.updated_departure_time = None
            while True:
                flight.arrival_time = input("Enter arrival time (HH:MM): ")
                try:
                    datetime.strptime(flight.arrival_time, "%H:%M")
                    break
                except ValueError:
                    print("Invalid time. Please use HH:MM e.g. 09:30")
            while True:
                status_input = input("Enter status - O (On Time), D (Delayed), C (Cancelled): ").upper()
                if status_input == "O":
                    flight.status = "On Time"
                    break
                elif status_input == "D":
                    flight.status = "Delayed"
                    break
                elif status_input == "C":
                    flight.status = "Cancelled"
                    break
                else:
                    print("Invalid input. Please enter O, D or C")
            while True:
                try:
                    flight.pilot_id = int(input("Enter pilot ID: "))
                    break
                except ValueError:
                    print("Pilot ID must be a number. Please try again.")
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
            print("Flight added to database")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    #  Selects All

    def select_all_flights(self):
        try:
            self.get_connection()
            self.cur.execute(self.sql_select_all_flights)

            rows = self.cur.fetchall()

            if not rows:
                print("No flights found")
            else:
                print("\nList of All Flights")
                print("-" * 70)
                for row in rows:
                    print(f"{row[0]} | {row[1]} | {row[5]} | {row[7]}")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def select_all_pilots(self):
        try:
            self.get_connection()
            self.cur.execute(self.sql_select_all_pilots)
            rows = self.cur.fetchall()
            if rows:
                print("\nList of All Pilots")
                print("\n----------------------------------------------------------------")
                print(f"{'Pilot ID':<12}{'First Name':<15}{'Last Name':<15}{'Licence No':<18}{'Rank'}")
                print("-" * 70)
                for row in rows:
                    print(f"{str(row[0]):<12}{str(row[1]):<15}{str(row[2]):<15}{str(row[3]):<18}{str(row[4])}")
            else:
                print("No pilots found")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    #  Selects all the destinations
    def select_all_destinations(self):
        try:
            self.get_connection()
            self.cur.execute(self.sql_select_all_destinations)
            rows = self.cur.fetchall()
            if rows:
                print("\n List of All Destinations")
                print("\n ----------------------------------------------------------------------------------")
                print(f"{'Airport Code':<14}{'Airport Name':<40}{'City':<15}{'Country':<20}{'Timezone'}")
                print("-" * 100)
                for row in rows:
                    print(f"{str(row[0]):<14}{str(row[1]):<40}{str(row[2]):<15}{str(row[3]):<20}{str(row[4])}")
            else:
                print("No destinations found")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    # Searches Database
    def search_flight(self):
        try:
            self.get_connection()
            flight_number = input("Enter flight number: ").upper()
            self.cur.execute("SELECT * FROM FLIGHT WHERE flight_number = ?", (flight_number,))
            results = self.cur.fetchall()
            if results:
                print(f"\nFlights found for {flight_number}:")
                print(f"{'#':<5}{'Date':<14}{'Dep Time':<12}{'Arr Time':<12}{'Status':<12}{'Pilot ID':<10}{'Airport'}")
                print("-" * 70)
                for i, row in enumerate(results, 1):
                    print(f"{str(i):<5}{str(row[1]):<14}{str(row[2]):<12}{str(row[4]):<12}{str(row[5]):<12}{str(row[6]):<10}{str(row[7])}")
            else:
                print(f"No flights found for {flight_number}")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def search_pilot(self):
        try:
            self.get_connection()
            while True:
                try:
                    pilot_id = int(input("Enter pilot ID: "))
                    break
                except ValueError:
                    print("Pilot ID must be a number. Please try again.")
            self.cur.execute(self.sql_search_pilot, (pilot_id,))
            results = self.cur.fetchall()
            if results:
                print("\nPilot Found")
                print(f"{'Pilot ID':<12}{'First Name':<15}{'Last Name':<15}{'Licence No':<18}{'Rank'}")
                print("-" * 70)
                for row in results:
                    print(f"{str(row[0]):<12}{str(row[1]):<15}{str(row[2]):<15}{str(row[3]):<18}{str(row[4])}")
            else:
                print("No pilot found with that ID")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    #  updates Data
    def update_flight(self):
        try:
            self.get_connection()
            flight_number = input("Enter flight number to update: ").upper()
            self.cur.execute("SELECT * FROM FLIGHT WHERE flight_number = ?", (flight_number,))
            results = self.cur.fetchall()
            if not results:
                print(f"No flights found for {flight_number}")
                return
            print(f"\nFlights found for {flight_number}:")
            print(f"{'#':<5}{'Date':<14}{'Dep Time':<12}{'Arr Time':<12}{'Status':<12}{'Pilot ID':<10}{'Airport'}")
            print("-" * 70)
            for i, row in enumerate(results, 1):
                print(f"{str(i):<5}{str(row[1]):<14}{str(row[2]):<12}{str(row[4]):<12}{str(row[5]):<12}{str(row[6]):<10}{str(row[7])}")
            while True:
                try:
                    choice = int(input("\nEnter the number of the flight to update: "))
                    if 1 <= choice <= len(results):
                        break
                    else:
                        print(f"Please enter a number between 1 and {len(results)}")
                except ValueError:
                    print("Please enter a valid number")
            selected = results[choice - 1]
            departure_date = selected[1]
            print(f"\nUpdating {flight_number} on {departure_date}")
            while True:
                updated_departure_time = input("Enter updated departure time (HH:MM): ")
                try:
                    datetime.strptime(updated_departure_time, "%H:%M")
                    break
                except ValueError:
                    print("Invalid time. Please use HH:MM e.g. 14:45")
            while True:
                status_input = input("Enter status - O (On Time), D (Delayed), C (Cancelled): ").upper()
                if status_input == "O":
                    status = "On Time"
                    break
                elif status_input == "D":
                    status = "Delayed"
                    break
                elif status_input == "C":
                    status = "Cancelled"
                    break
                else:
                    print("Invalid input. Please enter O, D or C")
            self.cur.execute(self.sql_update_flight, (
                updated_departure_time,
                status,
                flight_number,
                departure_date))
            if self.cur.rowcount > 0:
                self.conn.commit()
                print("Flight schedule updated")
            else:
                print("No flight found with that number and date")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def assign_pilot(self):
        try:
            self.get_connection()
            flight_number = input("Enter flight number: ").upper()
            self.cur.execute("SELECT * FROM FLIGHT WHERE flight_number = ?", (flight_number,))
            results = self.cur.fetchall()
            if not results:
                print(f"No flights found for {flight_number}")
                return
            print(f"\nFlights found for {flight_number}:")
            print(f"{'#':<5}{'Date':<14}{'Dep Time':<12}{'Arr Time':<12}{'Status':<12}{'Current Pilot ID'}")
            print("-" * 70)
            for i, row in enumerate(results, 1):
                print(f"{str(i):<5}{str(row[1]):<14}{str(row[2]):<12}{str(row[4]):<12}{str(row[5]):<12}{str(row[6])}")
            while True:
                try:
                    choice = int(input("\nEnter the number of the flight to assign a pilot to: "))
                    if 1 <= choice <= len(results):
                        break
                    else:
                        print(f"Please enter a number between 1 and {len(results)}")
                except ValueError:
                    print("Please enter a valid number")
            selected = results[choice - 1]
            departure_date = selected[1]
            print(f"\nAssigning pilot to {flight_number} on {departure_date}")
            while True:
                try:
                    pilot_id = int(input("Enter new pilot ID: "))
                    break
                except ValueError:
                    print("Pilot ID must be a number. Please try again.")
            self.cur.execute(self.sql_assign_pilot, (
                pilot_id,
                flight_number,
                departure_date))
            if self.cur.rowcount > 0:
                self.conn.commit()
                print("Pilot assigned to flight")
            else:
                print("No flight found with that number and date")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    #  Deletes Data 
    def delete_flight(self):
        try:
            self.get_connection()
            flight_number = input("Enter flight number to delete: ").upper()
            while True:
                departure_date = input("Enter departure date (YYYY-MM-DD): ")
                try:
                    datetime.strptime(departure_date, "%Y-%m-%d")
                    break
                except ValueError:
                    print("Invalid date. Please use YYYY-MM-DD e.g. 2025-06-01")
            confirm = input(f"Are you sure you want to delete {flight_number} on {departure_date}? (yes/no): ")
            if confirm.lower() == "yes":
                self.cur.execute(self.sql_delete_flight, (flight_number, departure_date))
                if self.cur.rowcount > 0:
                    self.conn.commit()
                    print("Flight removed")
                else:
                    print("No flight found with that number and date")
            else:
                print("Delete cancelled")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    # flights by destination
    def flights_by_destination(self):
        try:
            self.get_connection()
            while True:
                airport_code = input("Enter airport code (e.g. LHR): ").upper()
                if len(airport_code) == 3 and airport_code.isalpha():
                    break
                else:
                    print("Airport code must be exactly 3 letters e.g. LHR")
            self.cur.execute("SELECT airport_name, city, country FROM DESTINATION WHERE airport_code = ?", (airport_code,))
            destination = self.cur.fetchone()
            if not destination:
                print(f"No destination found with airport code {airport_code}")
                return
            print(f"\n--- FLIGHTS TO {destination[0]}, {destination[1]}, {destination[2]} ---")
            self.cur.execute(self.sql_flights_by_destination, (airport_code,))
            results = self.cur.fetchall()
            if results:
                print(f"{'Flight No':<12}{'Date':<14}{'Dep Time':<12}{'Arr Time':<12}{'Status':<12}{'Pilot'}")
                print("-" * 80)
                for row in results:
                    pilot_name = f"{row[5]} {row[6]}"
                    print(f"{str(row[0]):<12}{str(row[1]):<14}{str(row[2]):<12}{str(row[3]):<12}{str(row[4]):<12}{pilot_name}")
                print(f"\nTotal flights to {airport_code}: {len(results)}")
            else:
                print(f"No flights found to {airport_code}")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()
    # Data Summary
    def database_summary(self):
        try:
            self.get_connection()
            self.cur.execute(self.sql_database_summary)
            row = self.cur.fetchone()
            print("\n--- DATABASE SUMMARY ---")
            print(f"{'Table':<20}{'Total Records'}")
            print("-" * 35)
            print(f"{'Pilots':<20}{row[0]}")
            print(f"{'Destinations':<20}{row[1]}")
            print(f"{'Flights':<20}{row[2]}")
            print("-" * 35)
            print(f"{'Total':<20}{row[0] + row[1] + row[2]}")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()


# The Classes
#--------------------------

class Pilot:
    def __init__(self):
        self.pilot_id = None
        self.first_name = None
        self.last_name = None
        self.licence_no = None
        self.rank = None

    def __str__(self):
        return f"Pilot ID: {self.pilot_id}, Name: {self.first_name} {self.last_name}, Licence: {self.licence_no}, Rank: {self.rank}"


class Destination:
    def __init__(self):
        self.airport_code = None
        self.airport_name = None
        self.city = None
        self.country = None
        self.timezone = None

    def __str__(self):
        return f"Airport: {self.airport_code} - {self.airport_name}, {self.city}, {self.country} ({self.timezone})"


class Flight:
    def __init__(self):
        self.flight_number = None
        self.departure_date = None
        self.departure_time = None
        self.updated_departure_time = None
        self.arrival_time = None
        self.status = None
        self.pilot_id= None
        self.airport_code = None

    def __str__(self):
        return f"Flight: {self.flight_number} on {self.departure_date}, Dep: {self.departure_time}, Arr: {self.arrival_time}, Status: {self.status}"


# Main Menu
# -----------------

def main_menu():
    db = DBOperations()
    while True:
        print("\n FLIGHT MANAGEMENT SYSTEM MENU")
        print("\n--------------------------------")
        print("1. Add New Pilot")
        print("2. Add a New Destination")
        print("3. Add a New Flight")
        print("4. View All flights")
        print("5. View All Pilots")
        print("6. View All Destinations")
        print("7. Search Flight")
        print("8. Search Pilot")
        print("9. Update Existing Flight")
        print("10. Assign Pilot to Flight")
        print("11. Delete Existing Flight")
        print("12. View Flights with Pilots")
        print("13. Summary of Data")
        print("14. View Flights by Destination")
        print("0. Exit")
        choice = input("Enter Number of your choice: ")
        
        if choice == "1":
            db.insert_pilot()
        elif choice == "2":
            db.insert_destination()
        elif choice == "3":
            db.insert_flight()
        elif choice == "4":
            db.select_all_flights()
        elif choice == "5":
            db.select_all_pilots()
        elif choice == "6":
            db.select_all_destinations()
        elif choice == "7":
            db.search_flight()
        elif choice == "8":
            db.search_pilot()
        elif choice == "9":
            db.update_flight()
        elif choice == "10":
            db.assign_pilot()
        elif choice == "11":
            db.delete_flight()
        elif choice == "12":
            db.flights_with_pilots()
        elif choice == "13":
            db.database_summary()
        elif choice == "14":
            db.flights_by_destination()
        elif choice == "0":
            print("Closing...")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main_menu()


