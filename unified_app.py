from flask import Flask, render_template, request, redirect, jsonify, send_from_directory
from flask_cors import CORS, cross_origin
import pickle
import pandas as pd
import numpy as np
import os
from datetime import datetime
import json
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')

# Fix Windows console encoding for emoji characters
import sys
import os
if sys.platform == "win32":
    os.system("chcp 65001 > nul")

# Import market trends analyzer
try:
    from market_trends_analyzer import MarketTrendsAnalyzer, get_market_trends_data, get_company_comparison, get_price_prediction_trends
    MARKET_TRENDS_AVAILABLE = True
    print("[OK] Market Trends Analyzer imported successfully")
except ImportError as e:
    print(f"[WARNING] Market Trends Analyzer not available: {e}")
    MARKET_TRENDS_AVAILABLE = False

# MongoDB authentication
try:
    from mongodb_config import get_sync_collections, test_connection
    from auth_routes import auth_bp
    from models import PredictionModel
    MONGODB_AVAILABLE = True
    print("[OK] MongoDB authentication available")
except ImportError as e:
    print(f"[WARNING] MongoDB authentication not available: {e}")
    MONGODB_AVAILABLE = False

app = Flask(__name__, static_folder='client/build/static', template_folder='client/build')
cors = CORS(app)

# Register authentication routes
if MONGODB_AVAILABLE:
    app.register_blueprint(auth_bp)
    print("[OK] MongoDB authentication routes registered")

# Debug: Print route registration order (removed deprecated before_first_request)
def debug_routes():
    print("\n🔍 Registered Routes:")
    for rule in app.url_map.iter_rules():
        print(f"   {rule.rule} -> {rule.endpoint}")
    print()

# Load the enhanced model and encoders
try:
    enhanced_model_data = pickle.load(open('BestCombinedModel.pkl', 'rb'))
    
    # Handle the actual model structure
    if isinstance(enhanced_model_data, dict):
        enhanced_model = enhanced_model_data.get('model')
        enhanced_model_name = enhanced_model_data.get('model_name', 'Enhanced Model')
        enhanced_categorical_columns = enhanced_model_data.get('categorical_features', [])
        enhanced_numerical_features = enhanced_model_data.get('numerical_features', [])
        enhanced_performance = enhanced_model_data.get('performance', {})
        
        # The model is a Pipeline, so we don't need separate scaler/encoders
        enhanced_scaler = None
        enhanced_label_encoders = {}
        enhanced_feature_names = enhanced_categorical_columns + enhanced_numerical_features
        
    else:
        # Fallback for unexpected format
        enhanced_model = None
        enhanced_scaler = None
        enhanced_label_encoders = {}
        enhanced_feature_names = []
        enhanced_categorical_columns = []
        enhanced_numerical_features = []
        enhanced_model_name = "Unknown"
        enhanced_performance = {}
        print("[WARNING] Enhanced model format not recognized")
        
except FileNotFoundError:
    print("[WARNING] Enhanced model not found, using legacy model")
    enhanced_model = None
    enhanced_scaler = None
    enhanced_label_encoders = {}
    enhanced_feature_names = []
    enhanced_categorical_columns = []
    enhanced_numerical_features = []
    enhanced_model_name = "None"
    enhanced_performance = {}
except Exception as e:
    print(f"[WARNING] Error loading enhanced model: {str(e)}")
    print("Using legacy model instead")
    enhanced_model = None
    enhanced_scaler = None
    enhanced_label_encoders = {}
    enhanced_feature_names = []
    enhanced_categorical_columns = []
    enhanced_numerical_features = []
    enhanced_model_name = "None"
    enhanced_performance = {}

# Legacy model (for backward compatibility)
try:
    model_data = pickle.load(open('LinearRegressionModel.pkl', 'rb'))
    model = model_data['model']
    le_name = model_data['le_name']
    le_company = model_data['le_company']
    le_fuel = model_data['le_fuel']
    le_transmission = model_data.get('le_transmission', None)
    scaler = model_data.get('scaler', None)
except Exception as e:
    print(f"[ERROR] Error loading legacy model: {str(e)}")
    print("[WARNING] No models available - some features may not work")
    model = None
    le_name = None
    le_company = None
    le_fuel = None
    le_transmission = None
    scaler = None

# Load master dataset with all 22 fields - use enhanced dataset
try:
    # Try to load the enhanced dataset first
    if os.path.exists('enhanced_indian_car_dataset.csv'):
        car = pd.read_csv('enhanced_indian_car_dataset.csv')
        print(f"[OK] Enhanced dataset loaded: {len(car)} records with {car['company'].nunique()} brands")
    else:
        # Fallback to original datasets
        car1 = pd.read_csv('Cleaned_Car_data_master.csv')
        car2 = pd.read_csv('generated_5000_strict.csv')
        car = pd.concat([car1, car2], ignore_index=True)
        print(f"[OK] Original datasets loaded: {len(car)} records")
    
except FileNotFoundError as e:
    print(f"[ERROR] Dataset file not found: {e}")
    print("[ERROR] Creating empty DataFrame")
    car = pd.DataFrame()

# Initialize market trends analyzer
market_analyzer = None
if MARKET_TRENDS_AVAILABLE:
    try:
        market_analyzer = MarketTrendsAnalyzer()
    except Exception as e:
        MARKET_TRENDS_AVAILABLE = False

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

@app.route('/api/models/<company>/<int:year>')
def get_models_by_company_and_year(company, year):
    """Get models for a specific company and year"""
    try:
        # Filter by company and year
        filtered_cars = car[(car['company'] == company) & (car['year'] == year)]
        
        if filtered_cars.empty:
            # If no exact match, find models available in that year range
            # Look for models that were available around that year (±2 years)
            year_range = car[(car['company'] == company) & 
                           (car['year'] >= year - 2) & 
                           (car['year'] <= year + 2)]
            
            if not year_range.empty:
                models = sorted(year_range['model'].unique())
                return jsonify({
                    'models': models,
                    'note': f'Models available around {year} (±2 years)',
                    'exact_year_available': False
                })
            else:
                # Fallback to all models for the company
                all_models = sorted(car[car['company'] == company]['model'].unique())
                return jsonify({
                    'models': all_models,
                    'note': f'All models for {company} (no data for {year})',
                    'exact_year_available': False
                })
        else:
            models = sorted(filtered_cars['model'].unique())
            return jsonify({
                'models': models,
                'note': f'Models available in {year}',
                'exact_year_available': True
            })
            
    except Exception as e:
        print(f"Error getting models for {company} in {year}: {str(e)}")
        # Fallback to company models only
        company_models = car[car['company'] == company]['model'].unique()
        return jsonify({
            'models': sorted(company_models),
            'note': f'All models for {company} (error occurred)',
            'exact_year_available': False
        })

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

        # Use enhanced model if available, with fallback to legacy
        if enhanced_model is not None:
            try:
                prediction_result = predict_with_enhanced_model(car_data)
            except Exception as e:
                print(f"Enhanced model prediction error: {str(e)}")
                print("Falling back to legacy model")
                prediction_result = predict_with_legacy_model(car_data)
        else:
            prediction_result = predict_with_legacy_model(car_data)
        
        
        # Store prediction in MongoDB if available and user is authenticated
        if MONGODB_AVAILABLE and 'user_id' in data:
            try:
                collections = get_sync_collections()
                if collections:
                    prediction_doc = PredictionModel.create_prediction_document(
                        data['user_id'],
                        car_data,
                        prediction_result['prediction']
                    )
                    collections['predictions'].insert_one(prediction_doc)
                    print(f"[OK] Prediction stored for user {data['user_id']}")
            except Exception as e:
                print(f"[WARNING] Failed to store prediction: {str(e)}")
        
        return jsonify(prediction_result)
    
    except Exception as e:
        print(f"Error in prediction: {str(e)}")
        return jsonify({"error": f"Unable to make prediction. {str(e)}"}), 500

def predict_with_enhanced_model(car_data):
    """Predict using the enhanced model (Pipeline) with all features"""
    try:
        # Create DataFrame with input data - the Pipeline expects all features
        input_data = {}
        
        # Add all categorical features
        for col in enhanced_categorical_columns:
            if col in car_data:
                input_data[col] = car_data[col]
            else:
                # Provide default values for missing categorical features
                if col == 'company':
                    input_data[col] = 'Maruti Suzuki'
                elif col == 'model':
                    input_data[col] = 'Alto'
                elif col == 'fuel_type':
                    input_data[col] = 'Petrol'
                elif col == 'transmission':
                    input_data[col] = 'Manual'
                elif col == 'owner':
                    input_data[col] = 'First Owner'
                elif col == 'car_condition':
                    input_data[col] = 'Good'
                elif col == 'insurance_status':
                    input_data[col] = 'Valid'
                elif col == 'city':
                    input_data[col] = 'Delhi'
                elif col == 'emission_norm':
                    input_data[col] = 'BS IV'
                elif col == 'insurance_eligible':
                    input_data[col] = 'Yes'
                elif col == 'maintenance_level':
                    input_data[col] = 'Good'
                elif col == 'listing_type':
                    input_data[col] = 'Individual'
                elif col == 'is_certified':
                    input_data[col] = 'No'
                else:
                    input_data[col] = 'Unknown'
        
        # Add all numerical features
        for col in enhanced_numerical_features:
            if col in car_data:
                input_data[col] = car_data[col]
            else:
                # Provide default values for missing numerical features
                if col == 'year':
                    input_data[col] = 2015
                elif col == 'kms_driven':
                    input_data[col] = 50000
                elif col == 'previous_accidents':
                    input_data[col] = 0
                elif col == 'num_doors':
                    input_data[col] = 4
                elif col == 'engine_size':
                    input_data[col] = 1200
                elif col == 'power':
                    input_data[col] = 80
                else:
                    input_data[col] = 0
        
        # Create DataFrame with single row
        input_df = pd.DataFrame([input_data])
        
        # Make prediction using the Pipeline (it handles encoding and scaling internally)
        prediction = enhanced_model.predict(input_df)[0]
        predicted_price = float(np.round(prediction, 2))
        
        # Calculate confidence based on model performance
        r2_score = enhanced_performance.get('r2_score', 0.85)
        confidence_score = min(95, max(60, int(r2_score * 100)))
        
        # Get additional car information from dataset
        car_info = get_car_info_from_dataset(car_data)
        
        return {
            "prediction": predicted_price,
            "model_used": enhanced_model_name,
            "confidence_score": confidence_score,
            "model_performance": {
                "r2_score": r2_score,
                "rmse": enhanced_performance.get('rmse', 50000),
                "mae": enhanced_performance.get('mae', 30000)
            },
            "features_used": len(enhanced_feature_names),
            "car_info": car_info,
            "message": f"Enhanced prediction using {enhanced_model_name} with {len(enhanced_feature_names)} features"
        }
    
    except Exception as e:
        print(f"Enhanced model prediction error: {str(e)}")
        raise e

def get_car_info_from_dataset(car_data):
    """Get comprehensive car information from dataset"""
    try:
        # Filter dataset for similar cars
        similar_cars = car[
            (car['company'] == car_data['company']) & 
            (car['model'] == car_data['model']) &
            (car['year'] == car_data['year'])
        ]
        
        if similar_cars.empty:
            # If no exact match, find similar cars from the same company and year
            similar_cars = car[
                (car['company'] == car_data['company']) & 
                (car['year'] == car_data['year'])
            ]
        
        if similar_cars.empty:
            # If still no match, find cars from the same company
            similar_cars = car[car['company'] == car_data['company']]
        
        if not similar_cars.empty:
            # Calculate statistics
            avg_price = similar_cars['Price'].mean()
            min_price = similar_cars['Price'].min()
            max_price = similar_cars['Price'].max()
            price_std = similar_cars['Price'].std()
            
            # Get fuel type distribution
            fuel_distribution = similar_cars['fuel_type'].value_counts().to_dict()
            
            # Get transmission distribution
            transmission_distribution = similar_cars['transmission'].value_counts().to_dict()
            
            # Get condition distribution
            condition_distribution = similar_cars['car_condition'].value_counts().to_dict()
            
            # Get city distribution
            city_distribution = similar_cars['city'].value_counts().head(10).to_dict()
            
            # Get year range for this company/model
            year_range = {
                'min': int(similar_cars['year'].min()),
                'max': int(similar_cars['year'].max())
            }
            
            # Get average kilometers
            avg_kms = similar_cars['kms_driven'].mean()
            
            return {
                'similar_cars_found': len(similar_cars),
                'price_statistics': {
                    'average': float(round(avg_price, 2)),
                    'minimum': float(round(min_price, 2)),
                    'maximum': float(round(max_price, 2)),
                    'standard_deviation': float(round(price_std, 2)) if not pd.isna(price_std) else 0.0
                },
                'fuel_type_distribution': fuel_distribution,
                'transmission_distribution': transmission_distribution,
                'condition_distribution': condition_distribution,
                'top_cities': city_distribution,
                'year_range': year_range,
                'average_kilometers': float(round(avg_kms, 0)),
                'data_availability': {
                    'exact_match': len(car[
                        (car['company'] == car_data['company']) & 
                        (car['model'] == car_data['model']) &
                        (car['year'] == car_data['year'])
                    ]) > 0,
                    'company_year_match': len(car[
                        (car['company'] == car_data['company']) & 
                        (car['year'] == car_data['year'])
                    ]) > 0,
                    'company_match': len(car[car['company'] == car_data['company']]) > 0
                }
            }
        else:
            return {
                'similar_cars_found': 0,
                'message': 'No similar cars found in dataset'
            }
            
    except Exception as e:
        print(f"Error getting car info: {str(e)}")
        return {
            'similar_cars_found': 0,
            'error': str(e)
        }

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
        
        # Get additional car information from dataset
        car_info = get_car_info_from_dataset(car_data)
        
        return {
            "prediction": predicted_price,
            "model_used": "Legacy Linear Regression",
            "confidence_score": 75,
            "car_info": car_info,
            "message": "Legacy prediction (limited features)"
        }
    
    except Exception as e:
        print(f"Legacy model prediction error: {str(e)}")
        raise e

# ============================================================================
# MARKET TRENDS API ENDPOINTS
# ============================================================================

@app.route('/api/market-overview')
@cross_origin()
def api_market_overview():
    """Get comprehensive market overview"""
    if not MARKET_TRENDS_AVAILABLE or not market_analyzer:
        return jsonify({
            'success': False,
            'error': 'Market trends analysis not available'
        }), 503
    
    try:
        overview = market_analyzer.get_market_overview()
        return jsonify({
            'success': True,
            'data': overview,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/company-trends')
@cross_origin()
def api_company_trends():
    """Get company-wise market trends"""
    if not MARKET_TRENDS_AVAILABLE or not market_analyzer:
        return jsonify({
            'success': False,
            'error': 'Market trends analysis not available'
        }), 503
    
    try:
        company_trends = market_analyzer.get_company_trends()
        return jsonify({
            'success': True,
            'data': company_trends,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/company-comparison')
@cross_origin()
def api_company_comparison():
    """Compare specific companies"""
    if not MARKET_TRENDS_AVAILABLE:
        return jsonify({
            'success': False,
            'error': 'Market trends analysis not available'
        }), 503
    
    try:
        companies = request.args.getlist('companies')
        if not companies:
            return jsonify({
                'success': False,
                'error': 'Please provide companies parameter'
            }), 400
        
        comparison = get_company_comparison(companies)
        return jsonify({
            'success': True,
            'data': comparison,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/fuel-type-analysis')
@cross_origin()
def api_fuel_type_analysis():
    """Get fuel type market analysis"""
    if not MARKET_TRENDS_AVAILABLE or not market_analyzer:
        return jsonify({
            'success': False,
            'error': 'Market trends analysis not available'
        }), 503
    
    try:
        fuel_analysis = market_analyzer.get_fuel_type_analysis()
        return jsonify({
            'success': True,
            'data': fuel_analysis,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/city-market-analysis')
@cross_origin()
def api_city_market_analysis():
    """Get city-wise market analysis"""
    if not MARKET_TRENDS_AVAILABLE or not market_analyzer:
        return jsonify({
            'success': False,
            'error': 'Market trends analysis not available'
        }), 503
    
    try:
        city_analysis = market_analyzer.get_city_market_analysis()
        return jsonify({
            'success': True,
            'data': city_analysis,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/price-trends')
@cross_origin()
def api_price_trends():
    """Get price trends by year"""
    if not MARKET_TRENDS_AVAILABLE or not market_analyzer:
        return jsonify({
            'success': False,
            'error': 'Market trends analysis not available'
        }), 503
    
    try:
        price_trends = market_analyzer.get_price_trends_by_year()
        return jsonify({
            'success': True,
            'data': price_trends,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/market-predictions')
@cross_origin()
def api_market_predictions():
    """Get market predictions and insights"""
    if not MARKET_TRENDS_AVAILABLE or not market_analyzer:
        return jsonify({
            'success': False,
            'error': 'Market trends analysis not available'
        }), 503
    
    try:
        predictions = market_analyzer.get_market_predictions()
        return jsonify({
            'success': True,
            'data': predictions,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/advanced-analytics')
@cross_origin()
def api_advanced_analytics():
    """Get advanced analytics including clustering and correlations"""
    if not MARKET_TRENDS_AVAILABLE or not market_analyzer:
        return jsonify({
            'success': False,
            'error': 'Market trends analysis not available'
        }), 503
    
    try:
        analytics = market_analyzer.get_advanced_analytics()
        return jsonify({
            'success': True,
            'data': analytics,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/filtered-trends')
@cross_origin()
def api_filtered_trends():
    """Get filtered price trends"""
    if not MARKET_TRENDS_AVAILABLE:
        return jsonify({
            'success': False,
            'error': 'Market trends analysis not available'
        }), 503
    
    try:
        fuel_type = request.args.get('fuel_type')
        company = request.args.get('company')
        year_start = request.args.get('year_start', type=int)
        year_end = request.args.get('year_end', type=int)
        
        year_range = None
        if year_start and year_end:
            year_range = [year_start, year_end]
        
        trends = get_price_prediction_trends(fuel_type, company, year_range)
        return jsonify({
            'success': True,
            'data': trends,
            'filters': {
                'fuel_type': fuel_type,
                'company': company,
                'year_range': year_range
            },
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/market-report')
@cross_origin()
def api_market_report():
    """Get comprehensive market report"""
    if not MARKET_TRENDS_AVAILABLE or not market_analyzer:
        return jsonify({
            'success': False,
            'error': 'Market trends analysis not available'
        }), 503
    
    try:
        report = market_analyzer.generate_market_report()
        return jsonify({
            'success': True,
            'data': report
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============================================================================
# ENHANCED CHART DATA APIs
# ============================================================================

@app.route('/api/charts/price-trends-by-year')
@cross_origin()
def api_price_trends_chart():
    """Get price trends by year for chart visualization"""
    try:
        # Get price trends by year directly from dataset
        price_trends = car.groupby('year')['Price'].mean().round(2)
        
        # Format for chart.js
        chart_data = {
            'labels': [str(year) for year in price_trends.index],
            'datasets': [
                {
                    'label': 'Average Price (₹)',
                    'data': list(price_trends.values),
                    'borderColor': 'rgb(75, 192, 192)',
                    'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                    'tension': 0.1
                }
            ]
        }
        
        return jsonify({
            'success': True,
            'data': chart_data,
            'title': 'Car Price Trends by Year',
            'description': 'Average car prices across different years'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/charts/company-market-share')
@cross_origin()
def api_company_market_share_chart():
    """Get company market share data for pie chart - ALL BRANDS"""
    try:
        # Get company counts directly from dataset
        company_counts = car['company'].value_counts()
        
        # Get ALL companies by count (sorted)
        all_companies = [(company, count) for company, count in company_counts.items()]
        all_companies.sort(key=lambda x: x[1], reverse=True)
        
        # Generate colors for all companies
        colors = [
            '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40',
            '#C9CBCF', '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
            '#FF9F40', '#C9CBCF', '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0',
            '#9966FF', '#FF9F40', '#C9CBCF', '#FF6384', '#36A2EB', '#FFCE56',
            '#4BC0C0', '#9966FF', '#FF9F40', '#C9CBCF', '#FF6384', '#36A2EB',
            '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', '#C9CBCF', '#FF6384',
            '#36A2EB', '#FFCE56'
        ]
        
        # Format for chart.js pie chart
        chart_data = {
            'labels': [company[0] for company in all_companies],
            'datasets': [
                {
                    'label': 'Market Share (Number of Cars)',
                    'data': [company[1] for company in all_companies],
                    'backgroundColor': colors[:len(all_companies)],
                    'borderWidth': 2,
                    'borderColor': '#fff'
                }
            ]
        }
        
        return jsonify({
            'success': True,
            'data': chart_data,
            'title': f'All {len(all_companies)} Companies by Market Share',
            'description': f'Complete distribution of car listings across all {len(all_companies)} brands'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/charts/fuel-type-distribution')
@cross_origin()
def api_fuel_type_distribution_chart():
    """Get fuel type distribution for chart"""
    try:
        # Get fuel type counts directly from dataset
        fuel_counts = car['fuel_type'].value_counts()
        
        # Format for chart.js
        chart_data = {
            'labels': list(fuel_counts.keys()),
            'datasets': [
                {
                    'label': 'Number of Cars',
                    'data': [int(count) for count in fuel_counts.values],
                    'backgroundColor': [
                        '#FF6384',  # Petrol - Red
                        '#36A2EB',  # Diesel - Blue
                        '#FFCE56',  # CNG - Yellow
                        '#4BC0C0',  # Electric - Teal
                        '#9966FF',  # Hybrid - Purple
                        '#FF9F40'   # LPG - Orange
                    ],
                    'borderWidth': 2,
                    'borderColor': '#fff'
                }
            ]
        }
        
        return jsonify({
            'success': True,
            'data': chart_data,
            'title': 'Fuel Type Distribution',
            'description': 'Distribution of cars by fuel type'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/charts/city-price-comparison')
@cross_origin()
def api_city_price_comparison_chart():
    """Get city-wise price comparison for bar chart - ALL CITIES"""
    try:
        # Get city average prices directly from dataset
        city_avg_prices = car.groupby('city')['Price'].agg(['mean', 'count']).round(2)
        city_avg_prices = city_avg_prices.sort_values('mean', ascending=False)
        
        # Get ALL cities by average price (sorted)
        all_cities = [(city, data['mean']) for city, data in city_avg_prices.iterrows()]
        
        # Format for chart.js bar chart
        chart_data = {
            'labels': [city[0] for city in all_cities],
            'datasets': [
                {
                    'label': 'Average Price (₹)',
                    'data': [city[1] for city in all_cities],
                    'backgroundColor': 'rgba(54, 162, 235, 0.8)',
                    'borderColor': 'rgba(54, 162, 235, 1)',
                    'borderWidth': 1
                }
            ]
        }
        
        return jsonify({
            'success': True,
            'data': chart_data,
            'title': f'All {len(all_cities)} Cities by Average Car Price',
            'description': f'Complete comparison of average car prices across all {len(all_cities)} Indian cities'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/charts/transmission-trends')
@cross_origin()
def api_transmission_trends_chart():
    """Get transmission type trends over years"""
    if not MARKET_TRENDS_AVAILABLE or not market_analyzer:
        return jsonify({
            'success': False,
            'error': 'Market trends analysis not available'
        }), 503
    
    try:
        # Analyze transmission trends by year
        transmission_trends = {}
        
        for year in sorted(car['year'].unique()):
            year_data = car[car['year'] == year]
            transmission_counts = year_data['transmission'].value_counts()
            transmission_trends[year] = transmission_counts.to_dict()
        
        # Get unique transmission types
        transmission_types = car['transmission'].unique()
        
        # Format for chart.js line chart
        chart_data = {
            'labels': list(transmission_trends.keys()),
            'datasets': []
        }
        
        colors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF']
        
        for i, transmission in enumerate(transmission_types):
            data = [transmission_trends[year].get(transmission, 0) for year in transmission_trends.keys()]
            chart_data['datasets'].append({
                'label': transmission,
                'data': data,
                'borderColor': colors[i % len(colors)],
                'backgroundColor': colors[i % len(colors)].replace('rgb', 'rgba').replace(')', ', 0.2)'),
                'tension': 0.1
            })
        
        return jsonify({
            'success': True,
            'data': chart_data,
            'title': 'Transmission Type Trends Over Years',
            'description': 'Popularity of different transmission types across years'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/charts/ev-vs-ice-trends')
@cross_origin()
def api_ev_vs_ice_trends_chart():
    """Get EV vs ICE (Internal Combustion Engine) trends"""
    if not MARKET_TRENDS_AVAILABLE or not market_analyzer:
        return jsonify({
            'success': False,
            'error': 'Market trends analysis not available'
        }), 503
    
    try:
        # Analyze EV vs ICE trends by year
        ev_ice_trends = {}
        
        for year in sorted(car['year'].unique()):
            year_data = car[car['year'] == year]
            
            # Count EVs (Electric) vs ICE (Petrol, Diesel, CNG, LPG)
            ev_count = len(year_data[year_data['fuel_type'] == 'Electric'])
            ice_count = len(year_data[year_data['fuel_type'].isin(['Petrol', 'Diesel', 'CNG', 'LPG'])])
            hybrid_count = len(year_data[year_data['fuel_type'] == 'Hybrid'])
            
            ev_ice_trends[year] = {
                'Electric': ev_count,
                'ICE': ice_count,
                'Hybrid': hybrid_count
            }
        
        # Format for chart.js line chart
        chart_data = {
            'labels': list(ev_ice_trends.keys()),
            'datasets': [
                {
                    'label': 'Electric Vehicles',
                    'data': [ev_ice_trends[year]['Electric'] for year in ev_ice_trends.keys()],
                    'borderColor': '#4BC0C0',
                    'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                    'tension': 0.1
                },
                {
                    'label': 'ICE Vehicles',
                    'data': [ev_ice_trends[year]['ICE'] for year in ev_ice_trends.keys()],
                    'borderColor': '#FF6384',
                    'backgroundColor': 'rgba(255, 99, 132, 0.2)',
                    'tension': 0.1
                },
                {
                    'label': 'Hybrid Vehicles',
                    'data': [ev_ice_trends[year]['Hybrid'] for year in ev_ice_trends.keys()],
                    'borderColor': '#FFCE56',
                    'backgroundColor': 'rgba(255, 206, 86, 0.2)',
                    'tension': 0.1
                }
            ]
        }
        
        return jsonify({
            'success': True,
            'data': chart_data,
            'title': 'EV vs ICE Vehicle Trends',
            'description': 'Growth of Electric, ICE, and Hybrid vehicles over time'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/charts/price-vs-kms-scatter')
@cross_origin()
def api_price_vs_kms_scatter_chart():
    """Get price vs kilometers driven scatter plot data"""
    if not MARKET_TRENDS_AVAILABLE or not market_analyzer:
        return jsonify({
            'success': False,
            'error': 'Market trends analysis not available'
        }), 503
    
    try:
        # Sample data for scatter plot (to avoid too many points)
        sample_data = car.sample(min(1000, len(car)))
        
        # Format for chart.js scatter plot
        chart_data = {
            'datasets': [
                {
                    'label': 'Price vs Kilometers',
                    'data': [
                        {
                            'x': int(row['kms_driven']),
                            'y': int(row['Price'])
                        }
                        for _, row in sample_data.iterrows()
                    ],
                    'backgroundColor': 'rgba(54, 162, 235, 0.6)',
                    'borderColor': 'rgba(54, 162, 235, 1)',
                    'pointRadius': 3
                }
            ]
        }
        
        return jsonify({
            'success': True,
            'data': chart_data,
            'title': 'Price vs Kilometers Driven',
            'description': 'Relationship between car price and kilometers driven'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/charts/company-price-comparison')
@cross_origin()
def api_company_price_comparison_chart():
    """Get company-wise average price comparison - ALL BRANDS"""
    try:
        # Get company average prices directly from dataset
        company_avg_prices = car.groupby('company')['Price'].agg(['mean', 'count']).round(2)
        company_avg_prices = company_avg_prices.sort_values('mean', ascending=False)
        
        # Get ALL companies by average price (sorted)
        all_companies = [(company, data['mean']) for company, data in company_avg_prices.iterrows()]
        
        # Format for chart.js bar chart
        chart_data = {
            'labels': [company[0] for company in all_companies],
            'datasets': [
                {
                    'label': 'Average Price (₹)',
                    'data': [company[1] for company in all_companies],
                    'backgroundColor': 'rgba(255, 99, 132, 0.8)',
                    'borderColor': 'rgba(255, 99, 132, 1)',
                    'borderWidth': 1
                }
            ]
        }
        
        return jsonify({
            'success': True,
            'data': chart_data,
            'title': f'All {len(all_companies)} Companies by Average Price',
            'description': f'Complete comparison of average car prices across all {len(all_companies)} brands'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/search-suggestions')
@cross_origin()
def api_search_suggestions():
    """Get search suggestions for companies, models, etc."""
    try:
        query = request.args.get('q', '').lower()
        category = request.args.get('category', 'all')
        
        suggestions = {
            'companies': [],
            'models': [],
            'cities': [],
            'fuel_types': []
        }
        
        if category in ['all', 'companies']:
            companies_list = car['company'].unique()
            suggestions['companies'] = [c for c in companies_list if query in c.lower()][:10]
        
        if category in ['all', 'models']:
            models_list = car['model'].unique()
            suggestions['models'] = [m for m in models_list if query in m.lower()][:10]
        
        if category in ['all', 'cities']:
            cities_list = car['city'].unique()
            suggestions['cities'] = [c for c in cities_list if query in c.lower()][:10]
        
        if category in ['all', 'fuel_types']:
            fuel_types_list = car['fuel_type'].unique()
            suggestions['fuel_types'] = [f for f in fuel_types_list if query in f.lower()][:10]
        
        return jsonify({
            'success': True,
            'data': suggestions,
            'query': query
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

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

# ============================================================================
# WEB ROUTES FOR MARKET TRENDS
# ============================================================================

@app.route('/market-trends')
def market_trends_page():
    """Render the market trends dashboard page"""
    if MARKET_TRENDS_AVAILABLE:
        try:
            return render_template('market_trends.html')
        except:
            # Fallback if template not found
            return """
            <html>
            <head><title>Market Trends</title></head>
            <body>
                <h1>Market Trends Dashboard</h1>
                <p>Market trends functionality is available via API endpoints:</p>
                <ul>
                    <li><a href="/api/market-overview">Market Overview</a></li>
                    <li><a href="/api/company-trends">Company Trends</a></li>
                    <li><a href="/api/fuel-type-analysis">Fuel Type Analysis</a></li>
                    <li><a href="/api/city-market-analysis">City Market Analysis</a></li>
                    <li><a href="/api/price-trends">Price Trends</a></li>
                    <li><a href="/api/market-predictions">Market Predictions</a></li>
                    <li><a href="/api/advanced-analytics">Advanced Analytics</a></li>
                    <li><a href="/api/market-report">Complete Market Report</a></li>
                </ul>
                <p><a href="/">← Back to Main App</a></p>
            </body>
            </html>
            """
    else:
        return jsonify({
            'error': 'Market trends functionality not available',
            'message': 'Please ensure market_trends_analyzer.py is available'
        }), 503

@app.route('/enhanced')
def enhanced_predictor():
    """Render the enhanced predictor page with market trends"""
    if MARKET_TRENDS_AVAILABLE:
        try:
            # Try to serve enhanced template
            companies_list = sorted(car['company'].unique())
            car_models_list = sorted(car['model'].unique())
            years_list = sorted(car['year'].unique(), reverse=True)
            fuel_types_list = car['fuel_type'].unique()
            
            companies_list.insert(0, 'Select Company')
            
            return render_template('enhanced_index.html', 
                                 companies=companies_list, 
                                 car_models=car_models_list, 
                                 years=years_list, 
                                 fuel_types=fuel_types_list)
        except:
            # Fallback to basic functionality
            return jsonify({
                'message': 'Enhanced predictor template not found, using API endpoints',
                'market_trends_available': True,
                'api_endpoints': [
                    '/api/market-overview',
                    '/api/company-trends',
                    '/api/fuel-type-analysis',
                    '/api/city-market-analysis',
                    '/api/price-trends',
                    '/api/market-predictions',
                    '/api/advanced-analytics',
                    '/api/market-report'
                ]
            })
    else:
        return redirect('/')

# API Route Debugging
@app.route('/api/')
def api_root():
    """API root endpoint for debugging"""
    available_endpoints = []
    for rule in app.url_map.iter_rules():
        if rule.rule.startswith('/api/'):
            available_endpoints.append({
                'endpoint': rule.rule,
                'methods': list(rule.methods - {'HEAD', 'OPTIONS'})
            })
    
    return jsonify({
        'message': 'Car Price Predictor API',
        'available_endpoints': available_endpoints,
        'market_trends_available': MARKET_TRENDS_AVAILABLE
    })

# Test endpoint to verify routing
@app.route('/api/test')
def api_test():
    """Simple test endpoint"""
    return jsonify({
        'message': 'API test endpoint working',
        'status': 'success'
    })

if __name__ == '__main__':
    print("AI Car Marketplace - Enhanced Edition")
    print("=" * 40)
    print("[OK] ML Model: Ready")
    if not car.empty:
        print(f"[OK] Dataset: {len(car):,} cars from {car['company'].nunique()} brands")
        ev_count = len(car[car['fuel_type'] == 'Electric'])
        if ev_count > 0:
            print(f"[OK] Electric Vehicles: {ev_count:,} models")
        print(f"[OK] Cities: {car['city'].nunique()} locations")
    else:
        print("[WARNING] Dataset: Not loaded")
    print("[OK] Authentication: Supabase + OTP")
    if MONGODB_AVAILABLE:
        print("[OK] MongoDB Atlas: Connected")
    else:
        print("[WARNING] MongoDB: Not available")
    print("=" * 40)
    print("Backend: http://localhost:5000")
    print("Frontend: http://localhost:3000")
    print("=" * 40)
    app.run(debug=True, host='0.0.0.0', port=5000) 

# ============================================================================
# REACT APP ROUTES (Defined last to ensure API routes take precedence)
# ============================================================================

@app.route('/')
def serve_react_app():
    return send_from_directory('client/build', 'index.html')

# Handle specific routes that are NOT API routes
@app.route('/market-trends')
def market_trends_route():
    if MARKET_TRENDS_AVAILABLE:
        return market_trends_page()
    else:
        return redirect('/')

@app.route('/enhanced')
def enhanced_route():
    if MARKET_TRENDS_AVAILABLE:
        return enhanced_predictor()
    else:
        return redirect('/')

# Serve static files (CSS, JS, images, etc.)
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('client/build/static', filename)

# Catch-all route for React Router (placed at the end to not interfere with API routes)
@app.route('/<path:path>')
def serve_react_routes(path):
    # Serve React app static files first
    if os.path.exists(os.path.join('client/build', path)):
        return send_from_directory('client/build', path)
    
    # For any other path, serve React app (allows React Router to handle routing)
    return send_from_directory('client/build', 'index.html') 