# Car Price Predictor

A comprehensive car rental and price prediction application with **Supabase authentication** and OTP verification.

## 🔐 Authentication System

This application uses **Supabase-only authentication** with the following features:

- ✅ **Email & Password Authentication**
- ✅ **OTP Verification** for new accounts
- ✅ **Password Reset** via email
- ✅ **Session Management** with JWT tokens
- ✅ **Database Storage** in Supabase PostgreSQL
- ✅ **Rate Limiting** and security protection

## 🚀 Quick Start

### Prerequisites:
- Node.js (v14 or higher)
- Supabase account

### Setup:

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd car_price_predictor-master
   ```

2. **Set up Supabase**
   - Create a project at [supabase.com](https://supabase.com)
   - Get your project URL and anon key
   - See `SUPABASE_SETUP.md` for detailed instructions

3. **Configure environment variables**
   ```bash
   cd client
   # Create .env file with your Supabase credentials
   echo "REACT_APP_SUPABASE_URL=your-project-url" > .env
   echo "REACT_APP_SUPABASE_ANON_KEY=your-anon-key" >> .env
   ```

4. **Install dependencies and start**
   ```bash
   npm install
   npm start
   ```

5. **Access the application**
   - Open `http://localhost:3000`
   - Sign up with your email
   - Verify your email with OTP
   - Start using the application

## 🌟 Features

### Authentication:
- **Secure Sign Up**: Email verification with OTP
- **Flexible Sign In**: Password or OTP authentication
- **Password Reset**: Email-based recovery
- **Session Persistence**: Automatic login state management

### Car Price Prediction:
- **ML Model**: Linear regression for price prediction
- **Input Validation**: Real-time form validation
- **Price Estimation**: Accurate car price predictions

### User Dashboard:
- **Personalized Experience**: User-specific dashboard
- **Car Management**: View and manage car data
- **Responsive Design**: Works on all devices

## 🔧 Configuration

### Supabase Setup:
See `SUPABASE_SETUP.md` for complete setup instructions.

### Environment Variables:
```bash
REACT_APP_SUPABASE_URL=your-supabase-project-url
REACT_APP_SUPABASE_ANON_KEY=your-supabase-anon-key
```

## 🧪 Testing

### Authentication Flow:
1. **Sign Up**: Create account → Receive OTP → Verify → Access
2. **Sign In**: Use credentials → Immediate access or OTP fallback
3. **Password Reset**: Request reset → Email link → New password

### Car Price Prediction:
1. Enter car details (year, mileage, etc.)
2. Get instant price prediction
3. View prediction accuracy and confidence

## 📁 Project Structure

```
car_price_predictor-master/
├── client/                 # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── supabaseClient.js # Supabase configuration
│   │   └── App.js         # Main application
│   └── package.json
├── SUPABASE_SETUP.md      # Supabase setup guide
└── README.md             # This file
```

## 🛡️ Security Features

- **Email Verification**: Required for all new accounts
- **OTP Authentication**: 6-digit verification codes
- **Password Security**: Secure password requirements
- **Session Management**: JWT token-based sessions
- **Rate Limiting**: Protection against abuse
- **Database Security**: Supabase's enterprise-grade security

## 🚀 Deployment

### Development:
```bash
cd client
npm start
```

### Production:
1. Build the application: `npm run build`
2. Deploy to your preferred hosting service
3. Update Supabase site URL for production
4. Configure environment variables

## 📞 Support

For authentication issues, see `SUPABASE_SETUP.md`.
For general issues, check the console logs and Supabase dashboard.

## 🎯 Current Status

- **Authentication**: ✅ Supabase-only with OTP
- **Database**: ✅ Supabase PostgreSQL
- **Security**: ✅ Production-ready
- **OTP**: ✅ Enabled and required
- **Demo Mode**: ❌ Removed (Supabase-only)

