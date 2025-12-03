# Caso de Estudio Educativo para Artículo de Congreso

## Análisis de Alternativas de Intercambiadores de Calor

### Contexto del Problema

Un estudiante de Diseño de Plantas debe seleccionar un intercambiador de calor para enfriar 50 kg/s de una corriente de proceso de 120°C a 40°C. Se han determinado los siguientes requerimientos:

**Datos de diseño:**
- Área de transferencia requerida: 150 m²
- Presión de operación lado proceso: 15 barg
- Presión de operación lado utilidad: 5 barg
- Fluido de proceso: Solución acuosa corrosiva (requiere SS)
- Fluido de enfriamiento: Agua de torre (puede ser CS)

### Pregunta Educativa

¿Qué configuración de intercambiador es más económica?

**Alternativas a evaluar:**
1. Floating Head - CS shell/CS tube
2. Floating Head - CS shell/SS tube
3. Floating Head - SS shell/SS tube
4. Fixed Tube Sheet - CS shell/SS tube
5. U-Tube - CS shell/SS tube
6. Air Cooler - SS tube

### Análisis con la Herramienta

#### Caso 1: Floating Head - CS shell/CS tube
```python
result = calculate_cost_updated(
    equipment_name="Heat Exchanger - Floating Head",
    size_param_value=150,
    material="CS shell/CS tube",
    pressure_barg=15,
    target_year=2024
)
```

**Resultados:**
- Cp° (2001): $33,500
- FM: 1.00
- FP: 1.00
- **Cp (2024): $68,800**

❌ **No recomendado:** El fluido corrosivo requiere SS en contacto con el proceso.

---

#### Caso 2: Floating Head - CS shell/SS tube ✅
```python
result = calculate_cost_updated(
    equipment_name="Heat Exchanger - Floating Head",
    size_param_value=150,
    material="CS shell/SS tube",
    pressure_barg=15,
    target_year=2024
)
```

**Resultados:**
- Cp° (2001): $33,500
- FM: 2.70
- FP: 1.00
- **Cp (2024): $185,800**

✅ **Viable técnicamente:** SS en contacto con proceso corrosivo.

---

#### Caso 3: Floating Head - SS shell/SS tube
```python
result = calculate_cost_updated(
    equipment_name="Heat Exchanger - Floating Head",
    size_param_value=150,
    material="SS shell/SS tube",
    pressure_barg=15,
    target_year=2024
)
```

**Resultados:**
- Cp° (2001): $33,500
- FM: 4.00
- FP: 1.00
- **Cp (2024): $275,200**

⚠️ **Sobredimensionado:** No necesario tener SS en ambos lados.

---

#### Caso 4: Fixed Tube Sheet - CS shell/SS tube ✅
```python
result = calculate_cost_updated(
    equipment_name="Heat Exchanger - Fixed Tube Sheet",
    size_param_value=150,
    material="CS shell/SS tube",
    pressure_barg=15,
    target_year=2024
)
```

**Resultados:**
- Cp° (2001): $28,700
- FM: 2.70
- FP: 1.00
- **Cp (2024): $159,100**

✅ **Más económico:** Ahorros de $26,700 vs. Floating Head

⚠️ **Limitación:** Difícil limpieza mecánica exterior de tubos

---

#### Caso 5: U-Tube - CS shell/SS tube ✅
```python
result = calculate_cost_updated(
    equipment_name="Heat Exchanger - U-Tube",
    size_param_value=150,
    material="CS shell/SS tube",
    pressure_barg=15,
    target_year=2024
)
```

**Resultados:**
- Cp° (2001): $26,900
- FM: 2.70
- FP: 1.00
- **Cp (2024): $149,400**

✅ **Más económico:** Ahorros de $36,400 vs. Floating Head

✅ **Ventaja:** Permite expansión térmica diferencial

⚠️ **Limitación:** Difícil limpieza interior de tubos

---

#### Caso 6: Air Cooler - SS tube
```python
result = calculate_cost_updated(
    equipment_name="Heat Exchanger - Air Cooler",
    size_param_value=150,
    material="SS tube",
    pressure_barg=15,
    target_year=2024
)
```

**Resultados:**
- Cp° (2001): $42,100
- FM: 2.20
- FP: 1.00
- **Cp (2024): $190,300**

⚠️ **Más caro:** Pero elimina costo de agua de enfriamiento

✅ **Considerar:** Costos operativos de agua vs. electricidad

---

### Tabla Comparativa de Resultados

| Configuración | Cp (2024) | Ventajas | Desventajas | Recomendación |
|---------------|-----------|----------|-------------|---------------|
| Floating Head CS/CS | $68,800 | Económico | ❌ No resistente a corrosión | No viable |
| **U-Tube CS/SS** | **$149,400** | ✅ Más económico<br>✅ Expansión térmica | Limpieza interior difícil | ⭐ Opción A |
| Fixed Tube CS/SS | $159,100 | ✅ Económico | Limpieza exterior difícil | ⭐ Opción B |
| Floating Head CS/SS | $185,800 | Fácil mantenimiento | Más caro | Opción C |
| Air Cooler SS | $190,300 | Sin agua de enfriamiento | Más caro, requiere ventiladores | Evaluar OPEX |
| Floating Head SS/SS | $275,200 | Máxima resistencia | ❌ Innecesariamente caro | No recomendado |

### Análisis de Sensibilidad

#### Efecto del Tamaño en el Costo

Usando U-Tube CS/SS como referencia:

| Área (m²) | Cp (2024) | Costo/m² |
|-----------|-----------|----------|
| 50 | $77,200 | $1,544 |
| 100 | $121,000 | $1,210 |
| **150** | **$149,400** | **$996** |
| 200 | $173,700 | $869 |
| 300 | $218,300 | $728 |

📊 **Observación:** Economías de escala evidentes - costo unitario disminuye ~50% al triplicar tamaño.

#### Efecto de la Presión

Para U-Tube CS/SS de 150 m²:

| Presión (barg) | FP | Cp (2024) |
|----------------|-----|-----------|
| 0 | 1.00 | $149,400 |
| 5 | 1.00 | $149,400 |
| 10 | 1.04 | $155,400 |
| **15** | **1.08** | **$161,300** |
| 20 | 1.12 | $167,300 |
| 30 | 1.19 | $177,900 |

📊 **Observación:** Presión tiene efecto moderado (+19% a 30 barg).

#### Efecto de Inflación (CEPCI)

Para U-Tube CS/SS de 150 m²:

| Año | CEPCI | Cp (USD) | Aumento |
|-----|-------|----------|---------|
| 2001 | 397 | $72,800 | Base |
| 2010 | 551 | $101,000 | +39% |
| 2020 | 596 | $109,400 | +50% |
| **2024** | **815** | **$149,400** | **+105%** |

📊 **Observación:** Costo se duplicó en 23 años. Aceleración post-2020.

### Decisión Final Educativa

**Recomendación basada en análisis:**

🏆 **Primera opción: U-Tube CS shell/SS tube**
- Costo: $149,400
- Ahorro: $36,400 vs. Floating Head estándar (19%)
- Justificación técnica: Permite expansión térmica, adecuado para diferencias de temperatura
- Limitación aceptable: Limpieza química suficiente para aplicación

💡 **Segunda opción: Fixed Tube Sheet CS/SS**
- Si la limpieza exterior no es crítica
- Ahorro adicional: $9,700 (6.5%)

### Lecciones Aprendidas

1. **Material es el factor dominante:**
   - FM puede variar de 1.0 a 10.9
   - Impacto mayor que presión o tamaño

2. **Configuración también afecta costo base:**
   - U-Tube < Fixed < Floating Head
   - ~10-15% de diferencia

3. **Economías de escala son significativas:**
   - Duplicar tamaño no duplica costo
   - Importante para selección de equipos redundantes

4. **Presión tiene efecto moderado:**
   - FP típicamente 1.0-1.5 para equipos estándar
   - Más significativo a presiones >50 barg

5. **Inflación debe considerarse:**
   - CEPCI se duplicó en 23 años
   - Datos de libros antiguos requieren actualización

### Aplicación Pedagógica

**Competencias desarrolladas:**
- ✅ Análisis de alternativas técnico-económico
- ✅ Uso de correlaciones de costeo
- ✅ Consideración de factores de diseño
- ✅ Toma de decisiones con múltiples criterios
- ✅ Presentación profesional de resultados

**Tiempo estimado:**
- Cálculo manual tradicional: 2-3 horas
- Con herramienta digital: 20-30 minutos
- **Beneficio:** Más tiempo para análisis y discusión

**Evaluación sugerida:**
1. Reproducir cálculos (30%)
2. Análisis de sensibilidad adicional (30%)
3. Justificación de selección final (40%)

---

### Extensiones del Caso de Estudio

**Preguntas adicionales para estudiantes:**

1. **Análisis CAPEX vs OPEX:**
   - Air cooler tiene mayor CAPEX pero menor OPEX
   - ¿Cuál es el payback si agua cuesta $1/m³?

2. **Consideraciones de mantenimiento:**
   - ¿Cómo afectan los costos de limpieza la selección?
   - Calcular NPV incluyendo mantenimiento

3. **Análisis de incertidumbre:**
   - Si área real puede variar ±20%, ¿cambia la selección?
   - Realizar análisis de Monte Carlo

4. **Optimización multiobjetivo:**
   - Minimizar costo inicial vs. costo de ciclo de vida
   - Considerar confiabilidad y disponibilidad

---

## Conclusión del Caso

Este caso de estudio demuestra cómo la herramienta digital:

✅ **Acelera** el proceso de evaluación de alternativas
✅ **Facilita** análisis de sensibilidad exhaustivos  
✅ **Mejora** la comprensión de factores de costo
✅ **Permite** enfoque en análisis técnico-económico profundo

La herramienta transforma una tarea de cálculo repetitivo en una experiencia de **aprendizaje activo** centrada en el **análisis crítico** y la **toma de decisiones**.

---

**Nota para el Congreso:**

Este caso de estudio puede presentarse como:
1. **Póster:** Con gráficas comparativas
2. **Presentación oral:** Con demostración en vivo
3. **Taller práctico:** Estudiantes replican el análisis
4. **Material suplementario:** Del artículo principal
