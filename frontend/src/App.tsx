import React, { useState, useEffect } from 'react';

interface WeatherData {
  date: string;
  weather_condition: string;
  temperature: number;
  humidity: number;
  pressure: number;
  month?: number;
  max_temp?: number;
  median_temp?: number;
  min_temp?: number;
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

  return (
    <div className="app-container">
      <div className="main-container">
        <div className="card">
          <div className="header">
            <h1>🌦 Delhi Weather Dashboard</h1>
            <p>Query by Date, Month, or Year</p>
          </div>
          
          <div className="search-form">
            <div className="form-group">
              <input
                type="date"
                value={date}
                onChange={(e) => setDate(e.target.value)}
                className="form-input"
                placeholder="Select date"
              />
            </div>
            <div className="form-group">
              <input
                type="number"
                value={year}
                onChange={(e) => setYear(e.target.value)}
                className="form-input"
                placeholder="Year (e.g. 2015)"
              />
            </div>
            <div className="form-group">
              <input
                type="number"
                value={month}
                onChange={(e) => setMonth(e.target.value)}
                className="form-input"
                placeholder="Month (1-12)"
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
                {loading ? '🔄' : '🔍'} Search
              </button>
              <button
                onClick={clearSearch}
                className="btn btn-secondary"
              >
                Clear
              </button>
            </div>
          </div>

          {message && (
            <div className="alert alert-info">
              {message}
            </div>
          )}
        </div>

        {data.length > 0 && (
          <div className="card">
            <div className="results-header">
              <h2 className="results-title">
                Results ({data.length} rows)
              </h2>
            </div>
            
            <div className="table-container">
              <table className="table">
                <thead>
                  <tr>
                    {Object.keys(data[0]).map((key) => (
                      <th key={key}>
                        {key.replace(/_/g, ' ').toUpperCase()}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {data.map((row, index) => (
                    <tr key={index}>
                      {Object.values(row).map((value, i) => (
                        <td key={i}>
                          {value !== null && value !== undefined ? String(value) : 'N/A'}
                        </td>
                      ))}
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