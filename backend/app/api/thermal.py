"""
Thermal assessment API endpoints.

Provides REST API for:
- Calculating U-values from material layers
- Assessing constructions against STN 73 0540-2/Z1+Z2
- Full building assessment
"""

from fastapi import APIRouter

from app.core.models.building import (
    AssessmentLevel,
    Building,
    Construction,
    HeatFlowDirection,
    MaterialLayer,
)
from app.core.services.thermal_assessment import (
    AssessmentResult,
    BuildingAssessmentResult,
    DetailedAssessmentRequest,
    DetailedAssessmentResult,
    LayerCalculationResult,
    assess_building,
    assess_construction,
    assess_detailed_construction,
    calculate_u_from_layers,
)
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/thermal", tags=["Thermal Assessment"])


# ---- Request/Response models ----

class CalculateURequest(BaseModel):
    """Request to calculate U-value from material layers."""
    layers: list[MaterialLayer] = Field(..., min_length=1)
    heat_flow_direction: HeatFlowDirection = HeatFlowDirection.HORIZONTAL
    rse: float = Field(default=0.04, ge=0, description="Vonkajší povrchový odpor Rse")


class AssessConstructionRequest(BaseModel):
    """Request to assess a single construction."""
    construction: Construction
    level: AssessmentLevel = AssessmentLevel.U_R1


class AssessBuildingRequest(BaseModel):
    """Request to assess an entire building."""
    building: Building
    level: AssessmentLevel = AssessmentLevel.U_R1


# ---- Endpoints ----

@router.post("/calculate-u", response_model=LayerCalculationResult)
async def calculate_u_endpoint(request: CalculateURequest) -> LayerCalculationResult:
    """
    Calculate U-value from material layers.

    Uses formulas (1.4) and (1.2):
    - ΣR = Σ(di / λi)
    - U = 1 / (Rsi + ΣR + Rse)
    """
    return calculate_u_from_layers(
        layers=request.layers,
        heat_flow_direction=request.heat_flow_direction,
        rse=request.rse,
    )


@router.post("/assess", response_model=AssessmentResult)
async def assess_construction_endpoint(request: AssessConstructionRequest) -> AssessmentResult:
    """
    Assess a single construction against STN 73 0540-2/Z1+Z2.

    Compares U-value with the required value for the given level.
    """
    return assess_construction(
        construction=request.construction,
        level=request.level,
    )


@router.post("/assess-detailed", response_model=DetailedAssessmentResult)
async def assess_detailed_endpoint(request: DetailedAssessmentRequest) -> DetailedAssessmentResult:
    """
    Perform detailed assessment of a construction (Elaborát).
    Includes surface temperature and mold risk.
    """
    return assess_detailed_construction(request)


@router.post("/assess-building", response_model=BuildingAssessmentResult)
async def assess_building_endpoint(request: AssessBuildingRequest) -> BuildingAssessmentResult:
    """
    Assess all constructions in a building.

    Returns individual results and overall pass/fail.
    """
    return assess_building(
        building=request.building,
        level=request.level,
    )
