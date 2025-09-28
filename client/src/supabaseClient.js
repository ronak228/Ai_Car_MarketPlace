import { createClient } from '@supabase/supabase-js';

// IMPORTANT: Replace with your Supabase project's URL and anon key
const supabaseUrl = process.env.REACT_APP_SUPABASE_URL || 'YOUR_SUPABASE_URL';
const supabaseAnonKey = process.env.REACT_APP_SUPABASE_ANON_KEY || 'YOUR_SUPABASE_ANON_KEY';

if (supabaseUrl === 'YOUR_SUPABASE_URL' || supabaseAnonKey === 'YOUR_SUPABASE_ANON_KEY') {
  console.warn(`
    ---------------------------------------------------
    !!! IMPORTANT: SUPABASE CREDENTIALS ARE MISSING !!!
    ---------------------------------------------------
    Please create a .env file in the 'client' directory 
    and add your Supabase URL and Anon Key:

    REACT_APP_SUPABASE_URL=your-supabase-url
    REACT_APP_SUPABASE_ANON_KEY=your-supabase-anon-key
    
    You can find these in your Supabase project's 
    dashboard under Settings > API.
    ---------------------------------------------------
  `);
}

export const supabase = createClient(supabaseUrl, supabaseAnonKey);
