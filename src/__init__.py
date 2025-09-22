"""
Energy Audit Desktop Application

Desktopová aplikácia na vykonávanie energetického auditu a certifikáciu budov.
"""

__version__ = "1.0.0"
__author__ = "Energy Audit Team"
__email__ = "team@energyaudit.local"

from .main import EnergyAuditApp, main
from .config import *

__all__ = [
    "EnergyAuditApp",
    "main",
    "APP_NAME",
    "APP_VERSION",
    "ENERGY_CONSTANTS",
    "ENERGY_CLASSES",
    "BUILDING_TYPES",
    "HEATING_TYPES"
]