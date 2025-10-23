#!/usr/bin/env python3
"""
Ejemplos de uso del modelo de predicción de tarifas de limpieza
"""

from cleaning_rate_predictor import CleaningRatePredictor
import json

def example_basic_usage():
    """Ejemplo básico de uso del modelo"""
    print("="*60)
    print("EJEMPLO 1: USO BÁSICO")
    print("="*60)
    
    # Inicializar predictor
    predictor = CleaningRatePredictor()
    
    # Cargar modelo entrenado
    try:
        predictor.load_model('cleaning_rate_model.pkl')
        print("✓ Modelo cargado exitosamente")
    except:
        print("⚠ Entrenando nuevo modelo...")
        predictor.train()
        predictor.save_model('cleaning_rate_model.pkl')
    
    # Datos de una propiedad
    property_data = {
        'sqft': 2500,
        'bedrooms': 4,
        'bathrooms': 3,
        'property_type': 'house',
        'state': 'CA',
        'city_type': 'large_city',
        'cleaning_type': 'deep',
        'frequency': 'one_time'
    }
    
    # Hacer predicción
    prediction = predictor.predict(property_data)
    
    print(f"\n📊 RESULTADO:")
    print(f"   Tarifa estimada: ${prediction['predicted_rate']}")
    print(f"   Rango: ${prediction['confidence_interval']['lower']} - ${prediction['confidence_interval']['upper']}")

def example_batch_predictions():
    """Ejemplo de predicciones en lote"""
    print("\n" + "="*60)
    print("EJEMPLO 2: PREDICCIONES EN LOTE")
    print("="*60)
    
    predictor = CleaningRatePredictor()
    predictor.load_model('cleaning_rate_model.pkl')
    
    # Múltiples propiedades
    properties = [
        {
            'name': 'Casa en Miami',
            'data': {
                'sqft': 2000, 'bedrooms': 3, 'bathrooms': 2,
                'property_type': 'house', 'state': 'FL', 'city_type': 'large_city',
                'cleaning_type': 'basic', 'frequency': 'weekly'
            }
        },
        {
            'name': 'Apartamento en Seattle',
            'data': {
                'sqft': 1200, 'bedrooms': 2, 'bathrooms': 1,
                'property_type': 'apartment', 'state': 'WA', 'city_type': 'large_city',
                'cleaning_type': 'deep', 'frequency': 'monthly'
            }
        },
        {
            'name': 'Casa en Austin',
            'data': {
                'sqft': 3000, 'bedrooms': 4, 'bathrooms': 3,
                'property_type': 'house', 'state': 'TX', 'city_type': 'medium_city',
                'cleaning_type': 'post_construction', 'frequency': 'one_time'
            }
        }
    ]
    
    results = []
    for prop in properties:
        prediction = predictor.predict(prop['data'])
        results.append({
            'property': prop['name'],
            'rate': prediction['predicted_rate'],
            'range': prediction['confidence_interval']
        })
    
    print("📊 RESULTADOS:")
    for result in results:
        print(f"   {result['property']}: ${result['rate']} (${result['range']['lower']}-${result['range']['upper']})")

def example_api_integration():
    """Ejemplo de integración con API"""
    print("\n" + "="*60)
    print("EJEMPLO 3: INTEGRACIÓN CON API")
    print("="*60)
    
    # Simular datos de API
    api_data = {
        "properties": [
            {
                "id": "prop_001",
                "address": "123 Main St, Los Angeles, CA",
                "sqft": 2500,
                "bedrooms": 4,
                "bathrooms": 3,
                "property_type": "house",
                "state": "CA",
                "city_type": "major_metro",
                "cleaning_type": "deep",
                "frequency": "one_time"
            },
            {
                "id": "prop_002", 
                "address": "456 Oak Ave, Dallas, TX",
                "sqft": 1800,
                "bedrooms": 3,
                "bathrooms": 2,
                "property_type": "house",
                "state": "TX",
                "city_type": "large_city",
                "cleaning_type": "basic",
                "frequency": "weekly"
            }
        ]
    }
    
    predictor = CleaningRatePredictor()
    predictor.load_model('cleaning_rate_model.pkl')
    
    # Procesar cada propiedad
    api_results = []
    for prop in api_data["properties"]:
        # Extraer datos necesarios para el modelo
        model_data = {
            'sqft': prop['sqft'],
            'bedrooms': prop['bedrooms'],
            'bathrooms': prop['bathrooms'],
            'property_type': prop['property_type'],
            'state': prop['state'],
            'city_type': prop['city_type'],
            'cleaning_type': prop['cleaning_type'],
            'frequency': prop['frequency']
        }
        
        # Hacer predicción
        prediction = predictor.predict(model_data)
        
        # Formatear resultado para API
        api_results.append({
            "property_id": prop['id'],
            "address": prop['address'],
            "estimated_rate": prediction['predicted_rate'],
            "confidence_interval": prediction['confidence_interval'],
            "factors": prediction['factors_considered']
        })
    
    print("📊 RESULTADOS DE API:")
    for result in api_results:
        print(f"   {result['property_id']}: {result['address']}")
        print(f"      Tarifa: ${result['estimated_rate']}")
        print(f"      Rango: ${result['confidence_interval']['lower']}-${result['confidence_interval']['upper']}")
        print()

def example_custom_training():
    """Ejemplo de entrenamiento personalizado"""
    print("\n" + "="*60)
    print("EJEMPLO 4: ENTRENAMIENTO PERSONALIZADO")
    print("="*60)
    
    # Crear predictor personalizado
    predictor = CleaningRatePredictor()
    
    # Entrenar con parámetros personalizados
    print("🔧 Entrenando modelo personalizado...")
    metrics = predictor.train()
    
    print(f"📊 MÉTRICAS DEL MODELO:")
    print(f"   MAE: ${metrics['mae']:.2f}")
    print(f"   RMSE: ${metrics['rmse']:.2f}")
    print(f"   R²: {metrics['r2']:.3f}")
    
    # Guardar modelo personalizado
    predictor.save_model('custom_cleaning_model.pkl')
    print("💾 Modelo personalizado guardado")

def example_data_analysis():
    """Ejemplo de análisis de datos"""
    print("\n" + "="*60)
    print("EJEMPLO 5: ANÁLISIS DE DATOS")
    print("="*60)
    
    predictor = CleaningRatePredictor()
    
    # Generar datos para análisis
    import pandas as pd
    data = predictor._generate_synthetic_data(1000)
    
    print("📊 ESTADÍSTICAS DE LOS DATOS:")
    print(f"   Total de propiedades: {len(data)}")
    print(f"   Tamaño promedio: {data['sqft'].mean():.0f} m²")
    print(f"   Habitaciones promedio: {data['bedrooms'].mean():.1f}")
    print(f"   Baños promedio: {data['bathrooms'].mean():.1f}")
    print(f"   Tarifa promedio: ${data['cleaning_rate'].mean():.2f}")
    print(f"   Tarifa mínima: ${data['cleaning_rate'].min():.2f}")
    print(f"   Tarifa máxima: ${data['cleaning_rate'].max():.2f}")
    
    # Análisis por estado
    print("\n📈 ANÁLISIS POR ESTADO:")
    state_analysis = data.groupby('state')['cleaning_rate'].agg(['mean', 'count']).round(2)
    state_analysis = state_analysis.sort_values('mean', ascending=False)
    print(state_analysis.head(10))
    
    # Análisis por tipo de limpieza
    print("\n🧽 ANÁLISIS POR TIPO DE LIMPIEZA:")
    cleaning_analysis = data.groupby('cleaning_type')['cleaning_rate'].agg(['mean', 'count']).round(2)
    print(cleaning_analysis)

def main():
    """Ejecutar todos los ejemplos"""
    print("🏠 EJEMPLOS DE USO - CALCULADORA DE TARIFAS DE LIMPIEZA")
    print("="*80)
    
    try:
        example_basic_usage()
        example_batch_predictions()
        example_api_integration()
        example_custom_training()
        example_data_analysis()
        
        print("\n" + "="*80)
        print("✅ TODOS LOS EJEMPLOS COMPLETADOS EXITOSAMENTE")
        print("="*80)
        print("""
        🚀 PRÓXIMOS PASOS:
        
        1. 🌐 Usar la aplicación web: python app.py
        2. 📊 Integrar en tu aplicación existente
        3. 🔧 Personalizar el modelo según tus necesidades
        4. 📈 Añadir más datos reales para mejorar precisión
        
        💡 CONSEJOS:
        • El modelo funciona mejor con datos reales
        • Puedes ajustar parámetros en config.py
        • Considera añadir factores estacionales
        • Implementa validación de datos en producción
        """)
        
    except Exception as e:
        print(f"❌ Error ejecutando ejemplos: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
