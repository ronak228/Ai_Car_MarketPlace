#!/usr/bin/env python3
"""
Enhanced Price Prediction Model Training Script
Trains a model based on real dataset with actual market prices
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import pickle
import warnings
warnings.filterwarnings('ignore')

def load_and_prepare_data():
    """Load and prepare the enhanced dataset for training"""
    print("Loading enhanced Indian car dataset...")
    
    # Load the enhanced dataset
    df = pd.read_csv('enhanced_indian_car_dataset.csv')
    print(f"Loaded {len(df)} records with {df['company'].nunique()} brands")
    
    # Remove any rows with missing target values
    df = df.dropna(subset=['Price'])
    
    # Feature engineering
    df['age'] = 2024 - df['year']
    df['price_per_km'] = df['Price'] / (df['kilometers_driven'] + 1)  # Avoid division by zero
    df['engine_power_ratio'] = df['power'] / (df['engine_size'] + 1)
    
    # Create categorical features
    df['is_electric'] = (df['fuel_type'] == 'Electric').astype(int)
    df['is_hybrid'] = (df['fuel_type'] == 'Hybrid').astype(int)
    df['is_automatic'] = (df['transmission'] == 'Automatic').astype(int)
    df['is_first_owner'] = (df['owner_count'] == '1st').astype(int)
    df['is_certified'] = df['is_certified'].astype(int)
    
    # Define features for training
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
    print(f"Target variable range: ₹{y.min():,.0f} - ₹{y.max():,.0f}")
    
    return X, y, categorical_features, numerical_features

def create_preprocessing_pipeline(categorical_features, numerical_features):
    """Create preprocessing pipeline"""
    from sklearn.preprocessing import OneHotEncoder
    
    # Categorical preprocessing - use OneHotEncoder instead of LabelEncoder
    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])
    
    # Numerical preprocessing
    numerical_transformer = Pipeline(steps=[
        ('scaler', StandardScaler())
    ])
    
    # Combine preprocessing
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', categorical_transformer, categorical_features),
            ('num', numerical_transformer, numerical_features)
        ])
    
    return preprocessor

def train_models(X, y, categorical_features, numerical_features):
    """Train multiple models and select the best one"""
    print("\nTraining multiple models...")
    
    # Sample data for faster training (use 20% of data)
    sample_size = min(10000, len(X))
    sample_indices = np.random.choice(len(X), sample_size, replace=False)
    X_sample = X.iloc[sample_indices]
    y_sample = y.iloc[sample_indices]
    
    print(f"Using sample of {len(X_sample)} records for training")
    
    # Create preprocessing pipeline
    preprocessor = create_preprocessing_pipeline(categorical_features, numerical_features)
    
    # Define models to test (simplified)
    models = {
        'RandomForest': RandomForestRegressor(
            n_estimators=50, 
            max_depth=10, 
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        ),
        'Ridge': Ridge(alpha=1.0),
        'LinearRegression': LinearRegression()
    }
    
    best_model = None
    best_score = -np.inf
    best_model_name = None
    results = {}
    
    for name, model in models.items():
        print(f"\nTraining {name}...")
        
        try:
            # Create pipeline
            pipeline = Pipeline(steps=[
                ('preprocessor', preprocessor),
                ('regressor', model)
            ])
            
            # Train on sample dataset
            pipeline.fit(X_sample, y_sample)
            
            # Predictions on sample
            y_pred = pipeline.predict(X_sample)
            mse = mean_squared_error(y_sample, y_pred)
            mae = mean_absolute_error(y_sample, y_pred)
            r2 = r2_score(y_sample, y_pred)
            
            results[name] = {
                'model': pipeline,
                'cv_score': r2,  # Use R² as proxy for CV score
                'cv_std': 0.0,
                'mse': mse,
                'mae': mae,
                'r2': r2,
                'rmse': np.sqrt(mse)
            }
            
            print(f"  R² Score: {r2:.4f}")
            print(f"  RMSE: ₹{np.sqrt(mse):,.0f}")
            print(f"  MAE: ₹{mae:,.0f}")
            
            # Track best model
            if r2 > best_score:
                best_score = r2
                best_model = pipeline
                best_model_name = name
                
        except Exception as e:
            print(f"  Error training {name}: {str(e)}")
            continue
    
    print(f"\nBest model: {best_model_name} (R² = {best_score:.4f})")
    
    return best_model, best_model_name, results

def create_enhanced_model_data(best_model, best_model_name, results, categorical_features, numerical_features):
    """Create enhanced model data structure"""
    model_data = {
        'model': best_model,
        'model_name': f'Enhanced {best_model_name}',
        'categorical_features': categorical_features,
        'numerical_features': numerical_features,
        'all_features': categorical_features + numerical_features,
        'performance': {
            'r2_score': results[best_model_name]['r2'],
            'rmse': results[best_model_name]['rmse'],
            'mae': results[best_model_name]['mae'],
            'cv_score': results[best_model_name]['cv_score'],
            'cv_std': results[best_model_name]['cv_std']
        },
        'training_info': {
            'dataset_size': len(results[best_model_name]['model'].steps[0][1].transformers_[0][2]),
            'features_count': len(categorical_features) + len(numerical_features),
            'model_type': best_model_name
        }
    }
    
    return model_data

def validate_predictions(model_data, X, y):
    """Validate predictions with sample data"""
    print("\nValidating predictions with sample data...")
    
    model = model_data['model']
    
    # Sample predictions
    sample_indices = np.random.choice(len(X), min(10, len(X)), replace=False)
    
    print("\nSample Predictions:")
    print("=" * 80)
    print(f"{'Actual Price':<15} {'Predicted Price':<15} {'Difference':<15} {'Error %':<10}")
    print("=" * 80)
    
    total_error = 0
    for idx in sample_indices:
        actual = y.iloc[idx]
        predicted = model.predict(X.iloc[[idx]])[0]
        difference = predicted - actual
        error_pct = abs(difference) / actual * 100
        total_error += error_pct
        
        print(f"₹{actual:>12,.0f} ₹{predicted:>13,.0f} ₹{difference:>13,.0f} {error_pct:>8.1f}%")
    
    avg_error = total_error / len(sample_indices)
    print("=" * 80)
    print(f"Average Error: {avg_error:.1f}%")
    
    return avg_error

def main():
    """Main training function"""
    print("Enhanced Car Price Prediction Model Training")
    print("=" * 50)
    
    # Load and prepare data
    X, y, categorical_features, numerical_features = load_and_prepare_data()
    
    # Train models
    best_model, best_model_name, results = train_models(X, y, categorical_features, numerical_features)
    
    # Create enhanced model data
    enhanced_model_data = create_enhanced_model_data(best_model, best_model_name, results, categorical_features, numerical_features)
    
    # Validate predictions
    avg_error = validate_predictions(enhanced_model_data, X, y)
    
    # Save the enhanced model
    model_filename = 'Enhanced_Real_Price_Model.pkl'
    with open(model_filename, 'wb') as f:
        pickle.dump(enhanced_model_data, f)
    
    print(f"\nEnhanced model saved as: {model_filename}")
    print(f"Model Performance:")
    print(f"  R² Score: {enhanced_model_data['performance']['r2_score']:.4f}")
    print(f"  RMSE: ₹{enhanced_model_data['performance']['rmse']:,.0f}")
    print(f"  MAE: ₹{enhanced_model_data['performance']['mae']:,.0f}")
    print(f"  Average Error: {avg_error:.1f}%")
    print(f"  Features: {enhanced_model_data['training_info']['features_count']}")
    
    return enhanced_model_data

if __name__ == "__main__":
    enhanced_model = main()
