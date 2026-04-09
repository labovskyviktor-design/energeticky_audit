"""
Domain models for Building, Zones, and Construction elements.

These models represent the core domain entities used throughout
the energy audit calculation engine. They are pure Pydantic models
with no infrastructure dependencies (Hexagonal Architecture).
"""

from enum import Enum

from pydantic import BaseModel, Field


class BuildingCategory(str, Enum):
    """Building category for energy classification (STN)."""
    RODINNY_DOM = "rodinny_dom"                    # Rodinný dom
    BYTOVY_DOM = "bytovy_dom"                      # Bytový dom
    ADMINISTRATIVA = "administrativa"              # Administratívna budova
    SKOLA = "skola"                                # Škola / Vzdelávacia budova
    NEMOCNICA = "nemocnica"                        # Nemocnica / Zdravotnícke zariadenie
    HOTEL = "hotel"                                # Hotel / Ubytovanie
    SPORTOVA_HALA = "sportova_hala"                # Športová hala
    OBCHODNY_DOM = "obchodny_dom"                  # Obchodný dom


class ConstructionType(str, Enum):
    WALL = "wall"
    ROOF = "roof"
    CEILING_EXT = "ceiling_ext"
    CEILING = "ceiling"
    INT_HOR_10 = "int_hor_10"
    INT_HOR_15 = "int_hor_15"
    INT_HOR_20 = "int_hor_20"
    INT_HOR_25 = "int_hor_25"
    INT_HOR_OVER25 = "int_hor_over25"
    INT_UP_10 = "int_up_10"
    INT_UP_15 = "int_up_15"
    INT_UP_20 = "int_up_20"
    INT_UP_25 = "int_up_25"
    INT_UP_OVER25 = "int_up_over25"
    INT_DOWN_10 = "int_down_10"
    INT_DOWN_15 = "int_down_15"
    INT_DOWN_20 = "int_down_20"
    INT_DOWN_25 = "int_down_25"
    INT_DOWN_OVER25 = "int_down_over25"
    EARTH_WALL_05 = "earth_wall_05"
    EARTH_WALL_20 = "earth_wall_20"
    EARTH_WALL_OVER20 = "earth_wall_over20"
    EARTH_FLOOR_EDGE = "earth_floor_edge"
    EARTH_FLOOR_OTHER = "earth_floor_other"
    WINDOW = "window"
    DOOR = "door"


class HeatFlowDirection(str, Enum):
    """Direction of heat flow through construction — determines Rsi value."""
    HORIZONTAL = "horizontal"   # Vodorovný tok — Rsi = 0.13
    UPWARD = "upward"           # Tok zdola nahor — Rsi = 0.10
    DOWNWARD = "downward"       # Tok zhora nadol — Rsi = 0.17


class AssessmentLevel(str, Enum):
    """
    Level of thermal-technical requirement (STN 73 0540-2/Z1+Z2).

    - U_MAX: Maximálna hodnota (for buildings with past partial renovations)
    - U_N: Normalizovaná hodnota (low-energy, valid until 2015)
    - U_R1: Odporúčaná hodnota (ultra-low-energy, from 2016)
    - U_R2: Cieľová odporúčaná hodnota (nearly zero energy, from 2021)
    """
    U_MAX = "u_max"
    U_N = "u_n"
    U_R1 = "u_r1"
    U_R2 = "u_r2"


class MaterialLayer(BaseModel):
    """
    A single material layer within a construction.

    Used for optional detail-mode calculation of R from layers.
    Formula (1.4): R_layer = d / λ
    """
    name: str = Field(..., description="Názov materiálu")
    thickness: float = Field(..., gt=0, description="Hrúbka vrstvy d [m]")
    thermal_conductivity: float = Field(
        ..., gt=0, description="Súčiniteľ tepelnej vodivosti λ [W/(m·K)]"
    )
    density: float = Field(
        default=0.0, ge=0, description="Objemová hmotnosť ρ [kg/m³]"
    )
    specific_heat_capacity: float = Field(
        default=0.0, ge=0, description="Merná tepelná kapacita c [J/(kg·K)]"
    )
    diffusion_resistance: float = Field(
        default=1.0, ge=0, description="Faktor difúzneho odporu μ [-]"
    )

    @property
    def thermal_resistance(self) -> float:
        """R = d / λ  [(m²·K)/W]"""
        return self.thickness / self.thermal_conductivity

    @property
    def vapor_resistance(self) -> float:
        """Sd = μ * d [m] (Equivalent air layer thickness)"""
        return self.diffusion_resistance * self.thickness


class Construction(BaseModel):
    """
    A single construction element of the building envelope.

    User provides U-value directly (core flow).
    Optionally, layers can be provided for detail-mode R → U calculation.
    """
    name: str = Field(..., description="Názov konštrukcie (napr. 'Obvodová stena sever')")
    construction_type: ConstructionType
    area: float = Field(..., gt=0, description="Plocha konštrukcie [m²]")
    u_value: float = Field(..., gt=0, description="Súčiniteľ prechodu tepla U [W/(m²·K)]")
    # Correction factor for temperature (e.g., for ground contact, unheated spaces)
    b_factor: float = Field(default=1.0, ge=0, le=1, description="Korekčný faktor [-]")
    # Optional: heat flow direction (for correct Rsi selection in detail mode)
    heat_flow_direction: HeatFlowDirection = Field(
        default=HeatFlowDirection.HORIZONTAL,
        description="Smer tepelného toku (pre výber Rsi)"
    )
    # Optional: material layers for detail-mode U calculation
    layers: list[MaterialLayer] = Field(
        default_factory=list,
        description="Vrstvy konštrukcie (voliteľné, pre výpočet R z vrstiev)"
    )


class Zone(BaseModel):
    """A thermal zone within the building."""
    name: str = Field(..., description="Názov zóny")
    heated_volume: float = Field(..., gt=0, description="Vykurovaný objem [m³]")
    heated_floor_area: float = Field(..., gt=0, description="Vykurovaná podlahová plocha [m²]")
    internal_temperature: float = Field(default=20.0, description="Vnútorná výpočtová teplota [°C]")
    constructions: list[Construction] = Field(default_factory=list)


class Building(BaseModel):
    """Top-level building model for an energy audit project."""
    name: str = Field(..., description="Názov projektu / budovy")
    category: BuildingCategory
    location: str = Field(default="", description="Lokalita budovy")
    altitude: float = Field(default=0, ge=0, description="Nadmorská výška [m.n.m.]")
    external_temperature: float = Field(
        default=-11.0,
        description="Vonkajšia výpočtová teplota [°C]"
    )
    zones: list[Zone] = Field(default_factory=list)
