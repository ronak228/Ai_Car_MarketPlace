# Supabase Setup Guide for Car Price Predictor

## Quick Setup to Fix OTP Issues

### 1. Create Supabase Project
1. Go to [supabase.com](https://supabase.com)
2. Create a new project
3. Wait for the project to be ready

### 2. Get Your Credentials
1. Go to **Settings > API** in your Supabase dashboard
2. Copy the **Project URL** and **anon public key**

### 3. Configure Environment Variables
1. Create a `.env` file in the `client` directory
2. Add your credentials:

```env
REACT_APP_SUPABASE_URL=https://your-project-id.supabase.co
REACT_APP_SUPABASE_ANON_KEY=your-anon-key-here
```

### 4. Enable Email Authentication
1. Go to **Authentication > Settings** in Supabase dashboard
2. Enable **Email Auth**
3. Configure **Email Templates** if needed

### 5. Test OTP Functionality
1. Restart your development server
2. Try signing up with a real email address
3. Check your email for OTP (also check spam folder)

## Common OTP Issues & Solutions

### Issue: OTP Not Arriving
**Solutions:**
- Check spam/junk folder
- Verify email address is correct
- Wait 1-2 minutes before requesting new OTP
- Ensure Supabase project is active

### Issue: OTP Validation Failing
**Solutions:**
- Enter exactly 6 digits
- Don't include spaces or special characters
- Try requesting a new OTP if current one expires
- Check browser console for error messages

### Issue: Rate Limiting
**Solutions:**
- Wait 1 minute between OTP requests
- Don't spam the resend button
- Check Supabase dashboard for rate limits

## Advanced Configuration

### Email Templates
1. Go to **Authentication > Email Templates**
2. Customize the **Magic Link** template
3. Test email delivery

### Security Settings
1. Go to **Authentication > Settings**
2. Configure **Site URL** to match your app
3. Set appropriate **Redirect URLs**

## Troubleshooting

### Check Console Logs
Open browser console (F12) to see detailed error messages:
- OTP sending status
- Verification attempts
- Error details

### Verify Supabase Connection
Check if your credentials are working:
1. Open browser console
2. Look for Supabase connection messages
3. Ensure no "credentials missing" warnings

### Test with Different Email
Try using a different email address to rule out email provider issues.

## Support

If you continue having OTP issues:
1. Check Supabase project status
2. Verify email authentication is enabled
3. Test with a different email provider
4. Check browser console for specific errors
