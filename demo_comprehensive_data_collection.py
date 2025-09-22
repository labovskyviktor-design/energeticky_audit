#!/usr/bin/env python3
"""
Rozšírené DEMO - Komplexný systém zberu dát pre energetické audity
Demonštrácia úplnej funkcionality integrujúcej poznatky z PDF 1,2,3 a STN EN 16247
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from datetime import datetime, date
import json
from typing import Dict, List, Any

from src.comprehensive_data_collection import (
    get_comprehensive_data_collector, 
    DataQualityLevel,
    ValidationStatus
)

from src.stn_en_16247 import (
    AuditType, 
    EnergyCarrier, 
    MeasurementMethod,
    create_sample_auditor_qualification
)

def comprehensive_data_collection_demo():
    """Kompletné demo zberu dát pre energetický audit"""
    
    print("="*70)
    print("🏢 KOMPLEXNÝ SYSTÉM ZBERU DÁT PRE ENERGETICKÉ AUDITY")
    print("📋 Integrácia poznatkov z PDF dokumentov a STN EN 16247")
    print("="*70)
    
    # Inicializácia zberača dát
    collector = get_comprehensive_data_collector(AuditType.BUILDING)
    
    # 1. SPUSTENIE ZBERU DÁT
    print("\n🚀 1. SPUSTENIE ZBERU DÁT")
    print("-" * 40)
    
    auditor = create_sample_auditor_qualification()
    audit_scope = {
        'scope_type': 'comprehensive',
        'boundaries': 'whole_building',
        'focus_areas': ['energy_efficiency', 'thermal_comfort', 'indoor_air_quality', 'sustainability'],
        'audit_objectives': [
            'Identifikácia úsporných opatrení',
            'Hodnotenie tepelno-technických vlastností',
            'Analýza prevádzkovej efektívnosti',
            'Návrh renovačných opatrení'
        ]
    }
    
    collection_start = collector.start_data_collection(
        'EA-2024-COMPREHENSIVE-001', 
        auditor, 
        audit_scope
    )
    
    print(f"✅ Audit ID: {collection_start['audit_id']}")
    print(f"📊 Požadované dátové elementy: {len(collection_start['required_data_elements'])}")
    print(f"🎯 Ciele kvality dát: {collection_start['data_quality_targets']}")
    
    # 2. ZBER ZÁKLADNÝCH ÚDAJOV O BUDOVE
    print("\n🏗️ 2. ZÁKLADNÉ INFORMÁCIE O BUDOVE")
    print("-" * 40)
    
    building_info = {
        'building_name': 'Kancelárska budova Green Office',
        'building_address': 'Námestie Slobody 12, 811 06 Bratislava, Slovensko',
        'building_type': 'Administratívna budova',
        'total_floor_area': 4500.0,        # m²
        'heated_floor_area': 4200.0,       # m²
        'conditioned_volume': 14700.0,     # m³
        'building_height': 21.0,           # m
        'number_of_floors': 6,
        'construction_year': 1998,
        
        # Prevádzkové údaje
        'occupancy_profile': {
            'max_occupants': 280,
            'typical_occupants': 230,
            'occupancy_schedule': 'weekdays 7:00-19:00',
            'seasonal_variation': 0.85  # leto vs zima
        },
        'operating_schedule': {
            'weekdays': '6:30-20:00',
            'saturdays': '8:00-14:00',
            'sundays': 'closed',
            'holidays': 'closed'
        },
        
        # Historické údaje
        'major_renovations': [
            {
                'year': 2010,
                'scope': 'Výmena okien',
                'description': 'Inštalácia trojskiel s nízkoemisnými nátermi',
                'cost': 180000  # EUR
            },
            {
                'year': 2018,
                'scope': 'Modernizácia vykurovacieho systému',
                'description': 'Inštalácia kondenzačného plynového kotla',
                'cost': 85000
            }
        ],
        
        # Klimatické údaje
        'climate_zone': 'Dfb',  # Kontinentálne podnebie
        'heating_degree_days': 3420,
        'cooling_degree_days': 180,
        
        # Kvalita dát
        'data_source': 'measured',
        'measurement_date': '2024-01-15',
        'uncertainty': 3.0  # %
    }
    
    general_result = collector.collect_general_building_info(building_info)
    print(f"✅ Základné údaje: {general_result['success']}")
    print(f"📈 Kvalita dát: {general_result['data_quality']}")
    print(f"📊 Kompletnosť: {general_result['completeness_score']:.1f}%")
    if general_result.get('validation_warnings'):
        print(f"⚠️  Upozornenia: {len(general_result['validation_warnings'])}")
    
    # 3. ZBER ÚDAJOV O OBÁLKE BUDOVY
    print("\n🏠 3. OBÁLKA BUDOVY - DETAILNÁ CHARAKTERIZÁCIA")
    print("-" * 40)
    
    envelope_data = {
        'total_envelope_area': 5850.0,  # m²
        'window_to_wall_ratio': 0.32,
        'thermal_bridge_coefficient': 0.08,
        
        # Steny
        'walls': [
            {
                'name': 'Obvodové steny - sever',
                'area': 980.0,
                'u_value': 0.35,  # W/m²K
                'construction_year': 1998,
                'condition_rating': 'good',
                'material_layers': [
                    {'material': 'Omietka vnútorná', 'thickness': 0.015, 'lambda': 0.8},
                    {'material': 'Porotherm 30', 'thickness': 0.300, 'lambda': 0.18},
                    {'material': 'Polystyrén EPS', 'thickness': 0.120, 'lambda': 0.04},
                    {'material': 'Omietka vonkajšia', 'thickness': 0.020, 'lambda': 0.8}
                ],
                'data_source': 'calculated'
            },
            {
                'name': 'Obvodové steny - juh',
                'area': 1020.0,
                'u_value': 0.28,  # lepšia izolácia na južnej strane
                'construction_year': 2010,  # renovované
                'condition_rating': 'excellent',
                'data_source': 'measured'
            }
        ],
        
        # Strecha
        'roof': [
            {
                'name': 'Plochá strecha',
                'area': 750.0,
                'u_value': 0.22,
                'construction_year': 1998,
                'condition_rating': 'fair',
                'material_layers': [
                    {'material': 'Hydroizolácia', 'thickness': 0.008},
                    {'material': 'Minerálna vlna', 'thickness': 0.200, 'lambda': 0.04},
                    {'material': 'Parozábrana', 'thickness': 0.002},
                    {'material': 'ŽB doska', 'thickness': 0.200, 'lambda': 1.6}
                ]
            }
        ],
        
        # Podlahy
        'floors': [
            {
                'name': 'Podlaha nad suterénom',
                'area': 750.0,
                'u_value': 0.31,
                'construction_year': 1998,
                'condition_rating': 'good'
            }
        ],
        
        # Okná
        'windows': [
            {
                'name': 'Okná - trojsklo',
                'area': 950.0,
                'u_value': 1.1,  # W/m²K
                'g_value': 0.6,   # solárny zisk
                'construction_year': 2010,
                'condition_rating': 'excellent',
                'frame_material': 'PVC',
                'glazing_type': 'Triple glazing, low-E coating'
            }
        ],
        
        # Vzduchotesnosť
        'airtightness': {
            'n50': 2.8,  # h⁻¹
            'q50': 1.9,  # m³/h/m²
            'test_date': '2023-11-15',
            'test_method': 'Blower door test EN 13829'
        }
    }
    
    envelope_result = collector.collect_building_envelope_data(envelope_data)
    print(f"✅ Obálka budovy: {envelope_result['success']}")
    print(f"📈 Kvalita dát: {envelope_result['data_quality']}")
    print(f"📊 Kompletnosť: {envelope_result['completeness_score']:.1f}%")
    
    # 4. TECHNICKÉ SYSTÉMY
    print("\n⚙️ 4. TECHNICKÉ SYSTÉMY - KOMPLETNÝ PREHĽAD")
    print("-" * 40)
    
    systems_data = [
        {
            'system_id': 'HEAT-001',
            'system_name': 'Plynový kondenzačný kotol',
            'system_category': 'heating',
            'system_type': 'Gas condensing boiler',
            'nominal_capacity': 320.0,  # kW
            'efficiency_nominal': 98.5,  # %
            'efficiency_actual': 94.2,   # %
            'installation_year': 2018,
            'manufacturer': 'Viessmann',
            'model': 'Vitocrossal 300',
            'design_life': 20,
            'operating_hours_annual': 2100,
            'capacity_factor': 0.65,
            'annual_consumption': {
                'natural_gas': 85000  # kWh/rok
            },
            'control_system': {
                'type': 'weather_compensated',
                'automation_level': 'automatic',
                'sensors': ['outdoor_temp', 'indoor_temp', 'flow_temp']
            },
            'maintenance_history': [
                {
                    'date': '2024-09-15',
                    'type': 'annual_service',
                    'findings': 'Všetky komponenty v poriadku',
                    'cost': 450
                }
            ],
            'operational_status': 'operational',
            'data_source': 'measured'
        },
        {
            'system_id': 'VENT-001',
            'system_name': 'Vzduchotechnická jednotka s rekuperáciou',
            'system_category': 'ventilation',
            'system_type': 'AHU with heat recovery',
            'nominal_capacity': 12000,  # m³/h
            'efficiency_nominal': 82.0,  # % rekuperácie
            'installation_year': 2015,
            'operating_hours_annual': 3500,
            'annual_consumption': {
                'electricity': 18500  # kWh/rok
            },
            'control_system': {
                'type': 'demand_controlled',
                'automation_level': 'smart',
                'sensors': ['co2', 'humidity', 'occupancy']
            }
        },
        {
            'system_id': 'LIGHT-001',
            'system_name': 'LED osvetľovací systém',
            'system_category': 'lighting',
            'system_type': 'LED with daylight control',
            'installation_year': 2020,
            'annual_consumption': {
                'electricity': 28000  # kWh/rok
            },
            'control_system': {
                'type': 'daylight_dimming',
                'automation_level': 'smart',
                'sensors': ['daylight', 'occupancy', 'motion']
            }
        },
        {
            'system_id': 'DHW-001',
            'system_name': 'Ohrev teplej vody',
            'system_category': 'dhw',
            'system_type': 'Gas water heater',
            'nominal_capacity': 45.0,  # kW
            'efficiency_nominal': 89.0,
            'annual_consumption': {
                'natural_gas': 15000  # kWh/rok
            }
        }
    ]
    
    systems_result = collector.collect_technical_systems_data(systems_data)
    print(f"✅ Technické systémy: {systems_result['success']}")
    print(f"🔧 Spracované systémy: {systems_result['systems_processed']}")
    print(f"📈 Celková kvalita: {systems_result['overall_data_quality']['overall_quality']}")
    
    # 5. SPOTREBA ENERGIE
    print("\n⚡ 5. PROFILY SPOTREBY ENERGIE")
    print("-" * 40)
    
    consumption_data = [
        {
            'energy_carrier': 'electricity',
            'annual_consumption': 185000.0,  # kWh/rok
            'annual_cost': 25900.0,         # EUR/rok
            'unit_price': 0.14,             # EUR/kWh
            'measurement_method': 'continuous',
            
            # Časové profily
            'monthly_profile': [
                16200, 15100, 14800, 13900, 12500,  # Jan-Máj
                13200, 14100, 13800, 14600, 15900,  # Jún-Okt  
                17800, 19200                         # Nov-Dec
            ],
            'daily_profile': [
                3.2, 2.8, 2.5, 2.3, 2.8, 4.5, 7.8, 9.2,  # 0-7h
                11.5, 12.8, 13.2, 13.5, 12.9, 13.1, 12.7, 12.3,  # 8-15h
                11.8, 10.9, 9.2, 7.5, 6.1, 5.2, 4.3, 3.8   # 16-23h
            ],
            'seasonal_variation': {
                'spring': 0.92,
                'summer': 0.85,
                'autumn': 0.98,
                'winter': 1.15
            },
            
            # Špičkové hodnoty
            'peak_demand': 45.8,  # kW
            'peak_demand_time': '2024-01-22T14:30:00',
            'load_factor': 0.52,
            
            # Faktúry
            'utility_bills': [
                {
                    'period': '2024-01',
                    'consumption': 16200,
                    'cost': 2268,
                    'peak_demand': 42.1
                },
                {
                    'period': '2024-02', 
                    'consumption': 15100,
                    'cost': 2114,
                    'peak_demand': 39.8
                }
            ],
            
            'measurement_uncertainty': 2.5,  # %
            'data_source': 'measured'
        },
        {
            'energy_carrier': 'natural_gas',
            'annual_consumption': 100000.0,  # kWh/rok
            'annual_cost': 6500.0,           # EUR/rok
            'unit_price': 0.065,
            'measurement_method': 'monthly_readings',
            
            'monthly_profile': [
                12500, 11200, 9800, 7400, 4200,     # Jan-Máj
                2800, 2200, 2100, 3500, 6800,       # Jún-Okt
                9200, 11800                          # Nov-Dec
            ],
            'seasonal_variation': {
                'heating_season': 1.45,
                'non_heating_season': 0.25
            },
            'weather_corrected': True,
            'degree_days_correlation': 0.89,
            'measurement_uncertainty': 5.0
        }
    ]
    
    consumption_result = collector.collect_energy_consumption_data(consumption_data)
    print(f"✅ Spotreba energie: {consumption_result['success']}")
    print(f"📊 Spracované profily: {consumption_result['profiles_processed']}")
    print(f"⚡ Celková spotreba: {consumption_result['total_annual_consumption']}")
    print(f"📈 Kvalita údajov: {consumption_result['data_quality_summary']}")
    
    # 6. DIAGNOSTICKÉ ZISTENIA
    print("\n🔍 6. DIAGNOSTICKÉ ZISTENIA")
    print("-" * 40)
    
    findings_data = [
        {
            'finding_id': 'THERMO-001',
            'diagnostic_method': 'thermography',
            'location': 'Obvodová stena - severozápadný roh',
            'severity': 'medium',
            'description': 'Tepelný mostík pri napojení steny na strop',
            'category': 'thermal',
            'measurement_date': '2024-01-20T10:30:00',
            'inspector': 'Ing. Peter Nový',
            
            'measured_values': {
                'surface_temperature': 14.2,  # °C
                'delta_temperature': 3.8      # K
            },
            'reference_values': {
                'acceptable_delta': 2.0       # K
            },
            
            'energy_impact': 2400,            # kWh/rok
            'cost_impact': 180,               # EUR/rok
            'comfort_impact': 'Pocit priezvanu v blízkosti',
            
            'recommended_actions': [
                'Dodatočná izolácia tepelného mostíka',
                'Aplikácia vnútornej izolácie v problémovej oblasti'
            ],
            'urgency_level': 'medium',
            'estimated_cost_to_fix': 850
        },
        {
            'finding_id': 'AIR-001', 
            'diagnostic_method': 'blower_door',
            'location': 'Celá budova',
            'severity': 'low',
            'description': 'Vzduchotesnosť v rámci normy, ale s možnosťou zlepšenia',
            'category': 'airtightness',
            'measurement_date': '2023-11-15T09:00:00',
            'inspector': 'Ing. Mária Krásna',
            
            'measured_values': {
                'n50': 2.8,    # h⁻¹
                'q50': 1.9     # m³/h/m²
            },
            'reference_values': {
                'target_n50': 2.0,
                'excellent_n50': 1.5
            },
            
            'energy_impact': 3200,
            'cost_impact': 250,
            'recommended_actions': [
                'Dotesnenie okien a dverí',
                'Kontrola a oprava netesností v rozvodoch'
            ],
            'urgency_level': 'low',
            'estimated_cost_to_fix': 1200
        },
        {
            'finding_id': 'HVAC-001',
            'diagnostic_method': 'performance_test',
            'location': 'Strojovňa vykurovania',
            'severity': 'low',
            'description': 'Kotol pracuje s dobrou účinnosťou, mierne zníženie oproti nominálu',
            'category': 'technical',
            'measurement_date': '2024-02-10T14:00:00',
            'inspector': 'Ing. Tomáš Technický',
            
            'measured_values': {
                'efficiency_measured': 94.2,  # %
                'emissions_nox': 42           # mg/kWh
            },
            'reference_values': {
                'efficiency_nominal': 98.5,
                'emissions_limit': 60
            },
            
            'energy_impact': 1800,
            'cost_impact': 140,
            'recommended_actions': [
                'Čistenie a optimalizácia nastavení horáka',
                'Kontrola výmenníka tepla'
            ],
            'urgency_level': 'low',
            'estimated_cost_to_fix': 350
        }
    ]
    
    findings_result = collector.collect_diagnostic_findings(findings_data)
    print(f"✅ Diagnostické zistenia: {findings_result['success']}")
    print(f"🔍 Spracované zistenia: {findings_result['findings_processed']}")
    print(f"⚠️  Závažnosť: {findings_result['severity_distribution']}")
    print(f"📋 Kategórie: {findings_result['categories_found']}")
    
    # 7. REPORT O KVALITE DÁT
    print("\n📊 7. HODNOTENIE KVALITY DÁT")
    print("-" * 40)
    
    quality_report = collector.generate_data_quality_report()
    
    print(f"🎯 Celkové hodnotenie:")
    print(f"   • Skóre kvality: {quality_report['overall_assessment']['overall_score']:.1f}/100")
    print(f"   • Úroveň kvality: {quality_report['overall_assessment']['quality_level']}")
    
    print(f"📈 Kompletnosť dát:")
    print(f"   • Celková kompletnosť: {quality_report['completeness_analysis']['overall_completeness']:.1f}%")
    
    print(f"🔧 Presnosť dát:")
    print(f"   • Presnosť meraní: {quality_report['accuracy_assessment']['measurement_accuracy']}")
    print(f"   • Úspešnosť validácie: {quality_report['accuracy_assessment']['validation_passed']}%")
    
    print(f"💡 Odporúčania na zlepšenie:")
    for i, rec in enumerate(quality_report['improvement_recommendations'][:3], 1):
        print(f"   {i}. {rec}")
    
    # 8. EXPORT DÁT
    print("\n💾 8. EXPORT NAZBIERANÝCH DÁT")
    print("-" * 40)
    
    # Export do JSON
    export_data = collector.export_collected_data('json')
    
    # Uloženie do súboru
    with open('comprehensive_audit_data.json', 'w', encoding='utf-8') as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"✅ Dáta exportované do: comprehensive_audit_data.json")
    print(f"📁 Veľkosť súboru: {len(json.dumps(export_data, default=str)) / 1024:.1f} KB")
    
    # 9. SÚHRN ZBERU DÁT
    print("\n📋 9. SÚHRN ZBERU DÁT")
    print("-" * 40)
    
    data_summary = {
        'general_info': bool(export_data['general_info']),
        'envelope_data': bool(export_data['building_envelope']),
        'technical_systems': len(export_data['technical_systems']),
        'energy_profiles': len(export_data['energy_consumption']),
        'diagnostic_findings': len(export_data['diagnostic_findings']),
        'total_data_points': sum([
            1 if export_data['general_info'] else 0,
            1 if export_data['building_envelope'] else 0,
            len(export_data['technical_systems']),
            len(export_data['energy_consumption']),
            len(export_data['diagnostic_findings'])
        ])
    }
    
    print(f"🏢 Základné informácie: {'✅' if data_summary['general_info'] else '❌'}")
    print(f"🏠 Obálka budovy: {'✅' if data_summary['envelope_data'] else '❌'}")
    print(f"⚙️  Technické systémy: {data_summary['technical_systems']}")
    print(f"⚡ Energetické profily: {data_summary['energy_profiles']}")
    print(f"🔍 Diagnostické zistenia: {data_summary['diagnostic_findings']}")
    print(f"📊 Celkom dátových bodov: {data_summary['total_data_points']}")
    
    # 10. ZÁVER
    print("\n" + "="*70)
    print("🎉 KOMPLEXNÝ ZBER DÁT ÚSPEŠNE DOKONČENÝ!")
    print("="*70)
    
    final_stats = export_data['data_quality_summary']
    print(f"🏆 Finálne hodnotenie:")
    print(f"   • Celková kvalita dát: {final_stats['overall_assessment']['quality_level']}")
    print(f"   • Kompletnosť: {final_stats['completeness_analysis']['overall_completeness']:.1f}%")
    print(f"   • Úspešnosť validácie: {final_stats['validation_summary']['success_rate']:.1f}%")
    print(f"   • Typ auditu: {export_data['audit_metadata']['audit_scope']['scope_type']}")
    
    return {
        'success': True,
        'audit_id': collection_start['audit_id'],
        'data_summary': data_summary,
        'quality_summary': final_stats,
        'export_file': 'comprehensive_audit_data.json'
    }

if __name__ == "__main__":
    try:
        result = comprehensive_data_collection_demo()
        print(f"\n✨ Demo dokončené s výsledkom: {result['success']}")
    except Exception as e:
        print(f"\n❌ Chyba počas demo: {e}")
        import traceback
        traceback.print_exc()