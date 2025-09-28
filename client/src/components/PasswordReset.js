import React, { useState } from 'react';
import { supabase } from '../supabaseClient';

const PasswordReset = ({ onBack, onResetComplete }) => {
  const [email, setEmail] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      const response = await supabase.auth.resetPasswordForEmail(email, {
        redirectTo: `${window.location.origin}/reset-password`
      });

      const { error } = response;

      if (error) {
        throw error;
      }

      setSuccess('Password reset link sent to your email! Please check your inbox.');
      setTimeout(() => {
        onResetComplete();
      }, 3000);
    } catch (err) {
      setError(err.message || 'Failed to send reset link. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleBack = () => {
    onBack();
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="card-body">
          <h2 className="auth-title">Reset Password</h2>
          
          <p className="text-center mb-4">
            Enter your email address and we'll send you a link to reset your password.
          </p>

          {error && (
            <div className="auth-alert auth-alert-danger" role="alert">
              {error}
            </div>
          )}

          {success && (
            <div className="auth-alert auth-alert-success" role="alert">
              {success}
            </div>
          )}

          <form onSubmit={handleSubmit}>
            <div className="auth-form-group">
              <label htmlFor="email">Email Address</label>
              <input
                type="email"
                className="auth-input"
                id="email"
                name="email"
                placeholder="Enter your email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            
            <button
              type="submit"
              className="auth-submit-btn"
              disabled={isLoading}
            >
              {isLoading && <span className="auth-loading"></span>}
              {isLoading ? 'Sending...' : 'Send Reset Link'}
            </button>
          </form>

          <div className="text-center mt-3">
            <button
              className="auth-toggle-btn"
              onClick={handleBack}
            >
              Back to Sign In
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PasswordReset;
