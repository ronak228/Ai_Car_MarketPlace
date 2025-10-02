import React, { useState, useEffect } from 'react';
import { Line, Pie, Bar, Doughnut } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  BarElement,
} from 'chart.js';

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  BarElement
);

const MarketTrends = () => {
  const [marketData, setMarketData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');

  // API base URL - adjust this to match your Flask server
  const API_BASE_URL = ''; // Use proxy to Flask API endpoint

  useEffect(() => {
    loadMarketData();
  }, []);

  const loadMarketData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Try multiple API base URLs
      const apiUrls = [
        'http://localhost:5000', // Direct connection
        'http://127.0.0.1:5000', // Alternative localhost
        '' // Proxy (if configured)
      ];

      let workingUrl = null;
      
      // Test which URL works
      for (const baseUrl of apiUrls) {
        try {
          const testResponse = await fetch(`${baseUrl}/api/health`, {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
            },
          });
          if (testResponse.ok) {
            workingUrl = baseUrl;
            console.log(`✅ Connected to Flask server at: ${baseUrl || 'proxy'}`);
            break;
          }
        } catch (e) {
          console.log(`❌ Failed to connect to: ${baseUrl || 'proxy'}`);
          continue;
        }
      }

      if (!workingUrl) {
        throw new Error('Cannot connect to Flask server. Please ensure it is running on port 5000.');
      }

      // Load all market data in parallel
      const [overviewRes, companiesRes, fuelRes, citiesRes, predictionsRes] = await Promise.all([
        fetch(`${workingUrl}/api/market-overview`),
        fetch(`${workingUrl}/api/company-trends`),
        fetch(`${workingUrl}/api/fuel-type-analysis`),
        fetch(`${workingUrl}/api/city-market-analysis`),
        fetch(`${workingUrl}/api/market-predictions`)
      ]);

      // Check if all responses are OK
      if (!overviewRes.ok || !companiesRes.ok || !fuelRes.ok || !citiesRes.ok || !predictionsRes.ok) {
        throw new Error('One or more API endpoints failed');
      }

      const overview = await overviewRes.json();
      const companies = await companiesRes.json();
      const fuel = await fuelRes.json();
      const cities = await citiesRes.json();
      const predictions = await predictionsRes.json();

      setMarketData({
        overview: overview.data,
        companies: companies.data,
        fuel: fuel.data,
        cities: cities.data,
        predictions: predictions.data
      });

      console.log('✅ Market data loaded successfully');

    } catch (err) {
      console.error('Error loading market data:', err);
      setError(`Failed to load market trends data. Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 0
    }).format(amount);
  };

  const formatNumber = (num) => {
    return new Intl.NumberFormat('en-IN').format(num);
  };

  // Chart configurations
  const getMarketShareChartData = () => {
    if (!marketData?.companies) return null;

    const topCompanies = Object.entries(marketData.companies)
      .sort(([,a], [,b]) => b.stats.market_share - a.stats.market_share)
      .slice(0, 8);

    return {
      labels: topCompanies.map(([name]) => name),
      datasets: [{
        data: topCompanies.map(([,data]) => data.stats.market_share),
        backgroundColor: [
          '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0',
          '#9966FF', '#FF9F40', '#FF6384', '#C9CBCF'
        ],
        borderWidth: 2,
        borderColor: '#fff'
      }]
    };
  };

  const getFuelTypeChartData = () => {
    if (!marketData?.fuel) return null;

    return {
      labels: Object.keys(marketData.fuel),
      datasets: [{
        label: 'Market Share (%)',
        data: Object.values(marketData.fuel).map(fuel => fuel.market_share),
        backgroundColor: ['#36A2EB', '#FF6384', '#FFCE56', '#4BC0C0'],
        borderColor: ['#36A2EB', '#FF6384', '#FFCE56', '#4BC0C0'],
        borderWidth: 1
      }]
    };
  };

  const getCityChartData = () => {
    if (!marketData?.cities) return null;

    const cities = Object.entries(marketData.cities)
      .sort(([,a], [,b]) => b.total_listings - a.total_listings)
      .slice(0, 6);

    return {
      labels: cities.map(([name]) => name),
      datasets: [{
        label: 'Total Listings',
        data: cities.map(([,data]) => data.total_listings),
        backgroundColor: 'rgba(255, 193, 7, 0.7)',
        borderColor: 'rgb(255, 193, 7)',
        borderWidth: 1
      }]
    };
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'bottom'
      }
    }
  };

  if (loading) {
    return (
      <div className="container mt-4">
        <div className="text-center">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <h4 className="mt-3">Loading Market Trends...</h4>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mt-4">
        <div className="alert alert-danger">
          <h4 className="alert-heading">Error Loading Market Trends</h4>
          <p>{error}</p>
          <button className="btn btn-outline-danger" onClick={loadMarketData}>
            Retry
          </button>
        </div>
      </div>
    );
  }

  if (!marketData) {
    return (
      <div className="container mt-4">
        <div className="alert alert-warning">
          No market data available.
        </div>
      </div>
    );
  }

  return (
    <div className="container-fluid mt-4">
      {/* Header */}
      <div className="row mb-4">
        <div className="col-12">
          <div className="d-flex justify-content-between align-items-center">
            <div>
              <h2 className="text-primary">
                <i className="fas fa-chart-line me-2"></i>
                Market Trends Dashboard
              </h2>
              <p className="text-muted">Real-time automotive market insights and analytics</p>
            </div>
            <button className="btn btn-outline-primary" onClick={loadMarketData}>
              <i className="fas fa-sync-alt me-1"></i>
              Refresh Data
            </button>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="row mb-4">
        <div className="col-12">
          <div className="btn-group" role="group">
            <button
              type="button"
              className={`btn ${activeTab === 'overview' ? 'btn-primary' : 'btn-outline-primary'}`}
              onClick={() => setActiveTab('overview')}
            >
              <i className="fas fa-tachometer-alt me-1"></i>
              Overview
            </button>
            <button
              type="button"
              className={`btn ${activeTab === 'companies' ? 'btn-primary' : 'btn-outline-primary'}`}
              onClick={() => setActiveTab('companies')}
            >
              <i className="fas fa-building me-1"></i>
              Companies
            </button>
            <button
              type="button"
              className={`btn ${activeTab === 'analytics' ? 'btn-primary' : 'btn-outline-primary'}`}
              onClick={() => setActiveTab('analytics')}
            >
              <i className="fas fa-chart-bar me-1"></i>
              Analytics
            </button>
            <button
              type="button"
              className={`btn ${activeTab === 'predictions' ? 'btn-primary' : 'btn-outline-primary'}`}
              onClick={() => setActiveTab('predictions')}
            >
              <i className="fas fa-crystal-ball me-1"></i>
              Predictions
            </button>
          </div>
        </div>
      </div>

      {/* Overview Tab */}
      {activeTab === 'overview' && (
        <>
          {/* KPI Cards */}
          <div className="row mb-4">
            <div className="col-md-3">
              <div className="card text-center border-primary">
                <div className="card-body">
                  <i className="fas fa-car fa-2x text-primary mb-2"></i>
                  <h3 className="text-primary">{formatNumber(marketData.overview.total_listings)}</h3>
                  <p className="text-muted mb-0">Total Listings</p>
                </div>
              </div>
            </div>
            <div className="col-md-3">
              <div className="card text-center border-success">
                <div className="card-body">
                  <i className="fas fa-rupee-sign fa-2x text-success mb-2"></i>
                  <h3 className="text-success">{formatCurrency(marketData.overview.average_price)}</h3>
                  <p className="text-muted mb-0">Average Price</p>
                </div>
              </div>
            </div>
            <div className="col-md-3">
              <div className="card text-center border-info">
                <div className="card-body">
                  <i className="fas fa-building fa-2x text-info mb-2"></i>
                  <h3 className="text-info">{marketData.overview.total_companies}</h3>
                  <p className="text-muted mb-0">Companies</p>
                </div>
              </div>
            </div>
            <div className="col-md-3">
              <div className="card text-center border-warning">
                <div className="card-body">
                  <i className="fas fa-calendar fa-2x text-warning mb-2"></i>
                  <h3 className="text-warning">{marketData.overview.average_age.toFixed(1)} years</h3>
                  <p className="text-muted mb-0">Average Age</p>
                </div>
              </div>
            </div>
          </div>

          {/* Charts */}
          <div className="row">
            <div className="col-lg-6 mb-4">
              <div className="card">
                <div className="card-header">
                  <h5><i className="fas fa-chart-pie me-2"></i>Market Share by Company</h5>
                </div>
                <div className="card-body">
                  {getMarketShareChartData() && (
                    <Doughnut data={getMarketShareChartData()} options={chartOptions} />
                  )}
                </div>
              </div>
            </div>
            <div className="col-lg-6 mb-4">
              <div className="card">
                <div className="card-header">
                  <h5><i className="fas fa-gas-pump me-2"></i>Fuel Type Distribution</h5>
                </div>
                <div className="card-body">
                  {getFuelTypeChartData() && (
                    <Bar data={getFuelTypeChartData()} options={chartOptions} />
                  )}
                </div>
              </div>
            </div>
          </div>

          <div className="row">
            <div className="col-lg-12 mb-4">
              <div className="card">
                <div className="card-header">
                  <h5><i className="fas fa-city me-2"></i>Top Cities by Volume</h5>
                </div>
                <div className="card-body">
                  {getCityChartData() && (
                    <Bar data={getCityChartData()} options={chartOptions} />
                  )}
                </div>
              </div>
            </div>
          </div>
        </>
      )}

      {/* Companies Tab */}
      {activeTab === 'companies' && (
        <div className="row">
          <div className="col">
            <div className="card">
              <div className="card-header">
                <h5><i className="fas fa-building me-2"></i>Company Performance Analysis</h5>
              </div>
              <div className="card-body">
                <div className="table-responsive">
                  <table className="table table-hover">
                    <thead className="table-dark">
                      <tr>
                        <th>Company</th>
                        <th>Market Share</th>
                        <th>Avg Price</th>
                        <th>Total Listings</th>
                        <th>Reliability Score</th>
                        <th>Price Trend</th>
                      </tr>
                    </thead>
                    <tbody>
                      {Object.entries(marketData.companies)
                        .sort(([,a], [,b]) => b.stats.market_share - a.stats.market_share)
                        .slice(0, 10)
                        .map(([company, data]) => (
                        <tr key={company}>
                          <td><strong>{company}</strong></td>
                          <td>{data.stats.market_share.toFixed(1)}%</td>
                          <td>{formatCurrency(data.stats.Price_mean)}</td>
                          <td>{formatNumber(data.stats.Price_count)}</td>
                          <td>
                            <span className={`badge bg-${data.reliability_score > 70 ? 'success' : data.reliability_score > 50 ? 'warning' : 'danger'}`}>
                              {data.reliability_score.toFixed(0)}/100
                            </span>
                          </td>
                          <td>
                            <span className={`badge bg-${data.price_trend === 'Increasing' ? 'success' : data.price_trend === 'Decreasing' ? 'danger' : 'secondary'}`}>
                              {data.price_trend}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Analytics Tab */}
      {activeTab === 'analytics' && (
        <div className="row">
          <div className="col-lg-6 mb-4">
            <div className="card">
              <div className="card-header">
                <h5><i className="fas fa-gas-pump me-2"></i>Fuel Type Analysis</h5>
              </div>
              <div className="card-body">
                {Object.entries(marketData.fuel).map(([fuelType, data]) => (
                  <div key={fuelType} className="mb-3 p-3 border rounded">
                    <h6 className="text-primary">{fuelType}</h6>
                    <div className="row">
                      <div className="col-6">
                        <small className="text-muted">Market Share:</small>
                        <div><strong>{data.market_share.toFixed(1)}%</strong></div>
                      </div>
                      <div className="col-6">
                        <small className="text-muted">Avg Price:</small>
                        <div><strong>{formatCurrency(data.average_price)}</strong></div>
                      </div>
                    </div>
                    <div className="row mt-2">
                      <div className="col-6">
                        <small className="text-muted">Avg Age:</small>
                        <div>{data.average_age.toFixed(1)} years</div>
                      </div>
                      <div className="col-6">
                        <small className="text-muted">Depreciation:</small>
                        <div className={data.depreciation_rate < 0 ? 'text-success' : 'text-danger'}>
                          {data.depreciation_rate.toFixed(1)}%
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
          <div className="col-lg-6 mb-4">
            <div className="card">
              <div className="card-header">
                <h5><i className="fas fa-city me-2"></i>City Market Analysis</h5>
              </div>
              <div className="card-body">
                {Object.entries(marketData.cities)
                  .sort(([,a], [,b]) => b.total_listings - a.total_listings)
                  .slice(0, 5)
                  .map(([city, data]) => (
                  <div key={city} className="mb-3 p-3 border rounded">
                    <h6 className="text-primary">{city}</h6>
                    <div className="row">
                      <div className="col-6">
                        <small className="text-muted">Total Listings:</small>
                        <div><strong>{formatNumber(data.total_listings)}</strong></div>
                      </div>
                      <div className="col-6">
                        <small className="text-muted">Market Share:</small>
                        <div><strong>{data.market_share.toFixed(1)}%</strong></div>
                      </div>
                    </div>
                    <div className="row mt-2">
                      <div className="col-12">
                        <small className="text-muted">Average Price:</small>
                        <div>{formatCurrency(data.average_price)}</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Predictions Tab */}
      {activeTab === 'predictions' && (
        <div className="row">
          <div className="col-lg-6 mb-4">
            <div className="card">
              <div className="card-header">
                <h5><i className="fas fa-arrow-up me-2"></i>Trending Up</h5>
              </div>
              <div className="card-body">
                {marketData.predictions.trending_up && marketData.predictions.trending_up.length > 0 ? (
                  marketData.predictions.trending_up.map((item, index) => (
                    <div key={index} className="alert alert-success">
                      <strong>{item.company}</strong><br />
                      Market Share: {item.market_share}%<br />
                      Reliability: {item.reliability_score}/100
                    </div>
                  ))
                ) : (
                  <p className="text-muted">No trending up companies identified.</p>
                )}
              </div>
            </div>
          </div>
          <div className="col-lg-6 mb-4">
            <div className="card">
              <div className="card-header">
                <h5><i className="fas fa-lightbulb me-2"></i>AI Recommendations</h5>
              </div>
              <div className="card-body">
                {marketData.predictions.recommendations && marketData.predictions.recommendations.length > 0 ? (
                  marketData.predictions.recommendations.map((rec, index) => (
                    <div key={index} className="alert alert-info">
                      <strong>{rec.type}:</strong><br />
                      {rec.description}<br />
                      <small className="text-muted">Confidence: {rec.confidence}</small>
                    </div>
                  ))
                ) : (
                  <p className="text-muted">No recommendations available.</p>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default MarketTrends;
