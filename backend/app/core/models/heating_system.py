"""
Heating system models for Chapter 3 — Heating Energy Demand.

Defines input models for emission, distribution, pump, and generation
subsystems per STN EN 15316-1/2/3.
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from app.core.models.calc_constants import CalcConstantsOverride


# ── Enums ──────────────────────────────────────────────────────

class PipeSystem(str, Enum):
    """Vykurovací systém — jednotrubkový / dvojtrubkový."""
    ONE_PIPE = "one_pipe"
    TWO_PIPE = "two_pipe"


class HydraulicBalancing(str, Enum):
    """Hydraulické vyregulovanie (Tab. 3.1)."""
    NONE = "none"
    STATIC_PER_RADIATOR = "static_per_radiator"
    STATIC_WITH_SYSTEM = "static_with_system"
    DYNAMIC_PER_CIRCUIT = "dynamic_per_circuit"
    DYNAMIC_PER_CIRCUIT_RETURN = "dynamic_per_circuit_return"
    DYNAMIC_PER_RADIATOR = "dynamic_per_radiator"


class EmitterType(str, Enum):
    """Typ odovzdávacieho systému."""
    RADIATOR = "radiator"           # voľné vykurovacie plochy
    FLOOR_WET = "floor_wet"         # podlahové — mokrý systém
    FLOOR_DRY = "floor_dry"         # podlahové — suchý systém
    FLOOR_DRY_LOW = "floor_dry_low" # suchý systém s malým prekrytím
    WALL = "wall"                   # stenové vykurovanie
    CEILING = "ceiling"             # stropné vykurovanie
    FORCED_VENT = "forced_vent"     # kombinované s núteným vetraním
    FAN_COIL = "fan_coil"           # fan coil / radiátor s ventilátorom


class RegulationType(str, Enum):
    """Regulácia teploty miestnosti (Tab. 3.2, 3.4)."""
    UNREGULATED = "unregulated"          # neregulovaná, centrálna
    REFERENCE_ROOM = "reference_room"    # podľa referenčnej miestnosti
    ROOM_LEVEL = "room_level"            # na úrovni miestnosti
    P_CONTROLLER_OLD = "p_controller_old"  # P-regulátor pred 1988
    P_CONTROLLER = "p_controller"        # P-regulátor / termostatická hlavica
    PI_CONTROLLER = "pi_controller"      # PI-regulátor
    PI_OPTIMIZED = "pi_optimized"        # PI s funkciou optimalizácie


class RadiatorPosition(str, Enum):
    """Poloha radiátora — pre ∆θemb (Tab. 3.4)."""
    INTERNAL_WALL = "internal_wall"
    EXTERNAL_WALL_NORMAL = "external_wall_normal"
    EXTERNAL_WALL_GF_NO_PROT = "external_wall_gf_no_protection"
    EXTERNAL_WALL_GF_WITH_PROT = "external_wall_gf_with_protection"


class RadiatorTempDrop(str, Enum):
    """Teplotný spád pre stratifikáciu radiátorov (Tab. 3.4)."""
    K60 = "60K"    # napr. 90/70
    K42_5 = "42.5K"  # napr. 70/55
    K30 = "30K"    # napr. 55/45
    K20 = "20K"    # napr. 45/35


class RoomAutomation(str, Enum):
    """Automatizácia riadenia (∆θroomaut)."""
    NONE = "none"               # 0 K
    STANDALONE = "standalone"   # -0.5 K
    ADAPTIVE = "adaptive"       # -1.0 K
    NETWORKED = "networked"     # -1.2 K


class PumpRegulation(str, Enum):
    """Regulácia obehového čerpadla (Tab. 3.8)."""
    NO_REGULATION = "no_regulation"
    DP_CONST = "dp_const"        # ∆p konštantné
    DP_VARIABLE = "dp_variable"  # ∆p premenlivé


class GeneratorRegulation(str, Enum):
    """Regulácia zdroja tepla — fG,PM korekčný faktor."""
    STANDARD_OTC = "standard_otc"        # 1.0
    WALL_MOUNTED_OTC = "wall_mounted_otc"  # 0.75
    ROOM_TEMP = "room_temp"              # 0.45


class FuelType(str, Enum):
    """Energetický nosič (Tab. 3.10)."""
    NATURAL_GAS_OLD = "natural_gas_old"
    NATURAL_GAS_NEW = "natural_gas_new"
    NATURAL_GAS_LOWTEMP = "natural_gas_lowtemp"
    NATURAL_GAS_CONDENSING = "natural_gas_condensing"
    NATURAL_GAS_CHP = "natural_gas_chp"
    LPG_NEW = "lpg_new"
    LPG_LOWTEMP = "lpg_lowtemp"
    LPG_CONDENSING = "lpg_condensing"
    BLACK_COAL = "black_coal"
    BROWN_COAL = "brown_coal"
    LIGHT_OIL = "light_oil"
    WOOD_PELLETS_OLD = "wood_pellets_old"
    WOOD_PELLETS_NEW = "wood_pellets_new"
    WOOD_CHIPS_OLD = "wood_chips_old"
    WOOD_CHIPS_NEW = "wood_chips_new"
    FIREWOOD = "firewood"
    FIREWOOD_GASIFICATION = "firewood_gasification"
    DISTRICT_HEATING_COAL = "district_heating_coal"
    DISTRICT_HEATING_BIOMASS = "district_heating_biomass"
    DISTRICT_CHP_GAS = "district_chp_gas"
    DISTRICT_CHP_COAL = "district_chp_coal"
    ELECTRIC = "electric"
    HP_AIR_WATER_RADIATOR = "hp_air_water_radiator"
    HP_AIR_WATER_LOWTEMP = "hp_air_water_lowtemp"
    HP_GROUND_WATER_RADIATOR = "hp_ground_water_radiator"
    HP_GROUND_WATER_LOWTEMP = "hp_ground_water_lowtemp"
    HP_WATER_WATER_RADIATOR = "hp_water_water_radiator"
    HP_WATER_WATER_LOWTEMP = "hp_water_water_lowtemp"
    PHOTOVOLTAICS = "photovoltaics"
    HEAT_EXCHANGER_STEAM_HW = "heat_exchanger_steam_hw"
    HEAT_EXCHANGER_HW_HW = "heat_exchanger_hw_hw"
    HEAT_EXCHANGER_SHW_HW = "heat_exchanger_shw_hw"
    HEAT_EXCHANGER_STEAM_SHW = "heat_exchanger_steam_shw"


class FloorInsulation(str, Enum):
    """Izolácia plošného vykurovania podľa STN EN 1264."""
    NO_MINIMUM = "no_minimum"
    MINIMUM = "minimum"
    DOUBLE_MINIMUM = "double_minimum"  # o 100 % lepšia


# ── Input Models ───────────────────────────────────────────────

class EmissionSystemInput(BaseModel):
    """Vstupné údaje pre podsystém odovzdávania tepla."""
    emitter_type: EmitterType = Field(
        default=EmitterType.RADIATOR,
        description="Typ odovzdávacieho systému",
    )
    regulation: RegulationType = Field(
        default=RegulationType.P_CONTROLLER,
        description="Spôsob regulácie teploty",
    )
    pipe_system: PipeSystem = Field(
        default=PipeSystem.TWO_PIPE,
        description="Jednotrubkový / dvojtrubkový systém",
    )
    hydraulic_balancing: HydraulicBalancing = Field(
        default=HydraulicBalancing.STATIC_WITH_SYSTEM,
        description="Hydraulické vyregulovanie (Tab. 3.1)",
    )
    has_cert: bool = Field(
        default=False,
        description="Regulátor s certifikátom (použije sa ∆θctr,2 namiesto ∆θctr,1)",
    )
    room_automation: RoomAutomation = Field(
        default=RoomAutomation.NONE,
        description="Automatizácia riadenia",
    )
    # Radiator-specific
    radiator_position: RadiatorPosition = Field(
        default=RadiatorPosition.EXTERNAL_WALL_NORMAL,
        description="Poloha radiátora na stene",
    )
    radiator_temp_drop: RadiatorTempDrop = Field(
        default=RadiatorTempDrop.K60,
        description="Teplotný spád systému",
    )
    is_one_pipe_renovated: bool = Field(
        default=False,
        description="Jednorúrkový systém po renovácii",
    )
    # Floor heating insulation
    floor_insulation: FloorInsulation = Field(
        default=FloorInsulation.MINIMUM,
        description="Izolácia plošného vykurovania",
    )
    n_emitters_le_10: bool = Field(
        default=False,
        description="Počet telies v okruhu ≤ 10 (ovplyvňuje ∆θhyd)",
    )


class DistributionPipeInput(BaseModel):
    """Jeden úsek rozvodov vykurovania."""
    name: str = Field(default="", description="Názov úseku")
    dn: float = Field(description="DN potrubia (mm)")
    psi: float = Field(description="Lineárny stratový súčiniteľ Ψ (W/(m·K))")
    length: float = Field(description="Dĺžka potrubia (m)")
    ambient_temp: float = Field(
        default=10.0,
        description="Teplota okolitého prostredia θi (°C)",
    )


class PumpInput(BaseModel):
    """Údaje o obehovom čerpadle."""
    p_el_pmp: Optional[float] = Field(
        default=None,
        description="Menovitý príkon čerpadla Pel,pmp (W). Ak None, použije sa odhad.",
    )
    regulation: PumpRegulation = Field(
        default=PumpRegulation.NO_REGULATION,
        description="Spôsob regulácie čerpadla (Tab. 3.8)",
    )
    generator_regulation: GeneratorRegulation = Field(
        default=GeneratorRegulation.STANDARD_OTC,
        description="Regulácia zdroja tepla — fG,PM",
    )
    is_balanced: bool = Field(
        default=True,
        description="Hydraulicky vyvážený systém (fHB = 1.0 alebo 1.15)",
    )
    is_insulated: bool = Field(
        default=False,
        description="Tepelná izolácia čerpadla (pre faux,rbl)",
    )
    is_in_heated_zone: bool = Field(
        default=False,
        description="Čerpadlo sa nachádza vo vykurovanej zóne",
    )
    is_new_building: bool = Field(
        default=False,
        description="Nová budova (b=1) alebo existujúca (b=2)",
    )
    # One-pipe specific
    kby: float = Field(
        default=0.0,
        description="Pomer zatekania pre jednorúrkový systém (-)",
    )
    # Floor heating
    delta_p_fh: Optional[float] = Field(
        default=None,
        description="Prídavný tlak. spád podlahových systémov ΔpFH (kPa). Default 25.",
    )


class GenerationSourceInput(BaseModel):
    """Vstup pre výpočet strát pri výrobe tepla."""
    fuel_type: FuelType = Field(default=FuelType.HEAT_EXCHANGER_HW_HW)
    is_external: bool = Field(default=True, description="Zdroj mimo obálky (OST)")
    efficiency_override: Optional[float] = Field(
        default=None,
        description="Ručne zadaná účinnosť zdroja (0.0 až 1.0) namiesto tabuľkovej",
    )


class HeatingEnergyInput(BaseModel):
    """Kompletný vstup pre výpočet potreby energie na vykurovanie."""
    building_name: str = Field(default="Budova")
    qh: float = Field(description="Potreba tepla na vykurovanie QH (kWh) — z Kapitoly 2")
    ab: float = Field(description="Podlahová plocha Ab (m²)")

    # Building geometry for pump Lmax estimate
    length_ll: float = Field(default=0, description="Dĺžka budovy LL (m)")
    width_lw: float = Field(default=0, description="Šírka budovy LW (m)")
    n_levels: int = Field(default=1, description="Počet vykurovaných podlaží")
    level_height: float = Field(default=2.8, description="Konštrukčná výška podlažia (m)")
    lmax_override: Optional[float] = Field(
        default=None,
        description="Maximálna dĺžka vykurovacieho okruhu Lmax (m). Ak zadaná, neodhaduje sa.",
    )

    # Design parameters
    theta_s_des: float = Field(default=90, description="Projektovaná teplota prívodnej vody (°C)")
    theta_r_des: float = Field(default=70, description="Projektovaná teplota vratnej vody (°C)")
    phi_em_out: float = Field(description="Projektovaný tepelný príkon ΦH,em,out (kW)")
    theta_e_comb: float = Field(
        default=3.86,
        description="Priemerná vonkajšia teplota počas vykurovacieho obdobia θe,comb (°C)",
    )
    theta_int_ini: float = Field(default=20, description="Počiatočná vnútorná teplota (°C)")
    heating_days: int = Field(default=212, description="Počet vykurovacích dní")

    # Subsystems
    emission: EmissionSystemInput = Field(default_factory=EmissionSystemInput)
    pipes: list[DistributionPipeInput] = Field(default_factory=list)
    pump: PumpInput = Field(default_factory=PumpInput)
    generation: GenerationSourceInput = Field(
        default_factory=lambda: GenerationSourceInput(
            fuel_type=FuelType.HEAT_EXCHANGER_HW_HW,
        ),
    )

    # Recoverable DHW pipe loss
    q_dhw_recoverable: float = Field(
        default=0,
        description="Spätne získateľná tepelná strata zo systému prípravy TV (kWh)",
    )
    overrides: CalcConstantsOverride | None = Field(default=None, description="Vlastné hodnoty normových konštánt")
