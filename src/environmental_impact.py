#!/usr/bin/env python3
"""
Environmental Impact Assessment Module
Implementuje hodnotenie environmentálneho dopadu energetických projektov
Obsahuje LCA (Life Cycle Assessment), uhlíková stopa, emisné faktory pre Slovensko
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from datetime import datetime
import math
import statistics

class EnergySource(Enum):
    """Zdroje energie"""
    ELECTRICITY_GRID = "electricity_grid"
    NATURAL_GAS = "natural_gas"
    HEATING_OIL = "heating_oil"
    BIOMASS = "biomass"
    DISTRICT_HEATING = "district_heating"
    SOLAR_PV = "solar_pv"
    HEAT_PUMP = "heat_pump"
    GEOTHERMAL = "geothermal"

class EmissionScope(Enum):
    """Rozsah emisií podľa GHG Protocol"""
    SCOPE_1 = "scope_1"  # Priame emisie
    SCOPE_2 = "scope_2"  # Nepriame emisie z energie
    SCOPE_3 = "scope_3"  # Ostatné nepriame emisie

@dataclass
class EmissionFactor:
    """Emisný faktor pre Slovensko"""
    energy_source: EnergySource
    co2_factor: float  # kg CO2/kWh
    ch4_factor: float  # kg CH4/kWh  
    n2o_factor: float  # kg N2O/kWh
    primary_energy_factor: float  # kWh_prim/kWh_final
    renewable_share: float = 0.0  # podiel obnoviteľných zdrojov [%]
    
    @property
    def co2_equivalent(self) -> float:
        """CO2 ekvivalent (GWP100)"""
        # GWP faktory: CH4=25, N2O=298
        return self.co2_factor + (self.ch4_factor * 25) + (self.n2o_factor * 298)

@dataclass
class MaterialImpact:
    """Environmentálny dopad materiálu"""
    material_name: str
    unit: str  # kg, m³, m², ks
    embodied_carbon: float  # kg CO2eq/unit
    embodied_energy: float  # MJ/unit
    recyclability: float  # % recyklovateľnosti
    lifespan_years: int = 50
    transport_distance: float = 100.0  # km
    
    def calculate_transport_emissions(self, quantity: float, 
                                    transport_factor: float = 0.062) -> float:
        """Výpočet emisií z dopravy (kg CO2eq/t·km = 0.062)"""
        weight_tons = quantity / 1000  # predpokladáme kg
        return quantity * weight_tons * self.transport_distance * transport_factor

@dataclass
class BuildingLCA:
    """Life Cycle Assessment budovy"""
    building_area: float  # m²
    construction_materials: List[Tuple[MaterialImpact, float]] = field(default_factory=list)
    annual_energy_consumption: Dict[EnergySource, float] = field(default_factory=dict)
    building_lifespan: int = 50  # roky
    renovation_cycles: int = 2  # počet renovácií za životnosť
    
    def add_material(self, material: MaterialImpact, quantity: float):
        """Pridanie materiálu do LCA"""
        self.construction_materials.append((material, quantity))
    
    def calculate_embodied_emissions(self) -> Dict[str, float]:
        """Výpočet zabudovaných emisií (A1-A3)"""
        total_embodied = 0
        material_breakdown = {}
        transport_emissions = 0
        
        for material, quantity in self.construction_materials:
            material_emissions = material.embodied_carbon * quantity
            total_embodied += material_emissions
            transport_emissions += material.calculate_transport_emissions(quantity)
            
            material_breakdown[material.material_name] = {
                'quantity': quantity,
                'unit': material.unit,
                'emissions_kg_co2eq': material_emissions,
                'emissions_per_m2': material_emissions / self.building_area
            }
        
        return {
            'total_embodied_emissions': total_embodied,
            'embodied_per_m2': total_embodied / self.building_area,
            'transport_emissions': transport_emissions,
            'material_breakdown': material_breakdown
        }
    
    def calculate_operational_emissions(self, years: int = None) -> Dict[str, float]:
        """Výpočet prevádzkových emisií (B6)"""
        years = years or self.building_lifespan
        emission_factors = get_slovak_emission_factors()
        
        annual_emissions = 0
        energy_breakdown = {}
        
        for energy_source, consumption in self.annual_energy_consumption.items():
            if energy_source in emission_factors:
                factor = emission_factors[energy_source]
                source_emissions = consumption * factor.co2_equivalent
                annual_emissions += source_emissions
                
                energy_breakdown[energy_source.value] = {
                    'consumption_kwh': consumption,
                    'emission_factor': factor.co2_equivalent,
                    'annual_emissions': source_emissions
                }
        
        total_operational = annual_emissions * years
        
        return {
            'annual_operational_emissions': annual_emissions,
            'total_operational_emissions': total_operational,
            'operational_per_m2_annual': annual_emissions / self.building_area,
            'energy_breakdown': energy_breakdown
        }
    
    def calculate_end_of_life_emissions(self) -> Dict[str, float]:
        """Výpočet emisií na konci životnosti (C1-C4)"""
        total_eol = 0
        recycling_credit = 0
        
        for material, quantity in self.construction_materials:
            # Zjednodušený odhad - 5% z embodied carbon pre demoláciu
            demolition_emissions = material.embodied_carbon * quantity * 0.05
            total_eol += demolition_emissions
            
            # Kredit za recykláciu
            recyclable_portion = quantity * (material.recyclability / 100)
            recycling_credit += recyclable_portion * material.embodied_carbon * 0.1
        
        net_eol = total_eol - recycling_credit
        
        return {
            'demolition_emissions': total_eol,
            'recycling_credit': recycling_credit,
            'net_end_of_life_emissions': net_eol,
            'eol_per_m2': net_eol / self.building_area
        }

class EnvironmentalImpactAssessor:
    """Hlavná trieda pre hodnotenie environmentálneho dopadu"""
    
    def __init__(self):
        """Inicializácia assessora"""
        self.emission_factors = get_slovak_emission_factors()
        self.material_database = self._load_material_database()
    
    def assess_renovation_project(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Komplexné hodnotenie environmentálneho dopadu renovačného projektu
        
        Args:
            project_data: Údaje o projekte
            
        Returns:
            Environmentálne hodnotenie
        """
        # Základné údaje
        building_area = project_data.get('building_area', 100)
        current_consumption = project_data.get('current_energy_consumption', {})
        projected_consumption = project_data.get('projected_energy_consumption', {})
        renovation_materials = project_data.get('renovation_materials', [])
        
        # Výpočet úspor emisií z prevádzky
        operational_impact = self._calculate_operational_impact_reduction(
            current_consumption, projected_consumption, building_area
        )
        
        # Výpočet zabudovaných emisií z renovácie
        embodied_impact = self._calculate_renovation_embodied_impact(
            renovation_materials, building_area
        )
        
        # Doba návratnosti z environmentálneho hľadiska
        environmental_payback = self._calculate_environmental_payback(
            embodied_impact['total_embodied_emissions'],
            operational_impact['annual_savings_kg_co2eq']
        )
        
        # Hodnotenie za celú životnosť
        lifecycle_assessment = self._perform_renovation_lca(
            embodied_impact, operational_impact, project_data.get('project_lifespan', 30)
        )
        
        # Porovnanie s benchmarks
        benchmark_comparison = self._compare_with_benchmarks(
            operational_impact, building_area, project_data.get('building_type', 'residential')
        )
        
        return {
            'assessment_metadata': {
                'assessment_date': datetime.now().isoformat(),
                'building_area': building_area,
                'methodology': 'STN EN 15978:2011 + Slovak emission factors'
            },
            'operational_impact': operational_impact,
            'embodied_impact': embodied_impact,
            'environmental_payback_years': environmental_payback,
            'lifecycle_assessment': lifecycle_assessment,
            'benchmark_comparison': benchmark_comparison,
            'sustainability_indicators': self._calculate_sustainability_indicators(
                operational_impact, embodied_impact, building_area
            ),
            'recommendations': self._generate_environmental_recommendations(
                operational_impact, embodied_impact, environmental_payback
            )
        }
    
    def _calculate_operational_impact_reduction(self, current: Dict, projected: Dict, 
                                             building_area: float) -> Dict[str, Any]:
        """Výpočet redukcie prevádzkových emisií"""
        current_annual_emissions = 0
        projected_annual_emissions = 0
        
        energy_breakdown = {}
        
        # Spracovanie aktuálnej spotreby
        for energy_type, consumption in current.items():
            if hasattr(EnergySource, energy_type.upper()):
                source = EnergySource[energy_type.upper()]
                if source in self.emission_factors:
                    factor = self.emission_factors[source]
                    emissions = consumption * factor.co2_equivalent
                    current_annual_emissions += emissions
        
        # Spracovanie projektovanej spotreby
        for energy_type, consumption in projected.items():
            if hasattr(EnergySource, energy_type.upper()):
                source = EnergySource[energy_type.upper()]
                if source in self.emission_factors:
                    factor = self.emission_factors[source]
                    emissions = consumption * factor.co2_equivalent
                    projected_annual_emissions += emissions
                    
                    energy_breakdown[energy_type] = {
                        'current_consumption': current.get(energy_type, 0),
                        'projected_consumption': consumption,
                        'savings_kwh': current.get(energy_type, 0) - consumption,
                        'emission_factor': factor.co2_equivalent,
                        'current_emissions': current.get(energy_type, 0) * factor.co2_equivalent,
                        'projected_emissions': emissions,
                        'emissions_savings': (current.get(energy_type, 0) - consumption) * factor.co2_equivalent
                    }
        
        annual_savings = current_annual_emissions - projected_annual_emissions
        
        return {
            'current_annual_emissions_kg_co2eq': current_annual_emissions,
            'projected_annual_emissions_kg_co2eq': projected_annual_emissions,
            'annual_savings_kg_co2eq': annual_savings,
            'annual_savings_per_m2': annual_savings / building_area,
            'reduction_percentage': (annual_savings / current_annual_emissions * 100) if current_annual_emissions > 0 else 0,
            'energy_breakdown': energy_breakdown
        }
    
    def _calculate_renovation_embodied_impact(self, materials: List[Dict], 
                                           building_area: float) -> Dict[str, Any]:
        """Výpočet zabudovaných emisií z renovácie"""
        total_embodied = 0
        material_impacts = []
        
        for material_data in materials:
            material_name = material_data.get('name', 'Unknown')
            quantity = material_data.get('quantity', 0)
            
            # Hľadanie materiálu v databáze
            if material_name in self.material_database:
                material = self.material_database[material_name]
                impact = material.embodied_carbon * quantity
                total_embodied += impact
                
                material_impacts.append({
                    'name': material_name,
                    'quantity': quantity,
                    'unit': material.unit,
                    'embodied_carbon_factor': material.embodied_carbon,
                    'total_impact': impact,
                    'impact_per_m2': impact / building_area
                })
        
        return {
            'total_embodied_emissions': total_embodied,
            'embodied_per_m2': total_embodied / building_area,
            'material_impacts': material_impacts,
            'material_count': len(material_impacts)
        }
    
    def _calculate_environmental_payback(self, embodied_emissions: float, 
                                       annual_savings: float) -> float:
        """Výpočet environmentálnej doby návratnosti"""
        if annual_savings <= 0:
            return float('inf')
        return embodied_emissions / annual_savings
    
    def _perform_renovation_lca(self, embodied: Dict, operational: Dict, 
                              lifespan: int) -> Dict[str, Any]:
        """LCA renovačného projektu"""
        
        # Celkové emisie za životnosť
        total_embodied = embodied['total_embodied_emissions']
        total_operational_savings = operational['annual_savings_kg_co2eq'] * lifespan
        net_lifecycle_impact = total_embodied - total_operational_savings
        
        # Rozloženie emisií po rokoch
        annual_breakdown = []
        cumulative_impact = total_embodied  # Začíname s embodied emissions
        
        for year in range(1, lifespan + 1):
            yearly_savings = -operational['annual_savings_kg_co2eq']  # Záporné = úspora
            cumulative_impact += yearly_savings
            
            annual_breakdown.append({
                'year': year,
                'annual_impact': yearly_savings,
                'cumulative_impact': cumulative_impact
            })
        
        return {
            'project_lifespan_years': lifespan,
            'total_embodied_emissions': total_embodied,
            'total_operational_savings': total_operational_savings,
            'net_lifecycle_impact': net_lifecycle_impact,
            'annual_breakdown': annual_breakdown,
            'carbon_payback_year': min([item['year'] for item in annual_breakdown 
                                      if item['cumulative_impact'] <= 0], default=lifespan),
            'impact_intensity': net_lifecycle_impact / (operational['annual_savings_kg_co2eq'] or 1)
        }
    
    def _compare_with_benchmarks(self, operational: Dict, building_area: float,
                               building_type: str) -> Dict[str, Any]:
        """Porovnanie s benchmarks"""
        
        # Slovenské benchmarks pre emisie (kg CO2eq/m²rok)
        benchmarks = {
            'residential': {
                'excellent': 15,
                'good': 25,
                'average': 45,
                'poor': 65
            },
            'office': {
                'excellent': 20,
                'good': 35,
                'average': 55,
                'poor': 80
            },
            'school': {
                'excellent': 18,
                'good': 30,
                'average': 50,
                'poor': 75
            }
        }
        
        current_intensity = operational['current_annual_emissions_kg_co2eq'] / building_area
        projected_intensity = operational['projected_annual_emissions_kg_co2eq'] / building_area
        
        building_benchmarks = benchmarks.get(building_type, benchmarks['residential'])
        
        # Klasifikácia
        def classify_performance(intensity):
            if intensity <= building_benchmarks['excellent']:
                return 'Vynikajúca'
            elif intensity <= building_benchmarks['good']:
                return 'Dobrá' 
            elif intensity <= building_benchmarks['average']:
                return 'Priemerná'
            elif intensity <= building_benchmarks['poor']:
                return 'Podpriemerná'
            else:
                return 'Nevyhovujúca'
        
        return {
            'building_type': building_type,
            'benchmarks': building_benchmarks,
            'current_performance': {
                'intensity_kg_co2_m2': current_intensity,
                'classification': classify_performance(current_intensity)
            },
            'projected_performance': {
                'intensity_kg_co2_m2': projected_intensity,
                'classification': classify_performance(projected_intensity)
            },
            'improvement_achieved': current_intensity - projected_intensity,
            'percentile_improvement': ((current_intensity - projected_intensity) / current_intensity * 100) if current_intensity > 0 else 0
        }
    
    def _calculate_sustainability_indicators(self, operational: Dict, embodied: Dict,
                                           building_area: float) -> Dict[str, Any]:
        """Výpočet ukazovateľov udržateľnosti"""
        
        # Ekvivalenty pre lepšie pochopenie
        annual_savings = operational['annual_savings_kg_co2eq']
        
        return {
            'annual_co2_savings': {
                'kg_co2eq': annual_savings,
                'equivalent_trees_planted': annual_savings / 21.77,  # 1 strom = ~21.77 kg CO2/rok
                'equivalent_cars_removed': annual_savings / 4600,    # auto = ~4.6t CO2/rok
                'equivalent_km_driving_saved': annual_savings / 0.12  # auto = ~0.12 kg CO2/km
            },
            'embodied_carbon_intensity': {
                'kg_co2eq_per_m2': embodied['embodied_per_m2'],
                'benchmark_comparison': 'Nízka' if embodied['embodied_per_m2'] < 100 else 
                                      'Priemerná' if embodied['embodied_per_m2'] < 200 else 'Vysoká'
            },
            'carbon_efficiency': {
                'operational_to_embodied_ratio': operational['annual_savings_kg_co2eq'] / embodied['total_embodied_emissions'] if embodied['total_embodied_emissions'] > 0 else 0,
                'efficiency_rating': self._rate_carbon_efficiency(operational['annual_savings_kg_co2eq'], embodied['total_embodied_emissions'])
            }
        }
    
    def _rate_carbon_efficiency(self, annual_savings: float, embodied_emissions: float) -> str:
        """Hodnotenie uhlíkovej efektívnosti"""
        if embodied_emissions == 0:
            return 'Nedefinované'
        
        ratio = annual_savings / embodied_emissions
        
        if ratio >= 0.5:
            return 'Vynikajúca'
        elif ratio >= 0.3:
            return 'Veľmi dobrá'
        elif ratio >= 0.2:
            return 'Dobrá'
        elif ratio >= 0.1:
            return 'Priemerná'
        else:
            return 'Nízka'
    
    def _generate_environmental_recommendations(self, operational: Dict, embodied: Dict,
                                             payback_years: float) -> List[str]:
        """Generovanie environmentálnych odporúčaní"""
        recommendations = []
        
        # Na základe doby návratnosti
        if payback_years < 5:
            recommendations.append("Výborná environmentálna návratnosť - projekt sa odporúča")
        elif payback_years < 10:
            recommendations.append("Dobrá environmentálna návratnosť")
        elif payback_years < 20:
            recommendations.append("Akceptovateľná environmentálna návratnosť")
        else:
            recommendations.append("Dlhá environmentálna návratnosť - zvážiť alternatívy")
        
        # Na základe embodied emissions
        if embodied['embodied_per_m2'] > 200:
            recommendations.append("Vysoké zabudované emisie - zvážiť materiály s nižším uhlíkovým obsahom")
        
        # Na základe úspor
        if operational['annual_savings_kg_co2eq'] < operational['current_annual_emissions_kg_co2eq'] * 0.3:
            recommendations.append("Nízke úspory emisií - zvážiť dodatočné opatrenia")
        
        # Všeobecné odporúčania
        recommendations.extend([
            "Prioritizovať materiály s nízkou uhlíkovou stopou",
            "Zvážiť možnosti recyklácie stavebných materiálov",
            "Monitorovať skutočnú spotrebu energie po renovácii"
        ])
        
        return recommendations
    
    def _load_material_database(self) -> Dict[str, MaterialImpact]:
        """Načítanie databázy materiálov s ich environmentálnym dopadom"""
        return {
            'EPS_insulation': MaterialImpact(
                'EPS izolácia', 'kg', 3.29, 85.3, 0, 50, 100
            ),
            'mineral_wool': MaterialImpact(
                'Minerálna vlna', 'kg', 1.35, 28.0, 75, 50, 100
            ),
            'concrete': MaterialImpact(
                'Betón C25/30', 'm³', 315, 1800, 5, 100, 50
            ),
            'steel': MaterialImpact(
                'Oceľ', 'kg', 2.75, 35.0, 90, 50, 150
            ),
            'aluminum': MaterialImpact(
                'Hliník', 'kg', 8.24, 155, 95, 50, 200
            ),
            'timber': MaterialImpact(
                'Drevo conc.', 'm³', -420, 2500, 80, 50, 100  # Záporná hodnota - sekvestrácia CO2
            ),
            'brick': MaterialImpact(
                'Tehla pálená', 'kg', 0.24, 3.0, 90, 100, 50
            ),
            'glass': MaterialImpact(
                'Sklo', 'kg', 0.85, 15.0, 100, 30, 100
            )
        }

def get_slovak_emission_factors() -> Dict[EnergySource, EmissionFactor]:
    """Emisné faktory pre Slovensko (2023)"""
    return {
        EnergySource.ELECTRICITY_GRID: EmissionFactor(
            EnergySource.ELECTRICITY_GRID, 0.209, 0.0001, 0.000003, 2.3, 23.5
        ),
        EnergySource.NATURAL_GAS: EmissionFactor(
            EnergySource.NATURAL_GAS, 0.202, 0.0002, 0.000001, 1.1, 0.0
        ),
        EnergySource.HEATING_OIL: EmissionFactor(
            EnergySource.HEATING_OIL, 0.279, 0.0001, 0.000001, 1.1, 0.0
        ),
        EnergySource.BIOMASS: EmissionFactor(
            EnergySource.BIOMASS, 0.018, 0.001, 0.000004, 1.2, 100.0
        ),
        EnergySource.DISTRICT_HEATING: EmissionFactor(
            EnergySource.DISTRICT_HEATING, 0.180, 0.0002, 0.000002, 1.3, 15.0
        ),
        EnergySource.SOLAR_PV: EmissionFactor(
            EnergySource.SOLAR_PV, 0.045, 0.0, 0.0, 1.0, 100.0
        ),
        EnergySource.HEAT_PUMP: EmissionFactor(
            EnergySource.HEAT_PUMP, 0.070, 0.00003, 0.000001, 2.0, 23.5  # Závisí od COP a grid mix
        )
    }

def get_environmental_impact_assessor():
    """Factory funkcia pre získanie environmentálneho assessora"""
    return EnvironmentalImpactAssessor()

if __name__ == "__main__":
    # Test základnej funkcionality
    assessor = EnvironmentalImpactAssessor()
    
    # Testovací projekt
    project_data = {
        'building_area': 150,
        'current_energy_consumption': {
            'natural_gas': 15000,  # kWh/rok
            'electricity_grid': 4000
        },
        'projected_energy_consumption': {
            'natural_gas': 8000,   # kWh/rok po renovácii
            'electricity_grid': 3500
        },
        'renovation_materials': [
            {'name': 'EPS_insulation', 'quantity': 500},  # kg
            {'name': 'mineral_wool', 'quantity': 200}
        ],
        'project_lifespan': 30
    }
    
    result = assessor.assess_renovation_project(project_data)
    print(f"Ročné úspory CO2: {result['operational_impact']['annual_savings_kg_co2eq']:.0f} kg")
    print(f"Environmentálna návratnosť: {result['environmental_payback_years']:.1f} rokov")
    print(f"Klasifikácia po renovácii: {result['benchmark_comparison']['projected_performance']['classification']}")