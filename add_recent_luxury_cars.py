#!/usr/bin/env python3
"""
Add recent luxury cars with low mileage to fix prediction issues
"""

import pandas as pd
import numpy as np
import random

def add_recent_luxury_cars():
    """Add recent luxury cars with low mileage"""
    print("Loading enhanced dataset...")
    df = pd.read_csv('enhanced_indian_car_dataset.csv')
    print(f"Original dataset: {len(df)} records")
    
    # Recent luxury car data with realistic prices
    recent_cars = [
        # BMW X5 2024 variants
        {'company': 'BMW', 'model': 'X5', 'year': 2024, 'price_range': (4500000, 6500000), 'engine_size': 3000, 'power': 265, 'km_range': (500, 5000)},
        {'company': 'BMW', 'model': 'X5', 'year': 2023, 'price_range': (4200000, 6000000), 'engine_size': 3000, 'power': 265, 'km_range': (1000, 10000)},
        {'company': 'BMW', 'model': 'X5', 'year': 2022, 'price_range': (3800000, 5500000), 'engine_size': 3000, 'power': 265, 'km_range': (5000, 20000)},
        
        # Mercedes-Benz C-Class 2024
        {'company': 'Mercedes-Benz', 'model': 'C-Class', 'year': 2024, 'price_range': (4000000, 5500000), 'engine_size': 2000, 'power': 255, 'km_range': (500, 5000)},
        {'company': 'Mercedes-Benz', 'model': 'C-Class', 'year': 2023, 'price_range': (3800000, 5200000), 'engine_size': 2000, 'power': 255, 'km_range': (1000, 10000)},
        
        # Audi A6 2024
        {'company': 'Audi', 'model': 'A6', 'year': 2024, 'price_range': (5000000, 7000000), 'engine_size': 3000, 'power': 340, 'km_range': (500, 5000)},
        {'company': 'Audi', 'model': 'A6', 'year': 2023, 'price_range': (4800000, 6500000), 'engine_size': 3000, 'power': 340, 'km_range': (1000, 10000)},
        
        # Jaguar F-PACE 2024
        {'company': 'Jaguar', 'model': 'F-PACE', 'year': 2024, 'price_range': (5000000, 7500000), 'engine_size': 3000, 'power': 340, 'km_range': (500, 5000)},
        
        # Land Rover Range Rover 2024
        {'company': 'Land Rover', 'model': 'Range Rover', 'year': 2024, 'price_range': (8000000, 12000000), 'engine_size': 3000, 'power': 400, 'km_range': (500, 3000)},
    ]
    
    new_cars = []
    
    for car_template in recent_cars:
        # Generate multiple variations
        for i in range(50):  # 50 variations per car
            # Randomize parameters
            year = car_template['year'] - random.randint(0, 1)  # Allow 2023-2024
            kilometers_driven = random.randint(car_template['km_range'][0], car_template['km_range'][1])
            
            # Price based on year and condition
            base_price = random.uniform(car_template['price_range'][0], car_template['price_range'][1])
            year_factor = 1.0 - (2024 - year) * 0.03  # 3% depreciation per year
            km_factor = 1.0 - (kilometers_driven / 100000) * 0.05  # 5% depreciation per 100k km
            final_price = base_price * year_factor * km_factor
            
            # Randomize other features
            conditions = ['Excellent', 'Good']
            car_condition = random.choice(conditions)
            condition_factor = {'Excellent': 1.0, 'Good': 0.95}[car_condition]
            final_price *= condition_factor
            
            owners = ['1st', '2nd']
            owner_count = random.choice(owners)
            owner_factor = {'1st': 1.0, '2nd': 0.98}[owner_count]
            final_price *= owner_factor
            
            # Ensure reasonable bounds
            final_price = max(1000000, min(final_price, car_template['price_range'][1]))
            
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
                'previous_accidents': random.randint(0, 1),
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
    
    print(f"Added {len(new_cars)} recent luxury cars")
    print(f"Enhanced dataset: {len(enhanced_df)} records")
    
    # Save enhanced dataset
    enhanced_df.to_csv('enhanced_indian_car_dataset.csv', index=False)
    print("Enhanced dataset saved successfully")
    
    # Show statistics
    print("\nRecent Luxury Car Statistics:")
    recent_df = enhanced_df[enhanced_df['year'] >= 2023]
    luxury_recent = recent_df[recent_df['company'].isin(['BMW', 'Mercedes-Benz', 'Audi', 'Jaguar', 'Land Rover'])]
    print(f"Recent luxury cars (2023+): {len(luxury_recent)}")
    print(f"Price range: ₹{luxury_recent['Price'].min():,.0f} - ₹{luxury_recent['Price'].max():,.0f}")
    print(f"KM range: {luxury_recent['kilometers_driven'].min()} - {luxury_recent['kilometers_driven'].max()}")
    
    # Check BMW X5 2024 with low mileage
    bmw_2024_low_km = enhanced_df[(enhanced_df['company'] == 'BMW') & (enhanced_df['model'] == 'X5') & (enhanced_df['year'] == 2024) & (enhanced_df['kilometers_driven'] <= 5000)]
    print(f"\nBMW X5 2024 with <5k km: {len(bmw_2024_low_km)}")
    if len(bmw_2024_low_km) > 0:
        print(f"Price range: ₹{bmw_2024_low_km['Price'].min():,.0f} - ₹{bmw_2024_low_km['Price'].max():,.0f}")
        print(f"Average price: ₹{bmw_2024_low_km['Price'].mean():,.0f}")
    
    return enhanced_df

if __name__ == "__main__":
    enhanced_df = add_recent_luxury_cars()
