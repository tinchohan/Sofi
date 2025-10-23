# 🚀 Guía de Despliegue en Render

## 📋 Pasos para Desplegar en Render

### 1. **Preparar el Repositorio**
El proyecto ya está configurado con los archivos necesarios:
- ✅ `render.yaml` - Configuración de Render
- ✅ `Procfile` - Comando de inicio
- ✅ `runtime.txt` - Versión de Python
- ✅ `requirements.txt` - Dependencias actualizadas

### 2. **Crear Cuenta en Render**
1. Ve a [render.com](https://render.com)
2. Regístrate con tu cuenta de GitHub
3. Conecta tu repositorio `tinchohan/Sofi`

### 3. **Configurar el Despliegue**

#### **Opción A: Usando render.yaml (Recomendado)**
1. En Render, selecciona "New Web Service"
2. Conecta tu repositorio GitHub
3. Render detectará automáticamente el archivo `render.yaml`
4. Configuración automática:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Python Version**: 3.9.7

#### **Opción B: Configuración Manual**
1. **Build Command**: `pip install -r requirements.txt`
2. **Start Command**: `gunicorn app:app`
3. **Environment**: `Python 3`
4. **Plan**: `Free` (para empezar)

### 4. **Variables de Entorno**
En la sección "Environment" de Render, añade:
```
FLASK_ENV=production
PYTHON_VERSION=3.9.7
```

### 5. **Desplegar**
1. Haz clic en "Create Web Service"
2. Render construirá automáticamente la aplicación
3. El proceso tomará 2-3 minutos
4. Obtendrás una URL como: `https://sofi-cleaning-calculator.onrender.com`

## 🔧 Configuración Técnica

### **Archivos de Configuración**

#### **render.yaml**
```yaml
services:
  - type: web
    name: sofi-cleaning-calculator
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.7
      - key: FLASK_ENV
        value: production
```

#### **Procfile**
```
web: gunicorn app:app
```

#### **runtime.txt**
```
python-3.9.7
```

### **Modificaciones Realizadas**

1. **app.py**: Configurado para usar variables de entorno
2. **requirements.txt**: Añadido gunicorn
3. **Puerto dinámico**: Usa `PORT` de Render automáticamente

## 🚀 Características del Despliegue

### **Plan Gratuito de Render**
- ✅ **Hasta 750 horas/mes** (suficiente para uso personal)
- ✅ **Auto-sleep** después de 15 minutos de inactividad
- ✅ **SSL automático** (HTTPS)
- ✅ **Deploy automático** desde GitHub
- ✅ **Logs en tiempo real**

### **Limitaciones del Plan Gratuito**
- ⚠️ **Sleep automático**: La app se "duerme" después de 15 min de inactividad
- ⚠️ **Tiempo de inicio**: 30-60 segundos para "despertar"
- ⚠️ **Recursos limitados**: 512MB RAM, 0.1 CPU

## 📊 Monitoreo y Logs

### **Ver Logs en Render**
1. Ve a tu dashboard de Render
2. Selecciona tu servicio
3. Haz clic en "Logs"
4. Ver logs en tiempo real

### **Métricas Importantes**
- **Build Time**: ~2-3 minutos
- **Start Time**: ~30-60 segundos (primera vez)
- **Memory Usage**: ~50-100MB
- **Response Time**: <1 segundo

## 🔄 Actualizaciones Automáticas

### **Deploy Automático**
1. Haz push a GitHub: `git push origin master`
2. Render detecta cambios automáticamente
3. Inicia nuevo build
4. Despliega nueva versión

### **Deploy Manual**
1. En Render dashboard
2. Haz clic en "Manual Deploy"
3. Selecciona commit específico

## 🐛 Solución de Problemas

### **Error: Build Failed**
```bash
# Verificar logs en Render
# Posibles causas:
# - Dependencias faltantes
# - Versión de Python incorrecta
# - Archivos faltantes
```

### **Error: App Crashed**
```bash
# Verificar:
# 1. Logs de aplicación
# 2. Variables de entorno
# 3. Puerto configurado correctamente
```

### **Error: Model Not Found**
```bash
# El modelo se entrena automáticamente en el primer inicio
# Si falla, verificar:
# 1. Permisos de archivos
# 2. Espacio en disco
# 3. Memoria disponible
```

## 💡 Optimizaciones

### **Para Mejor Rendimiento**
1. **Usar plan pago** para evitar sleep
2. **Implementar cache** para predicciones
3. **Optimizar modelo** para menor uso de memoria

### **Para Producción**
1. **Configurar dominio personalizado**
2. **Implementar monitoreo**
3. **Configurar backups**
4. **Usar base de datos externa**

## 📈 Escalabilidad

### **Upgrade a Plan Pago**
- **Starter Plan**: $7/mes
- **Standard Plan**: $25/mes
- **Pro Plan**: $85/mes

### **Características de Planes Pagos**
- ✅ **Sin sleep automático**
- ✅ **Más recursos** (RAM/CPU)
- ✅ **Deploy más rápido**
- ✅ **Soporte prioritario**

## 🎯 Próximos Pasos

1. **Desplegar en Render** siguiendo esta guía
2. **Probar la aplicación** en la URL de Render
3. **Configurar dominio personalizado** (opcional)
4. **Monitorear uso** y optimizar según necesidad

## 📞 Soporte

- **Render Docs**: [render.com/docs](https://render.com/docs)
- **GitHub Issues**: [Crear issue](https://github.com/tinchohan/Sofi/issues)
- **Render Support**: Disponible en dashboard

¡Tu calculadora de tarifas de limpieza estará disponible en la web en pocos minutos! 🚀
