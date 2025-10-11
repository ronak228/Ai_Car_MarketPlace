#!/usr/bin/env python3
"""
Add recent luxury cars to the dataset for better predictions
"""

import pandas as pd
import numpy as np
import random

def add_luxury_cars():
    """Add recent luxury cars to the dataset"""
    print("Loading enhanced dataset...")
    df = pd.read_csv('enhanced_indian_car_dataset.csv')
    print(f"Original dataset: {len(df)} records")
    
    # Luxury car data
    luxury_cars = [
        # BMW
        {'company': 'BMW', 'model': 'X5', 'year': 2024, 'price_range': (4500000, 6500000), 'engine_size': 3000, 'power': 265},
        {'company': 'BMW', 'model': 'X5', 'year': 2023, 'price_range': (4200000, 6000000), 'engine_size': 3000, 'power': 265},
        {'company': 'BMW', 'model': 'X5', 'year': 2022, 'price_range': (3800000, 5500000), 'engine_size': 3000, 'power': 265},
        {'company': 'BMW', 'model': '3 Series', 'year': 2024, 'price_range': (3500000, 5000000), 'engine_size': 2000, 'power': 184},
        {'company': 'BMW', 'model': '5 Series', 'year': 2024, 'price_range': (5500000, 7500000), 'engine_size': 3000, 'power': 340},
        
        # Mercedes-Benz
        {'company': 'Mercedes-Benz', 'model': 'C-Class', 'year': 2024, 'price_range': (4000000, 5500000), 'engine_size': 2000, 'power': 255},
        {'company': 'Mercedes-Benz', 'model': 'E-Class', 'year': 2024, 'price_range': (5500000, 7500000), 'engine_size': 3000, 'power': 258},
        {'company': 'Mercedes-Benz', 'model': 'S-Class', 'year': 2024, 'price_range': (12000000, 18000000), 'engine_size': 3000, 'power': 367},
        {'company': 'Mercedes-Benz', 'model': 'GLC', 'year': 2024, 'price_range': (4500000, 6500000), 'engine_size': 2000, 'power': 194},
        
        # Audi
        {'company': 'Audi', 'model': 'A4', 'year': 2024, 'price_range': (3500000, 5000000), 'engine_size': 2000, 'power': 190},
        {'company': 'Audi', 'model': 'A6', 'year': 2024, 'price_range': (5000000, 7000000), 'engine_size': 3000, 'power': 340},
        {'company': 'Audi', 'model': 'Q5', 'year': 2024, 'price_range': (4500000, 6500000), 'engine_size': 2000, 'power': 190},
        {'company': 'Audi', 'model': 'Q7', 'year': 2024, 'price_range': (6500000, 9500000), 'engine_size': 3000, 'power': 340},
        
        # Jaguar
        {'company': 'Jaguar', 'model': 'XF', 'year': 2024, 'price_range': (4500000, 6500000), 'engine_size': 2000, 'power': 250},
        {'company': 'Jaguar', 'model': 'F-PACE', 'year': 2024, 'price_range': (5000000, 7500000), 'engine_size': 3000, 'power': 340},
        
        # Land Rover
        {'company': 'Land Rover', 'model': 'Range Rover', 'year': 2024, 'price_range': (8000000, 12000000), 'engine_size': 3000, 'power': 400},
        {'company': 'Land Rover', 'model': 'Discovery', 'year': 2024, 'price_range': (5500000, 8000000), 'engine_size': 3000, 'power': 300},
    ]
    
    new_cars = []
    
    for car_template in luxury_cars:
        # Generate multiple variations
        for i in range(20):  # 20 variations per car
            # Randomize some parameters
            year = car_template['year'] - random.randint(0, 2)  # Allow 2022-2024
            km_range = (1000, 50000) if year >= 2023 else (1000, 100000)
            kilometers_driven = random.randint(km_range[0], km_range[1])
            
            # Price based on year and condition
            base_price = random.uniform(car_template['price_range'][0], car_template['price_range'][1])
            year_factor = 1.0 - (2024 - year) * 0.05  # 5% depreciation per year
            km_factor = 1.0 - (kilometers_driven / 100000) * 0.1  # 10% depreciation per 100k km
            final_price = base_price * year_factor * km_factor
            
            # Randomize other features
            conditions = ['Excellent', 'Good', 'Fair']
            car_condition = random.choice(conditions)
            condition_factor = {'Excellent': 1.0, 'Good': 0.9, 'Fair': 0.8}[car_condition]
            final_price *= condition_factor
            
            owners = ['1st', '2nd', '3rd']
            owner_count = random.choice(owners)
            owner_factor = {'1st': 1.0, '2nd': 0.95, '3rd': 0.9}[owner_count]
            final_price *= owner_factor
            
            # Ensure reasonable bounds
            final_price = max(500000, min(final_price, car_template['price_range'][1]))
            
            new_car = {
                'car_id': len(df) + len(new_cars) + 1,
                'company': car_template['company'],
                'model': car_template['model'],
                'year': year,
                'Price': final_price,
                'kilometers_driven': kilometers_driven,
                'fuel_type': random.choice(['Petrol', 'Diesel']),
                'transmission': random.choice(['Automatic', 'Manual']),
                'owner_count': owner_count,
                'car_condition': car_condition,
                'city': random.choice(['Delhi', 'Mumbai', 'Bangalore', 'Chennai', 'Hyderabad']),
                'engine_size': car_template['engine_size'],
                'power': car_template['power'],
                'num_doors': random.choice([4, 5]),
                'previous_accidents': random.randint(0, 2),
                'insurance_status': random.choice(['Yes', 'No']),
                'emission_norm': 'BS6',
                'maintenance_level': random.choice(['High', 'Medium']),
                'insurance_eligible': 'Yes',
                'listing_type': random.choice(['Dealer', 'Individual']),
                'is_certified': random.choice([True, False])
            }
            
            new_cars.append(new_car)
    
    # Add new cars to dataset
    new_df = pd.DataFrame(new_cars)
    enhanced_df = pd.concat([df, new_df], ignore_index=True)
    
    print(f"Added {len(new_cars)} luxury cars")
    print(f"Enhanced dataset: {len(enhanced_df)} records")
    
    # Save enhanced dataset
    enhanced_df.to_csv('enhanced_indian_car_dataset.csv', index=False)
    print("Enhanced dataset saved successfully")
    
    # Show statistics
    print("\nLuxury Car Statistics:")
    luxury_df = enhanced_df[enhanced_df['company'].isin(['BMW', 'Mercedes-Benz', 'Audi', 'Jaguar', 'Land Rover'])]
    print(f"Total luxury cars: {len(luxury_df)}")
    print(f"Price range: ₹{luxury_df['Price'].min():,.0f} - ₹{luxury_df['Price'].max():,.0f}")
    print(f"Year range: {luxury_df['year'].min()} - {luxury_df['year'].max()}")
    
    return enhanced_df

if __name__ == "__main__":
    enhanced_df = add_luxury_cars()
