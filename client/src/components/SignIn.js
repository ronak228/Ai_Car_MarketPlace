import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { supabase } from '../supabaseClient';
import PasswordReset from './PasswordReset';

const SignIn = ({ onLogin, isSignUp = false }) => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    name: ''
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [isSignUpMode, setIsSignUpMode] = useState(isSignUp);
  const [showPasswordReset, setShowPasswordReset] = useState(false);
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
        // Simple signup without OTP verification
        console.log('Attempting signup for:', formData.email);

        const signUpResponse = await supabase.auth.signUp({
          email: formData.email,
          password: formData.password,
          options: {
            data: {
              full_name: formData.name
            }
          }
        });

        if (signUpResponse.error) {
          console.log('Signup error:', signUpResponse.error.message);
          const errorMessage = signUpResponse.error.message.toLowerCase();
          if (errorMessage.includes('already registered') || 
              errorMessage.includes('already exists') ||
              errorMessage.includes('user already registered')) {
            throw new Error('An account with this email already exists. Please sign in instead.');
          }
          throw signUpResponse.error;
        }

        if (!signUpResponse.data.user) {
          throw new Error('Failed to create account. Please try again.');
        }

        // Auto-login after successful signup
        const userData = {
          id: signUpResponse.data.user.id,
          email: signUpResponse.data.user.email,
          name: formData.name || signUpResponse.data.user.email?.split('@')[0] || 'User',
          token: `token-${Date.now()}`
        };
        
        console.log('Signup successful, auto-logging in:', userData);
        onLogin(userData);
        navigate('/dashboard');
        return;
      } else {
        // Simple signin
        console.log('Attempting signin for:', formData.email);

        const signInResponse = await supabase.auth.signInWithPassword({
          email: formData.email,
          password: formData.password
        });

        if (signInResponse.error) {
          console.log('Signin error:', signInResponse.error.message);
          throw signInResponse.error;
        }

        if (!signInResponse.data.user) {
          throw new Error('Sign in failed. Please try again.');
        }

        // Login successful
        const userData = {
          id: signInResponse.data.user.id,
          email: signInResponse.data.user.email,
          name: signInResponse.data.user.user_metadata?.full_name || signInResponse.data.user.email?.split('@')[0] || 'User',
          token: signInResponse.data.session?.access_token || `token-${Date.now()}`
        };
        
        console.log('Signin successful:', userData);
        onLogin(userData);
        navigate('/dashboard');
        return;
      }
    } catch (error) {
      console.error('Authentication error:', error);
      setError(error.message || 'An error occurred during authentication');
    } finally {
      setIsLoading(false);
    }
  };

  if (showPasswordReset) {
    return (
      <PasswordReset 
        onComplete={handlePasswordResetComplete}
        onBack={handleBackFromPasswordReset}
      />
    );
  }

  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-md-6 col-lg-5">
          <div className="card shadow">
            <div className="card-header text-center bg-primary text-white">
              <h4>{isSignUpMode ? 'Sign Up' : 'Sign In'}</h4>
            </div>
            <div className="card-body">
              {error && (
                <div className="alert alert-danger" role="alert">
                  {error}
                </div>
              )}

              <form onSubmit={handleSubmit}>
                {isSignUpMode && (
                  <div className="mb-3">
                    <label htmlFor="name" className="form-label">Full Name</label>
                    <input
                      type="text"
                      className="form-control"
                      id="name"
                      name="name"
                      value={formData.name}
                      onChange={handleChange}
                      placeholder="Enter your full name"
                      required
                    />
                  </div>
                )}

                <div className="mb-3">
                  <label htmlFor="email" className="form-label">Email</label>
                  <input
                    type="email"
                    className="form-control"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    placeholder="Enter your email"
                    required
                  />
                </div>

                <div className="mb-3">
                  <label htmlFor="password" className="form-label">Password</label>
                  <div className="input-group">
                    <input
                      type={showPassword ? "text" : "password"}
                      className="form-control"
                      id="password"
                      name="password"
                      value={formData.password}
                      onChange={handleChange}
                      placeholder="Enter your password"
                      required
                    />
                    <button
                      type="button"
                      className="btn btn-outline-secondary"
                      onClick={() => setShowPassword(!showPassword)}
                    >
                      {showPassword ? '👁️' : '👁️‍🗨️'}
                    </button>
                  </div>
                </div>

                <div className="d-grid gap-2">
                  <button
                    type="submit"
                    className="btn btn-primary"
                    disabled={isLoading}
                  >
                    {isLoading ? (
                      <>
                        <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                        {isSignUpMode ? 'Signing Up...' : 'Signing In...'}
                      </>
                    ) : (
                      isSignUpMode ? 'Sign Up' : 'Sign In'
                    )}
                  </button>
                </div>
              </form>

              {!isSignUpMode && (
                <div className="text-center mt-3">
                  <button
                    type="button"
                    className="btn btn-link"
                    onClick={() => setShowPasswordReset(true)}
                  >
                    Forgot Password?
                  </button>
                </div>
              )}

              <div className="text-center mt-3">
                <small className="text-muted">
                  {isSignUpMode ? 'Already have an account?' : "Don't have an account?"}{' '}
                  <a href={isSignUpMode ? '/signin' : '/signup'}>
                    {isSignUpMode ? 'Sign In' : 'Sign Up'}
                  </a>
                </small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SignIn;