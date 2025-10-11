#!/usr/bin/env python3
"""
Comprehensive Model Training for All Car Brands
Fixes NaN errors and ensures all brands work properly
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import pickle
import warnings
warnings.filterwarnings('ignore')

def train_comprehensive_model():
    """Train a comprehensive model that handles all car brands"""
    print("Loading enhanced dataset...")
    df = pd.read_csv('enhanced_indian_car_dataset.csv')
    print(f"Loaded {len(df)} records")
    
    # Check all brands in dataset
    brands = df['company'].unique()
    print(f"Brands in dataset: {len(brands)}")
    print(f"Brands: {sorted(brands)}")
    
    # Feature engineering with robust handling
    df['age'] = 2024 - df['year']
    df['price_per_km'] = df['Price'] / (df['kilometers_driven'] + 1)
    df['engine_power_ratio'] = df['power'] / (df['engine_size'] + 1)
    
    # Create binary features with proper handling
    df['is_electric'] = (df['fuel_type'] == 'Electric').astype(int)
    df['is_hybrid'] = (df['fuel_type'] == 'Hybrid').astype(int)
    df['is_automatic'] = (df['transmission'] == 'Automatic').astype(int)
    df['is_first_owner'] = (df['owner_count'] == '1st').astype(int)
    df['is_certified'] = df['is_certified'].astype(int)
    
    # Define features
    categorical_features = ['company', 'model', 'fuel_type', 'transmission', 
                           'owner_count', 'car_condition', 'city', 'emission_norm', 
                           'maintenance_level', 'insurance_eligible', 'listing_type']
    
    numerical_features = ['year', 'kilometers_driven', 'engine_size', 'power', 
                        'num_doors', 'previous_accidents', 'age', 'price_per_km', 
                        'engine_power_ratio', 'is_electric', 'is_hybrid', 
                        'is_automatic', 'is_first_owner', 'is_certified']
    
    # Prepare features and target with robust data cleaning
    X = df[categorical_features + numerical_features].copy()
    y = df['Price'].copy()
    
    # Clean data - remove any rows with NaN values
    mask = ~(X.isnull().any(axis=1) | y.isnull())
    X = X[mask]
    y = y[mask]
    
    print(f"After cleaning: {len(X)} records")
    print(f"Features: {len(categorical_features)} categorical, {len(numerical_features)} numerical")
    print(f"Target range: ₹{y.min():,.0f} - ₹{y.max():,.0f}")
    
    # Check brand distribution after cleaning
    brand_counts = X['company'].value_counts()
    print(f"\nBrand distribution (top 10):")
    for brand, count in brand_counts.head(10).items():
        print(f"  {brand}: {count} cars")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print(f"\nTraining set: {len(X_train)} samples")
    print(f"Test set: {len(X_test)} samples")
    
    # Create robust preprocessing pipeline
    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False, drop=None))
    ])
    
    numerical_transformer = Pipeline(steps=[
        ('scaler', StandardScaler())
    ])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', categorical_transformer, categorical_features),
            ('num', numerical_transformer, numerical_features)
        ],
        remainder='drop'
    )
    
    # Create comprehensive model pipeline
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(
            n_estimators=200,
            max_depth=25,
            min_samples_split=3,
            min_samples_leaf=1,
            max_features='sqrt',
            random_state=42,
            n_jobs=-1,
            verbose=0
        ))
    ])
    
    print("\nTraining comprehensive model...")
    model.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"\nModel Performance:")
    print(f"R² Score: {r2:.4f}")
    print(f"RMSE: ₹{np.sqrt(mse):,.0f}")
    print(f"MAE: ₹{mae:,.0f}")
    
    # Test on various brands
    test_brands = ['Hyundai', 'Kia', 'BMW', 'Mercedes-Benz', 'Maruti Suzuki', 'Toyota', 'Honda']
    print(f"\nTesting predictions for various brands:")
    
    for brand in test_brands:
        brand_cars = X_test[X_test['company'] == brand]
        if len(brand_cars) > 0:
            brand_pred = model.predict(brand_cars)
            brand_actual = y_test[brand_cars.index]
            brand_r2 = r2_score(brand_actual, brand_pred)
            brand_mae = mean_absolute_error(brand_actual, brand_pred)
            print(f"  {brand}: R² = {brand_r2:.3f}, MAE = ₹{brand_mae:,.0f} ({len(brand_cars)} samples)")
        else:
            print(f"  {brand}: No test samples")
    
    # Test specific problematic cases
    print(f"\nTesting specific cases:")
    
    # Test Hyundai Venue
    hyundai_venue = X_test[(X_test['company'] == 'Hyundai') & (X_test['model'] == 'Venue')]
    if len(hyundai_venue) > 0:
        venue_pred = model.predict(hyundai_venue)
        venue_actual = y_test[hyundai_venue.index]
        print(f"  Hyundai Venue: Predicted ₹{venue_pred[0]:,.0f}, Actual ₹{venue_actual.iloc[0]:,.0f}")
    else:
        print(f"  Hyundai Venue: No test samples")
    
    # Test Kia Carnival
    kia_carnival = X_test[(X_test['company'] == 'Kia') & (X_test['model'] == 'Carnival')]
    if len(kia_carnival) > 0:
        carnival_pred = model.predict(kia_carnival)
        carnival_actual = y_test[kia_carnival.index]
        print(f"  Kia Carnival: Predicted ₹{carnival_pred[0]:,.0f}, Actual ₹{carnival_actual.iloc[0]:,.0f}")
    else:
        print(f"  Kia Carnival: No test samples")
    
    # Save the comprehensive model
    model_data = {
        'model': model,
        'model_name': 'Comprehensive RandomForest',
        'categorical_features': categorical_features,
        'numerical_features': numerical_features,
        'all_features': categorical_features + numerical_features,
        'performance': {
            'r2_score': r2,
            'rmse': np.sqrt(mse),
            'mae': mae
        },
        'training_info': {
            'dataset_size': len(X),
            'features_count': len(categorical_features) + len(numerical_features),
            'model_type': 'RandomForest',
            'brands_count': len(brands),
            'brands': sorted(brands)
        }
    }
    
    with open('Comprehensive_Model.pkl', 'wb') as f:
        pickle.dump(model_data, f)
    
    print(f"\nComprehensive model saved as: Comprehensive_Model.pkl")
    print(f"Model supports {len(brands)} brands: {sorted(brands)}")
    
    return model_data

if __name__ == "__main__":
    comprehensive_model = train_comprehensive_model()
