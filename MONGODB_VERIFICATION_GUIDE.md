# MongoDB Atlas Verification Guide

## Step 1: Check MongoDB Atlas Dashboard

1. **Login to MongoDB Atlas**
   - Go to https://cloud.mongodb.com/
   - Login with your MongoDB account

2. **Verify Cluster Status**
   - Check if your cluster `cluster0` is running
   - Status should show "Running" (green)

3. **Check Database Access**
   - Go to "Database Access" in the left sidebar
   - Verify user `harshdua26` exists
   - Check if password is `harshu@261`
   - Ensure user has "Read and write to any database" permissions

4. **Verify Network Access**
   - Go to "Network Access" in the left sidebar
   - Check if your current IP address is whitelisted
   - If not, click "Add IP Address" and add your current IP
   - OR add `0.0.0.0/0` to allow access from anywhere (for testing)

## Step 2: Test Connection from Atlas Dashboard

1. **Use MongoDB Compass or Atlas Data Explorer**
   - Click "Connect" on your cluster
   - Choose "Connect with MongoDB Compass"
   - Copy the connection string
   - Test the connection

## Step 3: Verify Database and Collections

1. **Check if database exists**
   - In Atlas Data Explorer, look for `car_marketplace` database
   - If it doesn't exist, it will be created automatically

2. **Verify Collections**
   - The following collections will be created automatically:
     - `users` - for user accounts
     - `predictions` - for user predictions
     - `cars` - for car data

## Step 4: Test Connection Programmatically

Run the diagnostic test to check connection:

```bash
python test_atlas_diagnostic.py
```

## Step 5: Common Issues and Solutions

### Issue 1: Authentication Failed
**Solution:**
- Double-check username and password
- Ensure user has proper permissions
- Try resetting the password in Atlas

### Issue 2: IP Not Whitelisted
**Solution:**
- Add your current IP address to Network Access
- Or temporarily add `0.0.0.0/0` for testing

### Issue 3: Database Doesn't Exist
**Solution:**
- Database will be created automatically on first connection
- No manual creation needed

### Issue 4: Connection Timeout
**Solution:**
- Check if cluster is running
- Verify network connectivity
- Try different connection string format

## Step 6: Test with Different Connection Strings

Try these connection string variations:

1. **With database specified:**
   ```
   mongodb+srv://harshdua26:harshu%40261@cluster0.oosmzck.mongodb.net/car_marketplace?retryWrites=true&w=majority
   ```

2. **Without database specified:**
   ```
   mongodb+srv://harshdua26:harshu%40261@cluster0.oosmzck.mongodb.net/?retryWrites=true&w=majority
   ```

3. **With different options:**
   ```
   mongodb+srv://harshdua26:harshu%40261@cluster0.oosmzck.mongodb.net/car_marketplace
   ```

## Step 7: Manual Verification Commands

You can also test manually using MongoDB shell:

```bash
# Install MongoDB shell if not installed
# Then connect:
mongosh "mongodb+srv://harshdua26:harshu%40261@cluster0.oosmzck.mongodb.net/car_marketplace"
```

## Step 8: Check Application Logs

When you run the application, check the console output for:
- `[OK] MongoDB authentication imported successfully`
- `[OK] Authentication routes registered`
- `[OK] Connected to MongoDB Atlas: car_marketplace`

If you see errors, they will help identify the specific issue.
