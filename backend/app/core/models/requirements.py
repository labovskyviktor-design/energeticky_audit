"""
STN 73 0540-2/Z1+Z2 — Thermal-technical requirement tables and constants.

Source of truth: Krajčík, M. a kol. — Energetické hodnotenie budov, Tab 1.1, 1.2, 1.3.
"""

from app.core.models.building import (
    AssessmentLevel,
    ConstructionType,
    HeatFlowDirection,
)

# ---------------------------------------------------------------------------
# Surface heat transfer resistances  [(m²·K)/W]
# (STN 73 0540-2/Z1+Z2, Tab 1.1 footnotes)
# ---------------------------------------------------------------------------
RSE: float = 0.04  # Vonkajší povrch

RSI_VALUES: dict[HeatFlowDirection, float] = {
    HeatFlowDirection.HORIZONTAL: 0.13,  # Vodorovný tepelný tok
    HeatFlowDirection.UPWARD: 0.10,      # Tok zdola nahor
    HeatFlowDirection.DOWNWARD: 0.17,    # Tok zhora nadol
}


def get_rsi(direction: HeatFlowDirection) -> float:
    """Return Rsi for a given heat flow direction."""
    return RSI_VALUES[direction]


# ---------------------------------------------------------------------------
# Tab 1.1 — Required U-values for opaque constructions  [W/(m²·K)]
# ---------------------------------------------------------------------------
U_REQUIREMENTS_OPAQUE: dict[ConstructionType, dict[AssessmentLevel, float]] = {
    ConstructionType.WALL: {
        AssessmentLevel.U_MAX: 0.46,
        AssessmentLevel.U_N: 0.32,
        AssessmentLevel.U_R1: 0.22,
        AssessmentLevel.U_R2: 0.15,
    },
    ConstructionType.ROOF: {
        AssessmentLevel.U_MAX: 0.3,
        AssessmentLevel.U_N: 0.2,
        AssessmentLevel.U_R1: 0.15,
        AssessmentLevel.U_R2: 0.1,
    },
    ConstructionType.CEILING_EXT: {
        AssessmentLevel.U_MAX: 0.3,
        AssessmentLevel.U_N: 0.2,
        AssessmentLevel.U_R1: 0.15,
        AssessmentLevel.U_R2: 0.1,
    },
    ConstructionType.CEILING: {
        AssessmentLevel.U_MAX: 0.35,
        AssessmentLevel.U_N: 0.25,
        AssessmentLevel.U_R1: 0.2,
        AssessmentLevel.U_R2: 0.15,
    },
    ConstructionType.INT_HOR_10: {
        AssessmentLevel.U_MAX: 2.75,
        AssessmentLevel.U_N: 1.5,
        AssessmentLevel.U_R1: 1.2,
        AssessmentLevel.U_R2: 1,
    },
    ConstructionType.INT_UP_10: {
        AssessmentLevel.U_MAX: 3.35,
        AssessmentLevel.U_N: 1.7,
        AssessmentLevel.U_R1: 1.2,
        AssessmentLevel.U_R2: 0.95,
    },
    ConstructionType.INT_DOWN_10: {
        AssessmentLevel.U_MAX: 2.3,
        AssessmentLevel.U_N: 1.35,
        AssessmentLevel.U_R1: 0.85,
        AssessmentLevel.U_R2: 0.6,
    },
    ConstructionType.INT_HOR_15: {
        AssessmentLevel.U_MAX: 1.8,
        AssessmentLevel.U_N: 1.05,
        AssessmentLevel.U_R1: 0.75,
        AssessmentLevel.U_R2: 0.7,
    },
    ConstructionType.INT_UP_15: {
        AssessmentLevel.U_MAX: 2,
        AssessmentLevel.U_N: 1.1,
        AssessmentLevel.U_R1: 0.75,
        AssessmentLevel.U_R2: 0.5,
    },
    ConstructionType.INT_DOWN_15: {
        AssessmentLevel.U_MAX: 1.6,
        AssessmentLevel.U_N: 0.95,
        AssessmentLevel.U_R1: 0.6,
        AssessmentLevel.U_R2: 0.35,
    },
    ConstructionType.INT_HOR_20: {
        AssessmentLevel.U_MAX: 1.3,
        AssessmentLevel.U_N: 0.8,
        AssessmentLevel.U_R1: 0.6,
        AssessmentLevel.U_R2: 0.55,
    },
    ConstructionType.INT_UP_20: {
        AssessmentLevel.U_MAX: 1.45,
        AssessmentLevel.U_N: 0.85,
        AssessmentLevel.U_R1: 0.6,
        AssessmentLevel.U_R2: 0.35,
    },
    ConstructionType.INT_DOWN_20: {
        AssessmentLevel.U_MAX: 1.2,
        AssessmentLevel.U_N: 0.75,
        AssessmentLevel.U_R1: 0.5,
        AssessmentLevel.U_R2: 0.25,
    },
    ConstructionType.INT_HOR_25: {
        AssessmentLevel.U_MAX: 1.05,
        AssessmentLevel.U_N: 0.65,
        AssessmentLevel.U_R1: 0.55,
        AssessmentLevel.U_R2: 0.45,
    },
    ConstructionType.INT_UP_25: {
        AssessmentLevel.U_MAX: 1.1,
        AssessmentLevel.U_N: 0.7,
        AssessmentLevel.U_R1: 0.5,
        AssessmentLevel.U_R2: 0.3,
    },
    ConstructionType.INT_DOWN_25: {
        AssessmentLevel.U_MAX: 0.95,
        AssessmentLevel.U_N: 0.6,
        AssessmentLevel.U_R1: 0.4,
        AssessmentLevel.U_R2: 0.2,
    },
    ConstructionType.INT_HOR_OVER25: {
        AssessmentLevel.U_MAX: 0.8,
        AssessmentLevel.U_N: 0.45,
        AssessmentLevel.U_R1: 0.4,
        AssessmentLevel.U_R2: 0.35,
    },
    ConstructionType.INT_UP_OVER25: {
        AssessmentLevel.U_MAX: 0.85,
        AssessmentLevel.U_N: 0.5,
        AssessmentLevel.U_R1: 0.4,
        AssessmentLevel.U_R2: 0.25,
    },
    ConstructionType.INT_DOWN_OVER25: {
        AssessmentLevel.U_MAX: 0.75,
        AssessmentLevel.U_N: 0.4,
        AssessmentLevel.U_R1: 0.3,
        AssessmentLevel.U_R2: 0.15,
    },
    ConstructionType.EARTH_WALL_05: {
        AssessmentLevel.U_MAX: 0.613,
        AssessmentLevel.U_N: 0.469,
        AssessmentLevel.U_R1: 0.38,
        AssessmentLevel.U_R2: 0.38,
    },
    ConstructionType.EARTH_WALL_20: {
        AssessmentLevel.U_MAX: 0.885,
        AssessmentLevel.U_N: 0.613,
        AssessmentLevel.U_R1: 0.469,
        AssessmentLevel.U_R2: 0.469,
    },
    ConstructionType.EARTH_WALL_OVER20: {
        AssessmentLevel.U_MAX: 1.205,
        AssessmentLevel.U_N: 0.752,
        AssessmentLevel.U_R1: 0.613,
        AssessmentLevel.U_R2: 0.613,
    },
    ConstructionType.EARTH_FLOOR_EDGE: {
        AssessmentLevel.U_MAX: 0.599,
        AssessmentLevel.U_N: 0.405,
        AssessmentLevel.U_R1: 0.375,
        AssessmentLevel.U_R2: 0.375,
    },
    ConstructionType.EARTH_FLOOR_OTHER: {
        AssessmentLevel.U_MAX: 0.855,
        AssessmentLevel.U_N: 0.599,
        AssessmentLevel.U_R1: 0.461,
        AssessmentLevel.U_R2: 0.461,
    },
}

# ---------------------------------------------------------------------------
# Tab 1.3 — Required U-values for transparent constructions (windows/doors)
# ---------------------------------------------------------------------------
U_REQUIREMENTS_TRANSPARENT: dict[ConstructionType, dict[AssessmentLevel, float]] = {
    ConstructionType.WINDOW: {
        AssessmentLevel.U_MAX: 1.7,
        AssessmentLevel.U_N: 1.4,
        AssessmentLevel.U_R1: 1.0,
        AssessmentLevel.U_R2: 0.6,
    },
    ConstructionType.DOOR: {
        AssessmentLevel.U_MAX: 4.3,
        AssessmentLevel.U_N: 3.0,
        AssessmentLevel.U_R1: 2.5,
        AssessmentLevel.U_R2: 2.0,
    },
}

# Merged lookup for convenience
_ALL_REQUIREMENTS = {**U_REQUIREMENTS_OPAQUE, **U_REQUIREMENTS_TRANSPARENT}


def get_required_u(
    construction_type: ConstructionType,
    level: AssessmentLevel,
) -> float:
    """
    Get the required U-value for a given construction type and assessment level.

    Raises KeyError if the combination is not found.
    """
    return _ALL_REQUIREMENTS[construction_type][level]


def is_transparent(construction_type: ConstructionType) -> bool:
    """Check if a construction type is transparent (window/door)."""
    return construction_type in U_REQUIREMENTS_TRANSPARENT
