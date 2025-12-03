"""
Pressure Factors (FP) from Turton 5th Edition - Equations A.2, A.3 and Table A.2
"""

import math

# Constants for pressure vessel equation (A.2)
S_CARBON_STEEL = 944  # bar (maximum allowable stress)
E_WELD = 0.9  # weld efficiency
T_MIN = 0.0063  # m (minimum thickness, 1/4 inch)
CA = 0.00315  # m (corrosion allowance, 1/8 inch)

def calculate_vessel_pressure_factor(pressure_barg, diameter_m):
    """
    Calculate pressure factor for horizontal and vertical process vessels
    Using Equation A.2 from Turton
    
    Args:
        pressure_barg: Operating pressure in bar gauge
        diameter_m: Vessel diameter in meters
    
    Returns:
        FP: Pressure factor
    """
    P = pressure_barg
    D = diameter_m
    
    # For pressures less than -0.5 barg (vacuum)
    if P < -0.5:
        return 1.25
    
    # Calculate thickness and pressure factor
    numerator = P * D
    denominator = 2 * S_CARBON_STEEL * E_WELD - 1.2 * P
    
    if denominator <= 0:
        # High pressure case, use conservative factor
        return 3.0
    
    t = numerator / denominator + CA
    
    # If thickness less than minimum, FP = 1
    if t < T_MIN:
        return 1.0
    
    # Calculate FP
    FP = (t + CA) / (T_MIN + CA)
    
    return max(1.0, FP)

# Pressure factor coefficients from Table A.2
# Format: {equipment: [(C1, C2, C3, P_min, P_max), ...]}
PRESSURE_COEFFICIENTS = {
    # HEAT EXCHANGERS
    "Heat Exchanger - Fixed Tube Sheet": [
        (0, 0, 0, -float('inf'), 5),
        (0.03881, -0.11272, 0.08183, 5, 140)
    ],
    "Heat Exchanger - Floating Head": [
        (0, 0, 0, -float('inf'), 5),
        (0.03881, -0.11272, 0.08183, 5, 140)
    ],
    "Heat Exchanger - U-Tube": [
        (0, 0, 0, -float('inf'), 5),
        (0.03881, -0.11272, 0.08183, 5, 140)
    ],
    "Heat Exchanger - Kettle Reboiler": [
        (0, 0, 0, -float('inf'), 5),
        (0.03881, -0.11272, 0.08183, 5, 140)
    ],
    "Heat Exchanger - Double Pipe": [
        (0, 0, 0, -float('inf'), 40),
        (0.6072, -0.9120, 0.3327, 40, 100),
        (13.1467, -12.6574, 3.0705, 100, 300)
    ],
    "Heat Exchanger - Flat Plate": [
        (0, 0, 0, -float('inf'), 19)
    ],
    "Heat Exchanger - Air Cooler": [
        (0, 0, 0, -float('inf'), 10),
        (-0.1250, 0.15361, -0.02861, 10, 100)
    ],
    
    # PUMPS
    "Pump - Reciprocating": [
        (0, 0, 0, -float('inf'), 10),
        (-0.245382, 0.259016, -0.01363, 10, 100)
    ],
    "Pump - Positive Displacement": [
        (0, 0, 0, -float('inf'), 10),
        (-0.245382, 0.259016, -0.01363, 10, 100)
    ],
    "Pump - Centrifugal": [
        (0, 0, 0, -float('inf'), 10),
        (-0.3935, 0.3957, -0.00226, 10, 100)
    ],
    
    # FURNACES
    "Furnace - Reformer": [
        (0, 0, 0, -float('inf'), 10),
        (0.1405, -0.2698, 0.1293, 10, 200)
    ],
    "Furnace - Pyrolysis": [
        (0, 0, 0, -float('inf'), 10),
        (0.1017, -0.1957, 0.09403, 10, 200)
    ],
    "Furnace - Nonreactive Fired Heater": [
        (0, 0, 0, -float('inf'), 10),
        (0.1347, -0.2368, 0.1021, 10, 200)
    ],
    
    # TANKS (low pressure only)
    "Tank - API Fixed Roof": [
        (0, 0, 0, -float('inf'), 0.07)
    ],
    "Tank - API Floating Roof": [
        (0, 0, 0, -float('inf'), 0.07)
    ],
    
    # COMPRESSORS (no pressure factor)
    "Compressor - Centrifugal/Axial/Reciprocating": [
        (0, 0, 0, -float('inf'), float('inf'))
    ],
    "Compressor - Rotary": [
        (0, 0, 0, -float('inf'), float('inf'))
    ],
    
    # TURBINES (no pressure factor)
    "Turbine - Steam": [
        (0, 0, 0, -float('inf'), float('inf'))
    ],
    "Turbine - Axial Gas": [
        (0, 0, 0, -float('inf'), float('inf'))
    ],
    "Turbine - Radial Gas/Liquid Expander": [
        (0, 0, 0, -float('inf'), float('inf'))
    ],
}

def calculate_pressure_factor(equipment_name, pressure_barg, diameter_m=None):
    """
    Calculate pressure factor for equipment using Equation A.3
    FP = C1 + C2*log10(P+1) + C3*[log10(P+1)]^2
    
    For vessels, uses Equation A.2 instead
    
    Args:
        equipment_name: Name of equipment
        pressure_barg: Operating pressure in bar gauge
        diameter_m: Diameter in meters (required for vessels)
    
    Returns:
        FP: Pressure factor (always >= 1.0)
    """
    # Special case for vessels - use Equation A.2
    if equipment_name in ["Vessel - Horizontal", "Vessel - Vertical", 
                          "Tower - Tray and Packed",
                          "Reactor - Autoclave", "Reactor - Fermenter",
                          "Reactor - Jacketed Agitated", "Reactor - Jacketed Non-Agitated"]:
        if diameter_m is None:
            # Estimate diameter from volume if not provided
            # This is a rough estimate for educational purposes
            diameter_m = 1.0  # Default 1m diameter
        return calculate_vessel_pressure_factor(pressure_barg, diameter_m)
    
    # For other equipment, use table lookup
    if equipment_name not in PRESSURE_COEFFICIENTS:
        return 1.0
    
    P = pressure_barg
    
    # Find appropriate coefficient range
    coeffs = PRESSURE_COEFFICIENTS[equipment_name]
    C1, C2, C3 = 0, 0, 0
    
    for coeff_set in coeffs:
        c1, c2, c3, p_min, p_max = coeff_set
        if p_min <= P < p_max:
            C1, C2, C3 = c1, c2, c3
            break
    
    # If all coefficients are zero, FP = 1
    if C1 == 0 and C2 == 0 and C3 == 0:
        return 1.0
    
    # Calculate FP using Equation A.3
    log_term = math.log10(P + 1)
    FP = C1 + C2 * log_term + C3 * (log_term ** 2)
    
    return max(1.0, FP)

def get_pressure_range(equipment_name):
    """
    Returns the valid pressure range for equipment
    
    Returns:
        tuple: (min_pressure, max_pressure) in barg
    """
    if equipment_name not in PRESSURE_COEFFICIENTS:
        return (0, 100)  # Default range
    
    coeffs = PRESSURE_COEFFICIENTS[equipment_name]
    p_min = coeffs[0][3]
    p_max = coeffs[-1][4]
    
    if p_min == -float('inf'):
        p_min = -1
    if p_max == float('inf'):
        p_max = 200
    
    return (p_min, p_max)
