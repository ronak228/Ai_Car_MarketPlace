import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import pickle
import warnings
warnings.filterwarnings('ignore')

print("=" * 70)
print("CAR PRICE PREDICTION - MODEL COMPARISON & IMPROVEMENT ANALYSIS")
print("=" * 70)

# Load the combined dataset
print("\n1. Loading combined dataset...")
df_combined = pd.read_csv('Cleaned_Car_data_master.csv')
df_synthetic = pd.read_csv('generated_5000_strict.csv')
df_combined = pd.concat([df_combined, df_synthetic], ignore_index=True)

print(f"   Combined dataset shape: {df_combined.shape}")

# Prepare data
feature_columns_to_remove = ['car_id', 'predicted_price']
target_column = 'Price'

X = df_combined.drop(columns=feature_columns_to_remove + [target_column])
y = df_combined[target_column]

categorical_features = X.select_dtypes(include=['object']).columns.tolist()
numerical_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()

print(f"   Features: {X.shape[1]} (Categorical: {len(categorical_features)}, Numerical: {len(numerical_features)})")

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"\n2. Training multiple models for comparison...")

# Model 1: LinearRegression (original approach)
print("\n   Model 1: LinearRegression")
lr_ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
lr_transformer = make_column_transformer((lr_ohe, categorical_features), remainder='passthrough')
lr_model = LinearRegression()
lr_pipeline = make_pipeline(lr_transformer, lr_model)
lr_pipeline.fit(X_train, y_train)

lr_train_pred = lr_pipeline.predict(X_train)
lr_test_pred = lr_pipeline.predict(X_test)

lr_train_r2 = r2_score(y_train, lr_train_pred)
lr_test_r2 = r2_score(y_test, lr_test_pred)
lr_train_rmse = np.sqrt(mean_squared_error(y_train, lr_train_pred))
lr_test_rmse = np.sqrt(mean_squared_error(y_test, lr_test_pred))
lr_train_mae = mean_absolute_error(y_train, lr_train_pred)
lr_test_mae = mean_absolute_error(y_test, lr_test_pred)

print(f"      Train R²: {lr_train_r2:.4f}, RMSE: {lr_train_rmse:.0f}, MAE: {lr_train_mae:.0f}")
print(f"      Test R²:  {lr_test_r2:.4f}, RMSE: {lr_test_rmse:.0f}, MAE: {lr_test_mae:.0f}")

# Model 2: RandomForestRegressor (better for this type of data)
print("\n   Model 2: RandomForestRegressor")
rf_ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
rf_transformer = make_column_transformer((rf_ohe, categorical_features), remainder='passthrough')
rf_model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
rf_pipeline = make_pipeline(rf_transformer, rf_model)
rf_pipeline.fit(X_train, y_train)

rf_train_pred = rf_pipeline.predict(X_train)
rf_test_pred = rf_pipeline.predict(X_test)

rf_train_r2 = r2_score(y_train, rf_train_pred)
rf_test_r2 = r2_score(y_test, rf_test_pred)
rf_train_rmse = np.sqrt(mean_squared_error(y_train, rf_train_pred))
rf_test_rmse = np.sqrt(mean_squared_error(y_test, rf_test_pred))
rf_train_mae = mean_absolute_error(y_train, rf_train_pred)
rf_test_mae = mean_absolute_error(y_test, rf_test_pred)

print(f"      Train R²: {rf_train_r2:.4f}, RMSE: {rf_train_rmse:.0f}, MAE: {rf_train_mae:.0f}")
print(f"      Test R²:  {rf_test_r2:.4f}, RMSE: {rf_test_rmse:.0f}, MAE: {rf_test_mae:.0f}")

# Model 3: LinearRegression with scaled features
print("\n   Model 3: LinearRegression with StandardScaler")
lr_scaled_ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
lr_scaled_transformer = make_column_transformer(
    (lr_scaled_ohe, categorical_features),
    (StandardScaler(), numerical_features)
)
lr_scaled_model = LinearRegression()
lr_scaled_pipeline = make_pipeline(lr_scaled_transformer, lr_scaled_model)
lr_scaled_pipeline.fit(X_train, y_train)

lr_scaled_train_pred = lr_scaled_pipeline.predict(X_train)
lr_scaled_test_pred = lr_scaled_pipeline.predict(X_test)

lr_scaled_train_r2 = r2_score(y_train, lr_scaled_train_pred)
lr_scaled_test_r2 = r2_score(y_test, lr_scaled_test_pred)
lr_scaled_train_rmse = np.sqrt(mean_squared_error(y_train, lr_scaled_train_pred))
lr_scaled_test_rmse = np.sqrt(mean_squared_error(y_test, lr_scaled_test_pred))
lr_scaled_train_mae = mean_absolute_error(y_train, lr_scaled_train_pred)
lr_scaled_test_mae = mean_absolute_error(y_test, lr_scaled_test_pred)

print(f"      Train R²: {lr_scaled_train_r2:.4f}, RMSE: {lr_scaled_train_rmse:.0f}, MAE: {lr_scaled_train_mae:.0f}")
print(f"      Test R²:  {lr_scaled_test_r2:.4f}, RMSE: {lr_scaled_test_rmse:.0f}, MAE: {lr_scaled_test_mae:.0f}")

# Performance comparison
print("\n" + "=" * 70)
print("MODEL PERFORMANCE COMPARISON")
print("=" * 70)

models = [
    ("LinearRegression", lr_test_r2, lr_test_rmse, lr_test_mae),
    ("RandomForest", rf_test_r2, rf_test_rmse, rf_test_mae),
    ("LinearRegression + Scaler", lr_scaled_test_r2, lr_scaled_test_rmse, lr_scaled_test_mae)
]

print(f"{'Model':<25} {'R² Score':<10} {'RMSE':<12} {'MAE':<12}")
print("-" * 60)
for name, r2, rmse, mae in models:
    print(f"{name:<25} {r2:<10.4f} {rmse:<12.0f} {mae:<12.0f}")

# Find best model
best_model_idx = np.argmax([r2 for _, r2, _, _ in models])
best_model_name, best_r2, best_rmse, best_mae = models[best_model_idx]

print(f"\n🏆 BEST MODEL: {best_model_name}")
print(f"   R² Score: {best_r2:.4f}")
print(f"   RMSE: {best_rmse:.0f}")
print(f"   MAE: {best_mae:.0f}")

# Feature importance for RandomForest (if it's the best model)
if best_model_name == "RandomForest":
    print(f"\n4. Feature Importance Analysis (RandomForest):")
    print("=" * 50)
    
    # Get feature names after one-hot encoding
    feature_names = []
    for i, feature in enumerate(categorical_features):
        categories = rf_pipeline.named_steps['columntransformer'].named_transformers_['onehotencoder'].categories_[i]
        for category in categories:
            feature_names.append(f"{feature}_{category}")
    feature_names.extend(numerical_features)
    
    # Get feature importance
    importances = rf_pipeline.named_steps['randomforestregressor'].feature_importances_
    
    # Create importance dataframe
    importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance': importances
    }).sort_values('importance', ascending=False)
    
    print("Top 15 Most Important Features:")
    print("-" * 40)
    for i, row in importance_df.head(15).iterrows():
        print(f"{row['feature']:<35} {row['importance']:.4f}")

# Save the best model
print(f"\n5. Saving the best model...")
if best_model_name == "RandomForest":
    best_pipeline = rf_pipeline
elif best_model_name == "LinearRegression + Scaler":
    best_pipeline = lr_scaled_pipeline
else:
    best_pipeline = lr_pipeline

model_data = {
    'model': best_pipeline,
    'model_name': best_model_name,
    'categorical_features': categorical_features,
    'numerical_features': numerical_features,
    'target_column': target_column,
    'performance': {
        'r2_score': best_r2,
        'rmse': best_rmse,
        'mae': best_mae
    }
}

with open('BestCombinedModel.pkl', 'wb') as f:
    pickle.dump(model_data, f)
print(f"   ✅ Best model ({best_model_name}) saved as 'BestCombinedModel.pkl'")

# Data analysis
print(f"\n6. Dataset Analysis:")
print("=" * 30)
print(f"   Total samples: {len(df_combined):,}")
print(f"   Price range: ₹{y.min():,.0f} - ₹{y.max():,.0f}")
print(f"   Average price: ₹{y.mean():,.0f}")
print(f"   Median price: ₹{y.median():,.0f}")
print(f"   Price std: ₹{y.std():,.0f}")

# Check for potential data issues
print(f"\n7. Data Quality Check:")
print("=" * 30)
print(f"   Unique companies: {df_combined['company'].nunique()}")
print(f"   Unique models: {df_combined['model'].nunique()}")
print(f"   Year range: {df_combined['year'].min()} - {df_combined['year'].max()}")
print(f"   Kms driven range: {df_combined['kms_driven'].min():,} - {df_combined['kms_driven'].max():,}")

print("\n" + "=" * 70)
print("ANALYSIS COMPLETE!")
print("=" * 70)
