# MongoDB Integration for AI Car Marketplace

This project now includes MongoDB integration for user authentication and data storage. Users can register, login, and have their prediction history stored in MongoDB.

## Features Added

### Backend (Flask)
- **MongoDB Authentication**: Complete user authentication system with MongoDB
- **User Management**: Registration, login, profile management, password changes
- **Prediction Storage**: User predictions are stored in MongoDB
- **JWT Tokens**: Secure authentication using JSON Web Tokens
- **Password Security**: Bcrypt password hashing with configurable rounds

### Frontend (React)
- **MongoDB Auth Client**: New authentication client for MongoDB
- **MongoDB Sign In/Up**: New authentication components
- **User Profile Management**: Update profile and change password
- **Prediction History**: View user's prediction history

## Setup Instructions

### 1. Install MongoDB

#### Windows
1. Download MongoDB Community Server from [mongodb.com](https://www.mongodb.com/try/download/community)
2. Install MongoDB with default settings
3. Start MongoDB service:
   ```cmd
   net start MongoDB
   ```

#### macOS
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb/brew/mongodb-community
```

#### Linux (Ubuntu/Debian)
```bash
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo systemctl start mongod
sudo systemctl enable mongod
```

### 2. Environment Variables

Create a `.env` file in the project root:

```env
# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017
MONGODB_DATABASE=car_marketplace
MONGODB_COLLECTION_USERS=users
MONGODB_COLLECTION_PREDICTIONS=predictions
MONGODB_COLLECTION_CARS=cars

# JWT Configuration
JWT_SECRET_KEY=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# Password Hashing
BCRYPT_ROUNDS=12
```

### 3. Install Dependencies

The MongoDB dependencies are already installed:
- `pymongo` - MongoDB driver for Python
- `motor` - Async MongoDB driver
- `bcrypt` - Password hashing
- `python-jose[cryptography]` - JWT token handling

### 4. Test MongoDB Integration

Run the test script to verify everything is working:

```bash
python test_mongodb.py
```

Expected output:
```
============================================================
MongoDB Integration Test Suite
============================================================
Testing MongoDB Connection...
[OK] MongoDB config imported successfully
[OK] Sync collections created: ['users', 'predictions', 'cars']
[OK] MongoDB ping successful: {'ok': 1.0}
...
[SUCCESS] All tests passed! MongoDB integration is working correctly.
```

## API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login user |
| GET | `/api/auth/profile` | Get user profile |
| PUT | `/api/auth/profile` | Update user profile |
| POST | `/api/auth/change-password` | Change password |
| POST | `/api/auth/logout` | Logout user |
| GET | `/api/auth/predictions` | Get user predictions |
| POST | `/api/auth/verify-token` | Verify JWT token |

### Example API Usage

#### Register User
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!",
    "name": "John Doe",
    "username": "johndoe"
  }'
```

#### Login User
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!"
  }'
```

#### Make Prediction (with authentication)
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "company": "Maruti Suzuki",
    "model": "Alto",
    "year": 2020,
    "kms_driven": 50000,
    "fuel_type": "Petrol",
    "user_id": "USER_ID"
  }'
```

## Frontend Usage

### MongoDB Authentication Routes

- `/mongo-signin` - MongoDB-based sign in
- `/mongo-signup` - MongoDB-based sign up

### Using MongoDB Auth Client

```javascript
import mongoAuthClient from './mongoAuthClient';

// Register user
const response = await mongoAuthClient.register({
  email: 'user@example.com',
  password: 'SecurePass123!',
  name: 'John Doe'
});

// Login user
const response = await mongoAuthClient.login('user@example.com', 'SecurePass123!');

// Make prediction
const prediction = await mongoAuthClient.makePrediction({
  company: 'Maruti Suzuki',
  model: 'Alto',
  year: 2020,
  kms_driven: 50000,
  fuel_type: 'Petrol'
});

// Get user predictions
const predictions = await mongoAuthClient.getUserPredictions();
```

## Database Schema

### Users Collection
```javascript
{
  "_id": ObjectId,
  "email": String (unique),
  "username": String (unique, optional),
  "name": String,
  "password_hash": String,
  "is_active": Boolean,
  "is_verified": Boolean,
  "profile": {
    "avatar": String,
    "phone": String,
    "address": String,
    "preferences": {
      "notifications": Boolean,
      "theme": String,
      "language": String
    }
  },
  "created_at": Date,
  "updated_at": Date,
  "last_login": Date
}
```

### Predictions Collection
```javascript
{
  "_id": ObjectId,
  "user_id": ObjectId,
  "prediction_data": Object,
  "predicted_price": Number,
  "model_used": String,
  "confidence_score": Number,
  "created_at": Date,
  "updated_at": Date
}
```

## Security Features

- **Password Hashing**: Bcrypt with configurable rounds
- **JWT Tokens**: Secure token-based authentication
- **Account Locking**: Temporary lockout after failed login attempts
- **Input Validation**: Email format and password strength validation
- **Token Expiration**: Configurable token expiration time

## Troubleshooting

### MongoDB Connection Issues
1. Ensure MongoDB is running: `mongosh` or `mongo`
2. Check MongoDB URL in environment variables
3. Verify MongoDB service is started

### Authentication Issues
1. Check JWT secret key is set
2. Verify token expiration settings
3. Check user account status (active/verified)

### Frontend Issues
1. Ensure API base URL is correct
2. Check CORS settings in Flask app
3. Verify token storage in localStorage

## Production Considerations

1. **Change JWT Secret**: Use a strong, random secret key
2. **MongoDB Security**: Enable authentication and use SSL
3. **Environment Variables**: Use proper environment variable management
4. **Rate Limiting**: Implement rate limiting for auth endpoints
5. **Logging**: Add comprehensive logging for security events
6. **Backup**: Set up MongoDB backup strategy

## Migration from Supabase

The project maintains backward compatibility with Supabase authentication. Users can choose between:
- Supabase authentication (existing routes: `/signin`, `/signup`)
- MongoDB authentication (new routes: `/mongo-signin`, `/mongo-signup`)

Both systems can coexist, allowing for gradual migration.
