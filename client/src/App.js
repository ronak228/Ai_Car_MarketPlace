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

  const handleLogin = (userData) => {
    setIsAuthenticated(true);
    setUser(userData);
    localStorage.setItem('token', userData.token);
    localStorage.setItem('user', JSON.stringify(userData));
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    setUser(null);
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  };

  React.useEffect(() => {
    try {
      const token = localStorage.getItem('token');
      const userData = localStorage.getItem('user');
      
      console.log('Checking auth state:', { token, userData });
      
      if (token && userData && userData !== 'undefined' && userData !== 'null') {
        try {
          const parsedUser = JSON.parse(userData);
          console.log('Parsed user data:', parsedUser);
          
          // Validate user data structure
          if (parsedUser && parsedUser.id && parsedUser.email) {
            setIsAuthenticated(true);
            setUser(parsedUser);
            console.log('User authenticated successfully');
          } else {
            console.log('Invalid user data structure, clearing storage');
            localStorage.removeItem('token');
            localStorage.removeItem('user');
          }
        } catch (parseError) {
          console.error('Error parsing user data:', parseError);
          // Clear invalid data
          localStorage.removeItem('token');
          localStorage.removeItem('user');
        }
      } else {
        console.log('No valid auth data found');
      }
    } catch (error) {
      console.error('Error accessing localStorage:', error);
    }
  }, []);

  return (
    <ErrorBoundary>
      <Router>
        <div className="App">
          <Navbar isAuthenticated={isAuthenticated} onLogout={handleLogout} user={user} />
          <Routes>
            <Route path="/" element={<Home isAuthenticated={isAuthenticated} />} />
            <Route path="/signin" element={<SignIn onLogin={handleLogin} isSignUp={false} />} />
            <Route path="/signup" element={<SignIn onLogin={handleLogin} isSignUp={true} />} />
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
