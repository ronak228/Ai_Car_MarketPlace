#!/usr/bin/env python3
"""
Authentication Routes for AI Car Marketplace
Handles user registration, login, OTP verification, and JWT tokens
"""

from flask import Blueprint, request, jsonify
from functools import wraps
from datetime import datetime, timedelta
import jwt
import os
from mongodb_config import get_sync_collections
from models import UserModel, PredictionModel, OTPModel
from bson import ObjectId
from bson.errors import InvalidId

# Create blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# JWT Configuration
JWT_SECRET = os.getenv('JWT_SECRET', 'your-secret-key-change-in-production')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24

def generate_jwt_token(user_id, email):
    """Generate JWT token for user"""
    payload = {
        'user_id': str(user_id),
        'email': email,
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_jwt_token(token):
    """Verify JWT token and return user data"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def require_auth(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                token = auth_header.split(' ')[1]  # Bearer <token>
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        # Verify token
        payload = verify_jwt_token(token)
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Add user info to request context
        request.current_user = payload
        return f(*args, **kwargs)
    
    return decorated_function

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        # Validate input data
        errors = UserModel.validate_user_data(data)
        if errors:
            return jsonify({'error': 'Validation failed', 'details': errors}), 400
        
        collections = get_sync_collections()
        if not collections:
            return jsonify({'error': 'Database connection failed'}), 500
        
        email = data['email'].lower().strip()
        
        # Check if user already exists
        existing_user = collections['users'].find_one({'email': email})
        if existing_user:
            return jsonify({'error': 'User already exists'}), 409
        
        # Create new user
        user_doc = UserModel.create_user_document(
            email, 
            data['password'], 
            data.get('full_name')
        )
        
        # Insert user into database
        result = collections['users'].insert_one(user_doc)
        
        if result.inserted_id:
            # Generate JWT token
            token = generate_jwt_token(result.inserted_id, email)
            
            # Prepare response
            user_data = UserModel.sanitize_user_output(user_doc)
            user_data['token'] = token
            
            return jsonify({
                'message': 'User registered successfully',
                'user': user_data
            }), 201
        else:
            return jsonify({'error': 'Failed to create user'}), 500
            
    except Exception as e:
        print(f"[ERROR] Registration error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        
        # Validate input data
        errors = UserModel.validate_user_data(data)
        if errors:
            return jsonify({'error': 'Validation failed', 'details': errors}), 400
        
        collections = get_sync_collections()
        if not collections:
            return jsonify({'error': 'Database connection failed'}), 500
        
        email = data['email'].lower().strip()
        
        # Find user
        user = collections['users'].find_one({'email': email})
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Verify password
        if not UserModel.verify_password(data['password'], user['password_hash']):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Check if user is active
        if not user.get('is_active', True):
            return jsonify({'error': 'Account is deactivated'}), 401
        
        # Update last login
        collections['users'].update_one(
            {'_id': user['_id']},
            {
                '$set': {'last_login': datetime.utcnow()},
                '$inc': {'login_count': 1}
            }
        )
        
        # Generate JWT token
        token = generate_jwt_token(user['_id'], email)
        
        # Prepare response
        user_data = UserModel.sanitize_user_output(user)
        user_data['token'] = token
        
        return jsonify({
            'message': 'Login successful',
            'user': user_data
        }), 200
        
    except Exception as e:
        print(f"[ERROR] Login error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/profile', methods=['GET'])
@require_auth
def get_profile():
    """Get user profile"""
    try:
        collections = get_sync_collections()
        if not collections:
            return jsonify({'error': 'Database connection failed'}), 500
        
        user_id = request.current_user['user_id']
        
        # Find user
        user = collections['users'].find_one({'_id': ObjectId(user_id)})
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Prepare response
        user_data = UserModel.sanitize_user_output(user)
        
        return jsonify({'user': user_data}), 200
        
    except Exception as e:
        print(f"[ERROR] Profile error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/change-password', methods=['POST'])
@require_auth
def change_password():
    """Change user password"""
    try:
        data = request.get_json()
        
        if not data.get('current_password') or not data.get('new_password'):
            return jsonify({'error': 'Current password and new password are required'}), 400
        
        if len(data['new_password']) < 6:
            return jsonify({'error': 'New password must be at least 6 characters'}), 400
        
        collections = get_sync_collections()
        if not collections:
            return jsonify({'error': 'Database connection failed'}), 500
        
        user_id = request.current_user['user_id']
        
        # Find user
        user = collections['users'].find_one({'_id': ObjectId(user_id)})
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Verify current password
        if not UserModel.verify_password(data['current_password'], user['password_hash']):
            return jsonify({'error': 'Current password is incorrect'}), 401
        
        # Update password
        new_password_hash = UserModel.hash_password(data['new_password'])
        collections['users'].update_one(
            {'_id': user['_id']},
            {
                '$set': {
                    'password_hash': new_password_hash,
                    'updated_at': datetime.utcnow()
                }
            }
        )
        
        return jsonify({'message': 'Password changed successfully'}), 200
        
    except Exception as e:
        print(f"[ERROR] Change password error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/logout', methods=['POST'])
@require_auth
def logout():
    """Logout user (client-side token removal)"""
    return jsonify({'message': 'Logout successful'}), 200

@auth_bp.route('/predictions', methods=['GET'])
@require_auth
def get_user_predictions():
    """Get user's prediction history"""
    try:
        collections = get_sync_collections()
        if not collections:
            return jsonify({'error': 'Database connection failed'}), 500
        
        user_id = request.current_user['user_id']
        
        # Get predictions for user
        predictions = list(collections['predictions'].find(
            {'user_id': ObjectId(user_id)}
        ).sort('created_at', -1).limit(50))
        
        # Sanitize predictions
        sanitized_predictions = [
            PredictionModel.sanitize_prediction_output(pred) 
            for pred in predictions
        ]
        
        return jsonify({
            'predictions': sanitized_predictions,
            'count': len(sanitized_predictions)
        }), 200
        
    except Exception as e:
        print(f"[ERROR] Get predictions error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/verify-token', methods=['POST'])
def verify_token():
    """Verify JWT token"""
    try:
        data = request.get_json()
        token = data.get('token')
        
        if not token:
            return jsonify({'error': 'Token is required'}), 400
        
        payload = verify_jwt_token(token)
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        return jsonify({
            'valid': True,
            'user_id': payload['user_id'],
            'email': payload['email']
        }), 200
        
    except Exception as e:
        print(f"[ERROR] Token verification error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# OTP routes removed - using simple authentication without email verification

if __name__ == "__main__":
    print("Authentication routes loaded successfully")