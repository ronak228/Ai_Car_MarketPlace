from flask import Flask,render_template,request,redirect
from flask_cors import CORS,cross_origin
import pickle
import pandas as pd
import numpy as np

app=Flask(__name__)
cors=CORS(app)

# Load the model and encoders
model_data = pickle.load(open('LinearRegressionModel.pkl','rb'))
model = model_data['model']
le_name = model_data['le_name']
le_company = model_data['le_company']
le_fuel = model_data['le_fuel']

car=pd.read_csv('Cleaned_Car_data.csv')

@app.route('/',methods=['GET','POST'])
def index():
    companies=sorted(car['company'].unique())
    car_models=sorted(car['name'].unique())
    year=sorted(car['year'].unique(),reverse=True)
    fuel_type=car['fuel_type'].unique()

    companies.insert(0,'Select Company')
    return render_template('index.html',companies=companies, car_models=car_models, years=year,fuel_types=fuel_type)


@app.route('/predict',methods=['POST'])
@cross_origin()
def predict():
    try:
        company=request.form.get('company')
        car_model=request.form.get('car_models')
        year=request.form.get('year')
        fuel_type=request.form.get('fuel_type')
        driven=request.form.get('kilo_driven')

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

        prediction=model.predict(input_encoded)
        print(f"Prediction: {prediction[0]}")

        return str(np.round(prediction[0],2))
    
    except Exception as e:
        print(f"Error in prediction: {str(e)}")
        return f"Error: Unable to make prediction. {str(e)}", 500


if __name__=='__main__':
    app.run(debug=True)