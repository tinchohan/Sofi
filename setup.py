#!/usr/bin/env python3
"""
Script de instalación y configuración para el modelo de predicción de tarifas de limpieza
"""

import subprocess
import sys
import os

def install_requirements():
    """Instala las dependencias necesarias"""
    print("🔧 Instalando dependencias...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        return False

def test_model():
    """Prueba el modelo básico"""
    print("\n🧪 Probando el modelo...")
    try:
        from cleaning_rate_predictor import CleaningRatePredictor
        
        predictor = CleaningRatePredictor()
        predictor.train()
        
        # Prueba básica
        test_data = {
            'sqft': 2000,
            'bedrooms': 3,
            'bathrooms': 2,
            'property_type': 'house',
            'state': 'CA',
            'city_type': 'medium_city',
            'cleaning_type': 'basic',
            'frequency': 'one_time'
        }
        
        prediction = predictor.predict(test_data)
        print(f"✅ Modelo funcionando correctamente")
        print(f"   Predicción de prueba: ${prediction['predicted_rate']}")
        return True
        
    except Exception as e:
        print(f"❌ Error probando el modelo: {e}")
        return False

def create_directories():
    """Crea directorios necesarios"""
    print("📁 Creando directorios...")
    directories = ['templates', 'static', 'models']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"   ✓ Creado directorio: {directory}")
        else:
            print(f"   ✓ Directorio ya existe: {directory}")

def show_usage():
    """Muestra instrucciones de uso"""
    print("\n" + "="*60)
    print("🚀 INSTALACIÓN COMPLETADA")
    print("="*60)
    print("""
    📋 PRÓXIMOS PASOS:
    
    1. 🧪 PROBAR EL MODELO:
       python demo.py
    
    2. 🌐 INICIAR APLICACIÓN WEB:
       python app.py
       Luego abrir: http://localhost:5000
    
    3. 📊 USAR EL MODELO PROGRAMÁTICAMENTE:
       from cleaning_rate_predictor import CleaningRatePredictor
       predictor = CleaningRatePredictor()
       predictor.load_model('cleaning_rate_model.pkl')
       prediction = predictor.predict(your_data)
    
    📁 ARCHIVOS CREADOS:
    • cleaning_rate_predictor.py  - Modelo de ML
    • app.py                      - Aplicación web Flask
    • templates/index.html        - Interfaz web
    • demo.py                     - Demo del modelo
    • config.py                   - Configuración
    • requirements.txt            - Dependencias
    • README.md                   - Documentación
    
    🔧 PERSONALIZACIÓN:
    • Editar config.py para ajustar parámetros
    • Modificar cleaning_rate_predictor.py para el modelo
    • Actualizar templates/index.html para la interfaz
    """)

def main():
    """Función principal de instalación"""
    print("🏠 CONFIGURANDO CALCULADORA DE TARIFAS DE LIMPIEZA")
    print("="*60)
    
    # Crear directorios
    create_directories()
    
    # Instalar dependencias
    if not install_requirements():
        print("❌ No se pudieron instalar las dependencias")
        return False
    
    # Probar modelo
    if not test_model():
        print("❌ El modelo no funciona correctamente")
        return False
    
    # Mostrar instrucciones
    show_usage()
    
    print("\n🎉 ¡Instalación completada exitosamente!")
    return True

if __name__ == "__main__":
    main()
