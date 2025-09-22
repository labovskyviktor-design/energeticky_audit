"""
Test runner pre Energy Audit Desktop Application
"""

import sys
import os
from pathlib import Path
import tempfile
import sqlite3

# Pridanie src adresára do Python cesty
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

def test_basic_functionality():
    """Základný test funkcionality"""
    print("🔍 Testovanie základnej funkcionality...")
    
    try:
        # Test importov
        print("  - Test importov modulov...")
        from config import ENERGY_CLASSES, BUILDING_TYPES, HEATING_TYPES
        print("    ✅ Konfiguračné moduly")
        
        from database import DatabaseManager
        print("    ✅ Databázový modul")
        
        from energy_calculations import EnergyCalculator, create_sample_building_data
        print("    ✅ Energetický kalkulátor")
        
        from certificate_generator import CertificateGenerator
        print("    ✅ Generátor certifikátov (pozor: bez reportlab)")
        
        # Test databázy
        print("  - Test databázy...")
        temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        temp_db.close()
        
        db_manager = DatabaseManager(Path(temp_db.name))
        
        # Test vytvorenia auditu
        audit_data = {
            'audit_name': 'Test audit',
            'building_name': 'Test budova',
            'building_type': 'Rodinný dom',
            'total_area': 120.0,
            'heated_area': 100.0,
            'construction_year': 2020
        }
        
        audit_id = db_manager.create_audit(audit_data)
        assert audit_id is not None, "Audit sa nepodarilo vytvoriť"
        
        retrieved_audit = db_manager.get_audit(audit_id)
        assert retrieved_audit is not None, "Audit sa nepodarilo načítať"
        assert retrieved_audit['audit_name'] == 'Test audit', "Nesprávny názov auditu"
        
        print("    ✅ CRUD operácie s auditmi")
        
        # Vyčistenie (Windows-friendly)
        try:
            os.unlink(temp_db.name)
        except PermissionError:
            # Windows môže mať zamknutý súbor, skúsime neskor
            pass
        
        # Test energetického kalkulátora
        print("  - Test energetického kalkulátora...")
        calculator = EnergyCalculator()
        
        # Test klasifikácie
        classification = calculator.classify_energy_efficiency(150)
        assert classification['energy_class'] in ENERGY_CLASSES, "Neplatná energetická trieda"
        print("    ✅ Klasifikácia energetickej efektívnosti")
        
        # Test kompletného hodnotenia
        building_data = create_sample_building_data()
        results = calculator.complete_building_assessment(building_data)
        
        assert 'energy_classification' in results, "Chýba energetická klasifikácia"
        assert 'summary' in results, "Chýba súhrn výsledkov"
        
        summary = results['summary']
        assert 'energy_class' in summary, "Chýba energetická trieda v súhrne"
        assert summary['energy_class'] in ENERGY_CLASSES, "Neplatná energetická trieda"
        
        print("    ✅ Kompletné energetické hodnotenie")
        
        # Test konfigurácie
        print("  - Test konfigurácie...")
        assert len(ENERGY_CLASSES) == 8, f"Očakáva sa 8 energetických tried, nájdených {len(ENERGY_CLASSES)}"
        assert len(BUILDING_TYPES) > 5, f"Príliš málo typov budov: {len(BUILDING_TYPES)}"
        assert len(HEATING_TYPES) > 5, f"Príliš málo typov vykurovania: {len(HEATING_TYPES)}"
        
        print("    ✅ Konfigurácia aplikácie")
        
        print("✅ Všetky základné testy prešli úspešne!")
        return True
        
    except Exception as e:
        print(f"❌ Test zlyhal: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_gui_import():
    """Test importu GUI komponentov"""
    print("🔍 Testovanie GUI komponentov...")
    
    try:
        # Test bez spustenia GUI
        from main import EnergyAuditApp
        print("    ✅ Hlavná aplikácia")
        
        from audit_forms import AuditFormDialog, AuditListFrame
        print("    ✅ Formuláre auditov")
        
        print("✅ GUI komponenty sa dajú importovať!")
        return True
        
    except Exception as e:
        print(f"❌ Test GUI zlyhal: {str(e)}")
        return False

def test_integration():
    """Integračný test"""
    print("🔍 Testovanie integrácie...")
    
    try:
        # Import všetkých modulov
        from database import DatabaseManager
        from energy_calculations import EnergyCalculator, create_sample_building_data
        
        # Vytvorenie dočasnej databázy
        temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        temp_db.close()
        
        db_manager = DatabaseManager(Path(temp_db.name))
        calculator = EnergyCalculator()
        
        # Pracovný tok: vytvorenie -> výpočet -> uloženie
        audit_data = {
            'audit_name': 'Integračný test',
            'building_name': 'Testovacia budova',
            'building_type': 'Rodinný dom',
            'total_area': 150.0,
            'heated_area': 120.0,
            'construction_year': 1995
        }
        
        # 1. Vytvorenie auditu
        audit_id = db_manager.create_audit(audit_data)
        
        # 2. Energetický výpočet
        building_data = create_sample_building_data()
        building_data['heated_area'] = audit_data['heated_area']
        results = calculator.complete_building_assessment(building_data)
        
        # 3. Kontrola výsledkov
        assert results['summary']['energy_class'] in ['D', 'E', 'F'], "Neočakávaná energetická trieda pre testovací dom"
        
        # 4. Aktualizácia auditu s výsledkami
        update_data = {
            'status': 'completed',
            'notes': f"Energetická trieda: {results['summary']['energy_class']}"
        }
        db_manager.update_audit(audit_id, update_data)
        
        # 5. Finálna kontrola
        final_audit = db_manager.get_audit(audit_id)
        assert final_audit['status'] == 'completed'
        
        # Vyčistenie (Windows-friendly)
        try:
            os.unlink(temp_db.name)
        except PermissionError:
            # Windows môže mať zamknutý súbor
            pass
        
        print("✅ Integračný test úspešný!")
        return True
        
    except Exception as e:
        print(f"❌ Integračný test zlyhal: {str(e)}")
        return False

def main():
    """Hlavná funkcia test runnera"""
    print("=" * 60)
    print("🧪 Energy Audit Desktop Application - Test Suite")
    print("=" * 60)
    print()
    
    tests = [
        test_basic_functionality,
        test_gui_import,
        test_integration
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} havaroval: {str(e)}")
            failed += 1
        print()
    
    print("=" * 60)
    print(f"📊 Výsledky testov:")
    print(f"   ✅ Úspešných: {passed}")
    print(f"   ❌ Zlyhaných: {failed}")
    print(f"   📈 Úspešnosť: {passed/(passed+failed)*100:.1f}%")
    print("=" * 60)
    
    if failed == 0:
        print("🎉 Všetky testy prešli úspešne!")
        print("📋 Aplikácia je pripravená na použitie!")
        print()
        print("💡 Pre spustenie aplikácie použite:")
        print("   python run.py")
        print()
        return True
    else:
        print("⚠️  Niektoré testy zlyhali. Skontrolujte chybové hlášky vyššie.")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)