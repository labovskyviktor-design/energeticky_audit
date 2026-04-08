"""
Thermal Assessment Service — Core calculation engine for Chapter 1.

Implements thermal-technical assessment of building constructions
according to STN 73 0540-2/Z1.

Formulas:
    (1.2) U = 1 / (Rsi + ΣR + Rse)
    (1.4) ΣR = Σ(di / λi)
    (1.1) U ≤ U_r1 (opaque)
    (1.5) UW ≤ UW,r1 (transparent)

Source of truth: Krajčík, M. a kol. — Energetické hodnotenie budov, str. 10–22.
"""

from pydantic import BaseModel, Field

from app.core.models.building import (
    AssessmentLevel,
    Building,
    Construction,
    HeatFlowDirection,
    MaterialLayer,
)
from app.core.models.requirements import RSE, get_required_u, get_rsi, is_transparent
from app.core.services.psychrometrics import (
    calculate_critical_surface_temperature,
    calculate_saturation_pressure,
)


class AssessmentResult(BaseModel):
    """Result of thermal-technical assessment for a single construction."""
    construction_name: str
    u_value: float = Field(description="Actual U-value [W/(m²·K)]")
    u_required: float = Field(description="Required U-value [W/(m²·K)]")
    passes: bool = Field(description="True if construction meets the requirement")
    verdict: str = Field(description="VYHOVUJE / NEVYHOVUJE")


class DetailedAssessmentRequest(BaseModel):
    """Detailed request for construction assessment (Elaborát)."""
    construction: Construction
    level: AssessmentLevel = AssessmentLevel.U_R2
    internal_temperature: float = Field(default=20.0, description="Vnútorná teplota θj [°C]")
    external_temperature: float = Field(default=-11.0, description="Vonkajšia teplota θe [°C]")
    internal_humidity: float = Field(default=50.0, description="Relatívna vlhkosť interiéru φi [%]")
    external_humidity: float = Field(default=83.0, description="Relatívna vlhkosť exteriéru φe [%]")
    rse: float = Field(default=0.04, description="Odpor pri prestupe tepla Rse [(m²·K)/W]")
    rsi: float = Field(default=0.13, description="Odpor pri prestupe tepla Rsi [(m²·K)/W]")
    safety_margin: float = Field(default=1.0, description="Bezpečnostná prirážka Δθsi [K]")


class DetailedAssessmentResult(BaseModel):
    """Comprehensive result for the construction assessment report."""
    construction_name: str
    # Parameters
    ti: float
    te: float
    phi_i: float
    phi_e: float
    rse: float
    rsi: float
    # Calculated values
    r_construction: float = Field(description="Tepelný odpor konštrukcie R [(m²·K)/W]")
    r_total: float = Field(description="Odpor pri prechode tepla R0 [(m²·K)/W]")
    u_value: float = Field(description="Súčiniteľ prechodu tepla U [W/(m²·K)]")
    sd_value: float = Field(description="Ekvivalentná difúzna hrúbka Sd [m]")
    # Surface temperature & mold risk
    theta_si: float = Field(description="Vnútorná povrchová teplota θsi [°C]")
    theta_si_min: float = Field(description="Kritická povrchová teplota θsi,min [°C]")
    # Assessments
    u_required: float
    u_pass: bool
    mold_pass: bool
    r_required: float
    r_pass: bool


class LayerCalculationResult(BaseModel):
    """Result of R and U calculation from material layers."""
    r_total: float = Field(description="Total thermal resistance ΣR [(m²·K)/W]")
    rsi: float = Field(description="Surface resistance Rsi [(m²·K)/W]")
    rse: float = Field(description="Surface resistance Rse [(m²·K)/W]")
    r_total_with_surface: float = Field(description="Rsi + ΣR + Rse [(m²·K)/W]")
    u_value: float = Field(description="Calculated U-value [W/(m²·K)]")


def assess_detailed_construction(request: DetailedAssessmentRequest) -> DetailedAssessmentResult:
    """
    Perform detailed assessment (Part 1 - Elaborát).
    """
    c = request.construction
    r_construction = calculate_r_from_layers(c.layers) if c.layers else (1.0 / c.u_value - request.rsi - request.rse)
    r_total = r_construction + request.rsi + request.rse
    u_value = 1.0 / r_total

    # Surface temperature
    delta_t = request.internal_temperature - request.external_temperature
    theta_si = request.internal_temperature - request.rsi * u_value * delta_t

    # Mold risk
    theta_si_min = calculate_critical_surface_temperature(
        request.internal_temperature, request.internal_humidity
    )
    mold_pass = theta_si >= (theta_si_min + request.safety_margin)

    # U-value assessment
    u_required = get_required_u(c.construction_type, request.level)
    u_pass = u_value <= u_required

    # R-value assessment (R >= R_N = 1/U_N - Rsi - Rse)
    r_required = (1.0 / u_required) - request.rsi - request.rse
    r_pass = r_construction >= r_required

    # Diffusion (Sd)
    sd_value = sum(layer.vapor_resistance for layer in c.layers) if c.layers else 0.0

    return DetailedAssessmentResult(
        construction_name=c.name,
        ti=request.internal_temperature,
        te=request.external_temperature,
        phi_i=request.internal_humidity,
        phi_e=request.external_humidity,
        rse=request.rse,
        rsi=request.rsi,
        r_construction=round(r_construction, 2),
        r_total=round(r_total, 2),
        u_value=round(u_value, 2),
        sd_value=round(sd_value, 2),
        theta_si=round(theta_si, 2),
        theta_si_min=round(theta_si_min, 2),
        u_required=u_required,
        u_pass=u_pass,
        mold_pass=mold_pass,
        r_required=round(r_required, 2),
        r_pass=r_pass,
    )


class BuildingAssessmentResult(BaseModel):
    """Full assessment result for an entire building."""
    building_name: str
    results: list[AssessmentResult]
    all_pass: bool


# ---------------------------------------------------------------------------
# Core calculation functions (pure, no side effects)
# ---------------------------------------------------------------------------


def calculate_r_from_layers(layers: list[MaterialLayer]) -> float:
    """
    Calculate total thermal resistance from material layers.

    Formula (1.4): ΣR = Σ(di / λi)

    Args:
        layers: List of material layers with thickness and conductivity.

    Returns:
        Total thermal resistance ΣR in (m²·K)/W.
    """
    if not layers:
        raise ValueError("At least one material layer is required.")
    return sum(layer.thermal_resistance for layer in layers)


def calculate_u_from_r(
    r_total: float,
    rsi: float,
    rse: float = RSE,
) -> float:
    """
    Calculate U-value from total thermal resistance and surface resistances.

    Formula (1.2): U = 1 / (Rsi + ΣR + Rse)

    Args:
        r_total: Total thermal resistance of layers ΣR [(m²·K)/W].
        rsi: Internal surface resistance Rsi [(m²·K)/W].
        rse: External surface resistance Rse [(m²·K)/W]. Defaults to 0.04.

    Returns:
        U-value in W/(m²·K).
    """
    denominator = rsi + r_total + rse
    if denominator <= 0:
        raise ValueError("Total resistance (Rsi + R + Rse) must be positive.")
    return 1.0 / denominator


def calculate_u_from_layers(
    layers: list[MaterialLayer],
    heat_flow_direction: HeatFlowDirection = HeatFlowDirection.HORIZONTAL,
    rse: float = RSE,
) -> LayerCalculationResult:
    """
    Full calculation: layers → R → U.

    Combines formulas (1.4) and (1.2).

    Args:
        layers: Material layers of the construction.
        heat_flow_direction: Direction of heat flow (determines Rsi).
        rse: External surface resistance. Defaults to 0.04.

    Returns:
        LayerCalculationResult with all intermediate values.
    """
    r_total = calculate_r_from_layers(layers)
    rsi = get_rsi(heat_flow_direction)
    r_with_surface = rsi + r_total + rse
    u_value = 1.0 / r_with_surface

    return LayerCalculationResult(
        r_total=round(r_total, 2),
        rsi=rsi,
        rse=rse,
        r_total_with_surface=round(r_with_surface, 2),
        u_value=round(u_value, 2),
    )


def assess_construction(
    construction: Construction,
    level: AssessmentLevel = AssessmentLevel.U_R1,
) -> AssessmentResult:
    """
    Assess a single construction against STN 73 0540-2/Z1 requirements.

    For opaque constructions: Formula (1.1) U ≤ U_r1
    For transparent constructions: Formula (1.5) UW ≤ UW,r1 (or UW,max)

    Args:
        construction: The construction element to assess.
        level: Assessment level (U_MAX, U_N, U_R1, U_R2).

    Returns:
        AssessmentResult with verdict.
    """
    u_required = get_required_u(construction.construction_type, level)
    passes = construction.u_value <= u_required
    verdict = "VYHOVUJE" if passes else "NEVYHOVUJE"

    return AssessmentResult(
        construction_name=construction.name,
        u_value=construction.u_value,
        u_required=u_required,
        passes=passes,
        verdict=verdict,
    )


def assess_building(
    building: Building,
    level: AssessmentLevel = AssessmentLevel.U_R1,
) -> BuildingAssessmentResult:
    """
    Assess all constructions in a building.

    Args:
        building: The building to assess.
        level: Assessment level for all constructions.

    Returns:
        BuildingAssessmentResult with individual results and overall pass/fail.
    """
    results: list[AssessmentResult] = []
    for zone in building.zones:
        for construction in zone.constructions:
            result = assess_construction(construction, level)
            results.append(result)

    return BuildingAssessmentResult(
        building_name=building.name,
        results=results,
        all_pass=all(r.passes for r in results),
    )
