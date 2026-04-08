"""
DHW (Domestic Hot Water) models for Chapter 4.
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from app.core.models.calc_constants import CalcConstantsOverride, ResolvedConstants
from app.core.models.heating_system import FuelType


class DHWPipeType(str, Enum):
    SUPPLY = "supply"
    CIRCULATION = "circulation"
    DEAD_LEG = "dead_leg"


class DHWPipeInput(BaseModel):
    """Jeden úsek rozvodov TV."""
    name: str = Field(default="", description="Názov úseku (napr. Prívod 1.NP)")
    length: float = Field(description="Dĺžka úseku (m)")
    dn: float = Field(description="DN potrubia (mm) - pre objem vody (ak treba)")
    psi: float = Field(description="Lineárny stratový súčiniteľ Ψ (W/(m·K))")
    ambient_temp: float = Field(default=15.0, description="Teplota okolia (°C)")
    water_temp: float = Field(default=60.0, description="Teplota vody v úseku (°C)")
    is_circulation: bool = Field(default=False, description="Je to cirkulačné potrubie?")


class DHWStorageInput(BaseModel):
    """Zásobník teplej vody."""
    volume: float = Field(default=0.0, description="Objem zásobníka (l)")
    standby_loss: float = Field(default=0.0, description="Pohotovostná strata Qst,loss (kWh/24h)")
    store_temp: float = Field(default=60.0, description="Teplota vody v zásobníku (°C)")
    ambient_temp: float = Field(default=20.0, description="Teplota okolia zásobníka (°C)")
    has_storage: bool = Field(default=False, description="Existuje zásobník?")


class DHWPumpInput(BaseModel):
    """Cirkulačné čerpadlo."""
    power: float = Field(default=0.0, description="Príkon čerpadla (W)")
    daily_hours: float = Field(default=24.0, description="Prevádzkové hodiny (h/deň)")
    has_circulation: bool = Field(default=False, description="Existuje cirkulácia?")


class DHWGenerationInput(BaseModel):
    """Zdroj tepla pre TV."""
    fuel_type: FuelType = Field(default=FuelType.NATURAL_GAS_NEW)
    efficiency_override: Optional[float] = Field(default=None, description="Vlastná účinnosť (napr. 0.90)")
    is_external: bool = Field(default=False, description="Zdroj mimo budovy (OST)")


class DHWInput(BaseModel):
    """Vstup pre výpočet potreby energie na TV (Kapitola 4)."""
    ab: float = Field(description="Podlahová plocha Ab (m²)")
    pipes: list[DHWPipeInput] = Field(default_factory=list)
    storage: DHWStorageInput = Field(default_factory=DHWStorageInput)
    pump: DHWPumpInput = Field(default_factory=DHWPumpInput)
    generation: DHWGenerationInput = Field(default_factory=DHWGenerationInput)
    heating_days: int = Field(default=212, description="Počet vykurovacích dní (pre recoverable)")
    overrides: CalcConstantsOverride | None = Field(default=None, description="Vlastné hodnoty normových konštánt")


class DHWResult(BaseModel):
    """Výsledok výpočtu TV."""
    q_w: float = Field(description="QW - Netto potreba tepla (kWh)")
    q_w_dis_ls: float = Field(description="QW,d,ls - Strata distribúciou (kWh)")
    q_w_dis_stag: float = Field(description="QW,d,stag - Strata stagnáciou (kWh)")
    q_w_sto_ls: float = Field(description="QW,s - Strata akumuláciou (kWh)")
    w_w_pump: float = Field(description="WW,d,pump - Energia cirkulačného čerpadla (kWh)")
    q_w_gen_ls: float = Field(description="QW,g - Strata výrobou (kWh)")
    
    q_tv: float = Field(description="QTV - Celková potreba energie (kWh)")
    q_tv_m: float = Field(description="Merná potreba energie (kWh/m2)")
    
    q_rec: float = Field(description="Recyklovateľné teplo do vykurovania (kWh)")
    resolved_constants: ResolvedConstants | None = None
    deviations: list[str] = Field(default_factory=list)
