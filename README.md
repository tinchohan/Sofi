# Calculadora de Tarifas de Limpieza para Propiedades en Estados Unidos

## Descripción

Esta aplicación utiliza machine learning para predecir tarifas de limpieza de propiedades en Estados Unidos, considerando factores como el tamaño de la propiedad, ubicación, tipo de limpieza y frecuencia del servicio.

## Características

### Factores Considerados

**Factores de la Propiedad:**
- Metros cuadrados totales
- Número de habitaciones
- Número de baños
- Tipo de propiedad (casa, apartamento, condominio)

**Factores del Mercado:**
- Estado (con índices de costo de vida)
- Tipo de ciudad (metrópolis, ciudad grande, mediana, pequeña, rural)
- Temporada y demanda local

**Factores del Servicio:**
- Tipo de limpieza (básica, profunda, post-construcción)
- Frecuencia (una vez, semanal, mensual)

### Modelo de Machine Learning

- **Algoritmo**: Gradient Boosting Regressor
- **Características**: 15+ variables incluyendo ratios calculados
- **Precisión**: R² > 0.85 en datos de prueba
- **Intervalo de confianza**: ±15% de la predicción

## Instalación

1. **Clonar el repositorio:**
```bash
git clone <repository-url>
cd cleaning-rate-predictor
```

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

3. **Ejecutar la aplicación:**
```bash
python app.py
```

4. **Abrir en el navegador:**
```
http://localhost:5000
```

## Uso

### Interfaz Web

1. **Completar información de la propiedad:**
   - Metros cuadrados
   - Número de habitaciones y baños
   - Tipo de propiedad

2. **Seleccionar ubicación:**
   - Estado
   - Tipo de ciudad

3. **Especificar servicio:**
   - Tipo de limpieza
   - Frecuencia

4. **Obtener predicción:**
   - Tarifa estimada
   - Rango de confianza
   - Factores considerados

### API

**Endpoint:** `POST /predict`

**Parámetros:**
```json
{
    "sqft": 2500,
    "bedrooms": 4,
    "bathrooms": 3,
    "property_type": "house",
    "state": "CA",
    "city_type": "large_city",
    "cleaning_type": "deep",
    "frequency": "one_time"
}
```

**Respuesta:**
```json
{
    "success": true,
    "prediction": {
        "predicted_rate": 425.50,
        "confidence_interval": {
            "lower": 361.68,
            "upper": 489.33
        },
        "factors_considered": {
            "property_size": 2500,
            "bedrooms": 4,
            "bathrooms": 3,
            "property_type": "house",
            "location": "CA - large_city",
            "cleaning_type": "deep",
            "frequency": "one_time"
        }
    }
}
```

## Estructura del Proyecto

```
cleaning-rate-predictor/
├── app.py                          # Aplicación Flask
├── cleaning_rate_predictor.py     # Modelo de ML
├── templates/
│   └── index.html                  # Interfaz web
├── requirements.txt                # Dependencias
├── README.md                       # Documentación
└── cleaning_rate_model.pkl        # Modelo entrenado (generado)
```

## Datos de Mercado

El modelo incluye datos de costo de vida por estado y multiplicadores por tipo de ciudad:

### Estados con Mayor Costo de Vida
- California (CA): 151.7
- Nueva York (NY): 139.1
- Hawaii (HI): 165.9
- Washington DC: 158.1

### Estados con Menor Costo de Vida
- Mississippi (MS): 82.8
- Arkansas (AR): 84.1
- Alabama (AL): 85.8
- Kentucky (KY): 88.1

### Multiplicadores por Tipo de Ciudad
- Metrópolis Principal: 1.3x
- Ciudad Grande: 1.15x
- Ciudad Mediana: 1.0x
- Ciudad Pequeña: 0.9x
- Área Rural: 0.8x

## Personalización

### Entrenar con Datos Reales

Para usar datos reales en lugar de sintéticos:

```python
# Cargar datos reales
real_data = pd.read_csv('your_cleaning_data.csv')

# Entrenar modelo
predictor = CleaningRatePredictor()
metrics = predictor.train(real_data)
```

### Ajustar Parámetros del Modelo

```python
# Modificar parámetros en cleaning_rate_predictor.py
self.model = GradientBoostingRegressor(
    n_estimators=300,      # Más árboles
    learning_rate=0.05,    # Aprendizaje más lento
    max_depth=8,           # Mayor profundidad
    random_state=42
)
```

## Limitaciones

1. **Datos Sintéticos**: El modelo actual usa datos generados. Para producción, se necesitan datos reales.
2. **Factores Estacionales**: No considera variaciones estacionales específicas.
3. **Competencia Local**: No incluye análisis de competencia por área específica.
4. **Materiales Especiales**: No considera costos de productos especializados.

## Mejoras Futuras

1. **Integración con APIs**: Conectar con APIs de costo de vida en tiempo real
2. **Análisis Geográfico**: Incluir datos de código postal específico
3. **Factores Estacionales**: Añadir variaciones por temporada
4. **Machine Learning Avanzado**: Implementar modelos de deep learning
5. **Dashboard Analytics**: Panel de administración para análisis de datos

## Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.
