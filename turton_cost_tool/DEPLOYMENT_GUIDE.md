# Guía de Instalación, Deployment y Uso

## Universidad Autónoma de Querétaro - Herramienta de Costeo Turton

---

## 1. INSTALACIÓN LOCAL

### 1.1 Requisitos Previos

**Software requerido:**
- Python 3.8 o superior ([Descargar](https://www.python.org/downloads/))
- pip (incluido con Python)
- Navegador web moderno (Chrome, Firefox, Edge)

**Verificar instalación:**
```bash
python --version    # Debe mostrar Python 3.8+
pip --version      # Debe mostrar pip instalado
```

### 1.2 Instalación Paso a Paso

#### Opción A: Instalación Rápida

```bash
# 1. Descargar o clonar el proyecto
cd turton_cost_tool

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar la aplicación
streamlit run app.py
```

#### Opción B: Instalación con Entorno Virtual (Recomendado)

```bash
# 1. Crear entorno virtual
python -m venv venv

# 2. Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Mac/Linux:
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar aplicación
streamlit run app.py
```

### 1.3 Verificación de Instalación

Si todo está correcto, verás:
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

---

## 2. USO DE LA APLICACIÓN

### 2.1 Interfaz Web

**Acceso:**
1. Abrir navegador
2. Ir a `http://localhost:8501`
3. La aplicación se carga automáticamente

**Navegación:**
- **Sidebar izquierda:** Selección de equipo y parámetros
- **Panel principal:** Entrada de datos y resultados
- **Scroll:** Para ver gráficas y detalles

### 2.2 Flujo de Trabajo Típico

```
1. Seleccionar categoría de equipo
   ↓
2. Seleccionar equipo específico
   ↓
3. Ingresar tamaño del equipo
   ↓
4. Seleccionar material de construcción
   ↓
5. Ingresar presión de operación
   ↓
6. (Si aplica) Ingresar diámetro del recipiente
   ↓
7. Seleccionar año objetivo para actualización
   ↓
8. Presionar "Calculate Equipment Cost"
   ↓
9. Analizar resultados y gráficas
```

### 2.3 Interpretación de Resultados

**Métricas principales:**
- **Base Cost (2001):** Costo en año base de correlación
- **Material Factor:** Multiplicador por material
- **Pressure Factor:** Multiplicador por presión
- **Updated Cost:** Costo actualizado al año seleccionado

**Indicadores:**
- ✅ Verde: Cálculo dentro de rango válido
- ⚠️ Amarillo: Advertencia de extrapolación
- ❌ Rojo: Error en cálculo

---

## 3. USO PROGRAMÁTICO (Python)

### 3.1 Importar Módulos

```python
from calculations import calculate_cost_updated
from data import get_equipment_list, EQUIPMENT_DATA
```

### 3.2 Ejemplo Básico

```python
# Calcular costo de intercambiador
result = calculate_cost_updated(
    equipment_name="Heat Exchanger - Floating Head",
    size_param_value=100,
    material="CS shell/SS tube",
    pressure_barg=10,
    target_year=2024
)

# Mostrar resultado
if result["success"]:
    print(f"Costo en 2024: ${result['Cp_updated']:,.2f}")
else:
    print(f"Error: {result['error']}")
```

### 3.3 Análisis de Sensibilidad

```python
import matplotlib.pyplot as plt

# Variar tamaño
sizes = [50, 100, 150, 200, 250, 300]
costs = []

for size in sizes:
    result = calculate_cost_updated(
        equipment_name="Heat Exchanger - Floating Head",
        size_param_value=size,
        material="CS shell/SS tube",
        pressure_barg=10,
        target_year=2024
    )
    costs.append(result['Cp_updated'])

# Graficar
plt.plot(sizes, costs, marker='o')
plt.xlabel('Área (m²)')
plt.ylabel('Costo (USD)')
plt.title('Efecto del Tamaño en el Costo')
plt.grid(True)
plt.show()
```

---

## 4. DEPLOYMENT EN SERVIDOR

### 4.1 Streamlit Community Cloud (GRATIS)

**Pasos:**
1. Crear cuenta en [streamlit.io](https://streamlit.io)
2. Conectar repositorio GitHub
3. Seleccionar archivo `app.py`
4. Hacer deploy

**Ventajas:**
- ✅ Gratis
- ✅ HTTPS automático
- ✅ Actualizaciones automáticas desde GitHub
- ✅ No requiere servidor propio

### 4.2 Servidor Universitario

#### Opción A: Docker (Recomendado)

**Crear Dockerfile:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**Construir y ejecutar:**
```bash
docker build -t turton-cost-tool .
docker run -p 8501:8501 turton-cost-tool
```

#### Opción B: Servidor Linux Tradicional

```bash
# 1. Instalar Python y dependencias
sudo apt update
sudo apt install python3-pip

# 2. Copiar archivos al servidor
scp -r turton_cost_tool/ user@server:/opt/

# 3. En el servidor, instalar dependencias
cd /opt/turton_cost_tool
pip3 install -r requirements.txt

# 4. Ejecutar con nohup para mantener corriendo
nohup streamlit run app.py --server.port=8501 &
```

#### Opción C: Systemd Service (Producción)

**Crear `/etc/systemd/system/turton-cost.service`:**
```ini
[Unit]
Description=Turton Cost Estimation Tool
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/turton_cost_tool
ExecStart=/usr/bin/streamlit run app.py --server.port=8501
Restart=always

[Install]
WantedBy=multi-user.target
```

**Activar servicio:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable turton-cost
sudo systemctl start turton-cost
```

### 4.3 Nginx Reverse Proxy

**Configuración `/etc/nginx/sites-available/turton`:**
```nginx
server {
    listen 80;
    server_name turton-cost.uaq.mx;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

---

## 5. MANTENIMIENTO Y ACTUALIZACIÓN

### 5.1 Actualizar CEPCI

**Archivo:** `data/cepci_data.py`

```python
CEPCI_DATA = {
    # ... datos existentes ...
    2025: xxx,  # Agregar nuevo año
}
```

### 5.2 Agregar Nuevo Equipo

**Archivo:** `data/equipment_data.py`

```python
"Nuevo Equipo": {
    "K1": x.xxxx,
    "K2": x.xxxx,
    "K3": x.xxxx,
    "size_param": "Parámetro",
    "units": "unidades",
    "min_size": min,
    "max_size": max,
    "category": "Categoría"
}
```

### 5.3 Actualizar Factores de Material

**Archivo:** `data/material_factors.py`

Agregar nuevas combinaciones de materiales según necesidad.

---

## 6. INTEGRACIÓN EN CURSOS

### 6.1 Canvas/Moodle

**Como actividad:**
1. Crear tarea en LMS
2. Proporcionar link a herramienta
3. Solicitar capturas de pantalla de resultados
4. Pedir análisis escrito de alternativas

**Como examen:**
1. Dar caso de estudio
2. Tiempo límite para resolver
3. Subir reporte con resultados

### 6.2 Google Classroom

**Integración:**
```
1. Crear asignación
2. Agregar link a herramienta
3. Adjuntar plantilla de reporte
4. Configurar rúbrica de evaluación
```

### 6.3 Uso en Clase

**Proyección en pantalla:**
- Demostración en vivo de cálculos
- Análisis de sensibilidad interactivo
- Comparación de alternativas
- Discusión de resultados

---

## 7. TROUBLESHOOTING

### 7.1 Problemas Comunes

**Error: "ModuleNotFoundError"**
```bash
# Solución:
pip install -r requirements.txt
```

**Error: "Port 8501 already in use"**
```bash
# Solución: Cambiar puerto
streamlit run app.py --server.port=8502
```

**Error: "Cannot import calculations"**
```bash
# Solución: Verificar estructura de archivos
# Ejecutar desde directorio turton_cost_tool/
cd turton_cost_tool
streamlit run app.py
```

**Aplicación lenta:**
```bash
# Solución: Cerrar pestañas innecesarias del navegador
# Reiniciar aplicación
# Verificar memoria disponible
```

### 7.2 Logs y Debugging

**Ver logs de Streamlit:**
```bash
streamlit run app.py --server.runOnSave=true --logger.level=debug
```

**Verificar cálculos:**
```python
# Usar example_usage.py para probar
python example_usage.py
```

---

## 8. RECURSOS ADICIONALES

### 8.1 Documentación

- `README.md` - Información general
- `DOCUMENTATION_CONGRESS.md` - Detalles técnicos
- `CASE_STUDY_EDUCATION.md` - Caso de estudio ejemplo
- `example_usage.py` - Ejemplos de código

### 8.2 Videos Tutorial (Sugerido)

Crear videos cortos mostrando:
1. Instalación (5 min)
2. Uso básico (10 min)
3. Caso de estudio completo (20 min)
4. Análisis de sensibilidad (15 min)

### 8.3 Soporte

**Para problemas técnicos:**
- Revisar esta guía
- Consultar documentación de Streamlit
- Contactar al desarrollador

**Para dudas de contenido:**
- Consultar libro de Turton
- Revisar apuntes de clase
- Preguntar al profesor

---

## 9. MEJORES PRÁCTICAS

### 9.1 Para Estudiantes

✅ **DO:**
- Verificar que tamaño esté en rango válido
- Comparar múltiples alternativas
- Documentar supuestos y decisiones
- Verificar unidades de medida

❌ **DON'T:**
- Confiar ciegamente en resultados sin validar
- Usar valores fuera de rango sin justificación
- Ignorar advertencias de la herramienta
- Olvidar actualizar a año relevante

### 9.2 Para Profesores

✅ **DO:**
- Explicar limitaciones de correlaciones
- Mostrar validación manual de al menos un caso
- Enfatizar análisis crítico sobre cálculo mecánico
- Proporcionar contexto ingenieril

❌ **DON'T:**
- Presentar herramienta como "caja negra"
- Olvidar enseñar ecuaciones subyacentes
- Permitir uso sin entendimiento
- Ignorar verificación de resultados

---

## 10. LICENCIA Y CRÉDITOS

**Código:**
- Código abierto para uso educativo
- Puede modificarse según necesidades

**Datos:**
- Basados en Turton 5ta edición
- CEPCI de Chemical Engineering Magazine
- Citar fuentes apropiadamente

**Uso comercial:**
- No recomendado (correlaciones son estimados ±30%)
- Para cotizaciones reales, consultar vendors

---

## 11. CONTACTO Y SOPORTE

**Desarrollador:**
Prof. Oscar
Universidad Autónoma de Querétaro
Facultad de Ingeniería

**Para:**
- 🐛 Reportar bugs
- 💡 Sugerir mejoras
- 📚 Colaboraciones
- ❓ Preguntas técnicas

**Contribuciones:**
Pull requests bienvenidos en GitHub (si se publica)

---

**Última actualización:** Diciembre 2024  
**Versión:** 1.0  
**Estado:** Producción
