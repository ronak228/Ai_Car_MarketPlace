import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

// Components
import Navbar from './components/Navbar';
import Home from './components/Home';
import SignIn from './components/SignIn';
import Dashboard from './components/Dashboard';
import CarPricePredictor from './components/CarPricePredictor';
import SupabaseTest from './components/SupabaseTest';

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
  const [isAuthenticated, setIsAuthenticated] = React.useState(false);
  const [user, setUser] = React.useState(null);
  const [isLoading, setIsLoading] = React.useState(true);

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

  const handleLogout = () => {
    console.log('Handling logout');
    setIsAuthenticated(false);
    setUser(null);
    
    // Clear all authentication data
    localStorage.removeItem('auth_token');
    localStorage.removeItem('auth_user');
    localStorage.removeItem('auth_timestamp');
    
    console.log('User logged out successfully');
  };

  // Check authentication state on app load
  React.useEffect(() => {
    const checkAuthState = async () => {
      try {
        setIsLoading(true);
        
        const token = localStorage.getItem('auth_token');
        const userData = localStorage.getItem('auth_user');
        const timestamp = localStorage.getItem('auth_timestamp');
        
        console.log('Checking auth state:', { 
          hasToken: !!token, 
          hasUserData: !!userData, 
          timestamp: timestamp ? new Date(parseInt(timestamp)).toLocaleString() : 'none'
        });
        
        // Check if token exists and is not expired (24 hours)
        if (token && userData && timestamp) {
          const tokenAge = Date.now() - parseInt(timestamp);
          const maxAge = 24 * 60 * 60 * 1000; // 24 hours
          
          if (tokenAge < maxAge) {
            try {
              const parsedUser = JSON.parse(userData);
              console.log('Parsed user data:', parsedUser);
              
              // Validate user data structure
              if (parsedUser && parsedUser.id && parsedUser.email) {
                setIsAuthenticated(true);
                setUser(parsedUser);
                console.log('✅ User authenticated successfully from localStorage');
              } else {
                console.log('❌ Invalid user data structure, clearing storage');
                clearAuthData();
              }
            } catch (parseError) {
              console.error('❌ Error parsing user data:', parseError);
              clearAuthData();
            }
          } else {
            console.log('❌ Token expired, clearing storage');
            clearAuthData();
          }
        } else {
          console.log('❌ No valid auth data found');
          clearAuthData();
        }
      } catch (error) {
        console.error('❌ Error checking auth state:', error);
        clearAuthData();
      } finally {
        setIsLoading(false);
      }
    };

    const clearAuthData = () => {
      localStorage.removeItem('auth_token');
      localStorage.removeItem('auth_user');
      localStorage.removeItem('auth_timestamp');
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
                isAuthenticated ? <Navigate to="/dashboard" /> : <SignIn onLogin={handleLogin} isSignUp={false} />
              } 
            />
            <Route 
              path="/signup" 
              element={
                isAuthenticated ? <Navigate to="/dashboard" /> : <SignIn onLogin={handleLogin} isSignUp={true} />
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
            <Route path="/test" element={<SupabaseTest />} />
          </Routes>
        </div>
      </Router>
    </ErrorBoundary>
  );
}

export default App;
