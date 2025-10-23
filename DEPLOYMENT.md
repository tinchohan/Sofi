# 🚀 Guía de Despliegue - Calculadora de Tarifas de Limpieza

## 📋 Requisitos del Sistema

- **Python**: 3.8 o superior
- **Memoria RAM**: Mínimo 2GB
- **Espacio en disco**: 100MB
- **Sistema operativo**: Windows, macOS, Linux

## 🔧 Instalación Local

### 1. **Clonar el Repositorio**
```bash
git clone https://github.com/tinchohan/Sofi.git
cd Sofi
```

### 2. **Instalación Automática**
```bash
python setup.py
```

### 3. **Instalación Manual**
```bash
# Instalar dependencias
pip install -r requirements.txt

# Entrenar modelo
python cleaning_rate_predictor.py

# Iniciar aplicación web
python app.py
```

## 🌐 Despliegue en Producción

### **Opción 1: Heroku**

1. **Crear archivo `Procfile`:**
```
web: gunicorn app:app
```

2. **Crear `runtime.txt`:**
```
python-3.9.7
```

3. **Desplegar:**
```bash
heroku create sofi-cleaning-calculator
git push heroku master
```

### **Opción 2: Docker**

1. **Crear `Dockerfile`:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "app.py"]
```

2. **Construir y ejecutar:**
```bash
docker build -t sofi-cleaning-calculator .
docker run -p 5000:5000 sofi-cleaning-calculator
```

### **Opción 3: AWS EC2**

1. **Configurar instancia EC2**
2. **Instalar dependencias:**
```bash
sudo apt update
sudo apt install python3-pip
pip3 install -r requirements.txt
```

3. **Configurar nginx como proxy reverso**
4. **Usar gunicorn para producción:**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 🔒 Configuración de Seguridad

### **Variables de Entorno**
```bash
export FLASK_ENV=production
export FLASK_DEBUG=False
export SECRET_KEY=your-secret-key-here
```

### **Configuración de Nginx**
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📊 Monitoreo y Logs

### **Logs de Aplicación**
```bash
# Ver logs en tiempo real
tail -f app.log

# Logs de errores
grep ERROR app.log
```

### **Métricas de Rendimiento**
- **Tiempo de respuesta**: < 1 segundo
- **Memoria utilizada**: ~50MB
- **CPU**: < 5% en reposo

## 🔄 Actualizaciones

### **Actualizar Modelo**
```bash
# Entrenar nuevo modelo
python cleaning_rate_predictor.py

# Reiniciar aplicación
sudo systemctl restart sofi-app
```

### **Backup de Datos**
```bash
# Backup del modelo
cp cleaning_rate_model.pkl backup_$(date +%Y%m%d).pkl
```

## 🐛 Solución de Problemas

### **Error: Modelo no encontrado**
```bash
# Re-entrenar modelo
python cleaning_rate_predictor.py
```

### **Error: Puerto en uso**
```bash
# Cambiar puerto en app.py
app.run(port=5001)
```

### **Error: Dependencias faltantes**
```bash
# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

## 📈 Escalabilidad

### **Para Alto Tráfico**
1. **Usar múltiples workers:**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

2. **Implementar cache Redis:**
```python
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'redis'})
```

3. **Usar load balancer:**
```nginx
upstream sofi_backend {
    server 127.0.0.1:5000;
    server 127.0.0.1:5001;
    server 127.0.0.1:5002;
}
```

## 🔧 Mantenimiento

### **Tareas Diarias**
- Verificar logs de errores
- Monitorear uso de memoria
- Backup del modelo

### **Tareas Semanales**
- Actualizar dependencias
- Revisar métricas de rendimiento
- Limpiar logs antiguos

### **Tareas Mensuales**
- Entrenar modelo con nuevos datos
- Revisar configuración de seguridad
- Actualizar documentación

## 📞 Soporte

Para soporte técnico o preguntas sobre el despliegue:
- **GitHub Issues**: [Crear issue](https://github.com/tinchohan/Sofi/issues)
- **Documentación**: Ver README.md
- **Ejemplos**: Ver example_usage.py

## 🎯 Mejores Prácticas

1. **Siempre usar HTTPS en producción**
2. **Implementar rate limiting**
3. **Monitorear logs regularmente**
4. **Hacer backup del modelo entrenado**
5. **Usar variables de entorno para configuración**
6. **Implementar health checks**
7. **Usar un servidor WSGI para producción**
