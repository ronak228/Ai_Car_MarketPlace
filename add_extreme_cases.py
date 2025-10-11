#!/usr/bin/env python3
"""
Add extreme/worst case scenarios to the dataset
This will help the model handle edge cases better
"""

import pandas as pd
import numpy as np
import random

def add_extreme_cases():
    """Add extreme cases to the enhanced dataset"""
    print("Loading enhanced dataset...")
    df = pd.read_csv('enhanced_indian_car_dataset.csv')
    print(f"Original dataset: {len(df)} records")
    
    # Create extreme cases
    extreme_cases = []
    
    # Define extreme scenarios
    scenarios = [
        {
            'name': 'Very Old Car',
            'year_range': (1995, 2005),
            'km_range': (200000, 500000),
            'condition': 'Poor',
            'accidents': (3, 8),
            'owner': '4th+',
            'maintenance': 'Low',
            'insurance': 'No'
        },
        {
            'name': 'High Mileage Car',
            'year_range': (2010, 2018),
            'km_range': (300000, 600000),
            'condition': 'Fair',
            'accidents': (2, 5),
            'owner': '3rd',
            'maintenance': 'Low',
            'insurance': 'No'
        },
        {
            'name': 'Multiple Accidents',
            'year_range': (2015, 2020),
            'km_range': (50000, 150000),
            'condition': 'Poor',
            'accidents': (5, 10),
            'owner': '2nd',
            'maintenance': 'Low',
            'insurance': 'No'
        },
        {
            'name': 'Very Small Engine',
            'year_range': (2008, 2015),
            'km_range': (100000, 300000),
            'condition': 'Fair',
            'accidents': (1, 3),
            'owner': '3rd',
            'maintenance': 'Medium',
            'insurance': 'Yes',
            'engine_size_range': (600, 1000),
            'power_range': (30, 60)
        },
        {
            'name': 'High End Damaged',
            'year_range': (2018, 2022),
            'km_range': (20000, 80000),
            'condition': 'Poor',
            'accidents': (4, 7),
            'owner': '2nd',
            'maintenance': 'Low',
            'insurance': 'No',
            'companies': ['BMW', 'Mercedes-Benz', 'Audi', 'Jaguar', 'Land Rover']
        }
    ]
    
    # Get unique values for reference
    companies = df['company'].unique()
    models = df['model'].unique()
    fuel_types = df['fuel_type'].unique()
    transmissions = df['transmission'].unique()
    cities = df['city'].unique()
    emission_norms = df['emission_norm'].unique()
    
    # Generate extreme cases
    for scenario in scenarios:
        print(f"Generating {scenario['name']} cases...")
        
        for i in range(50):  # 50 cases per scenario
            # Select company and model
            if 'companies' in scenario:
                company = random.choice(scenario['companies'])
                # Get models for this company
                company_models = df[df['company'] == company]['model'].unique()
                if len(company_models) > 0:
                    model = random.choice(company_models)
                else:
                    company = random.choice(companies)
                    model = random.choice(df[df['company'] == company]['model'].unique())
            else:
                company = random.choice(companies)
                model = random.choice(df[df['company'] == company]['model'].unique())
            
            # Generate extreme values
            year = random.randint(scenario['year_range'][0], scenario['year_range'][1])
            kilometers_driven = random.randint(scenario['km_range'][0], scenario['km_range'][1])
            previous_accidents = random.randint(scenario['accidents'][0], scenario['accidents'][1])
            
            # Engine specs
            if 'engine_size_range' in scenario:
                engine_size = random.randint(scenario['engine_size_range'][0], scenario['engine_size_range'][1])
                power = random.randint(scenario['power_range'][0], scenario['power_range'][1])
            else:
                # Get typical engine specs for this model
                model_data = df[(df['company'] == company) & (df['model'] == model)]
                if len(model_data) > 0:
                    engine_size = random.choice(model_data['engine_size'].values)
                    power = random.choice(model_data['power'].values)
                else:
                    engine_size = random.randint(1000, 2000)
                    power = random.randint(80, 150)
            
            # Calculate realistic price based on extreme conditions
            base_price = df[(df['company'] == company) & (df['model'] == model)]['Price'].median()
            if pd.isna(base_price):
                base_price = df['Price'].median()
            
            # Apply extreme depreciation factors
            age_factor = max(0.1, 1 - (2024 - year) * 0.15)  # Heavy depreciation
            km_factor = max(0.05, 1 - (kilometers_driven / 100000) * 0.3)  # High mileage penalty
            accident_factor = max(0.1, 1 - previous_accidents * 0.1)  # Accident penalty
            condition_factor = 0.3 if scenario['condition'] == 'Poor' else 0.6  # Poor condition penalty
            
            # Calculate extreme price
            extreme_price = base_price * age_factor * km_factor * accident_factor * condition_factor
            extreme_price = max(50000, min(extreme_price, base_price * 0.8))  # Reasonable bounds
            
            # Create extreme case
            extreme_case = {
                'car_id': len(df) + len(extreme_cases) + 1,
                'company': company,
                'model': model,
                'year': year,
                'Price': extreme_price,
                'kilometers_driven': kilometers_driven,
                'fuel_type': random.choice(fuel_types),
                'transmission': random.choice(transmissions),
                'owner_count': scenario['owner'],
                'car_condition': scenario['condition'],
                'city': random.choice(cities),
                'engine_size': engine_size,
                'power': power,
                'num_doors': random.choice([4, 5]),
                'previous_accidents': previous_accidents,
                'insurance_status': scenario['insurance'],
                'emission_norm': random.choice(emission_norms),
                'maintenance_level': scenario['maintenance'],
                'insurance_eligible': 'No' if scenario['insurance'] == 'No' else 'Yes',
                'listing_type': 'Individual',
                'is_certified': False
            }
            
            extreme_cases.append(extreme_case)
    
    # Add extreme cases to dataset
    extreme_df = pd.DataFrame(extreme_cases)
    enhanced_df = pd.concat([df, extreme_df], ignore_index=True)
    
    print(f"Added {len(extreme_cases)} extreme cases")
    print(f"Enhanced dataset: {len(enhanced_df)} records")
    
    # Save enhanced dataset
    enhanced_df.to_csv('enhanced_indian_car_dataset.csv', index=False)
    print("Enhanced dataset saved successfully")
    
    # Show statistics
    print("\nPrice Statistics:")
    print(f"Min Price: ₹{enhanced_df['Price'].min():,.0f}")
    print(f"Max Price: ₹{enhanced_df['Price'].max():,.0f}")
    print(f"Median Price: ₹{enhanced_df['Price'].median():,.0f}")
    
    print("\nYear Statistics:")
    print(f"Min Year: {enhanced_df['year'].min()}")
    print(f"Max Year: {enhanced_df['year'].max()}")
    
    print("\nMileage Statistics:")
    print(f"Min KM: {enhanced_df['kilometers_driven'].min():,}")
    print(f"Max KM: {enhanced_df['kilometers_driven'].max():,}")
    
    print("\nAccident Statistics:")
    print(f"Max Accidents: {enhanced_df['previous_accidents'].max()}")
    
    return enhanced_df

if __name__ == "__main__":
    enhanced_df = add_extreme_cases()
