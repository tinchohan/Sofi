from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from cleaning_rate_predictor import CleaningRatePredictor
import os

app = Flask(__name__)

# Inicializar el predictor
predictor = CleaningRatePredictor()

# Verificar si existe un modelo preentrenado
model_path = 'cleaning_rate_model.pkl'
if os.path.exists(model_path):
    try:
        predictor.load_model(model_path)
        print("Modelo preentrenado cargado exitosamente")
    except:
        print("Entrenando nuevo modelo...")
        predictor.train()
        predictor.save_model(model_path)
else:
    print("Entrenando nuevo modelo...")
    predictor.train()
    predictor.save_model(model_path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Obtener datos del formulario
        data = request.get_json()
        
        # Validar datos requeridos
        required_fields = ['sqft', 'bedrooms', 'bathrooms', 'property_type', 
                          'state', 'city_type', 'cleaning_type', 'frequency']
        
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo requerido faltante: {field}'}), 400
        
        # Convertir tipos de datos
        property_data = {
            'sqft': float(data['sqft']),
            'bedrooms': int(data['bedrooms']),
            'bathrooms': float(data['bathrooms']),
            'property_type': data['property_type'],
            'state': data['state'],
            'city_type': data['city_type'],
            'cleaning_type': data['cleaning_type'],
            'frequency': data['frequency']
        }
        
        # Validar rangos
        if property_data['sqft'] <= 0 or property_data['sqft'] > 20000:
            return jsonify({'error': 'Metros cuadrados debe estar entre 1 y 20,000'}), 400
        
        if property_data['bedrooms'] <= 0 or property_data['bedrooms'] > 20:
            return jsonify({'error': 'Número de habitaciones debe estar entre 1 y 20'}), 400
        
        if property_data['bathrooms'] <= 0 or property_data['bathrooms'] > 20:
            return jsonify({'error': 'Número de baños debe estar entre 1 y 20'}), 400
        
        # Hacer predicción
        prediction = predictor.predict(property_data)
        
        return jsonify({
            'success': True,
            'prediction': prediction
        })
        
    except Exception as e:
        return jsonify({'error': f'Error en la predicción: {str(e)}'}), 500

@app.route('/get_states')
def get_states():
    """Retorna lista de estados disponibles"""
    states = list(predictor.market_data['state_cost_index'].keys())
    return jsonify({'states': sorted(states)})

@app.route('/get_city_types')
def get_city_types():
    """Retorna tipos de ciudad disponibles"""
    city_types = list(predictor.market_data['city_type_multiplier'].keys())
    return jsonify({'city_types': city_types})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
