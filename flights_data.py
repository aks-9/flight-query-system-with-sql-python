from sqlalchemy import create_engine, text

# -------------------------
# Database setup
# -------------------------
DATABASE_URL = "sqlite:///data/flights.sqlite3"
engine = create_engine(DATABASE_URL)

# -------------------------
# SQL Queries
# -------------------------
QUERY_FLIGHT_BY_ID = """
SELECT
    flights.ID,
    flights.ORIGIN_AIRPORT,
    flights.DESTINATION_AIRPORT,
    airlines.airline AS AIRLINE,
    flights.DEPARTURE_DELAY AS DELAY
FROM flights
JOIN airlines ON flights.airline = airlines.id
WHERE flights.ID = :id
"""

QUERY_FLIGHTS_BY_DATE = """
SELECT
    flights.ID,
    flights.ORIGIN_AIRPORT,
    flights.DESTINATION_AIRPORT,
    airlines.airline AS AIRLINE,
    flights.DEPARTURE_DELAY AS DELAY
FROM flights
JOIN airlines ON flights.airline = airlines.id
WHERE flights.DAY = :day
  AND flights.MONTH = :month
  AND flights.YEAR = :year
"""

QUERY_DELAYED_BY_AIRLINE = """
SELECT
    flights.ID,
    flights.ORIGIN_AIRPORT,
    flights.DESTINATION_AIRPORT,
    airlines.airline AS AIRLINE,
    flights.DEPARTURE_DELAY AS DELAY
FROM flights
JOIN airlines ON flights.airline = airlines.id
WHERE airlines.airline LIKE :airline
  AND flights.DEPARTURE_DELAY >= 20
"""

QUERY_DELAYED_BY_AIRPORT = """
SELECT
    flights.ID,
    flights.ORIGIN_AIRPORT,
    flights.DESTINATION_AIRPORT,
    airlines.airline AS AIRLINE,
    flights.DEPARTURE_DELAY AS DELAY
FROM flights
JOIN airlines ON flights.airline = airlines.id
WHERE flights.ORIGIN_AIRPORT = :airport
  AND flights.DEPARTURE_DELAY >= 20
"""

# -------------------------
# Helper function
# -------------------------
def execute_query(query, params):
    """
    Execute an SQL query and return a list of rows.
    If an error occurs, return an empty list.
    """
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query), params)
            return result.fetchall()
    except Exception as e:
        print("Query error:", e)
        return []


# -------------------------
# DAL Functions (used by main.py)
# -------------------------
def get_flight_by_id(flight_id):
    params = {"id": flight_id}
    return execute_query(QUERY_FLIGHT_BY_ID, params)


def get_flights_by_date(day, month, year):
    params = {
        "day": day,
        "month": month,
        "year": year
    }
    return execute_query(QUERY_FLIGHTS_BY_DATE, params)


def get_delayed_flights_by_airline(airline_name):
    params = {
        "airline": f"%{airline_name}%"
    }
    return execute_query(QUERY_DELAYED_BY_AIRLINE, params)


def get_delayed_flights_by_airport(airport_code):
    params = {
        "airport": airport_code.upper()
    }
    return execute_query(QUERY_DELAYED_BY_AIRPORT, params)
