"""
Pokročilé reporty a analýzy pre energetický audit
Implementuje detailné správy s grafmi, porovnaniami a odporúčaniami na optimalizáciu
"""

import json
import math
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
import statistics

try:
    from .config import ENERGY_CLASSES, BUILDING_TYPES, HEATING_TYPES
    from .thermal_analysis import Construction, ThermalAnalyzer, get_thermal_analyzer
    from .building_diagnostics import BuildingDiagnostics, get_building_diagnostics
    from .construction_assessment import ConstructionAssessor, get_construction_assessor
    from .energy_calculations import EnergyCalculator, get_energy_calculator
    from .database import get_db_manager
except ImportError:
    from config import ENERGY_CLASSES, BUILDING_TYPES, HEATING_TYPES
    from thermal_analysis import Construction, ThermalAnalyzer, get_thermal_analyzer
    from building_diagnostics import BuildingDiagnostics, get_building_diagnostics
    from construction_assessment import ConstructionAssessor, get_construction_assessor
    from energy_calculations import EnergyCalculator, get_energy_calculator
    from database import get_db_manager


class ReportType(Enum):
    """Typy správ"""
    BASIC_AUDIT = "basic_audit"
    DETAILED_ANALYSIS = "detailed_analysis"
    COMPARISON_STUDY = "comparison_study"
    OPTIMIZATION_REPORT = "optimization_report"
    COMPLIANCE_CHECK = "compliance_check"
    INVESTMENT_ANALYSIS = "investment_analysis"


class ReportFormat(Enum):
    """Formáty správ"""
    JSON = "json"
    HTML = "html"
    PDF = "pdf"
    EXCEL = "excel"


class Priority(Enum):
    """Priorita odporúčaní"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class ImprovementRecommendation:
    """Odporúčanie na zlepšenie"""
    title: str
    description: str
    category: str  # "insulation", "windows", "heating", "ventilation", "other"
    priority: Priority
    estimated_cost: Optional[float] = None  # €
    estimated_savings_annual: Optional[float] = None  # €/rok
    estimated_energy_savings: Optional[float] = None  # kWh/rok
    payback_period: Optional[float] = None  # roky
    implementation_complexity: str = "medium"  # "low", "medium", "high"
    environmental_impact: Optional[float] = None  # kg CO2/rok
    
    def calculate_payback_period(self):
        """Výpočet doby návratnosti"""
        if self.estimated_cost and self.estimated_savings_annual and self.estimated_savings_annual > 0:
            self.payback_period = self.estimated_cost / self.estimated_savings_annual


@dataclass
class EnergyBalance:
    """Energetická bilancia budovy"""
    heating_demand: float  # kWh/rok
    hot_water_demand: float  # kWh/rok
    electricity_demand: float  # kWh/rok
    cooling_demand: float = 0.0  # kWh/rok
    renewable_generation: float = 0.0  # kWh/rok
    
    @property
    def total_demand(self) -> float:
        """Celková energetická potreba"""
        return self.heating_demand + self.hot_water_demand + self.electricity_demand + self.cooling_demand
    
    @property
    def net_demand(self) -> float:
        """Netto energetická potreba po odpočítaní obnoviteľných zdrojov"""
        return max(0, self.total_demand - self.renewable_generation)
    
    @property
    def self_sufficiency_ratio(self) -> float:
        """Podiel energetickej sebestačnosti [%]"""
        if self.total_demand == 0:
            return 100.0
        return min(100.0, (self.renewable_generation / self.total_demand) * 100)


@dataclass
class BenchmarkData:
    """Porovnacie údaje (benchmark)"""
    building_type: str
    typical_heating_demand: float  # kWh/m²rok
    typical_hot_water_demand: float  # kWh/m²rok
    typical_primary_energy: float  # kWh/m²rok
    typical_co2_emissions: float  # kg/m²rok
    best_practice_heating: float  # kWh/m²rok
    best_practice_primary_energy: float  # kWh/m²rok
    passive_house_standard: float  # kWh/m²rok


class AdvancedReportGenerator:
    """Generátor pokročilých správ"""
    
    def __init__(self):
        """Inicializácia generátora správ"""
        self.db_manager = get_db_manager()
        self.energy_calculator = get_energy_calculator()
        self.thermal_analyzer = get_thermal_analyzer()
        self.diagnostics = get_building_diagnostics()
        self.construction_assessor = get_construction_assessor()
        
        # Načítanie porovnacích údajov
        self.benchmarks = self._load_benchmarks()
    
    def _load_benchmarks(self) -> Dict[str, BenchmarkData]:
        """Načítanie porovnacích údajov pre rôzne typy budov"""
        return {
            "Rodinný dom": BenchmarkData(
                "Rodinný dom", 80.0, 15.0, 150.0, 35.0, 40.0, 80.0, 15.0
            ),
            "Bytový dom": BenchmarkData(
                "Bytový dom", 70.0, 12.0, 130.0, 30.0, 35.0, 70.0, 15.0
            ),
            "Administratívna budova": BenchmarkData(
                "Administratívna budova", 60.0, 5.0, 120.0, 28.0, 30.0, 60.0, 15.0
            ),
            "Škola": BenchmarkData(
                "Škola", 65.0, 8.0, 125.0, 30.0, 32.0, 65.0, 15.0
            )
        }
    
    def generate_comprehensive_report(self, audit_id: int) -> Dict[str, Any]:
        """
        Generovanie komplexnej správy pre audit
        
        Args:
            audit_id: ID auditu
            
        Returns:
            Komplexná správa
        """
        # Načítanie údajov auditu
        audit_data = self.db_manager.get_audit(audit_id)
        if not audit_data:
            raise ValueError(f"Audit s ID {audit_id} neexistuje")
        
        # Základné energetické výpočty
        building_data = self._prepare_building_data_for_calculation(audit_id, audit_data)
        energy_results = self.energy_calculator.complete_building_assessment(building_data)
        
        # Porovnanie s benchmarkom
        benchmark_analysis = self._analyze_benchmark_performance(audit_data, energy_results)
        
        # Analýza konštrukcií
        construction_analysis = self._analyze_constructions(audit_id)
        
        # Odporúčania na zlepšenie
        improvement_recommendations = self._generate_improvement_recommendations(
            audit_data, energy_results, construction_analysis
        )
        
        # Finančná analýza
        financial_analysis = self._perform_financial_analysis(improvement_recommendations)
        
        # Environmentálny dopad
        environmental_impact = self._calculate_environmental_impact(energy_results, improvement_recommendations)
        
        # Súhrn priority
        priority_matrix = self._create_priority_matrix(improvement_recommendations)
        
        report = {
            "report_metadata": {
                "report_id": f"ADV-{audit_id}-{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "generated_date": datetime.now().isoformat(),
                "report_type": ReportType.DETAILED_ANALYSIS.value,
                "audit_id": audit_id,
                "audit_name": audit_data.get('audit_name', 'Bez názvu')
            },
            "executive_summary": self._create_executive_summary(
                audit_data, energy_results, improvement_recommendations, financial_analysis
            ),
            "building_information": {
                "basic_data": audit_data,
                "energy_performance": energy_results['summary'],
                "energy_classification": energy_results['energy_classification']
            },
            "benchmark_analysis": benchmark_analysis,
            "detailed_analysis": {
                "thermal_performance": energy_results['transmission'],
                "ventilation_performance": energy_results['ventilation'],
                "energy_gains": {
                    "internal": energy_results['internal_gains'],
                    "solar": energy_results['solar_gains']
                },
                "primary_energy": energy_results['primary_energy']
            },
            "construction_analysis": construction_analysis,
            "improvement_recommendations": [
                self._recommendation_to_dict(rec) for rec in improvement_recommendations
            ],
            "financial_analysis": financial_analysis,
            "environmental_impact": environmental_impact,
            "priority_matrix": priority_matrix,
            "action_plan": self._create_action_plan(improvement_recommendations),
            "compliance_status": self._check_compliance_status(energy_results)
        }
        
        return report
    
    def _prepare_building_data_for_calculation(self, audit_id: int, audit_data: Dict[str, Any]) -> Dict[str, Any]:
        """Príprava údajov budovy pre výpočet"""
        building_data = {
            'heated_area': audit_data.get('heated_area', 100),
            'building_type': audit_data.get('building_type', 'Rodinný dom'),
            'structures': [],
            'heating_system': {}
        }
        
        # Načítanie stavebných konštrukcií z databázy
        structures = self.db_manager.get_building_structures(audit_id)
        for struct in structures:
            building_data['structures'].append({
                'name': struct.get('name', ''),
                'structure_type': struct.get('structure_type', 'wall'),
                'area': struct.get('area', 0),
                'u_value': struct.get('u_value', 1.0),
                'thermal_bridges': struct.get('thermal_bridges', 0)
            })
        
        # Ak nie sú definované konštrukcie, použijú sa predvolené hodnoty
        if not building_data['structures']:
            building_data['structures'] = [
                {'name': 'Obvodová stena', 'structure_type': 'wall', 'area': 100, 'u_value': 0.8, 'thermal_bridges': 0},
                {'name': 'Strecha', 'structure_type': 'roof', 'area': audit_data.get('heated_area', 100), 'u_value': 0.6, 'thermal_bridges': 0},
                {'name': 'Podlaha', 'structure_type': 'floor', 'area': audit_data.get('heated_area', 100), 'u_value': 0.7, 'thermal_bridges': 0},
                {'name': 'Okná', 'structure_type': 'window', 'area': 20, 'u_value': 1.8, 'thermal_bridges': 0}
            ]
        
        # Vykurovací systém (predvolené hodnoty ak nie sú definované)
        building_data['heating_system'] = {
            'system_type': 'Plynový kotol',
            'fuel_type': 'Zemný plyn',
            'efficiency': 85.0
        }
        
        return building_data
    
    def _analyze_benchmark_performance(self, audit_data: Dict[str, Any], 
                                     energy_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analýza výkonnosti oproti benchmark údajom"""
        building_type = audit_data.get('building_type', 'Rodinný dom')
        benchmark = self.benchmarks.get(building_type)
        
        if not benchmark:
            return {"error": f"Benchmark pre typ budovy '{building_type}' nie je dostupný"}
        
        summary = energy_results['summary']
        
        # Porovnanie s typickými hodnotami
        heating_comparison = (summary['specific_heating_demand'] / benchmark.typical_heating_demand) * 100
        hotwater_comparison = (summary['specific_hot_water_demand'] / benchmark.typical_hot_water_demand) * 100
        primary_energy_comparison = (summary['specific_primary_energy'] / benchmark.typical_primary_energy) * 100
        
        # Porovnanie s najlepšími praktikami
        heating_vs_best = (summary['specific_heating_demand'] / benchmark.best_practice_heating) * 100
        primary_vs_best = (summary['specific_primary_energy'] / benchmark.best_practice_primary_energy) * 100
        
        # Hodnotenie výkonnosti
        def get_performance_rating(ratio):
            if ratio <= 70:
                return "Vynikajúca"
            elif ratio <= 85:
                return "Veľmi dobrá"
            elif ratio <= 100:
                return "Dobrá"
            elif ratio <= 120:
                return "Priemerná"
            else:
                return "Podpriemerná"
        
        return {
            "building_type": building_type,
            "benchmark_data": {
                "typical_heating": benchmark.typical_heating_demand,
                "typical_primary_energy": benchmark.typical_primary_energy,
                "best_practice_heating": benchmark.best_practice_heating,
                "passive_house_standard": benchmark.passive_house_standard
            },
            "performance_comparison": {
                "heating_vs_typical": {
                    "ratio_percent": heating_comparison,
                    "rating": get_performance_rating(heating_comparison),
                    "difference": summary['specific_heating_demand'] - benchmark.typical_heating_demand
                },
                "primary_energy_vs_typical": {
                    "ratio_percent": primary_energy_comparison,
                    "rating": get_performance_rating(primary_energy_comparison),
                    "difference": summary['specific_primary_energy'] - benchmark.typical_primary_energy
                },
                "heating_vs_best_practice": {
                    "ratio_percent": heating_vs_best,
                    "rating": get_performance_rating(heating_vs_best),
                    "improvement_potential": max(0, summary['specific_heating_demand'] - benchmark.best_practice_heating)
                }
            },
            "percentile_ranking": self._calculate_percentile_ranking(summary, benchmark)
        }
    
    def _calculate_percentile_ranking(self, summary: Dict[str, Any], 
                                    benchmark: BenchmarkData) -> Dict[str, int]:
        """Výpočet percentilového umiestnenia"""
        # Zjednodušené percentily na základe benchmark údajov
        heating_percentile = max(0, min(100, 100 - (summary['specific_heating_demand'] / benchmark.typical_heating_demand - 0.5) * 100))
        primary_percentile = max(0, min(100, 100 - (summary['specific_primary_energy'] / benchmark.typical_primary_energy - 0.5) * 100))
        
        return {
            "heating_demand": int(heating_percentile),
            "primary_energy": int(primary_percentile),
            "overall": int((heating_percentile + primary_percentile) / 2)
        }
    
    def _analyze_constructions(self, audit_id: int) -> Dict[str, Any]:
        """Analýza stavebných konštrukcií"""
        try:
            # Získanie konštrukcií z databázy
            structures = self.db_manager.get_building_structures(audit_id)
            
            if not structures:
                return {"warning": "Žiadne stavebné konštrukcie nie sú definované"}
            
            construction_assessments = []
            
            for struct_data in structures:
                # Pre jednoduchosť vytvoríme základnú analýzu U-hodnôt
                u_value = struct_data.get('u_value', 1.0)
                area = struct_data.get('area', 0)
                structure_type = struct_data.get('structure_type', 'wall')
                
                # Hodnotenie U-hodnoty podľa typu konštrukcie
                if structure_type == 'wall':
                    if u_value <= 0.20:
                        rating = "Vynikajúca"
                    elif u_value <= 0.32:
                        rating = "Dobrá"
                    elif u_value <= 0.46:
                        rating = "Vyhovujúca"
                    else:
                        rating = "Nevyhovujúca"
                elif structure_type == 'roof':
                    if u_value <= 0.15:
                        rating = "Vynikajúca"
                    elif u_value <= 0.20:
                        rating = "Dobrá"
                    elif u_value <= 0.32:
                        rating = "Vyhovujúca"
                    else:
                        rating = "Nevyhovujúca"
                else:  # okná, podlahy, atď.
                    rating = "Vyžaduje detailnú analýzu"
                
                construction_assessments.append({
                    'name': struct_data.get('name', 'Bez názvu'),
                    'type': structure_type,
                    'area': area,
                    'u_value': u_value,
                    'rating': rating,
                    'heat_loss_coefficient': u_value * area
                })
            
            # Celková analýza
            total_heat_loss = sum(assessment['heat_loss_coefficient'] for assessment in construction_assessments)
            avg_u_value = sum(assessment['u_value'] * assessment['area'] for assessment in construction_assessments) / sum(assessment['area'] for assessment in construction_assessments) if construction_assessments else 0
            
            return {
                "individual_assessments": construction_assessments,
                "overall_analysis": {
                    "total_heat_loss_coefficient": total_heat_loss,
                    "area_weighted_avg_u_value": avg_u_value,
                    "construction_count": len(construction_assessments)
                }
            }
            
        except Exception as e:
            return {"error": f"Chyba pri analýze konštrukcií: {str(e)}"}
    
    def _generate_improvement_recommendations(self, audit_data: Dict[str, Any],
                                           energy_results: Dict[str, Any],
                                           construction_analysis: Dict[str, Any]) -> List[ImprovementRecommendation]:
        """Generovanie odporúčaní na zlepšenie"""
        recommendations = []
        
        summary = energy_results['summary']
        energy_class = summary['energy_class']
        
        # Odporúčania na základe energetickej triedy
        if energy_class in ['F', 'G']:
            recommendations.append(ImprovementRecommendation(
                title="Komplexná energetická renovácia",
                description="Budova má veľmi nízku energetickú efektívnosť. Odporúča sa komplexná renovácia zahŕňajúca zateplenie, výmenu okien a modernizáciu vykurovania.",
                category="comprehensive",
                priority=Priority.CRITICAL,
                estimated_cost=25000.0,
                estimated_savings_annual=2000.0,
                estimated_energy_savings=8000.0,
                implementation_complexity="high",
                environmental_impact=2400.0
            ))
        elif energy_class in ['D', 'E']:
            recommendations.append(ImprovementRecommendation(
                title="Zlepšenie tepelnej izolácie",
                description="Zateplenie obálky budovy s prioritou na obvodové steny a strechu.",
                category="insulation",
                priority=Priority.HIGH,
                estimated_cost=15000.0,
                estimated_savings_annual=1200.0,
                estimated_energy_savings=5000.0,
                implementation_complexity="medium",
                environmental_impact=1500.0
            ))
        
        # Odporúčania na základe analýzy konštrukcií
        if construction_analysis.get('individual_assessments'):
            for assessment in construction_analysis['individual_assessments']:
                if assessment['rating'] == 'Nevyhovujúca' and assessment['u_value'] > 1.0:
                    recommendations.append(ImprovementRecommendation(
                        title=f"Zlepšenie konštrukcie: {assessment['name']}",
                        description=f"Konštrukcia {assessment['name']} má vysokú U-hodnotu {assessment['u_value']:.3f} W/m²K. Odporúča sa zlepšenie tepelnoizolačných vlastností.",
                        category="insulation",
                        priority=Priority.MEDIUM,
                        estimated_cost=assessment['area'] * 50.0,  # €50/m²
                        estimated_savings_annual=assessment['heat_loss_coefficient'] * 20 * 0.08,  # odhad
                        implementation_complexity="medium"
                    ))
        
        # Odporúčania pre vykurovací systém
        if summary['specific_heating_demand'] > 80:
            recommendations.append(ImprovementRecommendation(
                title="Modernizácia vykurovacieho systému",
                description="Inštalácia moderného vykurovacieho systému s vyššou účinnosťou (kondenzačný kotol, tepelné čerpadlo).",
                category="heating",
                priority=Priority.MEDIUM,
                estimated_cost=8000.0,
                estimated_savings_annual=600.0,
                estimated_energy_savings=2500.0,
                implementation_complexity="medium",
                environmental_impact=750.0
            ))
        
        # Odporúčania pre okná
        if any(assess.get('type') == 'window' and assess.get('u_value', 0) > 1.4 
               for assess in construction_analysis.get('individual_assessments', [])):
            recommendations.append(ImprovementRecommendation(
                title="Výmena okien",
                description="Výmena starých okien za moderné s nízkym U-faktorom (U ≤ 1.0 W/m²K).",
                category="windows",
                priority=Priority.MEDIUM,
                estimated_cost=5000.0,
                estimated_savings_annual=400.0,
                estimated_energy_savings=1800.0,
                implementation_complexity="low",
                environmental_impact=540.0
            ))
        
        # Výpočet doby návratnosti pre všetky odporúčania
        for rec in recommendations:
            rec.calculate_payback_period()
        
        # Zoradenie podľa priority a doby návratnosti
        recommendations.sort(key=lambda r: (r.priority.value, r.payback_period or float('inf')), reverse=True)
        
        return recommendations
    
    def _perform_financial_analysis(self, recommendations: List[ImprovementRecommendation]) -> Dict[str, Any]:
        """Finančná analýza odporúčaní"""
        total_investment = sum(rec.estimated_cost or 0 for rec in recommendations)
        total_annual_savings = sum(rec.estimated_savings_annual or 0 for rec in recommendations)
        total_energy_savings = sum(rec.estimated_energy_savings or 0 for rec in recommendations)
        
        # Celková doba návratnosti
        overall_payback = total_investment / total_annual_savings if total_annual_savings > 0 else float('inf')
        
        # NPV výpočet (zjednodušený)
        discount_rate = 0.05  # 5%
        period_years = 20
        npv = -total_investment + sum(total_annual_savings / ((1 + discount_rate) ** year) for year in range(1, period_years + 1))
        
        # IRR aproximácia
        irr_approx = (total_annual_savings / total_investment) if total_investment > 0 else 0
        
        return {
            "total_investment_cost": total_investment,
            "total_annual_savings": total_annual_savings,
            "total_energy_savings": total_energy_savings,
            "overall_payback_period": overall_payback,
            "net_present_value": npv,
            "internal_rate_return_approx": irr_approx * 100,  # %
            "cost_effectiveness_ranking": self._rank_recommendations_by_cost_effectiveness(recommendations)
        }
    
    def _rank_recommendations_by_cost_effectiveness(self, recommendations: List[ImprovementRecommendation]) -> List[Dict[str, Any]]:
        """Zoradenie odporúčaní podľa nákladovej efektívnosti"""
        ranked = []
        
        for i, rec in enumerate(recommendations):
            if rec.estimated_cost and rec.estimated_energy_savings:
                cost_per_kwh_saved = rec.estimated_cost / rec.estimated_energy_savings
                ranked.append({
                    "title": rec.title,
                    "cost_per_kwh_saved": cost_per_kwh_saved,
                    "payback_period": rec.payback_period,
                    "priority": rec.priority.value,
                    "rank": i + 1
                })
        
        # Zoradenie podľa cost per kWh saved
        ranked.sort(key=lambda x: x['cost_per_kwh_saved'])
        
        # Aktualizácia rankov
        for i, item in enumerate(ranked):
            item['cost_effectiveness_rank'] = i + 1
        
        return ranked
    
    def _calculate_environmental_impact(self, energy_results: Dict[str, Any],
                                      recommendations: List[ImprovementRecommendation]) -> Dict[str, Any]:
        """Výpočet environmentálneho dopadu"""
        current_co2 = energy_results['summary']['specific_co2_emissions']
        floor_area = energy_results['summary']['floor_area']
        
        total_co2_reduction = sum(rec.environmental_impact or 0 for rec in recommendations)
        
        # Percentuálne zníženie emisií
        co2_reduction_percent = (total_co2_reduction / (current_co2 * floor_area)) * 100 if current_co2 > 0 else 0
        
        return {
            "current_annual_co2_emissions": current_co2 * floor_area,
            "potential_co2_reduction": total_co2_reduction,
            "co2_reduction_percent": co2_reduction_percent,
            "equivalent_trees_planted": total_co2_reduction / 21.77,  # 1 strom = ~21.77 kg CO2/rok
            "equivalent_cars_removed": total_co2_reduction / 4600,  # priemerné auto = ~4.6t CO2/rok
            "carbon_footprint_rating": self._get_carbon_footprint_rating(current_co2)
        }
    
    def _get_carbon_footprint_rating(self, co2_per_m2: float) -> str:
        """Hodnotenie uhlíkovej stopy"""
        if co2_per_m2 <= 15:
            return "Výborná"
        elif co2_per_m2 <= 25:
            return "Dobrá"
        elif co2_per_m2 <= 35:
            return "Priemerná"
        elif co2_per_m2 <= 50:
            return "Podpriemerná"
        else:
            return "Vysoká"
    
    def _create_priority_matrix(self, recommendations: List[ImprovementRecommendation]) -> Dict[str, Any]:
        """Vytvorenie priority matrice"""
        matrix = {
            "high_impact_low_cost": [],
            "high_impact_high_cost": [],
            "low_impact_low_cost": [],
            "low_impact_high_cost": []
        }
        
        # Medián nákladov a úspor pre rozdelenie na high/low
        costs = [rec.estimated_cost for rec in recommendations if rec.estimated_cost]
        savings = [rec.estimated_energy_savings for rec in recommendations if rec.estimated_energy_savings]
        
        median_cost = statistics.median(costs) if costs else 10000
        median_savings = statistics.median(savings) if savings else 2000
        
        for rec in recommendations:
            cost = rec.estimated_cost or 0
            savings = rec.estimated_energy_savings or 0
            
            if savings >= median_savings and cost <= median_cost:
                category = "high_impact_low_cost"
            elif savings >= median_savings and cost > median_cost:
                category = "high_impact_high_cost"
            elif savings < median_savings and cost <= median_cost:
                category = "low_impact_low_cost"
            else:
                category = "low_impact_high_cost"
            
            matrix[category].append({
                "title": rec.title,
                "cost": cost,
                "savings": savings,
                "priority": rec.priority.value
            })
        
        return matrix
    
    def _create_action_plan(self, recommendations: List[ImprovementRecommendation]) -> Dict[str, Any]:
        """Vytvorenie akčného plánu"""
        # Rozdelenie na fázy podľa priority a implementačnej zložitosti
        immediate_actions = [rec for rec in recommendations if rec.priority == Priority.CRITICAL]
        short_term_actions = [rec for rec in recommendations if rec.priority == Priority.HIGH and rec.implementation_complexity == "low"]
        medium_term_actions = [rec for rec in recommendations if rec.priority in [Priority.HIGH, Priority.MEDIUM] and rec.implementation_complexity == "medium"]
        long_term_actions = [rec for rec in recommendations if rec.priority == Priority.MEDIUM and rec.implementation_complexity == "high"]
        
        def create_phase_info(actions, phase_name):
            return {
                "phase": phase_name,
                "action_count": len(actions),
                "total_cost": sum(rec.estimated_cost or 0 for rec in actions),
                "total_annual_savings": sum(rec.estimated_savings_annual or 0 for rec in actions),
                "actions": [rec.title for rec in actions]
            }
        
        return {
            "immediate_phase": create_phase_info(immediate_actions, "Okamžité akcie (0-6 mesiacov)"),
            "short_term_phase": create_phase_info(short_term_actions, "Krátkodobé (6-12 mesiacov)"),
            "medium_term_phase": create_phase_info(medium_term_actions, "Strednodobé (1-2 roky)"),
            "long_term_phase": create_phase_info(long_term_actions, "Dlhodobé (2+ roky)"),
            "total_implementation_timeline": "2-5 rokov",
            "critical_path": [rec.title for rec in immediate_actions + short_term_actions[:2]]
        }
    
    def _check_compliance_status(self, energy_results: Dict[str, Any]) -> Dict[str, Any]:
        """Kontrola súladu s normami"""
        energy_class = energy_results['energy_classification']['energy_class']
        specific_energy = energy_results['energy_classification']['specific_primary_energy']
        
        # Hodnotenie súladu s rôznymi štandardmi
        compliance_checks = {
            "stn_73_0540_2012": {
                "standard_name": "STN 73 0540-2:2012",
                "compliant": specific_energy <= 150,
                "target_value": 150,
                "current_value": specific_energy,
                "status": "Vyhovuje" if specific_energy <= 150 else "Nevyhovuje"
            },
            "passive_house": {
                "standard_name": "Pasívny dom",
                "compliant": specific_energy <= 60,
                "target_value": 60,
                "current_value": specific_energy,
                "status": "Vyhovuje" if specific_energy <= 60 else "Nevyhovuje"
            },
            "nearly_zero_energy": {
                "standard_name": "Takmer nulová energia (nZEB)",
                "compliant": specific_energy <= 45,
                "target_value": 45,
                "current_value": specific_energy,
                "status": "Vyhovuje" if specific_energy <= 45 else "Nevyhovuje"
            }
        }
        
        return {
            "current_energy_class": energy_class,
            "compliance_checks": compliance_checks,
            "overall_compliance_rating": self._get_overall_compliance_rating(compliance_checks),
            "improvement_needed_for_compliance": specific_energy - 45 if specific_energy > 45 else 0
        }
    
    def _get_overall_compliance_rating(self, compliance_checks: Dict[str, Any]) -> str:
        """Celkové hodnotenie súladu"""
        compliant_count = sum(1 for check in compliance_checks.values() if check['compliant'])
        total_checks = len(compliance_checks)
        
        if compliant_count == total_checks:
            return "Plne vyhovuje všetkým štandardom"
        elif compliant_count >= total_checks * 0.7:
            return "Vyhovuje väčšine štandardov"
        elif compliant_count >= total_checks * 0.3:
            return "Čiastočne vyhovuje"
        else:
            return "Nevyhovuje základným štandardom"
    
    def _create_executive_summary(self, audit_data: Dict[str, Any], energy_results: Dict[str, Any],
                                recommendations: List[ImprovementRecommendation],
                                financial_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Vytvorenie exekutívneho súhrnu"""
        summary = energy_results['summary']
        classification = energy_results['energy_classification']
        
        return {
            "building_overview": {
                "name": audit_data.get('building_name', 'Bez názvu'),
                "type": audit_data.get('building_type', 'Neuvedený'),
                "area": audit_data.get('heated_area', 0),
                "construction_year": audit_data.get('construction_year', 'Neuvedený')
            },
            "energy_performance": {
                "energy_class": classification['energy_class'],
                "class_description": classification['class_description'],
                "primary_energy": f"{summary['specific_primary_energy']:.1f} kWh/m²rok",
                "heating_demand": f"{summary['specific_heating_demand']:.1f} kWh/m²rok",
                "co2_emissions": f"{summary['specific_co2_emissions']:.1f} kg/m²rok"
            },
            "improvement_potential": {
                "total_recommendations": len(recommendations),
                "critical_priority": len([r for r in recommendations if r.priority == Priority.CRITICAL]),
                "total_investment": f"{financial_analysis['total_investment_cost']:.0f} €",
                "annual_savings": f"{financial_analysis['total_annual_savings']:.0f} €/rok",
                "payback_period": f"{financial_analysis['overall_payback_period']:.1f} rokov"
            },
            "key_findings": self._extract_key_findings(energy_results, recommendations),
            "next_steps": [rec.title for rec in recommendations[:3]]  # Top 3 odporúčania
        }
    
    def _extract_key_findings(self, energy_results: Dict[str, Any],
                            recommendations: List[ImprovementRecommendation]) -> List[str]:
        """Extrakcia kľúčových zistení"""
        findings = []
        
        energy_class = energy_results['energy_classification']['energy_class']
        
        if energy_class in ['A1', 'A2']:
            findings.append("Budova má vynikajúcu energetickú efektívnosť")
        elif energy_class in ['F', 'G']:
            findings.append("Budova vyžaduje komplexnú energetickú renováciu")
        
        # Najväčšie straty
        transmission_losses = energy_results.get('transmission', {}).get('annual_transmission_losses', 0)
        ventilation_losses = energy_results.get('ventilation', {}).get('annual_ventilation_losses', 0)
        
        if transmission_losses > ventilation_losses * 2:
            findings.append("Hlavné straty sú cez stavebné konštrukcie - potrebné zateplenie")
        elif ventilation_losses > transmission_losses * 1.5:
            findings.append("Vysoké straty vetraním - kontrola vzduchotesnosti")
        
        # Odporúčania s najlepším pomerom náklad/prínos
        if recommendations:
            best_rec = min(recommendations, key=lambda r: r.payback_period or float('inf'))
            if best_rec.payback_period and best_rec.payback_period < 7:
                findings.append(f"Najefektívnejšie opatrenie: {best_rec.title} (návratnosť {best_rec.payback_period:.1f} rokov)")
        
        return findings
    
    def _recommendation_to_dict(self, rec: ImprovementRecommendation) -> Dict[str, Any]:
        """Konverzia odporúčania na slovník"""
        return {
            "title": rec.title,
            "description": rec.description,
            "category": rec.category,
            "priority": rec.priority.value,
            "priority_name": rec.priority.name,
            "estimated_cost": rec.estimated_cost,
            "estimated_savings_annual": rec.estimated_savings_annual,
            "estimated_energy_savings": rec.estimated_energy_savings,
            "payback_period": rec.payback_period,
            "implementation_complexity": rec.implementation_complexity,
            "environmental_impact": rec.environmental_impact
        }
    
    def generate_comparison_report(self, audit_ids: List[int]) -> Dict[str, Any]:
        """
        Generovanie porovnacej správy pre viac auditov
        
        Args:
            audit_ids: Zoznam ID auditov na porovnanie
            
        Returns:
            Porovnacia správa
        """
        if len(audit_ids) < 2:
            raise ValueError("Na porovnanie sú potrebné aspoň 2 audity")
        
        audit_reports = []
        for audit_id in audit_ids:
            try:
                report = self.generate_comprehensive_report(audit_id)
                audit_reports.append(report)
            except Exception as e:
                print(f"Chyba pri generovaní správy pre audit {audit_id}: {e}")
        
        if not audit_reports:
            raise ValueError("Nepodarilo sa vygenerovať žiadne správy")
        
        # Porovnacie analýzy
        comparison_data = self._create_comparison_analysis(audit_reports)
        
        return {
            "report_metadata": {
                "report_type": ReportType.COMPARISON_STUDY.value,
                "generated_date": datetime.now().isoformat(),
                "audit_count": len(audit_reports)
            },
            "individual_reports": audit_reports,
            "comparison_analysis": comparison_data,
            "benchmark_rankings": self._rank_audits_by_performance(audit_reports),
            "best_practices": self._identify_best_practices(audit_reports)
        }
    
    def _create_comparison_analysis(self, reports: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Vytvorenie porovnacej analýzy"""
        energy_classes = [report['building_information']['energy_classification']['energy_class'] for report in reports]
        primary_energies = [report['building_information']['energy_performance']['specific_primary_energy'] for report in reports]
        heating_demands = [report['building_information']['energy_performance']['specific_heating_demand'] for report in reports]
        
        return {
            "energy_class_distribution": {cls: energy_classes.count(cls) for cls in set(energy_classes)},
            "performance_statistics": {
                "primary_energy": {
                    "min": min(primary_energies),
                    "max": max(primary_energies),
                    "avg": statistics.mean(primary_energies),
                    "median": statistics.median(primary_energies)
                },
                "heating_demand": {
                    "min": min(heating_demands),
                    "max": max(heating_demands),
                    "avg": statistics.mean(heating_demands),
                    "median": statistics.median(heating_demands)
                }
            },
            "performance_gaps": {
                "primary_energy_gap": max(primary_energies) - min(primary_energies),
                "heating_demand_gap": max(heating_demands) - min(heating_demands)
            }
        }
    
    def _rank_audits_by_performance(self, reports: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Zoradenie auditov podľa výkonnosti"""
        rankings = []
        
        for report in reports:
            building_info = report['building_information']
            rankings.append({
                "audit_name": report['report_metadata']['audit_name'],
                "audit_id": report['report_metadata']['audit_id'],
                "energy_class": building_info['energy_classification']['energy_class'],
                "primary_energy": building_info['energy_performance']['specific_primary_energy'],
                "heating_demand": building_info['energy_performance']['specific_heating_demand']
            })
        
        # Zoradenie podľa primárnej energie
        rankings.sort(key=lambda x: x['primary_energy'])
        
        # Pridanie rankov
        for i, ranking in enumerate(rankings):
            ranking['rank'] = i + 1
        
        return rankings
    
    def _identify_best_practices(self, reports: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Identifikácia najlepších praktík"""
        best_practices = {}
        
        # Najlepší audit celkovo
        best_audit = min(reports, key=lambda r: r['building_information']['energy_performance']['specific_primary_energy'])
        
        best_practices['overall_best'] = {
            "audit_name": best_audit['report_metadata']['audit_name'],
            "energy_class": best_audit['building_information']['energy_classification']['energy_class'],
            "primary_energy": best_audit['building_information']['energy_performance']['specific_primary_energy']
        }
        
        # Najlepšie praktiky podľa kategórií
        best_practices['category_leaders'] = {
            "lowest_heating_demand": min(reports, key=lambda r: r['building_information']['energy_performance']['specific_heating_demand'])['report_metadata']['audit_name'],
            "lowest_co2_emissions": min(reports, key=lambda r: r['building_information']['energy_performance']['specific_co2_emissions'])['report_metadata']['audit_name']
        }
        
        return best_practices


# Globálna inštancia
advanced_report_generator = AdvancedReportGenerator()


def get_advanced_report_generator() -> AdvancedReportGenerator:
    """Získanie globálnej inštancie generátora pokročilých správ"""
    return advanced_report_generator