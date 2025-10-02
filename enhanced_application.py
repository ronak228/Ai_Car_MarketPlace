from flask import Flask, render_template, request, redirect, jsonify
from flask_cors import CORS, cross_origin
import pickle
import pandas as pd
import numpy as np
import json
from datetime import datetime
from market_trends_analyzer import MarketTrendsAnalyzer, get_market_trends_data, get_company_comparison, get_price_prediction_trends

app = Flask(__name__)
cors = CORS(app)

# Load the model and encoders
model_data = pickle.load(open('LinearRegressionModel.pkl','rb'))
model = model_data['model']
le_name = model_data['le_name']
le_company = model_data['le_company']
le_fuel = model_data['le_fuel']

# Load car data
car = pd.read_csv('Cleaned_Car_data_master.csv')

# Initialize market trends analyzer
market_analyzer = MarketTrendsAnalyzer()

@app.route('/', methods=['GET','POST'])
def index():
    companies = sorted(car['company'].unique())
    car_models = sorted(car['model'].unique())
    year = sorted(car['year'].unique(), reverse=True)
    fuel_type = car['fuel_type'].unique()

    companies.insert(0, 'Select Company')
    return render_template('enhanced_index.html', 
                         companies=companies, 
                         car_models=car_models, 
                         years=year, 
                         fuel_types=fuel_type)

@app.route('/market-trends')
def market_trends_page():
    """Render the market trends dashboard page"""
    return render_template('market_trends.html')

@app.route('/predict', methods=['POST'])
@cross_origin()
def predict():
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

# Market Trends API Endpoints

@app.route('/api/market-overview')
@cross_origin()
def api_market_overview():
    """Get comprehensive market overview"""
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
            companies = car['company'].unique()
            suggestions['companies'] = [c for c in companies if query in c.lower()][:10]
        
        if category in ['all', 'models']:
            models = car['model'].unique()
            suggestions['models'] = [m for m in models if query in m.lower()][:10]
        
        if category in ['all', 'cities']:
            cities = car['city'].unique()
            suggestions['cities'] = [c for c in cities if query in c.lower()][:10]
        
        if category in ['all', 'fuel_types']:
            fuel_types = car['fuel_type'].unique()
            suggestions['fuel_types'] = [f for f in fuel_types if query in f.lower()][:10]
        
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

if __name__ == '__main__':
    app.run(debug=True, port=5000)
