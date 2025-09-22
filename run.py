#!/usr/bin/env python3
"""
Spúštací skript pre Energy Audit Desktop Application
"""

import sys
import os
from pathlib import Path

# Pridanie src adresára do Python cesty
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

try:
    # Import hlavného modulu
    from main import main
    
    # Spustenie aplikácie
    if __name__ == "__main__":
        print("Spúšťam Energy Audit Desktop Application...")
        main()
        
except ImportError as e:
    print(f"Chyba pri importovaní: {e}")
    print("Uistite sa, že sú nainštalované všetky potrebné závislosti.")
    print("Spustite: pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"Neočakávaná chyba: {e}")
    sys.exit(1)