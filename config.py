"""
Configuración para el modelo de predicción de tarifas de limpieza
"""

# Configuración del modelo
MODEL_CONFIG = {
    'algorithm': 'GradientBoostingRegressor',
    'n_estimators': 200,
    'learning_rate': 0.1,
    'max_depth': 6,
    'random_state': 42
}

# Configuración de la aplicación web
WEB_CONFIG = {
    'host': '0.0.0.0',
    'port': 5000,
    'debug': True
}

# Estados de Estados Unidos con sus índices de costo de vida
STATE_COST_INDEX = {
    'CA': 151.7, 'NY': 139.1, 'HI': 165.9, 'DC': 158.1, 'MA': 131.4,
    'CT': 128.0, 'AK': 125.8, 'MD': 124.0, 'NJ': 120.4, 'WA': 118.9,
    'CO': 115.8, 'OR': 115.6, 'VT': 115.2, 'NH': 114.9, 'RI': 114.3,
    'IL': 113.2, 'DE': 112.8, 'VA': 111.8, 'MN': 111.6, 'UT': 110.8,
    'TX': 93.9, 'FL': 98.3, 'GA': 90.4, 'NC': 95.1, 'TN': 89.4,
    'OH': 95.0, 'PA': 99.1, 'MI': 90.1, 'IN': 88.9, 'WI': 95.7,
    'MO': 89.8, 'KY': 88.1, 'AL': 85.8, 'SC': 88.9, 'LA': 89.1,
    'MS': 82.8, 'AR': 84.1, 'OK': 87.4, 'KS': 88.1, 'NE': 90.8,
    'IA': 89.4, 'ND': 94.1, 'SD': 88.9, 'MT': 95.1, 'WY': 92.8,
    'ID': 95.4, 'NV': 108.1, 'AZ': 105.1, 'NM': 92.8
}

# Multiplicadores por tipo de ciudad
CITY_TYPE_MULTIPLIER = {
    'major_metro': 1.3,  # NYC, LA, Chicago, etc.
    'large_city': 1.15,  # Ciudades > 500k habitantes
    'medium_city': 1.0,   # Ciudades 100k-500k
    'small_city': 0.9,   # Ciudades < 100k
    'rural': 0.8         # Áreas rurales
}

# Multiplicadores por tipo de propiedad
PROPERTY_TYPE_MULTIPLIER = {
    'house': 1.0,
    'apartment': 0.9,
    'condo': 0.95
}

# Multiplicadores por tipo de limpieza
CLEANING_TYPE_MULTIPLIER = {
    'basic': 1.0,
    'deep': 1.5,
    'post_construction': 2.0
}

# Multiplicadores por frecuencia
FREQUENCY_MULTIPLIER = {
    'one_time': 1.0,
    'weekly': 0.8,
    'monthly': 0.9
}

# Configuración de datos sintéticos
SYNTHETIC_DATA_CONFIG = {
    'n_samples': 10000,
    'sqft_mean': 2000,
    'sqft_std': 800,
    'sqft_min': 500,
    'sqft_max': 8000,
    'bedrooms_mean': 3,
    'bedrooms_min': 1,
    'bedrooms_max': 8,
    'bathrooms_ratio_min': 0.8,
    'bathrooms_ratio_max': 1.2,
    'base_rate_per_sqft': 0.15
}

# Etiquetas para la interfaz web
LABELS = {
    'property_types': {
        'house': 'Casa',
        'apartment': 'Apartamento',
        'condo': 'Condominio'
    },
    'city_types': {
        'major_metro': 'Metrópolis Principal',
        'large_city': 'Ciudad Grande',
        'medium_city': 'Ciudad Mediana',
        'small_city': 'Ciudad Pequeña',
        'rural': 'Área Rural'
    },
    'cleaning_types': {
        'basic': 'Limpieza Básica',
        'deep': 'Limpieza Profunda',
        'post_construction': 'Post-Construcción'
    },
    'frequencies': {
        'one_time': 'Una vez',
        'weekly': 'Semanal',
        'monthly': 'Mensual'
    }
}

# Configuración de validación
VALIDATION_RULES = {
    'sqft': {'min': 100, 'max': 20000},
    'bedrooms': {'min': 1, 'max': 20},
    'bathrooms': {'min': 1, 'max': 20}
}
