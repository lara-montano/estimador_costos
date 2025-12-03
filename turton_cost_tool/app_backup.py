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

# Title and header
st.markdown("# 🏭 Equipment Cost Estimation Tool")
st.markdown("### Based on Turton *Analysis, Synthesis, and Design of Chemical Processes* (5th Ed.)")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.markdown("## ⚙️ Equipment Selection")
    
    # Get equipment organized by category
    equipment_by_cat = get_equipment_by_category()
    
    # Category selection
    category = st.selectbox(
        "Select Equipment Category:",
        options=list(equipment_by_cat.keys()),
        help="Choose the type of equipment you want to cost"
    )
    
    # Equipment selection within category
    equipment_name = st.selectbox(
        "Select Specific Equipment:",
        options=equipment_by_cat[category],
        help="Select the specific equipment configuration"
    )
    
    st.markdown("---")
    st.markdown("## 📊 Reference Information")
    st.info(f"""
    **Base Year:** 2001  
    **Base CEPCI:** 397  
    **Latest Year:** {get_latest_year()}  
    **Latest CEPCI:** {CEPCI_DATA[get_latest_year()]}
    """)
    
    st.markdown("---")
    st.markdown("### 📚 About This Tool")
    st.markdown("""
    Educational tool for estimating equipment costs using correlations 
    from Turton's textbook.
    
    **Features:**
    - 30+ equipment types
    - Material factors
    - Pressure corrections
    - CEPCI updating to any year
    
    **Developed by:**  
    Prof. Oscar  
    Universidad Autónoma de Querétaro
    """)

# Main content area
if equipment_name:
    equip_data = EQUIPMENT_DATA[equipment_name]
    
    # Display equipment information
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"## {equipment_name}")
        st.markdown(f"**Category:** {equip_data['category']}")
        
    with col2:
        st.metric("Size Parameter", equip_data['size_param'])
        st.metric("Units", equip_data['units'])
    
    # Input parameters
    st.markdown("---")
    st.markdown("## 📝 Input Parameters")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Size parameter input
        size_value = st.number_input(
            f"{equip_data['size_param']} ({equip_data['units']})",
            min_value=0.0,
            value=float(equip_data['min_size'] + equip_data['max_size']) / 2,
            step=float((equip_data['max_size'] - equip_data['min_size']) / 100),
            help=f"Valid range: {equip_data['min_size']} - {equip_data['max_size']} {equip_data['units']}"
        )
        
        # Show valid range
        st.caption(f"✅ Valid range: {equip_data['min_size']:.2f} - {equip_data['max_size']:.2f}")
    
    with col2:
        # Material selection
        available_materials = get_materials_for_equipment(equipment_name)
        material = st.selectbox(
            "Material of Construction",
            options=available_materials,
            help="Select the material of construction for the equipment"
        )
        
        if len(available_materials) == 1:
            st.caption("ℹ️ Only one material available for this equipment")
    
    with col3:
        # Pressure input
        p_min, p_max = get_pressure_range(equipment_name)
        pressure = st.number_input(
            "Operating Pressure (barg)",
            min_value=-1.0,
            max_value=500.0,
            value=0.0,
            step=1.0,
            help=f"Recommended range: {p_min:.1f} - {p_max:.1f} barg"
        )
        
        st.caption(f"✅ Typical range: {p_min:.1f} - {p_max:.1f} barg")
    
    # Diameter input for vessels (if needed)
    diameter = None
    if "Vessel" in equipment_name or "Tower" in equipment_name or "Reactor" in equipment_name:
        st.markdown("### Additional Parameters for Pressure Vessels")
        diameter = st.number_input(
            "Vessel Diameter (m)",
            min_value=0.1,
            max_value=10.0,
            value=1.0,
            step=0.1,
            help="Required for pressure factor calculation (ASME code)"
        )
    
    # Target year for cost updating
    st.markdown("---")
    st.markdown("## 📅 Cost Updating")
    
    available_years = get_available_years()
    target_year = st.selectbox(
        "Update cost to year:",
        options=available_years,
        index=len(available_years) - 1,  # Default to latest year
        help="Select year to update the cost using CEPCI indices"
    )
    
    # Calculate button
    st.markdown("---")
    if st.button("🧮 Calculate Equipment Cost", type="primary", use_container_width=True):
        # Perform calculation
        with st.spinner("Calculating..."):
            result = calculate_cost_updated(
                equipment_name=equipment_name,
                size_param_value=size_value,
                material=material,
                pressure_barg=pressure,
                diameter_m=diameter,
                target_year=target_year
            )
        
        # Display results
        st.markdown("---")
        st.markdown("## 💰 Results")
        
        if result["success"]:
            # Create columns for metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Base Cost (2001)",
                    f"${result['Cp_base_2001']:,.0f}",
                    help="Cp° - Base purchased cost in 2001 USD"
                )
            
            with col2:
                st.metric(
                    "Material Factor",
                    f"{result['FM']:.3f}",
                    help="FM - Material of construction factor"
                )
            
            with col3:
                st.metric(
                    "Pressure Factor",
                    f"{result['FP']:.3f}",
                    help="FP - Pressure correction factor"
                )
            
            with col4:
                if result.get("Cp_updated"):
                    increase = ((result['Cp_updated'] / result['Cp_2001']) - 1) * 100
                    st.metric(
                        f"Updated Cost ({target_year})",
                        f"${result['Cp_updated']:,.0f}",
                        f"{increase:+.1f}%",
                        help=f"Cost updated to {target_year} using CEPCI"
                    )
            
            # Detailed breakdown
            st.markdown("### 📋 Detailed Breakdown")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Cost in Base Year (2001)")
                st.markdown(f"""
                - **Base Cost (Cp°):** ${result['Cp_base_2001']:,.2f}
                - **Material Factor (FM):** {result['FM']:.3f}
                - **Pressure Factor (FP):** {result['FP']:.3f}
                - **Purchased Cost (Cp):** ${result['Cp_2001']:,.2f}
                - **CEPCI (2001):** {result['base_cepci']}
                """)
            
            with col2:
                if result.get("Cp_updated"):
                    st.markdown(f"#### Cost Updated to {target_year}")
                    increase_pct = ((result['Cp_updated'] / result['Cp_2001']) - 1) * 100
                    st.markdown(f"""
                    - **Updated Cost:** ${result['Cp_updated']:,.2f}
                    - **CEPCI ({target_year}):** {result['target_cepci']}
                    - **Cost Increase:** {increase_pct:+.1f}%
                    - **Inflation Factor:** {result['target_cepci'] / result['base_cepci']:.3f}
                    """)
            
            # Equation display
            st.markdown("### 📐 Equations Used")
            st.latex(r"\log_{10}(C_p^\circ) = K_1 + K_2 \cdot \log_{10}(A) + K_3 \cdot [\log_{10}(A)]^2")
            st.latex(r"C_p = C_p^\circ \times F_M \times F_P")
            st.latex(r"C_p(\text{year}) = C_p(2001) \times \frac{\text{CEPCI}_{\text{year}}}{\text{CEPCI}_{2001}}")
            
            # Warnings
            if not result["valid_range"]:
                st.warning(f"⚠️ {result['message']}")
            
            # Success message
            st.success("✅ Calculation completed successfully!")
            
            # Plot cost comparison
            st.markdown("### 📊 Cost Evolution")
            
            # Create plot showing cost over years
            years = available_years[-10:]  # Last 10 years
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
                name='Equipment Cost',
                line=dict(color='#2874a6', width=3),
                marker=dict(size=10, color='#1e3a5f')
            ))
            
            fig.update_layout(
                title=f"Cost Evolution for {equipment_name}",
                xaxis_title="Year",
                yaxis_title="Cost (USD)",
                template="plotly_white",
                height=400,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        else:
            st.error(f"❌ {result['error']}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d; padding: 2rem 0;'>
    <p><strong>Equipment Cost Estimation Tool</strong></p>
    <p>Based on: Turton, R., Bailie, R. C., Whiting, W. B., Shaeiwitz, J. A., & Bhattacharyya, D. (2018). 
    <em>Analysis, Synthesis, and Design of Chemical Processes</em> (5th ed.). Pearson Education.</p>
    <p>Developed for educational purposes | Universidad Autónoma de Querétaro</p>
</div>
""", unsafe_allow_html=True)
