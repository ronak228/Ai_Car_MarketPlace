#!/usr/bin/env python3
"""
MongoDB Models for AI Car Marketplace
Defines data models for users and predictions
"""

from datetime import datetime
from bson import ObjectId
from bson.errors import InvalidId
import bcrypt
import hashlib
import secrets

class UserModel:
    """User model for MongoDB"""
    
    @staticmethod
    def hash_password(password):
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(password, hashed):
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    @staticmethod
    def create_user_document(email, password, full_name=None):
        """Create a new user document"""
        return {
            '_id': ObjectId(),
            'email': email.lower().strip(),
            'password_hash': UserModel.hash_password(password),
            'full_name': full_name or email.split('@')[0],
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'is_active': True,
            'email_verified': False,
            'last_login': None,
            'login_count': 0,
            'profile': {
                'preferences': {},
                'settings': {}
            }
        }
    
    @staticmethod
    def validate_user_data(data):
        """Validate user registration/login data"""
        errors = []
        
        if not data.get('email'):
            errors.append('Email is required')
        elif '@' not in data['email']:
            errors.append('Invalid email format')
        
        if not data.get('password'):
            errors.append('Password is required')
        elif len(data['password']) < 6:
            errors.append('Password must be at least 6 characters')
        
        return errors
    
    @staticmethod
    def sanitize_user_output(user_doc):
        """Remove sensitive data from user document"""
        if not user_doc:
            return None
        
        # Create a copy and remove sensitive fields
        sanitized = user_doc.copy()
        sanitized.pop('password_hash', None)
        sanitized.pop('_id', None)
        
        # Convert ObjectId to string
        sanitized['id'] = str(user_doc['_id'])
        
        return sanitized

class PredictionModel:
    """Prediction model for MongoDB"""
    
    @staticmethod
    def create_prediction_document(user_id, prediction_data, predicted_price):
        """Create a new prediction document"""
        return {
            '_id': ObjectId(),
            'user_id': ObjectId(user_id) if isinstance(user_id, str) else user_id,
            'prediction_data': prediction_data,
            'predicted_price': predicted_price,
            'created_at': datetime.utcnow(),
            'model_version': '1.0',
            'accuracy_score': None,
            'feedback': None
        }
    
    @staticmethod
    def validate_prediction_data(data):
        """Validate prediction input data"""
        errors = []
        
        required_fields = ['brand', 'model', 'year', 'fuel_type', 'transmission', 'owner_type', 'km_driven']
        
        for field in required_fields:
            if field not in data or data[field] is None:
                errors.append(f'{field} is required')
        
        # Validate year
        if 'year' in data:
            try:
                year = int(data['year'])
                if year < 1990 or year > 2024:
                    errors.append('Year must be between 1990 and 2024')
            except (ValueError, TypeError):
                errors.append('Year must be a valid number')
        
        # Validate km_driven
        if 'km_driven' in data:
            try:
                km = int(data['km_driven'])
                if km < 0:
                    errors.append('Kilometers driven cannot be negative')
            except (ValueError, TypeError):
                errors.append('Kilometers driven must be a valid number')
        
        return errors
    
    @staticmethod
    def sanitize_prediction_output(prediction_doc):
        """Format prediction document for output"""
        if not prediction_doc:
            return None
        
        # Create a copy
        sanitized = prediction_doc.copy()
        
        # Convert ObjectId to string
        sanitized['id'] = str(prediction_doc['_id'])
        sanitized['user_id'] = str(prediction_doc['user_id'])
        
        # Format datetime
        sanitized['created_at'] = prediction_doc['created_at'].isoformat()
        
        return sanitized

class OTPModel:
    """OTP model for MongoDB"""
    
    @staticmethod
    def generate_otp():
        """Generate a 6-digit OTP"""
        return str(secrets.randbelow(900000) + 100000)
    
    @staticmethod
    def create_otp_document(email, otp_code):
        """Create an OTP document"""
        return {
            '_id': ObjectId(),
            'email': email.lower().strip(),
            'otp_code': otp_code,
            'created_at': datetime.utcnow(),
            'expires_at': datetime.utcnow().replace(minute=datetime.utcnow().minute + 5),  # 5 minutes
            'is_used': False,
            'attempts': 0
        }
    
    @staticmethod
    def is_otp_valid(otp_doc):
        """Check if OTP is still valid"""
        if not otp_doc:
            return False
        
        now = datetime.utcnow()
        return (
            not otp_doc.get('is_used', False) and
            now < otp_doc.get('expires_at', now) and
            otp_doc.get('attempts', 0) < 3
        )

if __name__ == "__main__":
    print("MongoDB Models loaded successfully")
    
    # Test user creation
    test_user = UserModel.create_user_document("test@example.com", "password123", "Test User")
    print(f"Test user created: {test_user['email']}")
    
    # Test prediction creation
    test_prediction = PredictionModel.create_prediction_document(
        test_user['_id'],
        {'brand': 'Toyota', 'model': 'Camry', 'year': 2020},
        25000
    )
    print(f"Test prediction created: {test_prediction['predicted_price']}")
    
    # Test OTP generation
    test_otp = OTPModel.generate_otp()
    print(f"Test OTP generated: {test_otp}")