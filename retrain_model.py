import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import pickle
import warnings
warnings.filterwarnings('ignore')

def analyze_datasets():
    """Analyze both datasets to understand their structure"""
    print("=== DATASET ANALYSIS ===")
    
    # Load original dataset
    print("\n1. Original Dataset (Cleaned_Car_data.csv):")
    df_original = pd.read_csv('Cleaned_Car_data.csv')
    print(f"   Shape: {df_original.shape}")
    print(f"   Columns: {list(df_original.columns)}")
    print(f"   Sample data:")
    print(df_original.head(2))
    
    # Load synthetic dataset
    print("\n2. Synthetic Dataset (generated_5000_strict.csv):")
    df_synthetic = pd.read_csv('generated_5000_strict.csv')
    print(f"   Shape: {df_synthetic.shape}")
    print(f"   Columns: {list(df_synthetic.columns)}")
    print(f"   Sample data:")
    print(df_synthetic.head(2))
    
    return df_original, df_synthetic

def preprocess_original_data(df):
    """Preprocess the original dataset to match synthetic dataset structure"""
    print("\n=== PREPROCESSING ORIGINAL DATASET ===")
    
    # Drop unnamed index column if exists
    if 'Unnamed: 0' in df.columns:
        df = df.drop('Unnamed: 0', axis=1)
    
    # Rename columns to match synthetic dataset
    df_processed = df.copy()
    df_processed = df_processed.rename(columns={
        'name': 'model',
        'Price': 'price'
    })
    
    # Add missing columns with default values
    df_processed['car_id'] = range(len(df_processed))
    df_processed['transmission'] = 'Manual'  # Default value
    df_processed['owner'] = '1st'  # Default value
    df_processed['car_condition'] = 'Good'  # Default value
    df_processed['insurance_status'] = 'Yes'  # Default value
    df_processed['previous_accidents'] = 0  # Default value
    df_processed['num_doors'] = 4  # Default value
    df_processed['engine_size'] = 1500  # Default value
    df_processed['power'] = 100  # Default value
    df_processed['city'] = 'Mumbai'  # Default value
    df_processed['emission_norm'] = 'BS-IV'  # Default value
    df_processed['insurance_eligible'] = 'Yes'  # Default value
    df_processed['maintenance_level'] = 'Medium'  # Default value
    df_processed['predicted_price'] = df_processed['price']  # Copy price as predicted
    df_processed['listing_type'] = 'Individual'  # Default value
    df_processed['is_certified'] = 'No'  # Default value
    
    # Rename price column to match synthetic dataset
    df_processed = df_processed.rename(columns={'price': 'Price'})
    
    print(f"   Processed shape: {df_processed.shape}")
    print(f"   Columns: {list(df_processed.columns)}")
    
    return df_processed

def preprocess_synthetic_data(df):
    """Preprocess the synthetic dataset"""
    print("\n=== PREPROCESSING SYNTHETIC DATASET ===")
    
    df_processed = df.copy()
    
    # Rename model column to match original
    df_processed = df_processed.rename(columns={'model': 'model'})
    
    print(f"   Processed shape: {df_processed.shape}")
    print(f"   Columns: {list(df_processed.columns)}")
    
    return df_processed

def combine_datasets(df_original, df_synthetic, option='A'):
    """Combine datasets based on user choice"""
    print(f"\n=== COMBINING DATASETS (Option {option}) ===")
    
    if option == 'A':
        # Concatenate both datasets
        combined_df = pd.concat([df_original, df_synthetic], ignore_index=True)
        print(f"   Combined dataset shape: {combined_df.shape}")
        print(f"   Total rows: {len(combined_df)}")
    elif option == 'B':
        # Use only synthetic dataset
        combined_df = df_synthetic.copy()
        print(f"   Using only synthetic dataset shape: {combined_df.shape}")
        print(f"   Total rows: {len(combined_df)}")
    
    return combined_df

def prepare_features(df):
    """Prepare features for ML model"""
    print("\n=== PREPARING FEATURES ===")
    
    # Select relevant features for prediction
    feature_columns = ['company', 'model', 'year', 'kms_driven', 'fuel_type']
    target_column = 'Price'
    
    # Check if all required columns exist
    missing_cols = [col for col in feature_columns if col not in df.columns]
    if missing_cols:
        print(f"   Warning: Missing columns: {missing_cols}")
        return None, None
    
    # Prepare features and target
    X = df[feature_columns].copy()
    y = df[target_column].copy()
    
    print(f"   Feature columns: {feature_columns}")
    print(f"   Target column: {target_column}")
    print(f"   Features shape: {X.shape}")
    print(f"   Target shape: {y.shape}")
    
    # Handle missing values
    print(f"   Missing values in features: {X.isnull().sum().sum()}")
    print(f"   Missing values in target: {y.isnull().sum()}")
    
    # Fill missing values
    X = X.fillna(X.mode().iloc[0] if not X.empty else 'Unknown')
    y = y.fillna(y.median())
    
    return X, y

def encode_features(X):
    """Encode categorical features"""
    print("\n=== ENCODING CATEGORICAL FEATURES ===")
    
    # Create label encoders
    le_company = LabelEncoder()
    le_model = LabelEncoder()
    le_fuel = LabelEncoder()
    
    # Encode categorical variables
    X_encoded = X.copy()
    X_encoded['company_encoded'] = le_company.fit_transform(X['company'])
    X_encoded['model_encoded'] = le_model.fit_transform(X['model'])
    X_encoded['fuel_encoded'] = le_fuel.fit_transform(X['fuel_type'])
    
    # Select encoded features
    feature_columns_encoded = ['company_encoded', 'model_encoded', 'year', 'kms_driven', 'fuel_encoded']
    X_final = X_encoded[feature_columns_encoded]
    
    print(f"   Encoded features: {feature_columns_encoded}")
    print(f"   Final features shape: {X_final.shape}")
    
    return X_final, le_company, le_model, le_fuel

def train_models(X, y):
    """Train multiple ML models"""
    print("\n=== TRAINING MODELS ===")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    models = {
        'Linear Regression': LinearRegression(),
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42)
    }
    
    results = {}
    
    for name, model in models.items():
        print(f"\n   Training {name}...")
        
        # Train model
        model.fit(X_train, y_train)
        
        # Make predictions
        y_pred = model.predict(X_test)
        
        # Calculate metrics
        r2 = r2_score(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        mae = mean_absolute_error(y_test, y_pred)
        
        results[name] = {
            'model': model,
            'r2': r2,
            'rmse': rmse,
            'mae': mae,
            'y_test': y_test,
            'y_pred': y_pred
        }
        
        print(f"   R² Score: {r2:.4f}")
        print(f"   RMSE: {rmse:.2f}")
        print(f"   MAE: {mae:.2f}")
    
    return results, X_train, X_test, y_train, y_test

def show_feature_importance(results, feature_names):
    """Show feature importance for tree-based models"""
    print("\n=== FEATURE IMPORTANCE ===")
    
    for name, result in results.items():
        if hasattr(result['model'], 'feature_importances_'):
            print(f"\n{name} Feature Importance:")
            importance_df = pd.DataFrame({
                'feature': feature_names,
                'importance': result['model'].feature_importances_
            }).sort_values('importance', ascending=False)
            
            for _, row in importance_df.iterrows():
                print(f"   {row['feature']}: {row['importance']:.4f}")

def save_best_model(results, le_company, le_model, le_fuel):
    """Save the best performing model"""
    print("\n=== SAVING BEST MODEL ===")
    
    # Find best model based on R² score
    best_model_name = max(results.keys(), key=lambda k: results[k]['r2'])
    best_model = results[best_model_name]['model']
    
    print(f"   Best model: {best_model_name}")
    print(f"   R² Score: {results[best_model_name]['r2']:.4f}")
    
    # Save model and encoders
    model_data = {
        'model': best_model,
        'le_company': le_company,
        'le_model': le_model,
        'le_fuel': le_fuel,
        'model_name': best_model_name,
        'performance': results[best_model_name]
    }
    
    with open('Updated_Car_Price_Model.pkl', 'wb') as f:
        pickle.dump(model_data, f)
    
    print("   Model saved as 'Updated_Car_Price_Model.pkl'")

def main():
    """Main function to run the complete pipeline"""
    print("🚗 CAR PRICE PREDICTION MODEL RETRAINING")
    print("=" * 50)
    
    # Step 1: Analyze datasets
    df_original, df_synthetic = analyze_datasets()
    
    # Step 2: Preprocess datasets
    df_original_processed = preprocess_original_data(df_original)
    df_synthetic_processed = preprocess_synthetic_data(df_synthetic)
    
    # Step 3: Ask user for combination option
    print("\n" + "=" * 50)
    print("COMBINATION OPTIONS:")
    print("Option A: Concatenate both datasets (Original + Synthetic)")
    print(f"   - Original: {len(df_original_processed)} rows")
    print(f"   - Synthetic: {len(df_synthetic_processed)} rows")
    print(f"   - Total: {len(df_original_processed) + len(df_synthetic_processed)} rows")
    print("\nOption B: Use only synthetic dataset")
    print(f"   - Synthetic: {len(df_synthetic_processed)} rows")
    print("=" * 50)
    
    # For now, let's use Option A (can be changed by user)
    option = 'A'  # User can change this
    print(f"\nUsing Option {option} (can be changed in the script)")
    
    # Step 4: Combine datasets
    combined_df = combine_datasets(df_original_processed, df_synthetic_processed, option)
    
    # Step 5: Prepare features
    X, y = prepare_features(combined_df)
    if X is None:
        print("Error: Could not prepare features")
        return
    
    # Step 6: Encode features
    X_encoded, le_company, le_model, le_fuel = encode_features(X)
    
    # Step 7: Train models
    results, X_train, X_test, y_train, y_test = train_models(X_encoded, y)
    
    # Step 8: Show feature importance
    feature_names = ['company', 'model', 'year', 'kms_driven', 'fuel_type']
    show_feature_importance(results, feature_names)
    
    # Step 9: Save best model
    save_best_model(results, le_company, le_model, le_fuel)
    
    print("\n" + "=" * 50)
    print("✅ MODEL RETRAINING COMPLETED!")
    print("=" * 50)

if __name__ == "__main__":
    main()
