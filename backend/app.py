from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.db_manager import (
    create_table, insert_dataframe, get_by_date,
    get_by_month_year, stats_monthly_for_year, DB_PATH
)
from modules.preprocess_utils import process_excel
from pathlib import Path
import sqlite3

app = Flask(__name__)
CORS(app)

EXCEL_PATH = Path("../testset.xlsx")
DATA_LOADED = False

def load_excel_to_db():
    global DATA_LOADED
    if not EXCEL_PATH.exists():
        print("❌ Excel file not found!")
        DATA_LOADED = False
        return
    try:
        print(f"📂 Loading dataset from {EXCEL_PATH}...")
        df = process_excel(EXCEL_PATH)
        create_table()
        insert_dataframe(df, if_exists="replace")
        DATA_LOADED = True
        print(f"✅ Loaded {len(df)} records")
    except Exception as e:
        print(f"❌ Error loading Excel: {e}")
        DATA_LOADED = False

@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({"data_loaded": DATA_LOADED})

@app.route("/api/weather", methods=["GET"])
def weather_data():
    try:
        if not Path(DB_PATH).exists():
            return jsonify({"error": "Database not found"}), 400

        date = request.args.get("date")
        year = request.args.get("year", type=int)
        month = request.args.get("month", type=int)

        print(f"Request params - date: {date}, year: {year}, month: {month}")

        if date:
            df = get_by_date(date)
            message = f"Results for date: {date}"
        elif year and month:
            df = get_by_month_year(year, month)
            message = f"Results for {year}-{month:02d}"
            print(f"Found {len(df)} records for {year}-{month}")
        elif year:
            df = stats_monthly_for_year(year)
            message = f"Monthly stats for {year}"
        else:
            return jsonify({"error": "Provide date, year, or year+month"}), 400

        # Handle NaN values and format datetime
        df = df.fillna("N/A")
        
        # Format datetime column if it exists
        if 'datetime' in df.columns:
            df['datetime'] = pd.to_datetime(df['datetime']).dt.strftime('%d-%m-%Y (%I:%M %p)')
        
        if df.empty:
            return jsonify({"message": "No data found", "data": []}), 200

        return jsonify({
            "message": message,
            "data": df.to_dict(orient="records"),
            "count": len(df)
        })
    except Exception as e:
        print(f"API Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    load_excel_to_db()
    app.run(debug=True, port=5000)