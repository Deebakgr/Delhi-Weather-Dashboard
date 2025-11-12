# 🌦 Delhi Weather Dashboard

## 📘 Overview
This project provides a complete **Weather Data Analysis System** that allows users to upload, process, and analyze 20 years of Delhi’s weather data.  
It includes both a **Streamlit Dashboard** and a **Flask API** interface that share the same underlying SQLite database.

Users can view weather details by **date**, **month**, or **yearly summaries**, and download query results as CSV files.  
The project is fully modular, fast, and easily extensible.

---

## 🧩 Features

### 🔹 Data Processing & Storage
- Reads Excel weather datasets (`.xlsx`) and preprocesses them.
- Automatically detects and normalizes date/time columns.
- Cleans invalid readings (e.g., `-9999`) and replaces them with `NaN`.
- Extracts useful features: `year`, `month`, `day`.
- Stores processed data in an **SQLite database (`weather.db`)** for efficient access.

### 🔹 Streamlit Dashboard
- Upload and process new Excel datasets directly from the UI.
- Query weather details:
  - By **Date** → Enter date in `DD-MM-YYYY` format.
  - By **Month** → View all records for a given month & year.
  - By **Yearly Stats** → Get high, median, and low temperatures per month.
- Download query results as CSV.
- Responsive and minimal design.
- Fast performance using Streamlit’s caching system.
- Custom PNG browser tab icon (`pngtree-cloud.png`).

### 🔹 Flask API Interface
- Beautiful web interface built using **Flask + Bootstrap**.
- Automatically loads dataset on startup (`testset.xlsx`).
- Query weather data by date, month, or year.
- Download search results as CSV.
- Shares the same database as Streamlit (no duplication).
- Automatically updates tab icon when changed (cache-busting feature).

---

## 🧱 Project Structure


weather_project/
├── api.py # Flask web API
├── streamlit_app.py # Streamlit dashboard
├── icon.png / pngtree-cloud.png # Browser tab icon
├── testset.xlsx # Example Excel dataset
├── weather.db # SQLite database (auto-created)
├── modules/
│ ├── db_manager.py # Database operations
│ └── preprocess_utils.py # Data preprocessing
└── README.md # Project documentation

yaml
Copy code

---

## ⚙️ Setup Instructions

### 🔸 Prerequisites
Ensure you have **Python 3.9+** installed, then install dependencies:

```bash
pip install -r requirements.txt
If you don’t have a requirements.txt, create one with:

bash
Copy code
pip install streamlit flask pandas numpy openpyxl
🚀 Running the Project
▶️ Run Streamlit App
bash
Copy code
streamlit run streamlit_app.py
Then open:
http://localhost:8501

▶️ Run Flask API
bash
Copy code
python api.py
Then open:
http://localhost:5000

