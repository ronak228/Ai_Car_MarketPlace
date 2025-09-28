import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import OTPVerification from './OTPVerification';
import PasswordReset from './PasswordReset';

const SignIn = ({ isSignUp = false }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const { signUp, signIn, signInWithOtp, resetPassword } = useAuth();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    name: ''
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [isSignUpMode, setIsSignUpMode] = useState(isSignUp);
  const [showOTPVerification, setShowOTPVerification] = useState(false);
  const [showPasswordReset, setShowPasswordReset] = useState(false);
  const [verificationEmail, setVerificationEmail] = useState('');
  const [verificationType, setVerificationType] = useState('signup');
  const [authMethod, setAuthMethod] = useState('password'); // 'password' or 'otp'
  const [showPassword, setShowPassword] = useState(false);

  // Update mode when prop changes
  React.useEffect(() => {
    setIsSignUpMode(isSignUp);
  }, [isSignUp]);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleVerificationComplete = (user) => {
    const userData = {
      id: user.id,
      email: user.email,
      name: user.user_metadata?.full_name || user.email?.split('@')[0] || 'User',
      token: user.access_token
    };
    onLogin(userData);
    navigate('/dashboard');
  };

  const handleBackFromOTP = () => {
    setShowOTPVerification(false);
    setVerificationEmail('');
    setVerificationType('signup');
  };

  const handlePasswordResetComplete = () => {
    setShowPasswordReset(false);
  };

  const handleBackFromPasswordReset = () => {
    setShowPasswordReset(false);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      if (isSignUpMode) {
        // Sign up with password
        const { data, error } = await signUp(formData.email, formData.password, formData.name);
        
        if (error) {
          const errorMessage = error.message.toLowerCase();
          if (errorMessage.includes('already registered') || 
              errorMessage.includes('already exists') ||
              errorMessage.includes('user already registered') ||
              errorMessage.includes('email already confirmed')) {
            throw new Error('An account with this email already exists. Please sign in instead.');
          }
          throw error;
        }

        // Send OTP for verification
        const { error: otpError } = await signInWithOtp(formData.email);
        
        if (otpError) {
          if (otpError.message.includes('429') || otpError.message.includes('rate limit')) {
            throw new Error('Rate limit reached. Please wait 1 minute before trying again.');
          }
          throw otpError;
        }

        setVerificationEmail(formData.email);
        setVerificationType('signup');
        setShowOTPVerification(true);
      } else {
        // Sign in
        if (authMethod === 'password') {
          const { data, error } = await signIn(formData.email, formData.password);
          
          if (error) {
            throw error;
          }

          // Redirect to intended page or dashboard
          const from = location.state?.from?.pathname || '/dashboard';
          navigate(from, { replace: true });
        } else {
          // OTP authentication
          const { error } = await signInWithOtp(formData.email);
          
          if (error) {
            if (error.message.includes('429') || error.message.includes('rate limit')) {
              throw new Error('Rate limit reached. Please wait 1 minute before trying again.');
            }
            throw error;
          }

          setVerificationEmail(formData.email);
          setVerificationType('signin');
          setShowOTPVerification(true);
        }
      }
    } catch (err) {
      setError(err.message || 'An error occurred. Please try again.');
      setShowOTPVerification(false);
      setVerificationEmail('');
      setVerificationType('signup');
    } finally {
      setIsLoading(false);
    }
  };

  // Show OTP verification if needed
  if (showOTPVerification) {
    // ADDITIONAL SAFETY CHECK: Don't show OTP for existing users
    if (error && error.includes('already exists')) {
      return (
        <div className="auth-container">
          <div className="auth-card">
            <div className="card-body">
              <h2 className="auth-title">Account Already Exists</h2>
              <div className="auth-alert auth-alert-danger" role="alert">
                <div className="d-flex align-items-center">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" className="me-2">
                    <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM13 17H11V15H13V17ZM13 13H11V7H13V13Z" fill="currentColor"/>
                  </svg>
                  <span>An account with this email already exists. Please sign in instead.</span>
                </div>
                <div className="mt-3">
                  <button
                    type="button"
                    className="btn btn-primary"
                    onClick={() => {
                      setShowOTPVerification(false);
                      setError('');
                      navigate('/signin');
                    }}
                  >
                    Go to Sign In
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      );
    }
    
    return (
      <OTPVerification
        email={verificationEmail}
        verificationType={verificationType}
        onVerificationComplete={handleVerificationComplete}
        onBack={handleBackFromOTP}
      />
    );
  }

  // Show password reset if needed
  if (showPasswordReset) {
    return (
      <PasswordReset
        onBack={handleBackFromPasswordReset}
        onResetComplete={handlePasswordResetComplete}
      />
    );
  }

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="card-body">
          <div className="auth-header">
            <div className="auth-logo">
              <span className="auth-logo-icon">🤖</span>
              <span className="auth-logo-text">CarPrice AI</span>
            </div>
            <h2 className="auth-title">
              {isSignUpMode ? 'Create Account' : 'Welcome Back'}
            </h2>
            <p className="auth-subtitle">
              {isSignUpMode 
                ? 'Join our platform and start predicting car prices with AI' 
                : 'Sign in to access your dashboard and prediction tools'
              }
            </p>
          </div>
          
          {error && (
            <div className="auth-alert auth-alert-danger" role="alert">
              <div className="d-flex align-items-center">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" className="me-2">
                  <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM13 17H11V15H13V17ZM13 13H11V7H13V13Z" fill="currentColor"/>
                </svg>
                <span>{error}</span>
              </div>
              {error.includes('already exists') && isSignUpMode && (
                <div className="mt-2">
                  <button
                    type="button"
                    className="btn btn-outline-primary btn-sm"
                    onClick={() => navigate('/signin')}
                  >
                    Go to Sign In
                  </button>
                </div>
              )}
            </div>
          )}

          <form onSubmit={handleSubmit}>
            {isSignUpMode && (
              <div className="auth-form-group">
                <label htmlFor="name">Full Name</label>
                <input
                  type="text"
                  className="auth-input"
                  id="name"
                  name="name"
                  placeholder="Enter your full name"
                  value={formData.name || ''}
                  onChange={handleChange}
                  required={isSignUpMode}
                />
              </div>
            )}
            
            {!isSignUpMode && (
              <div className="auth-form-group">
                <label className="auth-label">Authentication Method</label>
                <div className="auth-method-toggle">
                  <button
                    type="button"
                    className={`auth-method-btn ${authMethod === 'password' ? 'active' : ''}`}
                    onClick={() => setAuthMethod('password')}
                  >
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M12 2C13.1 2 14 2.9 14 4C14 5.1 13.1 6 12 6C10.9 6 10 5.1 10 4C10 2.9 10.9 2 12 2ZM21 9V7L15 1H5C3.89 1 3 1.89 3 3V21C3 22.11 3.89 23 5 23H19C20.11 23 21 22.11 21 21V9ZM19 9H14V4H5V21H19V9Z" fill="currentColor"/>
                    </svg>
                    Password
                  </button>
                  <button
                    type="button"
                    className={`auth-method-btn ${authMethod === 'otp' ? 'active' : ''}`}
                    onClick={() => setAuthMethod('otp')}
                  >
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM12 20C7.59 20 4 16.41 4 12C4 7.59 7.59 4 12 4C16.41 4 20 7.59 20 12C20 16.41 16.41 20 12 20ZM12 6C9.79 6 8 7.79 8 10C8 12.21 9.79 14 12 14C14.21 14 16 12.21 16 10C16 7.79 14.21 6 12 6ZM12 12C10.9 12 10 11.1 10 10C10 8.9 10.9 8 12 8C13.1 8 14 8.9 14 10C14 11.1 13.1 12 12 12Z" fill="currentColor"/>
                    </svg>
                    OTP
                  </button>
                </div>
              </div>
            )}
            
            <div className="auth-form-group">
              <label htmlFor="email">Email Address</label>
              <input
                type="email"
                className="auth-input"
                id="email"
                name="email"
                placeholder="Enter your email address"
                value={formData.email}
                onChange={handleChange}
                required
              />
            </div>
            
            {(isSignUpMode || authMethod === 'password') && (
              <div className="auth-form-group">
                <label htmlFor="password">Password</label>
                <div className="password-input-container">
                  <input
                    type={showPassword ? "text" : "password"}
                    className="auth-input"
                    id="password"
                    name="password"
                    placeholder="Enter your password"
                    value={formData.password}
                    onChange={handleChange}
                    required={isSignUpMode || authMethod === 'password'}
                  />
                  <button
                    type="button"
                    className="password-toggle-btn"
                    onClick={() => setShowPassword(!showPassword)}
                  >
                    {showPassword ? (
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12 4.5C7 4.5 2.73 7.61 1 12C2.73 16.39 7 19.5 12 19.5C17 19.5 21.27 16.39 23 12C21.27 7.61 17 4.5 12 4.5ZM12 17C9.24 17 7 14.76 7 12C7 9.24 9.24 7 12 7C14.76 7 17 9.24 17 12C17 14.76 14.76 17 12 17ZM12 9C10.34 9 9 10.34 9 12C9 13.66 10.34 15 12 15C13.66 15 15 13.66 15 12C15 10.34 13.66 9 12 9Z" fill="currentColor"/>
                      </svg>
                    ) : (
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12 7C14.76 7 17 9.24 17 12C17 12.65 16.87 13.26 16.64 13.83L19.56 16.75C21.07 15.49 22.26 13.86 22.99 12C21.26 7.61 17 4.5 12 4.5C10.94 4.5 9.93 4.67 9 4.97L11.17 7.14C11.45 7.05 11.72 7 12 7ZM2 4.27L3.28 3L20.72 20.44L19.44 21.72L17.29 19.57C15.91 20.41 14.05 21 12 21C7 21 2.73 17.89 1 13.5C1.73 11.64 2.92 10.01 4.43 8.75L2.27 6.59C1.53 7.84 1 9.38 1 12C1 15.76 3.24 18.5 7 18.5C8.06 18.5 9.07 18.33 10 18.03L7.83 15.86C7.55 15.95 7.28 16 7 16C4.24 16 2 13.76 2 11C2 9.38 2.53 7.84 3.28 6.59L2 4.27ZM7.53 9.8L9.25 11.52C9.26 11.67 9.25 11.83 9.25 12C9.25 13.66 10.59 15 12.25 15C12.42 15 12.58 14.99 12.73 14.98L14.45 16.7C14.04 16.89 13.53 17 13 17C10.24 17 8 14.76 8 12C8 11.47 8.11 10.96 8.3 10.55L7.53 9.8ZM11.84 9.02L14.7 11.88C14.71 11.93 14.71 11.97 14.71 12C14.71 13.66 13.37 15 11.71 15C11.66 15 11.62 15 11.57 14.99L8.7 12.12C8.69 12.07 8.69 12.03 8.69 12C8.69 10.34 10.03 9 11.69 9C11.74 9 11.78 9 11.84 9.02Z" fill="currentColor"/>
                      </svg>
                    )}
                  </button>
                </div>
                {!isSignUpMode && authMethod === 'password' && (
                  <div className="auth-forgot-password">
                    <button
                      type="button"
                      className="auth-forgot-btn"
                      onClick={() => setShowPasswordReset(true)}
                    >
                      Forgot your password?
                    </button>
                  </div>
                )}
              </div>
            )}
            
            {!isSignUpMode && authMethod === 'otp' && (
              <div className="auth-otp-notice">
                <div className="auth-otp-icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM12 20C7.59 20 4 16.41 4 12C4 7.59 7.59 4 12 4C16.41 4 20 7.59 20 12C20 16.41 16.41 20 12 20ZM11 7H13V9H11V7ZM11 11H13V17H11V11Z" fill="currentColor"/>
                  </svg>
                </div>
                <span className="auth-otp-text">
                  A verification code will be sent to your email address
                </span>
              </div>
            )}
            
            <button
              type="submit"
              className="auth-submit-btn"
              disabled={isLoading}
            >
              {isLoading && <span className="auth-loading"></span>}
              {isLoading ? 'Processing...' : (
                isSignUpMode ? 'Create Account' : 
                authMethod === 'password' ? 'Sign In' : 'Send Verification Code'
              )}
            </button>
          </form>

          <div className="text-center">
            <button
              className="auth-toggle-btn"
              onClick={() => {
                if (isSignUpMode) {
                  navigate('/signin');
                } else {
                  navigate('/signup');
                }
              }}
            >
              {isSignUpMode 
                ? 'Already have an account? Sign In' 
                : "Don't have an account? Sign Up"
              }
            </button>
          </div>

          {/* Authentication Mode Info */}
          <div className="text-center mt-3">
            <small className="text-muted">
              🔐 Choose your preferred authentication method
            </small>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SignIn; 