import React, { useState, useEffect } from 'react';
import { Line, Bar, Pie, Doughnut, Scatter } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js';
import axios from 'axios';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

const EnhancedMarketTrends = () => {
  const [charts, setCharts] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('overview');

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          usePointStyle: true,
          padding: 20,
          font: {
            size: 12
          }
        }
      },
      title: {
        display: true,
        font: {
          size: 16,
          weight: 'bold'
        }
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            if (context.dataset.label === 'Average Price (₹)') {
              return `${context.dataset.label}: ₹${context.parsed.y.toLocaleString()}`;
            }
            return `${context.dataset.label}: ${context.parsed.y}`;
          }
        }
      }
    },
    scales: {
      x: {
        ticks: {
          maxRotation: 45,
          minRotation: 45,
          font: {
            size: 10
          }
        }
      },
      y: {
        beginAtZero: true,
        ticks: {
          callback: function(value) {
            if (value >= 100000) {
              return '₹' + (value / 100000).toFixed(1) + 'L';
            }
            return '₹' + value.toLocaleString();
          }
        }
      }
    }
  };

  const pieOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'right',
        labels: {
          usePointStyle: true,
          padding: 15,
          font: {
            size: 11
          }
        }
      },
      title: {
        display: true,
        font: {
          size: 16,
          weight: 'bold'
        }
      }
    }
  };

  const scatterOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        font: {
          size: 16,
          weight: 'bold'
        }
      }
    },
    scales: {
      x: {
        title: {
          display: true,
          text: 'Kilometers Driven'
        }
      },
      y: {
        title: {
          display: true,
          text: 'Price (₹)'
        },
        ticks: {
          callback: function(value) {
            if (value >= 100000) {
              return '₹' + (value / 100000).toFixed(1) + 'L';
            }
            return '₹' + value.toLocaleString();
          }
        }
      }
    }
  };

  useEffect(() => {
    fetchAllCharts();
  }, []);

  const fetchAllCharts = async () => {
    setLoading(true);
    setError('');

    try {
      const chartEndpoints = [
        'price-trends-by-year',
        'company-market-share',
        'fuel-type-distribution',
        'city-price-comparison',
        'transmission-trends',
        'ev-vs-ice-trends',
        'price-vs-kms-scatter',
        'company-price-comparison'
      ];

      const chartPromises = chartEndpoints.map(endpoint =>
        axios.get(`/api/charts/${endpoint}`)
      );

      const responses = await Promise.all(chartPromises);
      
      const chartData = {};
      responses.forEach((response, index) => {
        if (response.data.success) {
          const endpoint = chartEndpoints[index];
          chartData[endpoint] = {
            data: response.data.data,
            title: response.data.title,
            description: response.data.description
          };
        }
      });

      setCharts(chartData);
    } catch (err) {
      console.error('Error fetching charts:', err);
      setError('Failed to load market trends data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const renderChart = (chartKey, ChartComponent, options = chartOptions, fullWidth = false) => {
    const chart = charts[chartKey];
    if (!chart) return null;

    const colClass = fullWidth ? "col-12" : "col-lg-6 col-xl-4";

    return (
      <div className={`${colClass} mb-4`}>
        <div className="card h-100 shadow-sm">
          <div className="card-header bg-primary text-white">
            <h6 className="card-title mb-0">{chart.title}</h6>
          </div>
          <div className="card-body">
            <div style={{ height: fullWidth ? '500px' : '400px', overflow: 'auto' }}>
              <ChartComponent data={chart.data} options={options} />
            </div>
            <p className="card-text small text-muted mt-2">{chart.description}</p>
          </div>
        </div>
      </div>
    );
  };

  if (loading) {
    return (
      <div className="container py-5">
        <div className="row justify-content-center">
          <div className="col-md-6 text-center">
            <div className="spinner-border text-primary mb-3" role="status">
              <span className="visually-hidden">Loading...</span>
            </div>
            <h4>Loading Market Trends...</h4>
            <p className="text-muted">Analyzing car market data and generating insights</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container py-5">
        <div className="row justify-content-center">
          <div className="col-md-6">
            <div className="alert alert-danger" role="alert">
              <h4 className="alert-heading">Error Loading Market Trends</h4>
              <p>{error}</p>
              <hr />
              <button className="btn btn-danger" onClick={fetchAllCharts}>
                Try Again
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container py-5">
      <div className="row">
        <div className="col-12">
          <div className="card shadow">
            <div className="card-header bg-primary text-white">
              <h2 className="mb-0">
                <i className="fas fa-chart-line me-2"></i>
                Enhanced Market Trends Dashboard
              </h2>
              <p className="mb-0 mt-2">Real-time insights from 20,780+ car records across 37 brands</p>
            </div>
            <div className="card-body">
              {/* Navigation Tabs */}
              <ul className="nav nav-tabs mb-4" id="trendsTab" role="tablist">
                <li className="nav-item" role="presentation">
                  <button
                    className={`nav-link ${activeTab === 'overview' ? 'active' : ''}`}
                    onClick={() => setActiveTab('overview')}
                  >
                    <i className="fas fa-chart-pie me-2"></i>Overview
                  </button>
                </li>
                <li className="nav-item" role="presentation">
                  <button
                    className={`nav-link ${activeTab === 'trends' ? 'active' : ''}`}
                    onClick={() => setActiveTab('trends')}
                  >
                    <i className="fas fa-chart-line me-2"></i>Trends
                  </button>
                </li>
                <li className="nav-item" role="presentation">
                  <button
                    className={`nav-link ${activeTab === 'comparison' ? 'active' : ''}`}
                    onClick={() => setActiveTab('comparison')}
                  >
                    <i className="fas fa-chart-bar me-2"></i>Comparisons
                  </button>
                </li>
                <li className="nav-item" role="presentation">
                  <button
                    className={`nav-link ${activeTab === 'analysis' ? 'active' : ''}`}
                    onClick={() => setActiveTab('analysis')}
                  >
                    <i className="fas fa-microscope me-2"></i>Analysis
                  </button>
                </li>
              </ul>

              {/* Tab Content */}
              <div className="tab-content">
                {/* Overview Tab */}
                {activeTab === 'overview' && (
                  <div className="row">
                    {renderChart('company-market-share', Doughnut, pieOptions, true)}
                    {renderChart('fuel-type-distribution', Pie, pieOptions)}
                    {renderChart('price-trends-by-year', Line)}
                  </div>
                )}

                {/* Trends Tab */}
                {activeTab === 'trends' && (
                  <div className="row">
                    {renderChart('ev-vs-ice-trends', Line)}
                    {renderChart('transmission-trends', Line)}
                    {renderChart('price-vs-kms-scatter', Scatter, scatterOptions)}
                  </div>
                )}

                {/* Comparisons Tab */}
                {activeTab === 'comparison' && (
                  <div className="row">
                    {renderChart('company-price-comparison', Bar, chartOptions, true)}
                    {renderChart('city-price-comparison', Bar, chartOptions, true)}
                  </div>
                )}

                {/* Analysis Tab */}
                {activeTab === 'analysis' && (
                  <div className="row">
                    <div className="col-12">
                      <div className="card">
                        <div className="card-header bg-info text-white">
                          <h5 className="mb-0">Market Analysis Summary</h5>
                        </div>
                        <div className="card-body">
                          <div className="row">
                            <div className="col-md-6">
                              <h6>Key Insights:</h6>
                              <ul className="list-unstyled">
                                <li><i className="fas fa-check text-success me-2"></i>Electric vehicle adoption is growing rapidly</li>
                                <li><i className="fas fa-check text-success me-2"></i>Automatic transmission preference is increasing</li>
                                <li><i className="fas fa-check text-success me-2"></i>Metro cities show higher average prices</li>
                                <li><i className="fas fa-check text-success me-2"></i>Premium brands maintain higher resale values</li>
                              </ul>
                            </div>
                            <div className="col-md-6">
                              <h6>Market Trends:</h6>
                              <ul className="list-unstyled">
                                <li><i className="fas fa-arrow-up text-primary me-2"></i>EV market share increasing year-over-year</li>
                                <li><i className="fas fa-arrow-up text-primary me-2"></i>CNG vehicles gaining popularity</li>
                                <li><i className="fas fa-arrow-down text-warning me-2"></i>Diesel vehicle share declining</li>
                                <li><i className="fas fa-arrow-up text-primary me-2"></i>Used car prices stabilizing</li>
                              </ul>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </div>

              {/* Refresh Button */}
              <div className="text-center mt-4">
                <button
                  className="btn btn-primary"
                  onClick={fetchAllCharts}
                  disabled={loading}
                >
                  <i className="fas fa-sync-alt me-2"></i>
                  Refresh Data
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EnhancedMarketTrends;
