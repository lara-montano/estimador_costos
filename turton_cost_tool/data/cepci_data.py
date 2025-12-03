"""
Chemical Engineering Plant Cost Index (CEPCI) Data
Historical values for cost updating

Base year for Turton 5th edition: 2001, CEPCI = 397
"""

# Historical CEPCI values (annual averages)
# Source: Chemical Engineering Magazine
CEPCI_DATA = {
    2001: 397.0,   # Base year for Turton 5th edition
    2002: 395.6,
    2003: 402.0,
    2004: 444.2,
    2005: 468.2,
    2006: 499.6,
    2007: 525.4,
    2008: 575.4,
    2009: 521.9,
    2010: 550.8,
    2011: 585.7,
    2012: 584.6,
    2013: 567.3,
    2014: 576.1,
    2015: 556.8,
    2016: 541.7,
    2017: 567.5,
    2018: 603.1,
    2019: 607.5,
    2020: 596.2,
    2021: 708.0,
    2022: 816.0,
    2023: 801.3,
    2024: 815.0,  # Preliminary
}

BASE_YEAR = 2001
BASE_CEPCI = 397.0

def get_cepci(year):
    """
    Get CEPCI value for a specific year
    
    Args:
        year: Year (integer)
    
    Returns:
        CEPCI value for that year, or None if not available
    """
    return CEPCI_DATA.get(year)

def get_latest_year():
    """Returns the most recent year with CEPCI data"""
    return max(CEPCI_DATA.keys())

def get_latest_cepci():
    """Returns the most recent CEPCI value"""
    latest_year = get_latest_year()
    return CEPCI_DATA[latest_year]

def update_cost(cost_base, year_base, year_target):
    """
    Update cost from base year to target year using CEPCI
    
    Args:
        cost_base: Cost in base year
        year_base: Base year
        year_target: Target year
    
    Returns:
        Updated cost in target year
    """
    if year_base not in CEPCI_DATA or year_target not in CEPCI_DATA:
        return None
    
    cepci_base = CEPCI_DATA[year_base]
    cepci_target = CEPCI_DATA[year_target]
    
    cost_target = cost_base * (cepci_target / cepci_base)
    
    return cost_target

def get_available_years():
    """Returns sorted list of years with CEPCI data"""
    return sorted(CEPCI_DATA.keys())
