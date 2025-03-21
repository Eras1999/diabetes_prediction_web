from flask import Flask, request, jsonify, render_template
import pandas as pd
import joblib
import numpy as np

app = Flask(__name__)

# Load the saved model and preprocessing objects
model = joblib.load('diabetes_model.pkl')
label_encoder_gender = joblib.load('label_encoder_gender.pkl')
label_encoder_smoking = joblib.load('label_encoder_smoking.pkl')
scaler = joblib.load('scaler.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from the form
        data = request.form
        gender = data['gender']
        age = float(data['age'])
        hypertension = int(data['hypertension'])
        heart_disease = int(data['heart_disease'])
        smoking_history = data['smoking_history']
        bmi = float(data['bmi'])
        hba1c_level = float(data['hba1c_level'])
        blood_glucose_level = float(data['blood_glucose_level'])

        # Create a DataFrame with user input
        user_data = pd.DataFrame({
            'gender': [gender],
            'age': [age],
            'hypertension': [hypertension],
            'heart_disease': [heart_disease],
            'smoking_history': [smoking_history],
            'bmi': [bmi],
            'HbA1c_level': [hba1c_level],
            'blood_glucose_level': [blood_glucose_level]
        })

        # Encode categorical variables
        user_data['gender'] = label_encoder_gender.transform(user_data['gender'])
        user_data['smoking_history'] = label_encoder_smoking.transform(user_data['smoking_history'])

        # Scale the user input
        user_data_scaled = scaler.transform(user_data)

        # Make prediction
        prediction = model.predict(user_data_scaled)

        # Prepare the result
        result = "The person is likely to have diabetes." if prediction[0] == 1 else "The person is not likely to have diabetes."
        return jsonify({'prediction': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)