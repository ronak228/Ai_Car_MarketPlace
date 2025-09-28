import { createClient } from '@supabase/supabase-js';

// IMPORTANT: Replace with your Supabase project's URL and anon key
const supabaseUrl = process.env.REACT_APP_SUPABASE_URL || 'YOUR_SUPABASE_URL';
const supabaseAnonKey = process.env.REACT_APP_SUPABASE_ANON_KEY || 'YOUR_SUPABASE_ANON_KEY';

// Check if we should use local authentication instead
const useLocalAuth = process.env.REACT_APP_USE_LOCAL_AUTH === 'true' || 
                    supabaseUrl === 'YOUR_SUPABASE_URL' || 
                    supabaseAnonKey === 'YOUR_SUPABASE_ANON_KEY';

if (useLocalAuth) {
  console.warn(`
    ---------------------------------------------------
    !!! IMPORTANT: SUPABASE CREDENTIALS ARE MISSING !!!
    ---------------------------------------------------
    Please create a .env file in the 'client' directory 
    and add your Supabase URL and Anon Key:

    REACT_APP_SUPABASE_URL=your-supabase-url
    REACT_APP_SUPABASE_ANON_KEY=your-supabase-anon-key
    
    OR set REACT_APP_USE_LOCAL_AUTH=true to use local authentication
    
    You can find these in your Supabase project's 
    dashboard under Settings > API.
    ---------------------------------------------------
  `);
}

// Create Supabase client with fallback for local development
let supabase;
if (useLocalAuth || supabaseUrl === 'YOUR_SUPABASE_URL' || supabaseAnonKey === 'YOUR_SUPABASE_ANON_KEY') {
  // Create a mock Supabase client for local development
  supabase = {
    auth: {
      signUp: async (credentials) => {
        // Simulate successful signup
        const userId = 'local-user-' + Date.now();
        const token = 'local-token-' + Date.now();
        
        // Store user data in localStorage for persistence
        const userData = {
          id: userId,
          email: credentials.email,
          user_metadata: { full_name: credentials.options?.data?.full_name || credentials.email.split('@')[0] },
          email_confirmed_at: null,
          created_at: new Date().toISOString()
        };
        
        localStorage.setItem('mock_user', JSON.stringify(userData));
        localStorage.setItem('mock_token', token);
        
        return {
          data: {
            user: userData
          },
          error: null
        };
      },
      signInWithPassword: async (credentials) => {
        // Simulate successful signin
        const userId = 'local-user-' + Date.now();
        const token = 'local-token-' + Date.now();
        
        const userData = {
          id: userId,
          email: credentials.email,
          user_metadata: { full_name: credentials.email.split('@')[0] }
        };
        
        localStorage.setItem('mock_user', JSON.stringify(userData));
        localStorage.setItem('mock_token', token);
        
        return {
          data: {
            user: userData,
            session: {
              access_token: token,
              refresh_token: 'local-refresh-' + Date.now()
            }
          },
          error: null
        };
      },
      signInWithOtp: async (credentials) => {
        // Simulate successful OTP send
        return {
          data: {
            user: null,
            session: null
          },
          error: null
        };
      },
      verifyOtp: async (credentials) => {
        // Simulate successful OTP verification
        const userId = 'local-user-' + Date.now();
        const token = 'local-token-' + Date.now();
        
        const userData = {
          id: userId,
          email: credentials.email,
          user_metadata: { full_name: credentials.email.split('@')[0] }
        };
        
        localStorage.setItem('mock_user', JSON.stringify(userData));
        localStorage.setItem('mock_token', token);
        
        return {
          data: {
            user: userData,
            session: {
              access_token: token,
              refresh_token: 'local-refresh-' + Date.now()
            }
          },
          error: null
        };
      },
      getSession: async () => {
        // Check for stored session
        const storedUser = localStorage.getItem('mock_user');
        const storedToken = localStorage.getItem('mock_token');
        
        if (storedUser && storedToken) {
          try {
            const userData = JSON.parse(storedUser);
            return {
              data: {
                session: {
                  access_token: storedToken,
                  refresh_token: 'local-refresh-' + Date.now(),
                  user: userData
                }
              },
              error: null
            };
          } catch (error) {
            return { data: { session: null }, error: null };
          }
        }
        
        return { data: { session: null }, error: null };
      },
      onAuthStateChange: (callback) => {
        // Simulate auth state change listener
        const checkAuthState = () => {
          const storedUser = localStorage.getItem('mock_user');
          const storedToken = localStorage.getItem('mock_token');
          
          if (storedUser && storedToken) {
            try {
              const userData = JSON.parse(storedUser);
              callback('SIGNED_IN', {
                access_token: storedToken,
                refresh_token: 'local-refresh-' + Date.now(),
                user: userData
              });
            } catch (error) {
              callback('SIGNED_OUT', null);
            }
          } else {
            callback('SIGNED_OUT', null);
          }
        };
        
        // Check immediately
        checkAuthState();
        
        // Return unsubscribe function
        return {
          data: {
            subscription: {
              unsubscribe: () => {}
            }
          }
        };
      },
      signOut: async () => {
        // Clear stored data
        localStorage.removeItem('mock_user');
        localStorage.removeItem('mock_token');
        return { error: null };
      }
    }
  };
  console.log('🔧 Using local authentication (Supabase credentials not configured)');
} else {
  supabase = createClient(supabaseUrl, supabaseAnonKey);
  console.log('✅ Using Supabase authentication');
}

export { supabase };
