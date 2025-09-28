import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { supabase } from '../supabaseClient';

const OTPVerification = ({ email, verificationType = 'signup', onVerificationComplete, onBack }) => {
  const navigate = useNavigate();
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
      
      // Check if we're using local authentication
      const useLocalAuth = process.env.REACT_APP_USE_LOCAL_AUTH === 'true';
      const supabaseUrl = process.env.REACT_APP_SUPABASE_URL || 'YOUR_SUPABASE_URL';
      const supabaseAnonKey = process.env.REACT_APP_SUPABASE_ANON_KEY || 'YOUR_SUPABASE_ANON_KEY';
      
      if (useLocalAuth || supabaseUrl === 'YOUR_SUPABASE_URL' || supabaseAnonKey === 'YOUR_SUPABASE_ANON_KEY') {
        // Local authentication - accept any 6-digit code
        console.log('Using local authentication - accepting OTP');
        
        // Simulate verification delay
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        const mockUser = {
          id: 'local-user-' + Date.now(),
          email: email,
          user_metadata: { full_name: email.split('@')[0] }
        };
        
        setSuccess('Verification successful! Redirecting to dashboard...');
        setTimeout(() => {
          onVerificationComplete(mockUser);
        }, 2000);
        return;
      }
      
      // Try multiple verification approaches for real Supabase
      let response;
      let error;

      // First try: Use the specified verification type
      response = await supabase.auth.verifyOtp({
        email: email,
        token: otp,
        type: verificationType === 'signup' ? 'signup' : 'signin'
      });

      error = response.error;

      // If that fails, try alternative types
      if (error) {
        console.log('First verification attempt failed, trying alternatives');
        
        // Try 'email' type
        response = await supabase.auth.verifyOtp({
          email: email,
          token: otp,
          type: 'email'
        });
        
        error = response.error;
      }

      // If still fails, try 'magiclink' type
      if (error) {
        console.log('Second verification attempt failed, trying magiclink');
        
        response = await supabase.auth.verifyOtp({
          email: email,
          token: otp,
          type: 'magiclink'
        });
        
        error = response.error;
      }

      const { data } = response;
      console.log('OTP verification response:', { data, error });

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
        }
        
        throw new Error(`Verification failed: ${error.message}`);
      }

      if (data.user) {
        setSuccess('Verification successful! Redirecting to dashboard...');
        setTimeout(() => {
          onVerificationComplete(data.user);
        }, 2000);
      } else {
        throw new Error('Verification completed but no user data received.');
      }
    } catch (err) {
      console.error('OTP verification error:', err);
      setError(err.message || 'Invalid OTP. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleResendOTP = async () => {
    setIsLoading(true);
    setError('');
    setAttempts(0);

    try {
      console.log('Resending OTP to:', email);
      
      // Check if we're using local authentication
      const useLocalAuth = process.env.REACT_APP_USE_LOCAL_AUTH === 'true';
      const supabaseUrl = process.env.REACT_APP_SUPABASE_URL || 'YOUR_SUPABASE_URL';
      const supabaseAnonKey = process.env.REACT_APP_SUPABASE_ANON_KEY || 'YOUR_SUPABASE_ANON_KEY';
      
      if (useLocalAuth || supabaseUrl === 'YOUR_SUPABASE_URL' || supabaseAnonKey === 'YOUR_SUPABASE_ANON_KEY') {
        // Local authentication - simulate OTP resend
        console.log('Using local authentication - simulating OTP resend');
        
        // Simulate resend delay
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        setSuccess('New OTP sent successfully! (Local mode - any 6-digit code will work)');
        setTimeLeft(60);
        setCanResend(false);
        setOtp('');
        
        // Clear success message after 5 seconds
        setTimeout(() => {
          setSuccess('');
        }, 5000);
        return;
      }
      
      // Try different approaches for resending OTP with real Supabase
      let response;
      let error;

      // First try: Use signInWithOtp with email redirect
      response = await supabase.auth.signInWithOtp({
        email: email,
        options: {
          shouldCreateUser: false,
          emailRedirectTo: window.location.origin
        }
      });

      error = response.error;

      // If that fails, try with resend method
      if (error) {
        console.log('First attempt failed, trying resend method');
        response = await supabase.auth.resend({
          type: 'signin',
          email: email
        });
        error = response.error;
      }

      console.log('Resend OTP response:', { error });

      if (error) {
        if (error.message.includes('429') || error.message.includes('rate limit')) {
          throw new Error('Rate limit reached. Please wait 1 minute before trying again.');
        }
        if (error.message.includes('already been sent')) {
          setSuccess('OTP already sent! Please check your email and spam folder.');
        } else {
          throw error;
        }
      } else {
        setSuccess('New OTP sent successfully! Check your email and spam folder.');
      }

      setTimeLeft(60);
      setCanResend(false);
      setOtp('');
      
      // Clear success message after 5 seconds
      setTimeout(() => {
        setSuccess('');
      }, 5000);
    } catch (err) {
      setError(err.message || 'Failed to resend OTP. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleBackToSignIn = () => {
    onBack();
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="card-body">
          <h2 className="auth-title">
            {verificationType === 'signup' ? 'Email Verification' : 'Login Verification'}
          </h2>
          
          <p className="text-center mb-4">
            We've sent a 6-digit verification code to <strong>{email}</strong>
            <br />
            <small className="text-muted">
              Please check your email and spam folder. OTP may take 1-2 minutes to arrive.
            </small>
          </p>
          
          <div className="alert alert-info" role="alert">
            <strong>💡 Tips for faster OTP:</strong>
            <ul className="mb-0 mt-2">
              <li>Check your spam/junk folder</li>
              <li>Make sure you entered the correct email address</li>
              <li>Wait 1-2 minutes before requesting a new OTP</li>
              <li>Enter the 6-digit code exactly as received</li>
            </ul>
          </div>

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

          <form onSubmit={handleVerifyOTP}>
            <div className="auth-form-group">
              <label htmlFor="otp">Verification Code</label>
              <input
                type="text"
                className="auth-input"
                id="otp"
                name="otp"
                placeholder="Enter 6-digit code"
                value={otp}
                onChange={handleOTPChange}
                maxLength={6}
                required
                autoComplete="one-time-code"
                disabled={attempts >= maxAttempts}
                style={{ 
                  letterSpacing: '0.5em',
                  textAlign: 'center',
                  fontSize: '1.2em',
                  fontWeight: 'bold'
                }}
              />
              <small className="text-muted">
                Enter the 6-digit code sent to your email
              </small>
            </div>
            
            <button
              type="submit"
              className="auth-submit-btn"
              disabled={isLoading || otp.length !== 6 || attempts >= maxAttempts}
            >
              {isLoading && <span className="auth-loading"></span>}
              {isLoading ? 'Verifying...' : 'Verify Code'}
            </button>
          </form>

          <div className="text-center mt-3">
            <div className="mb-3">
              <p className="mb-2">
                Didn't receive the code? 
                {canResend ? (
                  <button
                    className="auth-toggle-btn"
                    onClick={handleResendOTP}
                    disabled={isLoading}
                  >
                    Resend Code
                  </button>
                ) : (
                  <span className="text-muted">
                    Resend in {formatTime(timeLeft)}
                  </span>
                )}
              </p>
              
              {attempts > 0 && (
                <small className="text-warning">
                  Attempts: {attempts}/{maxAttempts}
                </small>
              )}
            </div>
            
            <button
              className="auth-toggle-btn"
              onClick={handleBackToSignIn}
            >
              Back to {verificationType === 'signup' ? 'Sign Up' : 'Sign In'}
            </button>
          </div>

          <div className="mt-4 p-3 bg-light rounded">
            <small className="text-muted">
              <strong>Security Notice:</strong><br />
              • OTP expires in 10 minutes<br />
              • Maximum 3 attempts per OTP<br />
              • Rate limit: 1 OTP per minute<br />
              • Check spam folder if not received
            </small>
          </div>
        </div>
      </div>
    </div>
  );
};

export default OTPVerification;
