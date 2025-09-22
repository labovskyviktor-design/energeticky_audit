#!/usr/bin/env python3
"""
INTERAKTÍVNY ENERGETICKÝ AUDIT SYSTÉM
Profesionálny energetický audit s možnosťou zadávania reálnych projektových dát
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from datetime import datetime
import json
from typing import Dict, List, Any, Optional

# Import našich modulov
try:
    from src.energy_calculations import get_energy_calculator
    from src.thermal_analysis import Construction, MaterialLayer, ConstructionType
    from src.certificate_generator import get_certificate_generator
except ImportError as e:
    print(f"Import warning: {e}")
    # Fallback - vytvoríme vlastné implementácie
    def get_energy_calculator():
        return None
    def get_certificate_generator():
        return None

class InteractiveEnergyAudit:
    """Interaktívny systém pre energetický audit"""
    
    def __init__(self):
        self.audit_data = {}
        self.results = {}
        # Zjednodušené inicializácie
        try:
            self.certificate_generator = get_certificate_generator()
        except:
            self.certificate_generator = None
        
    def welcome_screen(self):
        """Uvítacia obrazovka"""
        print("="*80)
        print("🏢 PROFESIONÁLNY ENERGETICKÝ AUDIT SYSTÉM")
        print("📋 Podľa STN EN 16247 a slovenských noriem")
        print("="*80)
        print()
        print("Tento systém vám umožní:")
        print("✅ Zadať reálne projektové dáta")
        print("✅ Vypočítať energetické vlastnosti podľa noriem") 
        print("✅ Vytvoriť profesionálny audit report")
        print("✅ Vygenerovať energetický certifikát")
        print()
        
    def collect_basic_building_data(self) -> Dict[str, Any]:
        """Zber základných údajov o budove"""
        print("📋 1. ZÁKLADNÉ ÚDAJE O BUDOVE")
        print("-" * 40)
        
        building_data = {}
        
        # Základné informácie
        building_data['name'] = input("Názov budovy: ").strip()
        building_data['address'] = input("Adresa: ").strip()
        
        # Typ budovy
        print("\nTypy budov:")
        print("1. Rodinný dom")
        print("2. Bytový dom") 
        print("3. Administratívna budova")
        print("4. Priemyselná budova")
        print("5. Škola")
        print("6. Nemocnica")
        print("7. Hotel")
        print("8. Obchodné centrum")
        
        building_type_choice = input("Vyberte typ budovy (1-8): ").strip()
        building_types = {
            '1': 'Rodinný dom',
            '2': 'Bytový dom',
            '3': 'Administratívna budova', 
            '4': 'Priemyselná budova',
            '5': 'Škola',
            '6': 'Nemocnica',
            '7': 'Hotel',
            '8': 'Obchodné centrum'
        }
        building_data['type'] = building_types.get(building_type_choice, 'Rodinný dom')
        
        # Geometrické parametre
        print("\n📐 GEOMETRICKÉ PARAMETRE:")
        try:
            building_data['floor_area'] = float(input("Podlahová plocha [m²]: ").strip())
            building_data['heated_area'] = float(input("Vykurovaná plocha [m²]: ").strip())
            building_data['volume'] = float(input("Objem budovy [m³]: ").strip())
            building_data['height'] = float(input("Výška budovy [m]: ").strip())
            building_data['floors'] = int(input("Počet podlaží: ").strip())
        except ValueError:
            print("❌ Neplatné číslo, používam predvolené hodnoty")
            building_data['floor_area'] = 120.0
            building_data['heated_area'] = 115.0
            building_data['volume'] = 350.0
            building_data['height'] = 8.5
            building_data['floors'] = 2
        
        # Rok výstavby
        try:
            building_data['construction_year'] = int(input("Rok výstavby: ").strip())
        except ValueError:
            building_data['construction_year'] = 2000
            
        return building_data
    
    def collect_envelope_data(self) -> Dict[str, Any]:
        """Zber údajov o obálke budovy"""
        print("\n🏠 2. OBÁLKA BUDOVY")
        print("-" * 40)
        
        envelope_data = {'constructions': []}
        
        # Steny
        print("\n🧱 OBVODOVÉ STENY:")
        wall_area = float(input("Celková plocha obvodových stien [m²]: ").strip() or "150")
        
        print("Vyberte typ obvodovej steny:")
        print("1. Muriva s kontaktnou izoláciou")
        print("2. Sendvičová murovaná")
        print("3. Železobetónová s izoláciou")
        print("4. Drevená konštrukcia")
        print("5. Vlastná konštrukcia")
        
        wall_choice = input("Výber (1-5): ").strip()
        
        if wall_choice == "5":
            print("Zadajte vrstvy konštrukcie (zvnútra smerom von):")
            layers = []
            layer_count = int(input("Počet vrstiev: ").strip() or "4")
            
            for i in range(layer_count):
                print(f"\nVrstva {i+1}:")
                material = input("  Materiál: ").strip()
                thickness = float(input("  Hrúbka [m]: ").strip())
                lambda_val = float(input("  Lambda [W/mK]: ").strip())
                density = float(input("  Hustota [kg/m³]: ").strip() or "1800")
                heat_capacity = float(input("  Merná tepelná kapacita [J/kgK]: ").strip() or "1000")
                
                layers.append(MaterialLayer(material, thickness, lambda_val, density, heat_capacity))
            
            wall_construction = Construction("Obvodová stena", ConstructionType.EXTERNAL_WALL, layers, wall_area)
            u_value = wall_construction.u_value
            
        else:
            # Predvolené konštrukcie
            typical_u_values = {
                '1': 0.25,  # Kontaktná izolácia
                '2': 0.30,  # Sendvič
                '3': 0.22,  # ŽB s izoláciou
                '4': 0.20   # Drevená
            }
            u_value = typical_u_values.get(wall_choice, 0.25)
            print(f"Použitá U-hodnota: {u_value} W/m²K")
        
        envelope_data['constructions'].append({
            'name': 'Obvodová stena',
            'type': 'wall',
            'area': wall_area,
            'u_value': u_value
        })
        
        # Strecha
        print("\n🏠 STRECHA:")
        roof_area = float(input("Plocha strechy [m²]: ").strip() or "80")
        roof_u = float(input("U-hodnota strechy [W/m²K] (Enter=0.20): ").strip() or "0.20")
        
        envelope_data['constructions'].append({
            'name': 'Strecha',
            'type': 'roof', 
            'area': roof_area,
            'u_value': roof_u
        })
        
        # Podlaha
        print("\n🔲 PODLAHA:")
        floor_area = float(input("Plocha podlahy [m²]: ").strip() or "80")
        floor_u = float(input("U-hodnota podlahy [W/m²K] (Enter=0.30): ").strip() or "0.30")
        
        envelope_data['constructions'].append({
            'name': 'Podlaha',
            'type': 'floor',
            'area': floor_area, 
            'u_value': floor_u
        })
        
        # Okná
        print("\n🪟 OKNÁ:")
        window_area = float(input("Celková plocha okien [m²]: ").strip() or "25")
        
        print("Typ okien:")
        print("1. Jednosklo (U=5.0)")
        print("2. Dvojsklo (U=2.8)")
        print("3. Trojsklo (U=1.1)")
        print("4. Pasívne okná (U=0.8)")
        print("5. Vlastná hodnota")
        
        window_choice = input("Výber (1-5): ").strip()
        window_u_values = {'1': 5.0, '2': 2.8, '3': 1.1, '4': 0.8}
        
        if window_choice == '5':
            window_u = float(input("U-hodnota okien [W/m²K]: ").strip())
        else:
            window_u = window_u_values.get(window_choice, 2.8)
            
        print(f"Použitá U-hodnota okien: {window_u} W/m²K")
        
        envelope_data['constructions'].append({
            'name': 'Okná',
            'type': 'window',
            'area': window_area,
            'u_value': window_u
        })
        
        return envelope_data
    
    def collect_systems_data(self) -> Dict[str, Any]:
        """Zber údajov o technických systémoch"""
        print("\n⚙️ 3. TECHNICKÉ SYSTÉMY")
        print("-" * 40)
        
        systems_data = {}
        
        # Vykurovanie
        print("\n🔥 VYKUROVACÍ SYSTÉM:")
        print("1. Plynový kotol")
        print("2. Elektrické vykurovanie")
        print("3. Tepelné čerpadlo")
        print("4. Biomasa")
        print("5. Diaľkové vykurovanie")
        
        heating_choice = input("Typ vykurovania (1-5): ").strip()
        heating_types = {
            '1': {'name': 'Plynový kotol', 'efficiency': 0.90, 'fuel': 'natural_gas'},
            '2': {'name': 'Elektrické vykurovanie', 'efficiency': 1.0, 'fuel': 'electricity'},
            '3': {'name': 'Tepelné čerpadlo', 'efficiency': 3.5, 'fuel': 'electricity'}, 
            '4': {'name': 'Biomasa', 'efficiency': 0.80, 'fuel': 'biomass'},
            '5': {'name': 'Diaľkové vykurovanie', 'efficiency': 0.95, 'fuel': 'district_heating'}
        }
        
        heating_system = heating_types.get(heating_choice, heating_types['1'])
        
        # Možnosť zadania vlastnej účinnosti
        custom_efficiency = input(f"Účinnosť systému [%] (Enter={heating_system['efficiency']*100:.1f}%): ").strip()
        if custom_efficiency:
            try:
                heating_system['efficiency'] = float(custom_efficiency) / 100
            except ValueError:
                pass
                
        systems_data['heating'] = heating_system
        
        # Teplá voda
        print("\n🚿 PRÍPRAVA TEPLEJ VODY:")
        dhw_same = input("Rovnaký systém ako vykurovanie? (a/n): ").strip().lower()
        
        if dhw_same == 'n':
            dhw_choice = input("Typ ohrevu TUV (1-5): ").strip()
            dhw_system = heating_types.get(dhw_choice, heating_types['2'])
        else:
            dhw_system = heating_system.copy()
            
        systems_data['dhw'] = dhw_system
        
        # Vetranie
        print("\n🌬️ VETRANIE:")
        print("1. Prirodzené vetranie")
        print("2. Mechanické vetranie")
        print("3. Rekuperácia (účinnosť 70%)")
        print("4. Rekuperácia (účinnosť 85%)")
        
        vent_choice = input("Typ vetrania (1-4): ").strip()
        vent_systems = {
            '1': {'name': 'Prirodzené', 'recovery_efficiency': 0.0},
            '2': {'name': 'Mechanické', 'recovery_efficiency': 0.0},
            '3': {'name': 'Rekuperácia 70%', 'recovery_efficiency': 0.70},
            '4': {'name': 'Rekuperácia 85%', 'recovery_efficiency': 0.85}
        }
        
        systems_data['ventilation'] = vent_systems.get(vent_choice, vent_systems['1'])
        
        return systems_data
    
    def collect_usage_data(self) -> Dict[str, Any]:
        """Zber údajov o užívaní budovy"""
        print("\n👥 4. ÚDAJE O UŽÍVANÍ")
        print("-" * 40)
        
        usage_data = {}
        
        # Počet obyvateľov/užívateľov
        try:
            usage_data['occupants'] = int(input("Počet stálych obyvateľov/užívateľov: ").strip())
        except ValueError:
            usage_data['occupants'] = 4
            
        # Teplota vykurovania
        try:
            usage_data['heating_temp'] = float(input("Požadovaná teplota vykurovania [°C] (Enter=20): ").strip() or "20")
        except ValueError:
            usage_data['heating_temp'] = 20.0
            
        # Teplota TUV
        try:
            usage_data['dhw_temp'] = float(input("Teplota teplej vody [°C] (Enter=55): ").strip() or "55")
        except ValueError:
            usage_data['dhw_temp'] = 55.0
            
        # Klimatická lokalita
        print("\nKlimatická lokalita:")
        print("1. Bratislava a okolie")
        print("2. Západné Slovensko")
        print("3. Stredné Slovensko") 
        print("4. Východné Slovensko")
        print("5. Horské oblasti")
        
        climate_choice = input("Klimatická lokalita (1-5): ").strip()
        climate_zones = {
            '1': {'name': 'Bratislava', 'hdd': 2800, 'avg_temp': 10.5},
            '2': {'name': 'Západné SK', 'hdd': 3000, 'avg_temp': 9.8},
            '3': {'name': 'Stredné SK', 'hdd': 3200, 'avg_temp': 8.5},
            '4': {'name': 'Východné SK', 'hdd': 3100, 'avg_temp': 9.0},
            '5': {'name': 'Horské oblasti', 'hdd': 3800, 'avg_temp': 6.5}
        }
        
        usage_data['climate'] = climate_zones.get(climate_choice, climate_zones['1'])
        
        return usage_data
        
    def calculate_energy_performance(self) -> Dict[str, Any]:
        """Výpočet energetických vlastností"""
        print("\n🔬 VÝPOČET ENERGETICKÝCH VLASTNOSTÍ")
        print("-" * 50)
        print("Prebieha výpočet podľa STN EN ISO 52016...")
        
        # Základné výpočty
        building_data = self.audit_data['building']
        envelope_data = self.audit_data['envelope'] 
        systems_data = self.audit_data['systems']
        usage_data = self.audit_data['usage']
        
        results = {}
        
        # Výpočet tepelných strát obálkou
        total_heat_loss = 0
        envelope_details = []
        
        for construction in envelope_data['constructions']:
            heat_loss = construction['area'] * construction['u_value']
            total_heat_loss += heat_loss
            
            envelope_details.append({
                'name': construction['name'],
                'area': construction['area'],
                'u_value': construction['u_value'],
                'heat_loss': heat_loss
            })
        
        results['envelope_analysis'] = {
            'total_heat_loss_coefficient': total_heat_loss,
            'details': envelope_details
        }
        
        # Výpočet potreby tepla na vykurovanie
        hdd = usage_data['climate']['hdd']
        heating_need = total_heat_loss * hdd * 24 / 1000  # kWh/rok
        
        # Korekcia na vetranie
        air_change_rate = 0.5  # h-1 (prirodzené)
        if systems_data['ventilation']['name'] == 'Mechanické':
            air_change_rate = 0.8
        elif 'Rekuperácia' in systems_data['ventilation']['name']:
            air_change_rate = 0.8 * (1 - systems_data['ventilation']['recovery_efficiency'])
        
        ventilation_loss = building_data['volume'] * air_change_rate * 0.34 * hdd * 24 / 1000
        
        total_heating_need = heating_need + ventilation_loss
        
        # Solárne a vnútorné zisky
        window_area = next((c['area'] for c in envelope_data['constructions'] if c['type'] == 'window'), 20)
        solar_gains = window_area * 150  # kWh/rok (zjednodušene)
        internal_gains = building_data['floor_area'] * 3.5 * 365 / 1000  # kWh/rok
        
        net_heating_need = max(0, total_heating_need - solar_gains - internal_gains)
        
        results['heating_analysis'] = {
            'transmission_losses': heating_need,
            'ventilation_losses': ventilation_loss, 
            'total_losses': total_heating_need,
            'solar_gains': solar_gains,
            'internal_gains': internal_gains,
            'net_heating_need': net_heating_need,
            'specific_heating_need': net_heating_need / building_data['heated_area']
        }
        
        # Výpočet spotreby energie na vykurovanie
        heating_energy = net_heating_need / systems_data['heating']['efficiency']
        
        # Výpočet potreby tepla na TUV  
        dhw_need = usage_data['occupants'] * 25 * 365 / 1000  # kWh/rok (25 l/os/deň)
        dhw_energy = dhw_need / systems_data['dhw']['efficiency']
        
        # Elektrická energia (osvetlenie, spotrebiče)
        electricity_need = building_data['floor_area'] * 15  # kWh/m²rok
        
        results['energy_consumption'] = {
            'heating_energy': heating_energy,
            'dhw_energy': dhw_energy,
            'electricity': electricity_need,
            'total_energy': heating_energy + dhw_energy + electricity_need,
            'specific_total': (heating_energy + dhw_energy + electricity_need) / building_data['heated_area']
        }
        
        # Primárna energia
        primary_factors = {
            'natural_gas': 1.1,
            'electricity': 3.0,
            'biomass': 0.2,
            'district_heating': 1.3
        }
        
        heating_primary = heating_energy * primary_factors.get(systems_data['heating']['fuel'], 1.1)
        dhw_primary = dhw_energy * primary_factors.get(systems_data['dhw']['fuel'], 1.1)
        electricity_primary = electricity_need * primary_factors['electricity']
        
        total_primary = heating_primary + dhw_primary + electricity_primary
        specific_primary = total_primary / building_data['heated_area']
        
        results['primary_energy'] = {
            'heating': heating_primary,
            'dhw': dhw_primary, 
            'electricity': electricity_primary,
            'total': total_primary,
            'specific': specific_primary
        }
        
        # Energetická trieda
        if specific_primary <= 50:
            energy_class = 'A'
        elif specific_primary <= 75:
            energy_class = 'B'
        elif specific_primary <= 110:
            energy_class = 'C'
        elif specific_primary <= 150:
            energy_class = 'D'
        elif specific_primary <= 200:
            energy_class = 'E'
        elif specific_primary <= 250:
            energy_class = 'F'
        else:
            energy_class = 'G'
            
        results['energy_class'] = {
            'class': energy_class,
            'specific_primary_energy': specific_primary
        }
        
        # CO2 emisie
        emission_factors = {
            'natural_gas': 0.202,  # kg CO2/kWh
            'electricity': 0.486,
            'biomass': 0.018,
            'district_heating': 0.280
        }
        
        heating_co2 = heating_energy * emission_factors.get(systems_data['heating']['fuel'], 0.202)
        dhw_co2 = dhw_energy * emission_factors.get(systems_data['dhw']['fuel'], 0.202)
        electricity_co2 = electricity_need * emission_factors['electricity']
        
        total_co2 = heating_co2 + dhw_co2 + electricity_co2
        
        results['co2_emissions'] = {
            'heating': heating_co2,
            'dhw': dhw_co2,
            'electricity': electricity_co2,
            'total': total_co2,
            'specific': total_co2 / building_data['heated_area']
        }
        
        print("✅ Výpočty dokončené!")
        return results
        
    def generate_professional_report(self):
        """Generovanie profesionálneho reportu"""
        print("\n📄 GENEROVANIE PROFESIONÁLNEHO REPORTU")
        print("-" * 50)
        
        # Základné údaje
        building = self.audit_data['building']
        results = self.results
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        report = {
            'audit_info': {
                'title': 'ENERGETICKÝ AUDIT BUDOVY',
                'subtitle': f"Energetické hodnotenie budovy {building['name']}",
                'date': timestamp,
                'auditor': 'Ing. Energetický Audítor',
                'standard': 'STN EN 16247-1, STN EN ISO 52016'
            },
            'building_info': building,
            'results': results,
            'recommendations': self._generate_recommendations(),
            'certification': {
                'energy_class': results['energy_class']['class'],
                'specific_primary_energy': f"{results['energy_class']['specific_primary_energy']:.1f} kWh/m²rok",
                'co2_emissions': f"{results['co2_emissions']['specific']:.1f} kg CO2/m²rok"
            }
        }
        
        # Uloženie reportu
        report_filename = f"energeticky_audit_{building['name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        
        with open(report_filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2, default=str)
            
        print(f"✅ Report uložený: {report_filename}")
        return report, report_filename
        
    def _generate_recommendations(self) -> List[Dict[str, Any]]:
        """Generovanie odporúčaní na základe výpočtov"""
        recommendations = []
        results = self.results
        
        # Hodnotenie obálky
        envelope = results['envelope_analysis']['details']
        
        for element in envelope:
            if element['name'] == 'Obvodová stena' and element['u_value'] > 0.30:
                recommendations.append({
                    'category': 'Tepelná izolácia',
                    'title': 'Zateplenie obvodových stien',
                    'description': f'Aktuálna U-hodnota {element["u_value"]:.2f} W/m²K je vysoká. Odporúčame zateplenie.',
                    'priority': 'Vysoká',
                    'estimated_savings': '25-35%'
                })
                
            if element['name'] == 'Okná' and element['u_value'] > 2.0:
                recommendations.append({
                    'category': 'Výplne otvorov',
                    'title': 'Výmena okien',
                    'description': f'Aktuálna U-hodnota okien {element["u_value"]:.1f} W/m²K. Výmena za kvalitné trojsklo.',
                    'priority': 'Stredná',
                    'estimated_savings': '15-20%'
                })
        
        # Hodnotenie systémov
        if self.audit_data['systems']['heating']['efficiency'] < 0.85:
            recommendations.append({
                'category': 'Vykurovací systém',
                'title': 'Modernizácia vykurovacieho systému',
                'description': 'Nízka účinnosť vykurovacieho systému. Odporúčame výmenu za efektívnejší.',
                'priority': 'Vysoká',
                'estimated_savings': '20-30%'
            })
            
        if 'Rekuperácia' not in self.audit_data['systems']['ventilation']['name']:
            recommendations.append({
                'category': 'Vetranie',
                'title': 'Inštalácia rekuperačnej jednotky',
                'description': 'Rekuperácia tepla z odvádzaného vzduchu môže priniesť významné úspory.',
                'priority': 'Stredná',
                'estimated_savings': '10-15%'
            })
            
        return recommendations
        
    def print_summary_report(self):
        """Výpis súhrnného reportu na obrazovku"""
        print("\n" + "="*80)
        print("📋 SÚHRNNÝ ENERGETICKÝ AUDIT")
        print("="*80)
        
        building = self.audit_data['building']
        results = self.results
        
        print(f"🏢 Budova: {building['name']}")
        print(f"📍 Adresa: {building['address']}")
        print(f"🏗️  Typ: {building['type']}")
        print(f"📐 Podlahová plocha: {building['floor_area']:.0f} m²")
        print(f"📅 Rok výstavby: {building['construction_year']}")
        
        print(f"\n⚡ ENERGETICKÁ BILANCIA:")
        print(f"├─ Potreba tepla na vykurovanie: {results['heating_analysis']['net_heating_need']:.0f} kWh/rok")
        print(f"├─ Spotreba na vykurovanie: {results['energy_consumption']['heating_energy']:.0f} kWh/rok")
        print(f"├─ Spotreba na TUV: {results['energy_consumption']['dhw_energy']:.0f} kWh/rok")
        print(f"├─ Elektrická energia: {results['energy_consumption']['electricity']:.0f} kWh/rok")
        print(f"└─ Celková spotreba: {results['energy_consumption']['total_energy']:.0f} kWh/rok")
        
        print(f"\n🎯 ENERGETICKÉ HODNOTENIE:")
        print(f"├─ Energetická trieda: {results['energy_class']['class']}")
        print(f"├─ Primárna energia: {results['primary_energy']['specific']:.1f} kWh/m²rok") 
        print(f"├─ CO2 emisie: {results['co2_emissions']['specific']:.1f} kg CO2/m²rok")
        print(f"└─ Špecifická spotreba: {results['energy_consumption']['specific_total']:.1f} kWh/m²rok")
        
        print(f"\n🏠 OBÁLKA BUDOVY:")
        for detail in results['envelope_analysis']['details']:
            print(f"├─ {detail['name']}: {detail['area']:.0f} m², U={detail['u_value']:.2f} W/m²K")
        print(f"└─ Celkový súčiniteľ prestupu: {results['envelope_analysis']['total_heat_loss_coefficient']:.1f} W/K")
        
        print(f"\n💡 HLAVNÉ ODPORÚČANIA:")
        recommendations = self._generate_recommendations()
        for i, rec in enumerate(recommendations[:3], 1):
            print(f"{i}. {rec['title']} - {rec['estimated_savings']} úspory")
            
    def run_interactive_audit(self):
        """Hlavný proces interaktívneho auditu"""
        self.welcome_screen()
        
        try:
            # Zber dát
            self.audit_data['building'] = self.collect_basic_building_data()
            self.audit_data['envelope'] = self.collect_envelope_data() 
            self.audit_data['systems'] = self.collect_systems_data()
            self.audit_data['usage'] = self.collect_usage_data()
            
            # Výpočty
            self.results = self.calculate_energy_performance()
            
            # Zobrazenie výsledkov
            self.print_summary_report()
            
            # Generovanie reportu
            report, filename = self.generate_professional_report()
            
            # Možnosť generovania certifikátu
            generate_cert = input("\n🏅 Chcete vygenerovať energetický certifikát? (a/n): ").strip().lower()
            if generate_cert == 'a':
                self.generate_energy_certificate()
                
            print(f"\n✅ Energetický audit dokončený!")
            print(f"📁 Report uložený: {filename}")
            
            return True
            
        except KeyboardInterrupt:
            print("\n\n❌ Audit prerušený používateľom.")
            return False
        except Exception as e:
            print(f"\n❌ Chyba počas auditu: {e}")
            return False
    
    def generate_energy_certificate(self):
        """Generovanie energetického certifikátu"""
        print("\n🏅 GENEROVANIE ENERGETICKÉHO CERTIFIKÁTU")
        print("-" * 50)
        
        building = self.audit_data['building']
        results = self.results
        
        certificate_data = {
            'building_name': building['name'],
            'address': building['address'],
            'building_type': building['type'],
            'floor_area': building['heated_area'],
            'energy_class': results['energy_class']['class'],
            'primary_energy': results['primary_energy']['specific'],
            'co2_emissions': results['co2_emissions']['specific'],
            'issue_date': datetime.now().strftime('%Y-%m-%d'),
            'valid_until': (datetime.now().replace(year=datetime.now().year + 10)).strftime('%Y-%m-%d'),
            'auditor': 'Ing. Energetický Audítor',
            'certificate_number': f"EC-{datetime.now().strftime('%Y%m%d%H%M')}"
        }
        
        try:
            # Jednoducho vytvoríme JSON s certifikátom
            certificate = {
                'certificate_type': 'Energetický certifikát budovy',
                'validity': 'Validácia podlťa STN EN 16247',
                'energy_performance': {
                    'class': certificate_data['energy_class'],
                    'primary_energy': certificate_data['primary_energy'],
                    'co2_emissions': certificate_data['co2_emissions']
                }
            }
            
            cert_filename = f"certifikat_{building['name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.json"
            
            with open(cert_filename, 'w', encoding='utf-8') as f:
                json.dump({
                    'certificate_data': certificate_data,
                    'certificate': certificate
                }, f, ensure_ascii=False, indent=2, default=str)
                
            print(f"✅ Energetický certifikát vygenerovaný: {cert_filename}")
            print(f"📋 Číslo certifikátu: {certificate_data['certificate_number']}")
            print(f"🏅 Energetická trieda: {certificate_data['energy_class']}")
            print(f"⚡ Primárna energia: {certificate_data['primary_energy']:.1f} kWh/m²rok")
            
        except Exception as e:
            print(f"❌ Chyba pri generovaní certifikátu: {e}")

def main():
    """Hlavná funkcia"""
    audit_system = InteractiveEnergyAudit()
    audit_system.run_interactive_audit()

if __name__ == "__main__":
    main()