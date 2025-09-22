#!/usr/bin/env python3
"""
Project Management Module pre energetické projekty
Implementuje proces prípravy projektov obnovy budov podľa kapitoly 10.8
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
import datetime
import json

class ProjectPhase(Enum):
    """Fázy projektu energetickej obnovy"""
    IDENTIFICATION = "Identifikácia projektu"
    INSPECTION = "Prehliadka"
    ENERGY_AUDIT = "Energetický audit"
    BUSINESS_PLAN = "Podnikateľský plán"
    IMPLEMENTATION = "Realizácia"
    OPERATION = "Prevádzka"

class ProjectStatus(Enum):
    """Status projektu"""
    PLANNING = "Plánovanie"
    IN_PROGRESS = "V procese" 
    COMPLETED = "Dokončené"
    ON_HOLD = "Pozastavené"
    CANCELLED = "Zrušené"

@dataclass
class EnergyMeasure:
    """Energetické úsporné opatrenie"""
    id: str
    name: str
    description: str
    investment: float  # EUR
    energy_savings: float  # kWh/rok
    cost_savings: float  # EUR/rok
    payback_time: float  # roky
    npv: float = 0.0
    irr: float = 0.0
    category: str = "Ostatné"
    
@dataclass
class ProjectPotential:
    """Potenciál energetických úspor projektu"""
    total_energy_savings: float = 0.0  # kWh/rok
    total_cost_savings: float = 0.0    # EUR/rok
    total_investment: float = 0.0      # EUR
    overall_payback: float = 0.0       # roky
    measures: List[EnergyMeasure] = field(default_factory=list)

@dataclass
class InspectionFindings:
    """Zistenia z prehliadky"""
    building_condition: str = "Dobrý"
    technical_systems: Dict[str, str] = field(default_factory=dict)
    energy_consumption: Dict[str, float] = field(default_factory=dict)
    identified_measures: List[str] = field(default_factory=list)
    renovation_needs: List[str] = field(default_factory=list)
    inspector_notes: str = ""
    inspection_date: Optional[datetime.date] = None

class EnergyProjectManager:
    """Hlavná trieda pre manažment energetických projektov"""
    
    def __init__(self):
        self.projects = {}
        
    def create_project(self, project_id: str, building_data: Dict) -> Dict:
        """
        Vytvorenie nového projektu energetickej obnovy
        
        Args:
            project_id: Jedinečný identifikátor projektu
            building_data: Základné údaje o budove
            
        Returns:
            Dict s informáciami o vytvorenom projekte
        """
        project = {
            'id': project_id,
            'building_data': building_data,
            'phase': ProjectPhase.IDENTIFICATION,
            'status': ProjectStatus.PLANNING,
            'created_date': datetime.datetime.now(),
            'phases_completed': [],
            'potential': ProjectPotential(),
            'inspection_findings': None,
            'audit_results': None,
            'business_plan': None,
            'financing': None,
            'implementation_plan': None
        }
        
        self.projects[project_id] = project
        return project
        
    def phase_1_project_identification(self, project_id: str, owner_data: Dict) -> Dict:
        """
        Fáza 1: Identifikácia projektu
        
        Zahŕňa:
        - Dialóg s vlastníkom budovy
        - Zozberanie hlavných údajov o budove
        - Zozberanie štatistík spotrieb energií
        - Zhodnotenie záujmu o realizáciu
        - Zhodnotenie investorových možností
        """
        if project_id not in self.projects:
            raise ValueError(f"Projekt {project_id} neexistuje")
            
        project = self.projects[project_id]
        
        # Identifikačné údaje
        identification_data = {
            'owner_info': owner_data,
            'building_characteristics': project['building_data'],
            'energy_statistics': self._collect_energy_statistics(project['building_data']),
            'investment_capacity': owner_data.get('investment_budget', 0),
            'motivation_level': owner_data.get('motivation', 'Stredná'),
            'decision_factors': owner_data.get('decision_factors', []),
            'preliminary_assessment': self._preliminary_viability_check(project_id)
        }
        
        project['identification_data'] = identification_data
        project['phase'] = ProjectPhase.INSPECTION
        project['phases_completed'].append(ProjectPhase.IDENTIFICATION)
        
        return identification_data
        
    def phase_2_inspection(self, project_id: str, inspection_data: Dict) -> InspectionFindings:
        """
        Fáza 2: Prehliadka
        
        Zahŕňa:
        - Prípravu na inšpekciu
        - Inšpekciu budovy
        - Presný opis skutkového stavu
        - Energetické výpočty a ekonomické hodnotenie
        - Vypracovanie správy z prehliadky
        """
        if project_id not in self.projects:
            raise ValueError(f"Projekt {project_id} neexistuje")
            
        project = self.projects[project_id]
        
        findings = InspectionFindings(
            building_condition=inspection_data.get('condition', 'Dobrý'),
            technical_systems=inspection_data.get('systems', {}),
            energy_consumption=inspection_data.get('consumption', {}),
            identified_measures=inspection_data.get('measures', []),
            renovation_needs=inspection_data.get('renovation_needs', []),
            inspector_notes=inspection_data.get('notes', ''),
            inspection_date=datetime.date.today()
        )
        
        # Výpočet potenciálu úspor
        potential = self._calculate_savings_potential(findings)
        project['potential'] = potential
        project['inspection_findings'] = findings
        
        # Rozhodnutie o pokračovaní
        if potential.overall_payback <= 10.0:  # Akceptovateľná návratnosť
            project['phase'] = ProjectPhase.ENERGY_AUDIT
            project['phases_completed'].append(ProjectPhase.INSPECTION)
            
        return findings
        
    def phase_3_energy_audit(self, project_id: str, audit_type: str = "detailed") -> Dict:
        """
        Fáza 3: Energetický audit
        
        Typy auditu:
        - "simple": presnosť ±10-15%
        - "detailed": presnosť ±5-10% so zárukou
        """
        if project_id not in self.projects:
            raise ValueError(f"Projekt {project_id} neexistuje")
            
        project = self.projects[project_id]
        
        audit_results = {
            'audit_type': audit_type,
            'accuracy': "±5-10%" if audit_type == "detailed" else "±10-15%",
            'detailed_measures': self._detailed_measures_analysis(project),
            'energy_calculations': self._perform_energy_calculations(project),
            'economic_analysis': self._perform_economic_analysis(project),
            'implementation_recommendations': self._generate_implementation_recommendations(project),
            'guarantee_offered': audit_type == "detailed"
        }
        
        project['audit_results'] = audit_results
        project['phase'] = ProjectPhase.BUSINESS_PLAN
        project['phases_completed'].append(ProjectPhase.ENERGY_AUDIT)
        
        return audit_results
        
    def phase_4_business_plan(self, project_id: str, financing_requirements: Dict) -> Dict:
        """
        Fáza 4: Podnikateľský plán
        
        Vypracováva sa ak sú potrebné vonkajšie zdroje financovania
        """
        if project_id not in self.projects:
            raise ValueError(f"Projekt {project_id} neexistuje")
            
        project = self.projects[project_id]
        
        business_plan = {
            'executive_summary': self._create_executive_summary(project),
            'debtor_information': financing_requirements.get('debtor_info', {}),
            'project_information': project['audit_results'],
            'environmental_benefits': self._calculate_environmental_benefits(project),
            'market_overview': self._market_analysis(),
            'financing_plan': self._create_financing_plan(project, financing_requirements),
            'financial_projections': self._create_financial_projections(project),
            'implementation_schedule': self._create_implementation_schedule(project)
        }
        
        project['business_plan'] = business_plan
        project['phase'] = ProjectPhase.IMPLEMENTATION
        project['phases_completed'].append(ProjectPhase.BUSINESS_PLAN)
        
        return business_plan
        
    def phase_5_implementation(self, project_id: str, implementation_data: Dict) -> Dict:
        """
        Fáza 5: Realizácia
        
        Zahŕňa:
        - Organizáciu projektu
        - Návrh/projekciu
        - Kontrahovanie dodávok
        - Realizáciu a montáž
        - Kontrolu dodávky a skúšky
        """
        if project_id not in self.projects:
            raise ValueError(f"Projekt {project_id} neexistuje")
            
        project = self.projects[project_id]
        
        implementation_plan = {
            'project_organization': implementation_data.get('organization', {}),
            'design_documentation': implementation_data.get('design_docs', []),
            'contractor_selection': implementation_data.get('contractors', []),
            'implementation_schedule': implementation_data.get('schedule', {}),
            'quality_control': implementation_data.get('quality_plan', {}),
            'commissioning_plan': implementation_data.get('commissioning', {}),
            'documentation_requirements': self._define_documentation_requirements(),
            'training_plan': implementation_data.get('training', {})
        }
        
        project['implementation_plan'] = implementation_plan
        project['phase'] = ProjectPhase.OPERATION
        project['phases_completed'].append(ProjectPhase.IMPLEMENTATION)
        
        return implementation_plan
        
    def phase_6_operation_maintenance(self, project_id: str) -> Dict:
        """
        Fáza 6: Prevádzka a údržba
        
        Zahŕňa:
        - Vytvorenie manuálu prevádzky a údržby
        - Energetický manažment
        - Monitoring výsledkov
        """
        if project_id not in self.projects:
            raise ValueError(f"Projekt {project_id} neexistuje")
            
        project = self.projects[project_id]
        
        operation_plan = {
            'operation_manual': self._create_operation_manual(project),
            'maintenance_schedule': self._create_maintenance_schedule(project),
            'energy_management_system': self._setup_energy_management(project),
            'monitoring_plan': self._create_monitoring_plan(project),
            'performance_targets': self._define_performance_targets(project),
            'reporting_schedule': self._define_reporting_schedule()
        }
        
        project['operation_plan'] = operation_plan
        project['status'] = ProjectStatus.COMPLETED
        project['phases_completed'].append(ProjectPhase.OPERATION)
        
        return operation_plan
        
    def get_project_status(self, project_id: str) -> Dict:
        """Získanie aktuálneho statusu projektu"""
        if project_id not in self.projects:
            raise ValueError(f"Projekt {project_id} neexistuje")
            
        project = self.projects[project_id]
        
        return {
            'id': project_id,
            'current_phase': project['phase'].value,
            'status': project['status'].value,
            'completed_phases': [phase.value for phase in project['phases_completed']],
            'progress_percentage': len(project['phases_completed']) / 6 * 100,
            'created_date': project['created_date'].strftime('%Y-%m-%d'),
            'potential_savings': {
                'energy': project['potential'].total_energy_savings,
                'cost': project['potential'].total_cost_savings,
                'investment': project['potential'].total_investment,
                'payback': project['potential'].overall_payback
            } if project['potential'] else None
        }
        
    def _collect_energy_statistics(self, building_data: Dict) -> Dict:
        """Zozberanie štatistík spotreby energií"""
        return {
            'electricity_consumption': building_data.get('electricity_annual', 0),
            'gas_consumption': building_data.get('gas_annual', 0),
            'heating_consumption': building_data.get('heating_annual', 0),
            'specific_consumption': building_data.get('specific_consumption', 0),
            'historical_data': building_data.get('historical_consumption', [])
        }
        
    def _preliminary_viability_check(self, project_id: str) -> Dict:
        """Predbežné posúdenie životaschopnosti projektu"""
        project = self.projects[project_id]
        building_data = project['building_data']
        
        # Jednoduchá analýza na základe typu a veku budovy
        building_age = building_data.get('construction_year', 2000)
        current_year = datetime.datetime.now().year
        age = current_year - building_age
        
        potential_rating = "Vysoký"
        if age < 10:
            potential_rating = "Nízky"
        elif age < 30:
            potential_rating = "Stredný"
            
        return {
            'energy_saving_potential': potential_rating,
            'estimated_payback': min(15, max(3, age * 0.3)),
            'recommended_proceed': age >= 15,
            'risk_assessment': "Nízke riziko" if age >= 20 else "Stredné riziko"
        }
        
    def _calculate_savings_potential(self, findings: InspectionFindings) -> ProjectPotential:
        """Výpočet potenciálu energetických úspor"""
        # Simulované výpočty na základe zistení
        measures = []
        total_investment = 0
        total_savings = 0
        
        # Príklady opatrení na základe identifikovaných potrieb
        if "Tepelná izolácia" in findings.identified_measures:
            measure = EnergyMeasure(
                id="TI001",
                name="Tepelná izolácia obvodových stien",
                description="Zateplenie obvodového plášťa",
                investment=15000,
                energy_savings=25000,
                cost_savings=2500,
                payback_time=6.0,
                category="Stavebné opatrenia"
            )
            measures.append(measure)
            total_investment += measure.investment
            total_savings += measure.cost_savings
            
        if "Výmena okien" in findings.identified_measures:
            measure = EnergyMeasure(
                id="VO001", 
                name="Výmena okien",
                description="Inštalácia nových energeticky efektívnych okien",
                investment=8000,
                energy_savings=8000,
                cost_savings=800,
                payback_time=10.0,
                category="Stavebné opatrenia"
            )
            measures.append(measure)
            total_investment += measure.investment
            total_savings += measure.cost_savings
            
        overall_payback = total_investment / total_savings if total_savings > 0 else float('inf')
        
        return ProjectPotential(
            total_energy_savings=sum(m.energy_savings for m in measures),
            total_cost_savings=total_savings,
            total_investment=total_investment,
            overall_payback=overall_payback,
            measures=measures
        )
        
    # Pomocné metódy pre ďalšie fázy (zjednodušené implementácie)
    def _detailed_measures_analysis(self, project: Dict) -> List[Dict]:
        """Detailná analýza opatrení"""
        return [
            {
                'measure_id': measure.id,
                'name': measure.name,
                'investment': measure.investment,
                'annual_savings': measure.cost_savings,
                'payback_period': measure.payback_time,
                'priority': 'Vysoká' if measure.payback_time < 5 else 'Stredná'
            }
            for measure in project['potential'].measures
        ]
        
    def _perform_energy_calculations(self, project: Dict) -> Dict:
        """Energetické výpočty"""
        return {
            'baseline_consumption': project['building_data'].get('total_consumption', 0),
            'projected_consumption': 0,  # Po implementácii opatrení
            'total_savings': project['potential'].total_energy_savings,
            'savings_percentage': 0,  # Percentuálne úspory
        }
        
    def _perform_economic_analysis(self, project: Dict) -> Dict:
        """Ekonomická analýza s detailnými finančnými výpočtami"""
        total_investment = project['potential'].total_investment
        annual_savings = project['potential'].total_cost_savings
        
        # Parametry pre finančnú analýzu
        discount_rate = 0.05  # 5% diskontná sadzba
        energy_price_escalation = 0.03  # 3% ročný rast cien energií
        maintenance_cost_rate = 0.02  # 2% z investície ročne na údržbu
        project_lifetime = 20  # roky
        
        # Výpočet NPV
        npv = self._calculate_npv(
            total_investment, annual_savings, discount_rate, 
            energy_price_escalation, maintenance_cost_rate, project_lifetime
        )
        
        # Výpočet IRR
        irr = self._calculate_irr(
            total_investment, annual_savings, energy_price_escalation, 
            maintenance_cost_rate, project_lifetime
        )
        
        # Výpočet modifikovanej doby návratnosti (s diskontom)
        discounted_payback = self._calculate_discounted_payback(
            total_investment, annual_savings, discount_rate, 
            energy_price_escalation, maintenance_cost_rate
        )
        
        # Analýza citlivosti
        sensitivity_analysis = self._perform_sensitivity_analysis(
            total_investment, annual_savings, discount_rate, project_lifetime
        )
        
        return {
            'total_investment': total_investment,
            'annual_savings': annual_savings,
            'simple_payback': project['potential'].overall_payback,
            'discounted_payback': discounted_payback,
            'npv_20_years': npv,
            'irr': irr * 100 if irr else 0,  # Konverzia na percentá
            'energy_price_escalation': energy_price_escalation * 100,
            'maintenance_cost_annual': total_investment * maintenance_cost_rate,
            'profitability_index': (npv + total_investment) / total_investment if total_investment > 0 else 0,
            'sensitivity_analysis': sensitivity_analysis
        }
        
    def _generate_implementation_recommendations(self, project: Dict) -> List[str]:
        """Odporúčania pre implementáciu"""
        return [
            "Začať s opatreniami s najkratšou dobou návratnosti",
            "Koordinovať stavebné práce pre minimalizáciu nákladov",
            "Zabezpečiť kvalitné prevedenie všetkých opatrení",
            "Implementovať systém monitorovania úspor"
        ]
        
    def _create_executive_summary(self, project: Dict) -> str:
        """Vytvorenie výkonného súhrnu"""
        return f"""
        Projekt energetickej obnovy budovy s celkovými investíciami {project['potential'].total_investment:.0f} EUR.
        Očakávané ročné úspory: {project['potential'].total_cost_savings:.0f} EUR.
        Doba návratnosti: {project['potential'].overall_payback:.1f} rokov.
        """
        
    def _calculate_environmental_benefits(self, project: Dict) -> Dict:
        """Výpočet environmentálnych prínosov"""
        return {
            'co2_reduction_annual': project['potential'].total_energy_savings * 0.2,  # kg CO2/rok
            'primary_energy_savings': project['potential'].total_energy_savings * 2.5,  # kWh/rok
            'environmental_value': 'Vysoká'
        }
        
    def _market_analysis(self) -> Dict:
        """Analýza trhu"""
        return {
            'energy_price_trend': 'Rastúci',
            'regulatory_environment': 'Podporný',
            'technology_availability': 'Dostupné',
            'market_readiness': 'Vysoká'
        }
        
    def _create_financing_plan(self, project: Dict, requirements: Dict) -> Dict:
        """Plán financovania"""
        return {
            'total_investment': project['potential'].total_investment,
            'own_resources': requirements.get('own_capital', 0),
            'external_financing': project['potential'].total_investment - requirements.get('own_capital', 0),
            'financing_sources': requirements.get('sources', []),
            'loan_terms': requirements.get('loan_terms', {})
        }
        
    def _create_financial_projections(self, project: Dict) -> Dict:
        """Detailné finančné prognózy na 20 rokov"""
        total_investment = project['potential'].total_investment
        annual_savings = project['potential'].total_cost_savings
        
        # Parametre
        energy_price_escalation = 0.03  # 3% ročný rast cien energií
        maintenance_rate = 0.02  # 2% z investície ročne
        discount_rate = 0.05  # 5% diskontná sadzba
        major_renovation_years = [10, 20]  # Veľké opravy
        major_renovation_cost_rate = 0.15  # 15% z pôvodnej investície
        
        cash_flows = []
        cumulative_savings = []
        cumulative_undiscounted = 0
        cumulative_discounted = 0
        break_even_year = None
        
        # Ročné projekcie
        for year in range(0, 21):  # 0-20 rokov
            if year == 0:
                # Počiatočná investícia
                cash_flow_item = {
                    'year': year,
                    'energy_savings': 0,
                    'maintenance_cost': 0,
                    'major_renovation_cost': 0,
                    'investment': total_investment,
                    'net_cash_flow': -total_investment,
                    'discounted_cash_flow': -total_investment,
                    'cumulative_undiscounted': -total_investment,
                    'cumulative_discounted': -total_investment
                }
                cumulative_undiscounted = -total_investment
                cumulative_discounted = -total_investment
            else:
                # Úspory s eskaláciou
                energy_savings = annual_savings * ((1 + energy_price_escalation) ** (year - 1))
                
                # Náklady na údržbu
                maintenance_cost = total_investment * maintenance_rate
                
                # Veľké opravy
                major_renovation_cost = 0
                if year in major_renovation_years:
                    major_renovation_cost = total_investment * major_renovation_cost_rate
                
                # čistý cash flow
                net_cash_flow = energy_savings - maintenance_cost - major_renovation_cost
                
                # Diskontovaný cash flow
                discount_factor = (1 + discount_rate) ** year
                discounted_cash_flow = net_cash_flow / discount_factor
                
                # Kumulatívne hodnoty
                cumulative_undiscounted += net_cash_flow
                cumulative_discounted += discounted_cash_flow
                
                # Kontrola bodu vyrovnania
                if break_even_year is None and cumulative_undiscounted >= 0:
                    break_even_year = year
                
                cash_flow_item = {
                    'year': year,
                    'energy_savings': energy_savings,
                    'maintenance_cost': maintenance_cost,
                    'major_renovation_cost': major_renovation_cost,
                    'investment': 0,
                    'net_cash_flow': net_cash_flow,
                    'discounted_cash_flow': discounted_cash_flow,
                    'cumulative_undiscounted': cumulative_undiscounted,
                    'cumulative_discounted': cumulative_discounted
                }
            
            cash_flows.append(cash_flow_item)
            cumulative_savings.append(cumulative_undiscounted)
        
        # Celkové súhrnné údaje
        total_energy_savings_20y = sum(cf['energy_savings'] for cf in cash_flows[1:])
        total_maintenance_costs_20y = sum(cf['maintenance_cost'] for cf in cash_flows[1:])
        total_renovation_costs_20y = sum(cf['major_renovation_cost'] for cf in cash_flows[1:])
        
        return {
            'cash_flow_projection': cash_flows,
            'cumulative_savings': cumulative_savings,
            'break_even_year': break_even_year or float('inf'),
            'total_energy_savings_20y': total_energy_savings_20y,
            'total_maintenance_costs_20y': total_maintenance_costs_20y,
            'total_renovation_costs_20y': total_renovation_costs_20y,
            'final_cumulative_savings': cumulative_undiscounted,
            'final_npv': cumulative_discounted,
            'average_annual_savings': total_energy_savings_20y / 20,
            'savings_to_investment_ratio': total_energy_savings_20y / total_investment if total_investment > 0 else 0
        }
        
    def _create_implementation_schedule(self, project: Dict) -> Dict:
        """Harmonogram implementácie"""
        return {
            'total_duration_months': 6,
            'phases': [
                {'phase': 'Projektová dokumentácia', 'duration': 2},
                {'phase': 'Výberové konania', 'duration': 1}, 
                {'phase': 'Realizácia', 'duration': 3},
                {'phase': 'Uvedenie do prevádzky', 'duration': 1}
            ]
        }
        
    def _define_documentation_requirements(self) -> List[str]:
        """Požiadavky na dokumentáciu"""
        return [
            "Projektová dokumentácia skutočného vyhotovenia",
            "Protokoly o skúškach a meraniach",
            "Manuály prevádzky a údržby",
            "Energetický certifikát",
            "Záručné listy"
        ]
        
    def _create_operation_manual(self, project: Dict) -> Dict:
        """Manuál prevádzky a údržby"""
        return {
            'operating_procedures': [],
            'maintenance_schedule': {},
            'troubleshooting_guide': {},
            'energy_management_instructions': {},
            'contact_information': {}
        }
        
    def _create_maintenance_schedule(self, project: Dict) -> Dict:
        """Harmonogram údržby"""
        return {
            'daily_checks': [],
            'weekly_maintenance': [],
            'monthly_maintenance': [],
            'annual_maintenance': []
        }
        
    def _setup_energy_management(self, project: Dict) -> Dict:
        """Nastavenie energetického manažmentu"""
        return {
            'monitoring_points': [],
            'target_consumption': 0,
            'reporting_frequency': 'monthly',
            'alert_thresholds': {}
        }
        
    def _create_monitoring_plan(self, project: Dict) -> Dict:
        """Plán monitorovania"""
        return {
            'kpi_indicators': ['energia', 'náklady', 'emisie'],
            'measurement_frequency': 'weekly',
            'reporting_schedule': 'monthly',
            'review_meetings': 'quarterly'
        }
        
    def _define_performance_targets(self, project: Dict) -> Dict:
        """Výkonnostné ciele"""
        return {
            'energy_reduction_target': f"{project['potential'].total_energy_savings:.0f} kWh/rok",
            'cost_savings_target': f"{project['potential'].total_cost_savings:.0f} EUR/rok",
            'payback_target': f"{project['potential'].overall_payback:.1f} rokov"
        }
        
    def _define_reporting_schedule(self) -> Dict:
        """Harmonogram reportovania"""
        return {
            'monthly_reports': 'Mesačné energetické reporty',
            'quarterly_reviews': 'Štvrťročné hodnotenie výkonnosti',
            'annual_assessment': 'Ročné vyhodnotenie projektu'
        }
    
    def _calculate_npv(self, investment: float, annual_savings: float, 
                      discount_rate: float, escalation_rate: float,
                      maintenance_rate: float, years: int) -> float:
        """
        Výpočet čistej súčasnej hodnoty (NPV)
        
        Args:
            investment: Počiatočná investícia
            annual_savings: Ročné úspory v prvom roku
            discount_rate: Diskontná sadzba
            escalation_rate: Rast cien energií
            maintenance_rate: Náklady na údržbu ako % z investície
            years: Počet rokov
            
        Returns:
            NPV hodnota
        """
        npv = -investment  # Počiatočná investícia
        
        for year in range(1, years + 1):
            # Úspory s eskaláciou
            savings_year = annual_savings * ((1 + escalation_rate) ** (year - 1))
            
            # Náklady na údržbu
            maintenance_cost = investment * maintenance_rate
            
            # čistý cash flow za rok
            net_cash_flow = savings_year - maintenance_cost
            
            # Diskontovaná hodnota
            pv = net_cash_flow / ((1 + discount_rate) ** year)
            npv += pv
        
        return npv
    
    def _calculate_irr(self, investment: float, annual_savings: float,
                      escalation_rate: float, maintenance_rate: float, 
                      years: int) -> float:
        """
        Výpočet vnútornej miery výnosnosti (IRR) pomocou iterácie
        
        Args:
            investment: Počiatočná investícia
            annual_savings: Ročné úspory
            escalation_rate: Rast cien energií
            maintenance_rate: Náklady na údržbu
            years: Počet rokov
            
        Returns:
            IRR ako desatinné číslo (0.1 = 10%)
        """
        def calculate_npv_at_rate(rate):
            npv = -investment
            for year in range(1, years + 1):
                savings_year = annual_savings * ((1 + escalation_rate) ** (year - 1))
                maintenance_cost = investment * maintenance_rate
                net_cash_flow = savings_year - maintenance_cost
                npv += net_cash_flow / ((1 + rate) ** year)
            return npv
        
        # Newton-Raphson metóda pre hľadanie IRR
        rate = 0.1  # Počiatočný odhad 10%
        tolerance = 1e-6
        max_iterations = 100
        
        for iteration in range(max_iterations):
            npv = calculate_npv_at_rate(rate)
            if abs(npv) < tolerance:
                return rate
            
            # Derivat (numerická aproximácia)
            delta = 1e-6
            npv_delta = calculate_npv_at_rate(rate + delta)
            derivative = (npv_delta - npv) / delta
            
            if abs(derivative) < tolerance:
                break
            
            # Newton-Raphson aktualizacía
            rate_new = rate - npv / derivative
            
            if abs(rate_new - rate) < tolerance:
                return rate_new
            
            rate = max(-0.99, min(rate_new, 10.0))  # Ohraničenie
        
        return rate if rate > 0 else 0
    
    def _calculate_discounted_payback(self, investment: float, annual_savings: float,
                                    discount_rate: float, escalation_rate: float,
                                    maintenance_rate: float) -> float:
        """
        Výpočet diskontovanej doby návratnosti
        
        Returns:
            Doba návratnosti v rokoch
        """
        cumulative_pv = 0
        year = 0
        
        while cumulative_pv < investment and year < 30:  # Maximum 30 rokov
            year += 1
            
            # Úspory s eskaláciou
            savings_year = annual_savings * ((1 + escalation_rate) ** (year - 1))
            
            # Náklady na údržbu
            maintenance_cost = investment * maintenance_rate
            
            # čistý cash flow
            net_cash_flow = savings_year - maintenance_cost
            
            # Diskontovaná hodnota
            pv = net_cash_flow / ((1 + discount_rate) ** year)
            cumulative_pv += pv
        
        return year if cumulative_pv >= investment else float('inf')
    
    def _perform_sensitivity_analysis(self, investment: float, annual_savings: float,
                                    base_discount_rate: float, years: int) -> Dict:
        """
        Analýza citlivosti NPV na zmeny kľúčových parametrov
        
        Returns:
            Slovník s výsledkami analýzy citlivosti
        """
        base_npv = self._calculate_npv(investment, annual_savings, base_discount_rate, 0.03, 0.02, years)
        
        sensitivity = {
            'base_npv': base_npv,
            'discount_rate_sensitivity': {},
            'savings_sensitivity': {},
            'investment_sensitivity': {}
        }
        
        # Citlivosť na diskontnú sadzbu (-2% až +2%)
        for delta in [-0.02, -0.01, 0.01, 0.02]:
            new_rate = base_discount_rate + delta
            new_npv = self._calculate_npv(investment, annual_savings, new_rate, 0.03, 0.02, years)
            sensitivity['discount_rate_sensitivity'][f'{delta*100:+.0f}%'] = {
                'npv': new_npv,
                'change': new_npv - base_npv
            }
        
        # Citlivosť na výšku úspor (-20% až +20%)
        for factor in [0.8, 0.9, 1.1, 1.2]:
            new_savings = annual_savings * factor
            new_npv = self._calculate_npv(investment, new_savings, base_discount_rate, 0.03, 0.02, years)
            sensitivity['savings_sensitivity'][f'{(factor-1)*100:+.0f}%'] = {
                'npv': new_npv,
                'change': new_npv - base_npv
            }
        
        # Citlivosť na výšku investície (-20% až +20%)
        for factor in [0.8, 0.9, 1.1, 1.2]:
            new_investment = investment * factor
            new_npv = self._calculate_npv(new_investment, annual_savings, base_discount_rate, 0.03, 0.02, years)
            sensitivity['investment_sensitivity'][f'{(factor-1)*100:+.0f}%'] = {
                'npv': new_npv,
                'change': new_npv - base_npv
            }
        
        return sensitivity

def get_project_manager():
    """Factory funkcia pre získanie project managera"""
    return EnergyProjectManager()

if __name__ == "__main__":
    # Test základnej funkcionality
    pm = EnergyProjectManager()
    
    # Testovací projekt
    building_data = {
        'name': 'Testovacia budova',
        'address': 'Bratislava',
        'construction_year': 1980,
        'heated_area': 1000,
        'total_consumption': 150000,
        'building_type': 'Bytový dom'
    }
    
    project = pm.create_project('TEST001', building_data)
    print(f"Vytvorený projekt: {project['id']}")
    
    # Test fázy identifikácie
    owner_data = {
        'name': 'Test Owner',
        'investment_budget': 50000,
        'motivation': 'Vysoká'
    }
    
    identification = pm.phase_1_project_identification('TEST001', owner_data)
    print(f"Fáza identifikácie dokončená: {identification['preliminary_assessment']}")
    
    status = pm.get_project_status('TEST001')
    print(f"Status projektu: {status}")