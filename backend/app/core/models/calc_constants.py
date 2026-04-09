"""
Shared CalcConstants model — Smart Defaults + Expert Override pattern.

Every normative constant used across all chapters can be optionally overridden
by the user via the API request. If an override is not provided, the STN/EN default
is used transparently.

Usage pattern:
    1. Accept ``CalcConstantsOverride | None`` in every chapter's request model.
    2. Call ``resolve_constants(overrides)`` at the start of each service function.
    3. Use ``ResolvedConstants`` values in all calculations.
    4. Include ``ResolvedConstants`` and ``list[CalcStep]`` in every result model.

Source of truth for defaults:
    - STN 73 0540-2/Z1+Z2 (Kap. 1)
    - STN EN ISO 52016-1, Krajčík et al. (Kap. 2)
    - STN EN 15316-1/2/3 (Kap. 3)
    - Vyhláška MDVRR SR č. 364/2012 (Kap. 9)
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# CalcStep — one step in a calculation trace
# ---------------------------------------------------------------------------

class CalcStep(BaseModel):
    """One step in a step-by-step calculation trace."""
    label: str = Field(description="Krátky popis kroku (po slovensky)")
    formula: str = Field(description="Formula so symbolmi, napr. 'HT = Σ(bx·U·A) + ΔU·ΣA'")
    inputs: dict[str, Any] = Field(
        default_factory=dict,
        description="Vstupné hodnoty použité v tomto kroku",
    )
    result: float = Field(description="Vypočítaný výsledok")
    unit: str = Field(default="", description="Fyzikálna jednotka výsledku")
    norm_ref: str = Field(
        default="",
        description="Referencia na normu, napr. 'STN EN ISO 52016-1, vzorec (2.3)'",
    )


# ---------------------------------------------------------------------------
# CalcConstantsOverride — user-supplied overrides (all optional)
# ---------------------------------------------------------------------------

class CalcConstantsOverride(BaseModel):
    """
    Optional user overrides for normative constants.

    Every field defaults to None, meaning "use the STN default".
    Provide a value only if you want to deviate from the norm.
    """

    # ── Chapter 1 — Thermal-technical assessment ───────────────────────────
    rse: float | None = Field(
        default=None,
        description=(
            "Vonkajší povrchový tepelný odpor Rse [(m²·K)/W]. "
            "Normová hodnota: 0.04 (STN 73 0540-2/Z1+Z2, Tab. 1.1 pozn.)"
        ),
    )
    rsi_horizontal: float | None = Field(
        default=None,
        description=(
            "Vnútorný povrchový odpor pre vodorovný tok Rsi [(m²·K)/W]. "
            "Normová hodnota: 0.13"
        ),
    )
    rsi_upward: float | None = Field(
        default=None,
        description=(
            "Vnútorný povrchový odpor pre tok zdola nahor Rsi [(m²·K)/W]. "
            "Normová hodnota: 0.10"
        ),
    )
    rsi_downward: float | None = Field(
        default=None,
        description=(
            "Vnútorný povrchový odpor pre tok zhora nadol Rsi [(m²·K)/W]. "
            "Normová hodnota: 0.17"
        ),
    )

    # ── Chapter 2 — Heating demand ─────────────────────────────────────────
    rho_air: float | None = Field(
        default=None,
        description=(
            "Hustota vzduchu ρa [kg/m³]. "
            "Normová hodnota: 1.2 (STN EN ISO 52016-1)"
        ),
    )
    c_air: float | None = Field(
        default=None,
        description=(
            "Merná tepelná kapacita vzduchu ca [J/(kg·K)]. "
            "Normová hodnota: 1010"
        ),
    )
    min_air_change: float | None = Field(
        default=None,
        description=(
            "Minimálna intenzita výmeny vzduchu ninf,min [1/h]. "
            "Normová hodnota: 0.5 (Vyhláška 364/2012)"
        ),
    )
    # Solar radiation overrides [kWh/(m²·vykurovaná sezóna)]
    solar_south: float | None = Field(
        default=None,
        description="Isol pre juh [kWh/m²]. Normová hodnota: 320",
    )
    solar_north: float | None = Field(
        default=None,
        description="Isol pre sever [kWh/m²]. Normová hodnota: 100",
    )
    solar_east_west: float | None = Field(
        default=None,
        description="Isol pre východ/západ [kWh/m²]. Normová hodnota: 200",
    )
    solar_se_sw: float | None = Field(
        default=None,
        description="Isol pre JV/JZ [kWh/m²]. Normová hodnota: 260",
    )
    solar_ne_nw: float | None = Field(
        default=None,
        description="Isol pre SV/SZ [kWh/m²]. Normová hodnota: 130",
    )
    solar_horizontal: float | None = Field(
        default=None,
        description="Isol pre horizontálnu rovinu [kWh/m²]. Normová hodnota: 340",
    )

    # ── Chapter 3 — Heating energy ─────────────────────────────────────────
    gen_efficiency_override: float | None = Field(
        default=None,
        ge=0.1,
        le=6.0,
        description=(
            "Vlastná účinnosť / COP zdroja tepla η_gen [-]. "
            "Ak None, použije sa hodnota z tabuľky (Tab. 3.10)."
        ),
    )

    # ── Chapter 4 — DHW ───────────────────────────────────────────────────
    dhw_water_density: float | None = Field(
        default=None,
        description=(
            "Hustota vody ρw [kg/l]. "
            "Normová hodnota: 1.0"
        ),
    )
    dhw_specific_heat: float | None = Field(
        default=None,
        description=(
            "Merná tepelná kapacita vody cw [Wh/(kg·K)]. "
            "Normová hodnota: 1.163"
        ),
    )
    dhw_cold_water_temp: float | None = Field(
        default=None,
        description=(
            "Teplota studenej vody θcw [°C]. "
            "Normová hodnota: 10.0"
        ),
    )
    dhw_hot_water_temp: float | None = Field(
        default=None,
        description=(
            "Teplota teplej vody θhw [°C]. "
            "Normová hodnota: 55.0"
        ),
    )

    # ── Chapter 6 — Renovation ────────────────────────────────────────────
    psi_insulated_overrides: dict[int, float] | None = Field(
        default=None,
        description=(
            "Vlastné hodnoty Ψ [W/(m·K)] po zaizolovaní podľa DN. "
            "Napr. {65: 0.296, 50: 0.243}. Normové hodnoty sú z Tab. 6.2."
        ),
    )


# ---------------------------------------------------------------------------
# ResolvedConstants — final values used in a calculation
# ---------------------------------------------------------------------------

class ResolvedConstant(BaseModel):
    """A single resolved constant with its source."""
    value: float
    source: str = Field(description="'STN default' alebo 'User override'")
    norm_ref: str = Field(default="", description="Normatívna referencia")
    description: str = Field(default="")


class ResolvedConstants(BaseModel):
    """
    Final values used in the calculation, after resolving user overrides
    against STN defaults. Included in every result model.
    """
    # Chapter 1
    rse: ResolvedConstant
    rsi_horizontal: ResolvedConstant
    rsi_upward: ResolvedConstant
    rsi_downward: ResolvedConstant

    # Chapter 2
    rho_air: ResolvedConstant
    c_air: ResolvedConstant
    min_air_change: ResolvedConstant
    solar_south: ResolvedConstant
    solar_north: ResolvedConstant
    solar_east_west: ResolvedConstant
    solar_se_sw: ResolvedConstant
    solar_ne_nw: ResolvedConstant
    solar_horizontal: ResolvedConstant

    # Chapter 4
    dhw_water_density: ResolvedConstant
    dhw_specific_heat: ResolvedConstant
    dhw_cold_water_temp: ResolvedConstant
    dhw_hot_water_temp: ResolvedConstant


# ---------------------------------------------------------------------------
# STN defaults registry
# ---------------------------------------------------------------------------

_STN_DEFAULTS: dict[str, tuple[float, str, str]] = {
    # key: (value, norm_ref, description_sk)
    "rse": (
        0.04,
        "STN 73 0540-2/Z1+Z2, Tab. 1.1 poznámka",
        "Vonkajší povrchový tepelný odpor Rse",
    ),
    "rsi_horizontal": (
        0.13,
        "STN 73 0540-2/Z1+Z2, Tab. 1.1",
        "Rsi — vodorovný tepelný tok (steny)",
    ),
    "rsi_upward": (
        0.10,
        "STN 73 0540-2/Z1+Z2, Tab. 1.1",
        "Rsi — tok zdola nahor (strechy)",
    ),
    "rsi_downward": (
        0.17,
        "STN 73 0540-2/Z1+Z2, Tab. 1.1",
        "Rsi — tok zhora nadol (podlahy)",
    ),
    "rho_air": (
        1.2,
        "STN EN ISO 52016-1",
        "Hustota vzduchu ρa",
    ),
    "c_air": (
        1010.0,
        "STN EN ISO 52016-1",
        "Merná tepelná kapacita vzduchu ca",
    ),
    "min_air_change": (
        0.5,
        "Vyhláška MDVRR SR č. 364/2012",
        "Minimálna intenzita výmeny vzduchu ninf,min",
    ),
    "solar_south": (320.0, "STN EN ISO 13790/NA, Tab. 2.3", "Isol — Juh"),
    "solar_north": (100.0, "STN EN ISO 13790/NA, Tab. 2.3", "Isol — Sever"),
    "solar_east_west": (200.0, "STN EN ISO 13790/NA, Tab. 2.3", "Isol — Východ/Západ"),
    "solar_se_sw": (260.0, "STN EN ISO 13790/NA, Tab. 2.3", "Isol — JV/JZ"),
    "solar_ne_nw": (130.0, "STN EN ISO 13790/NA, Tab. 2.3", "Isol — SV/SZ"),
    "solar_horizontal": (340.0, "STN EN ISO 13790/NA, Tab. 2.3", "Isol — Horizontálna"),
    "dhw_water_density": (1.0, "Fyzikálna konštanta", "Hustota vody ρw"),
    "dhw_specific_heat": (
        1.163,
        "Fyzikálna konštanta (4186 J/(kg·K) → Wh)",
        "Merná tepelná kapacita vody cw",
    ),
    "dhw_cold_water_temp": (
        10.0,
        "STN EN 15316-3-1, Tab. NA",
        "Teplota studenej vody θcw",
    ),
    "dhw_hot_water_temp": (
        55.0,
        "Vyhláška MDVRR SR č. 364/2012",
        "Teplota teplej vody θhw",
    ),
}


def _resolve_one(key: str, override: float | None) -> ResolvedConstant:
    """Resolve a single constant: use override if provided, else STN default."""
    default_value, norm_ref, description = _STN_DEFAULTS[key]
    if override is not None:
        return ResolvedConstant(
            value=override,
            source="User override",
            norm_ref=norm_ref,
            description=description,
        )
    return ResolvedConstant(
        value=default_value,
        source="STN default",
        norm_ref=norm_ref,
        description=description,
    )


def resolve_constants(
    overrides: CalcConstantsOverride | None = None,
) -> ResolvedConstants:
    """
    Resolve all constants against STN defaults.

    Call this once at the start of every service function.

    Args:
        overrides: Optional user-supplied overrides. Pass None to use all STN defaults.

    Returns:
        ResolvedConstants with final values and source annotations.
    """
    o = overrides or CalcConstantsOverride()

    return ResolvedConstants(
        rse=_resolve_one("rse", o.rse),
        rsi_horizontal=_resolve_one("rsi_horizontal", o.rsi_horizontal),
        rsi_upward=_resolve_one("rsi_upward", o.rsi_upward),
        rsi_downward=_resolve_one("rsi_downward", o.rsi_downward),
        rho_air=_resolve_one("rho_air", o.rho_air),
        c_air=_resolve_one("c_air", o.c_air),
        min_air_change=_resolve_one("min_air_change", o.min_air_change),
        solar_south=_resolve_one("solar_south", o.solar_south),
        solar_north=_resolve_one("solar_north", o.solar_north),
        solar_east_west=_resolve_one("solar_east_west", o.solar_east_west),
        solar_se_sw=_resolve_one("solar_se_sw", o.solar_se_sw),
        solar_ne_nw=_resolve_one("solar_ne_nw", o.solar_ne_nw),
        solar_horizontal=_resolve_one("solar_horizontal", o.solar_horizontal),
        dhw_water_density=_resolve_one("dhw_water_density", o.dhw_water_density),
        dhw_specific_heat=_resolve_one("dhw_specific_heat", o.dhw_specific_heat),
        dhw_cold_water_temp=_resolve_one("dhw_cold_water_temp", o.dhw_cold_water_temp),
        dhw_hot_water_temp=_resolve_one("dhw_hot_water_temp", o.dhw_hot_water_temp),
    )


def get_deviations(resolved: ResolvedConstants) -> list[str]:
    """
    Return a list of human-readable strings describing all user overrides.

    Useful for including in audit results so the reader knows which constants
    deviate from the STN norm.
    """
    deviations: list[str] = []
    for field_name in resolved.model_fields:
        rc: ResolvedConstant = getattr(resolved, field_name)
        if rc.source == "User override":
            default_value = _STN_DEFAULTS[field_name][0]
            deviations.append(
                f"{field_name}: použitá hodnota {rc.value} "
                f"(STN default: {default_value}, ref: {rc.norm_ref})"
            )
    return deviations
