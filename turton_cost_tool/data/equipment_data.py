"""
Equipment Cost Data from Turton 5th Edition - Table A.1
Base year: 2001, CEPCI = 397

Equation: log10(Cp°) = K1 + K2*log10(A) + K3*[log10(A)]^2
where A is the capacity or size parameter for the equipment
"""

EQUIPMENT_DATA = {
    # HEAT EXCHANGERS
    "Heat Exchanger - Floating Head": {
        "K1": 4.8306, "K2": -0.8509, "K3": 0.3187,
        "size_param": "Area", "units": "m²", "min_size": 10, "max_size": 1000,
        "category": "Heat Exchangers"
    },
    "Heat Exchanger - Fixed Tube Sheet": {
        "K1": 4.3247, "K2": -0.3030, "K3": 0.1634,
        "size_param": "Area", "units": "m²", "min_size": 10, "max_size": 1000,
        "category": "Heat Exchangers"
    },
    "Heat Exchanger - U-Tube": {
        "K1": 4.1884, "K2": -0.2503, "K3": 0.1974,
        "size_param": "Area", "units": "m²", "min_size": 10, "max_size": 1000,
        "category": "Heat Exchangers"
    },
    "Heat Exchanger - Kettle Reboiler": {
        "K1": 4.4646, "K2": -0.5277, "K3": 0.3955,
        "size_param": "Area", "units": "m²", "min_size": 10, "max_size": 100,
        "category": "Heat Exchangers"
    },
    "Heat Exchanger - Air Cooler": {
        "K1": 4.0336, "K2": 0.2341, "K3": 0.0497,
        "size_param": "Area", "units": "m²", "min_size": 10, "max_size": 10000,
        "category": "Heat Exchangers"
    },
    "Heat Exchanger - Double Pipe": {
        "K1": 3.3444, "K2": 0.2745, "K3": -0.0472,
        "size_param": "Area", "units": "m²", "min_size": 1, "max_size": 10,
        "category": "Heat Exchangers"
    },
    "Heat Exchanger - Flat Plate": {
        "K1": 4.6656, "K2": -0.1557, "K3": 0.1547,
        "size_param": "Area", "units": "m²", "min_size": 10, "max_size": 1000,
        "category": "Heat Exchangers"
    },
    
    # TOWERS
    "Tower - Tray and Packed": {
        "K1": 3.4974, "K2": 0.4485, "K3": 0.1074,
        "size_param": "Volume", "units": "m³", "min_size": 0.3, "max_size": 520,
        "category": "Towers"
    },
    
    # REACTORS
    "Reactor - Autoclave": {
        "K1": 4.5587, "K2": 0.2986, "K3": 0.0020,
        "size_param": "Volume", "units": "m³", "min_size": 1, "max_size": 15,
        "category": "Reactors"
    },
    "Reactor - Fermenter": {
        "K1": 4.1052, "K2": 0.5320, "K3": -0.0005,
        "size_param": "Volume", "units": "m³", "min_size": 0.1, "max_size": 35,
        "category": "Reactors"
    },
    "Reactor - Jacketed Agitated": {
        "K1": 4.1052, "K2": 0.5320, "K3": -0.0005,
        "size_param": "Volume", "units": "m³", "min_size": 0.1, "max_size": 35,
        "category": "Reactors"
    },
    "Reactor - Jacketed Non-Agitated": {
        "K1": 3.3496, "K2": 0.7235, "K3": 0.0025,
        "size_param": "Volume", "units": "m³", "min_size": 5, "max_size": 45,
        "category": "Reactors"
    },
    
    # VESSELS
    "Vessel - Horizontal": {
        "K1": 3.5565, "K2": 0.3776, "K3": 0.0905,
        "size_param": "Volume", "units": "m³", "min_size": 0.1, "max_size": 628,
        "category": "Vessels"
    },
    "Vessel - Vertical": {
        "K1": 3.4974, "K2": 0.4485, "K3": 0.1074,
        "size_param": "Volume", "units": "m³", "min_size": 0.3, "max_size": 520,
        "category": "Vessels"
    },
    
    # TANKS
    "Tank - API Fixed Roof": {
        "K1": 4.8509, "K2": -0.3973, "K3": 0.1445,
        "size_param": "Volume", "units": "m³", "min_size": 90, "max_size": 30000,
        "category": "Tanks"
    },
    "Tank - API Floating Roof": {
        "K1": 5.9567, "K2": -0.7585, "K3": 0.1749,
        "size_param": "Volume", "units": "m³", "min_size": 1000, "max_size": 40000,
        "category": "Tanks"
    },
    
    # PUMPS
    "Pump - Centrifugal": {
        "K1": 3.3892, "K2": 0.0536, "K3": 0.1538,
        "size_param": "Shaft Power", "units": "kW", "min_size": 1, "max_size": 300,
        "category": "Pumps"
    },
    "Pump - Reciprocating": {
        "K1": 3.8696, "K2": 0.3161, "K3": 0.1220,
        "size_param": "Shaft Power", "units": "kW", "min_size": 0.1, "max_size": 200,
        "category": "Pumps"
    },
    "Pump - Positive Displacement": {
        "K1": 3.4771, "K2": 0.1350, "K3": 0.1438,
        "size_param": "Shaft Power", "units": "kW", "min_size": 1, "max_size": 100,
        "category": "Pumps"
    },
    
    # COMPRESSORS
    "Compressor - Centrifugal/Axial/Reciprocating": {
        "K1": 2.2897, "K2": 1.3604, "K3": -0.1027,
        "size_param": "Fluid Power", "units": "kW", "min_size": 450, "max_size": 3000,
        "category": "Compressors"
    },
    "Compressor - Rotary": {
        "K1": 5.0355, "K2": -1.8002, "K3": 0.8253,
        "size_param": "Fluid Power", "units": "kW", "min_size": 18, "max_size": 950,
        "category": "Compressors"
    },
    
    # FURNACES
    "Furnace - Reformer": {
        "K1": 3.0680, "K2": 0.6597, "K3": 0.0194,
        "size_param": "Duty", "units": "kW", "min_size": 3000, "max_size": 100000,
        "category": "Furnaces"
    },
    "Furnace - Pyrolysis": {
        "K1": 2.3859, "K2": 0.9721, "K3": -0.0206,
        "size_param": "Duty", "units": "kW", "min_size": 3000, "max_size": 100000,
        "category": "Furnaces"
    },
    "Furnace - Nonreactive Fired Heater": {
        "K1": 7.3488, "K2": -1.1666, "K3": 0.2028,
        "size_param": "Duty", "units": "kW", "min_size": 1000, "max_size": 100000,
        "category": "Furnaces"
    },
    
    # TURBINES
    "Turbine - Steam": {
        "K1": 2.6259, "K2": 1.4398, "K3": -0.1776,
        "size_param": "Shaft Power", "units": "kW", "min_size": 70, "max_size": 7500,
        "category": "Turbines"
    },
    "Turbine - Axial Gas": {
        "K1": 2.7051, "K2": 1.4398, "K3": -0.1776,
        "size_param": "Fluid Power", "units": "kW", "min_size": 100, "max_size": 4000,
        "category": "Turbines"
    },
    "Turbine - Radial Gas/Liquid Expander": {
        "K1": 2.2476, "K2": 1.4965, "K3": -0.1618,
        "size_param": "Fluid Power", "units": "kW", "min_size": 100, "max_size": 1500,
        "category": "Turbines"
    },
}

# Base CEPCI for year 2001
BASE_CEPCI = 397
BASE_YEAR = 2001

def get_equipment_list():
    """Returns sorted list of equipment names"""
    return sorted(EQUIPMENT_DATA.keys())

def get_equipment_by_category():
    """Returns equipment organized by category"""
    categories = {}
    for equip_name, data in EQUIPMENT_DATA.items():
        cat = data["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(equip_name)
    return {k: sorted(v) for k, v in sorted(categories.items())}
