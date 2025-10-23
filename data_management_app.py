"""
Aplicación web para gestión de datos reales
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import pandas as pd
import os
from data_uploader import DataUploader
import json

app = Flask(__name__)

# Inicializar uploader
uploader = DataUploader()

@app.route('/')
def index():
    return render_template('data_management.html')

@app.route('/upload', methods=['POST'])
def upload_data():
    """Cargar datos desde CSV"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No se seleccionó archivo'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No se seleccionó archivo'}), 400
        
        if file and file.filename.endswith('.csv'):
            # Guardar archivo temporalmente
            file_path = 'temp_data.csv'
            file.save(file_path)
            
            # Cargar datos
            df = uploader.load_csv_data(file_path)
            
            if df is not None:
                # Entrenar modelo con datos reales
                metrics = uploader.train_with_real_data(df)
                
                # Limpiar archivo temporal
                os.remove(file_path)
                
                return jsonify({
                    'success': True,
                    'message': 'Datos cargados y modelo entrenado exitosamente',
                    'metrics': metrics,
                    'data_summary': {
                        'total_records': len(df),
                        'avg_rate': df['cleaning_rate'].mean(),
                        'min_rate': df['cleaning_rate'].min(),
                        'max_rate': df['cleaning_rate'].max()
                    }
                })
            else:
                return jsonify({'error': 'Error procesando datos CSV'}), 400
        else:
            return jsonify({'error': 'Formato de archivo no soportado'}), 400
            
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500

@app.route('/create_sample', methods=['POST'])
def create_sample_data():
    """Crear datos de muestra"""
    try:
        n_samples = int(request.json.get('n_samples', 100))
        
        # Crear datos de muestra
        df = uploader.create_sample_data(n_samples)
        
        # Entrenar modelo
        metrics = uploader.train_with_real_data(df)
        
        return jsonify({
            'success': True,
            'message': f'Datos de muestra creados ({n_samples} registros)',
            'metrics': metrics,
            'data_summary': {
                'total_records': len(df),
                'avg_rate': df['cleaning_rate'].mean(),
                'min_rate': df['cleaning_rate'].min(),
                'max_rate': df['cleaning_rate'].max()
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500

@app.route('/download_template')
def download_template():
    """Descargar template CSV"""
    try:
        # Crear template con datos de muestra
        df = uploader.create_sample_data(10)
        template_file = 'template_data.csv'
        df.to_csv(template_file, index=False)
        
        return jsonify({
            'success': True,
            'template_file': template_file,
            'message': 'Template CSV creado'
        })
        
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500

@app.route('/predict', methods=['POST'])
def predict():
    """Hacer predicción con modelo entrenado"""
    try:
        data = request.get_json()
        
        # Validar datos
        required_fields = ['sqft', 'bedrooms', 'bathrooms', 'property_type', 
                          'state', 'city_type', 'cleaning_type', 'frequency']
        
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo requerido: {field}'}), 400
        
        # Convertir tipos
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
        
        # Hacer predicción
        prediction = uploader.predictor.predict(property_data)
        
        return jsonify({
            'success': True,
            'prediction': prediction
        })
        
    except Exception as e:
        return jsonify({'error': f'Error en predicción: {str(e)}'}), 500

@app.route('/model_info')
def model_info():
    """Información del modelo actual"""
    try:
        if uploader.real_data is not None:
            return jsonify({
                'success': True,
                'model_type': 'real_data',
                'data_summary': {
                    'total_records': len(uploader.real_data),
                    'avg_rate': uploader.real_data['cleaning_rate'].mean(),
                    'states': uploader.real_data['state'].unique().tolist(),
                    'property_types': uploader.real_data['property_type'].unique().tolist()
                }
            })
        else:
            return jsonify({
                'success': True,
                'model_type': 'synthetic',
                'message': 'Modelo con datos sintéticos'
            })
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
