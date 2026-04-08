
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class EnergyClass(str, Enum):
    A0 = "A0"
    A1 = "A1"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"

class EnergyCarrier(str, Enum):
    ELECTRICITY = "electricity"
    NATURAL_GAS = "natural_gas"
    LPG = "lpg"
    COAL = "coal"
    WOOD = "wood"
    PELLETS = "pellets"
    DISTRICT_HEATING = "district_heating"
    PHOTOVOLTAICS = "photovoltaics" # For production

class EnergyFactor(BaseModel):
    carrier: EnergyCarrier
    f_prim: float = Field(description="Faktor primárnej energie")
    f_co2: float = Field(description="Faktor emisií CO2 (t/MWh)")

class EnergyCertificationInput(BaseModel):
    # Inputs from previous chapters (can be passed explicitly or fetched if we had persistence)
    # We will pass them explicitly for now to keep it stateless/simple
    heating_demand: float = Field(description="QH - Potreba energie na vykurovanie (kWh/rok)")
    heating_carrier: EnergyCarrier = Field(default=EnergyCarrier.NATURAL_GAS, description="Nosič energie pre vykurovanie")
    
    dhw_demand: float = Field(description="QW - Potreba energie na TV (kWh/rok)")
    dhw_carrier: EnergyCarrier = Field(default=EnergyCarrier.NATURAL_GAS, description="Nosič energie pre TV")
    
    # New inputs for Chapter 9
    lighting_demand: float = Field(default=0.0, description="Potreba energie na osvetlenie (kWh/rok)")
    cooling_demand: float = Field(default=0.0, description="Potreba energie na chladenie (kWh/rok)")
    ventilation_demand: float = Field(default=0.0, description="Potreba energie na vetranie (kWh/rok)")
    
    # Renewables
    pv_production: float = Field(default=0.0, description="Produkcia FVE (kWh/rok) na odpočet")
    
    # Factors (user can override defaults)
    factors: List[EnergyFactor] = Field(default_factory=list)
    
    # Building metadata for classification
    floor_area: float = Field(description="Podlahová plocha Ab (m2)")
    building_category: str = Field(default="family_house", description="Kategória budovy pre škálovanie (family_house, apartment_building...)")

class EnergyCertResult(BaseModel):
    # Delivered Energy
    del_heating: float
    del_dhw: float
    del_lighting: float
    del_cooling: float
    del_ventilation: float
    total_delivered: float
    
    # Primary Energy
    prim_heating: float
    prim_dhw: float
    prim_lighting: float
    prim_cooling: float
    prim_ventilation: float
    prim_pv_deduction: float
    total_primary: float
    
    # Specific Primary Energy
    specific_primary: float = Field(description="kWh/(m2.a)")
    
    # CO2
    total_co2: float = Field(description="Tonnes CO2/year")
    
    # Classification
    energy_class: EnergyClass
