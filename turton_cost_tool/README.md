# Herramienta de Estimación de Costos de Equipos - Turton

## 📋 Descripción

Herramienta educativa interactiva para la estimación de costos de equipos de proceso químico basada en las correlaciones del libro:

**Turton, R., Bailie, R. C., Whiting, W. B., Shaeiwitz, J. A., & Bhattacharyya, D. (2018).** *Analysis, Synthesis, and Design of Chemical Processes* (5th ed.). Pearson Education.

Esta herramienta fue desarrollada para ser presentada en el área de educación de congresos de ingeniería química y está diseñada para estudiantes y profesores de ingeniería química.

## 🎯 Características Principales

- **30+ tipos de equipos** organizados en 10 categorías principales
- **Factores de material** para diferentes materiales de construcción (CS, SS, Ti, Ni alloy, etc.)
- **Factores de presión** calculados según código ASME y correlaciones de Turton
- **Actualización automática** de costos usando índices CEPCI desde 2001 hasta 2024
- **Interfaz educativa** con ecuaciones, gráficas y explicaciones detalladas
- **Validación de rangos** para asegurar uso apropiado de correlaciones

## 🏭 Equipos Incluidos

### 1. Intercambiadores de Calor
- Floating Head
- Fixed Tube Sheet
- U-Tube
- Kettle Reboiler
- Air Cooler
- Double Pipe
- Flat Plate

### 2. Torres de Destilación/Absorción
- Tray and Packed Towers

### 3. Reactores
- Autoclave
- Fermenter
- Jacketed Agitated
- Jacketed Non-Agitated

### 4. Recipientes y Tanques
- Horizontal Vessels
- Vertical Vessels
- API Fixed Roof Tanks
- API Floating Roof Tanks

### 5. Bombas
- Centrifugal
- Reciprocating
- Positive Displacement

### 6. Compresores
- Centrifugal/Axial/Reciprocating
- Rotary

### 7. Hornos
- Reformer Furnace
- Pyrolysis Furnace
- Nonreactive Fired Heater

### 8. Turbinas
- Steam Turbine
- Axial Gas Turbine
- Radial Gas/Liquid Expander

## 📐 Ecuaciones Implementadas

### Costo Base
```
log₁₀(Cp°) = K₁ + K₂·log₁₀(A) + K₃·[log₁₀(A)]²
```

### Costo de Compra
```
Cp = Cp° × FM × FP
```

### Actualización por CEPCI
```
Cp(año) = Cp(2001) × (CEPCI_año / CEPCI_2001)
```

### Factor de Presión (Recipientes)
```
FP = (t + CA) / (t_min + CA)

donde: t = (P·D) / (2·S·E - 1.2·P) + CA
```

### Factor de Presión (Otros Equipos)
```
FP = C₁ + C₂·log₁₀(P+1) + C₃·[log₁₀(P+1)]²
```

## 🚀 Instalación y Uso

### Requisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalación

1. **Clonar o descargar el proyecto**

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

### Ejecutar la aplicación

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

## 📚 Estructura del Proyecto

```
turton_cost_tool/
│
├── app.py                      # Aplicación principal Streamlit
│
├── calculations.py             # Módulo de cálculos
│
├── data/                       # Paquete de datos
│   ├── __init__.py
│   ├── equipment_data.py       # Constantes K₁, K₂, K₃ (Tabla A.1)
│   ├── material_factors.py     # Factores de material (Tabla A.3)
│   ├── pressure_factors.py     # Factores de presión (Tabla A.2)
│   └── cepci_data.py          # Índices CEPCI históricos
│
├── requirements.txt            # Dependencias del proyecto
└── README.md                  # Este archivo
```

## 🎓 Uso Educativo

### Para Estudiantes

Esta herramienta permite:
1. Visualizar cómo las correlaciones de Turton funcionan en la práctica
2. Entender el efecto de material y presión en el costo de equipos
3. Aprender sobre actualización de costos usando índices CEPCI
4. Validar cálculos manuales de tareas y proyectos

### Para Profesores

Puede utilizarse para:
1. Demostraciones en clase de Diseño de Plantas
2. Asignación de tareas de costeo de equipos
3. Proyectos de diseño de procesos
4. Comparación de alternativas de equipos

## 📊 Datos y Referencias

### Año Base
- **Año:** 2001
- **CEPCI Base:** 397

### Índices CEPCI Incluidos
- Datos históricos desde 2001 hasta 2024
- Fuente: Chemical Engineering Magazine

### Validación de Rangos
- Todos los equipos tienen rangos de tamaño válidos definidos
- La herramienta advierte cuando se extrapola fuera del rango

## ⚠️ Limitaciones y Advertencias

1. **Extrapolación:** Usar con precaución fuera de los rangos especificados
2. **Precisión:** Las correlaciones dan estimados ±30% según Turton
3. **Año base:** Costos basados en datos de 2001, actualizados con CEPCI
4. **Factores de instalación:** Esta herramienta solo calcula costo de compra (Cp), no costo instalado
5. **Uso educativo:** Diseñada para propósitos educativos, no para cotizaciones reales

## 🔄 Actualizaciones Futuras

Posibles mejoras:
- [ ] Añadir más tipos de equipos (evaporadores, mezcladores, etc.)
- [ ] Incluir factores de módulo bare (costos instalados)
- [ ] Exportar resultados a PDF/Excel
- [ ] Modo de comparación múltiple de equipos
- [ ] Actualización automática de índices CEPCI
- [ ] Versión en inglés de la interfaz

## 👨‍🏫 Autor

**Prof. Oscar**
- Universidad Autónoma de Querétaro
- Profesor-Investigador en Ingeniería Química
- Especialización: Optimización de Procesos, Diseño de Plantas

## 📧 Contacto

Para preguntas, sugerencias o reportar problemas:
- Email: [Tu email]
- Universidad: Universidad Autónoma de Querétaro

## 📄 Licencia

Este proyecto es de código abierto y está disponible para uso educativo.

## 🙏 Agradecimientos

- Turton et al. por las correlaciones publicadas en su libro
- Chemical Engineering Magazine por los índices CEPCI
- Universidad Autónoma de Querétaro por el apoyo institucional

## 📖 Citación

Si utilizas esta herramienta en trabajos académicos, por favor cita:

```
[Tu nombre]. (2024). Herramienta de Estimación de Costos de Equipos - Turton. 
Universidad Autónoma de Querétaro. 
Basado en: Turton, R., et al. (2018). Analysis, Synthesis, and Design of Chemical Processes (5th ed.).
```

---

**Desarrollado para la educación en ingeniería química**
