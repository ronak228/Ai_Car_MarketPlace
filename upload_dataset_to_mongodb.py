#!/usr/bin/env python3
"""
Upload Car Dataset to MongoDB
This script uploads the car dataset to MongoDB Atlas for persistent storage
"""

import os
import pandas as pd
from pymongo import MongoClient, UpdateOne
from mongodb_config import get_sync_client, MONGODB_DATABASE
import json
from tqdm import tqdm

# Dataset files to check
DATASET_FILES = [
    'enhanced_indian_car_dataset.csv',
    'indian_car_brands_dataset.csv',
    'Cleaned_Car_data_master.csv'
]

# MongoDB collection for car data
CAR_COLLECTION = 'car_dataset'

def find_dataset_file():
    """Find the first available dataset file"""
    for file in DATASET_FILES:
        if os.path.exists(file):
            print(f"[OK] Found dataset file: {file}")
            return file
    raise FileNotFoundError(f"No dataset file found. Expected one of: {', '.join(DATASET_FILES)}")

def upload_dataset_to_mongodb():
    """Upload the dataset to MongoDB"""
    # Find dataset file
    dataset_file = find_dataset_file()
    
    # Load dataset
    print(f"[INFO] Loading dataset from {dataset_file}...")
    df = pd.read_csv(dataset_file)
    print(f"[OK] Loaded {len(df)} records from {dataset_file}")
    
    # Connect to MongoDB
    client = get_sync_client()
    if not client:
        print("[ERROR] Failed to connect to MongoDB")
        return False
    
    # Get database and collection
    db = client[MONGODB_DATABASE]
    collection = db[CAR_COLLECTION]
    
    # Check if collection already has data
    existing_count = collection.count_documents({})
    if existing_count > 0:
        print(f"[INFO] Collection already has {existing_count} documents")
        user_input = input("Do you want to replace existing data? (y/n): ")
        if user_input.lower() != 'y':
            print("[INFO] Operation cancelled by user")
            return False
        # Drop existing collection
        collection.drop()
        print("[OK] Existing collection dropped")
    
    # Convert DataFrame to list of dictionaries
    print("[INFO] Preparing data for MongoDB...")
    records = df.to_dict('records')
    
    # Add unique _id field based on combination of fields
    for record in records:
        # Create a unique identifier from company, model, year, and fuel_type
        unique_fields = {
            'company': str(record.get('company', '')),
            'model': str(record.get('model', '')),
            'year': str(record.get('year', '')),
            'fuel_type': str(record.get('fuel_type', ''))
        }
        # Convert to string and use as _id
        record['_id'] = f"{unique_fields['company']}_{unique_fields['model']}_{unique_fields['year']}_{unique_fields['fuel_type']}"
    
    # Insert data in batches
    batch_size = 1000
    total_batches = (len(records) + batch_size - 1) // batch_size
    
    print(f"[INFO] Uploading {len(records)} records to MongoDB in {total_batches} batches...")
    
    for i in tqdm(range(0, len(records), batch_size)):
        batch = records[i:i+batch_size]
        try:
            # Use bulk write with upsert to handle duplicates
            operations = [
                UpdateOne(
                    {'_id': record['_id']},
                    {'$set': record},
                    upsert=True
                ) for record in batch
            ]
            result = collection.bulk_write(operations)
            
        except Exception as e:
            print(f"[ERROR] Failed to upload batch: {str(e)}")
            return False
    
    # Verify upload
    final_count = collection.count_documents({})
    print(f"[OK] Successfully uploaded dataset to MongoDB")
    print(f"[STATS] Total records in MongoDB: {final_count}")
    
    # Create indexes for better query performance
    print("[INFO] Creating indexes...")
    collection.create_index([("company", 1)])
    collection.create_index([("model", 1)])
    collection.create_index([("year", 1)])
    collection.create_index([("fuel_type", 1)])
    print("[OK] Indexes created successfully")
    
    return True

if __name__ == "__main__":
    print("=== Car Dataset MongoDB Uploader ===")
    success = upload_dataset_to_mongodb()
    if success:
        print("[SUCCESS] Dataset uploaded to MongoDB successfully")
    else:
        print("[FAILED] Failed to upload dataset to MongoDB")