"""
Aplicación web para subir archivos Excel
"""

from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import os
import json
from excel_uploader import ExcelUploader
from cleaning_rate_predictor import CleaningRatePredictor

app = Flask(__name__)

# Inicializar uploader
uploader = ExcelUploader()

@app.route('/')
def index():
    return render_template('excel_upload.html')

@app.route('/upload_excel', methods=['POST'])
def upload_excel():
    """Cargar datos desde archivo Excel"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No se seleccionó archivo'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No se seleccionó archivo'}), 400
        
        # Verificar extensión
        if not (file.filename.endswith('.xlsx') or file.filename.endswith('.xls')):
            return jsonify({'error': 'Formato de archivo no soportado. Use .xlsx o .xls'}), 400
        
        # Guardar archivo temporalmente
        file_path = 'temp_data.xlsx'
        file.save(file_path)
        
        # Cargar datos
        df = uploader.load_excel_data(file_path)
        
        if df is not None:
            # Entrenar modelo con datos reales
            metrics = uploader.train_with_excel_data(df)
            
            # Limpiar archivo temporal
            os.remove(file_path)
            
            return jsonify({
                'success': True,
                'message': 'Datos de Excel cargados y modelo entrenado exitosamente',
                'metrics': metrics,
                'data_summary': {
                    'total_records': len(df),
                    'avg_rate': df['cleaning_rate'].mean(),
                    'min_rate': df['cleaning_rate'].min(),
                    'max_rate': df['cleaning_rate'].max(),
                    'states': df['state'].unique().tolist() if 'state' in df.columns else [],
                    'property_types': df['property_type'].unique().tolist() if 'property_type' in df.columns else []
                }
            })
        else:
            return jsonify({'error': 'Error procesando archivo Excel'}), 400
            
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500

@app.route('/download_template')
def download_template():
    """Descargar template Excel"""
    try:
        # Crear datos de muestra
        sample_data = uploader.create_sample_data(20)
        
        # Exportar a Excel
        template_file = 'template_cleaning_data.xlsx'
        uploader.export_to_excel(template_file)
        
        return send_file(template_file, as_attachment=True, 
                        download_name='template_cleaning_data.xlsx')
        
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
                'model_type': 'excel_data',
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

@app.route('/export_data')
def export_data():
    """Exportar datos procesados a Excel"""
    try:
        if uploader.real_data is None:
            return jsonify({'error': 'No hay datos para exportar'}), 400
        
        # Exportar datos
        export_file = 'processed_cleaning_data.xlsx'
        uploader.export_to_excel(export_file)
        
        return send_file(export_file, as_attachment=True, 
                        download_name='processed_cleaning_data.xlsx')
        
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
