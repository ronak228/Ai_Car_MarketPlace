import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

// Components
import Navbar from './components/Navbar';
import Home from './components/Home';
import SignIn from './components/SignIn';
import CarPriceAI from './components/MongoSignIn';
import Dashboard from './components/Dashboard';
import CarPricePredictor from './components/CarCrafterPredictor';
import MarketTrends from './components/MarketTrends';
import RealTimeSalesDashboard from './components/RealTimeSalesDashboard';
import SupabaseTest from './components/SupabaseTest';

// MongoDB Auth Client
import mongoAuthClient from './mongoAuthClient';

// Error Boundary Component
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="container mt-5">
          <div className="alert alert-danger">
            <h4>Something went wrong!</h4>
            <p>The application encountered an error. Please try refreshing the page.</p>
            <button 
              className="btn btn-primary"
              onClick={() => {
                try {
                  localStorage.clear();
                } catch (e) {
                  console.error('Error clearing localStorage:', e);
                }
                window.location.reload();
              }}
            >
              Clear Data & Reload
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  const handleLogin = (userData) => {
    console.log('Handling login:', userData);
    setIsAuthenticated(true);
    setUser(userData);
    
    // Store authentication data
    localStorage.setItem('auth_token', userData.token);
    localStorage.setItem('auth_user', JSON.stringify(userData));
    localStorage.setItem('auth_timestamp', Date.now().toString());
    
    console.log('User logged in successfully');
  };

  const handleLogout = async () => {
    console.log('Handling logout');
    try {
      // Try MongoDB logout first
      if (mongoAuthClient.isAuthenticated()) {
        await mongoAuthClient.logout();
      }
    } catch (error) {
      console.error('MongoDB logout error:', error);
    }
    
    setIsAuthenticated(false);
    setUser(null);
    
    // Clear localStorage
    localStorage.removeItem('auth_token');
    localStorage.removeItem('auth_user');
    localStorage.removeItem('auth_timestamp');
    localStorage.removeItem('mongo_auth_token');
    localStorage.removeItem('mongo_auth_user');
    localStorage.removeItem('mongo_auth_timestamp');
    
    console.log('User logged out successfully');
  };

  // Check authentication state on app load
  useEffect(() => {
    const checkAuthState = async () => {
      try {
        setIsLoading(true);
        
        // Check MongoDB authentication first
        if (mongoAuthClient.isAuthenticated()) {
          try {
            const isValid = await mongoAuthClient.verifyToken();
            if (isValid) {
              const currentUser = mongoAuthClient.getCurrentUser();
              setIsAuthenticated(true);
              setUser(currentUser);
              console.log('[OK] User authenticated successfully with MongoDB');
            } else {
              console.log('[ERROR] MongoDB token verification failed');
              mongoAuthClient.clearAuthData();
              setIsAuthenticated(false);
              setUser(null);
            }
          } catch (error) {
            console.error('[ERROR] MongoDB auth check error:', error);
            mongoAuthClient.clearAuthData();
            setIsAuthenticated(false);
            setUser(null);
          }
        } else {
          // Fallback to Supabase/local auth
          const authToken = localStorage.getItem('auth_token');
          const authUser = localStorage.getItem('auth_user');
          const authTimestamp = localStorage.getItem('auth_timestamp');
          
          if (authToken && authUser && authTimestamp) {
            // Check if token is not expired (24 hours)
            const tokenAge = Date.now() - parseInt(authTimestamp);
            const maxAge = 24 * 60 * 60 * 1000; // 24 hours
            
            if (tokenAge < maxAge) {
              try {
                const userData = JSON.parse(authUser);
                setIsAuthenticated(true);
                setUser(userData);
                console.log('[OK] User authenticated successfully with Supabase');
              } catch (error) {
                console.error('[ERROR] Error parsing user data:', error);
                localStorage.clear();
                setIsAuthenticated(false);
                setUser(null);
              }
            } else {
              console.log('[INFO] Token expired, clearing auth data');
              localStorage.clear();
              setIsAuthenticated(false);
              setUser(null);
            }
          } else {
            console.log('[INFO] No valid auth data found');
            setIsAuthenticated(false);
            setUser(null);
          }
        }
      } catch (error) {
        console.error('[ERROR] Error checking auth state:', error);
        setIsAuthenticated(false);
        setUser(null);
      } finally {
        setIsLoading(false);
      }
    };

    checkAuthState();
  }, []);

  // Show loading screen while checking authentication
  if (isLoading) {
    return (
      <ErrorBoundary>
        <div className="App">
          <div className="container-fluid" style={{ minHeight: '100vh', backgroundColor: '#f8f9fa', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <div className="text-center">
              <div className="spinner-border text-primary mb-3" role="status" style={{ width: '3rem', height: '3rem' }}>
                <span className="visually-hidden">Loading...</span>
              </div>
              <h4 className="text-primary">Loading Car Price Predictor...</h4>
              <p className="text-muted">Checking authentication status</p>
            </div>
          </div>
        </div>
      </ErrorBoundary>
    );
  }

  return (
    <ErrorBoundary>
      <Router>
        <div className="App">
          <Navbar isAuthenticated={isAuthenticated} onLogout={handleLogout} user={user} />
          <Routes>
            <Route path="/" element={<Home isAuthenticated={isAuthenticated} />} />
            <Route 
              path="/signin" 
              element={
            isAuthenticated ? <Navigate to="/dashboard" /> : <CarPriceAI onLogin={handleLogin} isSignUp={false} />
              } 
            />
            <Route 
              path="/signup" 
              element={
            isAuthenticated ? <Navigate to="/dashboard" /> : <CarPriceAI onLogin={handleLogin} isSignUp={true} />
              } 
            />
            <Route 
              path="/mongo-signin" 
              element={
                isAuthenticated ? <Navigate to="/dashboard" /> : <CarPriceAI onLogin={handleLogin} isSignUp={false} />
              } 
            />
            <Route 
              path="/mongo-signup" 
              element={
                isAuthenticated ? <Navigate to="/dashboard" /> : <CarPriceAI onLogin={handleLogin} isSignUp={true} />
              } 
            />
            <Route 
              path="/dashboard" 
              element={
                isAuthenticated ? <Dashboard user={user} /> : <Navigate to="/signin" />
              } 
            />
            <Route 
              path="/car-price-predictor" 
              element={
                isAuthenticated ? <CarPricePredictor /> : <Navigate to="/signin" />
              } 
            />
            <Route 
              path="/market-trends" 
              element={
            isAuthenticated ? <RealTimeSalesDashboard /> : <Navigate to="/signin" />
              } 
            />
            <Route path="/test" element={<SupabaseTest />} />
          </Routes>
        </div>
      </Router>
    </ErrorBoundary>
  );
}

export default App;
