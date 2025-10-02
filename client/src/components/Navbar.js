import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';

const Navbar = ({ isAuthenticated, onLogout, user }) => {
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    onLogout();
    navigate('/');
  };

  const isOnSignInPage = location.pathname === '/signin';
  const isOnSignUpPage = location.pathname === '/signup';

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm">
      <div className="container">
        <Link className="navbar-brand d-flex align-items-center" to="/">
          <span className="navbar-brand-icon me-2">🤖</span>
          <span className="navbar-brand-text">CarPrice AI</span>
        </Link>
        
        <button 
          className="navbar-toggler" 
          type="button" 
          data-bs-toggle="collapse" 
          data-bs-target="#navbarNav"
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav me-auto">
            <li className="nav-item">
              <Link className="nav-link" to="/">
                Home
              </Link>
            </li>
            {isAuthenticated && (
              <>
                <li className="nav-item">
                  <Link className="nav-link" to="/dashboard">
                    Dashboard
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/car-price-predictor">
                    Price Predictor
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/market-trends">
                    <i className="fas fa-chart-line me-1"></i>
                    Market Trends
                  </Link>
                </li>
              </>
            )}
          </ul>
          
          <ul className="navbar-nav">
            {isAuthenticated ? (
              <>
                <li className="nav-item">
                  <span className="nav-link">
                    Welcome, {user?.name || 'User'}!
                  </span>
                </li>
                <li className="nav-item">
                  <button 
                    className="btn btn-outline-light btn-sm" 
                    onClick={handleLogout}
                  >
                    Logout
                  </button>
                </li>
              </>
            ) : (
              <li className="nav-item">
                {isOnSignInPage ? (
                  <Link className="btn btn-primary btn-sm" to="/signup">
                    Sign Up
                  </Link>
                ) : (
                  <Link className="btn btn-primary btn-sm" to="/signin">
                    Sign In
                  </Link>
                )}
              </li>
            )}
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Navbar; 