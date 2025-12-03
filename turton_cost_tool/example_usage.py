"""
Ejemplo de uso de la herramienta de costeo de equipos
Este script muestra cómo usar las funciones de cálculo directamente
"""

from calculations import calculate_cost_updated, format_cost_result
from data import get_equipment_list, get_equipment_by_category

print("="*70)
print("EJEMPLO DE USO - HERRAMIENTA DE COSTEO DE EQUIPOS TURTON")
print("="*70)
print()

# Ejemplo 1: Intercambiador de calor
print("EJEMPLO 1: Intercambiador de Calor de Cabezal Flotante")
print("-"*70)

result1 = calculate_cost_updated(
    equipment_name="Heat Exchanger - Floating Head",
    size_param_value=100,  # m² de área
    material="CS shell/SS tube",
    pressure_barg=10,
    diameter_m=None,  # No aplica para intercambiadores
    target_year=2024
)

print(format_cost_result(result1))
print("\n" + "="*70 + "\n")

# Ejemplo 2: Reactor agitado con chaqueta
print("EJEMPLO 2: Reactor Agitado con Chaqueta")
print("-"*70)

result2 = calculate_cost_updated(
    equipment_name="Reactor - Jacketed Agitated",
    size_param_value=5,  # m³ de volumen
    material="SS",  # Acero inoxidable
    pressure_barg=5,
    diameter_m=1.5,  # m de diámetro (requerido para cálculo de presión)
    target_year=2024
)

print(format_cost_result(result2))
print("\n" + "="*70 + "\n")

# Ejemplo 3: Bomba centrífuga
print("EJEMPLO 3: Bomba Centrífuga")
print("-"*70)

result3 = calculate_cost_updated(
    equipment_name="Pump - Centrifugal",
    size_param_value=50,  # kW de potencia
    material="SS",
    pressure_barg=15,
    diameter_m=None,  # No aplica
    target_year=2024
)

print(format_cost_result(result3))
print("\n" + "="*70 + "\n")

# Ejemplo 4: Torre de destilación
print("EJEMPLO 4: Torre de Destilación con Platos")
print("-"*70)

result4 = calculate_cost_updated(
    equipment_name="Tower - Tray and Packed",
    size_param_value=50,  # m³ de volumen
    material="CS",
    pressure_barg=2,
    diameter_m=2.0,  # m de diámetro
    target_year=2024
)

print(format_cost_result(result4))
print("\n" + "="*70 + "\n")

# Mostrar equipos disponibles por categoría
print("EQUIPOS DISPONIBLES EN LA HERRAMIENTA")
print("-"*70)

equipment_by_cat = get_equipment_by_category()
for category, equipments in equipment_by_cat.items():
    print(f"\n{category}:")
    for eq in equipments:
        print(f"  - {eq}")

print("\n" + "="*70)
print("Para usar la interfaz web interactiva, ejecute: streamlit run app.py")
print("="*70)
