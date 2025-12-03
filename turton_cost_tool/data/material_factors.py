"""
Material Factors (FM) from Turton 5th Edition - Table A.3 and Figure A.18
"""

# Material factors extracted from Figure A.18
# Format: {equipment_type: {material: FM_value}}

MATERIAL_FACTORS = {
    # HEAT EXCHANGERS (ID 1-17 from Table A.3)
    "Heat Exchanger - Double Pipe": {
        "CS shell/CS tube": 1.0,
        "CS shell/Cu tube": 1.4,
        "Cu shell/Cu tube": 1.8,
        "CS shell/SS tube": 2.7,
        "SS shell/SS tube": 4.0,
        "CS shell/Ni alloy tube": 4.7,
        "Ni alloy shell/Ni alloy tube": 7.2,
        "CS shell/Ti tube": 6.3,
        "Ti shell/Ti tube": 9.6
    },
    "Heat Exchanger - Fixed Tube Sheet": {
        "CS shell/CS tube": 1.0,
        "CS shell/Cu tube": 1.4,
        "Cu shell/Cu tube": 1.8,
        "CS shell/SS tube": 2.7,
        "SS shell/SS tube": 4.0,
        "CS shell/Ni alloy tube": 4.7,
        "Ni alloy shell/Ni alloy tube": 7.2,
        "CS shell/Ti tube": 6.3,
        "Ti shell/Ti tube": 9.6
    },
    "Heat Exchanger - Floating Head": {
        "CS shell/CS tube": 1.0,
        "CS shell/Cu tube": 1.4,
        "Cu shell/Cu tube": 1.8,
        "CS shell/SS tube": 2.7,
        "SS shell/SS tube": 4.0,
        "CS shell/Ni alloy tube": 4.7,
        "Ni alloy shell/Ni alloy tube": 7.2,
        "CS shell/Ti tube": 6.3,
        "Ti shell/Ti tube": 9.6
    },
    "Heat Exchanger - U-Tube": {
        "CS shell/CS tube": 1.0,
        "CS shell/Cu tube": 1.4,
        "Cu shell/Cu tube": 1.8,
        "CS shell/SS tube": 2.7,
        "SS shell/SS tube": 4.0,
        "CS shell/Ni alloy tube": 4.7,
        "Ni alloy shell/Ni alloy tube": 7.2,
        "CS shell/Ti tube": 6.3,
        "Ti shell/Ti tube": 9.6
    },
    "Heat Exchanger - Kettle Reboiler": {
        "CS shell/CS tube": 1.0,
        "CS shell/Cu tube": 1.4,
        "Cu shell/Cu tube": 1.8,
        "CS shell/SS tube": 2.7,
        "SS shell/SS tube": 4.0,
        "CS shell/Ni alloy tube": 4.7,
        "Ni alloy shell/Ni alloy tube": 7.2,
        "CS shell/Ti tube": 6.3,
        "Ti shell/Ti tube": 9.6
    },
    "Heat Exchanger - Air Cooler": {
        "CS tube": 1.0,
        "Al tube": 1.2,
        "SS tube": 2.2
    },
    "Heat Exchanger - Flat Plate": {
        "CS": 1.0,
        "Cu": 1.5,
        "SS": 2.0,
        "Ni alloy": 2.7,
        "Ti": 4.4
    },
    
    # PROCESS VESSELS (ID 18-24 from Table A.3)
    "Vessel - Horizontal": {
        "CS": 1.0,
        "SS clad": 1.6,
        "SS": 2.9,
        "Ni alloy clad": 2.7,
        "Ni alloy": 4.7,
        "Ti clad": 4.0,
        "Ti": 7.4
    },
    "Vessel - Vertical": {
        "CS": 1.0,
        "SS clad": 1.6,
        "SS": 2.9,
        "Ni alloy clad": 2.7,
        "Ni alloy": 4.7,
        "Ti clad": 4.0,
        "Ti": 7.4
    },
    "Tower - Tray and Packed": {
        "CS": 1.0,
        "SS clad": 1.6,
        "SS": 2.9,
        "Ni alloy clad": 2.7,
        "Ni alloy": 4.7,
        "Ti clad": 4.0,
        "Ti": 7.4
    },
    
    # TANKS (Same as vessels, CS only typically)
    "Tank - API Fixed Roof": {
        "CS": 1.0
    },
    "Tank - API Floating Roof": {
        "CS": 1.0
    },
    
    # PUMPS (ID 25-40 from Table A.3)
    "Pump - Reciprocating": {
        "Cast iron": 1.0,
        "Carbon steel": 1.5,
        "Cu alloy": 1.8,
        "SS": 2.7,
        "Ni alloy": 4.8,
        "Ti": 10.9
    },
    "Pump - Positive Displacement": {
        "Cast iron": 1.0,
        "Carbon steel": 1.5,
        "Cu alloy": 1.8,
        "SS": 2.7,
        "Ni alloy": 4.8,
        "Ti": 10.9
    },
    "Pump - Centrifugal": {
        "Cast iron": 1.0,
        "Carbon steel": 1.5,
        "SS": 2.0,
        "Ni alloy": 5.0
    },
    
    # REACTORS (use same factors as vessels)
    "Reactor - Autoclave": {
        "CS": 1.0,
        "SS clad": 1.6,
        "SS": 2.9,
        "Ni alloy clad": 2.7,
        "Ni alloy": 4.7,
        "Ti clad": 4.0,
        "Ti": 7.4
    },
    "Reactor - Fermenter": {
        "CS": 1.0,
        "SS clad": 1.6,
        "SS": 2.9,
        "Ni alloy clad": 2.7,
        "Ni alloy": 4.7,
        "Ti clad": 4.0,
        "Ti": 7.4
    },
    "Reactor - Jacketed Agitated": {
        "CS": 1.0,
        "SS clad": 1.6,
        "SS": 2.9,
        "Ni alloy clad": 2.7,
        "Ni alloy": 4.7,
        "Ti clad": 4.0,
        "Ti": 7.4
    },
    "Reactor - Jacketed Non-Agitated": {
        "CS": 1.0,
        "SS clad": 1.6,
        "SS": 2.9,
        "Ni alloy clad": 2.7,
        "Ni alloy": 4.7,
        "Ti clad": 4.0,
        "Ti": 7.4
    },
    
    # COMPRESSORS - No material factors (FM = 1.0)
    "Compressor - Centrifugal/Axial/Reciprocating": {
        "CS": 1.0,
        "SS": 2.5,
        "Ni alloy": 5.0
    },
    "Compressor - Rotary": {
        "CS": 1.0,
        "SS": 2.5,
        "Ni alloy": 5.0
    },
    
    # FURNACES - Material factor typically CS tubes or alloy
    "Furnace - Reformer": {
        "CS tube": 1.0,
        "Alloy steel tube": 1.4,
        "SS tube": 1.7
    },
    "Furnace - Pyrolysis": {
        "CS tube": 1.0,
        "Alloy steel tube": 1.4,
        "SS tube": 1.7
    },
    "Furnace - Nonreactive Fired Heater": {
        "CS tube": 1.0,
        "Alloy steel tube": 1.4,
        "SS tube": 1.7
    },
    
    # TURBINES - No material factors typically
    "Turbine - Steam": {
        "CS": 1.0,
        "SS": 1.4,
        "Ni alloy": 2.1
    },
    "Turbine - Axial Gas": {
        "CS": 1.0,
        "SS": 1.4,
        "Ni alloy": 2.1
    },
    "Turbine - Radial Gas/Liquid Expander": {
        "CS": 1.0,
        "SS": 1.4,
        "Ni alloy": 2.1
    },
}

def get_materials_for_equipment(equipment_name):
    """Returns list of available materials for given equipment"""
    if equipment_name in MATERIAL_FACTORS:
        return list(MATERIAL_FACTORS[equipment_name].keys())
    return ["CS"]  # Default carbon steel

def get_material_factor(equipment_name, material):
    """Returns material factor for given equipment and material"""
    if equipment_name in MATERIAL_FACTORS:
        if material in MATERIAL_FACTORS[equipment_name]:
            return MATERIAL_FACTORS[equipment_name][material]
    return 1.0  # Default to 1.0 if not found
