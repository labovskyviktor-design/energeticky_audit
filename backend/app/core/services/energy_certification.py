
from app.core.models.certification import (
    EnergyCertificationInput,
    EnergyCertResult,
    EnergyClass,
    EnergyFactor,
    EnergyCarrier
)

def get_default_factors() -> dict[EnergyCarrier, EnergyFactor]:
    # Default SK factors (approximate from decree 324/2016 for typical carriers)
    return {
        EnergyCarrier.ELECTRICITY: EnergyFactor(carrier=EnergyCarrier.ELECTRICITY, f_prim=2.2, f_co2=0.167),
        EnergyCarrier.NATURAL_GAS: EnergyFactor(carrier=EnergyCarrier.NATURAL_GAS, f_prim=1.1, f_co2=0.220),
        EnergyCarrier.LPG: EnergyFactor(carrier=EnergyCarrier.LPG, f_prim=1.2, f_co2=0.240),
        EnergyCarrier.COAL: EnergyFactor(carrier=EnergyCarrier.COAL, f_prim=1.1, f_co2=0.360),
        EnergyCarrier.WOOD: EnergyFactor(carrier=EnergyCarrier.WOOD, f_prim=0.1, f_co2=0.020),
        EnergyCarrier.PELLETS: EnergyFactor(carrier=EnergyCarrier.PELLETS, f_prim=0.2, f_co2=0.020),
        EnergyCarrier.DISTRICT_HEATING: EnergyFactor(carrier=EnergyCarrier.DISTRICT_HEATING, f_prim=1.3, f_co2=0.300), 
        EnergyCarrier.PHOTOVOLTAICS: EnergyFactor(carrier=EnergyCarrier.PHOTOVOLTAICS, f_prim=2.2, f_co2=0.0) # Deduction factor same as electricity grid
    }

def calculate_certification(data: EnergyCertificationInput) -> EnergyCertResult:
    # 1. Resolve factors
    defaults = get_default_factors()
    active_factors = defaults.copy()
    
    # Override defaults with user provided factors
    if data.factors:
        for f in data.factors:
            active_factors[f.carrier] = f

    # Helper to get factor
    def get_f(carrier: EnergyCarrier):
        return active_factors.get(carrier, defaults.get(EnergyCarrier.ELECTRICITY)) # Fallback electric

    # 2. Assign carriers for inputs (simplification: assume user selects carrier per system in UI, 
    # but for now we need to know WHICH carrier corresponds to heating/dhw)
    # Since inputs from Ch3/Ch4 are just totals, we might need extra info or just assume main carrier.
    # To properly implement, we should probably add 'carrier' field to input for each demand type eventually.
    # FOR NOW: Let's assume standard carriers or pass them in input? 
    # Wait, the input model I created doesn't specify carrier for heating/dhw.
    # Let's fix this by assuming Natural Gas for HVAC as per context or relying on defaults, 
    # OR better: The user should specify the carrier in the frontend and pass factors for it.
    # Actually, let's assume the 'factors' list contains the relevant carriers used.
    # But which demand uses which carrier?
    
def calculate_certification(data: EnergyCertificationInput) -> EnergyCertResult:
    # 1. Resolve factors
    defaults = get_default_factors()
    active_factors = defaults.copy()
    
    # Override defaults with user provided factors
    if data.factors:
        for f in data.factors:
            active_factors[f.carrier] = f

    # Helper to get factor
    def get_f(carrier: EnergyCarrier) -> EnergyFactor:
        return active_factors.get(carrier, defaults.get(EnergyCarrier.ELECTRICITY)) # Fallback

    # 2. Accumulate Delivered Energy per Carrier
    # We map specific demands to their carriers
    # Lighting, Cooling, Ventilation, PV are assumed ELECTRICITY
    
    del_heating = data.heating_demand
    del_dhw = data.dhw_demand
    del_lighting = data.lighting_demand
    del_cooling = data.cooling_demand
    del_ventilation = data.ventilation_demand
    del_pv = data.pv_production # This is production, treated as deduction
    
    # 3. Calculate Primary Energy components
    # Heating
    f_heat = get_f(data.heating_carrier)
    prim_heating = del_heating * f_heat.f_prim
    co2_heating = del_heating * f_heat.f_co2
    
    # DHW
    f_dhw = get_f(data.dhw_carrier)
    prim_dhw = del_dhw * f_dhw.f_prim
    co2_dhw = del_dhw * f_dhw.f_co2
    
    # Electricity based (Lighting, Cooling, Vent)
    f_el = get_f(EnergyCarrier.ELECTRICITY)
    
    prim_lighting = del_lighting * f_el.f_prim
    co2_lighting = del_lighting * f_el.f_co2
    
    prim_cooling = del_cooling * f_el.f_prim
    co2_cooling = del_cooling * f_el.f_co2
    
    prim_ventilation = del_ventilation * f_el.f_prim
    co2_ventilation = del_ventilation * f_el.f_co2
    
    # PV Deduction (Primary Energy only usually, but depends on method)
    # Method: deduct primary energy equivalent of produced electricity
    f_pv_deduction = get_f(EnergyCarrier.PHOTOVOLTAICS).f_prim
    prim_pv_ded = del_pv * f_pv_deduction
    # CO2 deduction? Usually yes if it displaces grid
    # For now assume f_co2 for PV is 0.0 effectively in default, 
    # but if we displace grid, we should use grid factor?
    # Let's stick to the factor defined for PV (which was 2.2 deduction effectively in inputs if treated as grid displacement)
    # The default for PV was f_prim=2.2, f_co2=0.0 in my mock.
    # Actually, if we export, it displaces grid emissions. 
    # Let's assume we deduct CO2 based on grid electricity factor (0.167)
    co2_pv_ded = del_pv * f_el.f_co2 
    
    # 4. Totals
    total_delivered = (del_heating + del_dhw + del_lighting + del_cooling + del_ventilation) # PV is not "delivered" consumed, it reduces delivered? 
    # Use delivered as consumed from grid? Or total demand?
    # Standard: Total Delivered = Demand from systems. 
    # Primary = (Demand * f) - (PV * f)
    
    total_primary = (prim_heating + prim_dhw + prim_lighting + prim_cooling + prim_ventilation) - prim_pv_ded
    if total_primary < 0: total_primary = 0
    
    total_co2_val = (co2_heating + co2_dhw + co2_lighting + co2_cooling + co2_ventilation) - co2_pv_ded
    if total_co2_val < 0: total_co2_val = 0
    
    # 5. Specific Primary Energy
    if data.floor_area > 0:
        specific_primary = total_primary / data.floor_area
    else:
        specific_primary = 0.0
        
    # 6. Classification
    # Scale for Family Houses (Typical SK A0 <= 54)
    # We should support other scales but for MVP we hardcode or pick based on category
    # Simple scale:
    # class: (min, max)
    # A0: < 54
    # A1: 55 - 108
    # B: 109 - 216
    # C: 217 - 324
    # D: 325 - 432
    # E: 433 - 540
    # F: 541 - 648
    # G: > 648
    
    energy_class = EnergyClass.G
    val = specific_primary
    
    # This scale is for Global Indicator (Primary Energy)
    if val <= 54: energy_class = EnergyClass.A0
    elif val <= 108: energy_class = EnergyClass.A1
    elif val <= 216: energy_class = EnergyClass.B
    elif val <= 324: energy_class = EnergyClass.C
    elif val <= 432: energy_class = EnergyClass.D
    elif val <= 540: energy_class = EnergyClass.E
    elif val <= 648: energy_class = EnergyClass.F
    else: energy_class = EnergyClass.G
    
    return EnergyCertResult(
        del_heating=del_heating,
        del_dhw=del_dhw,
        del_lighting=del_lighting,
        del_cooling=del_cooling,
        del_ventilation=del_ventilation,
        total_delivered=total_delivered,
        
        prim_heating=prim_heating,
        prim_dhw=prim_dhw,
        prim_lighting=prim_lighting,
        prim_cooling=prim_cooling,
        prim_ventilation=prim_ventilation,
        prim_pv_deduction=prim_pv_ded,
        total_primary=total_primary,
        
        specific_primary=specific_primary,
        total_co2=total_co2_val / 1000.0, # Convert kg -> t ? No, factors are t/MWh = kg/kWh !
        # Wait: factor 0.167 t/MWh = 167 kg/MWh = 0.167 kg/kWh
        # So inputs in kWh * 0.167 => kg CO2.
        # Result defined as "Tonnes CO2/year" in model description?
        # Let's check model field description: "Tonnes CO2/year"
        # So we divide by 1000.
        
        energy_class=energy_class
    )
