"""
Herramienta de Estimación de Costos de Equipos - Turton
Herramienta educativa para estudiantes de ingeniería química
Basada en Turton 5ta Edición (2018)

Autores:
- Oscar Daniel Lara Montaño (UAQ)
- Fernando Israel Gómez Castro (UAQ)
- Betsie Martínez Cano (UAQ)
- Sergio Iván Martínez Guido (UAQ)

Para: Congreso de Educación en Ingeniería Química
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from data import (
    get_equipment_by_category,
    EQUIPMENT_DATA,
    get_materials_for_equipment,
    get_pressure_range,
    get_available_years,
    get_latest_year,
    CEPCI_DATA
)
from calculations import calculate_cost_updated, format_cost_result

# Configuración de la página
st.set_page_config(
    page_title="Herramienta de Costeo de Equipos - Turton",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para estilo profesional
st.markdown("""
<style>
    /* Estilo principal */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Encabezados */
    h1 {
        color: #1e3a5f;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 700;
        padding: 1rem 0;
        border-bottom: 3px solid #2874a6;
    }
    
    h2 {
        color: #2874a6;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        margin-top: 1.5rem;
    }
    
    h3 {
        color: #5499c7;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Cuadros de información */
    .stAlert {
        background-color: #ebf5fb;
        border-left: 4px solid #2874a6;
    }
    
    /* Barra lateral */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3a5f 0%, #2874a6 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Métricas */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #1e3a5f;
    }
    
    /* Cuadro de éxito */
    .success-box {
        background-color: #d5f4e6;
        border-left: 5px solid #27ae60;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    /* Cuadro de advertencia */
    .warning-box {
        background-color: #fef5e7;
        border-left: 5px solid #f39c12;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Título y encabezado
st.markdown("# 🏭 Herramienta de Estimación de Costos de Equipos")
st.markdown("### Basada en Turton *Analysis, Synthesis, and Design of Chemical Processes* (5ta Ed.)")
st.markdown("---")

# Barra lateral
with st.sidebar:
    st.markdown("## ⚙️ Selección de Equipo")
    
    # Obtener equipos organizados por categoría
    equipment_by_cat = get_equipment_by_category()
    
    # Selección de categoría
    category = st.selectbox(
        "Seleccione la Categoría de Equipo:",
        options=list(equipment_by_cat.keys()),
        help="Elija el tipo de equipo que desea costear"
    )
    
    # Selección de equipo dentro de la categoría
    equipment_name = st.selectbox(
        "Seleccione el Equipo Específico:",
        options=equipment_by_cat[category],
        help="Seleccione la configuración específica del equipo"
    )
    
    st.markdown("---")
    st.markdown("## 📊 Información de Referencia")
    st.info(f"""
    **Año Base:** 2001  
    **CEPCI Base:** 397  
    **Año Más Reciente:** {get_latest_year()}  
    **CEPCI Actual:** {CEPCI_DATA[get_latest_year()]}
    """)
    
    st.markdown("---")
    st.markdown("### 📚 Acerca de Esta Herramienta")
    st.markdown("""
    Herramienta educativa para estimación de costos de equipos usando 
    correlaciones del libro de Turton.
    
    **Características:**
    - 30+ tipos de equipos
    - Factores de material
    - Correcciones por presión
    - Actualización CEPCI
    
    **Desarrollado por:**  
    O.D. Lara-Montaño  
    F.I. Gómez-Castro  
    B. Martínez-Cano  
    S.I. Martínez-Guido  
    
    Universidad Autónoma de Querétaro
    """)

# Área de contenido principal
if equipment_name:
    equip_data = EQUIPMENT_DATA[equipment_name]
    
    # Mostrar información del equipo
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"## {equipment_name}")
        st.markdown(f"**Categoría:** {equip_data['category']}")
        
    with col2:
        st.metric("Parámetro de Tamaño", equip_data['size_param'])
        st.metric("Unidades", equip_data['units'])
    
    # Parámetros de entrada
    st.markdown("---")
    st.markdown("## 📝 Parámetros de Entrada")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Entrada del parámetro de tamaño
        size_value = st.number_input(
            f"{equip_data['size_param']} ({equip_data['units']})",
            min_value=0.0,
            value=float(equip_data['min_size'] + equip_data['max_size']) / 2,
            step=float((equip_data['max_size'] - equip_data['min_size']) / 100),
            help=f"Rango válido: {equip_data['min_size']} - {equip_data['max_size']} {equip_data['units']}"
        )
        
        # Mostrar rango válido
        st.caption(f"✅ Rango válido: {equip_data['min_size']:.2f} - {equip_data['max_size']:.2f}")
    
    with col2:
        # Selección de material
        available_materials = get_materials_for_equipment(equipment_name)
        material = st.selectbox(
            "Material de Construcción",
            options=available_materials,
            help="Seleccione el material de construcción del equipo"
        )
        
        if len(available_materials) == 1:
            st.caption("ℹ️ Solo un material disponible para este equipo")
    
    with col3:
        # Entrada de presión
        p_min, p_max = get_pressure_range(equipment_name)
        pressure = st.number_input(
            "Presión de Operación (barg)",
            min_value=-1.0,
            max_value=500.0,
            value=0.0,
            step=1.0,
            help=f"Rango recomendado: {p_min:.1f} - {p_max:.1f} barg"
        )
        
        st.caption(f"✅ Rango típico: {p_min:.1f} - {p_max:.1f} barg")
    
    # Entrada de diámetro para recipientes (si es necesario)
    diameter = None
    if "Vessel" in equipment_name or "Tower" in equipment_name or "Reactor" in equipment_name:
        st.markdown("### Parámetros Adicionales para Recipientes a Presión")
        diameter = st.number_input(
            "Diámetro del Recipiente (m)",
            min_value=0.1,
            max_value=10.0,
            value=1.0,
            step=0.1,
            help="Requerido para cálculo del factor de presión (código ASME)"
        )
    
    # Año objetivo para actualización de costos
    st.markdown("---")
    st.markdown("## 📅 Actualización de Costos")
    
    available_years = get_available_years()
    target_year = st.selectbox(
        "Actualizar costo al año:",
        options=available_years,
        index=len(available_years) - 1,  # Por defecto el año más reciente
        help="Seleccione el año al cual actualizar el costo usando índices CEPCI"
    )
    
    # Botón de calcular
    st.markdown("---")
    if st.button("🧮 Calcular Costo del Equipo", type="primary", use_container_width=True):
        # Realizar cálculo
        with st.spinner("Calculando..."):
            result = calculate_cost_updated(
                equipment_name=equipment_name,
                size_param_value=size_value,
                material=material,
                pressure_barg=pressure,
                diameter_m=diameter,
                target_year=target_year
            )
        
        # Mostrar resultados
        st.markdown("---")
        st.markdown("## 💰 Resultados")
        
        if result["success"]:
            # Crear columnas para métricas
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Costo Base (2001)",
                    f"${result['Cp_base_2001']:,.0f}",
                    help="Cp° - Costo base de compra en USD del 2001"
                )
            
            with col2:
                st.metric(
                    "Factor de Material",
                    f"{result['FM']:.3f}",
                    help="FM - Factor por material de construcción"
                )
            
            with col3:
                st.metric(
                    "Factor de Presión",
                    f"{result['FP']:.3f}",
                    help="FP - Factor de corrección por presión"
                )
            
            with col4:
                if result.get("Cp_updated"):
                    increase = ((result['Cp_updated'] / result['Cp_2001']) - 1) * 100
                    st.metric(
                        f"Costo Actualizado ({target_year})",
                        f"${result['Cp_updated']:,.0f}",
                        f"{increase:+.1f}%",
                        help=f"Costo actualizado a {target_year} usando CEPCI"
                    )
            
            # Desglose detallado
            st.markdown("### 📋 Desglose Detallado")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Costo en Año Base (2001)")
                st.markdown(f"""
                - **Costo Base (Cp°):** ${result['Cp_base_2001']:,.2f}
                - **Factor de Material (FM):** {result['FM']:.3f}
                - **Factor de Presión (FP):** {result['FP']:.3f}
                - **Costo de Compra (Cp):** ${result['Cp_2001']:,.2f}
                - **CEPCI (2001):** {result['base_cepci']}
                """)
            
            with col2:
                if result.get("Cp_updated"):
                    st.markdown(f"#### Costo Actualizado a {target_year}")
                    increase_pct = ((result['Cp_updated'] / result['Cp_2001']) - 1) * 100
                    st.markdown(f"""
                    - **Costo Actualizado:** ${result['Cp_updated']:,.2f}
                    - **CEPCI ({target_year}):** {result['target_cepci']}
                    - **Incremento de Costo:** {increase_pct:+.1f}%
                    - **Factor de Inflación:** {result['target_cepci'] / result['base_cepci']:.3f}
                    """)
            
            # Mostrar ecuaciones
            st.markdown("### 📐 Ecuaciones Utilizadas")
            st.latex(r"\log_{10}(C_p^\circ) = K_1 + K_2 \cdot \log_{10}(A) + K_3 \cdot [\log_{10}(A)]^2")
            st.latex(r"C_p = C_p^\circ \times F_M \times F_P")
            st.latex(r"C_p(\text{año}) = C_p(2001) \times \frac{\text{CEPCI}_{\text{año}}}{\text{CEPCI}_{2001}}")
            
            # Advertencias
            if not result["valid_range"]:
                st.warning(f"⚠️ {result['message']}")
            
            # Mensaje de éxito
            st.success("✅ ¡Cálculo completado exitosamente!")
            
            # Gráfica de comparación de costos
            st.markdown("### 📊 Evolución del Costo")
            
            # Crear gráfica mostrando costo a través de los años
            years = available_years[-10:]  # Últimos 10 años
            costs = []
            for year in years:
                from data import get_cepci
                cepci = get_cepci(year)
                if cepci:
                    cost = result['Cp_2001'] * (cepci / result['base_cepci'])
                    costs.append(cost)
                else:
                    costs.append(None)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=years,
                y=costs,
                mode='lines+markers',
                name='Costo del Equipo',
                line=dict(color='#2874a6', width=3),
                marker=dict(size=10, color='#1e3a5f')
            ))
            
            fig.update_layout(
                title=f"Evolución del Costo para {equipment_name}",
                xaxis_title="Año",
                yaxis_title="Costo (USD)",
                template="plotly_white",
                height=400,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        else:
            st.error(f"❌ {result['error']}")

# Pie de página
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d; padding: 2rem 0;'>
    <p><strong>Herramienta de Estimación de Costos de Equipos</strong></p>
    <p>Basada en: Turton, R., Bailie, R. C., Whiting, W. B., Shaeiwitz, J. A., & Bhattacharyya, D. (2018). 
    <em>Analysis, Synthesis, and Design of Chemical Processes</em> (5ta ed.). Pearson Education.</p>
    <p><strong>Autores:</strong> O.D. Lara-Montaño, F.I. Gómez-Castro, B. Martínez-Cano, S.I. Martínez-Guido</p>
    <p>Desarrollado con fines educativos | Universidad Autónoma de Querétaro</p>
</div>
""", unsafe_allow_html=True)
