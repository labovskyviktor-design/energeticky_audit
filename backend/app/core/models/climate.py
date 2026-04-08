"""
Climate and energy balance domain models.

Models for ventilation, solar orientation, climate data,
and window solar properties used in heating demand calculations.
"""

from enum import Enum

from pydantic import BaseModel, Field

from app.core.models.calc_constants import CalcConstantsOverride


class Orientation(str, Enum):
    """Cardinal direction orientation for solar radiation calculations."""
    SOUTH = "south"                    # Juh
    NORTH = "north"                    # Sever
    EAST_WEST = "east_west"            # Východ / Západ
    SE_SW = "se_sw"                    # Juhovýchod / Juhozápad
    NE_NW = "ne_nw"                    # Severovýchod / Severozápad
    HORIZONTAL = "horizontal"          # Horizontálna rovina


class ThermalBridgeLevel(str, Enum):
    """
    Level of thermal bridge surcharge ΔU (STN 73 0540-2).
    """
    CONTINUOUS_NEW = "continuous_new"      # ΔU = 0.02 — spojitá izolácia, nové systémy od 2016
    CONTINUOUS_POST2002 = "continuous_post2002"  # ΔU = 0.05 — spojitá izolácia, po 2002
    PANEL_ORIGINAL = "panel_original"     # ΔU = 0.10 — panelové, murované pred obnovou
    CUSTOM = "custom"                     # Vlastná hodnota


DELTA_U_VALUES: dict[ThermalBridgeLevel, float] = {
    ThermalBridgeLevel.CONTINUOUS_NEW: 0.02,
    ThermalBridgeLevel.CONTINUOUS_POST2002: 0.05,
    ThermalBridgeLevel.PANEL_ORIGINAL: 0.10,
}


class ClimateData(BaseModel):
    """
    Climate data for energy balance calculation.

    Normalized values per vyhláška MDVRR SR č. 364/2012:
    - θint = 20 °C
    - θe,m = 3.86 °C
    - heating_days = 212
    - degree_days = 3422 K·deň
    """
    theta_int: float = Field(default=20.0, description="Vnútorná výpočtová teplota [°C]")
    theta_e_m: float = Field(default=3.86, description="Priemerná vonkajšia teplota [°C]")
    heating_days: int = Field(default=212, description="Počet vykurovacích dní")
    degree_days: float = Field(default=3422.0, description="Počet dennostupňov [K·deň]")
    theta_e_des: float = Field(default=-11.0, description="Vonkajšia návrhová teplota [°C]")


class InfiltrationEntry(BaseModel):
    """Single entry for air infiltration through joints."""
    description: str = Field(..., description="Popis otvorovej konštrukcie")
    joint_length: float = Field(..., gt=0, description="Celková dĺžka škár l [m]")
    ilv: float = Field(..., gt=0, description="Súčiniteľ prievzdušnosti ilv × 10⁴ [m²/(s·Pa⁰·⁶⁷)]")


class VentilationData(BaseModel):
    """Ventilation parameters for HV calculation."""
    v_vb_ratio: float = Field(
        default=0.85,
        description="Pomer V/Vb [-] (0.75=nové RD, 0.80=ostatné, 0.85=obnovované)"
    )
    n_inf_override: float | None = Field(
        default=None, ge=0,
        description="Priamo zadaná intenzita výmeny vzduchu [1/h]. Ak None, počíta sa z infiltrácie."
    )
    infiltration_entries: list[InfiltrationEntry] = Field(
        default_factory=list,
        description="Údaje o infiltrácii cez škáry (pre výpočet ninf)"
    )


class WindowSolarEntry(BaseModel):
    """A window group for solar gain calculation."""
    orientation: Orientation
    area: float = Field(..., gt=0, description="Celková plocha okien pre túto orientáciu [m²]")
    ggl: float = Field(
        default=0.62,
        description="Celková priepustnosť slnečnej energie zasklenia [-]"
    )
    f_shading: float = Field(
        default=0.5,
        description="Celkový tieniaci faktor: Fsh,ob · Fsh,gl · (1-FF) [-]"
    )


class HeatingDemandInput(BaseModel):
    """Complete input data for seasonal heating demand calculation."""
    # Building geometry
    building_name: str
    ab: float = Field(..., gt=0, description="Merná (celková podlahová) plocha Ab [m²]")
    vb: float = Field(..., gt=0, description="Obostavaný objem Vb [m³]")

    # Construction data for HT (same as Building.zones.constructions but flattened)
    constructions: list["ConstructionHTEntry"] = Field(default_factory=list)

    # Thermal bridges
    delta_u: float = Field(default=0.10, description="Prirážka na tepelné mosty ΔU [W/(m²·K)]")

    # Ventilation
    ventilation: VentilationData = Field(default_factory=VentilationData)

    # Internal gains
    qi: float = Field(default=5.0, description="Priemerný tepelný výkon vnútorných zdrojov [W/m²]")

    # Solar gains
    windows_solar: list[WindowSolarEntry] = Field(default_factory=list)

    # Climate
    climate: ClimateData = Field(default_factory=ClimateData)

    # Utilization factor
    eta_gn: float = Field(default=0.95, description="Faktor využitia tepelných ziskov [-]")

    overrides: CalcConstantsOverride | None = Field(default=None, description="Vlastné hodnoty normových konštánt")


class ConstructionHTEntry(BaseModel):
    """Construction element for HT calculation (flattened from Building model)."""
    name: str
    u_value: float = Field(..., gt=0, description="U [W/(m²·K)]")
    area: float = Field(..., gt=0, description="Plocha A [m²]")
    bx: float = Field(default=1.0, ge=0, le=1, description="Redukčný faktor bx [-]")
