# Weather Dashboard

A React frontend with Tailwind CSS and Flask backend for weather data analysis.

## Setup Instructions

### Backend (Flask API)
1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask server:
   ```bash
   python app.py
   ```
   Server runs on http://localhost:5000

### Frontend (React + Tailwind)
1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```
   App runs on http://localhost:3000

## API Endpoints

- `GET /api/status` - Check if data is loaded
- `GET /api/weather` - Get weather data
  - Query params: `date`, `year`, `month`
  - Examples:
    - `/api/weather?date=2015-01-01`
    - `/api/weather?year=2015&month=1`
    - `/api/weather?year=2015`

## Features

- Search by specific date
- Search by month and year
- Search by year (returns monthly stats)
- Responsive design with Tailwind CSS
- Clean table display of results