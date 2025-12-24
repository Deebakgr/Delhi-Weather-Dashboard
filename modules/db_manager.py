import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path("weather.db")

# -----------------------------------------------------------
# Create DB and table
# -----------------------------------------------------------
def create_table():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            year INTEGER,
            month INTEGER,
            day INTEGER,
            temperature REAL,
            humidity REAL,
            pressure REAL,
            heat_index REAL,
            weather_condition TEXT
        )
    """)
    conn.commit()
    conn.close()

# -----------------------------------------------------------
# Insert DataFrame into DB
# -----------------------------------------------------------
def insert_dataframe(df, if_exists='replace'):
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("weather", conn, if_exists=if_exists, index=False)
    conn.close()

# -----------------------------------------------------------
# Query Helpers
# -----------------------------------------------------------
def query_to_df(query, params=None):
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return df
    except Exception as e:
        print(f"Database query error: {e}")
        conn.close()
        return pd.DataFrame()

def get_by_date(date_iso):
    query = """
        SELECT datetime(date, 'localtime') as datetime, weather_condition, temperature, humidity, pressure 
        FROM weather WHERE date(date)=date(?)
    """
    return query_to_df(query, (date_iso,))

def get_by_month_year(year, month):
    query = """
        SELECT datetime(date, 'localtime') as datetime, weather_condition, temperature, humidity, pressure 
        FROM weather WHERE year=? AND month=? ORDER BY date
    """
    return query_to_df(query, (year, month))

def stats_monthly_for_year(year):
    query = "SELECT month, temperature FROM weather WHERE year=?"
    df = query_to_df(query, (year,))
    if df.empty:
        return pd.DataFrame(columns=["month", "max_temp", "median_temp", "min_temp"])
    grouped = df.groupby("month")["temperature"].agg(["max", "median", "min"]).reset_index()
    grouped.columns = ["month", "max_temp", "median_temp", "min_temp"]
    return grouped




