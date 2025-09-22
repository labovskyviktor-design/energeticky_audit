"""
Engine pre energetické výpočty a hodnotenie budov
Obsahuje algoritmy pre výpočet tepelných strát, energetickej spotreby a klasifikácie
"""

import math
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum

try:
    from .config import ENERGY_CONSTANTS, ENERGY_CLASSES
except ImportError:
    from config import ENERGY_CONSTANTS, ENERGY_CLASSES


class SeasonType(Enum):
    """Typy sezón pre výpočty"""
    HEATING = "heating"
    COOLING = "cooling"
    TRANSITION = "transition"


@dataclass
class BuildingStructure:
    """Stavebná konštrukcia budovy"""
    name: str
    structure_type: str  # 'wall', 'roof', 'floor', 'window', 'door'
    area: float  # m²
    u_value: float  # W/m²K
    thermal_bridges: float = 0.0  # W/K


@dataclass
class HeatingSystem:
    """Vykurovací systém"""
    system_type: str
    fuel_type: str
    efficiency: float  # %
    nominal_power: Optional[float] = None  # kW


@dataclass
class VentilationSystem:
    """Ventilačný systém"""
    system_type: str  # 'natural', 'mechanical', 'heat_recovery'
    air_flow_rate: float  # m³/h
    heat_recovery_efficiency: float = 0.0  # %
    specific_fan_power: float = 0.0  # W/(m³/h)


@dataclass
class ClimateData:
    """Klimatické údaje"""
    heating_degree_days: float = 3500  # HDD - Bratislava
    cooling_degree_days: float = 200   # CDD - Bratislava
    average_external_temp_heating: float = 0.5  # °C
    average_external_temp_cooling: float = 25.0  # °C
    solar_irradiation: float = 1000  # kWh/m²/rok


class EnergyCalculator:
    """Hlavný výpočtový engine pre energetický audit"""
    
    def __init__(self):
        """Inicializácia kalkulátora"""
        self.thermal_constants = ENERGY_CONSTANTS
        self.energy_classes = ENERGY_CLASSES
        self.internal_temp_heating = 20.0  # °C
        self.internal_temp_cooling = 24.0  # °C
        self.climate_data = ClimateData()
    
    def calculate_transmission_losses(self, structures: List[BuildingStructure]) -> Dict[str, float]:
        """
        Výpočet tepelných strát prechodom cez konštrukcie
        
        Args:
            structures: Zoznam stavebných konštrukcií
            
        Returns:
            Slovník s výsledkami výpočtu
        """
        total_heat_loss = 0.0  # W/K
        structure_losses = {}
        
        for structure in structures:
            # Základný tepelný tok: Q = U × A × ΔT
            heat_loss_coefficient = structure.u_value * structure.area
            
            # Pridanie tepelných mostíkov
            heat_loss_coefficient += structure.thermal_bridges
            
            structure_losses[structure.name] = {
                'u_value': structure.u_value,
                'area': structure.area,
                'heat_loss_coefficient': heat_loss_coefficient,
                'structure_type': structure.structure_type
            }
            
            total_heat_loss += heat_loss_coefficient
        
        return {
            'total_heat_loss_coefficient': total_heat_loss,  # W/K
            'structure_losses': structure_losses,
            'annual_transmission_losses': total_heat_loss * self.climate_data.heating_degree_days * 24 / 1000  # kWh/rok
        }
    
    def calculate_ventilation_losses(self, building_volume: float, 
                                   ventilation_system: Optional[VentilationSystem] = None) -> Dict[str, float]:
        """
        Výpočet tepelných strát vetraním
        
        Args:
            building_volume: Objem budovy [m³]
            ventilation_system: Ventilačný systém
            
        Returns:
            Slovník s výsledkami výpočtu
        """
        air_density = 1.2  # kg/m³
        specific_heat_capacity = 1000  # J/kg·K
        
        if ventilation_system:
            # Mechanické vetranie
            air_flow_rate = ventilation_system.air_flow_rate  # m³/h
            
            # Tepelné straty s rekuperáciou
            heat_recovery_factor = 1 - (ventilation_system.heat_recovery_efficiency / 100)
            
            # Energia ventilátora
            fan_energy = (ventilation_system.specific_fan_power * 
                         ventilation_system.air_flow_rate / 1000)  # kW
        else:
            # Prirodzené vetranie - predpokladaná výmena vzduchu 0.5 1/h
            air_change_rate = 0.5  # 1/h
            air_flow_rate = building_volume * air_change_rate  # m³/h
            heat_recovery_factor = 1.0
            fan_energy = 0.0
        
        # Výpočet tepelných strát
        ventilation_heat_loss = (air_flow_rate * air_density * specific_heat_capacity * 
                               heat_recovery_factor) / 3600  # W/K
        
        annual_ventilation_losses = (ventilation_heat_loss * 
                                   self.climate_data.heating_degree_days * 24 / 1000)  # kWh/rok
        
        return {
            'air_flow_rate': air_flow_rate,
            'ventilation_heat_loss_coefficient': ventilation_heat_loss,
            'heat_recovery_factor': heat_recovery_factor,
            'annual_ventilation_losses': annual_ventilation_losses,
            'annual_fan_energy': fan_energy * 8760 if fan_energy > 0 else 0  # kWh/rok
        }
    
    def calculate_internal_gains(self, floor_area: float, building_type: str = "Rodinný dom") -> Dict[str, float]:
        """
        Výpočet vnútorných tepelných ziskov
        
        Args:
            floor_area: Podlahová plocha [m²]
            building_type: Typ budovy
            
        Returns:
            Slovník s tepelnými ziskami
        """
        # Špecifické zisky podľa typu budovy [W/m²]
        internal_gains_map = {
            "Rodinný dom": 4.0,
            "Bytový dom": 3.5,
            "Administratívna budova": 6.0,
            "Škola": 5.0,
            "Nemocnica": 8.0,
            "Obchodné centrum": 10.0,
            "Priemyselná budova": 12.0
        }
        
        specific_internal_gains = internal_gains_map.get(building_type, 4.0)
        
        # Celkové vnútorné zisky
        total_internal_gains = specific_internal_gains * floor_area  # W
        
        # Ročné vnútorné zisky (predpoklad prevádzky 16h/deň, 250 dní/rok)
        annual_internal_gains = total_internal_gains * 16 * 250 / 1000  # kWh/rok
        
        return {
            'specific_internal_gains': specific_internal_gains,
            'total_internal_gains': total_internal_gains,
            'annual_internal_gains': annual_internal_gains
        }
    
    def calculate_solar_gains(self, windows: List[BuildingStructure], 
                            building_orientation: str = "south") -> Dict[str, float]:
        """
        Výpočet solárnych ziskov
        
        Args:
            windows: Zoznam okien
            building_orientation: Orientácia budovy
            
        Returns:
            Slovník so solárnymi ziskami
        """
        # Orientačné faktory pre slnečné žiarenie
        orientation_factors = {
            "south": 1.0,
            "southeast": 0.9,
            "southwest": 0.9,
            "east": 0.7,
            "west": 0.7,
            "northeast": 0.5,
            "northwest": 0.5,
            "north": 0.3
        }
        
        orientation_factor = orientation_factors.get(building_orientation.lower(), 0.7)
        
        total_window_area = sum(window.area for window in windows if window.structure_type == "window")
        
        # Priepustnosť okien pre slnečné žiarenie (typicky 0.6-0.8)
        solar_transmittance = 0.7
        
        # Ročné solárne zisky
        annual_solar_gains = (total_window_area * self.climate_data.solar_irradiation * 
                            orientation_factor * solar_transmittance)  # kWh/rok
        
        return {
            'total_window_area': total_window_area,
            'orientation_factor': orientation_factor,
            'solar_transmittance': solar_transmittance,
            'annual_solar_gains': annual_solar_gains
        }
    
    def calculate_heating_demand(self, transmission_losses: Dict, ventilation_losses: Dict,
                               internal_gains: Dict, solar_gains: Dict,
                               floor_area: float) -> Dict[str, float]:
        """
        Výpočet potreby tepla na vykurovanie
        
        Args:
            transmission_losses: Straty prechodom
            ventilation_losses: Straty vetraním
            internal_gains: Vnútorné zisky
            solar_gains: Solárne zisky
            floor_area: Podlahová plocha [m²]
            
        Returns:
            Slovník s potrebou tepla
        """
        # Celkové straty
        total_losses = (transmission_losses['annual_transmission_losses'] + 
                       ventilation_losses['annual_ventilation_losses'])  # kWh/rok
        
        # Celkové zisky
        total_gains = (internal_gains['annual_internal_gains'] + 
                      solar_gains['annual_solar_gains'])  # kWh/rok
        
        # Využiteľnosť ziskov (zjednodušený model)
        gain_utilization_factor = 0.7  # typicky 0.6-0.8
        utilized_gains = total_gains * gain_utilization_factor
        
        # Potreba tepla na vykurovanie
        heating_demand = max(0, total_losses - utilized_gains)  # kWh/rok
        
        # Špecifická potreba tepla
        specific_heating_demand = heating_demand / floor_area  # kWh/m²rok
        
        return {
            'total_losses': total_losses,
            'total_gains': total_gains,
            'utilized_gains': utilized_gains,
            'gain_utilization_factor': gain_utilization_factor,
            'heating_demand': heating_demand,
            'specific_heating_demand': specific_heating_demand
        }
    
    def calculate_hot_water_demand(self, floor_area: float, building_type: str = "Rodinný dom",
                                 number_of_occupants: Optional[int] = None) -> Dict[str, float]:
        """
        Výpočet potreby tepla na prípravu teplej vody
        
        Args:
            floor_area: Podlahová plocha [m²]
            building_type: Typ budovy
            number_of_occupants: Počet obyvateľov
            
        Returns:
            Slovník s potrebou tepla na TV
        """
        if number_of_occupants:
            # Výpočet na základe počtu obyvateľov (40 l/osoba/deň)
            daily_hot_water_consumption = number_of_occupants * 40  # l/deň
        else:
            # Výpočet na základe plochy
            specific_consumption_map = {
                "Rodinný dom": 35,  # l/m²rok
                "Bytový dom": 30,
                "Administratívna budova": 10,
                "Škola": 5,
                "Nemocnica": 50,
                "Obchodné centrum": 8,
                "Priemyselná budova": 15
            }
            specific_consumption = specific_consumption_map.get(building_type, 35)
            annual_hot_water_consumption = floor_area * specific_consumption  # l/rok
            daily_hot_water_consumption = annual_hot_water_consumption / 365  # l/deň
        
        # Teplota studenej vody a teplej vody
        cold_water_temp = 10  # °C
        hot_water_temp = 45   # °C
        temperature_difference = hot_water_temp - cold_water_temp  # K
        
        # Hustota a tepelná kapacita vody
        water_density = 1.0    # kg/l
        water_heat_capacity = 4186  # J/kg·K
        
        # Ročná spotreba teplej vody
        annual_hot_water_consumption = daily_hot_water_consumption * 365  # l/rok
        
        # Potreba tepla na TV
        hot_water_demand = (annual_hot_water_consumption * water_density * 
                          water_heat_capacity * temperature_difference / 
                          (3600 * 1000))  # kWh/rok
        
        # Špecifická potreba tepla na TV
        specific_hot_water_demand = hot_water_demand / floor_area  # kWh/m²rok
        
        return {
            'annual_hot_water_consumption': annual_hot_water_consumption,
            'daily_hot_water_consumption': daily_hot_water_consumption,
            'temperature_difference': temperature_difference,
            'hot_water_demand': hot_water_demand,
            'specific_hot_water_demand': specific_hot_water_demand
        }
    
    def calculate_primary_energy(self, heating_demand: float, hot_water_demand: float,
                               heating_system: HeatingSystem) -> Dict[str, float]:
        """
        Výpočet primárnej energie a emisií CO2
        
        Args:
            heating_demand: Potreba tepla na vykurovanie [kWh/rok]
            hot_water_demand: Potreba tepla na TV [kWh/rok]
            heating_system: Vykurovací systém
            
        Returns:
            Slovník s primárnou energiou a emisiami
        """
        # Faktory primárnej energie a emisií CO2 podľa typu paliva
        primary_energy_factors = {
            "Plynový kotol": 1.1,
            "Elektrické vykurovanie": 3.0,
            "Tepelné čerpadlo": 2.5,
            "Diaľkové vykurovanie": 1.3,
            "Tuhé palivo": 1.2,
            "Solárne kolektory": 0.1,
            "Kombinované systémy": 1.5
        }
        
        co2_emission_factors = {
            "Plynový kotol": 0.202,  # kg CO2/kWh
            "Elektrické vykurovanie": 0.486,
            "Tepelné čerpadlo": 0.390,
            "Diaľkové vykurovanie": 0.280,
            "Tuhé palivo": 0.354,
            "Solárne kolektory": 0.020,
            "Kombinované systémy": 0.300
        }
        
        primary_factor = primary_energy_factors.get(heating_system.system_type, 1.2)
        co2_factor = co2_emission_factors.get(heating_system.system_type, 0.300)
        
        # Celková potreba energie
        total_energy_demand = heating_demand + hot_water_demand  # kWh/rok
        
        # Finálna energia (zohľadnenie účinnosti systému)
        system_efficiency = heating_system.efficiency / 100  # prevod z % na desatinné číslo
        final_energy = total_energy_demand / system_efficiency  # kWh/rok
        
        # Primárna energia
        primary_energy = final_energy * primary_factor  # kWh/rok
        
        # Emisie CO2
        co2_emissions = final_energy * co2_factor  # kg CO2/rok
        
        return {
            'total_energy_demand': total_energy_demand,
            'system_efficiency': system_efficiency,
            'final_energy': final_energy,
            'primary_energy_factor': primary_factor,
            'primary_energy': primary_energy,
            'co2_emission_factor': co2_factor,
            'co2_emissions': co2_emissions
        }
    
    def classify_energy_efficiency(self, specific_primary_energy: float) -> Dict[str, Any]:
        """
        Klasifikácia energetickej efektívnosti budovy
        
        Args:
            specific_primary_energy: Špecifická primárna energia [kWh/m²rok]
            
        Returns:
            Slovník s klasifikáciou
        """
        energy_class = "G"  # Predvolená najhoršia trieda
        
        for class_name, class_data in self.energy_classes.items():
            if specific_primary_energy <= class_data["max_consumption"]:
                energy_class = class_name
                break
        
        class_info = self.energy_classes[energy_class]
        
        return {
            'energy_class': energy_class,
            'specific_primary_energy': specific_primary_energy,
            'class_description': class_info['description'],
            'class_color': class_info['color'],
            'max_consumption_for_class': class_info['max_consumption']
        }
    
    def complete_building_assessment(self, building_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Kompletné hodnotenie budovy
        
        Args:
            building_data: Komplexné údaje o budove
            
        Returns:
            Kompletné hodnotenie s všetkými výpočtami
        """
        # Extrakcia údajov
        floor_area = building_data.get('heated_area', 100)
        building_height = building_data.get('building_height', 2.7)  # m
        building_volume = floor_area * building_height  # m³
        building_type = building_data.get('building_type', 'Rodinný dom')
        
        # Stavebné konštrukcie
        structures = []
        for struct_data in building_data.get('structures', []):
            structures.append(BuildingStructure(
                name=struct_data.get('name', ''),
                structure_type=struct_data.get('structure_type', 'wall'),
                area=struct_data.get('area', 0),
                u_value=struct_data.get('u_value', 1.0),
                thermal_bridges=struct_data.get('thermal_bridges', 0)
            ))
        
        # Vykurovací systém
        heating_data = building_data.get('heating_system', {})
        heating_system = HeatingSystem(
            system_type=heating_data.get('system_type', 'Plynový kotol'),
            fuel_type=heating_data.get('fuel_type', 'Zemný plyn'),
            efficiency=heating_data.get('efficiency', 85.0)
        )
        
        # Výpočty
        results = {}
        
        # 1. Tepelné straty prechodom
        results['transmission'] = self.calculate_transmission_losses(structures)
        
        # 2. Tepelné straty vetraním
        results['ventilation'] = self.calculate_ventilation_losses(building_volume)
        
        # 3. Vnútorné zisky
        results['internal_gains'] = self.calculate_internal_gains(floor_area, building_type)
        
        # 4. Solárne zisky
        windows = [s for s in structures if s.structure_type == 'window']
        results['solar_gains'] = self.calculate_solar_gains(windows)
        
        # 5. Potreba tepla na vykurovanie
        results['heating_demand'] = self.calculate_heating_demand(
            results['transmission'], results['ventilation'],
            results['internal_gains'], results['solar_gains'], floor_area
        )
        
        # 6. Potreba tepla na teplú vodu
        results['hot_water_demand'] = self.calculate_hot_water_demand(floor_area, building_type)
        
        # 7. Primárna energia a emisie
        results['primary_energy'] = self.calculate_primary_energy(
            results['heating_demand']['heating_demand'],
            results['hot_water_demand']['hot_water_demand'],
            heating_system
        )
        
        # 8. Špecifická primárna energia
        specific_primary_energy = results['primary_energy']['primary_energy'] / floor_area
        
        # 9. Energetická klasifikácia
        results['energy_classification'] = self.classify_energy_efficiency(specific_primary_energy)
        
        # Súhrn
        results['summary'] = {
            'floor_area': floor_area,
            'building_type': building_type,
            'specific_heating_demand': results['heating_demand']['specific_heating_demand'],
            'specific_hot_water_demand': results['hot_water_demand']['specific_hot_water_demand'],
            'specific_primary_energy': specific_primary_energy,
            'specific_co2_emissions': results['primary_energy']['co2_emissions'] / floor_area,
            'energy_class': results['energy_classification']['energy_class'],
            'heating_system': heating_system.system_type
        }
        
        return results


def create_sample_building_data() -> Dict[str, Any]:
    """Vytvorenie vzorových údajov pre testovanie"""
    return {
        'heated_area': 120.0,
        'building_height': 2.7,
        'building_type': 'Rodinný dom',
        'structures': [
            {
                'name': 'Obvodová stena',
                'structure_type': 'wall',
                'area': 150.0,
                'u_value': 0.8,
                'thermal_bridges': 5.0
            },
            {
                'name': 'Strecha',
                'structure_type': 'roof', 
                'area': 120.0,
                'u_value': 0.4,
                'thermal_bridges': 2.0
            },
            {
                'name': 'Podlaha',
                'structure_type': 'floor',
                'area': 120.0,
                'u_value': 0.6,
                'thermal_bridges': 0.0
            },
            {
                'name': 'Okná',
                'structure_type': 'window',
                'area': 25.0,
                'u_value': 1.4,
                'thermal_bridges': 0.0
            }
        ],
        'heating_system': {
            'system_type': 'Plynový kotol',
            'fuel_type': 'Zemný plyn',
            'efficiency': 90.0
        }
    }


# Globálna inštancia kalkulátora
energy_calculator = EnergyCalculator()


def get_energy_calculator() -> EnergyCalculator:
    """Získanie globálnej inštancie kalkulátora"""
    return energy_calculator