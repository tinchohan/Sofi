#!/bin/bash
# Script de inicio para Render
echo "Starting Sofi Cleaning Calculator..."

# Verificar que el modelo existe
if [ ! -f "cleaning_rate_model.pkl" ]; then
    echo "Training model..."
    python -c "from cleaning_rate_predictor import CleaningRatePredictor; predictor = CleaningRatePredictor(); predictor.train(); predictor.save_model('cleaning_rate_model.pkl')"
fi

# Iniciar aplicación
echo "Starting application on port $PORT..."
gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 120 app:app
