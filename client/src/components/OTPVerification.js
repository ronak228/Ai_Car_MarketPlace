import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const OTPVerification = ({ email, verificationType = 'signup', onVerificationComplete, onBack }) => {
  const navigate = useNavigate();
  const { verifyOtp, signInWithOtp } = useAuth();
  const [otp, setOtp] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [timeLeft, setTimeLeft] = useState(60);
  const [canResend, setCanResend] = useState(false);
  const [attempts, setAttempts] = useState(0);
  const [maxAttempts] = useState(3);

  useEffect(() => {
    if (timeLeft > 0) {
      const timer = setTimeout(() => setTimeLeft(timeLeft - 1), 1000);
      return () => clearTimeout(timer);
    } else {
      setCanResend(true);
    }
  }, [timeLeft]);

  const handleOTPChange = (e) => {
    const value = e.target.value.replace(/\D/g, '').slice(0, 6);
    setOtp(value);
  };

  const handleVerifyOTP = async (e) => {
    e.preventDefault();
    
    if (attempts >= maxAttempts) {
      setError(`Maximum attempts reached. Please request a new OTP.`);
      return;
    }

    if (otp.length !== 6) {
      setError('Please enter a 6-digit OTP code.');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      console.log('Verifying OTP:', { email, otp, verificationType });
      
      // Use the authentication context to verify OTP
      const { data, error } = await verifyOtp(email, otp, verificationType === 'signup' ? 'signup' : 'email');

      if (error) {
        setAttempts(attempts + 1);
        
        // Provide more specific error messages
        if (error.message.includes('Invalid token') || error.message.includes('expired')) {
          throw new Error(`Invalid or expired OTP. ${maxAttempts - attempts - 1} attempts remaining.`);
        } else if (error.message.includes('429') || error.message.includes('rate limit')) {
          throw new Error('Rate limit reached. Please wait 1 minute before trying again.');
        } else if (error.message.includes('already been used')) {
          throw new Error('This OTP has already been used. Please request a new one.');
        } else if (error.message.includes('not found')) {
          throw new Error('OTP not found. Please check the code and try again.');
        } else {
          throw new Error(`Verification failed: ${error.message}`);
        }
      }

      if (data?.user) {
        console.log('OTP verification successful:', data.user);
        
        // Determine the verification type for success message
        const successMessage = verificationType === 'signup' 
          ? 'Account created successfully! Redirecting to dashboard...'
          : 'Sign in successful! Redirecting to dashboard...';
        
        setSuccess(successMessage);
        
        // Call the completion handler after a short delay
        setTimeout(() => {
          onVerificationComplete(data.user);
        }, 2000);
      } else {
        throw new Error('Verification failed. Please try again.');
      }

    } catch (err) {
      console.error('OTP verification error:', err);
      setError(err.message || 'Verification failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleResendOTP = async () => {
    setIsLoading(true);
    setError('');
    setSuccess('');
    setOtp('');
    setAttempts(0);
    setTimeLeft(60);
    setCanResend(false);

    try {
      const { error } = await signInWithOtp(email);
      
      if (error) {
        if (error.message.includes('429') || error.message.includes('rate limit')) {
          throw new Error('Rate limit reached. Please wait 1 minute before trying again.');
        }
        throw error;
      }

      setSuccess('New OTP sent successfully!');
    } catch (err) {
      setError(err.message || 'Failed to resend OTP. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="card-body">
          <div className="auth-header">
            <div className="auth-logo">
              <span className="auth-logo-icon">📧</span>
              <span className="auth-logo-text">Verify Email</span>
            </div>
            <h2 className="auth-title">Enter Verification Code</h2>
            <p className="auth-subtitle">
              We've sent a 6-digit code to <strong>{email}</strong>
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
            </div>
          )}

          {success && (
            <div className="auth-alert auth-alert-success" role="alert">
              <div className="d-flex align-items-center">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" className="me-2">
                  <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM10 17L5 12L6.41 10.59L10 14.17L17.59 6.58L19 8L10 17Z" fill="currentColor"/>
                </svg>
                <span>{success}</span>
              </div>
            </div>
          )}

          <form onSubmit={handleVerifyOTP}>
            <div className="auth-form-group">
              <label htmlFor="otp">Verification Code</label>
              <input
                type="text"
                className="auth-input text-center"
                id="otp"
                placeholder="000000"
                value={otp}
                onChange={handleOTPChange}
                maxLength={6}
                style={{ fontSize: '1.5rem', letterSpacing: '0.5rem' }}
                required
              />
              <small className="text-muted">
                Enter the 6-digit code sent to your email
              </small>
            </div>

            <button
              type="submit"
              className="auth-submit-btn"
              disabled={isLoading || otp.length !== 6}
            >
              {isLoading && <span className="auth-loading"></span>}
              {isLoading ? 'Verifying...' : 'Verify Code'}
            </button>
          </form>

          <div className="text-center mt-3">
            <p className="text-muted">
              Didn't receive the code? 
              {canResend ? (
                <button
                  type="button"
                  className="auth-link-btn"
                  onClick={handleResendOTP}
                  disabled={isLoading}
                >
                  Resend Code
                </button>
              ) : (
                <span className="text-muted">
                  {' '}Resend in {timeLeft}s
                </span>
              )}
            </p>
          </div>

          <div className="text-center mt-3">
            <button
              type="button"
              className="auth-toggle-btn"
              onClick={onBack}
              disabled={isLoading}
            >
              ← Back to {verificationType === 'signup' ? 'Sign Up' : 'Sign In'}
            </button>
          </div>

          {/* Attempts counter */}
          {attempts > 0 && (
            <div className="text-center mt-3">
              <small className="text-warning">
                Attempts: {attempts}/{maxAttempts}
              </small>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default OTPVerification;