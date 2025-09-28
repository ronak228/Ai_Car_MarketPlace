import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

const Dashboard = ({ user }) => {
  const [recentPredictions, setRecentPredictions] = useState([]);
  const [savedPredictions, setSavedPredictions] = useState([]);
  const [marketTrends, setMarketTrends] = useState([]);
  const [userStats, setUserStats] = useState({
    totalPredictions: 0,
    averageConfidence: 0,
    favoriteBrand: 'Toyota',
    totalSaved: 0,
    accuracyRate: 0
  });
  const [activeTab, setActiveTab] = useState('overview');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = () => {
    setLoading(true);
    
    // Simulate loading data
    setTimeout(() => {
      // Load recent predictions
      const recent = [
        { 
          id: 1, 
          car: 'Honda Civic 2020', 
          predictedPrice: 1850000, 
          confidence: 87, 
          date: '2024-01-15',
          actualPrice: 1820000,
          accuracy: '98.4%',
          saved: true
        },
        { 
          id: 2, 
          car: 'Toyota Camry 2019', 
          predictedPrice: 2230000, 
          confidence: 92, 
          date: '2024-01-14',
          actualPrice: null,
          accuracy: null,
          saved: false
        },
        { 
          id: 3, 
          car: 'Ford Mustang 2021', 
          predictedPrice: 3580000, 
          confidence: 78, 
          date: '2024-01-13',
          actualPrice: 3650000,
          accuracy: '97.9%',
          saved: true
        }
      ];

      // Load saved predictions
      const saved = recent.filter(p => p.saved);

      // Load market trends
      const trends = [
        { brand: 'Toyota', trend: 'Rising', change: '+5.2%', confidence: 89 },
        { brand: 'Honda', trend: 'Stable', change: '+0.8%', confidence: 76 },
        { brand: 'Ford', trend: 'Falling', change: '-2.1%', confidence: 82 },
        { brand: 'BMW', trend: 'Rising', change: '+8.5%', confidence: 91 },
        { brand: 'Mercedes', trend: 'Stable', change: '+1.3%', confidence: 85 }
      ];

      // Calculate user stats
      const stats = {
        totalPredictions: recent.length,
        averageConfidence: Math.round(recent.reduce((sum, p) => sum + p.confidence, 0) / recent.length),
        favoriteBrand: 'Toyota',
        totalSaved: saved.length,
        accuracyRate: Math.round(recent.filter(p => p.actualPrice).reduce((sum, p) => sum + parseFloat(p.accuracy), 0) / recent.filter(p => p.actualPrice).length)
      };

      setRecentPredictions(recent);
      setSavedPredictions(saved);
      setMarketTrends(trends);
      setUserStats(stats);
      setLoading(false);
    }, 1000);
  };

  const toggleSavePrediction = (predictionId) => {
    setRecentPredictions(prev => 
      prev.map(p => 
        p.id === predictionId 
          ? { ...p, saved: !p.saved }
          : p
      )
    );
    
    setSavedPredictions(prev => {
      const prediction = recentPredictions.find(p => p.id === predictionId);
      if (prediction.saved) {
        return prev.filter(p => p.id !== predictionId);
      } else {
        return [...prev, { ...prediction, saved: true }];
      }
    });
  };

  const getTrendColor = (trend) => {
    switch (trend) {
      case 'Rising': return 'success';
      case 'Stable': return 'info';
      case 'Falling': return 'danger';
      default: return 'secondary';
    }
  };

  const getTrendIcon = (trend) => {
    switch (trend) {
      case 'Rising': return '📈';
      case 'Stable': return '➡️';
      case 'Falling': return '📉';
      default: return '❓';
    }
  };

  const exportPredictions = () => {
    const csvContent = [
      ['Car', 'Predicted Price', 'Confidence', 'Date', 'Accuracy', 'Saved'],
      ...recentPredictions.map(p => [
        p.car,
        p.predictedPrice,
        p.confidence + '%',
        p.date,
        p.accuracy || 'Pending',
        p.saved ? 'Yes' : 'No'
      ])
    ].map(row => row.join(',')).join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `predictions-${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
  };

  const getPredictionInsights = () => {
    const insights = [];
    
    if (userStats.averageConfidence > 85) {
      insights.push('🎯 High confidence predictions - your model is performing well!');
    }
    
    if (userStats.accuracyRate > 90) {
      insights.push('📊 Excellent accuracy rate - predictions are very reliable!');
    }
    
    if (userStats.totalSaved > 0) {
      insights.push(`⭐ You've saved ${userStats.totalSaved} predictions for future reference`);
    }
    
    const topBrand = marketTrends.find(t => t.brand === userStats.favoriteBrand);
    if (topBrand) {
      insights.push(`📈 ${topBrand.brand} prices are ${topBrand.trend.toLowerCase()} (${topBrand.change})`);
    }
    
    return insights;
  };

  if (loading) {
    return (
      <div className="container py-5">
        <div className="text-center">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p className="mt-3">Loading your dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container py-5">
      {/* Welcome Section */}
      <div className="row mb-5">
        <div className="col-12">
          <div className="card bg-primary text-white">
            <div className="card-body">
              <h2 className="card-title">Welcome back, {user?.name || 'User'}! 🤖</h2>
              <p className="card-text">
                Your AI-powered car price prediction dashboard with advanced analytics and market insights.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Stats */}
      <div className="row mb-5">
        <div className="col-md-2 mb-3">
          <div className="card text-center">
            <div className="card-body">
              <h3 className="text-primary">{userStats.totalPredictions}</h3>
              <p className="card-text">Total Predictions</p>
            </div>
          </div>
        </div>
        <div className="col-md-2 mb-3">
          <div className="card text-center">
            <div className="card-body">
              <h3 className="text-success">{userStats.averageConfidence}%</h3>
              <p className="card-text">Avg Confidence</p>
            </div>
          </div>
        </div>
        <div className="col-md-2 mb-3">
          <div className="card text-center">
            <div className="card-body">
              <h3 className="text-info">{userStats.favoriteBrand}</h3>
              <p className="card-text">Top Brand</p>
            </div>
          </div>
        </div>
        <div className="col-md-2 mb-3">
          <div className="card text-center">
            <div className="card-body">
              <h3 className="text-warning">{userStats.totalSaved}</h3>
              <p className="card-text">Saved</p>
            </div>
          </div>
        </div>
        <div className="col-md-2 mb-3">
          <div className="card text-center">
            <div className="card-body">
              <h3 className="text-danger">{userStats.accuracyRate}%</h3>
              <p className="card-text">Accuracy</p>
            </div>
          </div>
        </div>
        <div className="col-md-2 mb-3">
          <div className="card text-center">
            <div className="card-body">
              <h3 className="text-secondary">4</h3>
              <p className="card-text">ML Models</p>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="row mb-4">
        <div className="col-12">
          <ul className="nav nav-tabs" id="dashboardTabs" role="tablist">
            <li className="nav-item" role="presentation">
              <button 
                className={`nav-link ${activeTab === 'overview' ? 'active' : ''}`}
                onClick={() => setActiveTab('overview')}
              >
                📊 Overview
              </button>
            </li>
            <li className="nav-item" role="presentation">
              <button 
                className={`nav-link ${activeTab === 'predictions' ? 'active' : ''}`}
                onClick={() => setActiveTab('predictions')}
              >
                🚗 Recent Predictions
              </button>
            </li>
            <li className="nav-item" role="presentation">
              <button 
                className={`nav-link ${activeTab === 'saved' ? 'active' : ''}`}
                onClick={() => setActiveTab('saved')}
              >
                ⭐ Saved Predictions
              </button>
            </li>
            <li className="nav-item" role="presentation">
              <button 
                className={`nav-link ${activeTab === 'trends' ? 'active' : ''}`}
                onClick={() => setActiveTab('trends')}
              >
                📈 Market Trends
              </button>
            </li>
            <li className="nav-item" role="presentation">
              <button 
                className={`nav-link ${activeTab === 'models' ? 'active' : ''}`}
                onClick={() => setActiveTab('models')}
              >
                🤖 Model Comparison
              </button>
            </li>
          </ul>
        </div>
      </div>

      {/* Tab Content */}
      <div className="tab-content">
        {/* Overview Tab */}
        {activeTab === 'overview' && (
          <div className="row">
            <div className="col-md-8">
              <div className="card">
                <div className="card-header">
                  <h5 className="mb-0">📊 Prediction Analytics</h5>
                </div>
                <div className="card-body">
                  <div className="row">
                    <div className="col-md-6">
                      <h6>Recent Activity</h6>
                      <div className="list-group list-group-flush">
                        {recentPredictions.slice(0, 3).map((prediction) => (
                          <div key={prediction.id} className="list-group-item d-flex justify-content-between align-items-center">
                            <div>
                              <strong>{prediction.car}</strong>
                              <br />
                              <small className="text-muted">{prediction.date}</small>
                            </div>
                            <div className="text-end">
                              <span className="badge bg-primary">₹{prediction.predictedPrice.toLocaleString()}</span>
                              <br />
                              <small className="text-muted">{prediction.confidence}% confidence</small>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                    <div className="col-md-6">
                      <h6>Performance Metrics</h6>
                      <div className="mb-3">
                        <label className="form-label">Average Confidence</label>
                        <div className="progress">
                          <div className="progress-bar bg-success" style={{width: `${userStats.averageConfidence}%`}}>
                            {userStats.averageConfidence}%
                          </div>
                        </div>
                      </div>
                      <div className="mb-3">
                        <label className="form-label">Prediction Accuracy</label>
                        <div className="progress">
                          <div className="progress-bar bg-info" style={{width: `${userStats.accuracyRate}%`}}>
                            {userStats.accuracyRate}%
                          </div>
                        </div>
                      </div>
                      <div className="mb-3">
                        <label className="form-label">Saved Predictions</label>
                        <div className="progress">
                          <div className="progress-bar bg-warning" style={{width: `${(userStats.totalSaved/userStats.totalPredictions)*100}%`}}>
                            {userStats.totalSaved}/{userStats.totalPredictions}
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div className="col-md-4">
              <div className="card">
                <div className="card-header">
                  <h5 className="mb-0">🚀 Quick Actions</h5>
                </div>
                <div className="card-body">
                  <div className="d-grid gap-2">
                    <Link to="/car-price-predictor" className="btn btn-primary">
                      🚗 New Price Prediction
                    </Link>
                    <button className="btn btn-outline-success">
                      📊 View Market Trends
                    </button>
                    <button className="btn btn-outline-info">
                      📈 Compare Models
                    </button>
                    <button className="btn btn-outline-warning">
                      ⭐ Saved Predictions
                    </button>
                    <button className="btn btn-outline-secondary" onClick={exportPredictions}>
                      📥 Export Predictions
                    </button>
                  </div>
                </div>
                            </div>
              
              {/* AI Insights */}
              <div className="card mt-3">
                <div className="card-header">
                  <h5 className="mb-0">💡 AI Insights</h5>
                </div>
                <div className="card-body">
                  {getPredictionInsights().map((insight, index) => (
                    <div key={index} className="alert alert-info alert-sm mb-2">
                      {insight}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Recent Predictions Tab */}
        {activeTab === 'predictions' && (
          <div className="row">
            <div className="col-12">
              <div className="card">
                <div className="card-header d-flex justify-content-between align-items-center">
                  <h5 className="mb-0">🚗 Recent Predictions</h5>
                  <Link to="/car-price-predictor" className="btn btn-primary btn-sm">
                    New Prediction
                  </Link>
                </div>
                <div className="card-body">
                  <div className="table-responsive">
                    <table className="table table-hover">
                      <thead>
                        <tr>
                          <th>Car</th>
                          <th>Predicted Price</th>
                          <th>Confidence</th>
                          <th>Date</th>
                          <th>Accuracy</th>
                          <th>Actions</th>
                        </tr>
                      </thead>
                      <tbody>
                        {recentPredictions.map((prediction) => (
                          <tr key={prediction.id}>
                            <td>
                              <strong>{prediction.car}</strong>
                              {prediction.saved && <span className="badge bg-warning ms-2">⭐</span>}
                            </td>
                            <td>
                              <span className="badge bg-primary fs-6">
                                ₹{prediction.predictedPrice.toLocaleString()}
                              </span>
                            </td>
                            <td>
                              <span className={`badge bg-${prediction.confidence >= 90 ? 'success' : prediction.confidence >= 80 ? 'warning' : 'danger'}`}>
                                {prediction.confidence}%
                              </span>
                            </td>
                            <td>{prediction.date}</td>
                            <td>
                              {prediction.accuracy ? (
                                <span className="badge bg-success">{prediction.accuracy}</span>
                              ) : (
                                <span className="text-muted">Pending</span>
                              )}
                            </td>
                            <td>
                              <div className="btn-group btn-group-sm">
                                <button 
                                  className={`btn ${prediction.saved ? 'btn-warning' : 'btn-outline-warning'}`}
                                  onClick={() => toggleSavePrediction(prediction.id)}
                                >
                                  {prediction.saved ? '⭐' : '☆'}
                                </button>
                                <button className="btn btn-outline-primary">View</button>
                                <button className="btn btn-outline-info">Compare</button>
                              </div>
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

        {/* Saved Predictions Tab */}
        {activeTab === 'saved' && (
          <div className="row">
            <div className="col-12">
              <div className="card">
                <div className="card-header">
                  <h5 className="mb-0">⭐ Saved Predictions ({savedPredictions.length})</h5>
                </div>
                <div className="card-body">
                  {savedPredictions.length === 0 ? (
                    <div className="text-center py-5">
                      <h4>No saved predictions yet</h4>
                      <p className="text-muted">Save your favorite predictions to track them here</p>
                      <Link to="/car-price-predictor" className="btn btn-primary">
                        Make Your First Prediction
                      </Link>
                    </div>
                  ) : (
                    <div className="row g-4">
                      {savedPredictions.map((prediction) => (
                        <div key={prediction.id} className="col-md-6 col-lg-4">
                          <div className="card h-100">
                            <div className="card-body">
                              <h6 className="card-title">{prediction.car}</h6>
                              <div className="mb-3">
                                <span className="badge bg-primary fs-6">
                                  ₹{prediction.predictedPrice.toLocaleString()}
                                </span>
                              </div>
                              <p className="card-text">
                                <strong>Confidence:</strong> {prediction.confidence}%<br/>
                                <strong>Date:</strong> {prediction.date}<br/>
                                {prediction.accuracy && (
                                  <><strong>Accuracy:</strong> {prediction.accuracy}<br/></>
                                )}
                              </p>
                              <div className="d-flex gap-2">
                                <button className="btn btn-outline-primary btn-sm">View Details</button>
                                <button className="btn btn-outline-danger btn-sm">Remove</button>
                              </div>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Market Trends Tab */}
        {activeTab === 'trends' && (
          <div className="row">
            <div className="col-12">
              <div className="card">
                <div className="card-header">
                  <h5 className="mb-0">📈 Market Trends Analysis</h5>
                </div>
                <div className="card-body">
                  <div className="row g-4">
                    {marketTrends.map((trend, index) => (
                      <div key={index} className="col-md-6 col-lg-4">
                        <div className="card">
                          <div className="card-body text-center">
                            <h5 className="card-title">{trend.brand}</h5>
                            <div className="mb-3">
                              <span className={`badge bg-${getTrendColor(trend.trend)} fs-5`}>
                                {getTrendIcon(trend.trend)} {trend.trend}
                              </span>
                            </div>
                            <p className="card-text">
                              <strong>Price Change:</strong> {trend.change}<br/>
                              <strong>Confidence:</strong> {trend.confidence}%
                            </p>
                            <button className="btn btn-outline-primary btn-sm">View Details</button>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Model Comparison Tab */}
        {activeTab === 'models' && (
          <div className="row">
            <div className="col-12">
              <div className="card">
                <div className="card-header">
                  <h5 className="mb-0">🤖 ML Model Comparison</h5>
                </div>
                <div className="card-body">
                  <div className="table-responsive">
                    <table className="table table-hover">
                      <thead>
                        <tr>
                          <th>Model</th>
                          <th>Accuracy</th>
                          <th>Speed</th>
                          <th>Memory Usage</th>
                          <th>Best For</th>
                          <th>Status</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr>
                          <td><strong>Linear Regression</strong></td>
                          <td><span className="badge bg-warning">82%</span></td>
                          <td><span className="badge bg-success">Fast</span></td>
                          <td><span className="badge bg-success">Low</span></td>
                          <td>Simple relationships</td>
                          <td><span className="badge bg-success">Active</span></td>
                        </tr>
                        <tr>
                          <td><strong>Random Forest</strong></td>
                          <td><span className="badge bg-info">89%</span></td>
                          <td><span className="badge bg-warning">Medium</span></td>
                          <td><span className="badge bg-warning">Medium</span></td>
                          <td>Complex patterns</td>
                          <td><span className="badge bg-success">Active</span></td>
                        </tr>
                        <tr>
                          <td><strong>XGBoost</strong></td>
                          <td><span className="badge bg-success">91%</span></td>
                          <td><span className="badge bg-warning">Medium</span></td>
                          <td><span className="badge bg-warning">Medium</span></td>
                          <td>High accuracy</td>
                          <td><span className="badge bg-success">Active</span></td>
                        </tr>
                        <tr>
                          <td><strong>Neural Network</strong></td>
                          <td><span className="badge bg-info">87%</span></td>
                          <td><span className="badge bg-danger">Slow</span></td>
                          <td><span className="badge bg-danger">High</span></td>
                          <td>Deep learning</td>
                          <td><span className="badge bg-success">Active</span></td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                  <div className="mt-4">
                    <h6>Model Performance Summary</h6>
                    <div className="row">
                      <div className="col-md-3">
                        <div className="text-center">
                          <h4 className="text-success">91%</h4>
                          <p>Best Accuracy (XGBoost)</p>
                        </div>
                      </div>
                      <div className="col-md-3">
                        <div className="text-center">
                          <h4 className="text-primary">Fast</h4>
                          <p>Best Speed (Linear Regression)</p>
                        </div>
                      </div>
                      <div className="col-md-3">
                        <div className="text-center">
                          <h4 className="text-info">Low</h4>
                          <p>Best Memory (Linear Regression)</p>
                        </div>
                      </div>
                      <div className="col-md-3">
                        <div className="text-center">
                          <h4 className="text-warning">4</h4>
                          <p>Active Models</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard; 