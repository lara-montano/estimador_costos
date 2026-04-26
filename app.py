"""
Estimador de Costos de Equipos de Proceso
Basado en Turton et al. (2018) - Apéndice A
Desarrollado con Streamlit
"""

import math
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from data import (
    CEPCI, CEPCI_BASE, EQUIPMENT, B1B2, FM_MAP,
    FBM_FIXED, PRESSURE_FACTORS, COST_METHOD,
)

# ============================================================
# Funciones de cálculo
# ============================================================

def calc_cp0(K1, K2, K3, A):
    """Costo base de compra (Eq. A.1). Cp° en USD (CEPCI=397)."""
    log_A = math.log10(A)
    log_Cp = K1 + K2 * log_A + K3 * log_A**2
    return 10**log_Cp


def calc_fp_equation(C1, C2, C3, P):
    """Factor de presión con Eq. A.3. P en barg."""
    if P <= 0:
        return 1.0
    log_P = math.log10(P)
    log_FP = C1 + C2 * log_P + C3 * log_P**2
    FP = 10**log_FP
    return max(FP, 1.0)


def calc_fp_vessel(P, D):
    """Factor de presión para recipientes (Eq. A.2).
    P en barg, D en metros.
    FP = ((P*D)/(2*(850-0.6*P)) + 0.00315) / 0.0063
    """
    if P < -0.5:
        return 1.25
    if P <= 0:
        return 1.0
    numerator = (P * D) / (2 * (850 - 0.6 * P)) + 0.00315
    FP = numerator / 0.0063
    return max(FP, 1.0)


def calc_fq(N):
    """Factor de cantidad para platos (Fq). N = número de platos."""
    if N >= 20:
        return 1.0
    if N <= 0:
        return 1.0
    log_N = math.log10(N)
    log_Fq = 0.4771 + 0.08516 * log_N - 0.3473 * log_N**2
    return 10**log_Fq


# Equipos shell-and-tube con FP separado para shell y tube
HX_WITH_SIDES = {
    "Floating head", "Fixed tube sheet", "U-tube",
    "Bayonet", "Kettle reboiler", "Spiral tube",
}


def get_fp(category, equip_name, P, D=None, pressure_side="shell"):
    """Obtiene el factor de presión para un equipo dado."""
    method = COST_METHOD.get(category, "")

    # Recipientes y torres usan Eq. A.2
    if method == "vessel":
        if D is None:
            D = 1.0
        return calc_fp_vessel(P, D)

    # Equipos con factores de presión tabulados
    if category in PRESSURE_FACTORS and equip_name in PRESSURE_FACTORS[category]:
        pf_list = PRESSURE_FACTORS[category][equip_name]

        # Para HX con sides, buscar el lado correcto
        if equip_name in HX_WITH_SIDES:
            for pf in pf_list:
                if pf.get("side") == pressure_side:
                    pmin, pmax = pf["range"]
                    if pmin <= P <= pmax:
                        return calc_fp_equation(pf["C1"], pf["C2"], pf["C3"], P)
            return 1.0

        # Para equipos sin side, buscar rango directo
        for pf in pf_list:
            if "side" not in pf:
                pmin, pmax = pf["range"]
                if pmin <= P <= pmax:
                    return calc_fp_equation(pf["C1"], pf["C2"], pf["C3"], P)

        return 1.0

    return 1.0


def calc_cost(category, equip_name, A, material, P, D, N, cepci_year,
              pressure_side="shell"):
    """Calcula el costo de módulo desnudo (CBM) actualizado."""
    equip_data = EQUIPMENT[category][equip_name]
    K1, K2, K3 = equip_data["K1"], equip_data["K2"], equip_data["K3"]

    # Costo base
    Cp0 = calc_cp0(K1, K2, K3, A)

    method = COST_METHOD[category]
    FP = 1.0
    FM = 1.0
    FBM = 1.0
    Fq = 1.0

    if method == "B1B2":
        b = B1B2[category][equip_name]
        B1, B2 = b["B1"], b["B2"]
        fm_table = FM_MAP.get(category, {}).get(equip_name, {})
        FM = fm_table.get(material, 1.0)
        FP = get_fp(category, equip_name, P, pressure_side=pressure_side)
        FBM = B1 + B2 * FM * FP
        CBM = Cp0 * FBM

    elif method == "vessel":
        b = B1B2[category][equip_name]
        B1, B2 = b["B1"], b["B2"]
        fm_table = FM_MAP.get(category, {}).get(equip_name, {})
        FM = fm_table.get(material, 1.0)
        FP = calc_fp_vessel(P, D)
        FBM = B1 + B2 * FM * FP
        CBM = Cp0 * FBM

    elif method == "FBM":
        fbm_table = FBM_FIXED.get(category, {}).get(equip_name, {})
        FBM = fbm_table.get(material, list(fbm_table.values())[0] if fbm_table else 1.0)
        CBM = Cp0 * FBM

    elif method == "FBM_FP":
        fbm_table = FBM_FIXED.get(category, {}).get(equip_name, {})
        FBM = fbm_table.get(material, list(fbm_table.values())[0] if fbm_table else 1.0)
        FP = get_fp(category, equip_name, P)
        CBM = Cp0 * FBM * FP

    elif method == "tray":
        fbm_table = FBM_FIXED.get(category, {}).get(equip_name, {})
        FBM = fbm_table.get(material, list(fbm_table.values())[0] if fbm_table else 1.0)
        Fq = calc_fq(N)
        CBM = Cp0 * N * FBM * Fq

    else:
        CBM = Cp0

    # Actualización temporal con CEPCI
    cepci_target = CEPCI.get(cepci_year, CEPCI_BASE)
    CBM_updated = CBM * (cepci_target / CEPCI_BASE)

    return {
        "Cp0": Cp0,
        "FM": FM,
        "FP": FP,
        "FBM": FBM,
        "Fq": Fq,
        "N": N,
        "CBM_base": CBM,
        "CEPCI_base": CEPCI_BASE,
        "CEPCI_target": cepci_target,
        "CBM_updated": CBM_updated,
        "method": method,
    }


def cost_evolution(category, equip_name, A, material, P, D, N,
                   pressure_side="shell"):
    """Calcula la evolución del costo a través de los años."""
    years = sorted(CEPCI.keys())
    costs = []
    for year in years:
        result = calc_cost(category, equip_name, A, material, P, D, N, year,
                           pressure_side=pressure_side)
        costs.append(result["CBM_updated"])
    return years, costs


# ============================================================
# Interfaz Streamlit
# ============================================================

st.set_page_config(
    page_title="Estimador de Costos de Equipos",
    page_icon="🏭",
    layout="wide",
)

# --- CSS personalizado ---
st.markdown("""
<style>
    /* Encabezado principal */
    .main-header {
        background: linear-gradient(135deg, #1a5276 0%, #2e86c1 100%);
        padding: 1.5rem 2rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        color: white;
    }
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 1.8rem;
    }
    .main-header p {
        color: #d5e8f0;
        margin: 0.3rem 0 0 0;
        font-size: 0.95rem;
    }

    /* Tarjetas de resultados */
    [data-testid="stMetric"] {
        background-color: #0e1117;
        border: 1px solid #2e86c1;
        border-radius: 8px;
        padding: 12px 16px;
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.8rem;
    }
    [data-testid="stMetricValue"] {
        font-size: 1.3rem;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0a0e14;
    }
    [data-testid="stSidebar"] hr {
        border-color: #2e86c1;
    }

    /* Expander */
    .streamlit-expanderHeader {
        font-size: 0.9rem;
    }

    /* Info box */
    .info-box {
        background-color: #1a2332;
        border-left: 4px solid #2e86c1;
        padding: 0.8rem 1rem;
        border-radius: 0 6px 6px 0;
        margin-bottom: 1rem;
        font-size: 0.85rem;
        line-height: 1.5;
    }
    .credits {
        text-align: center;
        color: #7f8c8d;
        font-size: 0.78rem;
        margin-top: 0.5rem;
        padding-top: 0.5rem;
        border-top: 1px solid #2c3e50;
    }
</style>
""", unsafe_allow_html=True)

# --- Encabezado ---
st.markdown("""
<div class="main-header">
    <h1>Estimador de Costos de Equipos de Proceso</h1>
    <p>Basado en Turton et al. (2018) — Apéndice A &nbsp;|&nbsp; CEPCI base = 397 (Sept. 2001)</p>
</div>
""", unsafe_allow_html=True)

# --- Sidebar: selección de equipo ---
st.sidebar.header("Selección de equipo")

category = st.sidebar.selectbox("Categoría", list(EQUIPMENT.keys()))
equip_name = st.sidebar.selectbox("Tipo de equipo", list(EQUIPMENT[category].keys()))

equip_data = EQUIPMENT[category][equip_name]

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Parámetro:** {equip_data['units']}")
st.sidebar.markdown(f"**Rango válido:** {equip_data['min']} – {equip_data['max']}")

A = st.sidebar.number_input(
    f"Capacidad ({equip_data['units']})",
    min_value=float(equip_data["min"]),
    max_value=float(equip_data["max"]),
    value=float(equip_data["min"]),
    format="%.4f",
)

# Material
method = COST_METHOD[category]
if method in ("B1B2", "vessel"):
    fm_table = FM_MAP.get(category, {}).get(equip_name, {})
    materials = list(fm_table.keys()) if fm_table else ["CS"]
elif method in ("FBM", "FBM_FP", "tray"):
    fbm_table = FBM_FIXED.get(category, {}).get(equip_name, {})
    materials = list(fbm_table.keys()) if fbm_table else ["Default"]
else:
    materials = ["Default"]

material = st.sidebar.selectbox("Material de construcción", materials)

st.sidebar.markdown("---")

# Presión
needs_pressure = method in ("B1B2", "vessel", "FBM_FP")
if needs_pressure and (
    (category in PRESSURE_FACTORS and equip_name in PRESSURE_FACTORS.get(category, {}))
    or method == "vessel"
):
    P = st.sidebar.number_input("Presión de operación (barg)", value=0.0, format="%.2f")
else:
    P = 0.0

# Selección shell/tube para HX con sides
pressure_side = "shell"
if (category == "Intercambiadores de calor" and equip_name in HX_WITH_SIDES
        and needs_pressure):
    pressure_side = st.sidebar.radio(
        "Lado de la presión",
        options=["shell", "tube"],
        horizontal=True,
        help="Lado del intercambiador donde se aplica la presión de diseño",
    )

# Diámetro (para recipientes)
if method == "vessel":
    D = st.sidebar.number_input(
        "Diámetro del recipiente (m)", value=1.0, min_value=0.1, format="%.2f"
    )
else:
    D = 1.0

# Número de platos
if method == "tray":
    N = st.sidebar.number_input("Número de platos", value=10, min_value=1, max_value=500)
else:
    N = 1

st.sidebar.markdown("---")

# Año CEPCI
cepci_year = st.sidebar.selectbox(
    "Año de actualización (CEPCI)", sorted(CEPCI.keys(), reverse=True)
)

# --- Instrucciones breves ---
with st.sidebar.expander("Instrucciones de uso"):
    st.markdown("""
1. **Seleccione la categoría** y el tipo de equipo.
2. **Ingrese la capacidad** dentro del rango válido mostrado.
3. **Elija el material** de construcción.
4. Si aplica, ingrese la **presión de operación** (barg) y el
   **lado** (shell/tube) para intercambiadores.
5. Para recipientes y torres, ingrese el **diámetro** (m).
6. Para platos, indique el **número de platos**.
7. Seleccione el **año CEPCI** para actualizar el costo.

Los resultados se actualizan automáticamente.

**Ecuaciones principales:**
- *Eq. A.1:* Costo base con K₁, K₂, K₃
- *Eq. A.2:* Factor de presión (recipientes, ASME)
- *Eq. A.3:* Factor de presión (otros equipos)
- *Eq. A.4:* Costo de módulo desnudo
""")

# --- Cálculo (siempre activo, reactivo a cambios) ---
result = calc_cost(category, equip_name, A, material, P, D, N, cepci_year,
                   pressure_side=pressure_side)

# --- Resultados ---
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("Resultados")

    # Tarjetas de resultados
    c1, c2, c3 = st.columns(3)
    c1.metric("Costo base Cp° (USD, 2001)", f"${result['Cp0']:,.2f}")
    c2.metric(f"CBM (USD, {cepci_year})", f"${result['CBM_updated']:,.2f}")
    c3.metric(f"CEPCI {cepci_year}", f"{result['CEPCI_target']:.1f}")

    c4, c5, c6 = st.columns(3)
    c4.metric("Factor de material (FM)", f"{result['FM']:.4f}")
    c5.metric("Factor de presión (FP)", f"{result['FP']:.4f}")
    c6.metric("Factor de módulo (FBM)", f"{result['FBM']:.4f}")

    if result["method"] == "tray":
        c7, c8, _ = st.columns(3)
        c7.metric("Número de platos (N)", f"{N}")
        c8.metric("Factor de cantidad (Fq)", f"{result['Fq']:.4f}")

    # Ecuaciones utilizadas
    st.subheader("Ecuaciones utilizadas")

    K1, K2, K3 = equip_data["K1"], equip_data["K2"], equip_data["K3"]
    st.latex(r"\log_{10}(C_p^\circ) = K_1 + K_2 \log_{10}(A) + K_3 [\log_{10}(A)]^2")
    st.caption(f"K₁ = {K1}, K₂ = {K2}, K₃ = {K3}, A = {A}")

    if result["method"] == "B1B2":
        b = B1B2[category][equip_name]
        st.latex(r"C_{BM} = C_p^\circ \left(B_1 + B_2 \, F_M \, F_P\right)")
        st.caption(
            f"B₁ = {b['B1']}, B₂ = {b['B2']}, "
            f"F_M = {result['FM']:.4f}, F_P = {result['FP']:.4f}"
        )
    elif result["method"] == "vessel":
        b = B1B2[category][equip_name]
        st.latex(
            r"F_P = \frac{\dfrac{P \cdot D}{2\,(850 - 0.6\,P)} + 0.00315}{0.0063}"
        )
        st.latex(r"C_{BM} = C_p^\circ \left(B_1 + B_2 \, F_M \, F_P\right)")
        st.caption(
            f"B₁ = {b['B1']}, B₂ = {b['B2']}, "
            f"F_M = {result['FM']:.4f}, F_P = {result['FP']:.4f}"
        )
    elif result["method"] == "FBM":
        st.latex(r"C_{BM} = C_p^\circ \cdot F_{BM}")
        st.caption(f"F_BM = {result['FBM']:.4f}")
    elif result["method"] == "FBM_FP":
        st.latex(r"C_{BM} = C_p^\circ \cdot F_{BM} \cdot F_P")
        st.caption(f"F_BM = {result['FBM']:.4f}, F_P = {result['FP']:.4f}")
    elif result["method"] == "tray":
        st.latex(r"C_{BM} = C_p^\circ \cdot N \cdot F_{BM} \cdot F_q")
        st.caption(f"N = {N}, F_BM = {result['FBM']:.4f}, F_q = {result['Fq']:.4f}")

    cepci_val = result["CEPCI_target"]
    st.latex(
        r"C_{actualizado} = C_{BM} \times "
        r"\frac{CEPCI_{" + str(cepci_year) + r"}}{CEPCI_{2001}} = "
        r"C_{BM} \times \frac{" + f"{cepci_val:.1f}" + r"}{397}"
    )

    # Tabla de desglose
    st.subheader("Desglose del cálculo")
    breakdown_vars = [
        "A (capacidad)", "K₁", "K₂", "K₃", "Cp° (USD)",
        "F_M", "F_P", "F_BM",
        "CBM base (USD, 2001)", f"CEPCI {cepci_year}",
        f"CBM actualizado (USD, {cepci_year})",
    ]
    breakdown_vals = [
        f"{A:.4f}", f"{K1}", f"{K2}", f"{K3}",
        f"${result['Cp0']:,.2f}", f"{result['FM']:.4f}",
        f"{result['FP']:.4f}", f"{result['FBM']:.4f}",
        f"${result['CBM_base']:,.2f}", f"{result['CEPCI_target']:.1f}",
        f"${result['CBM_updated']:,.2f}",
    ]
    if result["method"] == "tray":
        # Insertar N y Fq antes de CBM base
        idx = breakdown_vars.index("CBM base (USD, 2001)")
        breakdown_vars.insert(idx, "N (platos)")
        breakdown_vals.insert(idx, f"{N}")
        breakdown_vars.insert(idx + 1, "F_q")
        breakdown_vals.insert(idx + 1, f"{result['Fq']:.4f}")

    df_breakdown = pd.DataFrame({"Variable": breakdown_vars, "Valor": breakdown_vals})
    st.dataframe(df_breakdown, use_container_width=True, hide_index=True)

with col2:
    # Gráfica de evolución temporal
    st.subheader("Evolución temporal del costo")
    years, costs = cost_evolution(
        category, equip_name, A, material, P, D, N,
        pressure_side=pressure_side,
    )

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years, y=costs,
        mode="lines+markers",
        name="CBM",
        line=dict(color="#2e86c1", width=2),
        marker=dict(size=5),
    ))
    # Marcar año seleccionado
    fig.add_trace(go.Scatter(
        x=[cepci_year], y=[result["CBM_updated"]],
        mode="markers",
        name=f"Año {cepci_year}",
        marker=dict(color="#e74c3c", size=12, symbol="diamond"),
    ))
    fig.update_layout(
        xaxis_title="Año",
        yaxis_title="Costo CBM (USD)",
        template="plotly_white",
        height=370,
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        font=dict(size=11),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Análisis de sensibilidad: variación de capacidad
    st.subheader("Sensibilidad al tamaño")
    A_min = equip_data["min"]
    A_max = equip_data["max"]
    n_points = 50
    if A_max / A_min > 100:
        A_values = [A_min * (A_max / A_min) ** (i / (n_points - 1))
                    for i in range(n_points)]
    else:
        step = (A_max - A_min) / (n_points - 1)
        A_values = [A_min + i * step for i in range(n_points)]

    costs_sens = []
    for a_val in A_values:
        r = calc_cost(category, equip_name, a_val, material, P, D, N, cepci_year,
                      pressure_side=pressure_side)
        costs_sens.append(r["CBM_updated"])

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=A_values, y=costs_sens,
        mode="lines",
        name="CBM vs Capacidad",
        line=dict(color="#e67e22", width=2),
        fill="tozeroy",
        fillcolor="rgba(230, 126, 34, 0.1)",
    ))
    fig2.add_trace(go.Scatter(
        x=[A], y=[result["CBM_updated"]],
        mode="markers",
        name="Punto actual",
        marker=dict(color="#e74c3c", size=12, symbol="star"),
    ))
    fig2.update_layout(
        xaxis_title=equip_data["units"],
        yaxis_title=f"CBM (USD, {cepci_year})",
        template="plotly_white",
        height=370,
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        font=dict(size=11),
    )
    if A_max / A_min > 100:
        fig2.update_xaxes(type="log")
    st.plotly_chart(fig2, use_container_width=True)

# Tabla CEPCI
with st.expander("Tabla de índices CEPCI (2001–2024)"):
    cepci_df = pd.DataFrame({"Año": list(CEPCI.keys()), "CEPCI": list(CEPCI.values())})
    st.dataframe(cepci_df, use_container_width=True, hide_index=True)

# --- Pie: referencia y créditos ---
st.markdown("---")
st.markdown(
    "**Referencia:** Turton, R., Shaeiwitz, J.A., Bhattacharyya, D., Whiting, W.B. "
    "*Analysis, Synthesis, and Design of Chemical Processes*, 5th Ed. Prentice Hall, 2018."
)
st.markdown("""
<div class="credits">
    <strong>Desarrollado por:</strong><br>
    Oscar Daniel Lara-Montaño &nbsp;·&nbsp;
    Sergio Iván Martínez-Guido &nbsp;·&nbsp;
    Fernando Israel Gómez-Castro &nbsp;·&nbsp;
    Betsie Martínez-Cano<br>
    Universidad Autónoma de Querétaro &nbsp;|&nbsp; Universidad de Guanajuato<br><br>
    <em>Si encuentra algún error o bug, por favor repórtelo en
    <a href="https://github.com/lara-montano/estimador_costos/issues" target="_blank" style="color: #2e86c1;">
    github.com/lara-montano/estimador_costos/issues</a></em>
</div>
""", unsafe_allow_html=True)
