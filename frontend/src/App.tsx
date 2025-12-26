import React, { useState, useEffect } from 'react';

interface WeatherData {
  datetime: string;
  weather_condition: string;
  temperature: number | string;
  humidity: number | string;
  pressure: number | string;
  month?: number;
  max_temp?: number | string;
  median_temp?: number | string;
  min_temp?: number | string;
}

interface ApiResponse {
  message: string;
  data: WeatherData[];
  count: number;
  error?: string;
}

const App: React.FC = () => {
  const [data, setData] = useState<WeatherData[]>([]);
  const [message, setMessage] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [dataLoaded, setDataLoaded] = useState<boolean>(false);
  
  const [date, setDate] = useState<string>('');
  const [year, setYear] = useState<string>('');
  const [month, setMonth] = useState<string>('');

  useEffect(() => {
    checkStatus();
  }, []);

  const checkStatus = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/status');
      const result = await response.json();
      setDataLoaded(result.data_loaded);
    } catch (error) {
      console.error('Error checking status:', error);
    }
  };

  const searchWeather = async () => {
    if (!date && !year) {
      setMessage('Please enter a date or year');
      return;
    }

    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (date) params.append('date', date);
      if (year) params.append('year', year);
      if (month) params.append('month', month);

      const response = await fetch(`http://localhost:5000/api/weather?${params}`);
      const result: ApiResponse = await response.json();

      if (response.ok) {
        setData(result.data);
        setMessage(result.message);
      } else {
        setMessage(result.error || 'Error fetching data');
        setData([]);
      }
    } catch (error) {
      setMessage('Error connecting to server');
      setData([]);
    } finally {
      setLoading(false);
    }
  };

  const clearSearch = () => {
    setDate('');
    setYear('');
    setMonth('');
    setData([]);
    setMessage('');
  };

  const getWeatherIcon = (condition: string) => {
    if (!condition || condition === 'N/A') return '🌤️';
    const cond = condition.toLowerCase();
    if (cond.includes('clear') || cond.includes('sunny')) return '☀️';
    if (cond.includes('cloud')) return '☁️';
    if (cond.includes('rain')) return '🌧️';
    if (cond.includes('storm')) return '⛈️';
    if (cond.includes('snow')) return '❄️';
    if (cond.includes('fog') || cond.includes('mist')) return '🌫️';
    return '🌤️';
  };

  const formatValue = (value: any, type: string) => {
    if (value === null || value === undefined || value === 'N/A') return 'N/A';
    
    switch (type) {
      case 'temperature':
        return `${value}°C`;
      case 'humidity':
        return `${value}%`;
      case 'pressure':
        return `${value} hPa`;
      default:
        return String(value);
    }
  };

  const getStatsFromData = () => {
    if (!data.length) return null;
    
    const temps = data.filter(d => d.temperature && d.temperature !== 'N/A').map(d => Number(d.temperature));
    const humidities = data.filter(d => d.humidity && d.humidity !== 'N/A').map(d => Number(d.humidity));
    
    return {
      totalRecords: data.length,
      avgTemp: temps.length ? (temps.reduce((a, b) => a + b, 0) / temps.length).toFixed(1) : 'N/A',
      maxTemp: temps.length ? Math.max(...temps) : 'N/A',
      minTemp: temps.length ? Math.min(...temps) : 'N/A',
      avgHumidity: humidities.length ? (humidities.reduce((a, b) => a + b, 0) / humidities.length).toFixed(1) : 'N/A'
    };
  };

  if (!dataLoaded) {
    return (
      <div className="error-container">
        <div className="error-card">
          <div className="error-icon">❌</div>
          <h1 className="error-title">Dataset Not Found</h1>
          <p className="error-message">Please ensure testset.xlsx exists and restart the server.</p>
        </div>
      </div>
    );
  }

  const stats = getStatsFromData();

  return (
    <div className="app-container">
      <div className="main-container">
        <div className="header">
          <h1>🌦️ Delhi Weather Dashboard</h1>
          <p>Weather Data Analytics Platform</p>
        </div>
        
        <div className="dashboard-grid">
          <div className="search-panel">
            <h2 className="search-title">
              <span>🔍</span> Search Weather Data
            </h2>
            
            <div className="search-form">
              <div className="form-group">
                <label className="form-label">Select Date</label>
                <input
                  type="date"
                  value={date}
                  onChange={(e) => setDate(e.target.value)}
                  className="form-input"
                  placeholder="Select specific date"
                />
              </div>
              
              <div className="form-group">
                <label className="form-label">Year</label>
                <input
                  type="number"
                  value={year}
                  onChange={(e) => setYear(e.target.value)}
                  className="form-input"
                  placeholder="e.g. 2015"
                  min="1996"
                  max="2030"
                />
              </div>
              
              <div className="form-group">
                <label className="form-label">Month</label>
                <input
                  type="number"
                  value={month}
                  onChange={(e) => setMonth(e.target.value)}
                  className="form-input"
                  placeholder="1-12"
                  min="1"
                  max="12"
                />
              </div>
              
              <div className="button-group">
                <button
                  onClick={searchWeather}
                  disabled={loading}
                  className="btn btn-primary"
                >
                  {loading ? (
                    <><span className="loading-spinner"></span> Searching...</>
                  ) : (
                    <>🔍 Search</>
                  )}
                </button>
                <button
                  onClick={clearSearch}
                  className="btn btn-secondary"
                >
                  🗑️ Clear
                </button>
              </div>
            </div>

            {message && (
              <div className={`alert ${message.includes('Error') ? 'alert-danger' : 'alert-info'}`}>
                {message}
              </div>
            )}
          </div>

          {stats && (
            <div className="stats-panel">
              <h2 className="stats-title">📊 Quick Statistics</h2>
              <div className="stats-grid">
                <div className="stat-card">
                  <div className="stat-value">{stats.totalRecords}</div>
                  <div className="stat-label">Total Records</div>
                </div>
                <div className="stat-card">
                  <div className="stat-value">{stats.avgTemp}°</div>
                  <div className="stat-label">Avg Temperature</div>
                </div>
                <div className="stat-card">
                  <div className="stat-value">{stats.maxTemp}°</div>
                  <div className="stat-label">Max Temperature</div>
                </div>
                <div className="stat-card">
                  <div className="stat-value">{stats.minTemp}°</div>
                  <div className="stat-label">Min Temperature</div>
                </div>
                <div className="stat-card">
                  <div className="stat-value">{stats.avgHumidity}%</div>
                  <div className="stat-label">Avg Humidity</div>
                </div>
              </div>
            </div>
          )}
        </div>

        {data.length > 0 && (
          <div className="results-container">
            <div className="results-header">
              <h2 className="results-title">Weather Data Results</h2>
              <div className="results-count">{data.length} records found</div>
            </div>
            
            <div className="table-container">
              <table className="table">
                <thead>
                  <tr>
                    <th>Date & Time</th>
                    <th>Weather</th>
                    <th>Temperature</th>
                    <th>Humidity</th>
                    <th>Pressure</th>
                  </tr>
                </thead>
                <tbody>
                  {data.map((row, index) => (
                    <tr key={index}>
                      <td>{row.datetime || 'N/A'}</td>
                      <td>
                        <span className="weather-icon">{getWeatherIcon(row.weather_condition)}</span>
                        {row.weather_condition || 'N/A'}
                      </td>
                      <td className="temperature">{formatValue(row.temperature, 'temperature')}</td>
                      <td className="humidity">{formatValue(row.humidity, 'humidity')}</td>
                      <td className="pressure">{formatValue(row.pressure, 'pressure')}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default App;