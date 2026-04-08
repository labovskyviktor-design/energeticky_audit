"""
Lookup tables for Chapter 3 — Heating system losses.

All data from STN EN 15316-2/3, Vyhláška MDVRR SR č. 324/2016 Z.z.,
and Vyhláška ÚRSO č. 59/2008 Z.z.
"""

from app.core.models.heating_system import (
    EmitterType,
    FloorInsulation,
    FuelType,
    HydraulicBalancing,
    PipeSystem,
    PumpRegulation,
    RadiatorPosition,
    RadiatorTempDrop,
    RegulationType,
    RoomAutomation,
)


# ── Tab. 3.1 — ∆θhyd (hydraulic balancing) ────────────────────

# Key: (PipeSystem, HydraulicBalancing, n_le_10: bool)
# n_le_10 only matters for TWO_PIPE
_DELTA_THETA_HYD: dict[tuple, float] = {
    # One-pipe
    (PipeSystem.ONE_PIPE, HydraulicBalancing.NONE, True): 0.7,
    (PipeSystem.ONE_PIPE, HydraulicBalancing.NONE, False): 0.7,
    (PipeSystem.ONE_PIPE, HydraulicBalancing.STATIC_PER_RADIATOR, True): 0.4,
    (PipeSystem.ONE_PIPE, HydraulicBalancing.STATIC_PER_RADIATOR, False): 0.4,
    (PipeSystem.ONE_PIPE, HydraulicBalancing.DYNAMIC_PER_CIRCUIT, True): 0.3,
    (PipeSystem.ONE_PIPE, HydraulicBalancing.DYNAMIC_PER_CIRCUIT, False): 0.3,
    (PipeSystem.ONE_PIPE, HydraulicBalancing.DYNAMIC_PER_CIRCUIT_RETURN, True): 0.2,
    (PipeSystem.ONE_PIPE, HydraulicBalancing.DYNAMIC_PER_CIRCUIT_RETURN, False): 0.2,
    # Two-pipe n ≤ 10
    (PipeSystem.TWO_PIPE, HydraulicBalancing.NONE, True): 0.6,
    (PipeSystem.TWO_PIPE, HydraulicBalancing.STATIC_PER_RADIATOR, True): 0.3,
    (PipeSystem.TWO_PIPE, HydraulicBalancing.STATIC_WITH_SYSTEM, True): 0.2,
    (PipeSystem.TWO_PIPE, HydraulicBalancing.DYNAMIC_PER_CIRCUIT, True): 0.1,
    (PipeSystem.TWO_PIPE, HydraulicBalancing.DYNAMIC_PER_CIRCUIT_RETURN, True): 0.0,
    (PipeSystem.TWO_PIPE, HydraulicBalancing.DYNAMIC_PER_RADIATOR, True): 0.0,
    # Two-pipe n > 10
    (PipeSystem.TWO_PIPE, HydraulicBalancing.NONE, False): 0.6,
    (PipeSystem.TWO_PIPE, HydraulicBalancing.STATIC_PER_RADIATOR, False): 0.4,
    (PipeSystem.TWO_PIPE, HydraulicBalancing.STATIC_WITH_SYSTEM, False): 0.3,
    (PipeSystem.TWO_PIPE, HydraulicBalancing.DYNAMIC_PER_CIRCUIT, False): 0.2,
    (PipeSystem.TWO_PIPE, HydraulicBalancing.DYNAMIC_PER_CIRCUIT_RETURN, False): 0.1,
    (PipeSystem.TWO_PIPE, HydraulicBalancing.DYNAMIC_PER_RADIATOR, False): 0.0,
}


def get_delta_theta_hyd(
    pipe_system: PipeSystem,
    balancing: HydraulicBalancing,
    n_emitters_le_10: bool = False,
) -> float:
    """Tab. 3.1 — Zmena teploty v závislosti od hydraulického vyregulovania."""
    key = (pipe_system, balancing, n_emitters_le_10)
    if key in _DELTA_THETA_HYD:
        return _DELTA_THETA_HYD[key]
    # Default fallback
    return _DELTA_THETA_HYD.get(
        (pipe_system, balancing, True), 0.4
    )


# ── Tab. 3.4 — Radiators: ∆θctr, ∆θstr ───────────────────────

# ∆θctr for radiators (free heating surfaces), Tab 3.4
# Key: (RegulationType, has_cert)
_DELTA_THETA_CTR_RADIATOR: dict[tuple, float] = {
    (RegulationType.UNREGULATED, False): 2.5,
    (RegulationType.REFERENCE_ROOM, False): 2.0,
    (RegulationType.ROOM_LEVEL, False): 1.8,
    (RegulationType.P_CONTROLLER_OLD, False): 1.4,
    (RegulationType.P_CONTROLLER, False): 1.2,
    (RegulationType.P_CONTROLLER, True): 1.2,
    (RegulationType.PI_CONTROLLER, False): 1.2,
    (RegulationType.PI_CONTROLLER, True): 0.7,
    (RegulationType.PI_OPTIMIZED, False): 0.9,
    (RegulationType.PI_OPTIMIZED, True): 0.5,
    # uncertified defaults
    (RegulationType.UNREGULATED, True): 2.5,
    (RegulationType.REFERENCE_ROOM, True): 1.8,
    (RegulationType.ROOM_LEVEL, True): 1.6,
    (RegulationType.P_CONTROLLER_OLD, True): 1.4,
}

# ∆θstr,1 for radiators (Tab 3.4 top part)
# Key: (RadiatorTempDrop, is_one_pipe_original)
_DELTA_THETA_STR1_RADIATOR: dict[tuple, float] = {
    # Two-pipe / renovated one-pipe
    (RadiatorTempDrop.K60, False): 1.2,
    (RadiatorTempDrop.K42_5, False): 0.7,
    (RadiatorTempDrop.K30, False): 0.5,
    (RadiatorTempDrop.K20, False): 0.4,
    # Original one-pipe
    (RadiatorTempDrop.K60, True): 1.2,
    (RadiatorTempDrop.K42_5, True): 0.7,
}

# ∆θstr,2 for radiators (Tab 3.4 bottom part)
_DELTA_THETA_STR2_RADIATOR: dict[RadiatorPosition, float] = {
    RadiatorPosition.INTERNAL_WALL: 0.0,
    RadiatorPosition.EXTERNAL_WALL_NORMAL: 0.3,
    RadiatorPosition.EXTERNAL_WALL_GF_NO_PROT: 1.7,
    RadiatorPosition.EXTERNAL_WALL_GF_WITH_PROT: 1.2,
}

# ∆θemb for radiators — depends on position (Tab. 3.4)
_DELTA_THETA_EMB_RADIATOR: dict[RadiatorPosition, float] = {
    RadiatorPosition.INTERNAL_WALL: 0.0,
     RadiatorPosition.EXTERNAL_WALL_NORMAL: 0.0, # Fixed: 0 per worked example/text ("∆θemb = 0 pre voľné plochy")
    RadiatorPosition.EXTERNAL_WALL_GF_NO_PROT: 0.0,
    RadiatorPosition.EXTERNAL_WALL_GF_WITH_PROT: 0.0,
}
# Note: Tab 3.4 lists ∆θemb column, but worked example says for radiators:
# "∆θemb = 0 K pre voľné vykurovacie plochy".
# Actually Tab 3.4 does show ∆θemb values (same as str2?? No).
# Let's check PDF page 7 again.
# Tab 3.4 params: ∆θstr, ∆θctr,1, ∆θctr,2, ∆θemb.
# For radiators, ∆θemb column is empty / dashes?
# Page 42 text: "∆θemb sa stanoví na základe Tab. 3.4... pričom ∆θstr sa vypočíta ako priemer...".
# Page 55 worked example: "∆θemb = 0 K".
# So for radiators, ∆θemb is 0.
# The table 3.4 has columns for ∆θctr, but might not have ∆θemb.
# The previous code had 0.3/1.7 in _DELTA_THETA_EMB_RADIATOR. That was likely wrong.


def get_delta_theta_str(
    emitter_type: EmitterType,
    radiator_position: RadiatorPosition = RadiatorPosition.EXTERNAL_WALL_NORMAL,
    temp_drop: RadiatorTempDrop = RadiatorTempDrop.K60,
    is_one_pipe_original: bool = False,
    regulation: RegulationType = RegulationType.P_CONTROLLER,
) -> float:
    """Get ∆θstr. For radiators, averages (∆θstr,1 + ∆θstr,2) / 2."""
    if _is_integrated(emitter_type):
        return _DELTA_THETA_STR_INTEGRATED.get(regulation, 0.0)
    
    # Radiators
    key1 = (temp_drop, is_one_pipe_original)
    str1 = _DELTA_THETA_STR1_RADIATOR.get(key1, 0.75)
    
    str2 = _DELTA_THETA_STR2_RADIATOR.get(radiator_position, 0.3)
    
    return (str1 + str2) / 2

# ── Tab. 3.2 — Integrated heating surfaces: ∆θ ───────────────

# ∆θctr for integrated surfaces (same structure as radiators)
_DELTA_THETA_CTR_INTEGRATED: dict[tuple, float] = {
    (RegulationType.UNREGULATED, False): 2.5,
    (RegulationType.REFERENCE_ROOM, False): 2.0,
    (RegulationType.ROOM_LEVEL, False): 1.8,
    (RegulationType.P_CONTROLLER_OLD, False): 1.4,
    (RegulationType.P_CONTROLLER, False): 1.2,
    (RegulationType.P_CONTROLLER, True): 0.7,
    (RegulationType.PI_CONTROLLER, False): 1.2,
    (RegulationType.PI_CONTROLLER, True): 0.7,
    (RegulationType.PI_OPTIMIZED, False): 0.9,
    (RegulationType.PI_OPTIMIZED, True): 0.5,
    (RegulationType.UNREGULATED, True): 2.5,
    (RegulationType.REFERENCE_ROOM, True): 1.8,
    (RegulationType.ROOM_LEVEL, True): 1.6,
    (RegulationType.P_CONTROLLER_OLD, True): 1.4,
}

# ∆θstr for integrated surfaces — Tab 3.2, same regulation controls
_DELTA_THETA_STR_INTEGRATED: dict[RegulationType, float] = {
    RegulationType.UNREGULATED: 0.0,
    RegulationType.REFERENCE_ROOM: 0.0,
    RegulationType.ROOM_LEVEL: 0.0,
    RegulationType.P_CONTROLLER_OLD: 0.0,
    RegulationType.P_CONTROLLER: 0.0,
    RegulationType.PI_CONTROLLER: 0.0,
    RegulationType.PI_OPTIMIZED: 0.0,
}

# ∆θemb for integrated surfaces (Tab 3.2)
# (EmitterType, FloorInsulation) → (∆θemb,1, ∆θemb,2)
_DELTA_THETA_EMB_INTEGRATED: dict[tuple, tuple[float, float]] = {
    (EmitterType.FLOOR_WET, FloorInsulation.NO_MINIMUM): (0.7, 0.7),
    (EmitterType.FLOOR_WET, FloorInsulation.MINIMUM): (0.7, 0.4),
    (EmitterType.FLOOR_WET, FloorInsulation.DOUBLE_MINIMUM): (0.7, 0.2),
    (EmitterType.FLOOR_DRY, FloorInsulation.NO_MINIMUM): (0.4, 0.7),
    (EmitterType.FLOOR_DRY, FloorInsulation.MINIMUM): (0.4, 0.4),
    (EmitterType.FLOOR_DRY, FloorInsulation.DOUBLE_MINIMUM): (0.4, 0.2),
    (EmitterType.FLOOR_DRY_LOW, FloorInsulation.NO_MINIMUM): (0.2, 0.7),
    (EmitterType.FLOOR_DRY_LOW, FloorInsulation.MINIMUM): (0.2, 0.4),
    (EmitterType.FLOOR_DRY_LOW, FloorInsulation.DOUBLE_MINIMUM): (0.2, 0.2),
    (EmitterType.WALL, FloorInsulation.NO_MINIMUM): (1.4, 0.0),
    (EmitterType.WALL, FloorInsulation.MINIMUM): (1.4, 0.0),
    (EmitterType.WALL, FloorInsulation.DOUBLE_MINIMUM): (1.4, 0.0),
    (EmitterType.CEILING, FloorInsulation.NO_MINIMUM): (0.5, 0.0),
    (EmitterType.CEILING, FloorInsulation.MINIMUM): (0.5, 0.0),
    (EmitterType.CEILING, FloorInsulation.DOUBLE_MINIMUM): (0.5, 0.0),
    (EmitterType.FORCED_VENT, FloorInsulation.NO_MINIMUM): (0.0, 1.3),
    (EmitterType.FORCED_VENT, FloorInsulation.MINIMUM): (0.0, 1.3),
}


# ── ∆θroomaut ─────────────────────────────────────────────────

DELTA_THETA_ROOMAUT: dict[RoomAutomation, float] = {
    RoomAutomation.NONE: 0.0,
    RoomAutomation.STANDALONE: -0.5,
    RoomAutomation.ADAPTIVE: -1.0,
    RoomAutomation.NETWORKED: -1.2,
}


# ── Public API for emission ∆θ lookups ─────────────────────────

def get_delta_theta_ctr(
    emitter_type: EmitterType,
    regulation: RegulationType,
    has_cert: bool,
) -> float:
    """Get ∆θctr for the emitter/regulation combination."""
    key = (regulation, has_cert)
    if _is_integrated(emitter_type):
        return _DELTA_THETA_CTR_INTEGRATED.get(key, 1.2)
    return _DELTA_THETA_CTR_RADIATOR.get(key, 1.2)


def get_delta_theta_str(
    emitter_type: EmitterType,
    radiator_position: RadiatorPosition = RadiatorPosition.EXTERNAL_WALL_NORMAL,
    temp_drop: RadiatorTempDrop = RadiatorTempDrop.K60,
    is_one_pipe_original: bool = False,
    regulation: RegulationType = RegulationType.P_CONTROLLER,
) -> float:
    """Get ∆θstr. For radiators, averages (∆θstr,1 + ∆θstr,2) / 2."""
    if _is_integrated(emitter_type):
        return _DELTA_THETA_STR_INTEGRATED.get(regulation, 0.0)
    
    # Radiators
    key1 = (temp_drop, is_one_pipe_original)
    str1 = _DELTA_THETA_STR1_RADIATOR.get(key1, 0.75)
    
    str2 = _DELTA_THETA_STR2_RADIATOR.get(radiator_position, 0.3)
    
    return (str1 + str2) / 2


def get_delta_theta_emb(
    emitter_type: EmitterType,
    radiator_position: RadiatorPosition = RadiatorPosition.EXTERNAL_WALL_NORMAL,
    floor_insulation: FloorInsulation = FloorInsulation.MINIMUM,
) -> float:
    """Get ∆θemb. For integrated surfaces, averages (∆θemb,1 + ∆θemb,2) / 2."""
    if _is_integrated(emitter_type):
        key = (emitter_type, floor_insulation)
        vals = _DELTA_THETA_EMB_INTEGRATED.get(key, (0.0, 0.0))
        return (vals[0] + vals[1]) / 2
    return _DELTA_THETA_EMB_RADIATOR.get(radiator_position, 0.0)


def get_delta_theta_rad(emitter_type: EmitterType) -> float:
    """∆θrad = 0 for all types when room height ≤ 4m."""
    return 0.0


def get_delta_theta_im_emt(emitter_type: EmitterType) -> float:
    """∆θim,emt — intermittent operation of heating system."""
    if _is_integrated(emitter_type):
        return -0.2
    return -0.3


def get_delta_theta_im_ctr() -> float:
    """∆θim,ctr = 0.0 K always."""
    return 0.0


def _is_integrated(emitter_type: EmitterType) -> bool:
    """Check if emitter is an integrated heating surface (floor/wall/ceiling)."""
    return emitter_type in (
        EmitterType.FLOOR_WET,
        EmitterType.FLOOR_DRY,
        EmitterType.FLOOR_DRY_LOW,
        EmitterType.WALL,
        EmitterType.CEILING,
        EmitterType.FORCED_VENT,
    )


# ── Tab. 3.7 — Generator pressure drop ΔpG ────────────────────

def get_delta_p_g(phi_max_kw: float, v_des: float, water_volume_gt_015: bool = True) -> float:
    """Tab. 3.7 — Tlakový spád zdroja tepla (kPa)."""
    if water_volume_gt_015:
        return 1.0
    if phi_max_kw < 35:
        return 20.0 * v_des ** 2
    return 80.0


# ── Tab. 3.8 — CP1, CP2 for pump power factor ─────────────────

PUMP_CP: dict[PumpRegulation, tuple[float, float]] = {
    PumpRegulation.NO_REGULATION: (0.25, 0.75),
    PumpRegulation.DP_CONST: (0.75, 0.25),
    PumpRegulation.DP_VARIABLE: (0.90, 0.10),
}


# ── Tab. 3.9 — Heat exchanger station efficiency ──────────────

HEAT_EXCHANGER_EFF: dict[FuelType, float] = {
    FuelType.HEAT_EXCHANGER_STEAM_HW: 0.97,
    FuelType.HEAT_EXCHANGER_HW_HW: 0.99,
    FuelType.HEAT_EXCHANGER_SHW_HW: 0.985,
    FuelType.HEAT_EXCHANGER_STEAM_SHW: 0.96,
}


# ── Tab. 3.10 — Fuel data (efficiency, CO2, fp) ───────────────

class FuelData:
    """Data for a single fuel/system type."""

    __slots__ = ("efficiency", "co2_kg_per_kwh", "fp")

    def __init__(self, efficiency: float, co2: float, fp: float):
        self.efficiency = efficiency
        self.co2_kg_per_kwh = co2
        self.fp = fp


# Using midpoint of ranges where applicable
FUEL_DATA: dict[FuelType, FuelData] = {
    FuelType.NATURAL_GAS_OLD: FuelData(0.86, 0.220, 1.1),
    FuelType.NATURAL_GAS_NEW: FuelData(0.895, 0.220, 1.1),
    FuelType.NATURAL_GAS_LOWTEMP: FuelData(0.915, 0.220, 1.1),
    FuelType.NATURAL_GAS_CONDENSING: FuelData(1.01, 0.220, 1.1),
    FuelType.NATURAL_GAS_CHP: FuelData(0.85, 0.220, 1.1),
    FuelType.LPG_NEW: FuelData(0.895, 0.2484, 1.35),
    FuelType.LPG_LOWTEMP: FuelData(0.915, 0.2484, 1.35),
    FuelType.LPG_CONDENSING: FuelData(1.01, 0.2484, 1.35),
    FuelType.BLACK_COAL: FuelData(0.735, 0.360, 1.1),
    FuelType.BROWN_COAL: FuelData(0.735, 0.360, 1.1),
    FuelType.LIGHT_OIL: FuelData(0.70, 0.290, 1.1),
    FuelType.WOOD_PELLETS_OLD: FuelData(0.82, 0.020, 0.20),
    FuelType.WOOD_PELLETS_NEW: FuelData(0.85, 0.020, 0.15),
    FuelType.WOOD_CHIPS_OLD: FuelData(0.87, 0.020, 0.10),
    FuelType.WOOD_CHIPS_NEW: FuelData(0.91, 0.020, 0.10),
    FuelType.FIREWOOD: FuelData(0.82, 0.020, 0.10),
    FuelType.FIREWOOD_GASIFICATION: FuelData(0.83, 0.020, 0.10),
    FuelType.DISTRICT_HEATING_COAL: FuelData(0.80, 0.360, 1.3),
    FuelType.DISTRICT_HEATING_BIOMASS: FuelData(0.76, 0.020, 1.3),
    FuelType.DISTRICT_CHP_GAS: FuelData(0.82, 0.220, 0.7),
    FuelType.DISTRICT_CHP_COAL: FuelData(0.65, 0.360, 0.7),
    FuelType.ELECTRIC: FuelData(0.99, 0.167, 2.2),
    FuelType.HP_AIR_WATER_RADIATOR: FuelData(2.6, 0.167, 2.2),
    FuelType.HP_AIR_WATER_LOWTEMP: FuelData(2.9, 0.167, 2.2),
    FuelType.HP_GROUND_WATER_RADIATOR: FuelData(3.4, 0.167, 2.2),
    FuelType.HP_GROUND_WATER_LOWTEMP: FuelData(3.9, 0.167, 2.2),
    FuelType.HP_WATER_WATER_RADIATOR: FuelData(4.0, 0.167, 2.2),
    FuelType.HP_WATER_WATER_LOWTEMP: FuelData(4.4, 0.167, 2.2),
    FuelType.PHOTOVOLTAICS: FuelData(1.0, 0.0, 0.0),
    FuelType.HEAT_EXCHANGER_STEAM_HW: FuelData(0.97, 0.0, 0.0),
    FuelType.HEAT_EXCHANGER_HW_HW: FuelData(0.99, 0.0, 0.0),
    FuelType.HEAT_EXCHANGER_SHW_HW: FuelData(0.985, 0.0, 0.0),
    FuelType.HEAT_EXCHANGER_STEAM_SHW: FuelData(0.96, 0.0, 0.0),
}


def get_fuel_efficiency(fuel_type: FuelType) -> float:
    """Return efficiency η (or COP for heat pumps) from Tab 3.10."""
    data = FUEL_DATA.get(fuel_type)
    if data is None:
        raise ValueError(f"Unknown fuel type: {fuel_type}")
    return data.efficiency


def get_fuel_co2(fuel_type: FuelType) -> float:
    """Return CO2 emission factor kg/kWh from Tab 3.10."""
    data = FUEL_DATA.get(fuel_type)
    if data is None:
        raise ValueError(f"Unknown fuel type: {fuel_type}")
    return data.co2_kg_per_kwh


def get_fuel_fp(fuel_type: FuelType) -> float:
    """Return primary energy factor fp from Tab 3.10."""
    data = FUEL_DATA.get(fuel_type)
    if data is None:
        raise ValueError(f"Unknown fuel type: {fuel_type}")
    return data.fp
