import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import pickle
import warnings
warnings.filterwarnings('ignore')

print("=" * 60)
print("CAR PRICE PREDICTION MODEL - DATASET COMBINATION & TRAINING")
print("=" * 60)

# Step 1: Load both CSV files
print("\n1. Loading CSV files...")
df_original = pd.read_csv('Cleaned_Car_data_master.csv')
df_synthetic = pd.read_csv('generated_5000_strict.csv')

print(f"   Original dataset shape: {df_original.shape}")
print(f"   Synthetic dataset shape: {df_synthetic.shape}")

# Step 2: Concatenate datasets (Option A)
print("\n2. Concatenating datasets...")
df_combined = pd.concat([df_original, df_synthetic], ignore_index=True)
print(f"   Combined dataset shape: {df_combined.shape}")
print(f"   Total rows: {len(df_combined)}")

# Step 3: Data preprocessing
print("\n3. Preprocessing data...")

# Check for missing values
print(f"   Missing values check:")
missing_values = df_combined.isnull().sum()
if missing_values.sum() == 0:
    print("   ✅ No missing values found")
else:
    print("   ⚠️ Missing values found:")
    print(missing_values[missing_values > 0])

# Identify categorical and numerical columns
categorical_columns = df_combined.select_dtypes(include=['object']).columns.tolist()
numerical_columns = df_combined.select_dtypes(include=['int64', 'float64']).columns.tolist()

print(f"   Categorical columns: {categorical_columns}")
print(f"   Numerical columns: {numerical_columns}")

# Remove non-feature columns for modeling
feature_columns_to_remove = ['car_id', 'predicted_price']  # These are not features for prediction
target_column = 'Price'

# Prepare features and target
X = df_combined.drop(columns=feature_columns_to_remove + [target_column])
y = df_combined[target_column]

print(f"   Features shape: {X.shape}")
print(f"   Target shape: {y.shape}")

# Identify categorical features for encoding
categorical_features = X.select_dtypes(include=['object']).columns.tolist()
numerical_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()

print(f"   Categorical features for encoding: {categorical_features}")
print(f"   Numerical features: {numerical_features}")

# Step 4: Train-test split
print("\n4. Splitting data into train and test sets...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"   Training set shape: {X_train.shape}")
print(f"   Test set shape: {X_test.shape}")

# Step 5: Create preprocessing pipeline
print("\n5. Creating preprocessing pipeline...")

# Create OneHotEncoder for categorical features
ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=False)

# Create column transformer
column_transformer = make_column_transformer(
    (ohe, categorical_features),
    remainder='passthrough'
)

# Step 6: Train LinearRegression model (same as used before)
print("\n6. Training LinearRegression model...")

# Create pipeline with preprocessing and model
lr_model = LinearRegression()
pipeline = make_pipeline(column_transformer, lr_model)

# Fit the model
pipeline.fit(X_train, y_train)
print("   ✅ Model training completed")

# Step 7: Make predictions
print("\n7. Making predictions...")
y_pred_train = pipeline.predict(X_train)
y_pred_test = pipeline.predict(X_test)

# Step 8: Evaluate performance
print("\n8. Model Performance Evaluation:")
print("=" * 40)

# Training set metrics
train_r2 = r2_score(y_train, y_pred_train)
train_rmse = np.sqrt(mean_squared_error(y_train, y_pred_train))
train_mae = mean_absolute_error(y_train, y_pred_train)

# Test set metrics
test_r2 = r2_score(y_test, y_pred_test)
test_rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
test_mae = mean_absolute_error(y_test, y_pred_test)

print(f"TRAINING SET METRICS:")
print(f"  R² Score: {train_r2:.4f}")
print(f"  RMSE: {train_rmse:.2f}")
print(f"  MAE: {train_mae:.2f}")

print(f"\nTEST SET METRICS:")
print(f"  R² Score: {test_r2:.4f}")
print(f"  RMSE: {test_rmse:.2f}")
print(f"  MAE: {test_mae:.2f}")

# Step 9: Feature importance (for LinearRegression, we can show coefficients)
print("\n9. Feature Analysis:")
print("=" * 40)

# Get feature names after one-hot encoding
feature_names = []
for i, feature in enumerate(categorical_features):
    categories = pipeline.named_steps['columntransformer'].named_transformers_['onehotencoder'].categories_[i]
    for category in categories:
        feature_names.append(f"{feature}_{category}")

# Add numerical feature names
feature_names.extend(numerical_features)

# Get coefficients
coefficients = pipeline.named_steps['linearregression'].coef_

# Create feature importance dataframe
feature_importance_df = pd.DataFrame({
    'feature': feature_names,
    'coefficient': coefficients
})

# Sort by absolute coefficient value
feature_importance_df['abs_coefficient'] = np.abs(feature_importance_df['coefficient'])
feature_importance_df = feature_importance_df.sort_values('abs_coefficient', ascending=False)

print("Top 15 Most Important Features (by coefficient magnitude):")
print("-" * 50)
for i, row in feature_importance_df.head(15).iterrows():
    print(f"{row['feature']:<30} {row['coefficient']:>10.2f}")

# Step 10: Save the trained model
print("\n10. Saving the trained model...")
model_data = {
    'model': pipeline,
    'feature_names': feature_names,
    'categorical_features': categorical_features,
    'numerical_features': numerical_features,
    'target_column': target_column
}

with open('CombinedDatasetModel.pkl', 'wb') as f:
    pickle.dump(model_data, f)
print("   ✅ Model saved as 'CombinedDatasetModel.pkl'")

# Step 11: Summary
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"✅ Successfully combined datasets: {len(df_combined)} total rows")
print(f"✅ Trained LinearRegression model on combined dataset")
print(f"✅ Test R² Score: {test_r2:.4f}")
print(f"✅ Test RMSE: {test_rmse:.2f}")
print(f"✅ Test MAE: {test_mae:.2f}")
print(f"✅ Model saved for future use")

# Additional analysis
print(f"\nDataset Statistics:")
print(f"  Price range: ₹{y.min():,.0f} - ₹{y.max():,.0f}")
print(f"  Average price: ₹{y.mean():,.0f}")
print(f"  Median price: ₹{y.median():,.0f}")

print("\n" + "=" * 60)
print("ANALYSIS COMPLETE!")
print("=" * 60)
