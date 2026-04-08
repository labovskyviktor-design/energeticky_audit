"""Test renovation API endpoint."""
import urllib.request
import json

data = json.dumps({
    "building_name": "Test",
    "qh": 135860,
    "ab": 4486.1,
    "phi_em_out": 100.6,
    "theta_s_des": 90,
    "theta_r_des": 70,
    "pipes": [
        {"dn": 65, "psi": 0.642, "length": 14},
        {"dn": 50, "psi": 0.524, "length": 20},
        {"dn": 40, "psi": 0.445, "length": 88},
        {"dn": 32, "psi": 0.403, "length": 54},
    ],
    "pump_p_el": 800,
    "fuel_type": "heat_exchanger_hw_hw",
    "is_external": True,
    "measures": [
        {"measure_id": "hydraulic_balancing"},
        {"measure_id": "thermostatic_valves"},
        {"measure_id": "pipe_insulation"},
        {"measure_id": "temp_gradient_reduction", "new_theta_s_des": 75, "new_theta_r_des": 65},
        {"measure_id": "new_pump", "new_pump_p_el": 179},
    ],
}).encode()

req = urllib.request.Request(
    "http://localhost:8000/api/v1/energy/renovation",
    data=data,
    headers={"Content-Type": "application/json"},
)
try:
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
        print("API Response OK!")
        print(f"Q_VYK pred:  {result['q_vyk_before']:,.0f} kWh")
        print(f"Q_VYK po:    {result['q_vyk_after']:,.0f} kWh")
        print(f"Savings:     {result['savings_kwh']:,.0f} kWh ({result['savings_pct']}%)")
        print(f"Measures:    {result['applied_measures']}")
        print("SUCCESS")
except Exception as e:
    print(f"Error: {e}")
    # Try to read the error body
    if hasattr(e, "read"):
        print(e.read().decode())
