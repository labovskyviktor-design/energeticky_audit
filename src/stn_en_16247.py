#!/usr/bin/env python3
"""
STN EN 16247 Energy Audit Standard Implementation
Implementácia európskej normy STN EN 16247 pre energetické audity

Štandard definuje:
- Všeobecné požiadavky na energetické audity
- Štruktúru procesu auditu  
- Kvalifikácie audítorov
- Požiadavky na reporting
- Metodológiu merania a validácie
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Union
from enum import Enum
from datetime import datetime, date
import json
import logging

class AuditType(Enum):
    """Typy auditov podľa EN 16247"""
    BUILDING = "building"           # EN 16247-2: Budovy
    INDUSTRY = "industry"          # EN 16247-3: Priemysel  
    TRANSPORT = "transport"        # EN 16247-4: Doprava

class AuditScope(Enum):
    """Rozsah auditu"""
    COMPREHENSIVE = "comprehensive"  # Komplexný audit
    PARTIAL = "partial"             # Čiastkový audit
    WALK_THROUGH = "walk_through"   # Orientačný audit

class EnergyCarrier(Enum):
    """Energetické nosič podľa EN 16247"""
    ELECTRICITY = "electricity"
    NATURAL_GAS = "natural_gas"
    HEATING_OIL = "heating_oil"
    DISTRICT_HEATING = "district_heating"
    COAL = "coal"
    BIOMASS = "biomass"
    SOLAR = "solar"
    OTHER_RENEWABLE = "other_renewable"
    OTHER = "other"

class MeasurementMethod(Enum):
    """Metódy merania podľa EN 16247"""
    CONTINUOUS = "continuous"       # Kontinuálne meranie
    SHORT_TERM = "short_term"      # Krátkodobé meranie
    SPOT = "spot"                  # Bodové meranie
    CALCULATION = "calculation"     # Výpočet
    ESTIMATION = "estimation"       # Odhad
    MONTHLY_READINGS = "monthly_readings"  # Mesačné odpisy
    ANNUAL_BILLS = "annual_bills"   # Ročné faktúry

@dataclass
class AuditorQualification:
    """Kvalifikácia audítora podľa EN 16247"""
    name: str
    education_level: str           # Vzdelanostná úroveň
    experience_years: int          # Roky skúseností
    certification_number: Optional[str] = None
    certification_body: Optional[str] = None
    specialized_areas: List[str] = field(default_factory=list)
    continuous_education_hours: int = 0  # Hodin ďalšieho vzdelávania

    def is_qualified_for_audit_type(self, audit_type: AuditType) -> bool:
        """Kontrola či je audítor kvalifikovaný pre typ auditu"""
        min_experience = {
            AuditType.BUILDING: 2,
            AuditType.INDUSTRY: 3, 
            AuditType.TRANSPORT: 2
        }
        return self.experience_years >= min_experience.get(audit_type, 3)

@dataclass
class EnergyConsumptionData:
    """Údaje o spotrebe energie podľa EN 16247"""
    energy_carrier: EnergyCarrier
    annual_consumption: float      # kWh/rok
    unit_cost: float              # €/kWh
    measurement_method: MeasurementMethod
    measurement_period: str        # obdobie merania
    weather_correction: bool = False
    peak_demand: Optional[float] = None  # kW
    load_profile: List[float] = field(default_factory=list)
    seasonal_variation: Optional[Dict[str, float]] = None
    measurement_uncertainty: Optional[float] = None  # %

    @property
    def annual_cost(self) -> float:
        """Ročné náklady na energiu"""
        return self.annual_consumption * self.unit_cost

    @property
    def specific_consumption(self) -> Optional[float]:
        """Špecifická spotreba - bude vypočítaná vzhľadom na referenčnú jednotku"""
        return None  # Implementované v odvodených triedach

@dataclass
class EnergySystem:
    """Energetický systém podľa EN 16247"""
    system_id: str
    system_name: str
    system_type: str               # typ systému
    energy_input: List[EnergyConsumptionData]
    energy_output: Optional[List[EnergyConsumptionData]] = None
    efficiency: Optional[float] = None  # %
    capacity: Optional[float] = None    # kW
    age_years: Optional[int] = None
    operating_hours_annual: Optional[float] = None
    maintenance_status: str = "unknown"
    control_system: Optional[str] = None

    @property
    def total_input_energy(self) -> float:
        """Celková vstupná energia"""
        return sum(data.annual_consumption for data in self.energy_input)

    @property
    def total_input_cost(self) -> float:
        """Celkové náklady na vstupnú energiu"""
        return sum(data.annual_cost for data in self.energy_input)

@dataclass
class EnergyPerformanceIndicator:
    """Ukazovateľ energetickej výkonnosti (EnPI) podľa EN 16247"""
    name: str
    value: float
    unit: str
    reference_period: str
    baseline_value: Optional[float] = None
    target_value: Optional[float] = None
    improvement_potential: Optional[float] = None

    @property
    def improvement_percentage(self) -> Optional[float]:
        """Percentuálne zlepšenie oproti baseline"""
        if self.baseline_value and self.baseline_value != 0:
            return ((self.value - self.baseline_value) / self.baseline_value) * 100
        return None

@dataclass
class EnergyEfficiencyMeasure:
    """Opatrenie energetickej efektívnosti podľa EN 16247"""
    measure_id: str
    title: str
    description: str
    category: str                  # kategória opatrenia
    energy_savings: Dict[EnergyCarrier, float]  # úspory po nosičoch
    investment_cost: float         # € investičné náklady
    annual_savings: float          # € ročné úspory
    simple_payback: float          # roky
    technical_lifetime: int        # roky technická životnosť
    
    # Hodnotenie kvality
    data_quality: str = "estimated"  # estimated, calculated, measured
    measurement_verification: bool = False
    
    # Implementačné detaily
    implementation_complexity: str = "medium"  # low, medium, high
    prerequisites: List[str] = field(default_factory=list)
    risks_barriers: List[str] = field(default_factory=list)
    
    # Finančná analýza
    npv: Optional[float] = None
    irr: Optional[float] = None

    @property
    def total_energy_savings(self) -> float:
        """Celkové energetické úspory"""
        return sum(self.energy_savings.values())

    @property
    def cost_effectiveness(self) -> float:
        """Nákladová efektívnosť €/kWh"""
        if self.total_energy_savings > 0:
            return self.investment_cost / self.total_energy_savings
        return float('inf')

class EN16247AuditProcess:
    """Hlavná trieda pre proces auditu podľa EN 16247"""
    
    def __init__(self, audit_type: AuditType):
        """Inicializácia audit procesu"""
        self.audit_type = audit_type
        self.audit_id = None
        self.current_phase = None
        self.audit_data = {}
        
        # Fázy auditu podľa EN 16247
        self.phases = [
            "preliminary_contact",    # Úvodný kontakt
            "opening_meeting",       # Úvodné stretnutie  
            "data_collection",       # Zber dát
            "field_visit",          # Terénna prehliadka
            "analysis",             # Analýza
            "reporting"             # Reporting
        ]
        
    def start_audit(self, audit_id: str, client_info: Dict[str, Any]) -> Dict[str, Any]:
        """Spustenie auditu"""
        self.audit_id = audit_id
        self.current_phase = "preliminary_contact"
        
        self.audit_data = {
            'audit_id': audit_id,
            'audit_type': self.audit_type.value,
            'client_info': client_info,
            'start_date': datetime.now().isoformat(),
            'auditor_info': None,
            'scope_definition': None,
            'energy_data': {},
            'systems_inventory': {},
            'measurements': {},
            'analysis_results': {},
            'measures': {},
            'report_generated': False
        }
        
        return {
            'audit_id': audit_id,
            'current_phase': self.current_phase,
            'next_steps': self._get_phase_requirements("preliminary_contact")
        }
    
    def phase_1_preliminary_contact(self, auditor_info: AuditorQualification, 
                                   scope_definition: Dict[str, Any]) -> Dict[str, Any]:
        """Fáza 1: Úvodný kontakt a definovanie rozsahu"""
        
        # Validácia kvalifikácie audítora
        if not auditor_info.is_qualified_for_audit_type(self.audit_type):
            return {
                'success': False,
                'error': 'Audítor nemá dostatočnú kvalifikáciu pre tento typ auditu'
            }
        
        self.audit_data['auditor_info'] = auditor_info
        self.audit_data['scope_definition'] = scope_definition
        self.current_phase = "opening_meeting"
        
        # Príprava štruktúry pre zber dát
        data_structure = self._prepare_data_collection_structure()
        
        return {
            'success': True,
            'current_phase': self.current_phase,
            'data_collection_structure': data_structure,
            'next_steps': self._get_phase_requirements("opening_meeting")
        }
    
    def phase_2_opening_meeting(self, meeting_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fáza 2: Úvodné stretnutie a plánovanie"""
        
        required_topics = [
            'audit_objectives',      # Ciele auditu
            'system_boundaries',     # Systémové hranice
            'data_availability',     # Dostupnosť dát
            'measurement_plan',      # Plán meraní
            'timeline',             # Časový harmonogram
            'reporting_requirements' # Požiadavky na reporting
        ]
        
        # Kontrola či boli pokryté všetky potrebné témy
        missing_topics = [topic for topic in required_topics if topic not in meeting_data]
        if missing_topics:
            return {
                'success': False,
                'error': f'Chýbajú informácie o: {", ".join(missing_topics)}'
            }
        
        self.audit_data['opening_meeting'] = meeting_data
        self.current_phase = "data_collection"
        
        return {
            'success': True,
            'current_phase': self.current_phase,
            'next_steps': self._get_phase_requirements("data_collection")
        }
    
    def phase_3_data_collection(self, energy_data: List[EnergyConsumptionData],
                               systems_data: List[EnergySystem]) -> Dict[str, Any]:
        """Fáza 3: Zber energetických dát"""
        
        # Validácia kvality dát
        validation_results = self._validate_energy_data(energy_data)
        if not validation_results['valid']:
            return {
                'success': False,
                'error': 'Neplatné energetické dáta',
                'validation_errors': validation_results['errors']
            }
        
        # Uloženie dát
        self.audit_data['energy_data'] = {
            'consumption_data': energy_data,
            'validation_results': validation_results
        }
        self.audit_data['systems_inventory'] = systems_data
        
        # Analýza úplnosti dát
        completeness = self._assess_data_completeness(energy_data, systems_data)
        
        self.current_phase = "field_visit"
        
        return {
            'success': True,
            'current_phase': self.current_phase,
            'data_completeness': completeness,
            'next_steps': self._get_phase_requirements("field_visit")
        }
    
    def phase_4_field_visit(self, visit_data: Dict[str, Any],
                           measurements: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Fáza 4: Terénna prehliadka a merania"""
        
        # Dokumentácia prehliadky
        required_documentation = [
            'visual_inspection',     # Vizuálna inšpekcia
            'operational_practices', # Prevádzkové praktiky
            'maintenance_status',    # Stav údržby
            'control_systems',       # Riadiace systémy
            'energy_flows'          # Energetické toky
        ]
        
        # Validácia meraní
        measurement_validation = self._validate_measurements(measurements)
        
        self.audit_data['field_visit'] = visit_data
        self.audit_data['measurements'] = {
            'data': measurements,
            'validation': measurement_validation
        }
        
        self.current_phase = "analysis"
        
        return {
            'success': True,
            'current_phase': self.current_phase,
            'measurement_validation': measurement_validation,
            'next_steps': self._get_phase_requirements("analysis")
        }
    
    def phase_5_analysis(self) -> Dict[str, Any]:
        """Fáza 5: Energetická analýza a identifikácia opatrení"""
        
        # Výpočet EnPI (Energy Performance Indicators)
        enpi_results = self._calculate_energy_performance_indicators()
        
        # Identifikácia opatrení energetickej efektívnosti
        efficiency_measures = self._identify_efficiency_measures()
        
        # Hodnotenie a prioritizácia opatrení
        prioritized_measures = self._prioritize_measures(efficiency_measures)
        
        # Finančná analýza
        financial_analysis = self._perform_financial_analysis(prioritized_measures)
        
        self.audit_data['analysis_results'] = {
            'enpi_results': enpi_results,
            'efficiency_measures': efficiency_measures,
            'prioritized_measures': prioritized_measures,
            'financial_analysis': financial_analysis
        }
        
        self.current_phase = "reporting"
        
        return {
            'success': True,
            'current_phase': self.current_phase,
            'analysis_summary': {
                'total_measures': len(efficiency_measures),
                'total_savings_potential': sum(m.annual_savings for m in efficiency_measures),
                'total_investment': sum(m.investment_cost for m in efficiency_measures)
            },
            'next_steps': self._get_phase_requirements("reporting")
        }
    
    def phase_6_reporting(self, report_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Fáza 6: Generovanie reportu podľa EN 16247"""
        
        # Generovanie štandardizovaného reportu
        report = self._generate_en16247_report(report_requirements)
        
        # Validácia reportu proti požiadavkám normy
        report_validation = self._validate_report_compliance(report)
        
        self.audit_data['report_generated'] = True
        self.audit_data['final_report'] = report
        
        return {
            'success': True,
            'report': report,
            'compliance_validation': report_validation,
            'audit_completed': True
        }
    
    def _prepare_data_collection_structure(self) -> Dict[str, Any]:
        """Príprava štruktúry pre zber dát podľa typu auditu"""
        
        base_structure = {
            'facility_information': {
                'name': str,
                'address': str,
                'floor_area': float,
                'number_of_occupants': int,
                'operating_hours': str,
                'climate_zone': str
            },
            'energy_consumption': {
                'carriers': [carrier.value for carrier in EnergyCarrier],
                'measurement_methods': [method.value for method in MeasurementMethod],
                'historical_data_years': int,
                'utility_bills': bool
            }
        }
        
        # Špecializácia podľa typu auditu
        if self.audit_type == AuditType.BUILDING:
            base_structure.update({
                'building_envelope': {
                    'construction_year': int,
                    'renovation_history': str,
                    'thermal_characteristics': dict
                },
                'hvac_systems': {
                    'heating_system': dict,
                    'cooling_system': dict,
                    'ventilation_system': dict
                },
                'lighting_systems': dict,
                'domestic_hot_water': dict
            })
            
        elif self.audit_type == AuditType.INDUSTRY:
            base_structure.update({
                'production_processes': {
                    'main_products': list,
                    'production_volume': float,
                    'process_description': str
                },
                'industrial_equipment': {
                    'motors': list,
                    'compressors': list,
                    'boilers': list,
                    'other_equipment': list
                }
            })
        
        return base_structure
    
    def _validate_energy_data(self, energy_data: List[EnergyConsumptionData]) -> Dict[str, Any]:
        """Validácia kvality energetických dát"""
        
        errors = []
        warnings = []
        
        for i, data in enumerate(energy_data):
            # Kontrola úplnosti dát
            if data.annual_consumption <= 0:
                errors.append(f"Záznam {i}: Neplatná spotreba energie")
            
            if data.unit_cost <= 0:
                warnings.append(f"Záznam {i}: Nízka alebo nulová cena energie")
            
            # Kontrola metódy merania
            if data.measurement_method in [MeasurementMethod.ESTIMATION, MeasurementMethod.CALCULATION]:
                if data.measurement_uncertainty is None:
                    warnings.append(f"Záznam {i}: Chýba údaj o presnosti odhadu/výpočtu")
        
        # Kontrola pokrytia energetických nosičov
        covered_carriers = set(data.energy_carrier for data in energy_data)
        if EnergyCarrier.ELECTRICITY not in covered_carriers:
            warnings.append("Chýbajú údaje o spotrebe elektrickej energie")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'data_quality_score': self._calculate_data_quality_score(energy_data)
        }
    
    def _calculate_data_quality_score(self, energy_data: List[EnergyConsumptionData]) -> float:
        """Výpočet skóre kvality dát (0-100)"""
        
        if not energy_data:
            return 0
        
        quality_factors = []
        
        for data in energy_data:
            factor_score = 0
            
            # Metóda merania (40% váha)
            method_scores = {
                MeasurementMethod.CONTINUOUS: 40,
                MeasurementMethod.SHORT_TERM: 30,
                MeasurementMethod.SPOT: 20,
                MeasurementMethod.CALCULATION: 15,
                MeasurementMethod.ESTIMATION: 10
            }
            factor_score += method_scores.get(data.measurement_method, 0)
            
            # Presnosť dát (30% váha)
            if data.measurement_uncertainty is not None:
                if data.measurement_uncertainty <= 5:
                    factor_score += 30
                elif data.measurement_uncertainty <= 10:
                    factor_score += 25
                elif data.measurement_uncertainty <= 20:
                    factor_score += 20
                else:
                    factor_score += 10
            else:
                factor_score += 15  # stredná hodnota ak nie je špecifikované
            
            # Úplnosť dát (30% váha)
            completeness_score = 0
            if data.peak_demand is not None:
                completeness_score += 10
            if data.load_profile:
                completeness_score += 10
            if data.seasonal_variation:
                completeness_score += 10
            factor_score += completeness_score
            
            quality_factors.append(factor_score)
        
        return sum(quality_factors) / len(quality_factors) if quality_factors else 0
    
    def _assess_data_completeness(self, energy_data: List[EnergyConsumptionData],
                                 systems_data: List[EnergySystem]) -> Dict[str, Any]:
        """Posúdenie úplnosti dát"""
        
        completeness = {
            'energy_carriers_coverage': 0,
            'systems_documentation': 0,
            'measurement_data': 0,
            'overall_score': 0
        }
        
        # Pokrytie energetických nosičov
        total_carriers = len(EnergyCarrier)
        covered_carriers = len(set(data.energy_carrier for data in energy_data))
        completeness['energy_carriers_coverage'] = (covered_carriers / total_carriers) * 100
        
        # Dokumentácia systémov
        documented_systems = sum(1 for system in systems_data if system.efficiency is not None)
        completeness['systems_documentation'] = (documented_systems / len(systems_data) * 100) if systems_data else 0
        
        # Kvalita meraní
        measured_data = sum(1 for data in energy_data 
                          if data.measurement_method in [MeasurementMethod.CONTINUOUS, MeasurementMethod.SHORT_TERM])
        completeness['measurement_data'] = (measured_data / len(energy_data) * 100) if energy_data else 0
        
        # Celkové skóre
        completeness['overall_score'] = (
            completeness['energy_carriers_coverage'] * 0.4 +
            completeness['systems_documentation'] * 0.3 +
            completeness['measurement_data'] * 0.3
        )
        
        return completeness
    
    def _validate_measurements(self, measurements: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validácia výsledkov meraní"""
        
        validation = {
            'valid_measurements': 0,
            'calibration_status': 'unknown',
            'measurement_uncertainty': None,
            'recommendations': []
        }
        
        for measurement in measurements:
            # Kontrola kalibrácie meracích prístrojov
            if measurement.get('calibration_date'):
                validation['calibration_status'] = 'calibrated'
            
            # Kontrola presnosti
            if measurement.get('uncertainty'):
                if validation['measurement_uncertainty'] is None:
                    validation['measurement_uncertainty'] = []
                validation['measurement_uncertainty'].append(measurement['uncertainty'])
        
        validation['valid_measurements'] = len(measurements)
        
        # Odporúčania na zlepšenie
        if validation['calibration_status'] == 'unknown':
            validation['recommendations'].append("Overiť kalibráciu meracích prístrojov")
        
        return validation
    
    def _calculate_energy_performance_indicators(self) -> List[EnergyPerformanceIndicator]:
        """Výpočet ukazovateľov energetickej výkonnosti"""
        
        indicators = []
        energy_data = self.audit_data.get('energy_data', {}).get('consumption_data', [])
        
        if energy_data:
            # Celková spotreba energie
            total_consumption = sum(data.annual_consumption for data in energy_data)
            indicators.append(EnergyPerformanceIndicator(
                name="Celková spotreba energie",
                value=total_consumption,
                unit="kWh/rok",
                reference_period="ročne"
            ))
            
            # Náklady na energiu
            total_cost = sum(data.annual_cost for data in energy_data)
            indicators.append(EnergyPerformanceIndicator(
                name="Celkové náklady na energiu",
                value=total_cost,
                unit="€/rok",
                reference_period="ročne"
            ))
            
            # Rozloženie podľa nosičov
            carrier_breakdown = {}
            for data in energy_data:
                carrier = data.energy_carrier.value
                if carrier not in carrier_breakdown:
                    carrier_breakdown[carrier] = 0
                carrier_breakdown[carrier] += data.annual_consumption
            
            for carrier, consumption in carrier_breakdown.items():
                indicators.append(EnergyPerformanceIndicator(
                    name=f"Spotreba - {carrier}",
                    value=consumption,
                    unit="kWh/rok",
                    reference_period="ročne"
                ))
        
        return indicators
    
    def _identify_efficiency_measures(self) -> List[EnergyEfficiencyMeasure]:
        """Identifikácia opatrení energetickej efektívnosti"""
        
        measures = []
        
        # Štandardné opatrenia podľa typu auditu
        if self.audit_type == AuditType.BUILDING:
            measures.extend(self._identify_building_measures())
        elif self.audit_type == AuditType.INDUSTRY:
            measures.extend(self._identify_industrial_measures())
        elif self.audit_type == AuditType.TRANSPORT:
            measures.extend(self._identify_transport_measures())
        
        return measures
    
    def _identify_building_measures(self) -> List[EnergyEfficiencyMeasure]:
        """Identifikácia opatrení pre budovy"""
        
        measures = []
        
        # Štandardné opatrenia pre budovy
        standard_measures = [
            {
                'id': 'BLD-01',
                'title': 'Zateplenie obvodového plášťa',
                'description': 'Zateplenie obvodových stien, strechy a podlahy',
                'category': 'Stavebné opatrenia',
                'energy_savings': {EnergyCarrier.NATURAL_GAS: 8000, EnergyCarrier.ELECTRICITY: 500},
                'investment_cost': 15000,
                'annual_savings': 800,
                'simple_payback': 18.75,
                'technical_lifetime': 30
            },
            {
                'id': 'BLD-02', 
                'title': 'Výmena okien a dverí',
                'description': 'Inštalácia energeticky efektívnych okien a dverí',
                'category': 'Stavebné opatrenia',
                'energy_savings': {EnergyCarrier.NATURAL_GAS: 3000, EnergyCarrier.ELECTRICITY: 200},
                'investment_cost': 8000,
                'annual_savings': 400,
                'simple_payback': 20,
                'technical_lifetime': 25
            },
            {
                'id': 'BLD-03',
                'title': 'Modernizácia vykurovacieho systému', 
                'description': 'Výmena kotla za kondenzačný kotol s reguláciou',
                'category': 'Technické systémy',
                'energy_savings': {EnergyCarrier.NATURAL_GAS: 5000},
                'investment_cost': 12000,
                'annual_savings': 600,
                'simple_payback': 20,
                'technical_lifetime': 15
            },
            {
                'id': 'BLD-04',
                'title': 'LED osvetlenie',
                'description': 'Výmena osvetlenia za LED s inteligentným riadením',
                'category': 'Elektrické systémy',
                'energy_savings': {EnergyCarrier.ELECTRICITY: 2000},
                'investment_cost': 3000,
                'annual_savings': 300,
                'simple_payback': 10,
                'technical_lifetime': 15
            }
        ]
        
        for measure_data in standard_measures:
            measures.append(EnergyEfficiencyMeasure(
                measure_id=measure_data['id'],
                title=measure_data['title'],
                description=measure_data['description'],
                category=measure_data['category'],
                energy_savings=measure_data['energy_savings'],
                investment_cost=measure_data['investment_cost'],
                annual_savings=measure_data['annual_savings'],
                simple_payback=measure_data['simple_payback'],
                technical_lifetime=measure_data['technical_lifetime'],
                data_quality="estimated"
            ))
        
        return measures
    
    def _identify_industrial_measures(self) -> List[EnergyEfficiencyMeasure]:
        """Identifikácia opatrení pre priemysel"""
        
        measures = []
        
        # Štandardné priemyselné opatrenia
        standard_measures = [
            {
                'id': 'IND-01',
                'title': 'Optimalizácia kompresorových systémov',
                'description': 'Riadenie kompresora podľa potreby, oprava únikov',
                'category': 'Strojné zariadenia',
                'energy_savings': {EnergyCarrier.ELECTRICITY: 15000},
                'investment_cost': 5000,
                'annual_savings': 2000,
                'simple_payback': 2.5,
                'technical_lifetime': 10
            },
            {
                'id': 'IND-02',
                'title': 'Rekuperácia odpadového tepla',
                'description': 'Využitie odpadového tepla z procesov na predohrev',
                'category': 'Energetické toky',
                'energy_savings': {EnergyCarrier.NATURAL_GAS: 25000},
                'investment_cost': 20000,
                'annual_savings': 2500,
                'simple_payback': 8,
                'technical_lifetime': 15
            },
            {
                'id': 'IND-03',
                'title': 'Frekvenčné meniče pre motory',
                'description': 'Inštalácia frekvenčných meničov pre riadenie otáčok',
                'category': 'Strojné zariadenia',
                'energy_savings': {EnergyCarrier.ELECTRICITY: 20000},
                'investment_cost': 15000,
                'annual_savings': 3000,
                'simple_payback': 5,
                'technical_lifetime': 12
            }
        ]
        
        for measure_data in standard_measures:
            measures.append(EnergyEfficiencyMeasure(
                measure_id=measure_data['id'],
                title=measure_data['title'],
                description=measure_data['description'],
                category=measure_data['category'],
                energy_savings=measure_data['energy_savings'],
                investment_cost=measure_data['investment_cost'],
                annual_savings=measure_data['annual_savings'],
                simple_payback=measure_data['simple_payback'],
                technical_lifetime=measure_data['technical_lifetime'],
                data_quality="estimated"
            ))
        
        return measures
    
    def _identify_transport_measures(self) -> List[EnergyEfficiencyMeasure]:
        """Identifikácia opatrení pre dopravu"""
        
        measures = []
        
        # Základné opatrenia pre dopravu
        measures.append(EnergyEfficiencyMeasure(
            measure_id="TRA-01",
            title="Optimalizácia trás a logistiky",
            description="Optimalizácia prepravných trás a plánovanie",
            category="Logistika", 
            energy_savings={EnergyCarrier.HEATING_OIL: 5000},
            investment_cost=2000,
            annual_savings=600,
            simple_payback=3.33,
            technical_lifetime=5,
            data_quality="estimated"
        ))
        
        return measures
    
    def _prioritize_measures(self, measures: List[EnergyEfficiencyMeasure]) -> List[EnergyEfficiencyMeasure]:
        """Prioritizácia opatrení podľa viacerých kritérií"""
        
        # Výpočet skóre pre každé opatrenie
        for measure in measures:
            # Kritériá hodnotenia (váhované skóre)
            payback_score = max(0, (10 - measure.simple_payback) / 10 * 30)  # 30% váha
            savings_score = min(30, measure.annual_savings / 100)  # 30% váha  
            implementation_score = {'low': 25, 'medium': 15, 'high': 5}.get(measure.implementation_complexity, 15)  # 25% váha
            data_quality_score = {'measured': 15, 'calculated': 10, 'estimated': 5}.get(measure.data_quality, 5)  # 15% váha
            
            measure.priority_score = payback_score + savings_score + implementation_score + data_quality_score
        
        # Zoradenie podľa skóre
        return sorted(measures, key=lambda m: m.priority_score, reverse=True)
    
    def _perform_financial_analysis(self, measures: List[EnergyEfficiencyMeasure]) -> Dict[str, Any]:
        """Finančná analýza opatrení"""
        
        total_investment = sum(m.investment_cost for m in measures)
        total_savings = sum(m.annual_savings for m in measures)
        
        # Portfolio analýza
        portfolio_payback = total_investment / total_savings if total_savings > 0 else float('inf')
        
        # NPV analýza (zjednodušene s 5% diskontnou sazbou)
        discount_rate = 0.05
        portfolio_npv = -total_investment
        for year in range(1, 21):  # 20 ročná analýza
            portfolio_npv += total_savings / ((1 + discount_rate) ** year)
        
        return {
            'total_investment': total_investment,
            'total_annual_savings': total_savings,
            'portfolio_payback': portfolio_payback,
            'portfolio_npv': portfolio_npv,
            'measures_count': len(measures)
        }
    
    def _generate_en16247_report(self, report_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Generovanie reportu podľa EN 16247"""
        
        report = {
            'metadata': {
                'report_id': f"EN16247-{self.audit_id}",
                'generated_date': datetime.now().isoformat(),
                'auditor': self.audit_data.get('auditor_info'),
                'standard_version': 'STN EN 16247:2012',
                'audit_type': self.audit_type.value
            },
            'executive_summary': self._generate_executive_summary(),
            'audit_scope_and_boundaries': self.audit_data.get('scope_definition', {}),
            'data_collection_methodology': self._describe_methodology(),
            'energy_review_results': self.audit_data.get('analysis_results', {}).get('enpi_results', []),
            'identified_measures': self.audit_data.get('analysis_results', {}).get('prioritized_measures', []),
            'financial_analysis': self.audit_data.get('analysis_results', {}).get('financial_analysis', {}),
            'implementation_recommendations': self._generate_implementation_recommendations(),
            'quality_assurance': self._generate_quality_statement(),
            'appendices': {
                'energy_data': self.audit_data.get('energy_data'),
                'measurement_results': self.audit_data.get('measurements'),
                'calculations': {}
            }
        }
        
        return report
    
    def _generate_executive_summary(self) -> Dict[str, Any]:
        """Generovanie executive summary"""
        
        analysis_results = self.audit_data.get('analysis_results', {})
        financial_analysis = analysis_results.get('financial_analysis', {})
        measures = analysis_results.get('prioritized_measures', [])
        
        return {
            'audit_objectives': "Identifikácia opatrení energetickej efektívnosti",
            'key_findings': [
                f"Identifikované {len(measures)} opatrenia energetickej efektívnosti",
                f"Celkový potenciál úspor: {financial_analysis.get('total_annual_savings', 0):,.0f} €/rok",
                f"Potrebná investícia: {financial_analysis.get('total_investment', 0):,.0f} €",
                f"Doba návratnosti portfólia: {financial_analysis.get('portfolio_payback', 0):.1f} rokov"
            ],
            'main_recommendations': [measure.title for measure in measures[:5]],  # Top 5
            'implementation_priorities': self._classify_measures_by_priority(measures)
        }
    
    def _describe_methodology(self) -> Dict[str, Any]:
        """Opis metodológie zberu dát"""
        
        return {
            'data_sources': [
                'Faktúry za energiu za posledné 3 roky',
                'Terénna prehliadka zariadenia',
                'Rozhovory s prevádzkovým personálom',
                'Merania vybraných parametrov'
            ],
            'measurement_equipment': 'Kalibrované meracie prístroje',
            'analysis_methods': 'Podľa STN EN 16247',
            'data_quality_assessment': self.audit_data.get('energy_data', {}).get('validation_results', {})
        }
    
    def _generate_implementation_recommendations(self) -> List[Dict[str, Any]]:
        """Odporúčania pre implementáciu"""
        
        return [
            {
                'phase': 'Okamžité opatrenia (0-6 mesiacov)',
                'measures': ['Optimalizácia prevádzky existujúcich systémov'],
                'investment': 'Nízka',
                'priority': 'Vysoká'
            },
            {
                'phase': 'Krátkodobé opatrenia (6-18 mesiacov)',
                'measures': ['Výmena neefektívnych zariadení'],
                'investment': 'Stredná',
                'priority': 'Stredná'
            },
            {
                'phase': 'Dlhodobé opatrenia (1-5 rokov)',
                'measures': ['Komplexná renovácia systémov'],
                'investment': 'Vysoká', 
                'priority': 'Nízka'
            }
        ]
    
    def _generate_quality_statement(self) -> Dict[str, Any]:
        """Vyhlásenie o kvalite auditu"""
        
        return {
            'auditor_qualifications': {
                'certified': True,
                'experience_years': self.audit_data.get('auditor_info').experience_years if self.audit_data.get('auditor_info') else 0,
                'continuous_education': 'Aktuálne'
            },
            'standard_compliance': 'STN EN 16247:2012',
            'data_quality_score': self.audit_data.get('energy_data', {}).get('validation_results', {}).get('data_quality_score', 0),
            'limitations': [
                'Analýza založená na dostupných historických dátach',
                'Odhad úspor založený na typických hodnotách'
            ]
        }
    
    def _classify_measures_by_priority(self, measures: List[EnergyEfficiencyMeasure]) -> Dict[str, List[str]]:
        """Klasifikácia opatrení podľa priority"""
        
        high_priority = [m.title for m in measures if getattr(m, 'priority_score', 0) > 60]
        medium_priority = [m.title for m in measures if 30 <= getattr(m, 'priority_score', 0) <= 60]
        low_priority = [m.title for m in measures if getattr(m, 'priority_score', 0) < 30]
        
        return {
            'high_priority': high_priority,
            'medium_priority': medium_priority,
            'low_priority': low_priority
        }
    
    def _validate_report_compliance(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """Validácia súladu reportu s EN 16247"""
        
        required_sections = [
            'metadata',
            'executive_summary', 
            'audit_scope_and_boundaries',
            'data_collection_methodology',
            'energy_review_results',
            'identified_measures',
            'financial_analysis',
            'implementation_recommendations'
        ]
        
        missing_sections = [section for section in required_sections if section not in report]
        
        return {
            'compliant': len(missing_sections) == 0,
            'missing_sections': missing_sections,
            'completeness_score': (len(required_sections) - len(missing_sections)) / len(required_sections) * 100
        }
    
    def _get_phase_requirements(self, phase: str) -> List[str]:
        """Požiadavky pre danú fázu"""
        
        requirements = {
            'preliminary_contact': [
                'Definovať ciele auditu',
                'Stanoviť rozsah a hranice',
                'Overiť kvalifikácie audítora',
                'Pripraviť zmluvu o audite'
            ],
            'opening_meeting': [
                'Prezentovať ciele a rozsah',
                'Dohodnúť plán zberu dát',
                'Stanoviť časový harmonogram',
                'Identifikovať kľúčových kontaktov'
            ],
            'data_collection': [
                'Zozbierať historické údaje o spotrebe',
                'Zdokumentovať energetické systémy',
                'Získať pôdorysy a technickú dokumentáciu',
                'Pripraviť plán meraní'
            ],
            'field_visit': [
                'Vykonať vizuálnu inšpekciu',
                'Realizovať plánované merania',
                'Dokumentovať prevádzkové praktiky',
                'Identifikovať potenciálne opatrenia'
            ],
            'analysis': [
                'Analyzovať energetické dáta',
                'Vypočítať EnPI',
                'Vyhodnotiť účinnosť systémov',
                'Kvantifikovať potenciálne úspory'
            ],
            'reporting': [
                'Pripraviť draft reportu',
                'Overiť výpočty a odporúčania',
                'Prezentovať výsledky klientovi',
                'Finalizovať report'
            ]
        }
        
        return requirements.get(phase, [])

def get_en16247_audit_process(audit_type: AuditType) -> EN16247AuditProcess:
    """Factory funkcia pre EN 16247 audit proces"""
    return EN16247AuditProcess(audit_type)

# Pomocné funkcie pre prácu s EN 16247
def create_sample_auditor_qualification() -> AuditorQualification:
    """Vytvorenie vzorového audítora"""
    return AuditorQualification(
        name="Ing. Energetický Audítor",
        education_level="Vysokoškolské vzdelanie - energetika",
        experience_years=5,
        certification_number="EA-2024-001",
        certification_body="Slovenská komora energetických audítorov",
        specialized_areas=["Budovy", "Priemysel"],
        continuous_education_hours=40
    )

def create_sample_energy_data() -> List[EnergyConsumptionData]:
    """Vytvorenie vzorových energetických dát"""
    return [
        EnergyConsumptionData(
            energy_carrier=EnergyCarrier.ELECTRICITY,
            annual_consumption=25000,
            unit_cost=0.15,
            measurement_method=MeasurementMethod.CONTINUOUS,
            measurement_period="2023",
            weather_correction=False,
            peak_demand=45.0,
            measurement_uncertainty=2.0
        ),
        EnergyConsumptionData(
            energy_carrier=EnergyCarrier.NATURAL_GAS,
            annual_consumption=45000,
            unit_cost=0.08,
            measurement_method=MeasurementMethod.SHORT_TERM,
            measurement_period="2023",
            weather_correction=True,
            measurement_uncertainty=5.0
        ),
        EnergyConsumptionData(
            energy_carrier=EnergyCarrier.DISTRICT_HEATING,
            annual_consumption=15000,
            unit_cost=0.12,
            measurement_method=MeasurementMethod.CALCULATION,
            measurement_period="2023",
            measurement_uncertainty=10.0
        )
    ]

if __name__ == "__main__":
    # Ukážka použitia STN EN 16247 implementácie
    
    print("=== STN EN 16247 ENERGY AUDIT DEMO ===")
    
    # Vytvorenie audit procesu pre budovy
    audit_process = get_en16247_audit_process(AuditType.BUILDING)
    
    # Spustenie auditu
    client_info = {
        'name': 'Demo Building Ltd.',
        'address': 'Testovacia 123, Bratislava',
        'contact_person': 'Ing. Manager',
        'building_type': 'Office building'
    }
    
    audit_start = audit_process.start_audit('DEMO-EN16247-001', client_info)
    print(f"Audit spustený: {audit_start['audit_id']}")
    print(f"Aktuálna fáza: {audit_start['current_phase']}")
    
    # Fáza 1: Úvodný kontakt
    auditor = create_sample_auditor_qualification()
    scope_definition = {
        'audit_type': AuditType.BUILDING,
        'audit_scope': AuditScope.COMPREHENSIVE,
        'system_boundaries': 'Celá budova vrátane všetkých systémov',
        'expected_duration': '4 týždne'
    }
    
    phase1_result = audit_process.phase_1_preliminary_contact(auditor, scope_definition)
    print(f"\nFáza 1 dokončená: {phase1_result['success']}")
    
    # Fáza 2: Úvodné stretnutie
    meeting_data = {
        'audit_objectives': ['Identifikácia úspor energie', 'Zníženie nákladov'],
        'system_boundaries': 'HVAC, osvetlenie, kancelárske zariadenia',
        'data_availability': 'Faktúry za 3 roky dostupné',
        'measurement_plan': 'Meranie spotreby hlavných systémov',
        'timeline': '4 týždne',
        'reporting_requirements': 'Detailný report s odporúčaniami'
    }
    
    phase2_result = audit_process.phase_2_opening_meeting(meeting_data)
    print(f"Fáza 2 dokončená: {phase2_result['success']}")
    
    # Fáza 3: Zber dát
    energy_data = create_sample_energy_data()
    systems_data = [
        EnergySystem(
            system_id="SYS-001",
            system_name="HVAC System",
            system_type="Heat pump",
            energy_input=energy_data,
            efficiency=85.0,
            capacity=50.0,
            age_years=8,
            operating_hours_annual=2000
        )
    ]
    
    phase3_result = audit_process.phase_3_data_collection(energy_data, systems_data)
    print(f"Fáza 3 dokončená: {phase3_result['success']}")
    print(f"Kvalita dát: {phase3_result['data_completeness']['overall_score']:.1f}%")
    
    # Fáza 4: Terénna prehliadka
    visit_data = {
        'visual_inspection': 'Kompletná inšpekcia zariadenia',
        'operational_practices': 'Štandardné prevádzkové postupy',
        'maintenance_status': 'Pravidelná údržba',
        'control_systems': 'Automatické riadenie HVAC',
        'energy_flows': 'Zmapované všetky hlavné toky'
    }
    
    measurements = [
        {
            'parameter': 'Elektrická spotreba',
            'value': 45.2,
            'unit': 'kW',
            'calibration_date': '2024-01-15',
            'uncertainty': 2.0
        }
    ]
    
    phase4_result = audit_process.phase_4_field_visit(visit_data, measurements)
    print(f"Fáza 4 dokončená: {phase4_result['success']}")
    
    # Fáza 5: Analýza
    phase5_result = audit_process.phase_5_analysis()
    print(f"Fáza 5 dokončená: {phase5_result['success']}")
    print(f"Identifikované opatrenia: {phase5_result['analysis_summary']['total_measures']}")
    print(f"Potenciálne úspory: {phase5_result['analysis_summary']['total_savings_potential']:,.0f} €/rok")
    
    # Fáza 6: Reporting
    report_requirements = {
        'format': 'PDF',
        'language': 'Slovak',
        'detail_level': 'Comprehensive',
        'appendices': True
    }
    
    phase6_result = audit_process.phase_6_reporting(report_requirements)
    print(f"Fáza 6 dokončená: {phase6_result['success']}")
    print(f"Súlad s normou: {phase6_result['compliance_validation']['completeness_score']:.1f}%")
    
    print("\n=== AUDIT PODĽA STN EN 16247 ÚSPEŠNE DOKONČENÝ ===")