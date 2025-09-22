#!/usr/bin/env python3
"""
Energy Monitoring and Measurement Module
Implementuje systém monitorovania a merania energetickej efektívnosti po renovácii
Obsahuje M&V (Measurement and Verification) protokoly podľa IPMVP
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from datetime import datetime, timedelta
import statistics
import math
import json

class MeasurementType(Enum):
    """Typy merania energie"""
    ELECTRICITY = "electricity"
    GAS = "gas"
    NATURAL_GAS = "natural_gas"  # Alias pre plyn
    HEATING = "heating"
    HOT_WATER = "hot_water"
    COOLING = "cooling"
    TOTAL_ENERGY = "total_energy"

class MVOption(Enum):
    """M&V opcie podľa IPMVP"""
    OPTION_A = "A"  # Partially Measured Retrofit Isolation
    OPTION_B = "B"  # Retrofit Isolation
    OPTION_C = "C"  # Whole Facility
    OPTION_D = "D"  # Calibrated Simulation

class PerformanceStatus(Enum):
    """Status výkonnosti oproti predpokladom"""
    EXCEEDS = "exceeds_expectations"      # Predčí očakávania
    MEETS = "meets_expectations"          # Spĺňa očakávania  
    BELOW = "below_expectations"          # Pod očakávaniami
    CRITICAL = "critical_underperformance" # Kritické podvýkonnosť

@dataclass
class EnergyReading:
    """Meranie spotreby energie"""
    timestamp: datetime
    measurement_type: MeasurementType
    value: float  # kWh, m³, atď.
    unit: str
    meter_id: Optional[str] = None
    location: Optional[str] = None
    notes: Optional[str] = None
    
@dataclass
class BaselinePeriod:
    """Referenčné obdobie pred renováciou"""
    start_date: datetime
    end_date: datetime
    measurements: List[EnergyReading] = field(default_factory=list)
    weather_data: List[Dict] = field(default_factory=list)
    occupancy_data: List[Dict] = field(default_factory=list)
    
    @property
    def duration_days(self) -> int:
        """Dĺžka referenčného obdobia v dňoch"""
        return (self.end_date - self.start_date).days
    
    def get_total_consumption(self, measurement_type: MeasurementType) -> float:
        """Celková spotreba za referenčné obdobie"""
        return sum(reading.value for reading in self.measurements 
                  if reading.measurement_type == measurement_type)

@dataclass
class ReportingPeriod:
    """Obdobie reportovania po renovácii"""
    start_date: datetime
    end_date: datetime
    measurements: List[EnergyReading] = field(default_factory=list)
    weather_data: List[Dict] = field(default_factory=list)
    occupancy_data: List[Dict] = field(default_factory=list)
    
    @property
    def duration_days(self) -> int:
        """Dĺžka obdobia reportovania v dňoch"""
        return (self.end_date - self.start_date).days
    
    def get_total_consumption(self, measurement_type: MeasurementType) -> float:
        """Celková spotreba za obdobie reportovania"""
        return sum(reading.value for reading in self.measurements 
                  if reading.measurement_type == measurement_type)

@dataclass
class MVPlan:
    """Measurement and Verification plán"""
    mv_option: MVOption
    measurement_types: List[MeasurementType]
    baseline_period: BaselinePeriod
    measurement_frequency: str  # "hourly", "daily", "monthly"
    accuracy_requirements: Dict[MeasurementType, float]  # požadovaná presnosť v %
    reporting_frequency: str  # "monthly", "quarterly", "annual"
    savings_targets: Dict[MeasurementType, float]  # očakávané úspory
    measurement_equipment: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SavingsCalculation:
    """Výpočet energetických úspor"""
    measurement_type: MeasurementType
    baseline_consumption: float
    reporting_consumption: float
    normalized_baseline: Optional[float] = None
    normalized_reporting: Optional[float] = None
    weather_adjustment: Optional[float] = None
    occupancy_adjustment: Optional[float] = None
    
    @property
    def raw_savings(self) -> float:
        """Hrubé úspory bez normalizácie"""
        return self.baseline_consumption - self.reporting_consumption
    
    @property
    def normalized_savings(self) -> float:
        """Normalizované úspory"""
        if self.normalized_baseline and self.normalized_reporting:
            return self.normalized_baseline - self.normalized_reporting
        return self.raw_savings
    
    @property
    def savings_percentage(self) -> float:
        """Percentuálne úspory"""
        if self.baseline_consumption > 0:
            return (self.normalized_savings / self.baseline_consumption) * 100
        return 0

class EnergyMonitoringSystem:
    """Hlavný systém monitorovania energie"""
    
    def __init__(self):
        """Inicializácia monitorovacieho systému"""
        self.mv_plans: Dict[str, MVPlan] = {}
        self.active_monitoring: Dict[str, Any] = {}
        self.weather_stations: Dict[str, Any] = {}
        
    def create_mv_plan(self, project_id: str, mv_option: MVOption, 
                      baseline_start: datetime, baseline_end: datetime,
                      measurement_types: List[MeasurementType],
                      savings_targets: Dict[MeasurementType, float]) -> MVPlan:
        """
        Vytvorenie M&V plánu
        
        Args:
            project_id: ID projektu
            mv_option: M&V opcia podľa IPMVP
            baseline_start: Začiatok referenčného obdobia
            baseline_end: Koniec referenčného obdobia
            measurement_types: Typy merania
            savings_targets: Očakávané úspory
            
        Returns:
            M&V plán
        """
        baseline_period = BaselinePeriod(baseline_start, baseline_end)
        
        # Určenie presnosti podľa M&V opcie
        accuracy_requirements = self._determine_accuracy_requirements(mv_option, measurement_types)
        
        mv_plan = MVPlan(
            mv_option=mv_option,
            measurement_types=measurement_types,
            baseline_period=baseline_period,
            measurement_frequency=self._determine_measurement_frequency(mv_option),
            accuracy_requirements=accuracy_requirements,
            reporting_frequency="monthly",
            savings_targets=savings_targets
        )
        
        self.mv_plans[project_id] = mv_plan
        return mv_plan
    
    def add_baseline_measurement(self, project_id: str, reading: EnergyReading):
        """Pridanie merania do referenčného obdobia"""
        if project_id in self.mv_plans:
            self.mv_plans[project_id].baseline_period.measurements.append(reading)
    
    def calculate_savings(self, project_id: str, reporting_period: ReportingPeriod) -> Dict[MeasurementType, SavingsCalculation]:
        """
        Výpočet úspor energie
        
        Args:
            project_id: ID projektu
            reporting_period: Obdobie reportovania
            
        Returns:
            Slovník s výpočtami úspor pre každý typ merania
        """
        if project_id not in self.mv_plans:
            raise ValueError(f"M&V plán pre projekt {project_id} neexistuje")
        
        mv_plan = self.mv_plans[project_id]
        savings_results = {}
        
        for measurement_type in mv_plan.measurement_types:
            # Baseline spotreba
            baseline_consumption = mv_plan.baseline_period.get_total_consumption(measurement_type)
            
            # Reporting spotreba
            reporting_consumption = reporting_period.get_total_consumption(measurement_type)
            
            # Normalizácia na počasie a obsadenosť
            normalized_baseline = self._normalize_consumption(
                baseline_consumption, mv_plan.baseline_period, reporting_period, measurement_type
            )
            
            savings_calc = SavingsCalculation(
                measurement_type=measurement_type,
                baseline_consumption=baseline_consumption,
                reporting_consumption=reporting_consumption,
                normalized_baseline=normalized_baseline,
                normalized_reporting=reporting_consumption
            )
            
            savings_results[measurement_type] = savings_calc
        
        return savings_results
    
    def generate_performance_report(self, project_id: str, reporting_period: ReportingPeriod) -> Dict[str, Any]:
        """
        Generovanie reportu výkonnosti
        
        Args:
            project_id: ID projektu
            reporting_period: Obdobie reportovania
            
        Returns:
            Report výkonnosti
        """
        savings_calculations = self.calculate_savings(project_id, reporting_period)
        mv_plan = self.mv_plans[project_id]
        
        # Porovnanie s cieľmi
        performance_assessment = {}
        overall_performance = []
        
        for measurement_type, savings_calc in savings_calculations.items():
            target_savings = mv_plan.savings_targets.get(measurement_type, 0)
            actual_savings = savings_calc.normalized_savings
            
            # Hodnotenie výkonnosti
            if actual_savings >= target_savings * 1.1:  # 110% cieľa
                status = PerformanceStatus.EXCEEDS
            elif actual_savings >= target_savings * 0.9:  # 90% cieľa
                status = PerformanceStatus.MEETS
            elif actual_savings >= target_savings * 0.7:  # 70% cieľa
                status = PerformanceStatus.BELOW
            else:
                status = PerformanceStatus.CRITICAL
            
            performance_assessment[measurement_type] = {
                'target_savings': target_savings,
                'actual_savings': actual_savings,
                'achievement_rate': (actual_savings / target_savings * 100) if target_savings > 0 else 0,
                'status': status.value,
                'savings_percentage': savings_calc.savings_percentage
            }
            
            overall_performance.append(actual_savings / target_savings if target_savings > 0 else 1)
        
        # Celkové hodnotenie
        average_achievement = statistics.mean(overall_performance) * 100 if overall_performance else 0
        
        # Ekonomická analýza
        economic_analysis = self._calculate_economic_performance(savings_calculations, mv_plan)
        
        # Trendová analýza
        trend_analysis = self._analyze_consumption_trends(reporting_period)
        
        return {
            'report_metadata': {
                'project_id': project_id,
                'reporting_period': {
                    'start': reporting_period.start_date.isoformat(),
                    'end': reporting_period.end_date.isoformat(),
                    'duration_days': reporting_period.duration_days
                },
                'mv_option': mv_plan.mv_option.value,
                'generated_date': datetime.now().isoformat()
            },
            'savings_summary': {
                measurement_type.value: {
                    'baseline_consumption': calc.baseline_consumption,
                    'reporting_consumption': calc.reporting_consumption,
                    'raw_savings': calc.raw_savings,
                    'normalized_savings': calc.normalized_savings,
                    'savings_percentage': calc.savings_percentage
                }
                for measurement_type, calc in savings_calculations.items()
            },
            'performance_assessment': performance_assessment,
            'overall_performance': {
                'average_achievement_rate': average_achievement,
                'total_energy_savings': sum(calc.normalized_savings for calc in savings_calculations.values()),
                'total_baseline_consumption': sum(calc.baseline_consumption for calc in savings_calculations.values())
            },
            'economic_analysis': economic_analysis,
            'trend_analysis': trend_analysis,
            'recommendations': self._generate_performance_recommendations(performance_assessment)
        }
    
    def _determine_accuracy_requirements(self, mv_option: MVOption, 
                                       measurement_types: List[MeasurementType]) -> Dict[MeasurementType, float]:
        """Určenie požiadaviek na presnosť merania"""
        base_accuracy = {
            MVOption.OPTION_A: 20.0,  # ±20%
            MVOption.OPTION_B: 10.0,  # ±10%  
            MVOption.OPTION_C: 5.0,   # ±5%
            MVOption.OPTION_D: 10.0   # ±10%
        }
        
        accuracy = base_accuracy.get(mv_option, 10.0)
        return {mt: accuracy for mt in measurement_types}
    
    def _determine_measurement_frequency(self, mv_option: MVOption) -> str:
        """Určenie frekvencie merania"""
        frequency_map = {
            MVOption.OPTION_A: "monthly",
            MVOption.OPTION_B: "daily",
            MVOption.OPTION_C: "hourly", 
            MVOption.OPTION_D: "monthly"
        }
        return frequency_map.get(mv_option, "daily")
    
    def _normalize_consumption(self, baseline_consumption: float, baseline_period: BaselinePeriod,
                             reporting_period: ReportingPeriod, measurement_type: MeasurementType) -> float:
        """Normalizácia spotreby na počasie a obsadenosť"""
        
        # Normalizácia na stupne-dni (pre vykurovanie)
        if measurement_type in [MeasurementType.HEATING, MeasurementType.GAS]:
            baseline_hdd = self._calculate_heating_degree_days(baseline_period.weather_data)
            reporting_hdd = self._calculate_heating_degree_days(reporting_period.weather_data)
            
            if baseline_hdd > 0 and reporting_hdd > 0:
                weather_factor = reporting_hdd / baseline_hdd
                return baseline_consumption * weather_factor
        
        # Normalizácia na chladiace stupne-dni (pre klimatizáciu)
        elif measurement_type == MeasurementType.COOLING:
            baseline_cdd = self._calculate_cooling_degree_days(baseline_period.weather_data)
            reporting_cdd = self._calculate_cooling_degree_days(reporting_period.weather_data)
            
            if baseline_cdd > 0 and reporting_cdd > 0:
                weather_factor = reporting_cdd / baseline_cdd
                return baseline_consumption * weather_factor
        
        # Pre ostatné typy energie - jednoduchá normalizácia na dĺžku obdobia
        baseline_days = baseline_period.duration_days
        reporting_days = reporting_period.duration_days
        
        if baseline_days > 0:
            return baseline_consumption * (reporting_days / baseline_days)
        
        return baseline_consumption
    
    def _calculate_heating_degree_days(self, weather_data: List[Dict], base_temp: float = 15.0) -> float:
        """Výpočet vykurovacích stupňo-dní"""
        if not weather_data:
            return 0
        
        total_hdd = 0
        for day_data in weather_data:
            avg_temp = day_data.get('average_temperature', 15.0)
            if avg_temp < base_temp:
                total_hdd += base_temp - avg_temp
        
        return total_hdd
    
    def _calculate_cooling_degree_days(self, weather_data: List[Dict], base_temp: float = 24.0) -> float:
        """Výpočet chladiacich stupňo-dní"""
        if not weather_data:
            return 0
        
        total_cdd = 0
        for day_data in weather_data:
            avg_temp = day_data.get('average_temperature', 20.0)
            if avg_temp > base_temp:
                total_cdd += avg_temp - base_temp
        
        return total_cdd
    
    def _calculate_economic_performance(self, savings_calculations: Dict[MeasurementType, SavingsCalculation],
                                      mv_plan: MVPlan) -> Dict[str, Any]:
        """Výpočet ekonomickej výkonnosti"""
        
        # Jednoduché cenové predpoklady (€/kWh)
        energy_prices = {
            MeasurementType.ELECTRICITY: 0.15,
            MeasurementType.GAS: 0.08,
            MeasurementType.HEATING: 0.10,
            MeasurementType.HOT_WATER: 0.12,
            MeasurementType.COOLING: 0.18
        }
        
        total_savings_value = 0
        savings_by_type = {}
        
        for measurement_type, savings_calc in savings_calculations.items():
            price_per_unit = energy_prices.get(measurement_type, 0.10)
            savings_value = savings_calc.normalized_savings * price_per_unit
            total_savings_value += savings_value
            
            savings_by_type[measurement_type.value] = {
                'energy_savings_kwh': savings_calc.normalized_savings,
                'unit_price': price_per_unit,
                'cost_savings_eur': savings_value
            }
        
        return {
            'total_annual_savings': total_savings_value,
            'savings_by_type': savings_by_type,
            'average_unit_cost_savings': total_savings_value / sum(calc.normalized_savings for calc in savings_calculations.values()) if savings_calculations else 0
        }
    
    def _analyze_consumption_trends(self, reporting_period: ReportingPeriod) -> Dict[str, Any]:
        """Analýza trendov spotreby"""
        
        # Grupovanie meraní po mesiacoch
        monthly_data = {}
        for reading in reporting_period.measurements:
            month_key = reading.timestamp.strftime('%Y-%m')
            if month_key not in monthly_data:
                monthly_data[month_key] = {}
            
            measurement_type = reading.measurement_type.value
            if measurement_type not in monthly_data[month_key]:
                monthly_data[month_key][measurement_type] = 0
            
            monthly_data[month_key][measurement_type] += reading.value
        
        # Výpočet trendov
        trends = {}
        for measurement_type in [mt.value for mt in MeasurementType]:
            monthly_values = []
            for month in sorted(monthly_data.keys()):
                if measurement_type in monthly_data[month]:
                    monthly_values.append(monthly_data[month][measurement_type])
            
            if len(monthly_values) >= 3:
                # Jednoduchý lineárny trend
                n = len(monthly_values)
                x_sum = sum(range(n))
                y_sum = sum(monthly_values)
                xy_sum = sum(i * val for i, val in enumerate(monthly_values))
                x2_sum = sum(i * i for i in range(n))
                
                if n * x2_sum - x_sum * x_sum != 0:
                    slope = (n * xy_sum - x_sum * y_sum) / (n * x2_sum - x_sum * x_sum)
                    trends[measurement_type] = {
                        'trend_slope': slope,
                        'trend_direction': 'increasing' if slope > 0 else 'decreasing' if slope < 0 else 'stable',
                        'average_monthly_consumption': statistics.mean(monthly_values),
                        'monthly_values': monthly_values
                    }
        
        return {
            'monthly_data': monthly_data,
            'trends': trends,
            'analysis_period_months': len(monthly_data)
        }
    
    def _generate_performance_recommendations(self, performance_assessment: Dict) -> List[str]:
        """Generovanie odporúčaní na základe výkonnosti"""
        recommendations = []
        
        for measurement_type, assessment in performance_assessment.items():
            status = assessment['status']
            achievement_rate = assessment['achievement_rate']
            
            if status == PerformanceStatus.CRITICAL.value:
                recommendations.append(
                    f"Kritická situácia pre {measurement_type}: úspory dosahujú len {achievement_rate:.1f}% "
                    "cieľa. Potrebné okamžité riešenie a revízia opatrení."
                )
            elif status == PerformanceStatus.BELOW.value:
                recommendations.append(
                    f"Podpriemerný výkon pre {measurement_type}: úspory {achievement_rate:.1f}% cieľa. "
                    "Odporúčame kontrolu a optimalizáciu systémov."
                )
            elif status == PerformanceStatus.EXCEEDS.value:
                recommendations.append(
                    f"Vynikajúci výkon pre {measurement_type}: úspory {achievement_rate:.1f}% cieľa. "
                    "Možnosť replikovať úspešné postupy na iné objekty."
                )
        
        return recommendations

def get_energy_monitoring_system():
    """Factory funkcia pre získanie monitorovacieho systému"""
    return EnergyMonitoringSystem()

if __name__ == "__main__":
    # Test základnej funkcionality
    monitoring = EnergyMonitoringSystem()
    
    # Vytvorenie M&V plánu
    mv_plan = monitoring.create_mv_plan(
        project_id="TEST001",
        mv_option=MVOption.OPTION_B,
        baseline_start=datetime(2023, 1, 1),
        baseline_end=datetime(2023, 12, 31),
        measurement_types=[MeasurementType.ELECTRICITY, MeasurementType.HEATING],
        savings_targets={
            MeasurementType.ELECTRICITY: 5000,  # kWh/rok
            MeasurementType.HEATING: 15000      # kWh/rok
        }
    )
    
    print(f"Vytvorený M&V plán s opciou {mv_plan.mv_option.value}")
    print(f"Požadovaná presnosť: {mv_plan.accuracy_requirements}")