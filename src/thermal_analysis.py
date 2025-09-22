"""
Pokročilé tepelno-technické výpočty a analýzy
Implementuje detailné výpočty tepelných mostíkov, kondenzácie, letnej stability atď.
"""

import math
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import logging

try:
    from .config import ENERGY_CONSTANTS
except ImportError:
    from config import ENERGY_CONSTANTS


class ConstructionType(Enum):
    """Typy stavebných konštrukcií"""
    EXTERNAL_WALL = "external_wall"
    INTERNAL_WALL = "internal_wall"
    ROOF = "roof"
    FLOOR = "floor"
    CEILING = "ceiling"
    WINDOW = "window"
    DOOR = "door"
    FOUNDATION = "foundation"


class ThermalBridgeType(Enum):
    """Typy tepelných mostíkov"""
    CORNER = "corner"  # Roh
    JUNCTION = "junction"  # Spoj
    PENETRATION = "penetration"  # Prestup
    SUPPORT = "support"  # Podpera
    FRAME = "frame"  # Rám


@dataclass
class MaterialLayer:
    """Vrstva materiálu v konštrukcii"""
    name: str
    thickness: float  # hrúbka [m]
    thermal_conductivity: float  # tepelná vodivosť [W/mK]
    density: float  # hustota [kg/m³]
    specific_heat: float  # tepelná kapacita [J/kgK]
    vapor_resistance: float = 1.0  # odpor proti difúzii vodných pár [-]
    
    @property
    def thermal_resistance(self) -> float:
        """Tepelný odpor vrstvy [m²K/W]"""
        return self.thickness / self.thermal_conductivity
    
    @property
    def thermal_capacity(self) -> float:
        """Tepelná kapacita vrstvy [J/m²K]"""
        return self.density * self.specific_heat * self.thickness


@dataclass
class ThermalBridge:
    """Tepelný mostík"""
    bridge_type: ThermalBridgeType
    length: float  # dĺžka [m]
    psi_value: float  # lineárny tepelný mostík [W/mK]
    description: str = ""
    
    @property
    def heat_loss(self) -> float:
        """Tepelná strata mostíkom [W/K]"""
        return self.length * self.psi_value


@dataclass
class Construction:
    """Stavebná konštrukcia"""
    name: str
    construction_type: ConstructionType
    layers: List[MaterialLayer]
    area: float  # plocha [m²]
    thermal_bridges: List[ThermalBridge] = field(default_factory=list)
    
    @property
    def total_thickness(self) -> float:
        """Celková hrúbka konštrukcie [m]"""
        return sum(layer.thickness for layer in self.layers)
    
    @property
    def thermal_resistance(self) -> float:
        """Tepelný odpor konštrukcie [m²K/W]"""
        # R = Rsi + ΣRlayer + Rse
        rsi = 0.13  # vnútorný prestup tepla [m²K/W]
        rse = 0.04  # vonkajší prestup tepla [m²K/W]
        
        if self.construction_type == ConstructionType.ROOF:
            rse = 0.04  # zvýšený odpor pre strechu
        elif self.construction_type == ConstructionType.FLOOR:
            rse = 0.0   # podlaha na teréne
            
        r_layers = sum(layer.thermal_resistance for layer in self.layers)
        return rsi + r_layers + rse
    
    @property
    def u_value(self) -> float:
        """Súčiniteľ prestupu tepla [W/m²K]"""
        return 1.0 / self.thermal_resistance
    
    @property
    def thermal_capacity(self) -> float:
        """Tepelná kapacita konštrukcie [J/m²K]"""
        return sum(layer.thermal_capacity for layer in self.layers)
    
    @property
    def thermal_bridge_losses(self) -> float:
        """Straty tepelnými mostíkmi [W/K]"""
        return sum(bridge.heat_loss for bridge in self.thermal_bridges)


class ThermalAnalyzer:
    """Pokročilý tepelno-technický analyzátor"""
    
    def __init__(self):
        """Inicializácia analyzátora"""
        self.thermal_constants = ENERGY_CONSTANTS
        
        # Klimatické údaje pre Slovensko
        self.climate_data = {
            'exterior_temp_heating': -12.0,  # návrhová vonkajšia teplota [°C]
            'interior_temp_heating': 20.0,   # vnútorná teplota [°C]
            'exterior_temp_summer': 32.0,    # letná vonkajšia teplota [°C]
            'interior_temp_summer': 26.0,    # letná vnútorná teplota [°C]
            'relative_humidity_ext': 85.0,   # vonkajšia vlhkosť [%]
            'relative_humidity_int': 50.0,   # vnútorná vlhkosť [%]
        }
    
    def calculate_heat_transfer_coefficient(self, construction: Construction) -> Dict[str, float]:
        """
        Výpočet súčiniteľa prestupu tepla s tepelnými mostíkmi
        
        Args:
            construction: Stavebná konštrukcia
            
        Returns:
            Slovník s výsledkami
        """
        # Základný U-faktor
        u_basic = construction.u_value
        
        # Tepelné mostíky
        psi_total = sum(bridge.psi_value * bridge.length for bridge in construction.thermal_bridges)
        
        # Upravený U-faktor s tepelnými mostíkmi
        u_corrected = u_basic + (psi_total / construction.area)
        
        return {
            'u_basic': u_basic,
            'u_corrected': u_corrected,
            'thermal_bridge_effect': u_corrected - u_basic,
            'thermal_bridge_increase_percent': ((u_corrected - u_basic) / u_basic) * 100
        }
    
    def analyze_condensation_risk(self, construction: Construction) -> Dict[str, Any]:
        """
        Analýza rizika kondenzácie v konštrukcii (Glaser metóda)
        
        Args:
            construction: Stavebná konštrukcia
            
        Returns:
            Analýza kondenzácie
        """
        # Základné parametre
        t_ext = self.climate_data['exterior_temp_heating']
        t_int = self.climate_data['interior_temp_heating']
        rh_ext = self.climate_data['relative_humidity_ext'] / 100
        rh_int = self.climate_data['relative_humidity_int'] / 100
        
        # Saturačné tlaky vodnej pary
        def saturation_pressure(temp):
            """Saturačný tlak vodnej pary [Pa]"""
            return 611.2 * math.exp(17.62 * temp / (243.12 + temp))
        
        p_sat_int = saturation_pressure(t_int)
        p_sat_ext = saturation_pressure(t_ext)
        
        # Parciálne tlaky
        p_int = rh_int * p_sat_int
        p_ext = rh_ext * p_sat_ext
        
        # Analýza vrstiev
        results = {
            'condensation_risk': False,
            'critical_layers': [],
            'temperature_profile': [],
            'vapor_pressure_profile': [],
            'saturation_pressure_profile': []
        }
        
        # Teplotný profil
        total_resistance = construction.thermal_resistance
        temp_drop = t_int - t_ext
        
        current_temp = t_int
        current_resistance = 0.13  # Rsi
        
        for i, layer in enumerate(construction.layers):
            # Teplota na začiatku vrstvy
            results['temperature_profile'].append({
                'layer': layer.name,
                'position': 'start',
                'temperature': current_temp
            })
            
            # Pokles teploty v vrstve
            temp_drop_layer = temp_drop * (layer.thermal_resistance / total_resistance)
            current_temp -= temp_drop_layer
            current_resistance += layer.thermal_resistance
            
            # Teplota na konci vrstvy
            results['temperature_profile'].append({
                'layer': layer.name,
                'position': 'end',
                'temperature': current_temp
            })
            
            # Kontrola kondenzácie
            temp_mid = current_temp + temp_drop_layer / 2
            p_sat_mid = saturation_pressure(temp_mid)
            
            # Parciálny tlak v polovici vrstvy (zjednodušene)
            vapor_resistance_ratio = sum(l.vapor_resistance * l.thickness for l in construction.layers[:i+1]) / sum(l.vapor_resistance * l.thickness for l in construction.layers)
            p_mid = p_int - vapor_resistance_ratio * (p_int - p_ext)
            
            if p_mid > p_sat_mid:
                results['condensation_risk'] = True
                results['critical_layers'].append({
                    'layer': layer.name,
                    'temperature': temp_mid,
                    'partial_pressure': p_mid,
                    'saturation_pressure': p_sat_mid,
                    'excess_pressure': p_mid - p_sat_mid
                })
        
        return results
    
    def calculate_thermal_inertia(self, construction: Construction) -> Dict[str, float]:
        """
        Výpočet tepelnej zotrvačnosti konštrukcie
        
        Args:
            construction: Stavebná konštrukcia
            
        Returns:
            Parametre tepelnej zotrvačnosti
        """
        # Tepelná kapacita
        thermal_capacity = construction.thermal_capacity
        
        # Tepelná difuzivita
        total_density = sum(layer.density * layer.thickness for layer in construction.layers) / construction.total_thickness
        total_conductivity = 1.0 / sum(layer.thickness / layer.thermal_conductivity for layer in construction.layers) * construction.total_thickness
        total_specific_heat = sum(layer.specific_heat * layer.density * layer.thickness for layer in construction.layers) / sum(layer.density * layer.thickness for layer in construction.layers)
        
        thermal_diffusivity = total_conductivity / (total_density * total_specific_heat)
        
        # Časová konštanta
        time_constant = (construction.total_thickness ** 2) / (math.pi ** 2 * thermal_diffusivity)
        
        # Teplotná amplitúda
        amplitude_ratio = 1.0 / math.sqrt(1 + (2 * math.pi / (24 * 3600 / time_constant)) ** 2)
        
        # Fázové posunutie
        phase_shift = math.atan(2 * math.pi / (24 * 3600 / time_constant)) * 24 * 3600 / (2 * math.pi)
        
        return {
            'thermal_capacity': thermal_capacity,
            'thermal_diffusivity': thermal_diffusivity,
            'time_constant_hours': time_constant / 3600,
            'amplitude_ratio': amplitude_ratio,
            'phase_shift_hours': phase_shift / 3600,
            'thermal_inertia_class': self._classify_thermal_inertia(time_constant / 3600)
        }
    
    def _classify_thermal_inertia(self, time_constant_hours: float) -> str:
        """Klasifikácia tepelnej zotrvačnosti"""
        if time_constant_hours < 6:
            return "Ľahká (rýchla reakcia)"
        elif time_constant_hours < 24:
            return "Stredná (mierny pokles teploty)"
        elif time_constant_hours < 72:
            return "Ťažká (pomalá reakcia)"
        else:
            return "Veľmi ťažká (veľká stabilita)"
    
    def analyze_summer_comfort(self, construction: Construction, solar_gains: float = 0.0) -> Dict[str, Any]:
        """
        Analýza letného komfortu a prehrievania
        
        Args:
            construction: Stavebná konštrukcia
            solar_gains: Solárne zisky [W/m²]
            
        Returns:
            Analýza letného komfortu
        """
        t_ext_max = self.climate_data['exterior_temp_summer']
        t_int_desired = self.climate_data['interior_temp_summer']
        
        # Tepelná zotrvačnosť
        inertia = self.calculate_thermal_inertia(construction)
        
        # Maximálny nárast teploty
        temp_swing_ext = 10  # denný teplotný rozptyl vonku [K]
        temp_swing_int = temp_swing_ext * inertia['amplitude_ratio']
        
        # Prenos tepla cez konštrukciu
        heat_flux_basic = construction.u_value * (t_ext_max - t_int_desired)
        heat_flux_solar = solar_gains * 0.04  # absorpcia solárneho žiarenia na vonkajšom povrchu
        
        total_heat_flux = heat_flux_basic + heat_flux_solar
        
        # Výsledná vnútorná teplota
        t_int_max = t_int_desired + temp_swing_int + (total_heat_flux / 10)  # zjednodušený výpočet
        
        # Hodnotenie komfortu
        comfort_category = "Vyhovujúca"
        if t_int_max > 28:
            comfort_category = "Mierny diskomfort"
        if t_int_max > 30:
            comfort_category = "Výrazný diskomfort"
        if t_int_max > 32:
            comfort_category = "Nevyhovujúca"
        
        return {
            'max_interior_temp': t_int_max,
            'temperature_swing': temp_swing_int,
            'heat_flux_conduction': heat_flux_basic,
            'heat_flux_solar': heat_flux_solar,
            'total_heat_flux': total_heat_flux,
            'comfort_category': comfort_category,
            'overheating_hours_estimate': max(0, (t_int_max - 26) * 8),  # odhad hodín prehriatia za deň
            'cooling_need_estimate': max(0, total_heat_flux) * construction.area  # potreba chladenia [W]
        }
    
    def calculate_effective_u_value(self, constructions: List[Construction], 
                                   construction_ratios: List[float]) -> float:
        """
        Výpočet efektívneho U-faktora pre kombinované konštrukcie
        
        Args:
            constructions: Zoznam konštrukcií
            construction_ratios: Podiel jednotlivých konštrukcií [0-1]
            
        Returns:
            Efektívny U-faktor
        """
        if len(constructions) != len(construction_ratios):
            raise ValueError("Počet konštrukcií musí zodpovedať počtu pomerov")
        
        if abs(sum(construction_ratios) - 1.0) > 0.01:
            raise ValueError("Súčet pomerov musí byť 1.0")
        
        # Vážený priemer U-faktorov
        effective_u = sum(
            const.u_value * ratio 
            for const, ratio in zip(constructions, construction_ratios)
        )
        
        return effective_u
    
    def analyze_thermal_comfort_parameters(self, constructions: List[Construction], 
                                         room_volume: float) -> Dict[str, Any]:
        """
        Analýza parametrov tepelnej pohody
        
        Args:
            constructions: Stavebné konštrukcie miestnosti
            room_volume: Objem miestnosti [m³]
            
        Returns:
            Parametre tepelnej pohody
        """
        t_int = 20.0  # vnútorná teplota [°C]
        
        # Radiačná teplota povrchov
        surface_temps = []
        total_area = 0
        
        for construction in constructions:
            # Teplota vnútorného povrchu
            if construction.construction_type in [ConstructionType.EXTERNAL_WALL, ConstructionType.ROOF]:
                t_ext = -12.0
                temp_drop = (t_int - t_ext) * (0.13 / construction.thermal_resistance)
                surface_temp = t_int - temp_drop
            else:
                surface_temp = t_int  # vnútorné konštrukcie
            
            surface_temps.append(surface_temp)
            total_area += construction.area
        
        # Priemerná radiačná teplota
        mean_radiant_temp = sum(
            temp * const.area for temp, const in zip(surface_temps, constructions)
        ) / total_area
        
        # Operatívna teplota
        operative_temp = (t_int + mean_radiant_temp) / 2
        
        # Asymetria radiácie
        min_surface_temp = min(surface_temps)
        max_surface_temp = max(surface_temps)
        radiant_asymmetry = max_surface_temp - min_surface_temp
        
        # Vertikálny teplotný gradient (zjednodušene)
        air_change_rate = 0.5  # h⁻¹
        vertical_gradient = max(0, (operative_temp - 18) * 0.1)  # odhad
        
        # Hodnotenie komfortu
        comfort_issues = []
        if mean_radiant_temp < 16:
            comfort_issues.append("Príliš chladné povrchy")
        if radiant_asymmetry > 10:
            comfort_issues.append("Vysoká asymetria radiácie")
        if vertical_gradient > 3:
            comfort_issues.append("Vysoký vertikálny teplotný gradient")
        
        comfort_rating = "Vyhovujúca" if not comfort_issues else "Problematická"
        
        return {
            'mean_radiant_temperature': mean_radiant_temp,
            'operative_temperature': operative_temp,
            'radiant_asymmetry': radiant_asymmetry,
            'vertical_temperature_gradient': vertical_gradient,
            'surface_temperatures': [
                {'construction': const.name, 'temperature': temp}
                for const, temp in zip(constructions, surface_temps)
            ],
            'comfort_rating': comfort_rating,
            'comfort_issues': comfort_issues
        }


# Predefinované materiály
COMMON_MATERIALS = {
    # Murivá
    'brick_solid': MaterialLayer("Plná tehla", 0.25, 0.8, 1800, 850, 8),
    'brick_hollow': MaterialLayer("Dutá tehla", 0.25, 0.45, 1200, 850, 8),
    'concrete_block': MaterialLayer("Betónový blok", 0.25, 1.0, 1600, 850, 12),
    'aac_block': MaterialLayer("Pórobetónový blok", 0.25, 0.15, 500, 850, 5),
    
    # Izolácie
    'eps': MaterialLayer("EPS polystyrén", 0.1, 0.035, 15, 1270, 40),
    'xps': MaterialLayer("XPS polystyrén", 0.1, 0.032, 35, 1270, 100),
    'mineral_wool': MaterialLayer("Minerálna vlna", 0.1, 0.040, 100, 850, 1),
    'pu_foam': MaterialLayer("PUR pena", 0.1, 0.025, 40, 1400, 50),
    
    # Omietky a povrchy
    'cement_plaster': MaterialLayer("Cementová omietka", 0.02, 0.8, 1900, 850, 15),
    'lime_plaster': MaterialLayer("Vápenná omietka", 0.02, 0.7, 1600, 850, 8),
    'gypsum_plaster': MaterialLayer("Sadrová omietka", 0.015, 0.4, 1200, 850, 4),
    
    # Konštrukcie
    'concrete': MaterialLayer("Betón", 0.2, 1.6, 2400, 850, 80),
    'reinforced_concrete': MaterialLayer("Železobetón", 0.2, 2.3, 2500, 850, 80),
    'wood_beam': MaterialLayer("Drevený trám", 0.1, 0.15, 500, 1600, 50),
    
    # Membrány a fólie
    'vapor_barrier': MaterialLayer("Parozábrana", 0.0002, 0.25, 1300, 1400, 100000),
    'windproof_membrane': MaterialLayer("Vetrotesná membrána", 0.0005, 0.25, 400, 1400, 2),
}


def create_standard_wall(wall_type: str = "insulated_brick") -> Construction:
    """
    Vytvorenie štandardnej stenovej konštrukcie
    
    Args:
        wall_type: Typ steny
        
    Returns:
        Stavebná konštrukcia
    """
    if wall_type == "insulated_brick":
        layers = [
            COMMON_MATERIALS['cement_plaster'],
            COMMON_MATERIALS['brick_hollow'],
            COMMON_MATERIALS['eps'].replace(thickness=0.15),
            COMMON_MATERIALS['cement_plaster']
        ]
    elif wall_type == "cavity_wall":
        layers = [
            COMMON_MATERIALS['lime_plaster'],
            COMMON_MATERIALS['brick_solid'].replace(thickness=0.15),
            COMMON_MATERIALS['mineral_wool'].replace(thickness=0.12),
            COMMON_MATERIALS['brick_hollow'].replace(thickness=0.12),
            COMMON_MATERIALS['cement_plaster']
        ]
    elif wall_type == "aac_wall":
        layers = [
            COMMON_MATERIALS['lime_plaster'],
            COMMON_MATERIALS['aac_block'].replace(thickness=0.30),
            COMMON_MATERIALS['eps'].replace(thickness=0.12),
            COMMON_MATERIALS['cement_plaster']
        ]
    else:
        raise ValueError(f"Neznámy typ steny: {wall_type}")
    
    return Construction(
        name=f"Obvodová stena - {wall_type}",
        construction_type=ConstructionType.EXTERNAL_WALL,
        layers=layers,
        area=100.0  # štandardná plocha
    )


# Globálna inštancia analyzátora
thermal_analyzer = ThermalAnalyzer()


def get_thermal_analyzer() -> ThermalAnalyzer:
    """Získanie globálnej inštancie tepelno-technického analyzátora"""
    return thermal_analyzer