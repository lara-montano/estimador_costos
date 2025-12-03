"""
Main calculation functions for equipment cost estimation
Based on Turton 5th Edition correlations
"""

import math
from data import (
    EQUIPMENT_DATA, 
    BASE_CEPCI, 
    get_material_factor,
    calculate_pressure_factor,
    update_cost,
    get_cepci
)

def calculate_base_cost(equipment_name, size_param_value):
    """
    Calculate base purchased cost (Cp°) using Equation A.1
    log10(Cp°) = K1 + K2*log10(A) + K3*[log10(A)]^2
    
    Args:
        equipment_name: Name of equipment
        size_param_value: Value of size parameter (area, volume, power, etc.)
    
    Returns:
        tuple: (Cp_base, valid, message)
            Cp_base: Base cost in 2001 USD
            valid: Boolean indicating if calculation is valid
            message: Warning message if outside range
    """
    if equipment_name not in EQUIPMENT_DATA:
        return None, False, "Equipment not found in database"
    
    equip_data = EQUIPMENT_DATA[equipment_name]
    K1 = equip_data["K1"]
    K2 = equip_data["K2"]
    K3 = equip_data["K3"]
    min_size = equip_data["min_size"]
    max_size = equip_data["max_size"]
    
    A = size_param_value
    
    # Check if within valid range
    message = ""
    valid = True
    if A < min_size:
        message = f"⚠️ Size below minimum ({min_size} {equip_data['units']}). Extrapolating - use with caution."
        valid = False
    elif A > max_size:
        message = f"⚠️ Size above maximum ({max_size} {equip_data['units']}). Extrapolating - use with caution."
        valid = False
    
    # Calculate using Equation A.1
    try:
        log_A = math.log10(A)
        log_Cp = K1 + K2 * log_A + K3 * (log_A ** 2)
        Cp_base = 10 ** log_Cp
        
        return Cp_base, valid, message
    except Exception as e:
        return None, False, f"Calculation error: {str(e)}"

def calculate_purchased_cost(equipment_name, size_param_value, material="CS", 
                            pressure_barg=0, diameter_m=None):
    """
    Calculate purchased cost (Cp) with material and pressure factors
    Cp = Cp° × FM × FP
    
    Args:
        equipment_name: Name of equipment
        size_param_value: Value of size parameter
        material: Material of construction (default: "CS")
        pressure_barg: Operating pressure in bar gauge (default: 0)
        diameter_m: Diameter in meters for vessels (default: None)
    
    Returns:
        dict: Dictionary with calculation results
    """
    # Calculate base cost
    Cp_base, valid, message = calculate_base_cost(equipment_name, size_param_value)
    
    if Cp_base is None:
        return {
            "success": False,
            "error": message,
            "Cp_base_2001": None,
            "FM": None,
            "FP": None,
            "Cp_2001": None,
            "valid_range": False
        }
    
    # Get material factor
    FM = get_material_factor(equipment_name, material)
    
    # Get pressure factor
    FP = calculate_pressure_factor(equipment_name, pressure_barg, diameter_m)
    
    # Calculate final purchased cost in 2001 USD
    Cp_2001 = Cp_base * FM * FP
    
    return {
        "success": True,
        "Cp_base_2001": Cp_base,
        "FM": FM,
        "FP": FP,
        "Cp_2001": Cp_2001,
        "valid_range": valid,
        "message": message,
        "base_year": 2001,
        "base_cepci": BASE_CEPCI
    }

def calculate_cost_updated(equipment_name, size_param_value, material="CS",
                          pressure_barg=0, diameter_m=None, target_year=2024):
    """
    Calculate equipment cost updated to target year using CEPCI
    
    Args:
        equipment_name: Name of equipment
        size_param_value: Value of size parameter
        material: Material of construction
        pressure_barg: Operating pressure in bar gauge
        diameter_m: Diameter in meters for vessels
        target_year: Year to update cost to
    
    Returns:
        dict: Complete calculation results with updated cost
    """
    # Calculate purchased cost in 2001
    result = calculate_purchased_cost(equipment_name, size_param_value, 
                                     material, pressure_barg, diameter_m)
    
    if not result["success"]:
        return result
    
    # Update cost to target year
    Cp_2001 = result["Cp_2001"]
    
    cepci_target = get_cepci(target_year)
    if cepci_target is None:
        result["Cp_updated"] = None
        result["target_year"] = target_year
        result["target_cepci"] = None
        result["update_error"] = f"CEPCI data not available for year {target_year}"
    else:
        Cp_updated = Cp_2001 * (cepci_target / BASE_CEPCI)
        result["Cp_updated"] = Cp_updated
        result["target_year"] = target_year
        result["target_cepci"] = cepci_target
    
    return result

def format_cost_result(result):
    """
    Format calculation result as string for display
    
    Args:
        result: Dictionary from calculate_cost_updated
    
    Returns:
        str: Formatted result text
    """
    if not result["success"]:
        return f"❌ Error: {result['error']}"
    
    text = []
    text.append("="*60)
    text.append("COST CALCULATION RESULTS")
    text.append("="*60)
    text.append("")
    
    # Base calculations
    text.append(f"Base Cost (Cp°, {result['base_year']}): ${result['Cp_base_2001']:,.2f} USD")
    text.append(f"Material Factor (FM): {result['FM']:.3f}")
    text.append(f"Pressure Factor (FP): {result['FP']:.3f}")
    text.append("")
    text.append(f"Purchased Cost ({result['base_year']}): ${result['Cp_2001']:,.2f} USD")
    text.append(f"  [CEPCI = {result['base_cepci']}]")
    text.append("")
    
    # Updated cost
    if result.get("Cp_updated"):
        text.append(f"Updated Cost ({result['target_year']}): ${result['Cp_updated']:,.2f} USD")
        text.append(f"  [CEPCI = {result['target_cepci']}]")
        
        # Cost increase
        increase_pct = ((result['Cp_updated'] / result['Cp_2001']) - 1) * 100
        text.append(f"  Cost increase from 2001: {increase_pct:+.1f}%")
    else:
        text.append(f"⚠️ {result.get('update_error', 'Cost update unavailable')}")
    
    text.append("")
    
    # Warnings
    if not result["valid_range"]:
        text.append("⚠️ WARNING: " + result["message"])
    
    text.append("="*60)
    
    return "\n".join(text)
