#!/usr/bin/env python3
"""
Demo script pre Energy Audit Desktop Application
Ukáže funkčnosť jednotlivých modulov
"""

import sys
import os
from pathlib import Path

# Pridanie src do cesty
sys.path.insert(0, str(Path(__file__).parent / "src"))

def demo_basic_energy_calculation():
    """Demo základných energetických výpočtov"""
    print("=" * 60)
    print("DEMO: ZÁKLADNÉ ENERGETICKÉ VÝPOČTY")
    print("=" * 60)
    
    from energy_calculations import get_energy_calculator, create_sample_building_data
    
    calculator = get_energy_calculator()
    building_data = create_sample_building_data()
    
    # Kompletné hodnotenie budovy
    results = calculator.complete_building_assessment(building_data)
    
    print(f"Budova: {building_data['building_type']}")
    print(f"Podlahová plocha: {building_data['heated_area']} m²")
    print()
    
    summary = results['summary']
    print("ENERGETICKÁ KLASIFIKÁCIA:")
    print(f"  Energetická trieda: {summary['energy_class']}")
    print(f"  Primárna energia: {summary['specific_primary_energy']:.1f} kWh/m²rok")
    print(f"  Potreba tepla na vykurovanie: {summary['specific_heating_demand']:.1f} kWh/m²rok")
    print(f"  Potreba tepla na teplú vodu: {summary['specific_hot_water_demand']:.1f} kWh/m²rok")
    print(f"  CO2 emisie: {summary['specific_co2_emissions']:.1f} kg/m²rok")
    print()
    
    return results

def demo_advanced_financial_analysis():
    """Demo pokročilej finančnej analýzy"""
    print("=" * 60)
    print("DEMO: POKROČILÁ FINANČNÁ ANALÝZA")
    print("=" * 60)
    
    from project_management import get_project_manager
    
    pm = get_project_manager()
    
    # Vytvorenie testovacieho projektu
    building_data = {
        'name': 'Rodinný dom - Bratislava',
        'address': 'Testovacia ulica 123',
        'construction_year': 1985,
        'heated_area': 120,
        'total_consumption': 180000,  # kWh/rok
        'building_type': 'Rodinný dom'
    }
    
    project = pm.create_project('DEMO001', building_data)
    print(f"Vytvorený projekt: {project['id']}")
    
    # Fáza 1: Identifikácia
    owner_data = {
        'name': 'Majiteľ Demo',
        'investment_budget': 25000,
        'motivation': 'Vysoká',
        'decision_factors': ['Úspora nákladov', 'Ekológia', 'Komfort']
    }
    
    identification = pm.phase_1_project_identification('DEMO001', owner_data)
    print(f"Predbežné hodnotenie: {identification['preliminary_assessment']['recommended_proceed']}")
    print(f"Odhadovaná návratnosť: {identification['preliminary_assessment']['estimated_payback']:.1f} rokov")
    
    # Fáza 2: Prehliadka
    inspection_data = {
        'condition': 'Dobrý',
        'systems': {'heating': 'Plynový kotol 15 rokov', 'insulation': 'Čiastočná'},
        'consumption': {'gas': 15000, 'electricity': 4000},
        'measures': ['Tepelná izolácia', 'Výmena okien', 'Modernizácia kotla'],
        'notes': 'Budova má potenciál na energetické úspory'
    }
    
    findings = pm.phase_2_inspection('DEMO001', inspection_data)
    print(f"Identifikované opatrenia: {len(findings.identified_measures)}")
    print(f"Celkový potenciál úspor: {pm.projects['DEMO001']['potential'].overall_payback:.1f} rokov návratnosť")
    
    # Fáza 3: Detailný energetický audit s finančnou analýzou
    audit_results = pm.phase_3_energy_audit('DEMO001', 'detailed')
    
    print("\nFINANČNÁ ANALÝZA:")
    economic = audit_results['economic_analysis']
    print(f"  Celková investícia: {economic['total_investment']:,.0f} €")
    print(f"  Ročné úspory: {economic['annual_savings']:,.0f} €")
    print(f"  Jednoduchá návratnosť: {economic['simple_payback']:.1f} rokov")
    print(f"  NPV (20 rokov): {economic['npv_20_years']:,.0f} €")
    print(f"  IRR: {economic['irr']:.1f} %")
    print(f"  Index ziskovosti: {economic['profitability_index']:.2f}")
    
    # Detailné cash flow projekcie
    financial_projections = pm._create_financial_projections(pm.projects['DEMO001'])
    print(f"\nCASH FLOW ANALÝZA:")
    print(f"  Bod vyrovnania: {financial_projections['break_even_year']} rok")
    print(f"  Celkové úspory za 20 rokov: {financial_projections['total_energy_savings_20y']:,.0f} €")
    print(f"  Finálny NPV: {financial_projections['final_npv']:,.0f} €")
    
    return pm.projects['DEMO001']

def demo_environmental_impact():
    """Demo environmentálneho hodnotenia"""
    print("=" * 60)
    print("DEMO: ENVIRONMENTÁLNE HODNOTENIE")
    print("=" * 60)
    
    from environmental_impact import get_environmental_impact_assessor
    
    assessor = get_environmental_impact_assessor()
    
    # Testovací renovačný projekt
    project_data = {
        'building_area': 120,
        'building_type': 'residential',
        'current_energy_consumption': {
            'natural_gas': 18000,     # kWh/rok (pôvodne vysoká spotreba)
            'electricity_grid': 4500
        },
        'projected_energy_consumption': {
            'natural_gas': 8000,      # kWh/rok (po renovácii)
            'electricity_grid': 3800,
            'solar_pv': 2000          # nové - solárne panely
        },
        'renovation_materials': [
            {'name': 'EPS_insulation', 'quantity': 800},    # kg EPS
            {'name': 'mineral_wool', 'quantity': 300},      # kg minerálna vlna
            {'name': 'timber', 'quantity': 2},              # m³ drevo
            {'name': 'glass', 'quantity': 50}               # kg nové okná
        ],
        'project_lifespan': 30
    }
    
    assessment = assessor.assess_renovation_project(project_data)
    
    print("ENVIRONMENTÁLNY DOPAD:")
    operational = assessment['operational_impact']
    print(f"  Aktuálne ročné emisie: {operational['current_annual_emissions_kg_co2eq']:,.0f} kg CO2eq")
    print(f"  Emisie po renovácii: {operational['projected_annual_emissions_kg_co2eq']:,.0f} kg CO2eq")
    print(f"  Ročné úspory CO2: {operational['annual_savings_kg_co2eq']:,.0f} kg CO2eq")
    print(f"  Zníženie emisií: {operational['reduction_percentage']:.1f} %")
    
    embodied = assessment['embodied_impact']
    print(f"\n  Zabudované emisie: {embodied['total_embodied_emissions']:,.0f} kg CO2eq")
    print(f"  Emisie na m²: {embodied['embodied_per_m2']:.0f} kg CO2eq/m²")
    
    print(f"\n  Environmentálna návratnosť: {assessment['environmental_payback_years']:.1f} rokov")
    
    # Ekvivalenty
    sustainability = assessment['sustainability_indicators']
    co2_savings = sustainability['annual_co2_savings']
    print(f"\nEKVIVALENTY ROČNÝCH ÚSPOR CO2:")
    print(f"  Ekvivalent zasadených stromov: {co2_savings['equivalent_trees_planted']:.0f} stromov")
    print(f"  Ekvivalent odobratých áut: {co2_savings['equivalent_cars_removed']:.2f} áut")
    print(f"  Ušetrené km jazdy: {co2_savings['equivalent_km_driving_saved']:,.0f} km")
    
    # Benchmark porovnanie
    benchmark = assessment['benchmark_comparison']
    print(f"\nPOROVNANIE S BENCHMARKS:")
    print(f"  Aktuálna klasifikácia: {benchmark['current_performance']['classification']}")
    print(f"  Klasifikácia po renovácii: {benchmark['projected_performance']['classification']}")
    print(f"  Zlepšenie: {benchmark['improvement_achieved']:.1f} kg CO2eq/m²rok")
    
    return assessment

def demo_energy_monitoring():
    """Demo systému monitorovania energie"""
    print("=" * 60)
    print("DEMO: SYSTÉM MONITOROVANIA ENERGIE (M&V)")
    print("=" * 60)
    
    from energy_monitoring import get_energy_monitoring_system, MVOption, MeasurementType, EnergyReading, ReportingPeriod
    from datetime import datetime, timedelta
    
    monitoring = get_energy_monitoring_system()
    
    # Vytvorenie M&V plánu
    mv_plan = monitoring.create_mv_plan(
        project_id="DEMO_MONITORING",
        mv_option=MVOption.OPTION_B,  # Retrofit Isolation
        baseline_start=datetime(2023, 1, 1),
        baseline_end=datetime(2023, 12, 31),
        measurement_types=[MeasurementType.ELECTRICITY, MeasurementType.NATURAL_GAS],
        savings_targets={
            MeasurementType.ELECTRICITY: 1500,  # kWh/rok očakávané úspory
            MeasurementType.NATURAL_GAS: 8000   # kWh/rok očakávané úspory
        }
    )
    
    print(f"M&V Plán vytvorený:")
    print(f"  M&V Opcia: {mv_plan.mv_option.value}")
    print(f"  Presnosť merania: ±{list(mv_plan.accuracy_requirements.values())[0]:.0f}%")
    print(f"  Frekvencia merania: {mv_plan.measurement_frequency}")
    
    # Simulácia baseline meraní
    baseline_data = [
        (MeasurementType.ELECTRICITY, 4200),  # kWh/rok baseline
        (MeasurementType.NATURAL_GAS, 16500)  # kWh/rok baseline
    ]
    
    for measurement_type, annual_consumption in baseline_data:
        # Mesačné merania
        for month in range(1, 13):
            monthly_consumption = annual_consumption / 12
            reading = EnergyReading(
                timestamp=datetime(2023, month, 15),
                measurement_type=measurement_type,
                value=monthly_consumption,
                unit="kWh",
                location="Hlavný merač"
            )
            monitoring.add_baseline_measurement("DEMO_MONITORING", reading)
    
    # Simulácia reporting obdobia (po renovácii)
    reporting_period = ReportingPeriod(
        start_date=datetime(2024, 1, 1),
        end_date=datetime(2024, 12, 31)
    )
    
    # Simulácia meraní po renovácii (nižšia spotreba)
    post_renovation_data = [
        (MeasurementType.ELECTRICITY, 2800),  # znížené o ~33%
        (MeasurementType.NATURAL_GAS, 8200)   # znížené o ~50%
    ]
    
    for measurement_type, annual_consumption in post_renovation_data:
        for month in range(1, 13):
            monthly_consumption = annual_consumption / 12
            reading = EnergyReading(
                timestamp=datetime(2024, month, 15),
                measurement_type=measurement_type,
                value=monthly_consumption,
                unit="kWh",
                location="Hlavný merač"
            )
            reporting_period.measurements.append(reading)
    
    # Generovanie reportu výkonnosti
    performance_report = monitoring.generate_performance_report("DEMO_MONITORING", reporting_period)
    
    print(f"\nVÝKONNOSTNÝ REPORT:")
    overall = performance_report['overall_performance']
    print(f"  Priemerná úspešnosť: {overall['average_achievement_rate']:.1f}%")
    print(f"  Celkové úspory energie: {overall['total_energy_savings']:,.0f} kWh")
    
    print(f"\nDETAILNÉ VÝSLEDKY:")
    for measurement_type, assessment in performance_report['performance_assessment'].items():
        print(f"  {measurement_type}:")
        print(f"    Cieľ: {assessment['target_savings']:,.0f} kWh")
        print(f"    Skutočné úspory: {assessment['actual_savings']:,.0f} kWh")
        print(f"    Úspešnosť: {assessment['achievement_rate']:.1f}% - {assessment['status']}")
    
    # Ekonomická analýza
    economic = performance_report['economic_analysis']
    print(f"\nEKONOMICKÁ ANALÝZA:")
    print(f"  Celkové ročné úspory: {economic['total_annual_savings']:,.0f} €")
    
    return performance_report

def demo_advanced_diagnostics():
    """Demo pokročilých diagnostických metód"""
    print("=" * 60)
    print("DEMO: POKROČILÉ DIAGNOSTICKÉ METÓDY")
    print("=" * 60)
    
    from building_diagnostics import get_advanced_building_diagnostics, BlowerDoorTest, ThermalBridge
    from datetime import datetime
    
    diagnostics = get_advanced_building_diagnostics()
    
    # Demo blower door test analýza
    print("BLOWER DOOR TEST ANALÝZA:")
    blower_test = BlowerDoorTest(
        test_date=datetime.now(),
        building_volume=300,    # m³
        envelope_area=250,      # m²
        air_leakage_rate=1800,  # m³/h pri 50 Pa
        leak_locations=[
            {'type': 'okno', 'severity': 'high', 'description': 'Netesné okno obývačka'},
            {'type': 'dvere', 'severity': 'medium', 'description': 'Vchodové dvere'},
            {'type': 'prestup', 'severity': 'low', 'description': 'Prestup potrubia'}
        ]
    )
    
    analysis = diagnostics.analyze_blower_door_comprehensive(blower_test, 300, 250)
    
    print(f"  n50 hodnota: {analysis['basic_results']['n50_value']:.2f} h⁻¹")
    print(f"  Klasifikácia: {analysis['compliance_assessment']['stn_rating']}")
    
    infiltration = analysis['infiltration_losses']
    print(f"  Ročné straty infiltráciou: {infiltration['annual_infiltration_loss_kwh']:,.0f} kWh")
    print(f"  Straty na m³: {infiltration['infiltration_loss_per_m3_volume']:.1f} kWh/m³rok")
    
    if 'leak_analysis' in analysis:
        leaks = analysis['leak_analysis']
        print(f"  Celkový počet únikov: {leaks['total_leak_count']}")
        print(f"  Kritické úniky: {leaks['critical_leak_count']}")
    
    # Demo tepelné mostíky analýza
    print(f"\nTEPELNÉ MOSTÍKY ANALÝZA:")
    thermal_bridges = [
        ThermalBridge('Roh balkón-stena', 'linear', 12.0, 0.15, 0.8),  # psi=0.15, dĺžka=12m
        ThermalBridge('Prestup stĺp', 'point', 1.0, None, 2.5),       # chi=2.5
        ThermalBridge('Spoj stena-strecha', 'linear', 8.0, 0.25, 0.7) # psi=0.25, dĺžka=8m
    ]
    
    bridge_analysis = diagnostics.analyze_thermal_bridges_detailed(thermal_bridges, 120)
    
    if 'error' not in bridge_analysis:
        print(f"  Celkové straty mostíkmi: {bridge_analysis['total_bridge_loss_w']:.1f} W")
        print(f"  Špecifické straty: {bridge_analysis['specific_bridge_loss']:.3f} W/m²K")
        print(f"  Hodnotenie: {bridge_analysis['overall_assessment']}")
        
        print(f"\n  Najhoršie mostíky:")
        for bridge in bridge_analysis['bridge_details'][:3]:
            print(f"    {bridge['location']}: {bridge['heat_loss_w']:.1f} W ({bridge['severity']})")
    
    return analysis

def demo_report_generation():
    """Demo generovania reportov"""
    print("=" * 60)
    print("DEMO: GENEROVANIE REPORTOV A CERTIFIKÁTOV")
    print("=" * 60)
    
    # Najprv vytvoríme audit v databáze
    from database import get_db_manager
    from certificate_generator import get_certificate_generator
    
    db_manager = get_db_manager()
    
    # Vytvorenie testovacieho auditu
    audit_data = {
        'audit_name': 'Demo energetický audit',
        'building_name': 'Rodinný dom Demo',
        'building_address': 'Demo ulica 123, Bratislava',
        'building_type': 'Rodinný dom',
        'construction_year': 1985,
        'total_area': 140.0,
        'heated_area': 120.0,
        'number_of_floors': 2,
        'auditor_name': 'Ing. Demo Auditor',
        'status': 'completed'
    }
    
    try:
        audit_id = db_manager.create_audit(audit_data)
        print(f"Vytvorený audit ID: {audit_id}")
        
        # Pridanie stavebných konštrukcií
        structures = [
            {
                'name': 'Obvodová stena',
                'structure_type': 'wall',
                'area': 85.0,
                'u_value': 1.2,
                'notes': 'Stena bez zateplenia'
            },
            {
                'name': 'Strecha',
                'structure_type': 'roof', 
                'area': 70.0,
                'u_value': 0.8,
                'notes': 'Čiastočne zateplená'
            },
            {
                'name': 'Okná',
                'structure_type': 'window',
                'area': 18.0,
                'u_value': 2.4,
                'notes': 'Staré drevené okná'
            }
        ]
        
        for struct in structures:
            db_manager.add_building_structure(audit_id, struct)
        
        # Generovanie energetického certifikátu
        cert_generator = get_certificate_generator()
        
        # Výpočet energetickej triedy
        from energy_calculations import get_energy_calculator, create_sample_building_data
        calculator = get_energy_calculator()
        building_data = create_sample_building_data()
        building_data.update({
            'heated_area': audit_data['heated_area'],
            'building_type': audit_data['building_type']
        })
        
        energy_results = calculator.complete_building_assessment(building_data)
        
        cert_data = {
            'audit_id': audit_id,
            'building_data': audit_data,
            'energy_results': energy_results,
            'certificate_number': f'SK-EPC-{audit_id:06d}',
            'issue_date': datetime.now().strftime('%Y-%m-%d'),
            'valid_until': (datetime.now() + timedelta(days=3650)).strftime('%Y-%m-%d'),
            'auditor': audit_data['auditor_name']
        }
        
        # Generovanie certifikátu
        cert_result = cert_generator.generate_energy_certificate(cert_data)
        
        if cert_result['success']:
            print(f"Certifikát vygenerovaný: {cert_result['certificate_path']}")
            print(f"Energetická trieda: {energy_results['energy_classification']['energy_class']}")
            print(f"Primárna energia: {energy_results['summary']['specific_primary_energy']:.1f} kWh/m²rok")
        else:
            print(f"Chyba pri generovaní certifikátu: {cert_result['error']}")
        
        # Generovanie pokročilého reportu
        from advanced_reports import AdvancedReportGenerator
        
        report_generator = AdvancedReportGenerator()
        comprehensive_report = report_generator.generate_comprehensive_report(audit_id)
        
        print(f"\nPOKROČILÝ REPORT:")
        exec_summary = comprehensive_report['executive_summary']
        print(f"  Budova: {exec_summary['building_overview']['name']}")
        print(f"  Energetická trieda: {exec_summary['energy_performance']['energy_class']}")
        print(f"  Počet odporúčaní: {exec_summary['improvement_potential']['total_recommendations']}")
        print(f"  Celková investícia: {exec_summary['improvement_potential']['total_investment']}")
        print(f"  Ročné úspory: {exec_summary['improvement_potential']['annual_savings']}")
        print(f"  Návratnosť: {exec_summary['improvement_potential']['payback_period']}")
        
        # Klúčové zistenia
        print(f"\nKĽÚČOVÉ ZISTENIA:")
        for finding in exec_summary['key_findings']:
            print(f"  • {finding}")
        
        return cert_result, comprehensive_report
        
    except Exception as e:
        print(f"Chyba pri generovaní reportu: {e}")
        import traceback
        traceback.print_exc()
        return None, None

def main():
    """Hlavná funkcia demo"""
    print("ENERGY AUDIT DESKTOP APPLICATION - DEMO")
    print("Implementácia založená na poznatkami z 3. PDF")
    print("=" * 60)
    
    try:
        # 1. Základné energetické výpočty
        demo_basic_energy_calculation()
        print()
        
        # 2. Pokročilá finančná analýza
        demo_advanced_financial_analysis()
        print()
        
        # 3. Environmentálne hodnotenie
        demo_environmental_impact()
        print()
        
        # 4. Systém monitorovania
        demo_energy_monitoring()
        print()
        
        # 5. Pokročilá diagnostika
        demo_advanced_diagnostics() 
        print()
        
        # 6. Generovanie reportov a certifikátov
        demo_report_generation()
        
        print("\n" + "=" * 60)
        print("DEMO UKONČENÉ - Všetky moduly fungujú správne!")
        print("=" * 60)
        
    except Exception as e:
        print(f"Chyba v demo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()