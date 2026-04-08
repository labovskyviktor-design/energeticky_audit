
import requests
import json

def test_dhw_api_polish():
    url = "http://localhost:8000/api/v1/energy/dhw-demand"
    
    # Payload similar to before but emphasizing that DN is now expected and should work
    payload = {
        "ab": 150.0,
        "pipes": [
            # Testing that DN is accepted
            {"name": "Supply", "length": 10, "dn": 25, "psi": 0.3, "ambient_temp": 15, "water_temp": 60, "is_circulation": False},
            {"name": "Circulation", "length": 10, "dn": 20, "psi": 0.3, "ambient_temp": 15, "water_temp": 55, "is_circulation": True}
        ],
        "storage": {
            "volume": 200,
            "standby_loss": 1.5,
            "store_temp": 60,
            "ambient_temp": 20,
            "has_storage": True
        },
        "pump": {
            "power": 30,
            "daily_hours": 24,
            "has_circulation": True
        },
        "generation": {
            "fuel_type": "natural_gas_condensing",
            "is_external": False
        }
    }
    
    print("Sending polished payload...")
    try:
        resp = requests.post(url, json=payload)
        resp.raise_for_status()
        data = resp.json()
        
        print("\n--- DHW Polished Results ---")
        print(json.dumps(data, indent=2))
        
        print("\n--- Validation ---")
        print(f"Q_W: {data['q_w']} (Expected: 20*150 = 3000)")
        if data['q_w'] == 3000:
            print("BASIC CHECK PASSED")
        else:
             print("BASIC CHECK FAILED")
        
    except Exception as e:
        print(f"Error: {e}")
        if 'resp' in locals():
            print(resp.text)

if __name__ == "__main__":
    test_dhw_api_polish()
