from app.core.models.certificate import CertificateInput, CertificateResult, GradeResult

def get_grade_heating(val: float) -> str:
    if val <= 27: return "A"
    if val <= 53: return "B"
    if val <= 80: return "C"
    if val <= 106: return "D"
    if val <= 133: return "E"
    if val <= 159: return "F"
    return "G"

def get_grade_dhw(val: float) -> str:
    if val <= 13: return "A"
    if val <= 26: return "B"
    if val <= 39: return "C"
    if val <= 52: return "D"
    if val <= 65: return "E"
    if val <= 78: return "F"
    return "G"

def get_grade_total(val: float) -> str:
    if val <= 40: return "A"
    if val <= 79: return "B"
    if val <= 119: return "C"
    if val <= 158: return "D"
    if val <= 198: return "E"
    if val <= 237: return "F"
    return "G"

def get_grade_primary(val: float) -> str:
    if val <= 32: return "A0"
    if val <= 63: return "A1"
    if val <= 126: return "B"
    if val <= 189: return "C"
    if val <= 252: return "D"
    if val <= 315: return "E"
    if val <= 378: return "F"
    return "G"

def generate_certificate(data: CertificateInput) -> CertificateResult:
    # 1. Total Delivered Energy components
    total_heating_kwh = (
        data.heating_demand + 
        data.heating_emission_loss + 
        data.heating_distribution_loss + 
        data.heating_generation_loss - 
        data.dhw_recoverable_loss
    )
    if total_heating_kwh < 0:
        total_heating_kwh = 0
        
    total_dhw_kwh = (
        data.dhw_demand + 
        data.dhw_distribution_loss + 
        data.dhw_generation_loss
    )
    
    total_aux_kwh = data.heating_aux_energy + data.dhw_aux_energy
    
    # Let's say we attribute auxiliary electricity entirely to "Electricity", 
    # but the primary heat source to whatever was provided.
    # So Total Delivered for Heating includes the heating source + its aux.
    delivered_heating = total_heating_kwh + data.heating_aux_energy
    delivered_dhw = total_dhw_kwh + data.dhw_aux_energy
    
    spec_heating = delivered_heating / data.total_area
    spec_dhw = delivered_dhw / data.total_area
    spec_total = (delivered_heating + delivered_dhw) / data.total_area
    
    # 2. Primary Energy calculation (kWh/rok)
    # Heating primary
    pe_heating_source = total_heating_kwh * data.heating_source.pe_factor
    pe_heating_aux = data.heating_aux_energy * 2.2 # electricity PE factor
    
    # DHW primary
    pe_dhw_source = total_dhw_kwh * data.dhw_source.pe_factor
    pe_dhw_aux = data.dhw_aux_energy * 2.2 # electricity PE factor
    
    total_pe_kwh = pe_heating_source + pe_heating_aux + pe_dhw_source + pe_dhw_aux
    spec_pe = total_pe_kwh / data.total_area
    
    # 3. CO2 calculation (kg/rok)
    co2_heating_source = total_heating_kwh * data.heating_source.co2_factor
    co2_heating_aux = data.heating_aux_energy * 0.167 # electricity CO2 factor (approx 0.167 based on SK standard)
    
    co2_dhw_source = total_dhw_kwh * data.dhw_source.co2_factor
    co2_dhw_aux = data.dhw_aux_energy * 0.167
    
    total_co2_kg = co2_heating_source + co2_dhw_source + co2_heating_aux + co2_dhw_aux
    spec_co2 = total_co2_kg / data.total_area
    
    return CertificateResult(
        heating_delivered_energy=round(delivered_heating, 0),
        heating_grade=GradeResult(value_kwh_m2=round(spec_heating, 1), grade=get_grade_heating(spec_heating)),
        
        dhw_delivered_energy=round(delivered_dhw, 0),
        dhw_grade=GradeResult(value_kwh_m2=round(spec_dhw, 1), grade=get_grade_dhw(spec_dhw)),
        
        total_aux_energy=round(total_aux_kwh, 0),
        
        total_delivered_energy=round(delivered_heating + delivered_dhw, 0),
        total_grade=GradeResult(value_kwh_m2=round(spec_total, 1), grade=get_grade_total(spec_total)),
        
        primary_energy=round(total_pe_kwh, 0),
        primary_energy_grade=GradeResult(value_kwh_m2=round(spec_pe, 1), grade=get_grade_primary(spec_pe)),
        
        total_co2_kg=round(total_co2_kg, 1),
        specific_co2=round(spec_co2, 2)
    )
