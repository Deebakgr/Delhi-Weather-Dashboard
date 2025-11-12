# # streamlit_app.py
# import streamlit as st
# import pandas as pd
# from modules.preprocess_utils import process_excel
# from pathlib import Path

# ICON_PATH = Path("pngtree-cloud.png")

# st.set_page_config(
#     page_title="Delhi Weather Explorer",
#     page_icon=str(ICON_PATH) if ICON_PATH.exists() else None,
#     layout="wide"
# )
# from modules.db_manager import (
#     create_table,
#     insert_dataframe,
#     get_by_date,
#     get_by_month_year,
#     stats_monthly_for_year,
#     DB_PATH
# )
# from pathlib import Path
# import sqlite3

# # -----------------------------------------------------------
# # Streamlit Page Configuration
# # -----------------------------------------------------------
# st.set_page_config(page_title="Delhi Weather Data Explorer", layout="wide")
# st.title("🌦 Delhi Weather Data Explorer — 20-Year Historical Dataset")

# # -----------------------------------------------------------
# # Upload Excel File Section
# # -----------------------------------------------------------
# uploaded = st.file_uploader("📤 Upload Excel Weather Dataset (.xlsx)", type=["xlsx"])

# if uploaded:
#     st.info("Processing uploaded Excel file... please wait ⏳")
#     try:
#         df = process_excel(uploaded)
#         create_table()
#         insert_dataframe(df, if_exists="replace")
#         st.success(f"✅ Dataset processed and stored successfully ({len(df)} rows).")
#     except Exception as e:
#         st.error(f"❌ Failed to process file: {e}")

# # -----------------------------------------------------------
# # Ensure Database Exists
# # -----------------------------------------------------------
# if not Path(DB_PATH).exists():
#     st.warning("⚠️ No database found. Please upload an Excel file first.")
#     st.stop()

# # -----------------------------------------------------------
# # Sidebar Options
# # -----------------------------------------------------------
# with st.sidebar:
#     st.header("🔍 Query Weather Data")
#     view = st.radio("Choose View", ["By Date", "By Month", "Yearly Stats"])

#     # default placeholders, no pre-filled or range limits
#     date_input = ""
#     year_input = ""
#     month_input = ""
#     stats_year = ""

#     if view == "By Date":
#         st.subheader("📅 Search by Date")
#         date_input = st.text_input("Enter Date (YYYY-MM-DD)", placeholder="e.g., 2015-06-12")

#     elif view == "By Month":
#         st.subheader("🗓 Search by Month")
#         year_input = st.text_input("Enter Year (e.g., 2015)")
#         month_input = st.text_input("Enter Month (1–12)")

#     elif view == "Yearly Stats":
#         st.subheader("📈 View Yearly Temperature Trends")
#         stats_year = st.text_input("Enter Year (e.g., 2018)")

# # -----------------------------------------------------------
# # Helper: SQLite Query Utility
# # -----------------------------------------------------------
# def run_query(sql, params=()):
#     conn = sqlite3.connect(DB_PATH)
#     df = pd.read_sql_query(sql, conn, params=params)
#     conn.close()
#     return df

# st.markdown("---")

# # -----------------------------------------------------------
# # Main Logic
# # -----------------------------------------------------------
# if view == "By Date":
#     if not date_input.strip():
#         st.info("🕓 Please enter a date in the format YYYY-MM-DD to fetch weather details.")
#     else:
#         try:
#             pd.to_datetime(date_input, format="%Y-%m-%d")  # Validate format
#             st.subheader(f"🌤 Weather Details for {date_input}")
#             df = get_by_date(date_input)
#             if df.empty:
#                 st.warning("No data found for this date.")
#             else:
#                 st.dataframe(df)
#                 st.success(f"✅ {len(df)} record(s) found for {date_input}.")
#                 st.download_button(
#                     "⬇️ Download CSV",
#                     df.to_csv(index=False).encode("utf-8"),
#                     file_name=f"weather_{date_input}.csv"
#                 )
#         except ValueError:
#             st.error("❌ Please enter a valid date in the format YYYY-MM-DD.")

# elif view == "By Month":
#     if not year_input.strip() or not month_input.strip():
#         st.info("🕓 Please enter both year and month to view weather data.")
#     else:
#         try:
#             y, m = int(year_input), int(month_input)
#             st.subheader(f"📆 Weather Records for {y}-{m:02d}")
#             df = get_by_month_year(y, m)
#             if df.empty:
#                 st.warning("No data found for this month and year.")
#             else:
#                 st.dataframe(df)
#                 numeric_cols = [c for c in ['temperature', 'humidity', 'pressure', 'heat_index'] if c in df.columns]
#                 if numeric_cols:
#                     st.write("### Summary Statistics:")
#                     st.dataframe(df[numeric_cols].describe())
#                 else:
#                     st.info("No numeric weather columns found for summary statistics.")

#                 st.download_button(
#                     "⬇️ Download CSV",
#                     df.to_csv(index=False).encode("utf-8"),
#                     file_name=f"weather_{y}_{m:02d}.csv"
#                 )
#         except ValueError:
#             st.error("❌ Please enter valid numeric values for year and month.")

# elif view == "Yearly Stats":
#     if not stats_year.strip():
#         st.info("🕓 Please enter a year to view temperature statistics.")
#     else:
#         try:
#             y = int(stats_year)
#             st.subheader(f"📊 Monthly Temperature Summary for {y}")
#             df = stats_monthly_for_year(y)
#             if df.empty:
#                 st.warning("No temperature data found for this year.")
#             else:
#                 st.dataframe(df)
#                 st.line_chart(df.set_index("month")[["max_temp", "median_temp", "min_temp"]])
#                 st.download_button(
#                     "⬇️ Download CSV",
#                     df.to_csv(index=False).encode("utf-8"),
#                     file_name=f"weather_stats_{y}.csv"
#                 )
#         except ValueError:
#             st.error("❌ Please enter a valid numeric year.")






# streamlit_app.py
import streamlit as st
import pandas as pd
from modules.preprocess_utils import process_excel
from pathlib import Path
from modules.db_manager import (
    create_table,
    insert_dataframe,
    get_by_date,
    get_by_month_year,
    stats_monthly_for_year,
    DB_PATH
)
import sqlite3

# -----------------------------------------------------------
# Streamlit Page Configuration
# -----------------------------------------------------------
ICON_PATH = Path("pngtree-cloud.png")

st.set_page_config(
    page_title="Delhi Weather Data Explorer",
    page_icon=str(ICON_PATH) if ICON_PATH.exists() else None,
    layout="wide"
)

st.title("🌦 Delhi Weather Data Explorer — 20-Year Historical Dataset")

# -----------------------------------------------------------
# Upload Excel File Section
# -----------------------------------------------------------
uploaded = st.file_uploader("📤 Upload Excel Weather Dataset (.xlsx)", type=["xlsx"])

if uploaded:
    st.info("Processing uploaded Excel file... please wait ⏳")
    try:
        df = process_excel(uploaded)
        create_table()
        insert_dataframe(df, if_exists="replace")
        st.success(f"✅ Dataset processed and stored successfully ({len(df)} rows).")
    except Exception as e:
        st.error(f"❌ Failed to process file: {e}")

# -----------------------------------------------------------
# Ensure Database Exists
# -----------------------------------------------------------
if not Path(DB_PATH).exists():
    st.warning("⚠️ No database found. Please upload an Excel file first.")
    st.stop()

# -----------------------------------------------------------
# Sidebar Options
# -----------------------------------------------------------
with st.sidebar:
    st.header("🔍 Query Weather Data")
    view = st.radio("Choose View", ["By Date", "By Month", "Yearly Stats"])

    # default placeholders, no pre-filled or range limits
    date_input = ""
    year_input = ""
    month_input = ""
    stats_year = ""

    if view == "By Date":
        st.subheader("📅 Search by Date")
        date_input = st.text_input("Enter Date (DD-MM-YYYY)", placeholder="e.g., 12-06-2015")

    elif view == "By Month":
        st.subheader("🗓 Search by Month")
        year_input = st.text_input("Enter Year (e.g., 2015)")
        month_input = st.text_input("Enter Month (1–12)")

    elif view == "Yearly Stats":
        st.subheader("📈 View Yearly Temperature Trends")
        stats_year = st.text_input("Enter Year (e.g., 2018)")

# -----------------------------------------------------------
# Helper: SQLite Query Utility
# -----------------------------------------------------------
def run_query(sql, params=()):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(sql, conn, params=params)
    conn.close()
    return df

st.markdown("---")

# -----------------------------------------------------------
# Main Logic
# -----------------------------------------------------------
if view == "By Date":
    if not date_input.strip():
        st.info("🕓 Please enter a date in the format DD-MM-YYYY to fetch weather details.")
    else:
        try:
            # Convert DD-MM-YYYY → YYYY-MM-DD for querying
            parsed_date = pd.to_datetime(date_input, format="%d-%m-%Y")
            date_query = parsed_date.strftime("%Y-%m-%d")

            st.subheader(f"🌤 Weather Details for {date_input}")
            df = get_by_date(date_query)

            if df.empty:
                st.warning("No data found for this date.")
            else:
                st.dataframe(df)
                st.success(f"✅ {len(df)} record(s) found for {date_input}.")
                st.download_button(
                    "⬇️ Download CSV",
                    df.to_csv(index=False).encode("utf-8"),
                    file_name=f"weather_{date_input.replace('-', '_')}.csv"
                )
        except ValueError:
            st.error("❌ Please enter a valid date in the format DD-MM-YYYY.")

elif view == "By Month":
    if not year_input.strip() or not month_input.strip():
        st.info("🕓 Please enter both year and month to view weather data.")
    else:
        try:
            y, m = int(year_input), int(month_input)
            st.subheader(f"📆 Weather Records for {m:02d}-{y}")
            df = get_by_month_year(y, m)
            if df.empty:
                st.warning("No data found for this month and year.")
            else:
                st.dataframe(df)
                numeric_cols = [c for c in ['temperature', 'humidity', 'pressure', 'heat_index'] if c in df.columns]
                if numeric_cols:
                    st.write("### Summary Statistics:")
                    st.dataframe(df[numeric_cols].describe())
                else:
                    st.info("No numeric weather columns found for summary statistics.")

                st.download_button(
                    "⬇️ Download CSV",
                    df.to_csv(index=False).encode("utf-8"),
                    file_name=f"weather_{m:02d}_{y}.csv"
                )
        except ValueError:
            st.error("❌ Please enter valid numeric values for year and month.")

elif view == "Yearly Stats":
    if not stats_year.strip():
        st.info("🕓 Please enter a year to view temperature statistics.")
    else:
        try:
            y = int(stats_year)
            st.subheader(f"📊 Monthly Temperature Summary for {y}")
            df = stats_monthly_for_year(y)
            if df.empty:
                st.warning("No temperature data found for this year.")
            else:
                st.dataframe(df)
                st.line_chart(df.set_index("month")[["max_temp", "median_temp", "min_temp"]])
                st.download_button(
                    "⬇️ Download CSV",
                    df.to_csv(index=False).encode("utf-8"),
                    file_name=f"weather_stats_{y}.csv"
                )
        except ValueError:
            st.error("❌ Please enter a valid numeric year.")
