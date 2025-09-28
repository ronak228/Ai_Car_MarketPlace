from flask import Flask, render_template, request, redirect, jsonify, send_from_directory
from flask_cors import CORS, cross_origin
import pickle
import pandas as pd
import numpy as np
import os

app = Flask(__name__, static_folder='client/build/static', template_folder='client/build')
cors = CORS(app)

# Load the model and encoders
model_data = pickle.load(open('LinearRegressionModel.pkl', 'rb'))
model = model_data['model']
le_name = model_data['le_name']
le_company = model_data['le_company']
le_fuel = model_data['le_fuel']

car = pd.read_csv('Cleaned_Car_data.csv')

# API Routes
@app.route('/api/health')
def health_check():
    return jsonify({"status": "healthy", "message": "Car Price Predictor API is running"})

@app.route('/api/companies')
def get_companies():
    companies = sorted(car['company'].unique())
    return jsonify(companies)

@app.route('/api/models/<company>')
def get_models(company):
    company_models = car[car['company'] == company]['name'].unique()
    return jsonify(sorted(company_models))

@app.route('/api/years')
def get_years():
    years = sorted(car['year'].unique(), reverse=True)
    return jsonify([int(y) for y in years])

@app.route('/api/fuel-types')
def get_fuel_types():
    fuel_types = car['fuel_type'].unique().tolist()
    return jsonify(fuel_types)

@app.route('/api/dataset-info')
@cross_origin()
def get_dataset_info():
    info = {
        'total_companies': len(car['company'].unique()),
        'total_models': len(car['name'].unique()),
        'year_range': {
            'min': int(car['year'].min()),
            'max': int(car['year'].max())
        },
        'fuel_types': car['fuel_type'].unique().tolist()
    }
    return jsonify(info)

@app.route('/api/predict', methods=['POST'])
@cross_origin()
def predict():
    try:
        # Accept both JSON and form data for flexibility
        if request.is_json:
            data = request.get_json()
            company = data.get('company')
            car_model = data.get('car_models')
            year = data.get('year')
            fuel_type = data.get('fuel_type')
            driven = data.get('kilo_driven')
        else:
            company = request.form.get('company')
            car_model = request.form.get('car_models')
            year = request.form.get('year')
            fuel_type = request.form.get('fuel_type')
            driven = request.form.get('kilo_driven')

        # Validate input values
        if not all([company, car_model, year, fuel_type, driven]):
            return jsonify({"error": "All fields are required."}), 400

        # Convert year and driven to proper data types
        try:
            year = int(year)
            driven = int(driven)
        except ValueError:
            return jsonify({"error": "Year and kilometers must be valid numbers."}), 400

        # Validate that values exist in training data
        if company not in le_company.classes_:
            return jsonify({"error": f"Company '{company}' not found in training data."}), 400
        
        if car_model not in le_name.classes_:
            return jsonify({"error": f"Car model '{car_model}' not found in training data."}), 400
        
        if fuel_type not in le_fuel.classes_:
            return jsonify({"error": f"Fuel type '{fuel_type}' not found in training data."}), 400

        # Create DataFrame with input data
        input_data = pd.DataFrame({
            'name': [car_model],
            'company': [company], 
            'year': [year],
            'kms_driven': [driven],
            'fuel_type': [fuel_type]
        })

        # Encode categorical variables
        input_data['name_encoded'] = le_name.transform(input_data['name'])
        input_data['company_encoded'] = le_company.transform(input_data['company'])
        input_data['fuel_encoded'] = le_fuel.transform(input_data['fuel_type'])

        # Select only the encoded features
        input_encoded = input_data[['name_encoded', 'company_encoded', 'year', 'kms_driven', 'fuel_encoded']]

        prediction = model.predict(input_encoded)
        predicted_price = float(np.round(prediction[0], 2))
        
        print(f"Prediction: {predicted_price}")

        return jsonify({
            "prediction": predicted_price,
            "message": "Price prediction successful"
        })
    
    except Exception as e:
        print(f"Error in prediction: {str(e)}")
        return jsonify({"error": f"Unable to make prediction. {str(e)}"}), 500

# In-memory user store (for demonstration purposes)
users = {
    "admin@example.com": {
        "password": "password",
        "name": "Admin User"
    }
}

@app.route('/api/cars')
@cross_origin()
def get_cars():
    # In a real application, you would fetch this from a database.
    # Here, we'll use the unique cars from the dataset and add placeholder data.
    unique_cars = car.drop_duplicates(subset=['name', 'company', 'year'])
    
    car_list = []
    for i, row in enumerate(unique_cars.to_dict(orient='records')):
        car_list.append({
            'id': i + 1,
            'name': row['name'],
            'company': row['company'],
            'year': int(row['year']),
            'price': np.random.randint(50, 200),  # Placeholder price
            'image': f"https://source.unsplash.com/400x300/?car,{row['company']},{i}", # Placeholder image
            'available': np.random.choice([True, False]) # Placeholder availability
        })

    return jsonify(car_list)

# Legacy route for backward compatibility
@app.route('/predict', methods=['POST'])
@cross_origin()
def predict_legacy():
    try:
        company = request.form.get('company')
        car_model = request.form.get('car_models')
        year = request.form.get('year')
        fuel_type = request.form.get('fuel_type')
        driven = request.form.get('kilo_driven')

        # Validate input values
        if not all([company, car_model, year, fuel_type, driven]):
            return "Error: All fields are required.", 400

        # Convert year and driven to proper data types
        try:
            year = int(year)
            driven = int(driven)
        except ValueError:
            return "Error: Year and kilometers must be valid numbers.", 400

        # Validate that values exist in training data
        if company not in le_company.classes_:
            return f"Error: Company '{company}' not found in training data.", 400
        
        if car_model not in le_name.classes_:
            return f"Error: Car model '{car_model}' not found in training data.", 400
        
        if fuel_type not in le_fuel.classes_:
            return f"Error: Fuel type '{fuel_type}' not found in training data.", 400

        # Create DataFrame with input data
        input_data = pd.DataFrame({
            'name': [car_model],
            'company': [company], 
            'year': [year],
            'kms_driven': [driven],
            'fuel_type': [fuel_type]
        })

        # Encode categorical variables
        input_data['name_encoded'] = le_name.transform(input_data['name'])
        input_data['company_encoded'] = le_company.transform(input_data['company'])
        input_data['fuel_encoded'] = le_fuel.transform(input_data['fuel_type'])

        # Select only the encoded features
        input_encoded = input_data[['name_encoded', 'company_encoded', 'year', 'kms_driven', 'fuel_encoded']]

        prediction = model.predict(input_encoded)
        print(f"Prediction: {prediction[0]}")

        return str(np.round(prediction[0], 2))
    
    except Exception as e:
        print(f"Error in prediction: {str(e)}")
        return f"Error: Unable to make prediction. {str(e)}", 500

# React App Routes
@app.route('/')
def serve_react_app():
    return send_from_directory('client/build', 'index.html')

@app.route('/<path:path>')
def serve_react_routes(path):
    if os.path.exists(os.path.join('client/build', path)):
        return send_from_directory('client/build', path)
    else:
        return send_from_directory('client/build', 'index.html')

if __name__ == '__main__':
    print("🚗 Car Price Predictor - Unified Application")
    print("📊 ML Model: Loaded and ready")
    print("🌐 React App: Serving from client/build")
    print("🔗 API Endpoints:")
    print("   - GET  /api/health")
    print("   - GET  /api/companies")
    print("   - GET  /api/models/<company>")
    print("   - GET  /api/years")
    print("   - GET  /api/fuel-types")
    print("   - GET  /api/dataset-info")
    print("   - POST /api/predict")
    print("   - POST /predict (legacy)")
    print("🌍 Web App: http://localhost:5000")
    print("⚡ Starting server...")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 