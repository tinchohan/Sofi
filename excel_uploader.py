#!/usr/bin/env python3
"""
Sistema para cargar datos desde archivos Excel
"""

import pandas as pd
import numpy as np
from cleaning_rate_predictor import CleaningRatePredictor
import json
import os
from typing import Dict, List, Optional

class ExcelUploader:
    """
    Clase para manejar datos desde archivos Excel
    """
    
    def __init__(self):
        self.predictor = CleaningRatePredictor()
        self.real_data = None
        
    def load_csv_data(self, file_path: str) -> pd.DataFrame:
        """
        Carga datos desde un archivo CSV
        """
        try:
            # Cargar CSV
            df = pd.read_csv(file_path)
            
            print(f"✅ Archivo CSV cargado: {len(df)} registros")
            print(f"📊 Columnas disponibles: {list(df.columns)}")
            
            # Mostrar primeras filas
            print("\n📋 Primeras 5 filas:")
            print(df.head())
            
            # Mapear columnas automáticamente
            df_mapped = self._map_columns(df)
            
            if df_mapped is not None:
                # Validar y limpiar datos
                df_clean = self._clean_data(df_mapped)
                self.real_data = df_clean
                return df_clean
            else:
                print("❌ No se pudieron mapear las columnas automáticamente")
                return None
                
        except Exception as e:
            print(f"❌ Error cargando CSV: {e}")
            return None

    def load_excel_data(self, file_path: str, sheet_name: str = None) -> pd.DataFrame:
        """
        Carga datos desde un archivo Excel
        
        Parámetros:
        - file_path: Ruta del archivo Excel
        - sheet_name: Nombre de la hoja (opcional)
        """
        try:
            # Cargar Excel
            if sheet_name:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
            else:
                df = pd.read_excel(file_path)
            
            print(f"✅ Archivo Excel cargado: {len(df)} registros")
            print(f"📊 Columnas disponibles: {list(df.columns)}")
            
            # Mostrar primeras filas
            print("\n📋 Primeras 5 filas:")
            print(df.head())
            
            # Mapear columnas automáticamente
            df_mapped = self._map_columns(df)
            
            if df_mapped is not None:
                # Validar y limpiar datos
                df_clean = self._clean_data(df_mapped)
                self.real_data = df_clean
                return df_clean
            else:
                print("❌ No se pudieron mapear las columnas automáticamente")
                return None
                
        except Exception as e:
            print(f"❌ Error cargando Excel: {e}")
            return None
    
    def _map_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Mapea automáticamente las columnas del Excel a las columnas requeridas
        """
        # Diccionario de mapeo de columnas comunes
        column_mapping = {
            # Metros cuadrados
            'sqft': ['sqft', 'sq_ft', 'square_feet', 'metros', 'm2', 'area', 'tamaño', 'property_square_footage', 'square_footage'],
            # Habitaciones
            'bedrooms': ['bedrooms', 'bed', 'dormitorios', 'habitaciones', 'rooms', 'property_bedrooms_count', 'bedrooms_count'],
            # Baños
            'bathrooms': ['bathrooms', 'bath', 'baños', 'bathroom', 'property_bathrooms_count', 'bathrooms_count'],
            # Tipo de propiedad
            'property_type': ['property_type', 'tipo', 'type', 'tipo_propiedad', 'property_room_type', 'room_type', 'property_asset_type', 'asset_type'],
            # Estado
            'state': ['state', 'estado', 'state_code', 'estado_codigo', 'property_state', 'property_state_code'],
            # Tipo de ciudad
            'city_type': ['city_type', 'tipo_ciudad', 'city', 'ciudad', 'property_city', 'property_sub_market', 'sub_market'],
            # Tipo de limpieza
            'cleaning_type': ['cleaning_type', 'tipo_limpieza', 'cleaning', 'limpieza'],
            # Frecuencia
            'frequency': ['frequency', 'frecuencia', 'freq'],
            # Tarifa
            'cleaning_rate': ['cleaning_rate', 'rate', 'tarifa', 'precio', 'costo', 'price', 'cost', 'cleaning_cost', 'service_rate']
        }
        
        # Buscar columnas que coincidan
        mapped_columns = {}
        for target_col, possible_names in column_mapping.items():
            for col in df.columns:
                if any(name.lower() in col.lower() for name in possible_names):
                    mapped_columns[target_col] = col
                    break
        
        print(f"\n🔍 Mapeo de columnas encontrado:")
        for target, source in mapped_columns.items():
            print(f"   {target} -> {source}")
        
        # Verificar si tenemos las columnas mínimas
        required_columns = ['sqft', 'bedrooms', 'bathrooms', 'cleaning_rate']
        missing_required = [col for col in required_columns if col not in mapped_columns]
        
        if missing_required:
            print(f"❌ Columnas requeridas faltantes: {missing_required}")
            print("💡 Sugerencias de nombres de columnas:")
            for col in missing_required:
                print(f"   {col}: {column_mapping[col]}")
            
            # Intentar mapear columnas que podrían ser útiles
            print("\n🔍 Columnas disponibles en tu archivo:")
            for col in df.columns:
                print(f"   - {col}")
            
            # Si falta cleaning_rate, sugerir crear una columna estimada
            if 'cleaning_rate' in missing_required:
                print("\n💡 SUGERENCIA: Tu archivo no tiene tarifas de limpieza.")
                print("   Puedo crear tarifas estimadas basadas en el tamaño y tipo de propiedad.")
                print("   ¿Quieres que genere tarifas estimadas? (Esto creará una columna 'cleaning_rate_estimated')")
                
                # Crear tarifas estimadas automáticamente
                df_mapped['cleaning_rate'] = self._estimate_cleaning_rates(df_mapped)
                print("✅ Tarifas estimadas creadas basadas en patrones del mercado")
                missing_required = [col for col in missing_required if col != 'cleaning_rate']
            
            # Si aún faltan columnas críticas, retornar None
            if missing_required:
                return None
        
        # Renombrar columnas
        df_mapped = df.rename(columns={v: k for k, v in mapped_columns.items()})
        
        # Añadir columnas faltantes con valores por defecto
        if 'property_type' not in mapped_columns:
            df_mapped['property_type'] = 'house'
            print("⚠️ Tipo de propiedad no encontrado, usando 'house' por defecto")
        
        if 'state' not in mapped_columns:
            df_mapped['state'] = 'CA'
            print("⚠️ Estado no encontrado, usando 'CA' por defecto")
        
        if 'city_type' not in mapped_columns:
            df_mapped['city_type'] = 'medium_city'
            print("⚠️ Tipo de ciudad no encontrado, usando 'medium_city' por defecto")
        
        if 'cleaning_type' not in mapped_columns:
            df_mapped['cleaning_type'] = 'basic'
            print("⚠️ Tipo de limpieza no encontrado, usando 'basic' por defecto")
        
        if 'frequency' not in mapped_columns:
            df_mapped['frequency'] = 'one_time'
            print("⚠️ Frecuencia no encontrada, usando 'one_time' por defecto")
        
        return df_mapped
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Limpia y valida los datos
        """
        print("\n🧹 Limpiando datos...")
        
        # Convertir tipos de datos
        numeric_columns = ['sqft', 'bedrooms', 'bathrooms', 'cleaning_rate']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Eliminar filas con datos faltantes en columnas críticas
        critical_columns = ['sqft', 'bedrooms', 'bathrooms', 'cleaning_rate']
        df_clean = df.dropna(subset=critical_columns)
        
        # Validar rangos
        df_clean = df_clean[
            (df_clean['sqft'] > 0) & (df_clean['sqft'] <= 50000) &
            (df_clean['bedrooms'] > 0) & (df_clean['bedrooms'] <= 20) &
            (df_clean['bathrooms'] > 0) & (df_clean['bathrooms'] <= 20) &
            (df_clean['cleaning_rate'] > 0) & (df_clean['cleaning_rate'] <= 10000)
        ]
        
        # Estandarizar valores categóricos
        if 'property_type' in df_clean.columns:
            df_clean['property_type'] = df_clean['property_type'].str.lower()
            df_clean['property_type'] = df_clean['property_type'].replace({
                'casa': 'house', 'apartamento': 'apartment', 'condominio': 'condo',
                'home': 'house', 'apt': 'apartment'
            })
        
        if 'cleaning_type' in df_clean.columns:
            df_clean['cleaning_type'] = df_clean['cleaning_type'].str.lower()
            df_clean['cleaning_type'] = df_clean['cleaning_type'].replace({
                'básica': 'basic', 'profunda': 'deep', 'post-construcción': 'post_construction',
                'post_construccion': 'post_construction', 'post_construcción': 'post_construction'
            })
        
        if 'frequency' in df_clean.columns:
            df_clean['frequency'] = df_clean['frequency'].str.lower()
            df_clean['frequency'] = df_clean['frequency'].replace({
                'una_vez': 'one_time', 'semanal': 'weekly', 'mensual': 'monthly',
                'una vez': 'one_time'
            })
        
        print(f"✅ Datos limpios: {len(df_clean)} registros")
        print(f"📊 Estadísticas:")
        print(f"   Tarifa promedio: ${df_clean['cleaning_rate'].mean():.2f}")
        print(f"   Tarifa mínima: ${df_clean['cleaning_rate'].min():.2f}")
        print(f"   Tarifa máxima: ${df_clean['cleaning_rate'].max():.2f}")
        
        return df_clean
    
    def _estimate_cleaning_rates(self, df: pd.DataFrame) -> pd.Series:
        """
        Estima tarifas de limpieza basadas en patrones del mercado
        """
        print("🧮 Estimando tarifas de limpieza...")
        
        # Patrones de tarifas por estado
        state_rates = {
            'CA': 0.20, 'NY': 0.18, 'TX': 0.12, 'FL': 0.15, 'WA': 0.16,
            'IL': 0.14, 'PA': 0.13, 'OH': 0.11, 'GA': 0.12, 'NC': 0.12,
            'MI': 0.11, 'NJ': 0.16, 'VA': 0.14, 'TN': 0.10, 'IN': 0.10,
            'MO': 0.10, 'MD': 0.15, 'WI': 0.11, 'CO': 0.15, 'MN': 0.13
        }
        
        # Multiplicadores por tipo de propiedad
        property_multipliers = {
            'house': 1.0, 'apartment': 0.9, 'condo': 0.95,
            'entire_home': 1.0, 'private_room': 0.7, 'shared_room': 0.5
        }
        
        # Multiplicadores por tipo de ciudad
        city_multipliers = {
            'major_metro': 1.3, 'large_city': 1.15, 'medium_city': 1.0,
            'small_city': 0.9, 'rural': 0.8
        }
        
        estimated_rates = []
        
        for _, row in df.iterrows():
            # Obtener valores
            sqft = row.get('sqft', 2000)
            bedrooms = row.get('bedrooms', 3)
            bathrooms = row.get('bathrooms', 2)
            property_type = row.get('property_type', 'house')
            state = row.get('state', 'CA')
            city_type = row.get('city_type', 'medium_city')
            
            # Normalizar valores
            if pd.isna(sqft) or sqft <= 0:
                sqft = 2000
            if pd.isna(bedrooms) or bedrooms <= 0:
                bedrooms = 3
            if pd.isna(bathrooms) or bathrooms <= 0:
                bathrooms = 2
            
            # Obtener tarifa base por estado
            base_rate_per_sqft = state_rates.get(state, 0.15)
            
            # Obtener multiplicadores
            property_mult = property_multipliers.get(property_type.lower(), 1.0)
            city_mult = city_multipliers.get(city_type.lower(), 1.0)
            
            # Calcular tarifa base
            base_rate = sqft * base_rate_per_sqft
            
            # Aplicar multiplicadores
            final_rate = base_rate * property_mult * city_mult
            
            # Añadir variabilidad realista
            final_rate *= np.random.uniform(0.8, 1.2)
            
            # Asegurar rango realista
            final_rate = max(50, min(2000, final_rate))
            
            estimated_rates.append(final_rate)
        
        print(f"✅ Tarifas estimadas: ${min(estimated_rates):.2f} - ${max(estimated_rates):.2f} (promedio: ${np.mean(estimated_rates):.2f})")
        
        return pd.Series(estimated_rates)
    
    def train_with_excel_data(self, df: pd.DataFrame = None) -> Dict:
        """
        Entrena el modelo con datos de Excel
        """
        if df is None:
            if self.real_data is None:
                raise ValueError("No hay datos cargados")
            df = self.real_data
        
        print("\n🤖 Entrenando modelo con datos de Excel...")
        
        # Entrenar modelo
        metrics = self.predictor.train(df)
        
        # Guardar modelo
        self.predictor.save_model('excel_data_model.pkl')
        
        print("✅ Modelo entrenado con datos de Excel")
        print(f"📊 Precisión: R² = {metrics['r2']:.3f}")
        print(f"📈 Error promedio: ${metrics['mae']:.2f}")
        
        return metrics
    
    def create_sample_data(self, n_samples: int = 100) -> pd.DataFrame:
        """
        Crea datos de muestra para Excel
        """
        print("📝 Creando datos de muestra para Excel...")
        
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

    def export_to_excel(self, filename: str = 'cleaning_data_export.xlsx'):
        """
        Exporta los datos procesados a Excel
        """
        if self.real_data is None:
            print("❌ No hay datos para exportar")
            return None
        
        try:
            # Crear Excel con múltiples hojas
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                # Hoja principal con datos
                self.real_data.to_excel(writer, sheet_name='Datos', index=False)
                
                # Hoja con estadísticas
                stats_df = pd.DataFrame({
                    'Métrica': ['Total Registros', 'Tarifa Promedio', 'Tarifa Mínima', 'Tarifa Máxima'],
                    'Valor': [
                        len(self.real_data),
                        f"${self.real_data['cleaning_rate'].mean():.2f}",
                        f"${self.real_data['cleaning_rate'].min():.2f}",
                        f"${self.real_data['cleaning_rate'].max():.2f}"
                    ]
                })
                stats_df.to_excel(writer, sheet_name='Estadísticas', index=False)
                
                # Hoja con análisis por estado
                if 'state' in self.real_data.columns:
                    state_analysis = self.real_data.groupby('state')['cleaning_rate'].agg([
                        'count', 'mean', 'min', 'max'
                    ]).round(2)
                    state_analysis.to_excel(writer, sheet_name='Análisis por Estado')
            
            print(f"📁 Datos exportados a {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ Error exportando a Excel: {e}")
            return None

def main():
    """
    Función principal para demostrar el uso
    """
    print("📊 SISTEMA DE CARGA DE DATOS EXCEL")
    print("="*50)
    
    uploader = ExcelUploader()
    
    # Crear datos de muestra en Excel
    print("\n1. Creando datos de muestra en Excel...")
    sample_data = uploader.create_sample_data(50)
    
    # Exportar a Excel
    print("\n2. Exportando a Excel...")
    excel_file = uploader.export_to_excel('sample_cleaning_data.xlsx')
    
    print(f"\n✅ Sistema configurado")
    print(f"📁 Archivo Excel creado: {excel_file}")
    print("\n💡 INSTRUCCIONES PARA SUBIR TU EXCEL:")
    print("1. Edita el archivo Excel con tus datos reales")
    print("2. Asegúrate de que las columnas tengan estos nombres:")
    print("   - sqft (metros cuadrados)")
    print("   - bedrooms (habitaciones)")
    print("   - bathrooms (baños)")
    print("   - cleaning_rate (tarifa de limpieza)")
    print("   - property_type (tipo de propiedad)")
    print("   - state (estado)")
    print("   - city_type (tipo de ciudad)")
    print("   - cleaning_type (tipo de limpieza)")
    print("   - frequency (frecuencia)")
    print("3. Usa el sistema de carga para subir tu archivo")

if __name__ == "__main__":
    main()
