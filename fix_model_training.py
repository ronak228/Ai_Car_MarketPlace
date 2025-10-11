#!/usr/bin/env python3
"""
Fix the enhanced model training to ensure proper predictions
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

def fix_model_training():
    """Retrain the model with proper preprocessing"""
    print("Loading enhanced dataset...")
    df = pd.read_csv('enhanced_indian_car_dataset.csv')
    print(f"Loaded {len(df)} records")
    
    # Feature engineering
    df['age'] = 2024 - df['year']
    df['price_per_km'] = df['Price'] / (df['kilometers_driven'] + 1)
    df['engine_power_ratio'] = df['power'] / (df['engine_size'] + 1)
    
    # Create binary features
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
    
    # Prepare features and target
    X = df[categorical_features + numerical_features].copy()
    y = df['Price'].copy()
    
    print(f"Features: {len(categorical_features)} categorical, {len(numerical_features)} numerical")
    print(f"Target range: ₹{y.min():,.0f} - ₹{y.max():,.0f}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print(f"Training set: {len(X_train)} samples")
    print(f"Test set: {len(X_test)} samples")
    
    # Create preprocessing pipeline
    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])
    
    numerical_transformer = Pipeline(steps=[
        ('scaler', StandardScaler())
    ])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', categorical_transformer, categorical_features),
            ('num', numerical_transformer, numerical_features)
        ])
    
    # Create model pipeline
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(
            n_estimators=100,
            max_depth=20,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        ))
    ])
    
    print("Training model...")
    model.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"Model Performance:")
    print(f"R² Score: {r2:.4f}")
    print(f"RMSE: ₹{np.sqrt(mse):,.0f}")
    print(f"MAE: ₹{mae:,.0f}")
    
    # Test on BMW X5 sample
    bmw_sample = df[df['model'] == 'X5'].iloc[0]
    sample_input = X.iloc[[bmw_sample.name]]
    sample_prediction = model.predict(sample_input)[0]
    sample_actual = bmw_sample['Price']
    
    print(f"\nBMW X5 Test:")
    print(f"Actual Price: ₹{sample_actual:,.0f}")
    print(f"Predicted Price: ₹{sample_prediction:,.0f}")
    print(f"Error: ₹{abs(sample_prediction - sample_actual):,.0f}")
    print(f"Error %: {abs(sample_prediction - sample_actual) / sample_actual * 100:.1f}%")
    
    # Save the fixed model
    model_data = {
        'model': model,
        'model_name': 'Fixed Enhanced RandomForest',
        'categorical_features': categorical_features,
        'numerical_features': numerical_features,
        'all_features': categorical_features + numerical_features,
        'performance': {
            'r2_score': r2,
            'rmse': np.sqrt(mse),
            'mae': mae
        },
        'training_info': {
            'dataset_size': len(df),
            'features_count': len(categorical_features) + len(numerical_features),
            'model_type': 'RandomForest'
        }
    }
    
    with open('Fixed_Enhanced_Model.pkl', 'wb') as f:
        pickle.dump(model_data, f)
    
    print(f"\nFixed model saved as: Fixed_Enhanced_Model.pkl")
    
    return model_data

if __name__ == "__main__":
    fixed_model = fix_model_training()
