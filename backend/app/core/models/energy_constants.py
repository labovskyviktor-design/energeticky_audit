"""
Energy constants and reference tables for Chapter 2.

Source of truth: Krajčík, M. a kol. — Energetické hodnotenie budov
Tables: 2.1 (bx), 2.3 (solar radiation), 2.5 (ggl), 2.6 (η), 2.7 (QH,nd requirements)
"""

from app.core.models.building import AssessmentLevel, BuildingCategory
from app.core.models.climate import Orientation

# ---------------------------------------------------------------------------
# Air constants
# ---------------------------------------------------------------------------
RHO_AIR: float = 1.2        # kg/m³
C_AIR: float = 1010.0       # J/(kg·K)
MIN_AIR_CHANGE: float = 0.5  # Minimum ninf = 0.5 1/h

# ---------------------------------------------------------------------------
# Tab 2.1 — Redukčný (teplotný korekčný) faktor bx
# ---------------------------------------------------------------------------
BX_FACTORS: dict[str, float] = {
    "exterior_wall": 1.00,
    "window": 1.00,
    "exterior_door": 1.00,
    "roof": 1.00,
    "floor_on_ground": 1.00,
    "floor_attic": 0.80,
    "wall_to_unheated": 0.80,
    "wall_basement_unheated": 0.50,
    "wall_tempered": 0.35,
    "open_dilatation": 0.35,
    "closed_insulated_dilatation": 0.10,
    "ceiling_open_passage": 1.00,
    "wall_unheated_single_glass": 0.70,
    "wall_unheated_double_glass": 0.60,
    "wall_unheated_insulating_glass": 0.50,
}

# ---------------------------------------------------------------------------
# Tab 2.3 — Normalizované intenzity slnečného žiarenia (kWh/m²)
# Seasonal totals for standard heating period (Oct–Apr)
# ---------------------------------------------------------------------------
SOLAR_RADIATION_SEASONAL: dict[Orientation, float] = {
    Orientation.SOUTH: 320.0,
    Orientation.NORTH: 100.0,
    Orientation.EAST_WEST: 200.0,
    Orientation.SE_SW: 260.0,
    Orientation.NE_NW: 130.0,
    Orientation.HORIZONTAL: 340.0,
}

# Monthly breakdown for future monthly method
SOLAR_RADIATION_MONTHLY: dict[Orientation, list[float]] = {
    # Order: I, II, III, IV, X, XI, XII
    Orientation.SOUTH: [30.2, 43.6, 61.2, 66.3, 57.2, 33.1, 28.4],
    Orientation.NORTH: [9.1, 13.8, 20.1, 27.2, 14.5, 8.4, 6.8],
    Orientation.EAST_WEST: [14.9, 24.5, 42.0, 59.1, 32.2, 15.4, 11.8],
    Orientation.SE_SW: [22.7, 33.8, 50.9, 62.0, 44.8, 24.9, 20.8],
    Orientation.NE_NW: [10.2, 16.1, 26.8, 41.6, 18.3, 9.6, 7.4],
    Orientation.HORIZONTAL: [22.2, 38.6, 71.4, 108.2, 55.0, 26.2, 18.4],
}

# ---------------------------------------------------------------------------
# Tab 2.6 — Faktor využitia tepelných ziskov ηH,gn
# ---------------------------------------------------------------------------
UTILIZATION_FACTORS: dict[str, dict[str, float]] = {
    "energy_efficient": {"rd": 0.95, "bd": 0.95},
    "low_energy": {"rd": 0.95, "bd": 0.95},
    "ultra_low_energy": {"rd": 0.95, "bd": 0.84},
    "nearly_zero": {"rd": 0.95, "bd": 0.84},
}

# ---------------------------------------------------------------------------
# Tab 2.7 — Požiadavky na QH,nd [kWh/(m²·a)]
# Indexed by shape factor → (QH,nd,max, QH,nd,N, QH,nd,r1, QH,nd,r2)
# ---------------------------------------------------------------------------
QH_ND_REQUIREMENTS: list[tuple[float, float, float, float, float]] = [
    # (shape_factor, max, N, r1, r2)
    (0.3, 70.00, 50.00, 25.00, 12.50),
    (0.4, 78.60, 57.10, 28.55, 14.28),
    (0.5, 87.10, 64.30, 32.15, 16.08),
    (0.6, 95.70, 71.40, 35.70, 17.85),
    (0.7, 104.30, 78.60, 39.30, 19.65),
    (0.8, 112.90, 85.70, 42.85, 21.43),
    (0.9, 121.40, 92.90, 46.45, 23.23),
    (1.0, 130.00, 100.00, 50.00, 25.00),
]

_LEVEL_INDEX: dict[AssessmentLevel, int] = {
    AssessmentLevel.U_MAX: 1,  # QH,nd,max
    AssessmentLevel.U_N: 2,    # QH,nd,N
    AssessmentLevel.U_R1: 3,   # QH,nd,r1
    AssessmentLevel.U_R2: 4,   # QH,nd,r2
}


def get_qh_nd_required(
    shape_factor: float,
    level: AssessmentLevel = AssessmentLevel.U_R1,
) -> float:
    """
    Get required QH,nd for a given shape factor using linear interpolation.

    Per Tab 2.7: values for intermediate shape factors are determined by
    linear interpolation, rounded to one decimal place.
    """
    col_idx = _LEVEL_INDEX[level]

    # Clamp to table range
    if shape_factor <= QH_ND_REQUIREMENTS[0][0]:
        return QH_ND_REQUIREMENTS[0][col_idx]
    if shape_factor >= QH_ND_REQUIREMENTS[-1][0]:
        return QH_ND_REQUIREMENTS[-1][col_idx]

    # Find surrounding rows and interpolate
    for i in range(len(QH_ND_REQUIREMENTS) - 1):
        sf_low, *vals_low = QH_ND_REQUIREMENTS[i]
        sf_high, *vals_high = QH_ND_REQUIREMENTS[i + 1]
        if sf_low <= shape_factor <= sf_high:
            ratio = (shape_factor - sf_low) / (sf_high - sf_low)
            val_low = vals_low[col_idx - 1]
            val_high = vals_high[col_idx - 1]
            result = val_low + ratio * (val_high - val_low)
            return round(result, 1)

    # Fallback (should not reach here)
    return QH_ND_REQUIREMENTS[-1][col_idx]


# ---------------------------------------------------------------------------
# Internal heat gain density qi [W/m²]
# ---------------------------------------------------------------------------
QI_DEFAULTS: dict[BuildingCategory, float] = {
    BuildingCategory.RODINNY_DOM: 4.0,
    BuildingCategory.BYTOVY_DOM: 5.0,
    BuildingCategory.ADMINISTRATIVA: 6.0,
    BuildingCategory.SKOLA: 6.0,
    BuildingCategory.NEMOCNICA: 6.0,
    BuildingCategory.HOTEL: 6.0,
    BuildingCategory.SPORTOVA_HALA: 6.0,
    BuildingCategory.OBCHODNY_DOM: 6.0,
}
