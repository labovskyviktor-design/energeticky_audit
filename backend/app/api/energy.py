"""
Energy balance API endpoints.

Provides REST API for seasonal heating demand and heating energy calculation.
"""

from fastapi import APIRouter

from app.core.models.building import AssessmentLevel
from app.core.models.climate import HeatingDemandInput
from app.core.models.heating_system import HeatingEnergyInput
from app.core.services.energy_balance import (
    HeatingDemandResult,
    calculate_heating_demand,
)
from app.core.services.heating_energy import (
    HeatingEnergyResult,
    calculate_heating_energy_demand,
)
from app.core.models.dhw import DHWInput, DHWResult
from app.core.services.dhw import calculate_dhw_demand
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/energy", tags=["Energy Balance"])


class HeatingDemandRequest(BaseModel):
    """Request for heating demand calculation."""
    input_data: HeatingDemandInput
    level: AssessmentLevel = AssessmentLevel.U_R1


@router.post("/heating-demand", response_model=HeatingDemandResult)
async def heating_demand_endpoint(request: HeatingDemandRequest) -> HeatingDemandResult:
    """
    Calculate seasonal heating demand (QH, QH,nd).

    Uses the seasonal method per STN EN ISO 52016-1.
    Returns full breakdown: HT, HV, Qht, Qint, Qsol, QH, QH,nd, and assessment.
    """
    return calculate_heating_demand(
        input_data=request.input_data,
        level=request.level,
    )


@router.post("/heating-energy-demand", response_model=HeatingEnergyResult)
async def heating_energy_demand_endpoint(request: HeatingEnergyInput) -> HeatingEnergyResult:
    """
    Calculate heating energy demand (QVYK) — Chapter 3.

    Takes QH from Chapter 2 and adds system losses:
    emission, distribution, pump energy, and generation.
    Returns full breakdown per STN EN 15316-1/2/3.
    """
    return calculate_heating_energy_demand(request)


@router.post("/dhw-demand", response_model=DHWResult)
async def dhw_demand_endpoint(request: DHWInput) -> DHWResult:
    """
    Calculate DHW energy demand (Chapter 4).
    """
    return calculate_dhw_demand(request)


from app.core.models.certificate import CertificateInput, CertificateResult
from app.core.services.certificate import generate_certificate

@router.post("/certificate", response_model=CertificateResult)
async def certificate(data: CertificateInput):
    """
    Calculate Energy Certificate (Primary Energy, CO2, A0-G Ratings).
    Aggregates Heating and DHW energy demands and losses.
    """
    return generate_certificate(data)


from app.core.models.renovation import RenovationInput, RenovationComparisonResult
from app.core.services.renovation_service import calculate_renovation


@router.post("/renovation", response_model=RenovationComparisonResult)
async def renovation_endpoint(data: RenovationInput):
    """
    Calculate renovation comparison (Before vs After) — Chapter 6.
    """
    return calculate_renovation(data)


from app.core.models.economics import EconomicsInput, EconomicsResult
from app.core.services.economics import calculate_economics


@router.post("/economics", response_model=EconomicsResult)
async def economics_endpoint(data: EconomicsInput):
    """
    Calculate financial return (PB, NPV, NPVQ, Cashflow) — Chapter 8.
    """
    return calculate_economics(data)
