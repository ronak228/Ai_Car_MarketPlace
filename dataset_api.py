from flask import Flask, render_template, jsonify
import pandas as pd
import json

app = Flask(__name__)

def get_dataset_info():
    """Fetch and return dataset information"""
    try:
        # Load both datasets
        df_original = pd.read_csv('Cleaned_Car_data_master.csv')
        df_synthetic = pd.read_csv('generated_5000_strict.csv')
        
        # Combine datasets
        df_combined = pd.concat([df_original, df_synthetic], ignore_index=True)
        
        # Calculate statistics
        dataset_info = {
            'totalRecords': len(df_combined),
            'totalCompanies': df_combined['company'].nunique(),
            'totalModels': df_combined['model'].nunique(),
            'citiesAvailable': df_combined['city'].nunique(),
            'priceRange': {
                'min': int(df_combined['Price'].min()),
                'max': int(df_combined['Price'].max()),
                'mean': int(df_combined['Price'].mean()),
                'median': int(df_combined['Price'].median())
            },
            'yearRange': {
                'min': int(df_combined['year'].min()),
                'max': int(df_combined['year'].max())
            },
            'kmsDrivenRange': {
                'min': int(df_combined['kms_driven'].min()),
                'max': int(df_combined['kms_driven'].max()),
                'mean': int(df_combined['kms_driven'].mean())
            },
            'fuelTypes': df_combined['fuel_type'].value_counts().to_dict(),
            'transmissionTypes': df_combined['transmission'].value_counts().to_dict(),
            'topCompanies': df_combined['company'].value_counts().head(10).to_dict(),
            'topModels': df_combined['model'].value_counts().head(10).to_dict(),
            'cities': df_combined['city'].value_counts().to_dict()
        }
        
        return dataset_info
        
    except Exception as e:
        print(f"Error loading dataset: {str(e)}")
        return None

@app.route('/')
def index():
    """Serve the main dashboard page"""
    return render_template('dataset_dashboard.html')

@app.route('/api/dataset-info')
def api_dataset_info():
    """API endpoint to get dataset information"""
    dataset_info = get_dataset_info()
    
    if dataset_info is None:
        return jsonify({'error': 'Failed to load dataset information'}), 500
    
    return jsonify(dataset_info)

@app.route('/dashboard')
def dashboard():
    """Direct route to dashboard"""
    return render_template('dataset_dashboard.html')

if __name__ == '__main__':
    print("Starting Flask server...")
    print("Dashboard available at: http://localhost:5000/dashboard")
    print("API endpoint: http://localhost:5000/api/dataset-info")
    app.run(debug=True, host='0.0.0.0', port=5000)
