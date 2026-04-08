
import requests
import json

def test_dhw_api():
    url = "http://localhost:8000/api/v1/energy/dhw-demand"
    
    # Payload mimicking PDF Example 4.2
    # Ab = 4403.4
    # Pipes: 
    #  - Supply 1.NP: DN40, L=7, Psi=0.469, Amb=10, Wat=57.5
    #  - Supply 1.NP: DN32, L=6, Psi=0.432, Amb=10, Wat=57.5
    #  - Supply Shaft: DN25, L=56, Psi=1.058, Amb=15, Wat=57.5
    #  - Supply Shaft: DN20, L=76, Psi=0.845, Amb=15, Wat=57.5
    #  - Circ 1.NP: DN20, L=13, Psi=0.330, Amb=10, Wat=57.5
    #  - Circ Shaft: DN15, L=132, Psi=0.672, Amb=15, Wat=57.5
    
    payload = {
        "ab": 4403.4,
        "pipes": [
            {"name": "Supply 1.NP DN40", "length": 7, "dn": 40, "psi": 0.469, "ambient_temp": 10, "water_temp": 57.5, "is_circulation": False},
            {"name": "Supply 1.NP DN32", "length": 6, "dn": 32, "psi": 0.432, "ambient_temp": 10, "water_temp": 57.5, "is_circulation": False},
            {"name": "Supply Shaft DN25", "length": 56, "dn": 25, "psi": 1.058, "ambient_temp": 15, "water_temp": 57.5, "is_circulation": False},
            {"name": "Supply Shaft DN20", "length": 76, "dn": 20, "psi": 0.845, "ambient_temp": 15, "water_temp": 57.5, "is_circulation": False},
            {"name": "Circ 1.NP DN20", "length": 13, "dn": 20, "psi": 0.330, "ambient_temp": 10, "water_temp": 57.5, "is_circulation": True},
            {"name": "Circ Shaft DN15", "length": 132, "dn": 15, "psi": 0.672, "ambient_temp": 15, "water_temp": 57.5, "is_circulation": True}
        ],
        "storage": {
            "has_storage": False # External in PDF
        },
        "pump": {
            "has_circulation": False # External pump in PDF (pp 73)
        },
        "generation": {
            "is_external": True # External in PDF
        }
    }
    
    print("Sending payload...")
    try:
        resp = requests.post(url, json=payload)
        resp.raise_for_status()
        data = resp.json()
        
        print("\n--- DHW Results ---")
        print(json.dumps(data, indent=2))
        
        # Validation against PDF (pp 74)
        print("\n--- Validation ---")
        print(f"Q_W (Net): {data['q_w']} (Expected: 88068)")
        # PDF Q_d is 86798 (pipes) + 3577 (stagnation) = no, wait.
        # PDF says "Tepelná strata z distribúcie TV QW,d = 83 221 + 3 577 = 86 798"
        # My calc only does pipes for now. Stagnation is 0 unless I implement it.
        # Let's check pipe loss.
        # Expected Pipe Loss = 83 221 kWh
        print(f"Q_W,d,ls (Pipes): {data['q_w_dis_ls']} (Expected approx 83221)")
        
    except Exception as e:
        print(f"Error: {e}")
        if 'resp' in locals():
            print(resp.text)

if __name__ == "__main__":
    test_dhw_api()
