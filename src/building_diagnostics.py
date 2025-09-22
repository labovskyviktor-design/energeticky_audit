"""
Diagnostické metódy pre energetický audit budov
Implementuje termovízie, blower door testy, meranie teploty a vlhkosti, atď.
"""

import math
from typing import Dict, List, Tuple, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import statistics

try:
    from .config import ENERGY_CONSTANTS
    from .thermal_analysis import Construction, MaterialLayer
except ImportError:
    from config import ENERGY_CONSTANTS
    from thermal_analysis import Construction, MaterialLayer


class DiagnosticMethod(Enum):
    """Typy diagnostických metód"""
    THERMOGRAPHY = "thermography"  # Termovízia
    BLOWER_DOOR = "blower_door"  # Blower door test
    MOISTURE_MEASUREMENT = "moisture"  # Meranie vlhkosti
    AIR_QUALITY = "air_quality"  # Kvalita vzduchu
    TEMPERATURE_LOGGING = "temperature_logging"  # Záznam teploty
    SOUND_MEASUREMENT = "sound"  # Akustické merania
    VIBRATION_ANALYSIS = "vibration"  # Vibračná analýza


class SeverityLevel(Enum):
    """Úrovne závažnosti problémov"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class ThermalImage:
    """Termovízny snímok"""
    location: str
    timestamp: datetime
    min_temperature: float  # °C
    max_temperature: float  # °C
    avg_temperature: float  # °C
    temperature_difference: float  # ΔT °C
    thermal_anomalies: List[Dict[str, Any]] = field(default_factory=list)
    image_path: Optional[str] = None
    
    @property
    def temperature_range(self) -> float:
        """Teplotný rozsah snímky"""
        return self.max_temperature - self.min_temperature


@dataclass
class BlowerDoorTest:
    """Blower door test (test vzduchotesnosti)"""
    test_date: datetime
    building_volume: float  # m³
    test_pressure: float = 50.0  # Pa
    air_leakage_rate: Optional[float] = None  # m³/h
    n50_value: Optional[float] = None  # h⁻¹
    q50_value: Optional[float] = None  # m³/h/m²
    envelope_area: Optional[float] = None  # m²
    leak_locations: List[Dict[str, Any]] = field(default_factory=list)
    
    def calculate_air_change_rate(self):
        """Výpočet výmeny vzduchu n50"""
        if self.air_leakage_rate and self.building_volume:
            self.n50_value = self.air_leakage_rate / self.building_volume
    
    def calculate_specific_leakage(self):
        """Výpočet špecifického priesaku q50"""
        if self.air_leakage_rate and self.envelope_area:
            self.q50_value = self.air_leakage_rate / self.envelope_area


@dataclass
class MoistureReading:
    """Meranie vlhkosti"""
    location: str
    timestamp: datetime
    surface_moisture: Optional[float] = None  # % 
    material_moisture: Optional[float] = None  # %
    relative_humidity: Optional[float] = None  # %
    temperature: Optional[float] = None  # °C
    dew_point: Optional[float] = None  # °C
    material_type: Optional[str] = None
    
    def calculate_dew_point(self):
        """Výpočet rosného bodu"""
        if self.relative_humidity and self.temperature:
            rh = self.relative_humidity / 100
            temp = self.temperature
            
            # Magnus formula
            a = 17.27
            b = 237.7
            
            gamma = (a * temp) / (b + temp) + math.log(rh)
            self.dew_point = (b * gamma) / (a - gamma)


@dataclass 
class AirQualityMeasurement:
    """Meranie kvality vzduchu"""
    location: str
    timestamp: datetime
    co2_level: Optional[float] = None  # ppm
    co_level: Optional[float] = None  # ppm
    voc_level: Optional[float] = None  # μg/m³
    pm25_level: Optional[float] = None  # μg/m³
    pm10_level: Optional[float] = None  # μg/m³
    formaldehyde: Optional[float] = None  # μg/m³
    radon_level: Optional[float] = None  # Bq/m³
    
    def assess_air_quality(self) -> Dict[str, str]:
        """Hodnotenie kvality vzduchu"""
        assessment = {}
        
        if self.co2_level:
            if self.co2_level < 800:
                assessment['co2'] = 'Výborná'
            elif self.co2_level < 1200:
                assessment['co2'] = 'Dobrá'
            elif self.co2_level < 1500:
                assessment['co2'] = 'Stredná'
            else:
                assessment['co2'] = 'Nevyhovujúca'
        
        if self.radon_level:
            if self.radon_level < 200:
                assessment['radon'] = 'Bezpečná'
            elif self.radon_level < 400:
                assessment['radon'] = 'Zvýšená pozornosť'
            else:
                assessment['radon'] = 'Vysoké riziko'
        
        if self.pm25_level:
            if self.pm25_level < 15:
                assessment['pm25'] = 'Výborná'
            elif self.pm25_level < 25:
                assessment['pm25'] = 'Dobrá'
            elif self.pm25_level < 40:
                assessment['pm25'] = 'Znečistená'
            else:
                assessment['pm25'] = 'Veľmi znečistená'
        
        return assessment


@dataclass
class TemperatureLogger:
    """Dlhodobý záznam teplôt"""
    location: str
    start_time: datetime
    end_time: datetime
    readings: List[Tuple[datetime, float]] = field(default_factory=list)  # (čas, teplota)
    
    def add_reading(self, timestamp: datetime, temperature: float):
        """Pridanie merania"""
        self.readings.append((timestamp, temperature))
        self.readings.sort(key=lambda x: x[0])
    
    def get_statistics(self) -> Dict[str, float]:
        """Štatistiky teplôt"""
        if not self.readings:
            return {}
        
        temperatures = [reading[1] for reading in self.readings]
        
        return {
            'min_temperature': min(temperatures),
            'max_temperature': max(temperatures),
            'avg_temperature': statistics.mean(temperatures),
            'median_temperature': statistics.median(temperatures),
            'temperature_range': max(temperatures) - min(temperatures),
            'std_deviation': statistics.stdev(temperatures) if len(temperatures) > 1 else 0
        }
    
    def analyze_temperature_stability(self) -> Dict[str, Any]:
        """Analýza stability teploty"""
        stats = self.get_statistics()
        
        # Hodnotenie stability
        std_dev = stats.get('std_deviation', 0)
        if std_dev < 0.5:
            stability = 'Veľmi stabilná'
        elif std_dev < 1.0:
            stability = 'Stabilná'
        elif std_dev < 2.0:
            stability = 'Mierne nestabilná'
        else:
            stability = 'Nestabilná'
        
        # Počet extrémnych hodnôt
        avg = stats.get('avg_temperature', 20)
        extreme_count = sum(1 for _, temp in self.readings if abs(temp - avg) > 3.0)
        
        return {
            **stats,
            'stability_rating': stability,
            'extreme_readings_count': extreme_count,
            'extreme_readings_percent': (extreme_count / len(self.readings)) * 100 if self.readings else 0
        }


class BuildingDiagnostics:
    """Diagnostika budov - hlavná trieda"""
    
    def __init__(self):
        """Inicializácia diagnostiky"""
        self.thermal_images: List[ThermalImage] = []
        self.blower_door_tests: List[BlowerDoorTest] = []
        self.moisture_readings: List[MoistureReading] = []
        self.air_quality_measurements: List[AirQualityMeasurement] = []
        self.temperature_loggers: List[TemperatureLogger] = []
    
    def add_thermal_image(self, image: ThermalImage):
        """Pridanie termovízneho snímku"""
        self.thermal_images.append(image)
    
    def add_blower_door_test(self, test: BlowerDoorTest):
        """Pridanie blower door testu"""
        test.calculate_air_change_rate()
        test.calculate_specific_leakage()
        self.blower_door_tests.append(test)
    
    def analyze_thermal_anomalies(self, image: ThermalImage, 
                                normal_temp_range: Tuple[float, float] = (18.0, 22.0)) -> List[Dict[str, Any]]:
        """
        Analýza tepelných anomálií z termovízneho snímku
        
        Args:
            image: Termovízny snímok
            normal_temp_range: Normálny teplotný rozsah (min, max)
            
        Returns:
            Zoznam tepelných anomálií
        """
        anomalies = []
        
        # Studené miesta (tepelné mostíky)
        if image.min_temperature < normal_temp_range[0]:
            severity = SeverityLevel.HIGH if image.min_temperature < 10 else SeverityLevel.MEDIUM
            anomalies.append({
                'type': 'cold_spot',
                'temperature': image.min_temperature,
                'severity': severity.value,
                'description': f'Studené miesto s teplotou {image.min_temperature:.1f}°C',
                'likely_cause': 'Tepelný mostík, nedostatočná izolácia',
                'recommendation': 'Doplniť izoláciu, utesniť tepelný mostík'
            })
        
        # Horúce miesta (úniky tepla)
        if image.max_temperature > normal_temp_range[1] + 5:
            severity = SeverityLevel.HIGH if image.max_temperature > 30 else SeverityLevel.MEDIUM
            anomalies.append({
                'type': 'hot_spot',
                'temperature': image.max_temperature,
                'severity': severity.value,
                'description': f'Horúce miesto s teplotou {image.max_temperature:.1f}°C',
                'likely_cause': 'Úniky tepla, prehrievanie',
                'recommendation': 'Kontrola izolácie, ventilačných otvorov'
            })
        
        # Vysoký teplotný gradient
        if image.temperature_range > 10:
            severity = SeverityLevel.HIGH if image.temperature_range > 20 else SeverityLevel.MEDIUM
            anomalies.append({
                'type': 'high_gradient',
                'temperature_range': image.temperature_range,
                'severity': severity.value,
                'description': f'Vysoký teplotný gradient {image.temperature_range:.1f}K',
                'likely_cause': 'Nerovnomerná izolácia, tepelné mostíky',
                'recommendation': 'Vyrovnanie tepelnoizolačných vlastností'
            })
        
        return anomalies
    
    def evaluate_airtightness(self, test: BlowerDoorTest) -> Dict[str, Any]:
        """
        Hodnotenie vzduchotesnosti budovy
        
        Args:
            test: Blower door test
            
        Returns:
            Hodnotenie vzduchotesnosti
        """
        if not test.n50_value:
            return {'error': 'Chýbajú údaje o n50 hodnote'}
        
        n50 = test.n50_value
        
        # Klasifikácia podľa STN EN ISO 13829
        if n50 <= 1.0:
            category = 'Výborná (Pasívny dom)'
            rating = 'A+'
        elif n50 <= 1.5:
            category = 'Veľmi dobrá (Nízkoenergetický dom)'
            rating = 'A'
        elif n50 <= 3.0:
            category = 'Dobrá'
            rating = 'B'
        elif n50 <= 5.0:
            category = 'Stredná'
            rating = 'C'
        elif n50 <= 7.0:
            category = 'Podpriemerná'
            rating = 'D'
        else:
            category = 'Nevyhovujúca'
            rating = 'E'
        
        # Odhad energetických strát
        annual_air_change = n50 * 0.05  # zjednodušený prepočet na prirodzenú ventiláciu
        if test.building_volume:
            annual_air_loss = annual_air_change * test.building_volume * 8760  # m³/rok
            # Energetická strata (zjednodušene)
            energy_loss = annual_air_loss * 0.34 * 20 / 1000  # kWh/rok (ρcp = 0.34 Wh/m³K, ΔT = 20K)
        else:
            energy_loss = 0
        
        return {
            'n50_value': n50,
            'category': category,
            'rating': rating,
            'annual_energy_loss_kwh': energy_loss,
            'improvement_potential': self._get_airtightness_improvements(n50),
            'meets_passive_house_standard': n50 <= 0.6,
            'meets_low_energy_standard': n50 <= 1.5
        }
    
    def _get_airtightness_improvements(self, n50: float) -> List[str]:
        """Návr náhovy na zlepšenie vzduchotesnosti"""
        improvements = []
        
        if n50 > 5.0:
            improvements.extend([
                'Kompletné utesnenie budovy - okná, dvere',
                'Kontrola a utesnenie prestupov',
                'Parotesná vrstva v konštrukciách'
            ])
        elif n50 > 3.0:
            improvements.extend([
                'Utesnenie okien a dverí',
                'Kontrola prestupov inštalácií',
                'Doplnenie tesniacich pásov'
            ])
        elif n50 > 1.5:
            improvements.extend([
                'Jemné dotesnenie kritických miest',
                'Kontrola ventilačných otvorov',
                'Údržba tesnení'
            ])
        
        return improvements
    
    def analyze_moisture_problems(self, readings: List[MoistureReading]) -> Dict[str, Any]:
        """
        Analýza problémov s vlhkosťou
        
        Args:
            readings: Merania vlhkosti
            
        Returns:
            Analýza problémov s vlhkosťou
        """
        problems = []
        critical_locations = []
        recommendations = []
        
        for reading in readings:
            reading.calculate_dew_point()
            
            issues_found = []
            
            # Vysoká povrchová vlhkosť
            if reading.surface_moisture and reading.surface_moisture > 80:
                issues_found.append('Vysoká povrchová vlhkosť')
                if reading.surface_moisture > 95:
                    critical_locations.append(reading.location)
            
            # Vysoká vlhkosť materiálu
            if reading.material_moisture and reading.material_moisture > 20:
                issues_found.append('Vysoká vlhkosť materiálu')
                if reading.material_moisture > 30:
                    critical_locations.append(reading.location)
            
            # Riziko kondenzácie
            if (reading.temperature and reading.dew_point and 
                reading.temperature - reading.dew_point < 3):
                issues_found.append('Riziko kondenzácie')
                if reading.temperature - reading.dew_point < 1:
                    critical_locations.append(reading.location)
            
            if issues_found:
                problems.append({
                    'location': reading.location,
                    'issues': issues_found,
                    'surface_moisture': reading.surface_moisture,
                    'material_moisture': reading.material_moisture,
                    'temperature': reading.temperature,
                    'dew_point': reading.dew_point,
                    'severity': SeverityLevel.CRITICAL.value if reading.location in critical_locations else SeverityLevel.MEDIUM.value
                })
        
        # Odporúčania na základe problémov
        if critical_locations:
            recommendations.extend([
                'Okamžité riešenie kritických miest',
                'Zlepšenie vetrania v postihnutých oblastiach',
                'Kontrola hydroizolácie'
            ])
        
        if problems:
            recommendations.extend([
                'Zlepšenie tepelnej izolácie',
                'Úprava vnútornej vlhkosti',
                'Pravidelné meranie vlhkosti'
            ])
        
        return {
            'problems_found': len(problems),
            'critical_locations': len(critical_locations),
            'problem_details': problems,
            'recommendations': recommendations,
            'overall_assessment': self._assess_moisture_risk(problems)
        }
    
    def _assess_moisture_risk(self, problems: List[Dict]) -> str:
        """Celkové hodnotenie rizika vlhkosti"""
        if not problems:
            return 'Bez problémov s vlhkosťou'
        
        critical_count = sum(1 for p in problems if p['severity'] == 'critical')
        
        if critical_count > 2:
            return 'Vysoké riziko - nutné okamžité riešenie'
        elif critical_count > 0:
            return 'Stredné riziko - potrebné riešenie'
        else:
            return 'Nízke riziko - preventívne opatrenia'
    
    def generate_diagnostic_report(self) -> Dict[str, Any]:
        """
        Generovanie komplexnej diagnostickej správy
        
        Returns:
            Diagnostická správa
        """
        report = {
            'report_date': datetime.now().isoformat(),
            'summary': {},
            'thermal_analysis': {},
            'airtightness_analysis': {},
            'moisture_analysis': {},
            'air_quality_analysis': {},
            'recommendations': [],
            'priority_actions': []
        }
        
        # Termovízna analýza
        if self.thermal_images:
            all_anomalies = []
            for image in self.thermal_images:
                anomalies = self.analyze_thermal_anomalies(image)
                all_anomalies.extend(anomalies)
            
            report['thermal_analysis'] = {
                'images_analyzed': len(self.thermal_images),
                'anomalies_found': len(all_anomalies),
                'critical_issues': len([a for a in all_anomalies if a['severity'] == 'high']),
                'details': all_anomalies
            }
        
        # Vzduchotesnosť
        if self.blower_door_tests:
            latest_test = max(self.blower_door_tests, key=lambda t: t.test_date)
            airtightness = self.evaluate_airtightness(latest_test)
            report['airtightness_analysis'] = airtightness
        
        # Vlhkosť
        if self.moisture_readings:
            moisture_analysis = self.analyze_moisture_problems(self.moisture_readings)
            report['moisture_analysis'] = moisture_analysis
        
        # Kvalita vzduchu
        if self.air_quality_measurements:
            latest_air_quality = max(self.air_quality_measurements, key=lambda m: m.timestamp)
            air_assessment = latest_air_quality.assess_air_quality()
            report['air_quality_analysis'] = {
                'latest_measurement': latest_air_quality.timestamp.isoformat(),
                'assessment': air_assessment
            }
        
        # Súhrn a prioritné akcie
        report['summary'] = self._create_summary(report)
        report['priority_actions'] = self._identify_priority_actions(report)
        
        return report
    
    def _create_summary(self, report: Dict[str, Any]) -> Dict[str, str]:
        """Vytvorenie súhrnu diagnostiky"""
        summary = {}
        
        # Tepelná analýza
        thermal = report.get('thermal_analysis', {})
        if thermal:
            critical = thermal.get('critical_issues', 0)
            if critical > 5:
                summary['thermal'] = 'Vážne tepelné problémy'
            elif critical > 2:
                summary['thermal'] = 'Mierne tepelné problémy'
            else:
                summary['thermal'] = 'Bez väčších tepelných problémov'
        
        # Vzduchotesnosť
        airtightness = report.get('airtightness_analysis', {})
        if airtightness:
            summary['airtightness'] = airtightness.get('category', 'Nedefinované')
        
        # Vlhkosť
        moisture = report.get('moisture_analysis', {})
        if moisture:
            summary['moisture'] = moisture.get('overall_assessment', 'Nedefinované')
        
        return summary
    
    def _identify_priority_actions(self, report: Dict[str, Any]) -> List[str]:
        """Identifikácia prioritných akcií"""
        actions = []
        
        # Na základe tepelnej analýzy
        thermal = report.get('thermal_analysis', {})
        if thermal.get('critical_issues', 0) > 0:
            actions.append('Riešenie kritických tepelných mostíkov')
        
        # Na základe vzduchotesnosti
        airtightness = report.get('airtightness_analysis', {})
        if airtightness.get('n50_value', 0) > 3.0:
            actions.append('Zlepšenie vzduchotesnosti budovy')
        
        # Na základe vlhkosti
        moisture = report.get('moisture_analysis', {})
        if moisture.get('critical_locations', 0) > 0:
            actions.append('Urgentné riešenie vlhkostných problémov')
        
        # Na základe kvality vzduchu
        air_quality = report.get('air_quality_analysis', {})
        if air_quality:
            assessment = air_quality.get('assessment', {})
            if 'Vysoké riziko' in assessment.values():
                actions.append('Zlepšenie kvality vnútorného vzduchu')
        
        return actions[:5]  # Maximálne 5 prioritných akcií


# Globálna inštancia diagnostiky
building_diagnostics = BuildingDiagnostics()


def get_building_diagnostics() -> BuildingDiagnostics:
    """Získanie globálnej inštancie diagnostiky budov"""
    return building_diagnostics