# Car Price Predictor - Quick Setup Guide

## 🚀 Quick Fix for "Failed to Fetch" Error

The "failed to fetch" error occurs because Supabase credentials are not configured. Here are two solutions:

### Solution 1: Use Local Authentication (Quick Fix)

1. Create a `.env` file in the `client` directory:
```bash
cd client
echo "REACT_APP_USE_LOCAL_AUTH=true" > .env
```

2. Restart your development server:
```bash
npm start
```

3. Now you can sign up/sign in with any email and any 6-digit OTP code!

### Solution 2: Configure Supabase (Recommended for Production)

1. Go to [supabase.com](https://supabase.com) and create a new project
2. Get your credentials from Settings > API
3. Create a `.env` file in the `client` directory:
```bash
cd client
echo "REACT_APP_SUPABASE_URL=https://your-project-id.supabase.co" > .env
echo "REACT_APP_SUPABASE_ANON_KEY=your-anon-key-here" >> .env
```

4. Restart your development server

## 🔧 How to Run the Application

### Option 1: Run Everything Together
```bash
# Install dependencies
npm install
cd client && npm install && cd ..

# Start both backend and frontend
npm run run-all
```

### Option 2: Run Separately
```bash
# Terminal 1 - Backend (Flask)
python application.py

# Terminal 2 - Frontend (React)
cd client && npm start
```

## 📱 Testing Authentication

1. Go to `http://localhost:3000/signup`
2. Enter any email and password
3. For OTP verification, enter any 6-digit number (like 123456)
4. You should be logged in successfully!

## 🐛 Troubleshooting

- **"Failed to fetch"**: Use Solution 1 above
- **Port conflicts**: Make sure ports 3000 and 5000 are available
- **Dependencies**: Run `npm install` in both root and client directories

## 📞 Support

If you still have issues:
1. Check browser console for error messages
2. Ensure all dependencies are installed
3. Try the local authentication solution first
