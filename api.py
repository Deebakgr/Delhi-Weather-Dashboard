# # api.py
# from flask import Flask, request, render_template_string, jsonify
# from flask_cors import CORS
# from modules.db_manager import (
#     create_table,
#     insert_dataframe,
#     get_by_date,
#     get_by_month_year,
#     stats_monthly_for_year,
#     DB_PATH,
# )
# from modules.preprocess_utils import process_excel
# from pathlib import Path
# import pandas as pd

# app = Flask(__name__)
# CORS(app)

# # -----------------------------------------------------------
# # HTML Template (Bootstrap + Embedded CSS)
# # -----------------------------------------------------------
# HTML_TEMPLATE = """
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Delhi Weather Data Dashboard</title>
#     <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
#     <style>
#         body {
#             background: linear-gradient(135deg, #E8F0F2, #D9E8E4);
#             font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
#         }
#         .container {
#             max-width: 1000px;
#             margin-top: 40px;
#             background-color: white;
#             padding: 30px;
#             border-radius: 15px;
#             box-shadow: 0 0 15px rgba(0,0,0,0.1);
#         }
#         h1, h3 {
#             text-align: center;
#             color: #2c3e50;
#         }
#         table {
#             border-collapse: collapse;
#             width: 100%;
#         }
#         th {
#             background-color: #2c3e50;
#             color: #fff;
#             text-align: center;
#         }
#         td {
#             text-align: center;
#         }
#         tr:nth-child(even) {
#             background-color: #f8f9fa;
#         }
#         .footer {
#             margin-top: 30px;
#             text-align: center;
#             color: #888;
#         }
#         .disabled-section {
#             opacity: 0.5;
#             pointer-events: none;
#         }
#     </style>
# </head>
# <body>
# <div class="container">
#     <h1>🌦 Delhi Weather Data Dashboard</h1>
#     <p class="text-center text-muted">Upload Excel → Query Data by Date, Month, or Year</p>
#     <hr>

#     <!-- Upload Section -->
#     <form method="POST" action="/upload" enctype="multipart/form-data" class="mb-4">
#         <div class="input-group">
#             <input type="file" name="file" class="form-control" accept=".xlsx" required>
#             <button class="btn btn-primary" type="submit">📤 Upload Excel</button>
#         </div>
#     </form>

#     {% if not db_exists %}
#         <div class="alert alert-warning text-center">
#             ⚠️ Please upload an Excel file to activate the dashboard.
#         </div>
#     {% else %}
#         <!-- Query Section -->
#         <form method="GET" action="/dashboard">
#             <div class="row mb-3">
#                 <div class="col-md-4">
#                     <input type="date" name="date" class="form-control" placeholder="YYYY-MM-DD">
#                 </div>
#                 <div class="col-md-3">
#                     <input type="number" name="year" class="form-control" placeholder="Year (e.g. 2015)">
#                 </div>
#                 <div class="col-md-3">
#                     <input type="number" name="month" class="form-control" placeholder="Month (1-12)">
#                 </div>
#                 <div class="col-md-2">
#                     <button class="btn btn-success w-100" type="submit">🔍 Search</button>
#                 </div>
#             </div>
#         </form>

#         {% if message %}
#             <div class="alert alert-info text-center">{{ message }}</div>
#         {% endif %}

#         {% if data %}
#             <h3>Results ({{ rows }} rows)</h3>
#             <div class="table-responsive">
#                 <table class="table table-bordered table-striped">
#                     <thead>
#                         <tr>
#                             {% for col in columns %}
#                                 <th>{{ col }}</th>
#                             {% endfor %}
#                         </tr>
#                     </thead>
#                     <tbody>
#                         {% for row in data %}
#                             <tr>
#                                 {% for col in columns %}
#                                     <td>{{ row[col] }}</td>
#                                 {% endfor %}
#                             </tr>
#                         {% endfor %}
#                     </tbody>
#                 </table>
#             </div>
#         {% endif %}
#     {% endif %}

#     <div class="footer">
#         <hr>
#         <p>JSON API Endpoints: 
#         <a href="/weather?year=2015&month=1">/weather</a> |
#         <a href="/temperature_stats?year=2015">/temperature_stats</a>
#         </p>
#     </div>
# </div>
# </body>
# </html>
# """

# # -----------------------------------------------------------
# # Routes
# # -----------------------------------------------------------

# @app.route("/", methods=["GET"])
# def home():
#     """Main dashboard page."""
#     db_exists = Path(DB_PATH).exists()
#     return render_template_string(HTML_TEMPLATE, db_exists=db_exists, message=None, data=None)

# @app.route("/upload", methods=["POST"])
# def upload_excel():
#     """Handle Excel file upload and insert into DB."""
#     file = request.files.get("file")
#     if not file:
#         return render_template_string(HTML_TEMPLATE, db_exists=False, message="❌ No file uploaded", data=None)

#     try:
#         df = process_excel(file)
#         create_table()
#         insert_dataframe(df, if_exists="replace")
#         msg = f"✅ Uploaded and stored {len(df)} records successfully."
#         return render_template_string(HTML_TEMPLATE, db_exists=True, message=msg, data=None)
#     except Exception as e:
#         return render_template_string(HTML_TEMPLATE, db_exists=False, message=f"❌ Error processing file: {e}", data=None)

# @app.route("/dashboard", methods=["GET"])
# def dashboard():
#     """Query weather data by date, month, or year."""
#     db_exists = Path(DB_PATH).exists()
#     if not db_exists:
#         return render_template_string(HTML_TEMPLATE, db_exists=False, message=None, data=None)

#     date = request.args.get("date")
#     year = request.args.get("year", type=int)
#     month = request.args.get("month", type=int)

#     df = pd.DataFrame()
#     message = None

#     if date:
#         df = get_by_date(date)
#         message = f"Showing results for date: {date}"
#     elif year and month:
#         df = get_by_month_year(year, month)
#         message = f"Showing results for {year}-{month:02d}"
#     elif year:
#         df = stats_monthly_for_year(year)
#         message = f"Monthly temperature stats for {year}"
#     else:
#         message = "Enter a date, month, or year to view data."

#     if df.empty:
#         return render_template_string(HTML_TEMPLATE, db_exists=True, message="No data found.", data=None)

#     return render_template_string(
#         HTML_TEMPLATE,
#         db_exists=True,
#         message=message,
#         data=df.to_dict(orient="records"),
#         columns=df.columns,
#         rows=len(df)
#     )

# # -----------------------------------------------------------
# # API Endpoints (JSON)
# # -----------------------------------------------------------

# @app.route("/weather", methods=["GET"])
# def weather_json():
#     """Fetch weather data via JSON."""
#     if not Path(DB_PATH).exists():
#         return jsonify({"error": "Database not found. Please upload Excel file first."}), 400

#     date = request.args.get("date")
#     year = request.args.get("year", type=int)
#     month = request.args.get("month", type=int)

#     if date:
#         df = get_by_date(date)
#     elif year and month:
#         df = get_by_month_year(year, month)
#     elif year:
#         df = stats_monthly_for_year(year)
#     else:
#         return jsonify({"error": "Provide ?date=YYYY-MM-DD or ?year=YYYY&month=MM"}), 400

#     if df.empty:
#         return jsonify({"message": "No data found"}), 404
#     return jsonify(df.to_dict(orient="records"))

# @app.route("/temperature_stats", methods=["GET"])
# def temperature_stats_json():
#     """Return temperature stats by year."""
#     if not Path(DB_PATH).exists():
#         return jsonify({"error": "Database not found. Please upload Excel file first."}), 400

#     year = request.args.get("year", type=int)
#     if not year:
#         return jsonify({"error": "Provide ?year=YYYY"}), 400

#     df = stats_monthly_for_year(year)
#     if df.empty:
#         return jsonify({"message": "No data found"}), 404
#     return jsonify({"year": year, "monthly_stats": df.to_dict(orient="records")})

# # -----------------------------------------------------------
# # Run
# # -----------------------------------------------------------
# if __name__ == "__main__":
#     app.run(debug=True, port=5000)




# api.py
from flask import Flask, request, render_template_string, jsonify, Response, send_file
from flask_cors import CORS
from modules.db_manager import (
    create_table, insert_dataframe, get_by_date,
    get_by_month_year, stats_monthly_for_year, DB_PATH
)
from modules.preprocess_utils import process_excel
from pathlib import Path
import pandas as pd
import io

app = Flask(__name__)
CORS(app)

# ----------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------
EXCEL_PATH = Path("testset.xlsx")
ICON_PATH = Path("pngtree-cloud.png")
DATA_LOADED = False
LAST_QUERY_DF = None

# ----------------------------------------------------------------
# HTML Template
# ----------------------------------------------------------------
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Delhi Weather Dashboard</title>
    <link rel="icon" href="/icon.png?ts={{ timestamp }}" type="image/png">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #E8F0F2, #D9E8E4);
            font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
        }
        .container {
            max-width: 1000px;
            margin-top: 40px;
            background-color: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 0 15px rgba(0,0,0,0.1);
        }
        h1, h3 {
            text-align: center;
            color: #2c3e50;
        }
        th {
            background-color: #2c3e50;
            color: #fff;
            text-align: center;
        }
        td {
            text-align: center;
        }
        tr:nth-child(even) {
            background-color: #f8f9fa;
        }
        .download-btn {
            text-align: right;
            margin-bottom: 15px;
        }
    </style>
</head>
<body>
<div class="container">
    <h1>🌦 Delhi Weather Data Dashboard</h1>
    <p class="text-center text-muted">Query by Date, Month, or Year</p>
    <hr>

    {% if not data_loaded %}
        <div class="alert alert-danger text-center">
            ❌ Dataset not found. Please ensure <b>testset.xlsx</b> exists and restart the server.
        </div>
    {% else %}
        <form method="GET" action="/dashboard">
            <div class="row mb-3">
                <div class="col-md-4">
                    <input type="date" name="date" class="form-control" placeholder="YYYY-MM-DD">
                </div>
                <div class="col-md-3">
                    <input type="number" name="year" class="form-control" placeholder="Year (e.g. 2015)">
                </div>
                <div class="col-md-3">
                    <input type="number" name="month" class="form-control" placeholder="Month (1-12)">
                </div>
                <div class="col-md-2">
                    <button class="btn btn-success w-100" type="submit">🔍 Search</button>
                </div>
            </div>
        </form>

        {% if message %}
            <div class="alert alert-info text-center">{{ message }}</div>
        {% endif %}

        {% if data %}
            <div class="download-btn">
                <a href="/download_csv" class="btn btn-outline-primary btn-sm">⬇️ Download CSV</a>
            </div>
            <h3>Results ({{ rows }} rows)</h3>
            <div class="table-responsive">
                <table class="table table-bordered table-striped">
                    <thead>
                        <tr>
                            {% for col in columns %}
                                <th>{{ col }}</th>
                            {% endfor %}
                        </tr>
                    </thead>
                    <tbody>
                        {% for row in data %}
                            <tr>
                                {% for col in columns %}
                                    <td>{{ row[col] }}</td>
                                {% endfor %}
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        {% endif %}
    {% endif %}
</div>
</body>
</html>
"""

# ----------------------------------------------------------------
# Load Excel on Startup
# ----------------------------------------------------------------
def load_excel_to_db():
    global DATA_LOADED
    if not EXCEL_PATH.exists():
        print("❌ Excel file not found! Please place testset.xlsx in the project directory.")
        DATA_LOADED = False
        return
    try:
        print(f"📂 Loading dataset from {EXCEL_PATH} ...")
        df = process_excel(EXCEL_PATH)
        create_table()
        insert_dataframe(df, if_exists="replace")
        DATA_LOADED = True
        print(f"✅ Loaded {len(df)} records from {EXCEL_PATH}")
    except Exception as e:
        print(f"❌ Error loading Excel: {e}")
        DATA_LOADED = False

# ----------------------------------------------------------------
# Routes
# ----------------------------------------------------------------
@app.route("/icon.png")
def serve_icon():
    """Serve the tab icon."""
    if ICON_PATH.exists():
        return send_file(ICON_PATH, mimetype="image/png")
    return "Icon not found", 404

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE, data_loaded=DATA_LOADED, message=None, data=None)

@app.route("/dashboard")
def dashboard():
    global LAST_QUERY_DF
    if not DATA_LOADED:
        return render_template_string(HTML_TEMPLATE, data_loaded=False, message=None, data=None)

    date = request.args.get("date")
    year = request.args.get("year", type=int)
    month = request.args.get("month", type=int)

    df = pd.DataFrame()
    message = None

    if date:
        df = get_by_date(date)
        message = f"Showing results for date: {date}"
    elif year and month:
        df = get_by_month_year(year, month)
        message = f"Showing results for {year}-{month:02d}"
    elif year:
        df = stats_monthly_for_year(year)
        message = f"Monthly temperature stats for {year}"
    else:
        message = "Enter a date, month, or year to view data."

    if df.empty:
        return render_template_string(HTML_TEMPLATE, data_loaded=True, message="No data found.", data=None)

    LAST_QUERY_DF = df.copy()
    return render_template_string(
        HTML_TEMPLATE,
        data_loaded=True,
        message=message,
        data=df.to_dict(orient="records"),
        columns=df.columns,
        rows=len(df)
    )

@app.route("/download_csv")
def download_csv():
    global LAST_QUERY_DF
    if LAST_QUERY_DF is None or LAST_QUERY_DF.empty:
        return "❌ No data available for download.", 400

    buffer = io.StringIO()
    LAST_QUERY_DF.to_csv(buffer, index=False)
    buffer.seek(0)
    return Response(
        buffer.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=weather_query.csv"},
    )

# ----------------------------------------------------------------
# Run App
# ----------------------------------------------------------------
if __name__ == "__main__":
    load_excel_to_db()
    app.run(debug=True, port=5000)
