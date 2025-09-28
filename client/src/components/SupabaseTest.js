import React, { useState } from 'react';
import { supabase } from '../supabaseClient';

const SupabaseTest = () => {
  const [email, setEmail] = useState('');
  const [status, setStatus] = useState('');
  const [loading, setLoading] = useState(false);

  const testSupabaseConnection = async () => {
    setLoading(true);
    setStatus('Testing Supabase connection...');

    try {
      // Test basic connection by checking auth status instead of querying a dummy table
      const { data: { user }, error } = await supabase.auth.getUser();
      
      if (error) {
        setStatus(`❌ Connection error: ${error.message}`);
      } else {
        setStatus('✅ Supabase connection successful! (Auth service working)');
      }
    } catch (err) {
      setStatus(`❌ Connection failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const testOTP = async () => {
    if (!email) {
      setStatus('❌ Please enter an email address');
      return;
    }

    setLoading(true);
    setStatus('Sending OTP...');

    try {
      // Wait a bit to avoid rate limiting
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      const { data, error } = await supabase.auth.signInWithOtp({
        email: email,
        options: {
          shouldCreateUser: false
        }
      });

      if (error) {
        if (error.message.includes('429') || error.message.includes('rate limit')) {
          setStatus('❌ Rate limit reached. Please wait 1 minute before trying again.');
        } else {
          setStatus(`❌ OTP Error: ${error.message}`);
        }
      } else {
        setStatus('✅ OTP sent successfully! Check your email.');
        console.log('=== OTP RESPONSE ===');
        console.log('Full response:', data);
        console.log('User:', data.user);
        console.log('Session:', data.session);
        console.log('Check your email for the verification code.');
        console.log('===================');
      }
    } catch (err) {
      setStatus(`❌ OTP failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '600px', margin: '0 auto' }}>
      <h2>🔧 Supabase Connection Test</h2>
      
      <div style={{ marginBottom: '20px' }}>
        <button 
          onClick={testSupabaseConnection}
          disabled={loading}
          style={{ 
            padding: '10px 20px', 
            backgroundColor: '#007bff', 
            color: 'white', 
            border: 'none', 
            borderRadius: '5px',
            cursor: loading ? 'not-allowed' : 'pointer'
          }}
        >
          {loading ? 'Testing...' : 'Test Connection'}
        </button>
      </div>

      <div style={{ marginBottom: '20px' }}>
        <input
          type="email"
          placeholder="Enter email to test OTP"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          style={{ 
            padding: '10px', 
            width: '300px', 
            marginRight: '10px',
            borderRadius: '5px',
            border: '1px solid #ccc'
          }}
        />
        <button 
          onClick={testOTP}
          disabled={loading || !email}
          style={{ 
            padding: '10px 20px', 
            backgroundColor: '#28a745', 
            color: 'white', 
            border: 'none', 
            borderRadius: '5px',
            cursor: (loading || !email) ? 'not-allowed' : 'pointer'
          }}
        >
          {loading ? 'Sending...' : 'Send OTP'}
        </button>
      </div>

      <div style={{ 
        padding: '15px', 
        backgroundColor: '#f8f9fa', 
        borderRadius: '5px',
        border: '1px solid #dee2e6'
      }}>
        <strong>Status:</strong> {status}
      </div>

      <div style={{ marginTop: '20px', fontSize: '14px', color: '#666' }}>
        <h3>🔍 Troubleshooting Tips:</h3>
        <ul>
          <li>Make sure your <code>.env</code> file has the correct Supabase URL and anon key</li>
          <li>Check that email confirmations are enabled in Supabase dashboard</li>
          <li>Verify the Magic Link email template is configured</li>
          <li>Check your spam folder for OTP emails</li>
          <li>Ensure your Supabase project is fully initialized</li>
        </ul>
      </div>
    </div>
  );
};

export default SupabaseTest;
