"""
Psychrometric utilities for thermal-technical assessments.
"""

import math


def calculate_saturation_pressure(temperature: float) -> float:
    """
    Calculate saturation vapor pressure Psat [Pa] for a given temperature [°C].

    Uses the Magnus-Tetens formula:
    Psat = 611.2 * exp((17.62 * T) / (243.12 + T))   (for T >= 0)
    Psat = 611.2 * exp((22.46 * T) / (272.62 + T))   (for T < 0, over ice)
    """
    if temperature >= 0:
        return 611.2 * math.exp((17.62 * temperature) / (243.12 + temperature))
    else:
        return 611.2 * math.exp((22.46 * temperature) / (272.62 + temperature))


def calculate_vapor_pressure(temperature: float, relative_humidity: float) -> float:
    """
    Calculate actual vapor pressure Pi [Pa].

    Pi = (phi / 100) * Psat(T)
    """
    psat = calculate_saturation_pressure(temperature)
    return (relative_humidity / 100.0) * psat


def calculate_critical_surface_temperature(
    internal_temperature: float, internal_humidity: float
) -> float:
    """
    Calculate the minimum internal surface temperature theta_si,min [°C]
    to avoid 80% surface relative humidity (mold risk).

    phi_si = Pi / Psat(theta_si) = 0.8
    Psat(theta_si) = Pi / 0.8
    """
    pi = calculate_vapor_pressure(internal_temperature, internal_humidity)
    target_psat = pi / 0.8

    # Solve for T in Magnus formula: Psat = 611.2 * exp((17.62 * T) / (243.12 + T))
    # ln(Psat/611.2) = 17.62 * T / (243.12 + T)
    # let K = ln(Psat/611.2)
    # K * (243.12 + T) = 17.62 * T
    # 243.12K + K*T = 17.62 * T
    # 243.12K = (17.62 - K) * T
    # T = 243.12K / (17.62 - K)

    k = math.log(target_psat / 611.2)
    return (243.12 * k) / (17.62 - k)
