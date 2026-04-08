"""
Energy Balance Service — Seasonal heating demand calculation (Chapter 2).

Implements the seasonal method for calculating heating demand
according to STN EN ISO 52016-1.

Formulas:
    (2.1)  QH = Qht − ηgn · Qgn
    (2.2)  Qht = (HT + HV) · (θint − θe,m) · t · 0.024
    (2.3)  HT = Σ(bx·U·A) + ΔU·ΣA
    (2.4)  HV = (V/Vb) · ρa · ca · ninf · Vb / 3600
    (2.5)  ninf = (3600 · Σ(ilv·l)) / Vb
    (2.6)  Qgn = Qint + Qsol
    (2.7)  Qint = n · 0.024 · qi · Ab
    (2.8)  Qsol,k = Fsh,ob,k · Asol,k · Isol,k
    (2.9)  Asol = Fsh,gl · ggl · (1−FF) · Aw,p
    (2.10) ggl = Fw · ggl,n
    (2.11) Vb = Ab · hk,pr

Source of truth: Krajčík, M. a kol. — Energetické hodnotenie budov, str. 22–37.
"""

from pydantic import BaseModel, Field

from app.core.models.building import AssessmentLevel
from app.core.models.climate import (
    ClimateData,
    ConstructionHTEntry,
    HeatingDemandInput,
    InfiltrationEntry,
    WindowSolarEntry,
)
from app.core.models.energy_constants import (
    get_qh_nd_required,
)
from app.core.models.calc_constants import (
    resolve_constants,
    ResolvedConstants,
    get_deviations,
)


# ---------------------------------------------------------------------------
# Result models
# ---------------------------------------------------------------------------

class HTResult(BaseModel):
    """Result of HT (transmission heat loss) calculation."""
    sum_bx_u_a: float = Field(description="Σ(bx·U·A) [W/K]")
    delta_u: float = Field(description="ΔU [W/(m²·K)]")
    sum_a: float = Field(description="ΣA [m²]")
    delta_ht: float = Field(description="ΔU·ΣA [W/K]")
    ht: float = Field(description="HT = Σ(bx·U·A) + ΔU·ΣA [W/K]")


class HVResult(BaseModel):
    """Result of HV (ventilation heat loss) calculation."""
    n_inf: float = Field(description="Intenzita výmeny vzduchu [1/h]")
    v_vb_ratio: float = Field(description="V/Vb [-]")
    vb: float = Field(description="Obostavaný objem [m³]")
    hv: float = Field(description="HV [W/K]")


class HeatGainsResult(BaseModel):
    """Result of heat gains calculation."""
    q_internal: float = Field(description="Qint [kWh/a]")
    q_solar: float = Field(description="Qsol [kWh/a]")
    q_gains_total: float = Field(description="Qgn = Qint + Qsol [kWh/a]")


class HeatingDemandResult(BaseModel):
    """Complete result of seasonal heating demand calculation."""
    # Building info
    building_name: str
    ab: float = Field(description="Merná plocha Ab [m²]")
    vb: float = Field(description="Obostavaný objem Vb [m³]")
    shape_factor: float = Field(description="Faktor tvaru ΣAi/Vb [1/m]")

    # Heat losses
    ht_result: HTResult
    hv_result: HVResult
    h_total: float = Field(description="H = HT + HV [W/K]")
    q_ht: float = Field(description="Qht celková tepelná strata [kWh/a]")
    phi_hl: float = Field(description="ΦHL - Tepelný príkon (strata) pri návrhovej teplote [kW]")

    # Heat gains
    gains_result: HeatGainsResult
    eta_gn: float = Field(description="Faktor využitia tepelných ziskov [-]")

    # Final results
    qh: float = Field(description="QH potreba tepla na vykurovanie [kWh/a]")
    qh_nd: float = Field(description="QH,nd merná potreba tepla [kWh/(m²·a)]")

    # Assessment
    qh_nd_required: float = Field(description="Požadovaná QH,nd [kWh/(m²·a)]")
    passes: bool
    verdict: str
    resolved_constants: ResolvedConstants | None = None
    deviations: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Core calculation functions
# ---------------------------------------------------------------------------


def calculate_ht(
    constructions: list[ConstructionHTEntry],
    delta_u: float,
) -> HTResult:
    """
    Calculate transmission heat loss coefficient HT.

    Formula (2.3): HT = Σ(bx,i · Ui · Ai) + ΔU · ΣAi
    """
    sum_bx_u_a = sum(c.bx * c.u_value * c.area for c in constructions)
    sum_a = sum(c.area for c in constructions)
    delta_ht = delta_u * sum_a
    ht = sum_bx_u_a + delta_ht

    return HTResult(
        sum_bx_u_a=round(sum_bx_u_a, 1),
        delta_u=delta_u,
        sum_a=round(sum_a, 1),
        delta_ht=round(delta_ht, 1),
        ht=round(ht, 1),
    )


def calculate_infiltration(
    entries: list[InfiltrationEntry],
    vb: float,
    min_air_change: float,
    v_vb_ratio: float = 0.80,
) -> float:
    """
    Calculate air infiltration rate ninf.

    Formula (2.5) per STN 73 0540-3:
        ninf = (25200 · Σ(ilv,j · lj)) / V

    Where:
        - ilv values in input are × 10⁴ (as tabulated), so we apply × 1e-4
        - V = V/Vb · Vb (inner volume)
        - 25200 = STN standard coefficient
    """
    if not entries or vb <= 0:
        return min_air_change

    v_inner = v_vb_ratio * vb
    sum_ilv_l = sum(e.ilv * 1e-4 * e.joint_length for e in entries)
    n_inf = (25200.0 * sum_ilv_l) / v_inner
    return max(round(n_inf, 2), min_air_change)


def calculate_hv(
    vb: float,
    v_vb_ratio: float,
    n_inf: float,
    rho_air: float,
    c_air: float,
) -> HVResult:
    """
    Calculate ventilation heat loss coefficient HV.

    Formula (2.4): HV = (V/Vb) · ρa · ca · ninf · Vb / 3600
    """
    hv = v_vb_ratio * rho_air * c_air * n_inf * vb / 3600.0

    return HVResult(
        n_inf=round(n_inf, 2),
        v_vb_ratio=v_vb_ratio,
        vb=vb,
        hv=round(hv, 1),
    )


def calculate_qht(
    ht: float,
    hv: float,
    climate: ClimateData,
) -> float:
    """
    Calculate total heat loss during heating season.

    Formula (2.2): Qht = (HT + HV) · (θint − θe,m) · t · 0.024
    """
    return (ht + hv) * (climate.theta_int - climate.theta_e_m) * climate.heating_days * 0.024


def calculate_q_internal(
    heating_days: int,
    qi: float,
    ab: float,
) -> float:
    """
    Calculate internal heat gains.

    Formula (2.7): Qint = n · 0.024 · qi · Ab
    """
    return heating_days * 0.024 * qi * ab


def calculate_q_solar(
    windows: list[WindowSolarEntry],
    resolved: ResolvedConstants,
) -> float:
    """
    Calculate solar heat gains through windows.

    Formula (2.8): Qsol,k = Fsh,ob,k · Asol,k · Isol,k
    Where Asol,k is effectively f_shading · area (already includes ggl and FF).

    The f_shading in WindowSolarEntry already combines:
    Fsh,ob · Fsh,gl · (1-FF) as per simplified approach (section 2.1.4.2).
    """
    q_solar = 0.0
    for w in windows:
        isol_map = {
            "south": resolved.solar_south.value,
            "north": resolved.solar_north.value,
            "east_west": resolved.solar_east_west.value,
            "se_sw": resolved.solar_se_sw.value,
            "ne_nw": resolved.solar_ne_nw.value,
            "horizontal": resolved.solar_horizontal.value,
        }
        isol = isol_map.get(w.orientation.value, 0.0)
        # Effective collecting area: ggl · f_shading · area
        # f_shading already includes Fsh,ob · Fsh,gl · (1-FF) per script simplification
        q_solar += w.ggl * w.f_shading * w.area * isol
    return q_solar


def calculate_heating_demand(
    input_data: HeatingDemandInput,
    level: AssessmentLevel = AssessmentLevel.U_R1,
) -> HeatingDemandResult:
    """
    Full seasonal heating demand calculation.

    Combines all formulas (2.1)–(2.11) into a single calculation.
    """
    # 0. Resolve constants
    resolved = resolve_constants(input_data.overrides)

    # 1. HT — transmission heat loss
    ht_result = calculate_ht(input_data.constructions, input_data.delta_u)

    # 2. Ventilation — ninf and HV
    min_air_change = resolved.min_air_change.value
    if input_data.ventilation.n_inf_override is not None:
        n_inf = max(input_data.ventilation.n_inf_override, min_air_change)
    else:
        n_inf = calculate_infiltration(
            input_data.ventilation.infiltration_entries,
            input_data.vb,
            min_air_change,
            input_data.ventilation.v_vb_ratio,
        )

    hv_result = calculate_hv(
        vb=input_data.vb,
        v_vb_ratio=input_data.ventilation.v_vb_ratio,
        n_inf=n_inf,
        rho_air=resolved.rho_air.value,
        c_air=resolved.c_air.value,
    )

    # 3. Total heat loss
    h_total = ht_result.ht + hv_result.hv
    q_ht = calculate_qht(ht_result.ht, hv_result.hv, input_data.climate)

    # 4. Heat gains
    q_internal = calculate_q_internal(
        input_data.climate.heating_days,
        input_data.qi,
        input_data.ab,
    )
    q_solar = calculate_q_solar(input_data.windows_solar, resolved)
    q_gains_total = q_internal + q_solar

    gains_result = HeatGainsResult(
        q_internal=round(q_internal, 1),
        q_solar=round(q_solar, 1),
        q_gains_total=round(q_gains_total, 1),
    )

    # 5. Heating demand — Formula (2.1)
    qh = q_ht - input_data.eta_gn * q_gains_total
    qh = max(qh, 0.0)  # Heating demand cannot be negative

    # 6. Specific heating demand
    qh_nd = qh / input_data.ab

    # New: Calculate Phi_HL (Design Heat Load) for Chapter 3
    # Phi_HL = H_total * (theta_int - theta_e_des) / 1000 [kW]
    theta_e_des = input_data.climate.theta_e_des
    phi_hl = h_total * (input_data.climate.theta_int - theta_e_des) / 1000.0
    phi_hl = max(phi_hl, 0.0)

    # 7. Shape factor and assessment
    sum_a = ht_result.sum_a
    shape_factor = sum_a / input_data.vb if input_data.vb > 0 else 0
    qh_nd_required = get_qh_nd_required(shape_factor, level)
    passes = qh_nd <= qh_nd_required

    return HeatingDemandResult(
        building_name=input_data.building_name,
        ab=input_data.ab,
        vb=input_data.vb,
        shape_factor=round(shape_factor, 2),
        ht_result=ht_result,
        hv_result=hv_result,
        h_total=round(h_total, 1),
        q_ht=round(q_ht, 1),
        phi_hl=round(phi_hl, 2),
        gains_result=gains_result,
        eta_gn=input_data.eta_gn,
        qh=round(qh, 1),
        qh_nd=round(qh_nd, 2),
        qh_nd_required=qh_nd_required,
        passes=passes,
        verdict="VYHOVUJE" if passes else "NEVYHOVUJE",
        resolved_constants=resolved,
        deviations=get_deviations(resolved),
    )
