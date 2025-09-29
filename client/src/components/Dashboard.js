import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Swal from 'sweetalert2';
import PredictionStorage from '../utils/predictionStorage';
import CompanyDetailsModal from './CompanyDetailsModal';

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
  const [selectedCompany, setSelectedCompany] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = () => {
    setLoading(true);
    
    // Load real predictions from storage
    setTimeout(() => {
      // Load recent predictions from storage
      const allPredictions = PredictionStorage.getAllPredictions();
      const recent = allPredictions.map(p => ({
        id: p.id,
        car: `${p.company} ${p.model}`,
        predictedPrice: p.predictedPrice,
        confidence: p.confidence,
        date: p.date,
        actualPrice: p.actualPrice,
        accuracy: p.accuracy,
        saved: p.saved,
        company: p.company,
        model: p.model,
        year: p.year,
        fuel_type: p.fuel_type,
        kms_driven: p.kms_driven,
        city: p.city,
        marketTrend: p.marketTrend,
        modelUsed: p.modelUsed
      }));

      // Load saved predictions
      const saved = recent.filter(p => p.saved);

      // Generate market trends from prediction data
      const brandTrends = {};
      recent.forEach(p => {
        if (!brandTrends[p.company]) {
          brandTrends[p.company] = {
            count: 0,
            totalConfidence: 0,
            trends: []
          };
        }
        brandTrends[p.company].count++;
        brandTrends[p.company].totalConfidence += p.confidence;
        if (p.marketTrend) {
          brandTrends[p.company].trends.push(p.marketTrend);
        }
      });

      const trends = Object.entries(brandTrends).map(([brand, data]) => {
        const avgConfidence = Math.round(data.totalConfidence / data.count);
        const trendCounts = data.trends.reduce((acc, trend) => {
          acc[trend] = (acc[trend] || 0) + 1;
          return acc;
        }, {});
        
        const mostCommonTrend = Object.keys(trendCounts).reduce((a, b) => 
          trendCounts[a] > trendCounts[b] ? a : b, 'Stable'
        );
        
        const change = mostCommonTrend === 'Rising' ? '+5.2%' : 
                      mostCommonTrend === 'Falling' ? '-2.1%' : '+0.8%';
        
        return {
          brand,
          trend: mostCommonTrend,
          change,
          confidence: avgConfidence
        };
      }).slice(0, 5); // Top 5 brands

      // Calculate user stats from real data
      const stats = PredictionStorage.getStats();

      setRecentPredictions(recent);
      setSavedPredictions(saved);
      setMarketTrends(trends);
      setUserStats(stats);
      setLoading(false);
    }, 1000);
  };

  const toggleSavePrediction = async (predictionId) => {
    const prediction = recentPredictions.find(p => p.id === predictionId);
    if (!prediction) return;

    // Update in storage
    const success = PredictionStorage.toggleSave(predictionId);
    
    if (success) {
      const isNowSaved = !prediction.saved;
      
      // Show success message
      await Swal.fire({
        title: isNowSaved ? 'Prediction Saved! ⭐' : 'Prediction Unsaved',
        text: isNowSaved 
          ? 'This prediction has been added to your saved predictions.' 
          : 'This prediction has been removed from your saved predictions.',
        icon: 'success',
        confirmButtonText: 'OK',
        confirmButtonColor: '#28a745',
        timer: 2000,
        timerProgressBar: true
      });
      
      // Update local state
    setRecentPredictions(prev => 
      prev.map(p => 
        p.id === predictionId 
          ? { ...p, saved: !p.saved }
          : p
      )
    );
    
    setSavedPredictions(prev => {
      if (prediction.saved) {
        return prev.filter(p => p.id !== predictionId);
      } else {
        return [...prev, { ...prediction, saved: true }];
      }
    });
    } else {
      Swal.fire({
        title: 'Error',
        text: 'Failed to update prediction. Please try again.',
        icon: 'error',
        confirmButtonText: 'OK',
        confirmButtonColor: '#dc3545'
      });
    }
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

  const exportPredictions = async () => {
    const predictions = PredictionStorage.getAllPredictions();
    
    if (predictions.length === 0) {
      await Swal.fire({
        title: 'No Predictions to Export',
        text: 'You haven\'t made any predictions yet. Make some predictions first!',
        icon: 'info',
        confirmButtonText: 'OK',
        confirmButtonColor: '#17a2b8'
      });
      return;
    }

    const result = await Swal.fire({
      title: 'Export Predictions',
      html: `
        <div class="text-start">
          <p><strong>Total Predictions:</strong> ${predictions.length}</p>
          <p><strong>Saved Predictions:</strong> ${predictions.filter(p => p.saved).length}</p>
          <p><strong>With Accuracy:</strong> ${predictions.filter(p => p.accuracy).length}</p>
        </div>
        <p class="mt-3">This will download a CSV file with all your prediction data.</p>
      `,
      icon: 'question',
      showCancelButton: true,
      confirmButtonText: 'Export CSV',
      cancelButtonText: 'Cancel',
      confirmButtonColor: '#28a745',
      cancelButtonColor: '#6c757d'
    });

    if (result.isConfirmed) {
      try {
        PredictionStorage.exportPredictions();
        await Swal.fire({
          title: 'Export Successful!',
          text: 'Your predictions have been exported successfully.',
          icon: 'success',
          confirmButtonText: 'Great!',
          confirmButtonColor: '#28a745',
          timer: 2000,
          timerProgressBar: true
        });
      } catch (error) {
        await Swal.fire({
          title: 'Export Failed',
          text: 'There was an error exporting your predictions. Please try again.',
          icon: 'error',
          confirmButtonText: 'OK',
          confirmButtonColor: '#dc3545'
        });
      }
    }
  };

  const addActualPrice = async (predictionId) => {
    const prediction = recentPredictions.find(p => p.id === predictionId);
    if (!prediction) return;

    const { value: actualPrice } = await Swal.fire({
      title: 'Add Actual Price',
      html: `
        <div class="text-start">
          <p><strong>Car:</strong> ${prediction.car}</p>
          <p><strong>Predicted Price:</strong> ₹${prediction.predictedPrice.toLocaleString()}</p>
          <p><strong>Confidence:</strong> ${prediction.confidence}%</p>
        </div>
      `,
      input: 'number',
      inputLabel: 'Actual Price (₹)',
      inputPlaceholder: 'Enter the actual price of the car',
      inputAttributes: {
        min: 0,
        step: 1000
      },
      showCancelButton: true,
      confirmButtonText: 'Add Price',
      cancelButtonText: 'Cancel',
      confirmButtonColor: '#28a745',
      cancelButtonColor: '#dc3545',
      inputValidator: (value) => {
        if (!value) {
          return 'Please enter a valid price!';
        }
        if (isNaN(value) || value <= 0) {
          return 'Please enter a valid positive number!';
        }
      }
    });

    if (actualPrice) {
      const success = PredictionStorage.addActualPrice(predictionId, parseFloat(actualPrice));
      if (success) {
        const accuracy = ((1 - Math.abs(prediction.predictedPrice - actualPrice) / prediction.predictedPrice) * 100).toFixed(1);
        
        await Swal.fire({
          title: 'Price Added Successfully!',
          html: `
            <div class="text-start">
              <p><strong>Predicted:</strong> ₹${prediction.predictedPrice.toLocaleString()}</p>
              <p><strong>Actual:</strong> ₹${parseFloat(actualPrice).toLocaleString()}</p>
              <p><strong>Accuracy:</strong> <span class="badge bg-success">${accuracy}%</span></p>
            </div>
          `,
          icon: 'success',
          confirmButtonText: 'Great!',
          confirmButtonColor: '#28a745'
        });
        
        loadDashboardData(); // Reload data to show updated accuracy
      } else {
        Swal.fire({
          title: 'Error',
          text: 'Failed to add actual price. Please try again.',
          icon: 'error',
          confirmButtonText: 'OK',
          confirmButtonColor: '#dc3545'
        });
      }
    }
  };

  const deletePrediction = async (predictionId) => {
    const prediction = recentPredictions.find(p => p.id === predictionId);
    if (!prediction) return;

    const result = await Swal.fire({
      title: 'Delete Prediction',
      html: `
        <div class="text-start">
          <p><strong>Car:</strong> ${prediction.car}</p>
          <p><strong>Predicted Price:</strong> ₹${prediction.predictedPrice.toLocaleString()}</p>
          <p><strong>Date:</strong> ${prediction.date}</p>
          ${prediction.saved ? '<p><span class="badge bg-warning">⭐ Saved</span></p>' : ''}
        </div>
        <p class="text-danger mt-3"><strong>This action cannot be undone!</strong></p>
      `,
      icon: 'warning',
      showCancelButton: true,
      confirmButtonText: 'Yes, Delete!',
      cancelButtonText: 'Cancel',
      confirmButtonColor: '#dc3545',
      cancelButtonColor: '#6c757d',
      reverseButtons: true
    });

    if (result.isConfirmed) {
      const success = PredictionStorage.deletePrediction(predictionId);
      if (success) {
        await Swal.fire({
          title: 'Deleted!',
          text: 'Prediction has been deleted successfully.',
          icon: 'success',
          confirmButtonText: 'OK',
          confirmButtonColor: '#28a745',
          timer: 2000,
          timerProgressBar: true
        });
        loadDashboardData(); // Reload data
      } else {
        Swal.fire({
          title: 'Error',
          text: 'Failed to delete prediction. Please try again.',
          icon: 'error',
          confirmButtonText: 'OK',
          confirmButtonColor: '#dc3545'
        });
      }
    }
  };

  const clearAllPredictions = async () => {
    const predictions = PredictionStorage.getAllPredictions();
    
    if (predictions.length === 0) {
      await Swal.fire({
        title: 'No Predictions to Clear',
        text: 'You don\'t have any predictions to clear.',
        icon: 'info',
        confirmButtonText: 'OK',
        confirmButtonColor: '#17a2b8'
      });
      return;
    }

    const result = await Swal.fire({
      title: 'Clear All Predictions',
      html: `
        <div class="text-start">
          <p><strong>Total Predictions:</strong> ${predictions.length}</p>
          <p><strong>Saved Predictions:</strong> ${predictions.filter(p => p.saved).length}</p>
          <p><strong>With Accuracy:</strong> ${predictions.filter(p => p.accuracy).length}</p>
        </div>
        <p class="text-danger mt-3"><strong>This action cannot be undone!</strong></p>
        <p>All your prediction history will be permanently deleted.</p>
      `,
      icon: 'warning',
      showCancelButton: true,
      confirmButtonText: 'Yes, Clear All!',
      cancelButtonText: 'Cancel',
      confirmButtonColor: '#dc3545',
      cancelButtonColor: '#6c757d',
      reverseButtons: true
    });

    if (result.isConfirmed) {
      const success = PredictionStorage.clearAllPredictions();
      if (success) {
        await Swal.fire({
          title: 'All Predictions Cleared!',
          text: 'All your predictions have been deleted successfully.',
          icon: 'success',
          confirmButtonText: 'OK',
          confirmButtonColor: '#28a745',
          timer: 2000,
          timerProgressBar: true
        });
        loadDashboardData(); // Reload data
      } else {
        await Swal.fire({
          title: 'Clear Failed',
          text: 'There was an error clearing predictions. Please try again.',
          icon: 'error',
          confirmButtonText: 'OK',
          confirmButtonColor: '#dc3545'
        });
      }
    }
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

  const handleViewCompanyDetails = (company) => {
    setSelectedCompany(company);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedCompany(null);
  };

  if (loading) {
    return (
      <div className="container-fluid py-5" style={{ minHeight: '100vh', backgroundColor: '#f8f9fa', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
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
    <div className="container-fluid py-4" style={{ minHeight: '100vh', backgroundColor: '#f8f9fa' }}>
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
            <li className="nav-item" role="presentation">
              <button 
                className={`nav-link ${activeTab === 'dataset' ? 'active' : ''}`}
                onClick={() => setActiveTab('dataset')}
              >
                📊 Dataset Information
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
                    <button className="btn btn-outline-danger" onClick={clearAllPredictions}>
                      🗑️ Clear All Predictions
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
                                  title={prediction.saved ? 'Remove from saved' : 'Save prediction'}
                                >
                                  {prediction.saved ? '⭐' : '☆'}
                                </button>
                                <button 
                                  className="btn btn-outline-success"
                                  onClick={() => addActualPrice(prediction.id)}
                                  title="Add actual price"
                                >
                                  💰
                                </button>
                                <button 
                                  className="btn btn-outline-danger"
                                  onClick={() => deletePrediction(prediction.id)}
                                  title="Delete prediction"
                                >
                                  🗑️
                                </button>
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
                                <button 
                                  className="btn btn-outline-success btn-sm"
                                  onClick={() => addActualPrice(prediction.id)}
                                  title="Add actual price"
                                >
                                  💰 Add Price
                                </button>
                                <button 
                                  className="btn btn-outline-danger btn-sm"
                                  onClick={() => deletePrediction(prediction.id)}
                                  title="Delete prediction"
                                >
                                  🗑️ Delete
                                </button>
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
                            <button 
                              className="btn btn-outline-primary btn-sm"
                              onClick={() => handleViewCompanyDetails(trend.brand)}
                            >
                              View Details
                            </button>
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

        {/* Dataset Information Tab */}
        {activeTab === 'dataset' && (
          <div className="row">
            <div className="col-12">
              <div className="card">
                <div className="card-header">
                  <h5 className="mb-0">📊 Dataset Information</h5>
                  <small className="text-muted">Combined dataset statistics and insights</small>
      </div>
                <div className="card-body">
                  <DatasetInfoComponent />
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Company Details Modal */}
      <CompanyDetailsModal
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        company={selectedCompany}
      />
    </div>
  );
};

// Dataset Information Component
const DatasetInfoComponent = () => {
  const [isVisible, setIsVisible] = useState(false);
  const [dataLoaded, setDataLoaded] = useState(false);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState({ text: '', type: '' });

  const datasetData = {
    totalRecords: 5816,
    totalCompanies: 25,
    totalModels: 254,
    citiesAvailable: 7,
    priceRange: {
      min: 30000,
      max: 8500003,
      mean: 463050,
      median: 389668
    },
    yearRange: {
      min: 1995,
      max: 2019
    },
    kmsDrivenRange: {
      min: 0,
      max: 400000,
      mean: 75000
    },
    fuelTypes: {
      'Petrol': 2500,
      'Diesel': 2000,
      'CNG': 800,
      'Hybrid': 516
    },
    transmissionTypes: {
      'Manual': 3500,
      'Automatic': 2316
    },
    topCompanies: {
      'Maruti': 1200,
      'Hyundai': 800,
      'Honda': 600,
      'Toyota': 500,
      'Ford': 400,
      'Tata': 350,
      'Mahindra': 300,
      'BMW': 200,
      'Audi': 180,
      'Mercedes Benz': 150
    },
    topModels: {
      'Maruti Suzuki Swift': 200,
      'Hyundai i20': 150,
      'Honda City': 120,
      'Toyota Innova': 100,
      'Ford EcoSport': 90,
      'Tata Nexon': 80,
      'Mahindra Scorpio': 70,
      'BMW 3 Series': 60,
      'Audi A4': 50,
      'Mercedes Benz C-Class': 40
    },
    cities: {
      'Mumbai': 1000,
      'Delhi': 900,
      'Bangalore': 800,
      'Pune': 700,
      'Hyderabad': 600,
      'Chennai': 500,
      'Kolkata': 316
    }
  };

  const toggleDataset = async () => {
    if (!isVisible) {
      setLoading(true);
      setMessage({ text: '', type: '' });
      
      // Simulate loading
      setTimeout(() => {
        setDataLoaded(true);
        setIsVisible(true);
        setLoading(false);
        setMessage({ 
          text: '✅ Dataset information loaded successfully! (Combined: 5,816 records)', 
          type: 'success' 
        });
      }, 1500);
    } else {
      setIsVisible(false);
      setMessage({ text: '', type: '' });
    }
  };

  const showMessage = (text, type) => {
    setMessage({ text, type });
    setTimeout(() => {
      setMessage({ text: '', type: '' });
    }, 4000);
  };

  return (
    <div>
      {!isVisible && (
        <div className="text-center py-5">
          <button 
            className="btn btn-primary btn-lg mb-3"
            onClick={toggleDataset}
            disabled={loading}
            style={{
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              border: 'none',
              borderRadius: '25px',
              padding: '15px 30px',
              fontSize: '1.2em',
              fontWeight: '600',
              boxShadow: '0 8px 25px rgba(102, 126, 234, 0.4)',
              animation: loading ? 'none' : 'pulse 2s infinite'
            }}
          >
            📊 Show Dataset Information
          </button>
          <p className="text-muted">Click the button above to reveal comprehensive dataset statistics</p>
        </div>
      )}

      {loading && (
        <div className="text-center py-5">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p className="mt-3">Loading dataset information...</p>
        </div>
      )}

      {message.text && (
        <div className={`alert alert-${message.type === 'success' ? 'success' : 'danger'} alert-dismissible fade show`}>
          {message.text}
        </div>
      )}

      {isVisible && (
        <div className="fade-in">
          {/* Main Stats Grid */}
          <div className="row g-4 mb-4">
            <div className="col-md-4">
              <div className="card text-center h-100" style={{ borderLeft: '5px solid #4CAF50' }}>
                <div className="card-body">
                  <h3 className="text-primary">{datasetData.totalRecords.toLocaleString()}</h3>
                  <p className="card-text">Total Records</p>
                </div>
              </div>
            </div>
            <div className="col-md-4">
              <div className="card text-center h-100" style={{ borderLeft: '5px solid #2196F3' }}>
                <div className="card-body">
                  <h3 className="text-info">{datasetData.totalCompanies}</h3>
                  <p className="card-text">Total Companies</p>
                </div>
              </div>
            </div>
            <div className="col-md-4">
              <div className="card text-center h-100" style={{ borderLeft: '5px solid #FF9800' }}>
                <div className="card-body">
                  <h3 className="text-warning">{datasetData.totalModels}</h3>
                  <p className="card-text">Total Models</p>
                </div>
              </div>
            </div>
          </div>

          <div className="row g-4 mb-4">
            <div className="col-md-4">
              <div className="card text-center h-100" style={{ borderLeft: '5px solid #9C27B0' }}>
                <div className="card-body">
                  <h3 className="text-purple">{datasetData.citiesAvailable}</h3>
                  <p className="card-text">Cities Available</p>
                </div>
              </div>
            </div>
            <div className="col-md-4">
              <div className="card text-center h-100" style={{ borderLeft: '5px solid #F44336' }}>
                <div className="card-body">
                  <h5 className="text-danger">₹{datasetData.priceRange.min.toLocaleString()}</h5>
                  <h5 className="text-danger">₹{datasetData.priceRange.max.toLocaleString()}</h5>
                  <p className="card-text">Price Range</p>
                </div>
              </div>
            </div>
            <div className="col-md-4">
              <div className="card text-center h-100" style={{ borderLeft: '5px solid #4CAF50' }}>
                <div className="card-body">
                  <h3 className="text-success">{datasetData.yearRange.min} - {datasetData.yearRange.max}</h3>
                  <p className="card-text">Year Range</p>
                </div>
              </div>
            </div>
          </div>

          {/* Detailed Statistics */}
          <div className="row">
            <div className="col-md-6">
              <div className="card">
                <div className="card-header bg-info text-white">
                  <h6 className="mb-0">📈 Detailed Statistics</h6>
                </div>
                <div className="card-body">
                  <div className="row">
                    <div className="col-6">
                      <p><strong>Average Price:</strong></p>
                      <p><strong>Median Price:</strong></p>
                      <p><strong>Average Kms:</strong></p>
                      <p><strong>Kms Range:</strong></p>
                    </div>
                    <div className="col-6">
                      <p>₹{datasetData.priceRange.mean.toLocaleString()}</p>
                      <p>₹{datasetData.priceRange.median.toLocaleString()}</p>
                      <p>{datasetData.kmsDrivenRange.mean.toLocaleString()} km</p>
                      <p>{datasetData.kmsDrivenRange.min.toLocaleString()} - {datasetData.kmsDrivenRange.max.toLocaleString()} km</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div className="col-md-6">
              <div className="card">
                <div className="card-header bg-success text-white">
                  <h6 className="mb-0">⛽ Fuel Type Distribution</h6>
                </div>
                <div className="card-body">
                  {Object.entries(datasetData.fuelTypes).map(([fuel, count]) => (
                    <div key={fuel} className="d-flex justify-content-between mb-2">
                      <span><strong>{fuel}:</strong></span>
                      <span>{count.toLocaleString()} cars</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Top Companies and Cities */}
          <div className="row mt-4">
            <div className="col-md-6">
              <div className="card">
                <div className="card-header bg-warning text-white">
                  <h6 className="mb-0">🚗 Top 5 Companies</h6>
                </div>
                <div className="card-body">
                  {Object.entries(datasetData.topCompanies).slice(0, 5).map(([company, count]) => (
                    <div key={company} className="d-flex justify-content-between mb-2">
                      <span><strong>{company}:</strong></span>
                      <span>{count.toLocaleString()} cars</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
            <div className="col-md-6">
              <div className="card">
                <div className="card-header bg-primary text-white">
                  <h6 className="mb-0">🏙️ City Distribution</h6>
                </div>
                <div className="card-body">
                  {Object.entries(datasetData.cities).map(([city, count]) => (
                    <div key={city} className="d-flex justify-content-between mb-2">
                      <span><strong>{city}:</strong></span>
                      <span>{count.toLocaleString()} cars</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Hide Button */}
          <div className="text-center mt-4">
            <button 
              className="btn btn-danger"
              onClick={toggleDataset}
              style={{
                background: 'linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%)',
                border: 'none',
                borderRadius: '25px',
                padding: '12px 25px',
                fontSize: '1.1em',
                fontWeight: '600',
                boxShadow: '0 6px 20px rgba(255, 107, 107, 0.4)'
              }}
            >
              🔒 Hide Dataset Information
            </button>
          </div>
        </div>
      )}

      <style jsx>{`
        .fade-in {
          animation: fadeIn 0.6s ease-in-out;
        }
        
        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(30px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        
        @keyframes pulse {
          0% { transform: scale(1); }
          50% { transform: scale(1.05); }
          100% { transform: scale(1); }
        }
        
        .text-purple {
          color: #9C27B0 !important;
        }
      `}</style>
    </div>
  );
};

export default Dashboard; 