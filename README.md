# FlightManagement

A command-line application built with Python and SQLite to manage flights, pilots and destinations for an airline. Built for the Cloud and Databases module at the University of Bath.

---

## How to run

Open in GitHub CodeSpaces and run:

```
python main.py
```

The database and sample data load automatically on first run.

---

## Files

| File | Description |
|---|---|
| `main.py` | Main application |
| `seed_data.sql` | Sample data (loads on first run) |
| `FlightManagement.db` | SQLite database (auto-created) |

---

## Menu

```
1.  Add New Pilot          9.  Update Flight
2.  Add New Destination    10. Assign Pilot to Flight
3.  Add New Flight         11. Delete Flight
4.  View All Flights       12. View Flights with Pilots
5.  View All Pilots        13. Database Summary
6.  View All Destinations  14. Flights by Destination
7.  Search Flight          15. Check Unassigned Flights
8.  Search Pilot            0. Exit
```

---

## Database structure

**PILOT** — `pilot_id` (PK), `first_name`, `last_name`, `licence_no`, `rank`

**DESTINATION** — `airport_code` (PK), `airport_name`, `city`, `country`, `timezone`

**FLIGHT** — `flight_number` + `departure_date` (Composite PK), `departure_time`, `updated_departure_time`, `arrival_time`, `status`, `pilot_id` (FK), `airport_code` (FK)

---

## Requirements

Python 3 — no external libraries required.
