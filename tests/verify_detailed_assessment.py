import sys
from pathlib import Path

# Add backend to sys.path
sys.path.append(str(Path(__file__).parent.parent / "backend"))

from app.core.models.building import Construction, ConstructionType, MaterialLayer
from app.core.services.thermal_assessment import (
    DetailedAssessmentRequest,
    assess_detailed_construction,
)

def test_assessment():
    layers = [
        MaterialLayer(name="Silikátová omietka", thickness=0.002, thermal_conductivity=0.8, density=1700, specific_heat_capacity=1000, diffusion_resistance=45),
        MaterialLayer(name="EPS Fasádny", thickness=0.05, thermal_conductivity=0.038, density=20, specific_heat_capacity=1270, diffusion_resistance=30),
        MaterialLayer(name="Železobetón", thickness=0.3, thermal_conductivity=1.58, density=2400, specific_heat_capacity=1020, diffusion_resistance=29),
        MaterialLayer(name="Vápenná omietka", thickness=0.01, thermal_conductivity=0.88, density=1600, specific_heat_capacity=840, diffusion_resistance=6),
    ]

    construction = Construction(
        name="Obvodová stena ST1 železobetónová",
        construction_type=ConstructionType.WALL,
        area=1.0,
        u_value=0.59,  # placeholder, will be recalculated
        layers=layers
    )

    request = DetailedAssessmentRequest(
        construction=construction,
        internal_temperature=18.0,
        external_temperature=-11.0,
        internal_humidity=50.0,
        external_humidity=83.0,
        rsi=0.13,
        rse=0.04,
        safety_margin=1.0
    )

    result = assess_detailed_construction(request)

    print(f"Construction: {result.construction_name}")
    print(f"R: {result.r_construction} (Expected 1.52)")
    print(f"R0: {result.r_total} (Expected 1.69)")
    print(f"U: {result.u_value} (Expected 0.59)")
    print(f"theta_si: {result.theta_si} (Expected 15.77)")
    print(f"theta_si_min: {result.theta_si_min} (Expected 11.74)")
    print(f"Mold Pass: {result.mold_pass}")

if __name__ == "__main__":
    test_assessment()
