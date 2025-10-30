import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

const Home = ({ isAuthenticated }) => {
  const navigate = useNavigate();

  const handleGetStarted = () => {
    console.log('Button clicked!'); // Debug log
    if (isAuthenticated) {
      console.log('User is authenticated, navigating to predictor'); // Debug log
      navigate('/car-price-predictor');
    } else {
      console.log('User not authenticated, navigating to signin'); // Debug log
      navigate('/signin');
    }
  };

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f8f9fa' }}>
      {/* Hero Section */}
      <div className="bg-primary text-white py-5">
        <div className="container-fluid">
          <div className="row align-items-center">
            <div className="col-lg-6">
              <h1 className="display-4 fw-bold mb-4">
                <i className="fas fa-robot me-3"></i>CarCrafter AI
              </h1>
              <p className="lead mb-4">
                Advanced AI-powered car price prediction with real-time market analysis. 
                Get accurate predictions for all Indian car brands including EVs, with confidence scores and market trends.
              </p>
              <div className="d-flex gap-3">
                <button onClick={handleGetStarted} className="btn btn-light btn-lg">
                  {isAuthenticated ? 'Go to Predictor' : 'Get Started'}
                </button>
                {!isAuthenticated && (
                <Link to="/signin" className="btn btn-outline-light btn-lg">
                  <i className="fas fa-sign-in-alt me-2"></i>Sign In
                </Link>
                )}
              </div>
            </div>
            <div className="col-lg-6 text-center">
              <div className="hero-feature-card">
                <div className="hero-icons">
                  <div className="hero-icon-item">
                    <span className="hero-icon">🤖</span>
                    <span className="hero-icon-label">AI Engine</span>
                  </div>
                  <div className="hero-icon-item">
                    <span className="hero-icon">📊</span>
                    <span className="hero-icon-label">Analytics</span>
                  </div>
                  <div className="hero-icon-item">
                    <span className="hero-icon">🎯</span>
                    <span className="hero-icon-label">Accuracy</span>
                  </div>
                </div>
                <h4 className="hero-feature-title">Advanced ML Prediction Engine</h4>
                <p className="hero-feature-desc">Powered by cutting-edge machine learning algorithms</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-5">
        <div className="container-fluid">
          <h2 className="text-center mb-5">Advanced Prediction Features</h2>
          <div className="row g-4">
            <div className="col-md-3">
              <div className="card h-100 border-0 shadow-sm">
                <div className="card-body text-center">
                  <div className="mb-3">
                    <h1>📈</h1>
                  </div>
                  <h5 className="card-title">Price Range Prediction</h5>
                  <p className="card-text">
                    Get min/max price ranges instead of single values for better decision making.
                  </p>
                </div>
              </div>
            </div>
            <div className="col-md-3">
              <div className="card h-100 border-0 shadow-sm">
                <div className="card-body text-center">
                  <div className="mb-3">
                    <h1>🎯</h1>
                  </div>
                  <h5 className="card-title">Confidence Score</h5>
                  <p className="card-text">
                    See how confident our model is with each prediction (e.g., 85% confidence).
                  </p>
                </div>
              </div>
            </div>
            <div className="col-md-3">
              <div className="card h-100 border-0 shadow-sm">
                <div className="card-body text-center">
                  <div className="mb-3">
                    <h1>📊</h1>
                  </div>
                  <h5 className="card-title">Market Trends</h5>
                  <p className="card-text">
                    Analyze if prices are rising or falling for specific car types.
                  </p>
                </div>
              </div>
            </div>
            <div className="col-md-3">
              <div className="card h-100 border-0 shadow-sm">
                <div className="card-body text-center">
                  <div className="mb-3">
                    <h1>🔍</h1>
                  </div>
                  <h5 className="card-title">Model Comparison</h5>
                  <p className="card-text">
                    Compare predictions from different ML models for accuracy.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* How It Works Section */}
      <div className="bg-light py-5">
        <div className="container-fluid">
          <h2 className="text-center mb-5">How It Works</h2>
          <div className="row g-4">
            <div className="col-md-4">
              <div className="text-center">
                <div className="bg-primary text-white rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style={{width: '60px', height: '60px'}}>
                  <h4 className="mb-0">1</h4>
                </div>
                <h5>Sign Up & Login</h5>
                <p>Create your account to access our advanced prediction tools.</p>
              </div>
            </div>
            <div className="col-md-4">
              <div className="text-center">
                <div className="bg-primary text-white rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style={{width: '60px', height: '60px'}}>
                  <h4 className="mb-0">2</h4>
                </div>
                <h5>Enter Car Details</h5>
                <p>Provide car specifications like brand, model, year, mileage, etc.</p>
              </div>
            </div>
            <div className="col-md-4">
              <div className="text-center">
                <div className="bg-primary text-white rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style={{width: '60px', height: '60px'}}>
                  <h4 className="mb-0">3</h4>
                </div>
                <h5>Get Smart Predictions</h5>
                <p>Receive accurate price predictions with confidence scores and market insights.</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="py-5">
        <div className="container-fluid text-center">
          <h3 className="mb-4">Ready to Predict Car Prices?</h3>
          <p className="lead mb-4">
            Join our platform and get access to advanced AI-powered car price predictions.
          </p>
          <button onClick={handleGetStarted} className="btn btn-primary btn-lg">
            {isAuthenticated ? 'Go to Predictor' : 'Start Predicting Now'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Home;