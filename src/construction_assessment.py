"""
Systém posudzovania stavebných konštrukcií
Obsahuje databázu materiálov, výpočty U-hodnôt a hodnotenie konštrukcií
"""

import math
from typing import Dict, List, Tuple, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
import json

try:
    from .config import ENERGY_CONSTANTS
    from .thermal_analysis import Construction, MaterialLayer, ConstructionType, ThermalBridge, ThermalBridgeType
except ImportError:
    from config import ENERGY_CONSTANTS
    from thermal_analysis import Construction, MaterialLayer, ConstructionType, ThermalBridge, ThermalBridgeType


class ConstructionCategory(Enum):
    """Kategórie konštrukcií"""
    WALLS = "walls"
    ROOFS = "roofs"
    FLOORS = "floors"
    FOUNDATIONS = "foundations"
    WINDOWS = "windows"
    DOORS = "doors"


class MaterialCategory(Enum):
    """Kategórie materiálov"""
    MASONRY = "masonry"  # Murivá
    CONCRETE = "concrete"  # Betóny
    INSULATION = "insulation"  # Izolácie
    WOOD = "wood"  # Drevo
    METAL = "metal"  # Kovy
    PLASTER = "plaster"  # Omietky
    MEMBRANE = "membrane"  # Membrány
    OTHER = "other"  # Ostatné


class ComplianceLevel(Enum):
    """Úrovne súladu s normami"""
    EXCELLENT = "excellent"  # Vynikajúca
    GOOD = "good"  # Dobrá
    SATISFACTORY = "satisfactory"  # Vyhovujúca
    POOR = "poor"  # Nevyhovujúca
    CRITICAL = "critical"  # Kritická


@dataclass
class MaterialProperties:
    """Rozšírené vlastnosti materiálu"""
    name: str
    category: MaterialCategory
    thermal_conductivity: float  # W/mK
    density: float  # kg/m³
    specific_heat: float  # J/kgK
    vapor_resistance: float  # -
    
    # Doplnkové vlastnosti
    compressive_strength: Optional[float] = None  # MPa
    fire_class: Optional[str] = None  # A1, A2, B, C, D, E, F
    durability_class: Optional[str] = None
    environmental_impact: Optional[float] = None  # kg CO2-eq/kg
    cost_per_unit: Optional[float] = None  # €/m³ alebo €/m²
    
    # Certifikácie a normy
    ce_marking: bool = False
    eco_label: Optional[str] = None
    
    def to_material_layer(self, thickness: float) -> MaterialLayer:
        """Konverzia na MaterialLayer pre výpočty"""
        return MaterialLayer(
            name=self.name,
            thickness=thickness,
            thermal_conductivity=self.thermal_conductivity,
            density=self.density,
            specific_heat=self.specific_heat,
            vapor_resistance=self.vapor_resistance
        )


@dataclass
class ConstructionStandard:
    """Štandardy pre stavebné konštrukcie"""
    name: str
    construction_type: ConstructionType
    max_u_value: float  # W/m²K
    recommended_u_value: float  # W/m²K
    min_insulation_thickness: float  # m
    description: str = ""
    applicable_from: Optional[str] = None  # dátum platnosti


@dataclass
class ConstructionAssessment:
    """Hodnotenie konštrukcie"""
    construction: Construction
    compliance_level: ComplianceLevel
    u_value_rating: str
    insulation_adequacy: str
    thermal_bridge_assessment: str
    condensation_risk: str
    recommendations: List[str] = field(default_factory=list)
    estimated_improvement_cost: Optional[float] = None
    estimated_energy_savings: Optional[float] = None


class MaterialDatabase:
    """Databáza stavebných materiálov"""
    
    def __init__(self):
        """Inicializácia databázy materiálov"""
        self.materials: Dict[str, MaterialProperties] = {}
        self._load_default_materials()
    
    def _load_default_materials(self):
        """Načítanie predvolených materiálov"""
        default_materials = {
            # Murivá
            'brick_solid_240': MaterialProperties(
                "Plná tehla 240mm", MaterialCategory.MASONRY, 0.77, 1800, 880, 8,
                compressive_strength=15.0, fire_class="A1", durability_class="High"
            ),
            'brick_hollow_300': MaterialProperties(
                "Dutá tehla 300mm", MaterialCategory.MASONRY, 0.44, 1200, 880, 8,
                compressive_strength=12.0, fire_class="A1", durability_class="High"
            ),
            'aac_200': MaterialProperties(
                "Pórobetón 200mm", MaterialCategory.MASONRY, 0.14, 400, 1000, 5,
                compressive_strength=4.0, fire_class="A1", durability_class="Medium"
            ),
            'aac_300': MaterialProperties(
                "Pórobetón 300mm", MaterialCategory.MASONRY, 0.16, 500, 1000, 5,
                compressive_strength=5.0, fire_class="A1", durability_class="Medium"
            ),
            'aac_365': MaterialProperties(
                "Pórobetón 365mm", MaterialCategory.MASONRY, 0.18, 600, 1000, 5,
                compressive_strength=6.0, fire_class="A1", durability_class="Medium"
            ),
            
            # Betóny
            'concrete_c20_25': MaterialProperties(
                "Betón C20/25", MaterialCategory.CONCRETE, 1.65, 2300, 1000, 70,
                compressive_strength=25.0, fire_class="A1", durability_class="High"
            ),
            'concrete_c25_30': MaterialProperties(
                "Betón C25/30", MaterialCategory.CONCRETE, 1.74, 2400, 1000, 80,
                compressive_strength=30.0, fire_class="A1", durability_class="High"
            ),
            'lightweight_concrete': MaterialProperties(
                "Ľahký betón", MaterialCategory.CONCRETE, 0.55, 1200, 1000, 25,
                compressive_strength=8.0, fire_class="A1", durability_class="Medium"
            ),
            
            # Izolácie
            'eps_040': MaterialProperties(
                "EPS 040", MaterialCategory.INSULATION, 0.040, 15, 1270, 40,
                fire_class="E", environmental_impact=3.8
            ),
            'eps_038': MaterialProperties(
                "EPS 038", MaterialCategory.INSULATION, 0.038, 16, 1270, 50,
                fire_class="E", environmental_impact=3.9
            ),
            'eps_035': MaterialProperties(
                "EPS 035", MaterialCategory.INSULATION, 0.035, 18, 1270, 60,
                fire_class="E", environmental_impact=4.1
            ),
            'xps_032': MaterialProperties(
                "XPS 032", MaterialCategory.INSULATION, 0.032, 32, 1400, 100,
                fire_class="E", environmental_impact=4.5
            ),
            'mineral_wool_040': MaterialProperties(
                "Minerálna vlna 040", MaterialCategory.INSULATION, 0.040, 100, 850, 1,
                fire_class="A1", environmental_impact=1.2
            ),
            'mineral_wool_035': MaterialProperties(
                "Minerálna vlna 035", MaterialCategory.INSULATION, 0.035, 120, 850, 1,
                fire_class="A1", environmental_impact=1.4
            ),
            'pu_foam_025': MaterialProperties(
                "PUR pena 025", MaterialCategory.INSULATION, 0.025, 40, 1400, 50,
                fire_class="B2", environmental_impact=6.2
            ),
            'wood_fiber': MaterialProperties(
                "Drevovláknita izolácia", MaterialCategory.INSULATION, 0.042, 160, 2100, 2,
                fire_class="E", environmental_impact=0.8
            ),
            
            # Drevo
            'wood_spruce': MaterialProperties(
                "Smrekové drevo", MaterialCategory.WOOD, 0.13, 450, 1600, 50,
                fire_class="D", environmental_impact=-1.2
            ),
            'wood_oak': MaterialProperties(
                "Dubové drevo", MaterialCategory.WOOD, 0.17, 650, 1600, 200,
                fire_class="D", environmental_impact=-1.5
            ),
            'glulam': MaterialProperties(
                "Lepené drevo", MaterialCategory.WOOD, 0.13, 380, 1600, 50,
                fire_class="D", environmental_impact=-0.8
            ),
            
            # Omietky
            'cement_plaster': MaterialProperties(
                "Cementová omietka", MaterialCategory.PLASTER, 0.80, 1900, 850, 15,
                fire_class="A1", durability_class="High"
            ),
            'lime_plaster': MaterialProperties(
                "Vápenná omietka", MaterialCategory.PLASTER, 0.70, 1600, 850, 8,
                fire_class="A1", durability_class="Medium"
            ),
            'gypsum_plaster': MaterialProperties(
                "Sadrová omietka", MaterialCategory.PLASTER, 0.40, 1200, 850, 4,
                fire_class="A2", durability_class="Low"
            ),
            'thermal_plaster': MaterialProperties(
                "Tepelnoizolačná omietka", MaterialCategory.PLASTER, 0.12, 600, 1000, 6,
                fire_class="A1", durability_class="Medium"
            ),
            
            # Membrány
            'vapor_barrier': MaterialProperties(
                "Parozábrana", MaterialCategory.MEMBRANE, 0.25, 1300, 1400, 100000,
                fire_class="E"
            ),
            'windproof_membrane': MaterialProperties(
                "Vetrotesná membrána", MaterialCategory.MEMBRANE, 0.25, 400, 1400, 2,
                fire_class="E"
            ),
            'roof_membrane': MaterialProperties(
                "Strešná membrána", MaterialCategory.MEMBRANE, 0.25, 1200, 1400, 50000,
                fire_class="E"
            )
        }
        
        for key, material in default_materials.items():
            self.materials[key] = material
    
    def get_material(self, material_key: str) -> Optional[MaterialProperties]:
        """Získanie materiálu podľa kľúča"""
        return self.materials.get(material_key)
    
    def get_materials_by_category(self, category: MaterialCategory) -> Dict[str, MaterialProperties]:
        """Získanie materiálov podľa kategórie"""
        return {
            key: material for key, material in self.materials.items()
            if material.category == category
        }
    
    def add_material(self, key: str, material: MaterialProperties):
        """Pridanie nového materiálu"""
        self.materials[key] = material
    
    def search_materials(self, query: str) -> Dict[str, MaterialProperties]:
        """Vyhľadanie materiálov podľa názvu"""
        query_lower = query.lower()
        return {
            key: material for key, material in self.materials.items()
            if query_lower in material.name.lower()
        }


class ConstructionStandardsDatabase:
    """Databáza štandardov pre stavebné konštrukcie"""
    
    def __init__(self):
        """Inicializácia databázy štandardov"""
        self.standards: Dict[str, ConstructionStandard] = {}
        self._load_default_standards()
    
    def _load_default_standards(self):
        """Načítanie predvolených štandardov"""
        standards = {
            # Obvodové steny
            'wall_existing': ConstructionStandard(
                "Existujúce budovy - obvodové steny", ConstructionType.EXTERNAL_WALL,
                1.45, 0.25, 0.08, "Pre existujúce budovy do roku 1990", "1990-01-01"
            ),
            'wall_new_2006': ConstructionStandard(
                "Nové budovy 2006 - obvodové steny", ConstructionType.EXTERNAL_WALL,
                0.46, 0.25, 0.12, "STN 73 0540-2 od roku 2006", "2006-01-01"
            ),
            'wall_new_2012': ConstructionStandard(
                "Nové budovy 2012 - obvodové steny", ConstructionType.EXTERNAL_WALL,
                0.32, 0.20, 0.15, "STN 73 0540-2 od roku 2012", "2012-01-01"
            ),
            'wall_passive': ConstructionStandard(
                "Pasívne domy - obvodové steny", ConstructionType.EXTERNAL_WALL,
                0.15, 0.10, 0.25, "Štandard pre pasívne domy", "2010-01-01"
            ),
            
            # Strechy
            'roof_existing': ConstructionStandard(
                "Existujúce budovy - strechy", ConstructionType.ROOF,
                1.45, 0.20, 0.10, "Pre existujúce budovy do roku 1990", "1990-01-01"
            ),
            'roof_new_2006': ConstructionStandard(
                "Nové budovy 2006 - strechy", ConstructionType.ROOF,
                0.32, 0.16, 0.16, "STN 73 0540-2 od roku 2006", "2006-01-01"
            ),
            'roof_new_2012': ConstructionStandard(
                "Nové budovy 2012 - strechy", ConstructionType.ROOF,
                0.20, 0.15, 0.20, "STN 73 0540-2 od roku 2012", "2012-01-01"
            ),
            'roof_passive': ConstructionStandard(
                "Pasívne domy - strechy", ConstructionType.ROOF,
                0.12, 0.08, 0.30, "Štandard pre pasívne domy", "2010-01-01"
            ),
            
            # Podlahy
            'floor_existing': ConstructionStandard(
                "Existujúce budovy - podlahy", ConstructionType.FLOOR,
                1.45, 0.40, 0.05, "Pre existujúce budovy do roku 1990", "1990-01-01"
            ),
            'floor_new_2006': ConstructionStandard(
                "Nové budovy 2006 - podlahy", ConstructionType.FLOOR,
                0.60, 0.30, 0.08, "STN 73 0540-2 od roku 2006", "2006-01-01"
            ),
            'floor_new_2012': ConstructionStandard(
                "Nové budovy 2012 - podlahy", ConstructionType.FLOOR,
                0.32, 0.22, 0.12, "STN 73 0540-2 od roku 2012", "2012-01-01"
            ),
            'floor_passive': ConstructionStandard(
                "Pasívne domy - podlahy", ConstructionType.FLOOR,
                0.15, 0.10, 0.20, "Štandard pre pasívne domy", "2010-01-01"
            ),
            
            # Okná
            'windows_existing': ConstructionStandard(
                "Existujúce budovy - okná", ConstructionType.WINDOW,
                2.80, 1.40, 0.0, "Pre existujúce budovy do roku 2006", "1990-01-01"
            ),
            'windows_new_2012': ConstructionStandard(
                "Nové budovy 2012 - okná", ConstructionType.WINDOW,
                1.40, 1.00, 0.0, "STN 73 0540-2 od roku 2012", "2012-01-01"
            ),
            'windows_passive': ConstructionStandard(
                "Pasívne domy - okná", ConstructionType.WINDOW,
                0.80, 0.60, 0.0, "Štandard pre pasívne domy", "2010-01-01"
            )
        }
        
        for key, standard in standards.items():
            self.standards[key] = standard
    
    def get_applicable_standards(self, construction_type: ConstructionType) -> List[ConstructionStandard]:
        """Získanie aplikovateľných štandardov pre typ konštrukcie"""
        return [
            standard for standard in self.standards.values()
            if standard.construction_type == construction_type
        ]


class ConstructionAssessor:
    """Hodnotič stavebných konštrukcií"""
    
    def __init__(self):
        """Inicializácia hodnotiteľa"""
        self.material_db = MaterialDatabase()
        self.standards_db = ConstructionStandardsDatabase()
    
    def assess_construction(self, construction: Construction, 
                          target_standard: str = 'wall_new_2012') -> ConstructionAssessment:
        """
        Komplexné hodnotenie stavebnej konštrukcie
        
        Args:
            construction: Stavebná konštrukcia
            target_standard: Cieľový štandard
            
        Returns:
            Hodnotenie konštrukcie
        """
        standard = self.standards_db.standards.get(target_standard)
        if not standard:
            raise ValueError(f"Neznámy štandard: {target_standard}")
        
        # U-hodnota hodnotenie
        u_value_rating = self._assess_u_value(construction.u_value, standard)
        
        # Hodnotenie izolácie
        insulation_adequacy = self._assess_insulation(construction, standard)
        
        # Hodnotenie tepelných mostíkov
        thermal_bridge_assessment = self._assess_thermal_bridges(construction)
        
        # Celkové hodnotenie súladu
        compliance_level = self._determine_compliance_level(
            construction.u_value, standard, len(construction.thermal_bridges)
        )
        
        # Odporúčania
        recommendations = self._generate_recommendations(construction, standard, compliance_level)
        
        return ConstructionAssessment(
            construction=construction,
            compliance_level=compliance_level,
            u_value_rating=u_value_rating,
            insulation_adequacy=insulation_adequacy,
            thermal_bridge_assessment=thermal_bridge_assessment,
            condensation_risk=self._assess_condensation_risk(construction),
            recommendations=recommendations
        )
    
    def _assess_u_value(self, u_value: float, standard: ConstructionStandard) -> str:
        """Hodnotenie U-hodnoty"""
        if u_value <= standard.recommended_u_value:
            return f"Vynikajúca (U = {u_value:.3f} W/m²K)"
        elif u_value <= standard.max_u_value * 0.8:
            return f"Veľmi dobrá (U = {u_value:.3f} W/m²K)"
        elif u_value <= standard.max_u_value:
            return f"Vyhovujúca (U = {u_value:.3f} W/m²K)"
        elif u_value <= standard.max_u_value * 1.2:
            return f"Podpriemerná (U = {u_value:.3f} W/m²K)"
        else:
            return f"Nevyhovujúca (U = {u_value:.3f} W/m²K)"
    
    def _assess_insulation(self, construction: Construction, standard: ConstructionStandard) -> str:
        """Hodnotenie tepelnej izolácie"""
        insulation_layers = [
            layer for layer in construction.layers
            if layer.thermal_conductivity < 0.1  # Izolácie majú λ < 0.1 W/mK
        ]
        
        total_insulation_thickness = sum(layer.thickness for layer in insulation_layers)
        
        if total_insulation_thickness >= standard.min_insulation_thickness * 1.5:
            return f"Nadštandardná izolácia ({total_insulation_thickness*100:.0f} cm)"
        elif total_insulation_thickness >= standard.min_insulation_thickness:
            return f"Vyhovujúca izolácia ({total_insulation_thickness*100:.0f} cm)"
        elif total_insulation_thickness >= standard.min_insulation_thickness * 0.7:
            return f"Nedostatočná izolácia ({total_insulation_thickness*100:.0f} cm)"
        else:
            return f"Kriticky nedostatočná izolácia ({total_insulation_thickness*100:.0f} cm)"
    
    def _assess_thermal_bridges(self, construction: Construction) -> str:
        """Hodnotenie tepelných mostíkov"""
        if not construction.thermal_bridges:
            return "Tepelné mostíky nie sú definované"
        
        total_bridge_loss = construction.thermal_bridge_losses
        bridge_effect = total_bridge_loss / construction.area if construction.area > 0 else 0
        
        if bridge_effect < 0.02:
            return f"Minimálne tepelné mostíky ({bridge_effect:.3f} W/m²K)"
        elif bridge_effect < 0.05:
            return f"Mierny vplyv tepelných mostíkov ({bridge_effect:.3f} W/m²K)"
        elif bridge_effect < 0.10:
            return f"Značný vplyv tepelných mostíkov ({bridge_effect:.3f} W/m²K)"
        else:
            return f"Kritické tepelné mostíky ({bridge_effect:.3f} W/m²K)"
    
    def _determine_compliance_level(self, u_value: float, standard: ConstructionStandard, 
                                  bridge_count: int) -> ComplianceLevel:
        """Určenie celkovej úrovne súladu"""
        if u_value <= standard.recommended_u_value and bridge_count == 0:
            return ComplianceLevel.EXCELLENT
        elif u_value <= standard.max_u_value * 0.8:
            return ComplianceLevel.GOOD
        elif u_value <= standard.max_u_value:
            return ComplianceLevel.SATISFACTORY
        elif u_value <= standard.max_u_value * 1.5:
            return ComplianceLevel.POOR
        else:
            return ComplianceLevel.CRITICAL
    
    def _generate_recommendations(self, construction: Construction, standard: ConstructionStandard,
                                compliance: ComplianceLevel) -> List[str]:
        """Generovanie odporúčaní pre zlepšenie"""
        recommendations = []
        
        if compliance in [ComplianceLevel.POOR, ComplianceLevel.CRITICAL]:
            if construction.u_value > standard.max_u_value:
                recommendations.append(
                    f"Nutné zlepšenie tepelnoizolačných vlastností - súčasná U-hodnota "
                    f"{construction.u_value:.3f} W/m²K presahuje normu {standard.max_u_value} W/m²K"
                )
            
            # Návrh hrúbky izolácie
            required_additional_insulation = self._calculate_required_insulation(construction, standard)
            if required_additional_insulation > 0:
                recommendations.append(
                    f"Odporúčané pridanie {required_additional_insulation*100:.0f} cm tepelnej izolácie"
                )
        
        if construction.thermal_bridges:
            bridge_effect = construction.thermal_bridge_losses / construction.area
            if bridge_effect > 0.05:
                recommendations.append("Riešenie tepelných mostíkov - utesnenie, prerušenie")
        
        if compliance == ComplianceLevel.SATISFACTORY:
            recommendations.append("Konštrukcia spĺňa minimálne požiadavky, odporúčané zlepšenie pre vyššiu efektívnosť")
        
        return recommendations
    
    def _calculate_required_insulation(self, construction: Construction, 
                                     standard: ConstructionStandard) -> float:
        """Výpočet potrebnej dodatočnej izolácie"""
        if construction.u_value <= standard.max_u_value:
            return 0.0
        
        # Zjednodušený výpočet potrebnej dodatočnej izolácie
        current_resistance = construction.thermal_resistance
        required_resistance = 1.0 / standard.max_u_value
        additional_resistance = required_resistance - current_resistance
        
        # Predpokladáme EPS izoláciu s λ = 0.040 W/mK
        additional_thickness = additional_resistance * 0.040
        
        return additional_thickness
    
    def _assess_condensation_risk(self, construction: Construction) -> str:
        """
        Hodnotenie rizika kondenzácie pomocou Glaserovej metódy
        
        Args:
            construction: Stavebná konštrukcia
            
        Returns:
            Hodnotenie rizika kondenzácie
        """
        try:
            # Základné klimatické parametre pre Slovensko
            exterior_temp = -12.0  # °C (exteriérová teplota)
            interior_temp = 20.0   # °C (interiérová teplota)
            exterior_rh = 85.0     # % (vonkajšia relatívna vlhkosť)
            interior_rh = 50.0     # % (vnútorná relatívna vlhkosť)
            
            # Výpočet teplôt v jednotlivých vrstvách
            layer_temperatures = self._calculate_layer_temperatures(
                construction, exterior_temp, interior_temp
            )
            
            # Výpočet parciálnych tlakov vodnej pary
            vapor_pressures = self._calculate_vapor_pressures(
                construction, exterior_rh, interior_rh, layer_temperatures
            )
            
            # Hodnotenie kondenzácie
            condensation_layers = []
            
            for i, (temp, vapor_pressure) in enumerate(zip(layer_temperatures, vapor_pressures)):
                # Výpočet saturačného tlaku pri danej teplote
                saturation_pressure = self._calculate_saturation_pressure(temp)
                
                # Kontrola kondenzácie
                if vapor_pressure > saturation_pressure:
                    condensation_layers.append(i)
            
            # Výsledné hodnotenie
            if not condensation_layers:
                return "Bez rizika kondenzácie"
            elif len(condensation_layers) == 1 and condensation_layers[0] == 0:
                return "Povrchová kondenzácia - kontrolovať tepelné mostíky"
            elif any(i > 0 and i < len(construction.layers)-1 for i in condensation_layers):
                return "Kritické riziko - kondenzácia vo vnútri konštrukcie"
            else:
                return "Mierneho riziko kondenzácie"
                
        except Exception as e:
            return f"Chyba pri výpočte kondenzácie: {str(e)}"
    
    def _calculate_layer_temperatures(self, construction: Construction, 
                                    t_ext: float, t_int: float) -> List[float]:
        """
        Výpočet teplôt v jednotlivých vrstvách konštrukcie
        
        Args:
            construction: Stavebná konštrukcia
            t_ext: Vonkajšia teplota [°C]
            t_int: Vnútorná teplota [°C]
            
        Returns:
            Zoznam teplôt v jednotlivých vrstvách
        """
        temperatures = [t_ext]  # Začíname vonkajšou teplotou
        
        # Tepelné odpory jednotlivých vrstiev
        layer_resistances = []
        for layer in construction.layers:
            if layer.thickness > 0:
                resistance = layer.thickness / layer.thermal_conductivity
                layer_resistances.append(resistance)
            else:
                layer_resistances.append(0.001)  # Minimálny odpor
        
        total_resistance = sum(layer_resistances)
        if total_resistance == 0:
            return [t_int] * len(construction.layers)
        
        # Výpočet teploty na konci každej vrstvy
        cumulative_resistance = 0
        temp_diff = t_int - t_ext
        
        for resistance in layer_resistances:
            cumulative_resistance += resistance
            temp = t_ext + (cumulative_resistance / total_resistance) * temp_diff
            temperatures.append(temp)
        
        return temperatures[1:]  # Vrátime teploty bez počiatočnej vonkajšej
    
    def _calculate_vapor_pressures(self, construction: Construction, 
                                 rh_ext: float, rh_int: float, 
                                 temperatures: List[float]) -> List[float]:
        """
        Výpočet parciálnych tlakov vodnej pary
        
        Args:
            construction: Stavebná konštrukcia
            rh_ext: Vonkajšia relatívna vlhkosť [%]
            rh_int: Vnútorná relatívna vlhkosť [%]
            temperatures: Teploty v jednotlivých vrstvách [°C]
            
        Returns:
            Zoznam parciálnych tlakov vodnej pary [Pa]
        """
        # Výpočet difúznych odporov
        vapor_resistances = []
        for layer in construction.layers:
            # Predpokladáme difúzny odpor μ = 50 pre bežné materiály
            mu = getattr(layer, 'vapor_diffusion_resistance', 50)
            if layer.thickness > 0:
                vapor_resistance = mu * layer.thickness
                vapor_resistances.append(vapor_resistance)
            else:
                vapor_resistances.append(1)  # Minimálny odpor
        
        total_vapor_resistance = sum(vapor_resistances)
        if total_vapor_resistance == 0:
            return [self._rh_to_vapor_pressure(rh_int, temperatures[-1])] * len(temperatures)
        
        # Parciálne tlaky na začiatku a konci
        p_ext = self._rh_to_vapor_pressure(rh_ext, temperatures[0])
        p_int = self._rh_to_vapor_pressure(rh_int, temperatures[-1])
        
        vapor_pressures = [p_ext]
        cumulative_resistance = 0
        pressure_diff = p_int - p_ext
        
        for resistance in vapor_resistances[:-1]:
            cumulative_resistance += resistance
            pressure = p_ext + (cumulative_resistance / total_vapor_resistance) * pressure_diff
            vapor_pressures.append(pressure)
        
        return vapor_pressures
    
    def _calculate_saturation_pressure(self, temperature: float) -> float:
        """
        Výpočet nasýteného tlaku vodnej pary pri danej teplote
        
        Args:
            temperature: Teplota [°C]
            
        Returns:
            Nasýtený tlak vodnej pary [Pa]
        """
        import math
        
        # Magnus-Tetensova formula
        if temperature >= 0:
            # Pre vodu
            a = 17.27
            b = 237.7
        else:
            # Pre ľad
            a = 21.875
            b = 265.5
        
        exponent = (a * temperature) / (b + temperature)
        saturation_pressure = 610.78 * math.exp(exponent)
        
        return saturation_pressure
    
    def _rh_to_vapor_pressure(self, relative_humidity: float, temperature: float) -> float:
        """
        Konverzia relatívnej vlhkosti na parciálny tlak vodnej pary
        
        Args:
            relative_humidity: Relatívna vlhkosť [%]
            temperature: Teplota [°C]
            
        Returns:
            Parciálny tlak vodnej pary [Pa]
        """
        saturation_pressure = self._calculate_saturation_pressure(temperature)
        return (relative_humidity / 100.0) * saturation_pressure
    
    def compare_constructions(self, constructions: List[Construction], 
                            standard: str = 'wall_new_2012') -> Dict[str, Any]:
        """
        Porovnanie viacerých konštrukcií
        
        Args:
            constructions: Zoznam konštrukcií na porovnanie
            standard: Štandard pre hodnotenie
            
        Returns:
            Porovnacie hodnotenie
        """
        assessments = []
        for construction in constructions:
            assessment = self.assess_construction(construction, standard)
            assessments.append(assessment)
        
        # Najlepšia a najhoršia konštrukcia
        best_construction = min(assessments, key=lambda a: a.construction.u_value)
        worst_construction = max(assessments, key=lambda a: a.construction.u_value)
        
        # Štatistiky
        u_values = [a.construction.u_value for a in assessments]
        avg_u_value = sum(u_values) / len(u_values)
        
        return {
            'assessments': assessments,
            'summary': {
                'construction_count': len(constructions),
                'average_u_value': avg_u_value,
                'best_construction': {
                    'name': best_construction.construction.name,
                    'u_value': best_construction.construction.u_value,
                    'rating': best_construction.u_value_rating
                },
                'worst_construction': {
                    'name': worst_construction.construction.name,
                    'u_value': worst_construction.construction.u_value,
                    'rating': worst_construction.u_value_rating
                },
                'compliance_distribution': self._get_compliance_distribution(assessments)
            }
        }
    
    def _get_compliance_distribution(self, assessments: List[ConstructionAssessment]) -> Dict[str, int]:
        """Distribúcia úrovní súladu"""
        distribution = {level.value: 0 for level in ComplianceLevel}
        for assessment in assessments:
            distribution[assessment.compliance_level.value] += 1
        return distribution


def create_typical_wall_constructions() -> List[Construction]:
    """Vytvorenie typických stenových konštrukcií pre porovnanie"""
    material_db = MaterialDatabase()
    
    constructions = []
    
    # 1. Obvodová stena - tehla + EPS
    brick_eps_layers = [
        material_db.get_material('lime_plaster').to_material_layer(0.015),
        material_db.get_material('brick_hollow_300').to_material_layer(0.30),
        material_db.get_material('eps_040').to_material_layer(0.12),
        material_db.get_material('cement_plaster').to_material_layer(0.020)
    ]
    constructions.append(Construction(
        "Dutá tehla 300mm + EPS 120mm", ConstructionType.EXTERNAL_WALL,
        brick_eps_layers, 100.0
    ))
    
    # 2. Obvodová stena - pórobetón
    aac_layers = [
        material_db.get_material('lime_plaster').to_material_layer(0.015),
        material_db.get_material('aac_365').to_material_layer(0.365),
        material_db.get_material('eps_038').to_material_layer(0.10),
        material_db.get_material('cement_plaster').to_material_layer(0.020)
    ]
    constructions.append(Construction(
        "Pórobetón 365mm + EPS 100mm", ConstructionType.EXTERNAL_WALL,
        aac_layers, 100.0
    ))
    
    # 3. Obvodová stena - pasívny dom
    passive_layers = [
        material_db.get_material('gypsum_plaster').to_material_layer(0.015),
        material_db.get_material('aac_200').to_material_layer(0.20),
        material_db.get_material('mineral_wool_035').to_material_layer(0.25),
        material_db.get_material('cement_plaster').to_material_layer(0.020)
    ]
    constructions.append(Construction(
        "Pórobetón 200mm + MW 250mm (pasívny dom)", ConstructionType.EXTERNAL_WALL,
        passive_layers, 100.0
    ))
    
    return constructions


# Globálne inštancie
material_database = MaterialDatabase()
standards_database = ConstructionStandardsDatabase()
construction_assessor = ConstructionAssessor()


def get_material_database() -> MaterialDatabase:
    """Získanie globálnej inštancie databázy materiálov"""
    return material_database


def get_standards_database() -> ConstructionStandardsDatabase:
    """Získanie globálnej inštancie databázy štandardov"""
    return standards_database


def get_construction_assessor() -> ConstructionAssessor:
    """Získanie globálnej inštancie hodnotiteľa konštrukcií"""
    return construction_assessor