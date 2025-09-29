import { createClient } from '@supabase/supabase-js';

// IMPORTANT: Replace with your Supabase project's URL and anon key
const supabaseUrl = process.env.REACT_APP_SUPABASE_URL || 'YOUR_SUPABASE_URL';
const supabaseAnonKey = process.env.REACT_APP_SUPABASE_ANON_KEY || 'YOUR_SUPABASE_ANON_KEY';

// Check if we should use local authentication instead
const useLocalAuth = process.env.REACT_APP_USE_LOCAL_AUTH === 'true';

if ((supabaseUrl === 'YOUR_SUPABASE_URL' || supabaseAnonKey === 'YOUR_SUPABASE_ANON_KEY') && !useLocalAuth) {
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
        return {
          data: {
            user: {
              id: 'local-user-' + Date.now(),
              email: credentials.email,
              user_metadata: { full_name: credentials.options?.data?.full_name || credentials.email.split('@')[0] },
              email_confirmed_at: null,
              created_at: new Date().toISOString()
            }
          },
          error: null
        };
      },
      signInWithPassword: async (credentials) => {
        // Simulate successful signin
        return {
          data: {
            user: {
              id: 'local-user-' + Date.now(),
              email: credentials.email,
              user_metadata: { full_name: credentials.email.split('@')[0] }
            },
            session: {
              access_token: 'local-token-' + Date.now()
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
        return {
          data: {
            user: {
              id: 'local-user-' + Date.now(),
              email: credentials.email,
              user_metadata: { full_name: credentials.email.split('@')[0] }
            },
            session: {
              access_token: 'local-token-' + Date.now()
            }
          },
          error: null
        };
      },
      getUser: async () => {
        // Check localStorage for existing user session
        const token = localStorage.getItem('auth_token');
        const userData = localStorage.getItem('auth_user');
        
        if (token && userData) {
          try {
            const parsedUser = JSON.parse(userData);
            return { 
              data: { 
                user: {
                  id: parsedUser.id,
                  email: parsedUser.email,
                  user_metadata: { full_name: parsedUser.name }
                }
              }, 
              error: null 
            };
          } catch (error) {
            console.error('Error parsing stored user data:', error);
            return { data: { user: null }, error: null };
          }
        }
        
        return { data: { user: null }, error: null };
      },
      signOut: async () => {
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
