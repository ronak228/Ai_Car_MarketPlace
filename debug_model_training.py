#!/usr/bin/env python3
"""
Debug the model training to identify the issue
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

def debug_model_training():
    """Debug the model training process"""
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
    
    # Check BMW X5 2024 in training data
    bmw_2024 = df[(df['company'] == 'BMW') & (df['model'] == 'X5') & (df['year'] == 2024)]
    print(f"\nBMW X5 2024 in dataset: {len(bmw_2024)}")
    if len(bmw_2024) > 0:
        print(f"Price range: ₹{bmw_2024['Price'].min():,.0f} - ₹{bmw_2024['Price'].max():,.0f}")
        print(f"Average price: ₹{bmw_2024['Price'].mean():,.0f}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print(f"\nTraining set: {len(X_train)} samples")
    print(f"Test set: {len(X_test)} samples")
    
    # Check BMW X5 2024 in training set
    bmw_2024_train = X_train[(X_train['company'] == 'BMW') & (X_train['model'] == 'X5') & (X_train['year'] == 2024)]
    print(f"BMW X5 2024 in training set: {len(bmw_2024_train)}")
    
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
    
    print("\nTraining model...")
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
    
    # Test on BMW X5 2024 sample
    if len(bmw_2024) > 0:
        sample = bmw_2024.iloc[0]
        sample_input = X.iloc[[sample.name]]
        sample_prediction = model.predict(sample_input)[0]
        sample_actual = sample['Price']
        
        print(f"\nBMW X5 2024 Test:")
        print(f"Actual Price: ₹{sample_actual:,.0f}")
        print(f"Predicted Price: ₹{sample_prediction:,.0f}")
        print(f"Error: ₹{abs(sample_prediction - sample_actual):,.0f}")
        print(f"Error %: {abs(sample_prediction - sample_actual) / sample_actual * 100:.1f}%")
        
        # Test with our test case
        test_case = {
            'company': 'BMW', 'model': 'X5', 'year': 2024, 'kilometers_driven': 1000,
            'fuel_type': 'Diesel', 'transmission': 'Automatic', 'owner_count': '1st',
            'car_condition': 'Excellent', 'city': 'Delhi', 'emission_norm': 'BS6',
            'maintenance_level': 'High', 'insurance_eligible': 'Yes', 'listing_type': 'Dealer',
            'engine_size': 3000, 'power': 265, 'num_doors': 5, 'previous_accidents': 0,
            'age': 0, 'price_per_km': 0.0, 'engine_power_ratio': 265/3001,
            'is_electric': 0, 'is_hybrid': 0, 'is_automatic': 1, 'is_first_owner': 1, 'is_certified': 0
        }
        
        test_df = pd.DataFrame([test_case])
        test_prediction = model.predict(test_df)[0]
        
        print(f"\nTest Case Prediction:")
        print(f"Predicted Price: ₹{test_prediction:,.0f}")
        print(f"Expected Range: ₹3,000,000 - ₹6,000,000")
        print(f"Prediction is {'REALISTIC' if 3000000 <= test_prediction <= 6000000 else 'UNREALISTIC'}")
    
    # Save the debug model
    model_data = {
        'model': model,
        'model_name': 'Debug Enhanced RandomForest',
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
    
    with open('Debug_Enhanced_Model.pkl', 'wb') as f:
        pickle.dump(model_data, f)
    
    print(f"\nDebug model saved as: Debug_Enhanced_Model.pkl")
    
    return model_data

if __name__ == "__main__":
    debug_model = debug_model_training()
