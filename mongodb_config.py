#!/usr/bin/env python3
"""
MongoDB Configuration for AI Car Marketplace
Handles MongoDB Atlas connection and collection management
"""

import os
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
import logging

# MongoDB Configuration
MONGODB_URL = "mongodb+srv://harshdua26:harshu261@cluster0.oosmzck.mongodb.net/car_marketplace?retryWrites=true&w=majority"
MONGODB_DATABASE = "car_marketplace"

# Collection names
COLLECTIONS = {
    'users': 'users',
    'predictions': 'predictions',
    'market_trends': 'market_trends',
    'car_dataset': 'car_dataset',
    'user_car_data': 'user_car_data'  # New collection for user-specific car data
}

# Global client variables
sync_client = None
async_client = None

def get_sync_client():
    """Get synchronous MongoDB client"""
    global sync_client
    if sync_client is None:
        try:
            sync_client = MongoClient(MONGODB_URL)
            # Test connection
            sync_client.admin.command('ping')
            print("[OK] MongoDB Atlas: Connected successfully")
        except Exception as e:
            print(f"[ERROR] MongoDB connection failed: {str(e)}")
            sync_client = None
    return sync_client

def get_async_client():
    """Get asynchronous MongoDB client"""
    global async_client
    if async_client is None:
        try:
            async_client = AsyncIOMotorClient(MONGODB_URL)
            print("[OK] MongoDB Atlas: Async client created")
        except Exception as e:
            print(f"[ERROR] MongoDB async connection failed: {str(e)}")
            async_client = None
    return async_client

def get_sync_collections():
    """Get synchronous database collections"""
    client = get_sync_client()
    if client is None:
        return None
    
    db = client[MONGODB_DATABASE]
    return {
        'users': db[COLLECTIONS['users']],
        'predictions': db[COLLECTIONS['predictions']],
        'market_trends': db[COLLECTIONS['market_trends']]
    }

def get_async_collections():
    """Get asynchronous database collections"""
    client = get_async_client()
    if client is None:
        return None
    
    db = client[MONGODB_DATABASE]
    return {
        'users': db[COLLECTIONS['users']],
        'predictions': db[COLLECTIONS['predictions']],
        'market_trends': db[COLLECTIONS['market_trends']]
    }

def test_connection():
    """Test MongoDB connection"""
    try:
        client = get_sync_client()
        if client:
            # Test database access
            db = client[MONGODB_DATABASE]
            collections = get_sync_collections()
            
            # Test each collection
            for name, collection in collections.items():
                count = collection.count_documents({})
                print(f"[OK] Collection '{name}': {count} documents")
            
            return True
        return False
    except Exception as e:
        print(f"[ERROR] MongoDB test failed: {str(e)}")
        return False

def close_connections():
    """Close all MongoDB connections"""
    global sync_client, async_client
    
    if sync_client:
        sync_client.close()
        sync_client = None
        print("[OK] MongoDB sync client closed")
    
    if async_client:
        async_client.close()
        async_client = None
        print("[OK] MongoDB async client closed")

if __name__ == "__main__":
    print("Testing MongoDB Configuration...")
    test_connection()