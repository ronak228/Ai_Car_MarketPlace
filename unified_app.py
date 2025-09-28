from flask import Flask, render_template, request, redirect, jsonify, send_from_directory
from flask_cors import CORS, cross_origin
import pickle
import pandas as pd
import numpy as np
import os

app = Flask(__name__, static_folder='client/build/static', template_folder='client/build')
cors = CORS(app)

# Load the enhanced model and encoders
try:
    enhanced_model_data = pickle.load(open('EnhancedCarPriceModel.pkl', 'rb'))
    enhanced_model = enhanced_model_data['model']
    enhanced_scaler = enhanced_model_data['scaler']
    enhanced_label_encoders = enhanced_model_data['label_encoders']
    enhanced_feature_names = enhanced_model_data['feature_names']
    enhanced_categorical_columns = enhanced_model_data['categorical_columns']
    enhanced_numerical_features = enhanced_model_data['numerical_features']
    print("✅ Enhanced ML model loaded successfully")
    print(f"Model: {enhanced_model_data['best_model_name']}")
    print(f"Test R²: {enhanced_model_data['model_scores'][enhanced_model_data['best_model_name']]['test_r2']:.4f}")
except FileNotFoundError:
    print("⚠️ Enhanced model not found, using legacy model")
    enhanced_model = None

# Legacy model (for backward compatibility)
model_data = pickle.load(open('LinearRegressionModel.pkl', 'rb'))
model = model_data['model']
le_name = model_data['le_name']
le_company = model_data['le_company']
le_fuel = model_data['le_fuel']

# Load master dataset with all 22 fields
car = pd.read_csv('Cleaned_Car_data_master.csv')

# Get unique values for all categorical fields
companies = sorted(car['company'].unique().tolist())
models = sorted(car['model'].unique().tolist())
fuel_types = sorted(car['fuel_type'].unique().tolist())
transmission_types = sorted(car['transmission'].unique().tolist())
owner_types = sorted(car['owner'].unique().tolist())
condition_types = sorted(car['car_condition'].unique().tolist())
insurance_types = sorted(car['insurance_status'].unique().tolist())
cities = sorted(car['city'].unique().tolist())
emission_norms = sorted(car['emission_norm'].unique().tolist())
insurance_eligible_types = sorted(car['insurance_eligible'].unique().tolist())
maintenance_levels = sorted(car['maintenance_level'].unique().tolist())
listing_types = sorted(car['listing_type'].unique().tolist())
is_certified_types = sorted(car['is_certified'].unique().tolist())

# Get numerical ranges
year_range = {'min': int(car['year'].min()), 'max': int(car['year'].max())}
kms_range = {'min': int(car['kms_driven'].min()), 'max': int(car['kms_driven'].max())}
price_range = {'min': int(car['Price'].min()), 'max': int(car['Price'].max())}

# API Routes
@app.route('/api/health')
def health_check():
    return jsonify({"status": "healthy", "message": "Car Price Predictor API is running"})

@app.route('/api/companies')
def get_companies():
    return jsonify(companies)

@app.route('/api/models')
def get_all_models():
    return jsonify(models)

@app.route('/api/models/<company>')
def get_models_by_company(company):
    company_models = car[car['company'] == company]['model'].unique()
    return jsonify(sorted(company_models))

@app.route('/api/years')
def get_years():
    years = sorted(car['year'].unique(), reverse=True)
    return jsonify([int(y) for y in years])

@app.route('/api/fuel-types')
def get_fuel_types():
    return jsonify(fuel_types)

@app.route('/api/transmission-types')
def get_transmission_types():
    return jsonify(transmission_types)

@app.route('/api/owner-types')
def get_owner_types():
    return jsonify(owner_types)

@app.route('/api/condition-types')
def get_condition_types():
    return jsonify(condition_types)

@app.route('/api/insurance-types')
def get_insurance_types():
    return jsonify(insurance_types)

@app.route('/api/cities')
def get_cities():
    return jsonify(cities)

@app.route('/api/emission-norms')
def get_emission_norms():
    return jsonify(emission_norms)

@app.route('/api/insurance-eligible-types')
def get_insurance_eligible_types():
    return jsonify(insurance_eligible_types)

@app.route('/api/maintenance-levels')
def get_maintenance_levels():
    return jsonify(maintenance_levels)

@app.route('/api/listing-types')
def get_listing_types():
    return jsonify(listing_types)

@app.route('/api/certified-types')
def get_certified_types():
    return jsonify(is_certified_types)

@app.route('/api/dataset-info')
@cross_origin()
def get_dataset_info():
    info = {
        'total_companies': len(companies),
        'total_models': len(models),
        'total_records': len(car),
        'year_range': year_range,
        'kms_range': kms_range,
        'price_range': price_range,
        'fuel_types': fuel_types,
        'transmission_types': transmission_types,
        'owner_types': owner_types,
        'condition_types': condition_types,
        'insurance_types': insurance_types,
        'cities': cities,
        'emission_norms': emission_norms,
        'insurance_eligible_types': insurance_eligible_types,
        'maintenance_levels': maintenance_levels,
        'listing_types': listing_types,
        'certified_types': is_certified_types
    }
    return jsonify(info)

# Query endpoints for car data
@app.route('/api/cars')
@cross_origin()
def get_cars():
    """Get all cars with optional filtering"""
    try:
        # Get query parameters
        company = request.args.get('company')
        model = request.args.get('model')
        year = request.args.get('year')
        city = request.args.get('city')
        limit = int(request.args.get('limit', 50))  # Default limit
        
        # Start with all cars
        filtered_cars = car.copy()
        
        # Apply filters
        if company:
            filtered_cars = filtered_cars[filtered_cars['company'] == company]
        if model:
            filtered_cars = filtered_cars[filtered_cars['model'] == model]
        if year:
            filtered_cars = filtered_cars[filtered_cars['year'] == int(year)]
        if city:
            filtered_cars = filtered_cars[filtered_cars['city'] == city]
        
        # Limit results
        filtered_cars = filtered_cars.head(limit)
        
        # Convert to list of dictionaries
        cars_list = filtered_cars.to_dict('records')
        
        return jsonify({
            'cars': cars_list,
            'total_found': len(cars_list),
            'total_in_dataset': len(car)
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/cars/<int:car_id>')
@cross_origin()
def get_car_by_id(car_id):
    """Get specific car by ID"""
    try:
        car_data = car[car['car_id'] == car_id]
        if car_data.empty:
            return jsonify({"error": "Car not found"}), 404
        
        return jsonify(car_data.iloc[0].to_dict())
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/cars/search')
@cross_origin()
def search_cars():
    """Advanced search for cars"""
    try:
        # Get search parameters
        query = request.args.get('q', '').lower()
        min_price = request.args.get('min_price')
        max_price = request.args.get('max_price')
        min_year = request.args.get('min_year')
        max_year = request.args.get('max_year')
        fuel_type = request.args.get('fuel_type')
        transmission = request.args.get('transmission')
        owner = request.args.get('owner')
        condition = request.args.get('condition')
        
        # Start with all cars
        filtered_cars = car.copy()
        
        # Text search in company and model
        if query:
            filtered_cars = filtered_cars[
                filtered_cars['company'].str.lower().str.contains(query) |
                filtered_cars['model'].str.lower().str.contains(query)
            ]
        
        # Price range filter
        if min_price:
            filtered_cars = filtered_cars[filtered_cars['Price'] >= int(min_price)]
        if max_price:
            filtered_cars = filtered_cars[filtered_cars['Price'] <= int(max_price)]
        
        # Year range filter
        if min_year:
            filtered_cars = filtered_cars[filtered_cars['year'] >= int(min_year)]
        if max_year:
            filtered_cars = filtered_cars[filtered_cars['year'] <= int(max_year)]
        
        # Categorical filters
        if fuel_type:
            filtered_cars = filtered_cars[filtered_cars['fuel_type'] == fuel_type]
        if transmission:
            filtered_cars = filtered_cars[filtered_cars['transmission'] == transmission]
        if owner:
            filtered_cars = filtered_cars[filtered_cars['owner'] == owner]
        if condition:
            filtered_cars = filtered_cars[filtered_cars['car_condition'] == condition]
        
        # Convert to list of dictionaries
        cars_list = filtered_cars.to_dict('records')
        
        return jsonify({
            'cars': cars_list,
            'total_found': len(cars_list),
            'search_params': {
                'query': query,
                'min_price': min_price,
                'max_price': max_price,
                'min_year': min_year,
                'max_year': max_year,
                'fuel_type': fuel_type,
                'transmission': transmission,
                'owner': owner,
                'condition': condition
            }
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/predict', methods=['POST'])
@cross_origin()
def predict():
    try:
        # Accept both JSON and form data for flexibility
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
        
        # Extract all possible fields with defaults
        car_data = {
            'company': data.get('company'),
            'model': data.get('model') or data.get('car_models'),
            'year': data.get('year'),
            'kms_driven': data.get('kms_driven') or data.get('kilo_driven'),
            'fuel_type': data.get('fuel_type'),
            'transmission': data.get('transmission', 'Manual'),
            'owner': data.get('owner', '1st'),
            'car_condition': data.get('car_condition', 'Good'),
            'insurance_status': data.get('insurance_status', 'Yes'),
            'previous_accidents': data.get('previous_accidents', 0),
            'num_doors': data.get('num_doors', 4),
            'engine_size': data.get('engine_size', 1500),
            'power': data.get('power', 100),
            'city': data.get('city', 'Delhi'),
            'emission_norm': data.get('emission_norm', 'BS-IV'),
            'insurance_eligible': data.get('insurance_eligible', 'Yes'),
            'maintenance_level': data.get('maintenance_level', 'Medium')
        }

        # Validate required fields
        required_fields = ['company', 'model', 'year', 'fuel_type', 'kms_driven']
        missing_fields = [field for field in required_fields if not car_data[field]]
        
        if missing_fields:
            return jsonify({
                "error": f"Missing required fields: {', '.join(missing_fields)}"
            }), 400

        # Convert numeric fields
        try:
            car_data['year'] = int(car_data['year'])
            car_data['kms_driven'] = int(car_data['kms_driven'])
            car_data['previous_accidents'] = int(car_data['previous_accidents'])
            car_data['num_doors'] = int(car_data['num_doors'])
            car_data['engine_size'] = int(car_data['engine_size'])
            car_data['power'] = int(car_data['power'])
        except (ValueError, TypeError) as e:
            return jsonify({
                "error": f"Invalid numeric values: {str(e)}"
            }), 400

        # Use enhanced model if available
        if enhanced_model is not None:
            prediction_result = predict_with_enhanced_model(car_data)
        else:
            prediction_result = predict_with_legacy_model(car_data)
        
        return jsonify(prediction_result)
    
    except Exception as e:
        print(f"Error in prediction: {str(e)}")
        return jsonify({"error": f"Unable to make prediction. {str(e)}"}), 500

def predict_with_enhanced_model(car_data):
    """Predict using the enhanced model with all 22 fields"""
    try:
        # Create DataFrame with input data
        input_df = pd.DataFrame([car_data])
        
        # Encode categorical variables
        encoded_data = {}
        
        # Encode categorical features
        for col in enhanced_categorical_columns:
            if col in car_data:
                try:
                    encoded_data[col + '_encoded'] = enhanced_label_encoders[col].transform([car_data[col]])[0]
                except ValueError:
                    # Handle unseen categories by using the most common category
                    most_common = enhanced_label_encoders[col].classes_[0]
                    encoded_data[col + '_encoded'] = enhanced_label_encoders[col].transform([most_common])[0]
                    print(f"Warning: Unknown {col} '{car_data[col]}', using '{most_common}'")
        
        # Add numerical features
        for col in enhanced_numerical_features:
            if col in car_data:
                encoded_data[col] = car_data[col]
        
        # Create feature vector in correct order
        feature_vector = []
        for feature_name in enhanced_feature_names:
            if feature_name in encoded_data:
                feature_vector.append(encoded_data[feature_name])
            else:
                # Use default values for missing features
                if feature_name in enhanced_numerical_features:
                    feature_vector.append(0)  # Default for numerical
                else:
                    feature_vector.append(0)  # Default for encoded categorical
        
        # Convert to numpy array and reshape
        X = np.array(feature_vector).reshape(1, -1)
        
        # Scale features
        X_scaled = enhanced_scaler.transform(X)
        
        # Make prediction
        prediction = enhanced_model.predict(X_scaled)[0]
        predicted_price = float(np.round(prediction, 2))
        
        # Calculate confidence based on model performance
        confidence_score = min(95, max(60, int(enhanced_model_data['model_scores'][enhanced_model_data['best_model_name']]['test_r2'] * 100)))
        
        return {
            "prediction": predicted_price,
            "model_used": enhanced_model_data['best_model_name'],
            "confidence_score": confidence_score,
            "model_performance": {
                "test_r2": enhanced_model_data['model_scores'][enhanced_model_data['best_model_name']]['test_r2'],
                "test_rmse": enhanced_model_data['model_scores'][enhanced_model_data['best_model_name']]['test_rmse']
            },
            "features_used": len(enhanced_feature_names),
            "message": "Enhanced prediction with all features"
        }
    
    except Exception as e:
        print(f"Enhanced model prediction error: {str(e)}")
        raise e

def predict_with_legacy_model(car_data):
    """Fallback to legacy model for backward compatibility"""
    try:
        # Validate that values exist in training data
        if car_data['company'] not in le_company.classes_:
            return {"error": f"Company '{car_data['company']}' not found in training data."}
        
        if car_data['model'] not in le_name.classes_:
            return {"error": f"Car model '{car_data['model']}' not found in training data."}
        
        if car_data['fuel_type'] not in le_fuel.classes_:
            return {"error": f"Fuel type '{car_data['fuel_type']}' not found in training data."}

        # Create DataFrame with input data
        input_data = pd.DataFrame({
            'name': [car_data['model']],
            'company': [car_data['company']], 
            'year': [car_data['year']],
            'kms_driven': [car_data['kms_driven']],
            'fuel_type': [car_data['fuel_type']]
        })

        # Encode categorical variables
        input_data['name_encoded'] = le_name.transform(input_data['name'])
        input_data['company_encoded'] = le_company.transform(input_data['company'])
        input_data['fuel_encoded'] = le_fuel.transform(input_data['fuel_type'])

        # Select only the encoded features
        input_encoded = input_data[['name_encoded', 'company_encoded', 'year', 'kms_driven', 'fuel_encoded']]

        prediction = model.predict(input_encoded)
        predicted_price = float(np.round(prediction[0], 2))
        
        return {
            "prediction": predicted_price,
            "model_used": "Legacy Linear Regression",
            "confidence_score": 75,
            "message": "Legacy prediction (limited features)"
        }
    
    except Exception as e:
        print(f"Legacy model prediction error: {str(e)}")
        raise e

# In-memory user store (for demonstration purposes)
users = {
    "admin@example.com": {
        "password": "password",
        "name": "Admin User"
    }
}

# Legacy route for backward compatibility
@app.route('/predict', methods=['POST'])
@cross_origin()
def predict_legacy():
    try:
        # Handle both form data and JSON
        if request.is_json:
            data = request.get_json()
            company = data.get('company')
            car_model = data.get('car_models') or data.get('model')
            year = data.get('year')
            fuel_type = data.get('fuel_type')
            driven = data.get('kilo_driven') or data.get('kms_driven')
        else:
            company = request.form.get('company')
            car_model = request.form.get('car_models') or request.form.get('model')
            year = request.form.get('year')
            fuel_type = request.form.get('fuel_type')
            driven = request.form.get('kilo_driven') or request.form.get('kms_driven')

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
        
        print(f"Legacy Prediction: {predicted_price}")

        return jsonify({
            "prediction": predicted_price,
            "model_used": "Legacy Linear Regression",
            "message": "Legacy prediction successful"
        })
    
    except Exception as e:
        print(f"Error in legacy prediction: {str(e)}")
        return jsonify({"error": f"Unable to make prediction. {str(e)}"}), 500

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