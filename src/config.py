"""
Konfiguračný súbor pre Energy Audit aplikáciu
"""

import os
from pathlib import Path

# Základné nastavenia aplikácie
APP_NAME = "Energy Audit Desktop Application"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Energy Audit Team"

# Cesty k adresárom
BASE_DIR = Path(__file__).parent.parent
SRC_DIR = BASE_DIR / "src"
DATA_DIR = BASE_DIR / "data"
DOCS_DIR = BASE_DIR / "docs"
TESTS_DIR = BASE_DIR / "tests"
RESOURCES_DIR = BASE_DIR / "resources"
SCRIPTS_DIR = BASE_DIR / "scripts"

# Databázové nastavenia
DATABASE_PATH = DATA_DIR / "energy_audit.db"
BACKUP_DIR = DATA_DIR / "backups"

# Exportné nastavenia
EXPORT_DIR = DATA_DIR / "exports"
REPORT_TEMPLATES_DIR = RESOURCES_DIR / "templates"

# GUI nastavenia
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
MIN_WINDOW_WIDTH = 800
MIN_WINDOW_HEIGHT = 600

# Energetické konštanty a koeficienty
ENERGY_CONSTANTS = {
    # Tepelné kapacity materiálov [J/kg·K]
    "THERMAL_CAPACITY": {
        "concrete": 840,
        "brick": 800,
        "wood": 1600,
        "steel": 460,
        "glass": 840,
        "insulation": 1030
    },
    
    # Tepelné vodivosti materiálov [W/m·K]
    "THERMAL_CONDUCTIVITY": {
        "concrete": 1.4,
        "brick": 0.6,
        "wood": 0.12,
        "steel": 45,
        "glass": 1.0,
        "insulation_eps": 0.035,
        "insulation_mineral": 0.040,
        "insulation_pu": 0.025
    },
    
    # Hustoty materiálov [kg/m³]
    "DENSITY": {
        "concrete": 2400,
        "brick": 1800,
        "wood": 500,
        "steel": 7850,
        "glass": 2500,
        "insulation": 30
    }
}

# Energetické triedy budov
ENERGY_CLASSES = {
    "A1": {"max_consumption": 25, "color": "#00b050", "description": "Extrémne úsporná"},
    "A2": {"max_consumption": 50, "color": "#92d050", "description": "Veľmi úsporná"},
    "B": {"max_consumption": 75, "color": "#ffff00", "description": "Úsporná"},
    "C": {"max_consumption": 100, "color": "#ffc000", "description": "Mierne úsporná"},
    "D": {"max_consumption": 150, "color": "#ff8c00", "description": "Menej úsporná"},
    "E": {"max_consumption": 200, "color": "#ff0000", "description": "Nehospodárna"},
    "F": {"max_consumption": 250, "color": "#c00000", "description": "Veľmi nehospodárna"},
    "G": {"max_consumption": float('inf'), "color": "#800080", "description": "Mimoriadne nehospodárna"}
}

# Typy budov
BUILDING_TYPES = [
    "Rodinný dom",
    "Bytový dom",
    "Administratívna budova",
    "Škola",
    "Nemocnica",
    "Obchodné centrum",
    "Priemyselná budova",
    "Iné"
]

# Typy vykurovania
HEATING_TYPES = [
    "Plynový kotol",
    "Elektrické vykurovanie",
    "Tepelné čerpadlo",
    "Diaľkové vykurovanie",
    "Tuhé palivo",
    "Solárne kolektory",
    "Kombinované systémy"
]

# Logovanie
LOG_LEVEL = "INFO"
LOG_FILE = BASE_DIR / "logs" / "energy_audit.log"

# Vytvorenie potrebných adresárov
def ensure_directories():
    """Vytvorenie potrebných adresárov ak neexistujú"""
    directories = [
        DATA_DIR,
        BACKUP_DIR,
        EXPORT_DIR,
        BASE_DIR / "logs",
        RESOURCES_DIR,
        REPORT_TEMPLATES_DIR
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    ensure_directories()
    print(f"Konfigurácia aplikácie {APP_NAME} v{APP_VERSION}")
    print(f"Základný adresár: {BASE_DIR}")