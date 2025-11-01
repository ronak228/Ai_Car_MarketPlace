#!/usr/bin/env python3
"""
User-Specific Car Data Management Script
Allows adding, updating, and managing car data specific to individual users
"""

import pandas as pd
import os
import sys
from bson import ObjectId
from mongodb_config import get_sync_client, MONGODB_DATABASE, COLLECTIONS

def get_user_by_email(email):
    """Get user by email"""
    client = get_sync_client()
    if not client:
        print("Failed to connect to MongoDB")
        return None
    
    db = client[MONGODB_DATABASE]
    users_collection = db[COLLECTIONS['users']]
    
    user = users_collection.find_one({"email": email})
    return user

def add_car_to_user(user_id, car_data):
    """Add a car to user's specific dataset"""
    client = get_sync_client()
    if not client:
        print("Failed to connect to MongoDB")
        return False
    
    db = client[MONGODB_DATABASE]
    user_car_collection = db[COLLECTIONS['user_car_data']]
    
    # Add user_id to car data
    car_data['user_id'] = user_id
    
    # Insert car data
    result = user_car_collection.insert_one(car_data)
    return result.inserted_id is not None

def import_cars_for_user(user_id, csv_file):
    """Import cars from CSV file for a specific user"""
    if not os.path.exists(csv_file):
        print(f"File not found: {csv_file}")
        return False
    
    try:
        # Load CSV file
        df = pd.read_csv(csv_file)
        print(f"Loaded {len(df)} cars from {csv_file}")
        
        # Convert DataFrame to list of dictionaries
        cars = df.to_dict('records')
        
        # Add user_id to each car
        for car in cars:
            car['user_id'] = user_id
        
        # Insert into MongoDB
        client = get_sync_client()
        if not client:
            print("Failed to connect to MongoDB")
            return False
        
        db = client[MONGODB_DATABASE]
        user_car_collection = db[COLLECTIONS['user_car_data']]
        
        # Insert cars in batches
        batch_size = 100
        for i in range(0, len(cars), batch_size):
            batch = cars[i:i+batch_size]
            result = user_car_collection.insert_many(batch)
            print(f"Inserted batch {i//batch_size + 1}/{(len(cars)-1)//batch_size + 1}")
        
        print(f"Successfully imported {len(cars)} cars for user {user_id}")
        return True
    
    except Exception as e:
        print(f"Error importing cars: {str(e)}")
        return False

def get_user_cars(user_id):
    """Get all cars for a specific user"""
    client = get_sync_client()
    if not client:
        print("Failed to connect to MongoDB")
        return None
    
    db = client[MONGODB_DATABASE]
    user_car_collection = db[COLLECTIONS['user_car_data']]
    
    # Find all cars for user
    cars = list(user_car_collection.find({"user_id": user_id}))
    return cars

def delete_user_cars(user_id):
    """Delete all cars for a specific user"""
    client = get_sync_client()
    if not client:
        print("Failed to connect to MongoDB")
        return False
    
    db = client[MONGODB_DATABASE]
    user_car_collection = db[COLLECTIONS['user_car_data']]
    
    # Delete all cars for user
    result = user_car_collection.delete_many({"user_id": user_id})
    print(f"Deleted {result.deleted_count} cars for user {user_id}")
    return result.deleted_count > 0

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python manage_user_car_data.py import <user_email> <csv_file>")
        print("  python manage_user_car_data.py list <user_email>")
        print("  python manage_user_car_data.py delete <user_email>")
        return
    
    command = sys.argv[1]
    
    if command == "import" and len(sys.argv) == 4:
        user_email = sys.argv[2]
        csv_file = sys.argv[3]
        
        user = get_user_by_email(user_email)
        if not user:
            print(f"User not found: {user_email}")
            return
        
        user_id = str(user['_id'])
        import_cars_for_user(user_id, csv_file)
    
    elif command == "list" and len(sys.argv) == 3:
        user_email = sys.argv[2]
        
        user = get_user_by_email(user_email)
        if not user:
            print(f"User not found: {user_email}")
            return
        
        user_id = str(user['_id'])
        cars = get_user_cars(user_id)
        
        if not cars:
            print(f"No cars found for user {user_email}")
            return
        
        print(f"Found {len(cars)} cars for user {user_email}")
        for i, car in enumerate(cars[:10]):  # Show first 10 cars
            print(f"{i+1}. {car.get('company', 'Unknown')} {car.get('name', 'Unknown')} ({car.get('year', 'Unknown')})")
        
        if len(cars) > 10:
            print(f"... and {len(cars) - 10} more")
    
    elif command == "delete" and len(sys.argv) == 3:
        user_email = sys.argv[2]
        
        user = get_user_by_email(user_email)
        if not user:
            print(f"User not found: {user_email}")
            return
        
        user_id = str(user['_id'])
        delete_user_cars(user_id)
    
    else:
        print("Invalid command or arguments")
        print("Usage:")
        print("  python manage_user_car_data.py import <user_email> <csv_file>")
        print("  python manage_user_car_data.py list <user_email>")
        print("  python manage_user_car_data.py delete <user_email>")

if __name__ == "__main__":
    main()