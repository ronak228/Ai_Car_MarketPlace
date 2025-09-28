# 🔐 Supabase Dual Authentication Setup

This application uses **dual authentication** with Supabase - users can choose between **Password** or **OTP** authentication for maximum flexibility and security.

## 🚀 Quick Setup

### 1. Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Sign up/Login and create a new project
3. Wait for the project to be ready (usually 1-2 minutes)

### 2. Get Your Credentials

1. Go to **Settings > API** in your Supabase dashboard
2. Copy your **Project URL** and **anon public key**

### 3. Configure Environment Variables

Create a `.env` file in the `client` directory:

```bash
REACT_APP_SUPABASE_URL=your-project-url-here
REACT_APP_SUPABASE_ANON_KEY=your-anon-key-here
```

### 4. Configure Authentication Settings

In your Supabase dashboard:

1. Go to **Authentication > Settings**
2. Enable **Email Auth**
3. Configure **Email Templates** (optional)
4. Set **Site URL** to `http://localhost:3000` for development

### 5. Start the Application

```bash
cd client
npm start
```

## 🔐 Authentication Features

### Sign Up Process:
1. User enters email, name, and password
2. Account is created in Supabase
3. OTP is sent to user's email
4. User enters OTP code
5. Account is verified and user is logged in

### Sign In Process - Two Options:

#### Option 1: Password Authentication
1. User selects "Password" method
2. User enters email and password
3. Direct authentication - logged in immediately

#### Option 2: OTP Authentication
1. User selects "OTP" method
2. User enters email only
3. OTP is sent to user's email
4. User enters OTP code
5. User is authenticated and logged in

### Password Reset:
1. User clicks "Forgot Password?"
2. Enters email address
3. Reset link is sent via email
4. User sets new password

## 🛡️ Security Features

- ✅ **Dual Authentication**: Choose Password or OTP
- ✅ **Email Verification**: Required for new accounts
- ✅ **OTP Time Management**: 60-second resend cooldown
- ✅ **Attempt Limiting**: Maximum 3 attempts per OTP
- ✅ **Rate Limiting**: 1 OTP per minute protection
- ✅ **Session Management**: JWT tokens with automatic refresh
- ✅ **Database Storage**: All user data stored securely in Supabase

## ⏰ Time Management

### OTP Expiration:
- **OTP Validity**: 10 minutes
- **Resend Cooldown**: 60 seconds
- **Rate Limit**: 1 OTP per minute per email

### Attempt Management:
- **Maximum Attempts**: 3 per OTP
- **Lockout**: After 3 failed attempts, new OTP required
- **Reset**: Attempts reset when new OTP is requested

## 📧 Email Templates (Optional)

Customize your email templates in **Authentication > Email Templates**:

### OTP Email:
```
Subject: Your verification code
Body: Your verification code is: {{ .Token }}
```

### Password Reset Email:
```
Subject: Reset your password
Body: Click the link to reset your password: {{ .ConfirmationURL }}
```

## 🧪 Testing

### Test Sign Up:
1. Go to sign up page
2. Enter email, name, and password
3. Check your email for OTP
4. Enter OTP code
5. Should be logged in and redirected to dashboard

### Test Sign In - Password Method:
1. Go to sign in page
2. Select "Password" authentication
3. Enter email and password
4. Should log in immediately

### Test Sign In - OTP Method:
1. Go to sign in page
2. Select "OTP" authentication
3. Enter email only
4. Check email for OTP
5. Enter OTP code
6. Should be logged in and redirected to dashboard

### Test Password Reset:
1. Click "Forgot Password?"
2. Enter your email
3. Check email for reset link
4. Set new password

## 🔧 Troubleshooting

### Common Issues:

**"OTP not received"**
- Check spam folder
- Verify email address is correct
- Check Supabase email settings
- Wait 60 seconds before requesting new OTP

**"Rate limit reached"**
- Wait 1 minute before trying again
- Check Supabase rate limiting settings

**"Maximum attempts reached"**
- Request a new OTP
- Wait for the 60-second cooldown

**"Invalid OTP"**
- Make sure you're using the latest OTP
- OTP expires after 10 minutes
- Request a new OTP if needed

**"Invalid password"**
- Check your password is correct
- Use "Forgot Password?" to reset if needed
- Try OTP authentication as alternative

## 📱 Production Deployment

For production:

1. Update **Site URL** in Supabase settings
2. Configure **Redirect URLs**
3. Set up **Custom Domain** (optional)
4. Configure **Email Provider** (optional)

## 🎯 Current Status

- **Authentication**: Dual (Password + OTP)
- **Sign Up**: OTP verification required
- **Sign In**: User choice (Password or OTP)
- **Time Management**: 60s cooldown, 10min expiration
- **Attempt Limiting**: 3 attempts per OTP
- **Database**: Supabase PostgreSQL
- **Security**: Production-ready with enterprise features
