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
    PERFORMANCE_TEST = "performance_test"  # Test výkonnosti


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


@dataclass
class ThermalBridge:
    """Tepelný mostík"""
    location: str
    bridge_type: str  # "linear", "point", "area"
    length_or_area: float  # m alebo m²
    psi_value: Optional[float] = None  # W/mK (pre lineárny)
    chi_value: Optional[float] = None  # W/K (pre bodový)
    u_value_bridge: Optional[float] = None  # W/m²K (pre plošný)
    temperature_factor: Optional[float] = None  # fRsi
    description: str = ""
    mitigation_measures: List[str] = field(default_factory=list)
    
    def calculate_heat_loss(self, temperature_difference: float = 35.0) -> float:
        """Výpočet tepelnej straty mostíkom"""
        if self.bridge_type == "linear" and self.psi_value:
            return self.psi_value * self.length_or_area * temperature_difference
        elif self.bridge_type == "point" and self.chi_value:
            return self.chi_value * temperature_difference
        elif self.bridge_type == "area" and self.u_value_bridge:
            return self.u_value_bridge * self.length_or_area * temperature_difference
        return 0.0


class AdvancedBuildingDiagnostics:
    """Pokročilé diagnostické metódy pre energetické audity"""
    
    def __init__(self):
        """Inicializácia pokročilých diagnostických metód"""
        pass
    
    def analyze_blower_door_comprehensive(self, blower_door_test: BlowerDoorTest, 
                                        building_volume: float, envelope_area: float) -> Dict[str, Any]:
        """
        Komplexná analýza blower door testu podľa IPMVP a EN 13829
        
        Args:
            blower_door_test: Výsledky blower door testu
            building_volume: Objem budovy [m³]
            envelope_area: Plocha obálky [m²]
            
        Returns:
            Detailná analýza vzduchotesnosti
        """
        # Základné hodnoty
        blower_door_test.calculate_air_change_rate()
        blower_door_test.calculate_specific_leakage()
        
        analysis = {
            'basic_results': {
                'n50_value': blower_door_test.n50_value,
                'q50_value': blower_door_test.q50_value,
                'air_leakage_rate': blower_door_test.air_leakage_rate
            }
        }
        
        # Hodnotenie podľa noriem
        analysis['compliance_assessment'] = self._assess_airtightness_compliance(
            blower_door_test.n50_value, blower_door_test.q50_value
        )
        
        # Odhad infiltračných strát
        analysis['infiltration_losses'] = self._calculate_infiltration_losses(
            blower_door_test.n50_value, building_volume
        )
        
        # Analýza únikov
        if blower_door_test.leak_locations:
            analysis['leak_analysis'] = self._analyze_leak_locations(
                blower_door_test.leak_locations
            )
        
        # Odporúčania
        analysis['recommendations'] = self._generate_airtightness_recommendations(
            blower_door_test.n50_value, analysis['leak_analysis'] if 'leak_analysis' in analysis else None
        )
        
        return analysis
    
    def analyze_thermal_bridges_detailed(self, thermal_bridges: List[ThermalBridge],
                                       building_area: float = 100.0) -> Dict[str, Any]:
        """
        Detailná analýza tepelných mostíkov podľa EN ISO 14683
        
        Args:
            thermal_bridges: Zoznam tepelných mostíkov
            building_area: Plocha budovy pre normalizáciu
            
        Returns:
            Komplexná analýza tepelných mostíkov
        """
        if not thermal_bridges:
            return {'error': 'Žiadne tepelné mostíky nie sú definované'}
        
        analysis = {
            'bridge_summary': {
                'total_count': len(thermal_bridges),
                'linear_bridges': len([b for b in thermal_bridges if b.bridge_type == 'linear']),
                'point_bridges': len([b for b in thermal_bridges if b.bridge_type == 'point']),
                'area_bridges': len([b for b in thermal_bridges if b.bridge_type == 'area'])
            }
        }
        
        # Výpočet celkových strát
        total_bridge_loss = sum(bridge.calculate_heat_loss() for bridge in thermal_bridges)
        analysis['total_bridge_loss_w'] = total_bridge_loss
        analysis['specific_bridge_loss'] = total_bridge_loss / building_area
        
        # Analýza jednotlivých mostíkov
        bridge_details = []
        for bridge in thermal_bridges:
            heat_loss = bridge.calculate_heat_loss()
            contribution = (heat_loss / total_bridge_loss * 100) if total_bridge_loss > 0 else 0
            
            bridge_details.append({
                'location': bridge.location,
                'type': bridge.bridge_type,
                'heat_loss_w': heat_loss,
                'contribution_percent': contribution,
                'temperature_factor': bridge.temperature_factor,
                'severity': self._classify_bridge_severity(bridge, heat_loss)
            })
        
        analysis['bridge_details'] = sorted(bridge_details, key=lambda x: x['heat_loss_w'], reverse=True)
        
        # Hodnotenie celkového vplyvu
        if analysis['specific_bridge_loss'] < 0.02:
            analysis['overall_assessment'] = "Minimálny vplyv tepelných mostíkov"
        elif analysis['specific_bridge_loss'] < 0.05:
            analysis['overall_assessment'] = "Mierny vplyv tepelných mostíkov"
        elif analysis['specific_bridge_loss'] < 0.10:
            analysis['overall_assessment'] = "Značný vplyv tepelných mostíkov"
        else:
            analysis['overall_assessment'] = "Kritický vplyv tepelných mostíkov"
        
        # Odporúčania
        analysis['recommendations'] = self._generate_bridge_recommendations(thermal_bridges, analysis)
        
        return analysis
    
    def _assess_airtightness_compliance(self, n50: Optional[float], q50: Optional[float]) -> Dict[str, Any]:
        """Hodnotenie súladu s normami vzduchotesnosti"""
        compliance = {}
        
        if n50 is not None:
            # Hodnotenie podľa STN EN 12831
            if n50 <= 1.5:
                compliance['stn_rating'] = "Vynikajúca (pasívny dom)"
                compliance['stn_class'] = "A+"
            elif n50 <= 3.0:
                compliance['stn_rating'] = "Veľmi dobrá"
                compliance['stn_class'] = "A"
            elif n50 <= 4.5:
                compliance['stn_rating'] = "Dobrá"
                compliance['stn_class'] = "B"
            elif n50 <= 6.0:
                compliance['stn_rating'] = "Vyhovujúca"
                compliance['stn_class'] = "C"
            else:
                compliance['stn_rating'] = "Nevyhovujúca"
                compliance['stn_class'] = "D"
        
        if q50 is not None:
            # Hodnotenie podľa špecifického úniku
            if q50 <= 1.0:
                compliance['specific_rating'] = "Vynikajúca"
            elif q50 <= 2.0:
                compliance['specific_rating'] = "Veľmi dobrá"
            elif q50 <= 3.0:
                compliance['specific_rating'] = "Dobrá"
            elif q50 <= 4.0:
                compliance['specific_rating'] = "Vyhovujúca"
            else:
                compliance['specific_rating'] = "Nevyhovujúca"
        
        return compliance
    
    def _calculate_infiltration_losses(self, n50: float, building_volume: float, 
                                     wind_shelter_factor: float = 0.05) -> Dict[str, float]:
        """Výpočet infiltračných strát podľa EN ISO 13789"""
        if not n50 or not building_volume:
            return {}
        
        # Prepočet z n50 na prirodzenú infiltráciu
        n_natural = n50 * wind_shelter_factor
        
        # Ročné infiltračné straty pri ΔT = 35K
        annual_volume_flow = n_natural * building_volume * 8760  # m³/rok
        specific_heat_air = 0.34  # Wh/m³K
        temperature_difference = 35  # K
        
        annual_infiltration_loss = (annual_volume_flow * specific_heat_air * 
                                  temperature_difference / 1000)  # kWh/rok
        
        return {
            'natural_air_change_rate': n_natural,
            'annual_volume_flow_m3': annual_volume_flow,
            'annual_infiltration_loss_kwh': annual_infiltration_loss,
            'infiltration_loss_per_m3_volume': annual_infiltration_loss / building_volume
        }
    
    def _analyze_leak_locations(self, leak_locations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analýza miest únikov"""
        if not leak_locations:
            return {}
        
        # Kategorizácia únikov
        categories = {
            'windows_doors': [],
            'penetrations': [],
            'joints': [],
            'envelope': [],
            'other': []
        }
        
        for leak in leak_locations:
            location_type = leak.get('type', 'other')
            severity = leak.get('severity', 'medium')
            
            # Zaradenie do kategórie
            if any(keyword in location_type.lower() for keyword in ['okno', 'dvere', 'window', 'door']):
                categories['windows_doors'].append(leak)
            elif any(keyword in location_type.lower() for keyword in ['prestup', 'penetration', 'pipe']):
                categories['penetrations'].append(leak)
            elif any(keyword in location_type.lower() for keyword in ['spoj', 'joint', 'connection']):
                categories['joints'].append(leak)
            elif any(keyword in location_type.lower() for keyword in ['stena', 'strecha', 'wall', 'roof']):
                categories['envelope'].append(leak)
            else:
                categories['other'].append(leak)
        
        # Štatistiky
        total_leaks = len(leak_locations)
        critical_leaks = sum(1 for leak in leak_locations if leak.get('severity') == 'high')
        
        return {
            'total_leak_count': total_leaks,
            'critical_leak_count': critical_leaks,
            'leak_categories': categories,
            'category_summary': {
                cat: len(leaks) for cat, leaks in categories.items() if leaks
            },
            'priority_locations': [leak for leak in leak_locations if leak.get('severity') == 'high']
        }
    
    def _classify_bridge_severity(self, bridge: ThermalBridge, heat_loss: float) -> str:
        """Klasifikácia závažnosti tepelného mostíka"""
        if heat_loss > 10.0:  # W
            return "Kritický"
        elif heat_loss > 5.0:
            return "Vysoký"
        elif heat_loss > 1.0:
            return "Stredný"
        else:
            return "Nízky"
    
    def _generate_airtightness_recommendations(self, n50: float, 
                                             leak_analysis: Optional[Dict] = None) -> List[str]:
        """Generovanie odporúčaní pre zlepšenie vzduchotesnosti"""
        recommendations = []
        
        if n50 > 6.0:
            recommendations.append("Kritická potreba zlepšenia vzduchotesnosti - komplexné utesnenie")
        elif n50 > 4.5:
            recommendations.append("Potrebné výrazné zlepšenie vzduchotesnosti")
        elif n50 > 3.0:
            recommendations.append("Odporúčané zlepšenie vzduchotesnosti pre vyššiu efektívnosť")
        
        if leak_analysis:
            if leak_analysis.get('critical_leak_count', 0) > 0:
                recommendations.append("Riešenie kritických únikov ako priorita")
            
            category_summary = leak_analysis.get('category_summary', {})
            if category_summary.get('windows_doors', 0) > 0:
                recommendations.append("Kontrola a utesnenie okien a dverí")
            if category_summary.get('penetrations', 0) > 0:
                recommendations.append("Utesnenie prestupov inštalácií")
            if category_summary.get('joints', 0) > 0:
                recommendations.append("Utesnenie stavebných spojov")
        
        if not recommendations:
            recommendations.append("Vzduchotesnosť je na vyhovujúcej úrovni")
        
        return recommendations
    
    def _generate_bridge_recommendations(self, bridges: List[ThermalBridge], 
                                       analysis: Dict) -> List[str]:
        """Generovanie odporúčaní pre tepelné mostíky"""
        recommendations = []
        
        # Top 3 najhorších mostíkov
        top_bridges = analysis['bridge_details'][:3]
        for bridge in top_bridges:
            if bridge['severity'] in ['Kritický', 'Vysoký']:
                recommendations.append(
                    f"Priorita: riešenie tepelného mostíka {bridge['location']} "
                    f"({bridge['heat_loss_w']:.1f} W straty)"
                )
        
        # Všeobecné odporúčania
        if analysis['specific_bridge_loss'] > 0.05:
            recommendations.append("Komplexné riešenie tepelných mostíkov v rámci zateplenia")
            recommendations.append("Použitie prerušovačov tepelných mostíkov pri detailoch")
        
        # Špecifické odporúčania podľa typu
        linear_count = analysis['bridge_summary']['linear_bridges']
        if linear_count > 5:
            recommendations.append("Kontrola a optimalizácia lineárnych tepelných mostíkov")
        
        return recommendations


def get_advanced_building_diagnostics():
    """Factory funkcia pre získanie pokročilej diagnostiky budov"""
    return AdvancedBuildingDiagnostics()
