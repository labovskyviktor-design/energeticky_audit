
import requests
import json
import sys

API_URL = "http://localhost:8000/api/v1/energy/certificate"

def verify_certification():
    print("--- Verifying Chapter 9: Energy Certification ---")
    
    payload = {
        "heating_demand": 10000.0,
        "heating_carrier": "natural_gas",
        "dhw_demand": 4000.0,
        "dhw_carrier": "natural_gas",
        "lighting_demand": 500.0,
        "cooling_demand": 0.0,
        "ventilation_demand": 0.0,
        "pv_production": 0.0,
        "floor_area": 150.0,
        "building_category": "family_house",
        "factors": [
            {"carrier": "natural_gas", "f_prim": 1.1, "f_co2": 0.220},
            {"carrier": "electricity", "f_prim": 2.2, "f_co2": 0.167}
        ]
    }
    
    print("Payload:", json.dumps(payload, indent=2))
    
    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code != 200:
            print(f"FAILED: Status {response.status_code}")
            print(response.text)
            sys.exit(1)
            
        result = response.json()
        print("Result:", json.dumps(result, indent=2))
        
        # Validation
        # Primary Heat+DHW = 14000 * 1.1 = 15400
        # Primary Light = 500 * 2.2 = 1100
        # Total Primary = 16500
        # Specific = 16500 / 150 = 110.0
        
        calc_primary = result['total_primary']
        calc_specific = result['specific_primary']
        calc_class = result['energy_class']
        
        expected_primary = 16500.0
        expected_specific = 110.0
        
        # Check tolerance
        if abs(calc_primary - expected_primary) > 1.0:
            print(f"ERROR: Total Primary mismatch. Got {calc_primary}, expected {expected_primary}")
            sys.exit(1)
            
        if abs(calc_specific - expected_specific) > 0.1:
            print(f"ERROR: Specific Primary mismatch. Got {calc_specific}, expected {expected_specific}")
            sys.exit(1)
            
        # Class 110.0 -> A1 (55-108) or B (109-216)?
        # 110 > 108 => B
        if calc_class != "B":
             print(f"ERROR: Energy Class mismatch. Got {calc_class}, expected B (for specific 110.0)")
             # Wait, my logic: val <= 108 is A1. 110 is > 108. So B.
             sys.exit(1)
             
        print("SUCCESS: Calculation verified.")
        
    except Exception as e:
        print(f"Exception: {e}")
        sys.exit(1)

if __name__ == "__main__":
    verify_certification()
