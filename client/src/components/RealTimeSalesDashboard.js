import React, { useState, useEffect } from 'react';
import { Line, Bar, Pie, Doughnut } from 'react-chartjs-2';
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
import api from '../api';

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

const RealTimeSalesDashboard = () => {
  const [salesData, setSalesData] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('overview');
  const [lastUpdated, setLastUpdated] = useState(new Date());

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
        },
        padding: 20
      },
      tooltip: {
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        titleColor: '#fff',
        bodyColor: '#fff',
        borderColor: '#fff',
        borderWidth: 1,
        cornerRadius: 8,
        displayColors: true,
        callbacks: {
          label: function(context) {
            const label = context.dataset.label || '';
            const value = context.parsed.y || context.parsed;
            return `${label}: ${value.toLocaleString()} units`;
          }
        }
      }
    },
    scales: {
      x: {
        grid: {
          display: false
        },
        ticks: {
          font: {
            size: 11
          }
        }
      },
      y: {
        grid: {
          color: 'rgba(0, 0, 0, 0.1)'
        },
        ticks: {
          font: {
            size: 11
          },
          callback: function(value) {
            return `${value.toLocaleString()}`;
          }
        }
      }
    },
    interaction: {
      intersect: false,
      mode: 'index'
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
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            const label = context.label || '';
            const value = context.parsed;
            const total = context.dataset.data.reduce((a, b) => a + b, 0);
            const percentage = ((value / total) * 100).toFixed(1);
            return `${label}: ${value.toLocaleString()} units (${percentage}%)`;
          }
        }
      }
    }
  };

  const fetchSalesData = async () => {
    try {
      setLoading(true);
      setError('');

      // Fetch sales data for all Indian brands
      const response = await api.get('/api/sales/indian-brands');
      
      if (response.data.success) {
        setSalesData(response.data.data);
        setLastUpdated(new Date());
      } else {
        setError('Failed to load sales data');
      }
    } catch (err) {
      console.error('Error fetching sales data:', err);
      setError('Failed to load sales data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSalesData();
    
    // Auto-refresh every 30 seconds
    const interval = setInterval(fetchSalesData, 30000);
    
    return () => clearInterval(interval);
  }, []);

  const renderChart = (chartKey, ChartComponent, options = chartOptions, fullWidth = false) => {
    const chart = salesData[chartKey];
    if (!chart) return null;

    const colClass = fullWidth ? "col-12" : "col-lg-6 col-xl-4";

    return (
      <div className={`${colClass} mb-4`}>
        <div className="card h-100 shadow-sm">
          <div className="card-header bg-success text-white">
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

  const renderOverviewTab = () => (
    <div className="row">
      {/* Top Selling Brands */}
      {renderChart('top-brands', Bar, chartOptions, true)}
      
      {/* Fuel Type Distribution */}
      {renderChart('fuel-distribution', Pie, pieOptions)}
      
      {/* Monthly Sales Trend */}
      {renderChart('monthly-trend', Line, chartOptions)}
      
      {/* EV vs ICE Sales */}
      {renderChart('ev-vs-ice', Doughnut, pieOptions)}
    </div>
  );

  const renderBrandsTab = () => (
    <div className="row">
      {/* All Brands Sales */}
      {renderChart('all-brands', Bar, chartOptions, true)}
      
      {/* Brand Performance Comparison */}
      {renderChart('brand-performance', Line, chartOptions)}
    </div>
  );

  const renderFuelTypesTab = () => (
    <div className="row">
      {/* Fuel Type Sales */}
      {renderChart('fuel-sales', Bar, chartOptions, true)}
      
      {/* EV Growth Trend */}
      {renderChart('ev-growth', Line, chartOptions)}
      
      {/* Diesel vs Petrol */}
      {renderChart('diesel-petrol', Doughnut, pieOptions)}
    </div>
  );

  const renderRegionalTab = () => (
    <div className="row">
      {/* Regional Sales */}
      {renderChart('regional-sales', Bar, chartOptions, true)}
      
      {/* City-wise Performance */}
      {renderChart('city-performance', Line, chartOptions)}
    </div>
  );

  if (loading) {
    return (
      <div className="container-fluid py-4">
        <div className="row">
          <div className="col-12">
            <div className="card">
              <div className="card-body text-center">
                <div className="spinner-border text-primary" role="status">
                  <span className="visually-hidden">Loading...</span>
                </div>
                <p className="mt-3">Loading real-time sales data...</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container-fluid py-4">
        <div className="row">
          <div className="col-12">
            <div className="alert alert-danger" role="alert">
              <h4 className="alert-heading">Error Loading Sales Data</h4>
              <p>{error}</p>
              <hr />
              <button className="btn btn-danger" onClick={fetchSalesData}>
                Try Again
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container-fluid py-4">
      {/* Welcome Banner */}
      <div className="row mb-4">
        <div className="col-12">
          <div className="card bg-gradient-primary text-white">
            <div className="card-body">
              <div className="row align-items-center">
                <div className="col-md-8">
                  <h2 className="card-title mb-2">
                    <i className="fas fa-chart-line me-2"></i>
                    Welcome back, CarCrafter AI User! <span role="img" aria-label="dashboard">📊</span>
                  </h2>
                  <p className="card-text mb-0">
                    Live sales data for all Indian car brands including EV, Petrol, Diesel, CNG, and Hybrid vehicles
                  </p>
                </div>
                <div className="col-md-4 text-end">
                  <div className="d-flex flex-column">
                    <small className="text-light">Last Updated:</small>
                    <strong>{lastUpdated.toLocaleTimeString()}</strong>
                    <small className="text-light">Auto-refresh: 30s</small>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="row mb-4">
        <div className="col-12">
          <ul className="nav nav-tabs" role="tablist">
            <li className="nav-item" role="presentation">
              <button
                className={`nav-link ${activeTab === 'overview' ? 'active' : ''}`}
                onClick={() => setActiveTab('overview')}
              >
                <i className="fas fa-tachometer-alt me-2"></i>Overview
              </button>
            </li>
            <li className="nav-item" role="presentation">
              <button
                className={`nav-link ${activeTab === 'brands' ? 'active' : ''}`}
                onClick={() => setActiveTab('brands')}
              >
                <i className="fas fa-car me-2"></i>Brands
              </button>
            </li>
            <li className="nav-item" role="presentation">
              <button
                className={`nav-link ${activeTab === 'fuel-types' ? 'active' : ''}`}
                onClick={() => setActiveTab('fuel-types')}
              >
                <i className="fas fa-gas-pump me-2"></i>Fuel Types
              </button>
            </li>
            <li className="nav-item" role="presentation">
              <button
                className={`nav-link ${activeTab === 'regional' ? 'active' : ''}`}
                onClick={() => setActiveTab('regional')}
              >
                <i className="fas fa-map-marker-alt me-2"></i>Regional
              </button>
            </li>
          </ul>
        </div>
      </div>

      {/* Tab Content */}
      <div className="tab-content">
        {activeTab === 'overview' && renderOverviewTab()}
        {activeTab === 'brands' && renderBrandsTab()}
        {activeTab === 'fuel-types' && renderFuelTypesTab()}
        {activeTab === 'regional' && renderRegionalTab()}
      </div>

      {/* Summary Stats */}
      <div className="row mt-4">
        <div className="col-12">
          <div className="card">
            <div className="card-header">
              <h5 className="card-title mb-0">
                <i className="fas fa-info-circle me-2"></i>
                Sales Summary
              </h5>
            </div>
            <div className="card-body">
              <div className="row">
                <div className="col-md-3">
                  <div className="text-center">
                    <h3 className="text-success">{salesData.totalSales?.toLocaleString() || '0'}</h3>
                    <p className="text-muted mb-0">Total Units Sold</p>
                  </div>
                </div>
                <div className="col-md-3">
                  <div className="text-center">
                    <h3 className="text-primary">{salesData.totalBrands || '0'}</h3>
                    <p className="text-muted mb-0">Active Brands</p>
                  </div>
                </div>
                <div className="col-md-3">
                  <div className="text-center">
                    <h3 className="text-warning">{salesData.evSales?.toLocaleString() || '0'}</h3>
                    <p className="text-muted mb-0">EV Units Sold</p>
                  </div>
                </div>
                <div className="col-md-3">
                  <div className="text-center">
                    <h3 className="text-info">{salesData.topCity || 'N/A'}</h3>
                    <p className="text-muted mb-0">Top Selling City</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RealTimeSalesDashboard;
