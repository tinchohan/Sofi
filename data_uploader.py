#!/usr/bin/env python3
"""
Sistema para cargar y usar datos reales de tarifas de limpieza
"""

import pandas as pd
import numpy as np
from cleaning_rate_predictor import CleaningRatePredictor
import json
from typing import Dict, List, Optional

class DataUploader:
    """
    Clase para manejar datos reales de tarifas de limpieza
    """
    
    def __init__(self):
        self.predictor = CleaningRatePredictor()
        self.real_data = None
        
    def load_csv_data(self, file_path: str) -> pd.DataFrame:
        """
        Carga datos desde un archivo CSV
        
        Formato esperado del CSV:
        sqft,bedrooms,bathrooms,property_type,state,city_type,cleaning_type,frequency,cleaning_rate
        """
        try:
            df = pd.read_csv(file_path)
            
            # Validar columnas requeridas
            required_columns = [
                'sqft', 'bedrooms', 'bathrooms', 'property_type', 
                'state', 'city_type', 'cleaning_type', 'frequency', 'cleaning_rate'
            ]
            
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Columnas faltantes: {missing_columns}")
            
            # Validar tipos de datos
            df['sqft'] = pd.to_numeric(df['sqft'], errors='coerce')
            df['bedrooms'] = pd.to_numeric(df['bedrooms'], errors='coerce')
            df['bathrooms'] = pd.to_numeric(df['bathrooms'], errors='coerce')
            df['cleaning_rate'] = pd.to_numeric(df['cleaning_rate'], errors='coerce')
            
            # Eliminar filas con datos faltantes
            df = df.dropna()
            
            print(f"✅ Datos cargados: {len(df)} registros")
            print(f"📊 Rango de tarifas: ${df['cleaning_rate'].min():.2f} - ${df['cleaning_rate'].max():.2f}")
            print(f"📈 Tarifa promedio: ${df['cleaning_rate'].mean():.2f}")
            
            self.real_data = df
            return df
            
        except Exception as e:
            print(f"❌ Error cargando datos: {e}")
            return None
    
    def create_sample_data(self, n_samples: int = 100) -> pd.DataFrame:
        """
        Crea datos de muestra basados en patrones reales
        """
        print("📝 Creando datos de muestra...")
        
        # Patrones reales de tarifas por estado
        state_rates = {
            'CA': {'base': 0.20, 'min': 150, 'max': 800},
            'NY': {'base': 0.18, 'min': 120, 'max': 700},
            'TX': {'base': 0.12, 'min': 80, 'max': 400},
            'FL': {'base': 0.15, 'min': 100, 'max': 500},
            'WA': {'base': 0.16, 'min': 110, 'max': 600}
        }
        
        data = []
        
        for _ in range(n_samples):
            # Seleccionar estado
            state = np.random.choice(list(state_rates.keys()))
            state_info = state_rates[state]
            
            # Generar datos de propiedad
            sqft = np.random.normal(2000, 800)
            sqft = max(500, min(8000, sqft))
            
            bedrooms = np.random.poisson(3)
            bedrooms = max(1, min(8, bedrooms))
            
            bathrooms = bedrooms * np.random.uniform(0.8, 1.2)
            bathrooms = max(1, min(8, round(bathrooms, 1)))
            
            property_type = np.random.choice(['house', 'apartment', 'condo'], 
                                           p=[0.6, 0.3, 0.1])
            
            city_type = np.random.choice(['major_metro', 'large_city', 'medium_city', 
                                        'small_city', 'rural'], 
                                       p=[0.1, 0.2, 0.3, 0.3, 0.1])
            
            cleaning_type = np.random.choice(['basic', 'deep', 'post_construction'], 
                                           p=[0.7, 0.25, 0.05])
            
            frequency = np.random.choice(['one_time', 'weekly', 'monthly'], 
                                       p=[0.4, 0.4, 0.2])
            
            # Calcular tarifa basada en patrones reales
            base_rate = sqft * state_info['base']
            
            # Multiplicadores
            multipliers = {
                'house': 1.0, 'apartment': 0.9, 'condo': 0.95
            }
            
            cleaning_multipliers = {
                'basic': 1.0, 'deep': 1.5, 'post_construction': 2.0
            }
            
            frequency_multipliers = {
                'one_time': 1.0, 'weekly': 0.8, 'monthly': 0.9
            }
            
            city_multipliers = {
                'major_metro': 1.3, 'large_city': 1.15, 'medium_city': 1.0,
                'small_city': 0.9, 'rural': 0.8
            }
            
            final_rate = (base_rate * 
                         multipliers[property_type] *
                         cleaning_multipliers[cleaning_type] *
                         frequency_multipliers[frequency] *
                         city_multipliers[city_type])
            
            # Añadir variabilidad realista
            final_rate *= np.random.uniform(0.8, 1.2)
            final_rate = max(state_info['min'], min(state_info['max'], final_rate))
            
            data.append({
                'sqft': sqft,
                'bedrooms': bedrooms,
                'bathrooms': bathrooms,
                'property_type': property_type,
                'state': state,
                'city_type': city_type,
                'cleaning_type': cleaning_type,
                'frequency': frequency,
                'cleaning_rate': final_rate
            })
        
        df = pd.DataFrame(data)
        self.real_data = df
        return df
    
    def train_with_real_data(self, df: pd.DataFrame = None) -> Dict:
        """
        Entrena el modelo con datos reales
        """
        if df is None:
            if self.real_data is None:
                raise ValueError("No hay datos cargados")
            df = self.real_data
        
        print("🤖 Entrenando modelo con datos reales...")
        
        # Entrenar modelo
        metrics = self.predictor.train(df)
        
        # Guardar modelo
        self.predictor.save_model('real_data_model.pkl')
        
        print("✅ Modelo entrenado con datos reales")
        print(f"📊 Precisión: R² = {metrics['r2']:.3f}")
        print(f"📈 Error promedio: ${metrics['mae']:.2f}")
        
        return metrics
    
    def compare_predictions(self, test_data: Dict) -> Dict:
        """
        Compara predicciones entre modelo sintético y modelo real
        """
        # Cargar modelo original
        original_predictor = CleaningRatePredictor()
        try:
            original_predictor.load_model('cleaning_rate_model.pkl')
        except:
            print("⚠️ Modelo original no encontrado")
            return None
        
        # Predicciones
        original_pred = original_predictor.predict(test_data)
        real_pred = self.predictor.predict(test_data)
        
        return {
            'original_model': original_pred,
            'real_data_model': real_pred,
            'difference': abs(original_pred['predicted_rate'] - real_pred['predicted_rate']),
            'improvement': 'real_data_model' if real_pred['predicted_rate'] > original_pred['predicted_rate'] else 'original_model'
        }
    
    def export_sample_csv(self, filename: str = 'sample_cleaning_data.csv'):
        """
        Exporta datos de muestra a CSV
        """
        if self.real_data is None:
            self.create_sample_data(100)
        
        self.real_data.to_csv(filename, index=False)
        print(f"📁 Datos exportados a {filename}")
        
        return filename

def main():
    """
    Función principal para demostrar el uso
    """
    print("🏠 SISTEMA DE CARGA DE DATOS REALES")
    print("="*50)
    
    uploader = DataUploader()
    
    # Crear datos de muestra
    print("\n1. Creando datos de muestra...")
    sample_data = uploader.create_sample_data(200)
    
    # Exportar CSV de muestra
    print("\n2. Exportando CSV de muestra...")
    csv_file = uploader.export_sample_csv('sample_cleaning_data.csv')
    
    # Entrenar con datos reales
    print("\n3. Entrenando modelo con datos reales...")
    metrics = uploader.train_with_real_data()
    
    # Ejemplo de comparación
    print("\n4. Comparando predicciones...")
    test_property = {
        'sqft': 2500,
        'bedrooms': 4,
        'bathrooms': 3,
        'property_type': 'house',
        'state': 'CA',
        'city_type': 'large_city',
        'cleaning_type': 'deep',
        'frequency': 'one_time'
    }
    
    comparison = uploader.compare_predictions(test_property)
    if comparison:
        print(f"   Modelo original: ${comparison['original_model']['predicted_rate']:.2f}")
        print(f"   Modelo con datos reales: ${comparison['real_data_model']['predicted_rate']:.2f}")
        print(f"   Diferencia: ${comparison['difference']:.2f}")
    
    print("\n✅ Sistema de datos reales configurado")
    print(f"📁 Archivo CSV creado: {csv_file}")
    print("💡 Puedes editar el CSV y cargar tus propios datos")

if __name__ == "__main__":
    main()
