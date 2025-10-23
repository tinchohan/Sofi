import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import json
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

class CleaningRatePredictor:
    """
    Modelo para predecir tarifas de limpieza de propiedades en Estados Unidos
    """
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_columns = []
        self.market_data = self._load_market_data()
        
    def _load_market_data(self) -> Dict:
        """Carga datos de mercado por estado/ciudad"""
        return {
            # Datos de costo de vida por estado (índice base 100 = promedio nacional)
            'state_cost_index': {
                'CA': 151.7, 'NY': 139.1, 'HI': 165.9, 'DC': 158.1, 'MA': 131.4,
                'CT': 128.0, 'AK': 125.8, 'MD': 124.0, 'NJ': 120.4, 'WA': 118.9,
                'CO': 115.8, 'OR': 115.6, 'VT': 115.2, 'NH': 114.9, 'RI': 114.3,
                'IL': 113.2, 'DE': 112.8, 'VA': 111.8, 'MN': 111.6, 'UT': 110.8,
                'TX': 93.9, 'FL': 98.3, 'GA': 90.4, 'NC': 95.1, 'TN': 89.4,
                'OH': 95.0, 'PA': 99.1, 'MI': 90.1, 'IN': 88.9, 'WI': 95.7,
                'MO': 89.8, 'KY': 88.1, 'AL': 85.8, 'SC': 88.9, 'LA': 89.1,
                'MS': 82.8, 'AR': 84.1, 'OK': 87.4, 'KS': 88.1, 'NE': 90.8,
                'IA': 89.4, 'ND': 94.1, 'SD': 88.9, 'MT': 95.1, 'WY': 92.8,
                'ID': 95.4, 'NV': 108.1, 'AZ': 105.1, 'NM': 92.8, 'UT': 110.8
            },
            # Factores de mercado por tipo de ciudad
            'city_type_multiplier': {
                'major_metro': 1.3,  # NYC, LA, Chicago, etc.
                'large_city': 1.15,  # Ciudades > 500k habitantes
                'medium_city': 1.0,   # Ciudades 100k-500k
                'small_city': 0.9,   # Ciudades < 100k
                'rural': 0.8         # Áreas rurales
            }
        }
    
    def _generate_synthetic_data(self, n_samples: int = 10000) -> pd.DataFrame:
        """Genera datos sintéticos para entrenar el modelo"""
        np.random.seed(42)
        
        data = []
        
        for _ in range(n_samples):
            # Factores de la propiedad
            sqft = np.random.normal(2000, 800)  # Metros cuadrados
            sqft = max(500, min(8000, sqft))    # Límites realistas
            
            bedrooms = np.random.poisson(3)
            bedrooms = max(1, min(8, bedrooms))
            
            bathrooms = bedrooms * np.random.uniform(0.8, 1.2)
            bathrooms = max(1, min(8, round(bathrooms, 1)))
            
            property_type = np.random.choice(['house', 'apartment', 'condo'], 
                                           p=[0.6, 0.3, 0.1])
            
            # Factores de mercado
            state = np.random.choice(list(self.market_data['state_cost_index'].keys()))
            city_type = np.random.choice(['major_metro', 'large_city', 'medium_city', 
                                        'small_city', 'rural'], 
                                       p=[0.1, 0.2, 0.3, 0.3, 0.1])
            
            # Factores del servicio
            cleaning_type = np.random.choice(['basic', 'deep', 'post_construction'], 
                                           p=[0.7, 0.25, 0.05])
            frequency = np.random.choice(['one_time', 'weekly', 'monthly'], 
                                       p=[0.4, 0.4, 0.2])
            
            # Cálculo de tarifa base
            base_rate = self._calculate_base_rate(
                sqft, bedrooms, bathrooms, property_type, 
                state, city_type, cleaning_type, frequency
            )
            
            # Añadir variabilidad realista
            noise = np.random.normal(0, base_rate * 0.1)
            final_rate = max(50, base_rate + noise)  # Mínimo $50
            
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
        
        return pd.DataFrame(data)
    
    def _calculate_base_rate(self, sqft, bedrooms, bathrooms, property_type, 
                           state, city_type, cleaning_type, frequency) -> float:
        """Calcula tarifa base usando reglas de negocio"""
        
        # Tarifa base por metro cuadrado
        base_per_sqft = 0.15  # $0.15 por sqft
        
        # Multiplicadores por tipo de propiedad
        property_multipliers = {
            'house': 1.0,
            'apartment': 0.9,
            'condo': 0.95
        }
        
        # Multiplicadores por tipo de limpieza
        cleaning_multipliers = {
            'basic': 1.0,
            'deep': 1.5,
            'post_construction': 2.0
        }
        
        # Multiplicadores por frecuencia
        frequency_multipliers = {
            'one_time': 1.0,
            'weekly': 0.8,
            'monthly': 0.9
        }
        
        # Factor de complejidad por habitaciones/baños
        complexity_factor = 1 + (bedrooms * 0.05) + (bathrooms * 0.1)
        
        # Cálculo final
        base_rate = (sqft * base_per_sqft * 
                    property_multipliers[property_type] *
                    cleaning_multipliers[cleaning_type] *
                    frequency_multipliers[frequency] *
                    complexity_factor *
                    (self.market_data['state_cost_index'][state] / 100) *
                    self.market_data['city_type_multiplier'][city_type])
        
        return base_rate
    
    def prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Prepara las características para el modelo"""
        df_processed = df.copy()
        
        # Codificar variables categóricas
        categorical_columns = ['property_type', 'state', 'city_type', 'cleaning_type', 'frequency']
        
        for col in categorical_columns:
            if col not in self.label_encoders:
                self.label_encoders[col] = LabelEncoder()
                df_processed[col] = self.label_encoders[col].fit_transform(df_processed[col])
            else:
                df_processed[col] = self.label_encoders[col].transform(df_processed[col])
        
        # Crear características adicionales
        df_processed['sqft_per_room'] = df_processed['sqft'] / df_processed['bedrooms']
        df_processed['bathroom_ratio'] = df_processed['bathrooms'] / df_processed['bedrooms']
        df_processed['total_rooms'] = df_processed['bedrooms'] + df_processed['bathrooms']
        
        self.feature_columns = [col for col in df_processed.columns if col != 'cleaning_rate']
        
        return df_processed
    
    def train(self, df: pd.DataFrame = None):
        """Entrena el modelo"""
        if df is None:
            print("Generando datos sintéticos para entrenamiento...")
            df = self._generate_synthetic_data()
        
        # Preparar datos
        df_processed = self.prepare_features(df)
        
        # Separar características y objetivo
        X = df_processed[self.feature_columns]
        y = df_processed['cleaning_rate']
        
        # Dividir datos
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Escalar características
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Entrenar modelo (usando Gradient Boosting para mejor rendimiento)
        self.model = GradientBoostingRegressor(
            n_estimators=200,
            learning_rate=0.1,
            max_depth=6,
            random_state=42
        )
        
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluar modelo
        y_pred = self.model.predict(X_test_scaled)
        
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        print(f"Modelo entrenado exitosamente!")
        print(f"MAE: ${mae:.2f}")
        print(f"RMSE: ${np.sqrt(mse):.2f}")
        print(f"R²: {r2:.3f}")
        
        return {
            'mae': mae,
            'rmse': np.sqrt(mse),
            'r2': r2
        }
    
    def predict(self, property_data: Dict) -> Dict:
        """Predice la tarifa de limpieza para una propiedad"""
        if self.model is None:
            raise ValueError("El modelo debe ser entrenado primero")
        
        # Crear DataFrame con los datos de entrada
        df_input = pd.DataFrame([property_data])
        
        # Preparar características
        df_processed = self.prepare_features(df_input)
        X = df_processed[self.feature_columns]
        
        # Escalar características
        X_scaled = self.scaler.transform(X)
        
        # Hacer predicción
        prediction = self.model.predict(X_scaled)[0]
        
        # Calcular intervalo de confianza (aproximado)
        # Usar desviación estándar de las predicciones del conjunto de entrenamiento
        confidence_interval = prediction * 0.15  # ±15% como aproximación
        
        return {
            'predicted_rate': round(prediction, 2),
            'confidence_interval': {
                'lower': round(prediction - confidence_interval, 2),
                'upper': round(prediction + confidence_interval, 2)
            },
            'factors_considered': {
                'property_size': property_data.get('sqft', 0),
                'bedrooms': property_data.get('bedrooms', 0),
                'bathrooms': property_data.get('bathrooms', 0),
                'property_type': property_data.get('property_type', 'house'),
                'location': f"{property_data.get('state', 'Unknown')} - {property_data.get('city_type', 'medium_city')}",
                'cleaning_type': property_data.get('cleaning_type', 'basic'),
                'frequency': property_data.get('frequency', 'one_time')
            }
        }
    
    def save_model(self, filepath: str):
        """Guarda el modelo entrenado"""
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'label_encoders': self.label_encoders,
            'feature_columns': self.feature_columns,
            'market_data': self.market_data
        }
        joblib.dump(model_data, filepath)
        print(f"Modelo guardado en {filepath}")
    
    def load_model(self, filepath: str):
        """Carga un modelo previamente entrenado"""
        model_data = joblib.load(filepath)
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.label_encoders = model_data['label_encoders']
        self.feature_columns = model_data['feature_columns']
        self.market_data = model_data['market_data']
        print(f"Modelo cargado desde {filepath}")

# Ejemplo de uso
if __name__ == "__main__":
    # Crear y entrenar el modelo
    predictor = CleaningRatePredictor()
    
    # Entrenar con datos sintéticos
    metrics = predictor.train()
    
    # Ejemplo de predicción
    property_example = {
        'sqft': 2500,
        'bedrooms': 4,
        'bathrooms': 3,
        'property_type': 'house',
        'state': 'CA',
        'city_type': 'large_city',
        'cleaning_type': 'deep',
        'frequency': 'one_time'
    }
    
    prediction = predictor.predict(property_example)
    
    print("\n" + "="*50)
    print("PREDICCIÓN DE TARIFA DE LIMPIEZA")
    print("="*50)
    print(f"Tarifa estimada: ${prediction['predicted_rate']}")
    print(f"Rango de confianza: ${prediction['confidence_interval']['lower']} - ${prediction['confidence_interval']['upper']}")
    print("\nFactores considerados:")
    for factor, value in prediction['factors_considered'].items():
        print(f"  {factor}: {value}")
    
    # Guardar modelo
    predictor.save_model('cleaning_rate_model.pkl')
