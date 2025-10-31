#!/usr/bin/env python3
"""
Real-time Synthetic Data Generator for Car Price Predictor
Generates synthetic data on-the-fly for the application
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os
import random

# GST mapping (for reference in exports; model should use base price)
GST_RATES = {2019: 18, 2020: 20, 2021: 22, 2022: 25, 2023: 26, 2024: 28, 2025: 28}

# Showroom depreciation rates (percentage drop in first year)
SHOWROOM_DEPRECIATION = {
    'Budget': 15,      # Budget cars (< 5 lakh)
    'Mid-Range': 20,   # Mid-range cars (5-10 lakh)
    'Premium': 25,     # Premium cars (10-20 lakh)
    'Luxury': 30       # Luxury cars (> 20 lakh)
}

class RealtimeSyntheticDataGenerator:
    """Generates synthetic car data in real-time for the application"""
    
    def __init__(self, base_dataset_path='enhanced_indian_car_dataset.csv'):
        """Initialize the generator with the base dataset"""
        self.base_dataset_path = base_dataset_path
        self.current_year = datetime.now().year
        self.load_base_dataset()
        
    def load_base_dataset(self):
        """Load the base dataset for reference"""
        if os.path.exists(self.base_dataset_path):
            self.base_df = pd.read_csv(self.base_dataset_path)
            print(f"[OK] Base dataset loaded - {len(self.base_df)} records")
        else:
            print(f"[WARNING] Base dataset not found: {self.base_dataset_path}")
            self.base_df = pd.DataFrame()
    
    def generate_synthetic_car(self, company=None, model=None, year=None):
        """Generate a single synthetic car based on parameters"""
        # If no company specified, pick one from the dataset
        if not company:
            companies = self.base_df['company'].unique()
            company = random.choice(companies) if len(companies) > 0 else "Maruti"
            
        # If no model specified, pick one for the company
        if not model:
            company_models = self.base_df[self.base_df['company'] == company]['model'].unique()
            model = random.choice(company_models) if len(company_models) > 0 else "Swift"
            
        # If no year specified, use current year
        if not year:
            year = self.current_year
            
        # Get reference data for this company/model
        reference_data = self.base_df[(self.base_df['company'] == company) & 
                                      (self.base_df['model'] == model)]
        
        if len(reference_data) == 0:
            # No reference data, use general averages
            avg_price = 800000  # Default price
            fuel_type = random.choice(['Petrol', 'Diesel', 'CNG'])
            transmission = random.choice(['Manual', 'Automatic'])
        else:
            # Use reference data for realistic values
            avg_price = reference_data['Price'].median()
            fuel_types = reference_data['fuel_type'].unique()
            fuel_type = random.choice(fuel_types) if len(fuel_types) > 0 else 'Petrol'
            
            if 'transmission' in reference_data.columns:
                transmissions = reference_data['transmission'].unique()
                transmission = random.choice(transmissions) if len(transmissions) > 0 else 'Manual'
            else:
                transmission = random.choice(['Manual', 'Automatic'])
        
        # Adjust price for year (newer = more expensive)
        ref_year = reference_data['year'].max() if len(reference_data) > 0 else 2020
        year_diff = year - ref_year
        price_adjustment = 1.0 + (year_diff * 0.05)  # 5% increase per year
        
        # Add some randomness
        price_noise = random.uniform(0.9, 1.1)
        
        # Calculate base price
        base_price = avg_price * price_adjustment * price_noise
        
        # Determine if it's a new car (showroom condition)
        is_showroom_new = random.random() < 0.2  # 20% chance of being showroom new
        
        # Calculate kilometers driven
        if is_showroom_new:
            kilometers_driven = random.randint(0, 500)  # Very low mileage for new cars
        else:
            # Older cars have more kilometers
            year_age = self.current_year - year
            km_base = 5000 + (year_age * 10000)  # Base km per year
            kilometers_driven = random.randint(km_base * 0.5, km_base * 1.5)
        
        # Determine price category
        if base_price < 500000:
            price_category = 'Budget'
        elif base_price < 1000000:
            price_category = 'Mid-Range'
        elif base_price < 2000000:
            price_category = 'Premium'
        else:
            price_category = 'Luxury'
        
        # Apply showroom depreciation if it's a new car
        if is_showroom_new:
            depreciation_rate = SHOWROOM_DEPRECIATION.get(price_category, 20)
            depreciated_price = base_price * (1 - (depreciation_rate / 100))
        else:
            depreciated_price = base_price
        
        # Apply GST
        gst_percentage = GST_RATES.get(year, 18)
        price_with_gst = depreciated_price * (1 + (gst_percentage / 100))
        
        # Create synthetic car data
        synthetic_car = {
            'company': company,
            'model': model,
            'year': year,
            'kilometers_driven': kilometers_driven,
            'fuel_type': fuel_type,
            'transmission': transmission,
            'Price': round(depreciated_price, 2),
            'base_price': round(base_price, 2),
            'price_with_gst': round(price_with_gst, 2),
            'gst_percentage': gst_percentage,
            'is_showroom_new': is_showroom_new,
            'depreciation_applied': depreciation_rate if is_showroom_new else 0,
            'is_synthetic': True
        }
        
        return synthetic_car
    
    def generate_batch(self, count=10, params=None):
        """Generate a batch of synthetic cars"""
        if params is None:
            params = {}
            
        synthetic_cars = []
        for _ in range(count):
            synthetic_car = self.generate_synthetic_car(
                company=params.get('company'),
                model=params.get('model'),
                year=params.get('year')
            )
            synthetic_cars.append(synthetic_car)
            
        return synthetic_cars

# Singleton instance for use in the application
generator = RealtimeSyntheticDataGenerator()

def get_synthetic_car(company=None, model=None, year=None):
    """Get a single synthetic car"""
    return generator.generate_synthetic_car(company, model, year)

def get_synthetic_batch(count=10, params=None):
    """Get a batch of synthetic cars"""
    return generator.generate_batch(count, params)

if __name__ == '__main__':
    # Test the generator
    print("Testing Real-time Synthetic Data Generator")
    gen = RealtimeSyntheticDataGenerator()
    
    print("\nGenerating a single synthetic car:")
    car = gen.generate_synthetic_car()
    for key, value in car.items():
        print(f"{key}: {value}")
    
    print("\nGenerating a batch of 5 synthetic cars:")
    cars = gen.generate_batch(5)
    for i, car in enumerate(cars, 1):
        print(f"\nCar {i}:")
        print(f"Company: {car['company']}")
        print(f"Model: {car['model']}")
        print(f"Year: {car['year']}")
        print(f"Base Price: ₹{car['base_price']:,.2f}")
        print(f"Depreciated Price: ₹{car['Price']:,.2f}")
        print(f"GST: {car['gst_percentage']}%")
        print(f"Final Price with GST: ₹{car['price_with_gst']:,.2f}")
        print(f"Showroom New: {'Yes' if car['is_showroom_new'] else 'No'}")
        if car['is_showroom_new']:
            print(f"Depreciation Applied: {car['depreciation_applied']}%")