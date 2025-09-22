#!/usr/bin/env python3
"""
Comprehensive Data Collection System
Komplexný systém zberu dát integrujúci všetky poznatky z PDF 1,2,3 a STN EN 16247
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Union, Tuple
from enum import Enum
from datetime import datetime, date, timedelta
import json
import logging
from pathlib import Path

# Import našich modulov
try:
    from .stn_en_16247 import AuditType, EnergyCarrier, MeasurementMethod, AuditorQualification
    from .energy_calculations import get_energy_calculator
    from .thermal_analysis import ConstructionType
    from .building_diagnostics import DiagnosticMethod, SeverityLevel
    from .config import BUILDING_TYPES, HEATING_TYPES
except ImportError:
    from stn_en_16247 import AuditType, EnergyCarrier, MeasurementMethod, AuditorQualification
    from energy_calculations import get_energy_calculator
    from thermal_analysis import ConstructionType
    from building_diagnostics import DiagnosticMethod, SeverityLevel
    from config import BUILDING_TYPES, HEATING_TYPES

class DataQualityLevel(Enum):
    """Úrovne kvality dát"""
    MEASURED = "measured"           # Merané dáta
    CALCULATED = "calculated"       # Vypočítané
    ESTIMATED = "estimated"         # Odhadované  
    ASSUMED = "assumed"             # Predpokladané

class ValidationStatus(Enum):
    """Status validácie dát"""
    VALID = "valid"
    WARNING = "warning"
    ERROR = "error"
    INCOMPLETE = "incomplete"

@dataclass
class DataSource:
    """Zdroj dát"""
    source_type: str                # typ zdroja
    description: str                # popis
    reliability: float              # spoľahlivosť 0-1
    date_collected: Optional[datetime] = None
    collected_by: Optional[str] = None
    validation_method: Optional[str] = None

@dataclass
class MeasurementPoint:
    """Meracie miesto"""
    point_id: str
    location: str
    parameter: str
    unit: str
    measurement_method: MeasurementMethod
    accuracy: Optional[float] = None    # %
    calibration_date: Optional[date] = None
    measurement_range: Optional[Tuple[float, float]] = None

@dataclass
class BuildingGeneralInfo:
    """Základné informácie o budove - rozšírené podľa všetkých PDF"""
    # Základné údaje
    building_name: str
    building_address: str
    building_type: str              # z BUILDING_TYPES
    
    # Geometrické parametre
    total_floor_area: float         # m² celková plocha
    heated_floor_area: float        # m² vykurovaná plocha
    conditioned_volume: float       # m³ klimatizovaný objem
    building_height: float          # m výška budovy
    number_of_floors: int
    
    # Historické údaje
    construction_year: int
    major_renovations: List[Dict[str, Any]] = field(default_factory=list)
    
    # Prevádzkové údaje
    occupancy_profile: Dict[str, Any] = field(default_factory=dict)
    operating_schedule: Dict[str, Any] = field(default_factory=dict)
    typical_occupancy: int = 0      # typický počet osôb
    
    # Klimatické údaje
    climate_zone: str = "Dfb"       # Köppen klasifikácia pre Slovensko
    heating_degree_days: Optional[float] = None    # HDD
    cooling_degree_days: Optional[float] = None    # CDD
    
    # Regulačné údaje
    building_permits: List[str] = field(default_factory=list)
    energy_label: Optional[str] = None
    
    # Zdroj dát a kvalita
    data_sources: List[DataSource] = field(default_factory=list)
    data_quality: DataQualityLevel = DataQualityLevel.ESTIMATED

@dataclass
class BuildingEnvelope:
    """Obálka budovy - detailná charakterizácia"""
    # Celkové parametre
    total_envelope_area: float      # m² celková plocha obálky
    window_to_wall_ratio: float     # pomer okien k stenám
    thermal_bridge_coefficient: float = 0.05  # súčiniteľ tepelných mostíkov
    
    # Komponenty obálky
    walls: List[Dict[str, Any]] = field(default_factory=list)
    roof: List[Dict[str, Any]] = field(default_factory=list)  
    floors: List[Dict[str, Any]] = field(default_factory=list)
    windows: List[Dict[str, Any]] = field(default_factory=list)
    doors: List[Dict[str, Any]] = field(default_factory=list)
    
    # Airtightness
    airtightness_n50: Optional[float] = None    # h⁻¹
    airtightness_q50: Optional[float] = None    # m³/h/m²
    blower_door_test_date: Optional[date] = None
    
    # Tepelné mostíky
    thermal_bridges: List[Dict[str, Any]] = field(default_factory=list)
    
    # Kvalita dát
    data_quality: DataQualityLevel = DataQualityLevel.ESTIMATED
    validation_status: ValidationStatus = ValidationStatus.INCOMPLETE

@dataclass
class ConstructionElement:
    """Stavebný prvok - detailná charakterizácia"""
    element_id: str
    element_name: str
    construction_type: ConstructionType
    
    # Geometria
    area: float                     # m²
    
    # Tepelno-technické vlastnosti
    u_value: float                  # W/m²K súčiniteľ prestupu tepla
    
    # Voliteľné geometrické parametre
    length: Optional[float] = None  # m (pre lineárne prvky)
    thickness: Optional[float] = None  # m
    
    # Voliteľné tepelno-technické vlastnosti
    u_value_source: Optional[DataSource] = None
    thermal_mass: Optional[float] = None     # J/m²K
    
    # Materiálové vrstvy (zvnútra smerom von)
    material_layers: List[Dict[str, Any]] = field(default_factory=list)
    
    # Stav a vek
    construction_year: Optional[int] = None
    condition_rating: str = "good"  # excellent, good, fair, poor
    renovation_history: List[Dict[str, Any]] = field(default_factory=list)
    
    # Diagnostika
    diagnostic_findings: List[Dict[str, Any]] = field(default_factory=list)
    moisture_problems: bool = False
    thermal_bridge_issues: bool = False
    
    # Údržba
    maintenance_requirements: List[str] = field(default_factory=list)
    expected_lifetime: Optional[int] = None  # rokov
    
    # Kvalita dát
    data_quality: DataQualityLevel = DataQualityLevel.ESTIMATED
    measurement_points: List[MeasurementPoint] = field(default_factory=list)

@dataclass
class TechnicalSystem:
    """Technický systém - unifikovaná štruktúra pre všetky systémy"""
    system_id: str
    system_name: str
    system_category: str            # heating, cooling, ventilation, lighting, dhw, other
    system_type: str                # špecifikácia typu
    
    # Základné parametre
    nominal_capacity: Optional[float] = None    # kW
    actual_capacity: Optional[float] = None     # kW
    efficiency_nominal: Optional[float] = None  # %
    efficiency_actual: Optional[float] = None   # %
    
    # Energetické údaje
    energy_input: List[Dict[str, Any]] = field(default_factory=list)
    energy_output: List[Dict[str, Any]] = field(default_factory=list)
    annual_consumption: Dict[EnergyCarrier, float] = field(default_factory=dict)
    load_profile: List[float] = field(default_factory=list)
    
    # Technické špecifikácie
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    installation_year: Optional[int] = None
    design_life: Optional[int] = None
    
    # Prevádzka a údržba
    operating_hours_annual: Optional[float] = None
    capacity_factor: Optional[float] = None    # %
    maintenance_schedule: Dict[str, Any] = field(default_factory=dict)
    maintenance_history: List[Dict[str, Any]] = field(default_factory=list)
    
    # Riadenie
    control_system: Optional[Dict[str, Any]] = None
    automation_level: str = "manual"  # manual, semi-automatic, automatic, smart
    setpoints: Dict[str, float] = field(default_factory=dict)
    
    # Stav systému
    operational_status: str = "operational"  # operational, degraded, non-operational
    condition_assessment: Dict[str, Any] = field(default_factory=dict)
    identified_issues: List[Dict[str, Any]] = field(default_factory=list)
    
    # Merania a monitoring
    measurement_points: List[MeasurementPoint] = field(default_factory=list)
    monitoring_data: List[Dict[str, Any]] = field(default_factory=list)
    
    # Kvalita dát
    data_quality: DataQualityLevel = DataQualityLevel.ESTIMATED
    data_sources: List[DataSource] = field(default_factory=list)

@dataclass
class EnergyConsumptionProfile:
    """Profil spotreby energie - rozšírený model"""
    energy_carrier: EnergyCarrier
    
    # Ročné údaje
    annual_consumption: float       # kWh/rok
    annual_cost: float             # €/rok
    unit_price: float              # €/kWh
    
    # Kvalita dát - povinné pole
    measurement_method: MeasurementMethod
    
    # Časové profily
    hourly_profile: Optional[List[float]] = None    # 8760 hodnôt
    daily_profile: Optional[List[float]] = None     # 24 hodnôt
    weekly_profile: Optional[List[float]] = None    # 7 hodnôt
    monthly_profile: Optional[List[float]] = None   # 12 hodnôt
    seasonal_variation: Optional[Dict[str, float]] = None
    
    # Špičkové hodnoty
    peak_demand: Optional[float] = None             # kW
    peak_demand_time: Optional[datetime] = None
    load_factor: Optional[float] = None             # %
    
    # Faktúry a merania
    utility_bills: List[Dict[str, Any]] = field(default_factory=list)
    meter_readings: List[Dict[str, Any]] = field(default_factory=list)
    sub_metering: Dict[str, Any] = field(default_factory=dict)
    
    # Normalizácia
    weather_corrected: bool = False
    occupancy_corrected: bool = False
    degree_days_correlation: Optional[float] = None
    
    # Kvalita dát - voliteľné polia
    measurement_uncertainty: Optional[float] = None  # %
    data_quality: DataQualityLevel = DataQualityLevel.ESTIMATED
    validation_status: ValidationStatus = ValidationStatus.INCOMPLETE

@dataclass
class DiagnosticFinding:
    """Diagnostické zistenie"""
    finding_id: str
    diagnostic_method: DiagnosticMethod
    location: str
    
    # Charakteristika zistenia
    severity: SeverityLevel
    description: str
    category: str                   # thermal, moisture, airtightness, structural, other
    
    # Dokumentácia - povinné polia
    measurement_date: datetime
    inspector: str
    
    # Kvantifikatívne údaje - voliteľné
    measured_values: Dict[str, float] = field(default_factory=dict)
    reference_values: Dict[str, float] = field(default_factory=dict)
    deviation: Optional[float] = None
    
    # Dokumentácia - voliteľné
    photographic_evidence: List[str] = field(default_factory=list)
    
    # Dopady
    energy_impact: Optional[float] = None           # kWh/rok
    cost_impact: Optional[float] = None             # €/rok
    comfort_impact: Optional[str] = None
    structural_impact: Optional[str] = None
    
    # Odporúčania
    recommended_actions: List[str] = field(default_factory=list)
    urgency_level: str = "medium"   # low, medium, high, urgent
    estimated_cost_to_fix: Optional[float] = None

@dataclass
class PerformanceIndicator:
    """Ukazovateľ výkonnosti"""
    indicator_id: str
    name: str
    category: str                   # energy, cost, environmental, comfort
    
    # Hodnoty - povinné
    current_value: float
    unit: str
    measurement_period: str
    
    # Hodnoty - voliteľné
    reference_value: Optional[float] = None
    target_value: Optional[float] = None
    benchmark_value: Optional[float] = None
    
    # Časové údaje - voliteľné
    trend_data: List[Tuple[datetime, float]] = field(default_factory=list)
    
    # Kontext - voliteľné
    calculation_method: str = "standard"
    normalization_factors: List[str] = field(default_factory=list)
    influencing_factors: List[str] = field(default_factory=list)

class ComprehensiveDataCollector:
    """Hlavná trieda pre komplexný zber dát"""
    
    def __init__(self, audit_type: AuditType = AuditType.BUILDING):
        """Inicializácia zberača dát"""
        self.audit_type = audit_type
        self.data_model = {}
        self.validation_rules = {}
        self.data_quality_requirements = {}
        
        # Inicializácia štruktúr
        self._initialize_data_structures()
        self._load_validation_rules()
        self._load_quality_requirements()
    
    def _initialize_data_structures(self):
        """Inicializácia dátových štruktúr"""
        self.data_model = {
            'general_info': None,
            'building_envelope': None,
            'construction_elements': [],
            'technical_systems': [],
            'energy_consumption': [],
            'diagnostic_findings': [],
            'performance_indicators': [],
            'audit_metadata': {
                'audit_id': None,
                'auditor': None,
                'audit_date': None,
                'audit_scope': None,
                'data_collection_methods': [],
                'limitations': [],
                'assumptions': []
            }
        }
    
    def _load_validation_rules(self):
        """Načítanie validačných pravidiel"""
        self.validation_rules = {
            'building_area': {
                'min_value': 10,        # m²
                'max_value': 100000,    # m²
                'required': True
            },
            'u_values': {
                'wall': {'min': 0.1, 'max': 3.0},      # W/m²K
                'roof': {'min': 0.1, 'max': 2.0},
                'floor': {'min': 0.1, 'max': 2.0},
                'window': {'min': 0.5, 'max': 5.0}
            },
            'efficiency': {
                'min': 10,              # %
                'max': 150,             # %
                'typical_range': (60, 95)
            },
            'energy_consumption': {
                'specific_heating': {'min': 0, 'max': 400},    # kWh/m²rok
                'specific_electricity': {'min': 0, 'max': 200},  # kWh/m²rok
                'cost_per_kwh': {'min': 0.01, 'max': 1.0}     # €/kWh
            }
        }
    
    def _load_quality_requirements(self):
        """Načítanie požiadaviek na kvalitu dát"""
        self.data_quality_requirements = {
            DataQualityLevel.MEASURED: {
                'uncertainty_max': 5.0,        # %
                'calibration_required': True,
                'documentation_level': 'detailed'
            },
            DataQualityLevel.CALCULATED: {
                'uncertainty_max': 10.0,       # %
                'method_documented': True,
                'assumptions_listed': True
            },
            DataQualityLevel.ESTIMATED: {
                'uncertainty_max': 25.0,       # %
                'basis_documented': True,
                'expert_judgment': True
            },
            DataQualityLevel.ASSUMED: {
                'uncertainty_max': 50.0,       # %
                'typical_values': True,
                'conservative_estimate': True
            }
        }
    
    def start_data_collection(self, audit_id: str, auditor: AuditorQualification,
                            audit_scope: Dict[str, Any]) -> Dict[str, Any]:
        """Spustenie zberu dát"""
        
        self.data_model['audit_metadata'].update({
            'audit_id': audit_id,
            'auditor': auditor,
            'audit_date': datetime.now(),
            'audit_scope': audit_scope
        })
        
        # Vytvorenie štruktúry formulárov na základe typu auditu
        forms_structure = self._create_data_collection_forms()
        
        return {
            'audit_id': audit_id,
            'data_collection_started': True,
            'forms_structure': forms_structure,
            'required_data_elements': self._get_required_data_elements(),
            'data_quality_targets': self._get_data_quality_targets()
        }
    
    def collect_general_building_info(self, building_info: Dict[str, Any]) -> Dict[str, Any]:
        """Zber základných informácií o budove"""
        
        # Validácia vstupných dát
        validation_result = self._validate_building_info(building_info)
        if not validation_result['valid']:
            return validation_result
        
        # Vytvorenie objektu
        general_info = BuildingGeneralInfo(
            building_name=building_info['building_name'],
            building_address=building_info['building_address'],
            building_type=building_info['building_type'],
            total_floor_area=building_info['total_floor_area'],
            heated_floor_area=building_info['heated_floor_area'],
            conditioned_volume=building_info.get('conditioned_volume', 
                                                building_info['heated_floor_area'] * 3.0),
            building_height=building_info.get('building_height', 
                                           building_info.get('number_of_floors', 3) * 3.0),
            number_of_floors=building_info.get('number_of_floors', 1),
            construction_year=building_info['construction_year']
        )
        
        # Doplnenie voliteľných údajov
        if 'major_renovations' in building_info:
            general_info.major_renovations = building_info['major_renovations']
        if 'occupancy_profile' in building_info:
            general_info.occupancy_profile = building_info['occupancy_profile']
        if 'operating_schedule' in building_info:
            general_info.operating_schedule = building_info['operating_schedule']
        
        # Hodnotenie kvality dát
        general_info.data_quality = self._assess_data_quality(building_info, 'building_info')
        
        self.data_model['general_info'] = general_info
        
        return {
            'success': True,
            'data_quality': general_info.data_quality.value,
            'completeness_score': self._calculate_completeness_score(building_info, 'building_info'),
            'validation_warnings': validation_result.get('warnings', [])
        }
    
    def collect_building_envelope_data(self, envelope_data: Dict[str, Any]) -> Dict[str, Any]:
        """Zber údajov o obálke budovy"""
        
        envelope = BuildingEnvelope(
            total_envelope_area=envelope_data['total_envelope_area'],
            window_to_wall_ratio=envelope_data.get('window_to_wall_ratio', 0.15)
        )
        
        # Spracovanie komponentov obálky
        if 'walls' in envelope_data:
            envelope.walls = self._process_construction_elements(envelope_data['walls'], 'wall')
        if 'roof' in envelope_data:
            envelope.roof = self._process_construction_elements(envelope_data['roof'], 'roof')
        if 'floors' in envelope_data:
            envelope.floors = self._process_construction_elements(envelope_data['floors'], 'floor')
        if 'windows' in envelope_data:
            envelope.windows = self._process_construction_elements(envelope_data['windows'], 'window')
        if 'doors' in envelope_data:
            envelope.doors = self._process_construction_elements(envelope_data['doors'], 'door')
        
        # Vzduchotesnosť
        if 'airtightness' in envelope_data:
            airtightness = envelope_data['airtightness']
            envelope.airtightness_n50 = airtightness.get('n50')
            envelope.airtightness_q50 = airtightness.get('q50')
            if 'test_date' in airtightness:
                envelope.blower_door_test_date = datetime.fromisoformat(airtightness['test_date']).date()
        
        # Validácia a hodnotenie kvality
        validation_result = self._validate_envelope_data(envelope_data)
        envelope.data_quality = self._assess_data_quality(envelope_data, 'envelope')
        envelope.validation_status = ValidationStatus.VALID if validation_result['valid'] else ValidationStatus.WARNING
        
        self.data_model['building_envelope'] = envelope
        
        return {
            'success': True,
            'validation_result': validation_result,
            'data_quality': envelope.data_quality.value,
            'completeness_score': self._calculate_completeness_score(envelope_data, 'envelope')
        }
    
    def collect_technical_systems_data(self, systems_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Zber údajov o technických systémoch"""
        
        systems = []
        validation_results = []
        
        for system_data in systems_data:
            # Vytvorenie systému
            system = TechnicalSystem(
                system_id=system_data['system_id'],
                system_name=system_data['system_name'],
                system_category=system_data['system_category'],
                system_type=system_data['system_type']
            )
            
            # Základné parametre
            if 'nominal_capacity' in system_data:
                system.nominal_capacity = system_data['nominal_capacity']
            if 'efficiency_nominal' in system_data:
                system.efficiency_nominal = system_data['efficiency_nominal']
            if 'installation_year' in system_data:
                system.installation_year = system_data['installation_year']
            
            # Energetické údaje
            if 'annual_consumption' in system_data:
                for carrier, consumption in system_data['annual_consumption'].items():
                    try:
                        energy_carrier = EnergyCarrier[carrier.upper()]
                        system.annual_consumption[energy_carrier] = consumption
                    except KeyError:
                        logging.warning(f"Neznámy energetický nosič: {carrier}")
            
            # Prevádzka
            if 'operating_hours_annual' in system_data:
                system.operating_hours_annual = system_data['operating_hours_annual']
            if 'maintenance_history' in system_data:
                system.maintenance_history = system_data['maintenance_history']
            
            # Riadenie
            if 'control_system' in system_data:
                system.control_system = system_data['control_system']
                system.automation_level = system_data.get('automation_level', 'manual')
            
            # Validácia
            validation_result = self._validate_system_data(system_data)
            validation_results.append(validation_result)
            
            # Kvalita dát
            system.data_quality = self._assess_data_quality(system_data, 'technical_system')
            
            systems.append(system)
        
        self.data_model['technical_systems'] = systems
        
        return {
            'success': True,
            'systems_processed': len(systems),
            'validation_results': validation_results,
            'overall_data_quality': self._calculate_overall_quality(systems)
        }
    
    def collect_energy_consumption_data(self, consumption_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Zber údajov o spotrebe energie"""
        
        consumption_profiles = []
        
        for data in consumption_data:
            try:
                energy_carrier = EnergyCarrier[data['energy_carrier'].upper()]
                measurement_method = MeasurementMethod[data['measurement_method'].upper()]
                
                profile = EnergyConsumptionProfile(
                    energy_carrier=energy_carrier,
                    annual_consumption=data['annual_consumption'],
                    annual_cost=data['annual_cost'],
                    unit_price=data.get('unit_price', data['annual_cost'] / data['annual_consumption']),
                    measurement_method=measurement_method
                )
                
                # Časové profily
                if 'monthly_profile' in data:
                    profile.monthly_profile = data['monthly_profile']
                if 'daily_profile' in data:
                    profile.daily_profile = data['daily_profile']
                if 'seasonal_variation' in data:
                    profile.seasonal_variation = data['seasonal_variation']
                
                # Špičkové hodnoty
                if 'peak_demand' in data:
                    profile.peak_demand = data['peak_demand']
                if 'load_factor' in data:
                    profile.load_factor = data['load_factor']
                
                # Faktúry a merania
                if 'utility_bills' in data:
                    profile.utility_bills = data['utility_bills']
                if 'meter_readings' in data:
                    profile.meter_readings = data['meter_readings']
                
                # Kvalita dát
                if 'measurement_uncertainty' in data:
                    profile.measurement_uncertainty = data['measurement_uncertainty']
                
                profile.data_quality = self._assess_data_quality(data, 'energy_consumption')
                profile.validation_status = self._validate_consumption_data(data)
                
                consumption_profiles.append(profile)
                
            except KeyError as e:
                logging.error(f"Chyba pri spracovaní energetických dát: {e}")
                continue
        
        self.data_model['energy_consumption'] = consumption_profiles
        
        return {
            'success': True,
            'profiles_processed': len(consumption_profiles),
            'total_annual_consumption': self._calculate_total_consumption(),
            'data_quality_summary': self._summarize_consumption_quality()
        }
    
    def collect_diagnostic_findings(self, findings_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Zber diagnostických zistení"""
        
        findings = []
        
        for finding_data in findings_data:
            try:
                diagnostic_method = DiagnosticMethod[finding_data['diagnostic_method'].upper()]
                severity = SeverityLevel[finding_data['severity'].upper()]
                
                finding = DiagnosticFinding(
                    finding_id=finding_data['finding_id'],
                    diagnostic_method=diagnostic_method,
                    location=finding_data['location'],
                    severity=severity,
                    description=finding_data['description'],
                    category=finding_data.get('category', 'other'),
                    measurement_date=datetime.fromisoformat(finding_data['measurement_date']),
                    inspector=finding_data['inspector']
                )
                
                # Kvantifikatívne údaje
                if 'measured_values' in finding_data:
                    finding.measured_values = finding_data['measured_values']
                if 'reference_values' in finding_data:
                    finding.reference_values = finding_data['reference_values']
                
                # Dopady
                if 'energy_impact' in finding_data:
                    finding.energy_impact = finding_data['energy_impact']
                if 'cost_impact' in finding_data:
                    finding.cost_impact = finding_data['cost_impact']
                
                # Odporúčania
                if 'recommended_actions' in finding_data:
                    finding.recommended_actions = finding_data['recommended_actions']
                if 'urgency_level' in finding_data:
                    finding.urgency_level = finding_data['urgency_level']
                
                findings.append(finding)
                
            except KeyError as e:
                logging.error(f"Chyba pri spracovaní diagnostického zistenia: {e}")
                continue
        
        self.data_model['diagnostic_findings'] = findings
        
        return {
            'success': True,
            'findings_processed': len(findings),
            'severity_distribution': self._analyze_finding_severity(findings),
            'categories_found': self._categorize_findings(findings)
        }
    
    def generate_data_quality_report(self) -> Dict[str, Any]:
        """Generovanie reportu o kvalite dát"""
        
        report = {
            'overall_assessment': self._assess_overall_data_quality(),
            'completeness_analysis': self._analyze_data_completeness(),
            'accuracy_assessment': self._assess_data_accuracy(),
            'reliability_scores': self._calculate_reliability_scores(),
            'improvement_recommendations': self._generate_quality_improvements(),
            'validation_summary': self._summarize_validation_results()
        }
        
        return report
    
    def export_collected_data(self, format: str = 'json') -> Dict[str, Any]:
        """Export nazbieraných dát"""
        
        if format == 'json':
            return self._export_to_json()
        elif format == 'xml':
            return self._export_to_xml()
        elif format == 'excel':
            return self._export_to_excel()
        else:
            raise ValueError(f"Nepodporovaný formát: {format}")
    
    # Pomocné metódy
    
    def _create_data_collection_forms(self) -> Dict[str, Any]:
        """Vytvorenie formulárov pre zber dát"""
        
        forms = {
            'general_building_info': {
                'required_fields': [
                    'building_name', 'building_address', 'building_type',
                    'total_floor_area', 'heated_floor_area', 'construction_year'
                ],
                'optional_fields': [
                    'number_of_floors', 'occupancy_profile', 'operating_schedule'
                ],
                'validation_rules': self.validation_rules.get('building_area', {})
            },
            'building_envelope': {
                'required_sections': ['walls', 'roof', 'floors', 'windows'],
                'optional_sections': ['doors', 'thermal_bridges', 'airtightness'],
                'quality_requirements': 'medium'
            },
            'technical_systems': {
                'system_categories': ['heating', 'cooling', 'ventilation', 'lighting', 'dhw'],
                'required_for_each': ['system_type', 'capacity', 'efficiency', 'age'],
                'measurement_requirements': 'system_dependent'
            },
            'energy_consumption': {
                'required_carriers': [EnergyCarrier.ELECTRICITY],
                'typical_carriers': [EnergyCarrier.NATURAL_GAS, EnergyCarrier.DISTRICT_HEATING],
                'minimum_data_period': '12 months',
                'preferred_measurement_method': MeasurementMethod.CONTINUOUS
            }
        }
        
        return forms
    
    def _validate_building_info(self, building_info: Dict[str, Any]) -> Dict[str, Any]:
        """Validácia základných informácií o budove"""
        
        errors = []
        warnings = []
        
        # Povinné polia
        required_fields = ['building_name', 'building_address', 'building_type', 
                          'total_floor_area', 'heated_floor_area', 'construction_year']
        
        for field in required_fields:
            if field not in building_info or building_info[field] is None:
                errors.append(f"Chýba povinné pole: {field}")
        
        # Kontrola plôch
        if 'total_floor_area' in building_info and 'heated_floor_area' in building_info:
            if building_info['heated_floor_area'] > building_info['total_floor_area']:
                errors.append("Vykurovaná plocha nemôže byť väčšia ako celková plocha")
        
        # Kontrola roku výstavby
        current_year = datetime.now().year
        if 'construction_year' in building_info:
            if building_info['construction_year'] < 1800 or building_info['construction_year'] > current_year:
                errors.append(f"Neplatný rok výstavby: {building_info['construction_year']}")
        
        # Kontrola typu budovy
        if 'building_type' in building_info:
            if building_info['building_type'] not in BUILDING_TYPES:
                warnings.append(f"Neštandardný typ budovy: {building_info['building_type']}")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
    
    def _assess_data_quality(self, data: Dict[str, Any], data_type: str) -> DataQualityLevel:
        """Hodnotenie kvality dát"""
        
        # Algoritmus hodnotenia kvality na základe rôznych faktorov
        quality_score = 0
        
        # Faktor 1: Kompletnosť dát
        completeness = self._calculate_completeness_score(data, data_type)
        quality_score += completeness * 0.4
        
        # Faktor 2: Zdroj dát
        if 'data_source' in data:
            source_quality = {
                'measured': 100,
                'calculated': 80,
                'estimated': 60,
                'assumed': 40
            }
            quality_score += source_quality.get(data.get('data_source'), 50) * 0.3
        
        # Faktor 3: Presnosť (ak je uvedená)
        if 'uncertainty' in data:
            uncertainty = data['uncertainty']
            if uncertainty <= 5:
                quality_score += 30
            elif uncertainty <= 10:
                quality_score += 20
            elif uncertainty <= 25:
                quality_score += 10
        else:
            quality_score += 15  # predvolená hodnota
        
        # Faktor 4: Aktuálnosť dát
        if 'measurement_date' in data:
            try:
                measurement_date = datetime.fromisoformat(data['measurement_date'])
                days_old = (datetime.now() - measurement_date).days
                if days_old <= 365:
                    quality_score += 10
                elif days_old <= 1825:  # 5 rokov
                    quality_score += 5
            except:
                pass
        
        # Klasifikácia kvality
        if quality_score >= 85:
            return DataQualityLevel.MEASURED
        elif quality_score >= 65:
            return DataQualityLevel.CALCULATED
        elif quality_score >= 45:
            return DataQualityLevel.ESTIMATED
        else:
            return DataQualityLevel.ASSUMED
    
    def _calculate_completeness_score(self, data: Dict[str, Any], data_type: str) -> float:
        """Výpočet skóre kompletnosti dát"""
        
        # Definícia povinných a voliteľných polí pre každý typ dát
        field_definitions = {
            'building_info': {
                'required': ['building_name', 'building_address', 'building_type',
                           'total_floor_area', 'heated_floor_area', 'construction_year'],
                'optional': ['number_of_floors', 'occupancy_profile', 'climate_zone']
            },
            'envelope': {
                'required': ['total_envelope_area', 'walls', 'roof', 'floors'],
                'optional': ['windows', 'doors', 'thermal_bridges', 'airtightness']
            },
            'technical_system': {
                'required': ['system_type', 'nominal_capacity'],
                'optional': ['efficiency_nominal', 'installation_year', 'control_system']
            },
            'energy_consumption': {
                'required': ['energy_carrier', 'annual_consumption', 'measurement_method'],
                'optional': ['monthly_profile', 'peak_demand', 'utility_bills']
            }
        }
        
        definition = field_definitions.get(data_type, {'required': [], 'optional': []})
        
        # Výpočet skóre
        required_score = 0
        for field in definition['required']:
            if field in data and data[field] is not None:
                required_score += 1
        
        optional_score = 0
        for field in definition['optional']:
            if field in data and data[field] is not None:
                optional_score += 1
        
        # Vážené skóre (povinné polia 80%, voliteľné 20%)
        total_required = len(definition['required'])
        total_optional = len(definition['optional'])
        
        if total_required > 0:
            required_ratio = required_score / total_required
        else:
            required_ratio = 1.0
        
        if total_optional > 0:
            optional_ratio = optional_score / total_optional
        else:
            optional_ratio = 0.0
        
        return required_ratio * 80 + optional_ratio * 20
    
    def _process_construction_elements(self, elements: List[Dict], element_type: str) -> List[Dict]:
        """Spracovanie stavebných prvkov"""
        processed_elements = []
        
        for element in elements:
            processed = {
                'name': element.get('name', f'{element_type}_{len(processed_elements)+1}'),
                'area': element['area'],
                'u_value': element['u_value'],
                'construction_type': element_type,
                'data_quality': self._assess_data_quality(element, 'construction_element').value
            }
            
            # Doplniť voliteľné údaje
            if 'material_layers' in element:
                processed['material_layers'] = element['material_layers']
            if 'construction_year' in element:
                processed['construction_year'] = element['construction_year']
            if 'condition_rating' in element:
                processed['condition_rating'] = element['condition_rating']
            
            processed_elements.append(processed)
        
        return processed_elements
    
    def _get_required_data_elements(self) -> List[str]:
        """Získanie zoznamu povinných dátových elementov"""
        return [
            'building_general_info',
            'building_envelope',
            'technical_systems',
            'energy_consumption',
            'occupancy_data',
            'operational_data'
        ]
    
    def _get_data_quality_targets(self) -> Dict[str, str]:
        """Získanie cieľov kvality dát"""
        return {
            'overall_minimum': DataQualityLevel.ESTIMATED.value,
            'critical_data_minimum': DataQualityLevel.CALCULATED.value,
            'measurement_data_target': DataQualityLevel.MEASURED.value
        }
    
    def _validate_envelope_data(self, envelope_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validácia údajov obálky budovy"""
        errors = []
        warnings = []
        
        # Kontrola celkovej plochy obálky
        if 'total_envelope_area' not in envelope_data:
            errors.append("Chýba celková plocha obálky")
        
        # Kontrola komponentov
        required_components = ['walls', 'roof', 'floors']
        for component in required_components:
            if component not in envelope_data or not envelope_data[component]:
                warnings.append(f"Chýba komponente obálky: {component}")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
    
    def _validate_system_data(self, system_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validácia údajov technického systému"""
        errors = []
        warnings = []
        
        # Povinné polia
        required_fields = ['system_id', 'system_name', 'system_category', 'system_type']
        for field in required_fields:
            if field not in system_data:
                errors.append(f"Chýba povinné pole: {field}")
        
        # Kontrola efektívnosti
        if 'efficiency_nominal' in system_data:
            efficiency = system_data['efficiency_nominal']
            if efficiency < 10 or efficiency > 150:
                warnings.append(f"Neštandardná efektívnosť: {efficiency}%")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
    
    def _validate_consumption_data(self, data: Dict[str, Any]) -> ValidationStatus:
        """Validácia údajov spotreby energie"""
        errors = 0
        
        # Povinné polia
        required_fields = ['energy_carrier', 'annual_consumption', 'annual_cost']
        for field in required_fields:
            if field not in data or data[field] is None:
                errors += 1
        
        # Kontrola rozumnosti hodnôt
        if 'annual_consumption' in data and 'annual_cost' in data:
            if data['annual_consumption'] <= 0 or data['annual_cost'] <= 0:
                errors += 1
        
        if errors == 0:
            return ValidationStatus.VALID
        elif errors <= 2:
            return ValidationStatus.WARNING
        else:
            return ValidationStatus.ERROR
    
    def _calculate_overall_quality(self, systems: List[TechnicalSystem]) -> Dict[str, Any]:
        """Výpočet celkovej kvality systémov"""
        if not systems:
            return {'overall_quality': 'no_data', 'quality_distribution': {}}
        
        quality_counts = {}
        for system in systems:
            quality = system.data_quality.value
            quality_counts[quality] = quality_counts.get(quality, 0) + 1
        
        # Určenie celkovej kvality
        total_systems = len(systems)
        if quality_counts.get('measured', 0) / total_systems >= 0.5:
            overall_quality = 'high'
        elif quality_counts.get('calculated', 0) / total_systems >= 0.5:
            overall_quality = 'medium'
        else:
            overall_quality = 'low'
        
        return {
            'overall_quality': overall_quality,
            'quality_distribution': quality_counts,
            'total_systems': total_systems
        }
    
    def _calculate_total_consumption(self) -> Dict[str, float]:
        """Výpočet celkovej spotreby energie"""
        total_by_carrier = {}
        
        for profile in self.data_model.get('energy_consumption', []):
            carrier = profile.energy_carrier.value
            consumption = profile.annual_consumption
            total_by_carrier[carrier] = total_by_carrier.get(carrier, 0) + consumption
        
        return total_by_carrier
    
    def _summarize_consumption_quality(self) -> Dict[str, Any]:
        """Súhrn kvality údajov spotreby"""
        profiles = self.data_model.get('energy_consumption', [])
        if not profiles:
            return {'status': 'no_data'}
        
        quality_summary = {}
        for profile in profiles:
            quality = profile.data_quality.value
            quality_summary[quality] = quality_summary.get(quality, 0) + 1
        
        return {
            'total_profiles': len(profiles),
            'quality_distribution': quality_summary,
            'high_quality_percentage': (quality_summary.get('measured', 0) + 
                                      quality_summary.get('calculated', 0)) / len(profiles) * 100
        }
    
    def _analyze_finding_severity(self, findings: List[DiagnosticFinding]) -> Dict[str, int]:
        """Analýza závažnosti diagnostických zistení"""
        severity_counts = {}
        
        for finding in findings:
            severity = finding.severity.value
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        return severity_counts
    
    def _categorize_findings(self, findings: List[DiagnosticFinding]) -> Dict[str, int]:
        """Kategorizácia diagnostických zistení"""
        category_counts = {}
        
        for finding in findings:
            category = finding.category
            category_counts[category] = category_counts.get(category, 0) + 1
        
        return category_counts
    
    def _assess_overall_data_quality(self) -> Dict[str, Any]:
        """Celkové hodnotenie kvality dát"""
        scores = []
        weights = []
        
        # Hodnotenie základných údajov
        if self.data_model['general_info']:
            scores.append(self._quality_to_score(self.data_model['general_info'].data_quality))
            weights.append(0.2)
        
        # Hodnotenie obálky budovy
        if self.data_model['building_envelope']:
            scores.append(self._quality_to_score(self.data_model['building_envelope'].data_quality))
            weights.append(0.3)
        
        # Hodnotenie technických systémov
        systems = self.data_model['technical_systems']
        if systems:
            system_scores = [self._quality_to_score(sys.data_quality) for sys in systems]
            avg_system_score = sum(system_scores) / len(system_scores)
            scores.append(avg_system_score)
            weights.append(0.3)
        
        # Hodnotenie spotreby energie
        consumption = self.data_model['energy_consumption']
        if consumption:
            consumption_scores = [self._quality_to_score(prof.data_quality) for prof in consumption]
            avg_consumption_score = sum(consumption_scores) / len(consumption_scores)
            scores.append(avg_consumption_score)
            weights.append(0.2)
        
        # Vážený priemer
        if scores and weights:
            weighted_score = sum(s * w for s, w in zip(scores, weights)) / sum(weights)
            return {
                'overall_score': weighted_score,
                'quality_level': self._score_to_quality(weighted_score).value,
                'component_scores': dict(zip(['general', 'envelope', 'systems', 'consumption'], scores))
            }
        
        return {'overall_score': 0, 'quality_level': 'no_data'}
    
    def _quality_to_score(self, quality: DataQualityLevel) -> float:
        """Konverzia kvality na numerické skóre"""
        mapping = {
            DataQualityLevel.MEASURED: 100,
            DataQualityLevel.CALCULATED: 80,
            DataQualityLevel.ESTIMATED: 60,
            DataQualityLevel.ASSUMED: 40
        }
        return mapping.get(quality, 0)
    
    def _score_to_quality(self, score: float) -> DataQualityLevel:
        """Konverzia numerického skóre na kvalitu"""
        if score >= 85:
            return DataQualityLevel.MEASURED
        elif score >= 65:
            return DataQualityLevel.CALCULATED
        elif score >= 45:
            return DataQualityLevel.ESTIMATED
        else:
            return DataQualityLevel.ASSUMED
    
    def _analyze_data_completeness(self) -> Dict[str, Any]:
        """Analýza kompletnosti dát"""
        completeness_scores = {}
        
        # Základné informácie
        if self.data_model['general_info']:
            completeness_scores['general_info'] = 90  # Simulácia
        
        # Obálka budovy
        if self.data_model['building_envelope']:
            completeness_scores['building_envelope'] = 75  # Simulácia
        
        # Technické systémy
        if self.data_model['technical_systems']:
            completeness_scores['technical_systems'] = 80  # Simulácia
        
        # Spotreba energie
        if self.data_model['energy_consumption']:
            completeness_scores['energy_consumption'] = 85  # Simulácia
        
        overall_completeness = sum(completeness_scores.values()) / len(completeness_scores) if completeness_scores else 0
        
        return {
            'overall_completeness': overall_completeness,
            'component_completeness': completeness_scores,
            'missing_critical_data': self._identify_missing_critical_data()
        }
    
    def _assess_data_accuracy(self) -> Dict[str, Any]:
        """Hodnotenie presnosti dát"""
        return {
            'measurement_accuracy': 'high',  # Simulácia
            'calculation_accuracy': 'medium',
            'estimation_reliability': 'medium',
            'validation_passed': 85  # % validácií ktoré prešli
        }
    
    def _calculate_reliability_scores(self) -> Dict[str, float]:
        """Výpočet skóre spoľahlivosti"""
        return {
            'data_sources': 0.8,
            'measurement_methods': 0.9,
            'expert_assessments': 0.7,
            'documentation_quality': 0.8
        }
    
    def _generate_quality_improvements(self) -> List[str]:
        """Generovanie odporúčaní na zlepšenie kvality"""
        recommendations = []
        
        # Kontrola kvality dát a generovanie odporúčaní
        if self.data_model['general_info'] and self.data_model['general_info'].data_quality in [DataQualityLevel.ESTIMATED, DataQualityLevel.ASSUMED]:
            recommendations.append("Doplniť presné merania základných parametrov budovy")
        
        if not self.data_model['energy_consumption']:
            recommendations.append("Implementovať kontinuálne monitorovanie spotreby energie")
        
        if not self.data_model['diagnostic_findings']:
            recommendations.append("Vykonať podrobnú diagnostiku budovy")
        
        return recommendations
    
    def _summarize_validation_results(self) -> Dict[str, Any]:
        """Súhrn výsledkov validácie"""
        return {
            'total_validations': 10,  # Simulácia
            'passed': 8,
            'warnings': 2,
            'errors': 0,
            'success_rate': 80.0
        }
    
    def _identify_missing_critical_data(self) -> List[str]:
        """Identifikácia chýbajúcich kritických dát"""
        missing = []
        
        if not self.data_model['general_info']:
            missing.append('building_general_info')
        
        if not self.data_model['energy_consumption']:
            missing.append('energy_consumption_data')
        
        if not self.data_model['technical_systems']:
            missing.append('technical_systems_data')
        
        return missing
    
    def _export_to_xml(self) -> Dict[str, Any]:
        """Export do XML formátu"""
        return {'error': 'XML export not implemented yet'}
    
    def _export_to_excel(self) -> Dict[str, Any]:
        """Export do Excel formátu"""
        return {'error': 'Excel export not implemented yet'}
    
    def _export_to_json(self) -> Dict[str, Any]:
        """Export do JSON formátu"""
        
        # Konverzia dataclass objektov na slovníky
        export_data = {
            'audit_metadata': self.data_model['audit_metadata'],
            'general_info': self._dataclass_to_dict(self.data_model['general_info']),
            'building_envelope': self._dataclass_to_dict(self.data_model['building_envelope']),
            'technical_systems': [self._dataclass_to_dict(sys) for sys in self.data_model['technical_systems']],
            'energy_consumption': [self._dataclass_to_dict(prof) for prof in self.data_model['energy_consumption']],
            'diagnostic_findings': [self._dataclass_to_dict(find) for find in self.data_model['diagnostic_findings']],
            'export_timestamp': datetime.now().isoformat(),
            'data_quality_summary': self.generate_data_quality_report()
        }
        
        return export_data
    
    def _dataclass_to_dict(self, obj) -> Dict[str, Any]:
        """Konverzia dataclass na slovník"""
        if obj is None:
            return None
        
        result = {}
        for key, value in obj.__dict__.items():
            if isinstance(value, Enum):
                result[key] = value.value
            elif isinstance(value, datetime):
                result[key] = value.isoformat()
            elif isinstance(value, date):
                result[key] = value.isoformat()
            elif isinstance(value, dict):
                # Spracovanie slovníkov s enum kľúčmi
                converted_dict = {}
                for k, v in value.items():
                    if isinstance(k, Enum):
                        converted_dict[k.value] = v
                    else:
                        converted_dict[str(k)] = v
                result[key] = converted_dict
            elif isinstance(value, list):
                result[key] = [self._dataclass_to_dict(item) if hasattr(item, '__dict__') else item for item in value]
            elif hasattr(value, '__dict__'):
                result[key] = self._dataclass_to_dict(value)
            else:
                result[key] = value
        
        return result


def get_comprehensive_data_collector(audit_type: AuditType = AuditType.BUILDING) -> ComprehensiveDataCollector:
    """Factory funkcia pre komplexný zberač dát"""
    return ComprehensiveDataCollector(audit_type)

if __name__ == "__main__":
    # Demo použitia
    print("=== COMPREHENSIVE DATA COLLECTION DEMO ===")
    
    collector = get_comprehensive_data_collector(AuditType.BUILDING)
    
    # Spustenie zberu dát
    from stn_en_16247 import create_sample_auditor_qualification
    
    auditor = create_sample_auditor_qualification()
    audit_scope = {
        'scope_type': 'comprehensive',
        'boundaries': 'whole_building',
        'focus_areas': ['energy_efficiency', 'comfort', 'sustainability']
    }
    
    collection_start = collector.start_data_collection('DEMO-COLLECTION-001', auditor, audit_scope)
    print(f"Zber dát spustený: {collection_start['audit_id']}")
    print(f"Požadované elementy: {len(collection_start['required_data_elements'])}")
    
    # Príklad zberu základných údajov
    building_info = {
        'building_name': 'Demo Office Building',
        'building_address': 'Bratislava, Slovensko',
        'building_type': 'Administratívna budova',
        'total_floor_area': 2500.0,
        'heated_floor_area': 2300.0,
        'construction_year': 1995,
        'number_of_floors': 4,
        'occupancy_profile': {'max_occupants': 150, 'typical_occupants': 120},
        'operating_schedule': {'weekdays': '7:00-18:00', 'weekends': 'closed'}
    }
    
    general_result = collector.collect_general_building_info(building_info)
    print(f"Základné údaje: {general_result['success']}, kvalita: {general_result['data_quality']}")
    
    # Report o kvalite dát
    quality_report = collector.generate_data_quality_report()
    print(f"Celkové hodnotenie kvality: {quality_report['overall_assessment']}")
    
    print("\n=== DATA COLLECTION DEMO COMPLETED ===")