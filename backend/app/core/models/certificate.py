from typing import Optional
from pydantic import BaseModel, Field

from app.core.models.heating_system import FuelType

class CertificateEnergySource(BaseModel):
    """Energetický nosič a jeho parametre pre výpočet PE a CO2."""
    fuel_type: FuelType
    pe_factor: float = Field(default=1.1, description="Faktor primárnej energie")
    co2_factor: float = Field(default=0.202, description="Faktor emisií CO2 (kg/kWh)")

class CertificateInput(BaseModel):
    """Vstupné dáta pre výpočet energetického certifikátu (Kapitola 9)."""
    # Zákadné údaje o budove
    building_name: str = Field(default="Bytový dom")
    total_area: float = Field(description="Celková podlahová plocha Ab (m²)")
    
    # Vykurovanie (Heating) - kWh/rok
    heating_demand: float = Field(description="Potreba tepla na vykurovanie QH")
    heating_emission_loss: float = Field(description="Strata z odovzdávania Qem,ls")
    heating_distribution_loss: float = Field(description="Strata z rozvodu QH,dis,ls,an")
    heating_generation_loss: float = Field(description="Strata z výroby QH,g")
    heating_aux_energy: float = Field(description="Vlastná elektrická energia WH,dis,aux,an")
    heating_source: CertificateEnergySource
    
    # Príprava teplej vody (DHW) - kWh/rok
    dhw_demand: float = Field(description="Potreba tepla na prípravu TV QW")
    dhw_distribution_loss: float = Field(description="Strata z distribúcie QW,d")
    dhw_generation_loss: float = Field(description="Strata z výroby QW,g")
    dhw_aux_energy: float = Field(description="Vlastná elektrická energia (čerpadlo) Wd,pump")
    dhw_source: CertificateEnergySource
    
    # Spätne získaná strata
    dhw_recoverable_loss: float = Field(
        default=0.0, 
        description="Spätne získateľná tepelná strata zo systému TV, ktorá znižuje potrebu tepla na vykurovanie."
    )

class GradeResult(BaseModel):
    """Zatriedenie do energetickej triedy s príslušnou hodnotou."""
    value_kwh_m2: float = Field(description="Špecifická hodnota v kWh/(m2.a)")
    grade: str = Field(description="Energetická trieda (A0, A1, B, C, D, E, F, G)")

class CertificateResult(BaseModel):
    """Výsledok energetickej certifikácie."""
    # Vykurovanie
    heating_delivered_energy: float = Field(description="Celková dodaná energia na vykurovanie (kWh/rok)")
    heating_grade: GradeResult
    
    # TV
    dhw_delivered_energy: float = Field(description="Celková dodaná energia na prípravu TV (kWh/rok)")
    dhw_grade: GradeResult
    
    # Elektrická energia spolu (aux)
    total_aux_energy: float = Field(description="Súčet pomocnej elektrickej energie (kWh/rok)")
    
    # Celková energia
    total_delivered_energy: float = Field(description="Celková dodaná energia budovy (kWh/rok)")
    total_grade: GradeResult
    
    # Primárna energia a CO2
    primary_energy: float = Field(description="Primárna energia (kWh/rok)")
    primary_energy_grade: GradeResult
    total_co2_kg: float = Field(description="Celkové emisie CO2 (kg/rok)")
    specific_co2: float = Field(description="Merné emisie CO2 (kg/m2.a)")
