"""
Základné testy pre Energy Audit Desktop Application
"""

import unittest
import sys
import os
from pathlib import Path
import tempfile
import sqlite3

# Pridanie src adresára do Python cesty
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

from database import DatabaseManager, get_db_manager
from energy_calculations import EnergyCalculator, get_energy_calculator, create_sample_building_data
from config import ENERGY_CLASSES, BUILDING_TYPES, HEATING_TYPES


class TestDatabaseManager(unittest.TestCase):
    """Testy pre databázový manager"""
    
    def setUp(self):
        """Nastavenie pre každý test"""
        # Vytvorenie dočasného databázového súboru
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db_manager = DatabaseManager(Path(self.temp_db.name))
    
    def tearDown(self):
        """Vyčistenie po každom teste"""
        # Vymazanie dočasného súboru
        os.unlink(self.temp_db.name)
    
    def test_database_initialization(self):
        """Test inicializácie databázy"""
        self.assertTrue(Path(self.temp_db.name).exists())
        
        # Kontrola existencie tabuliek
        with sqlite3.connect(self.temp_db.name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            expected_tables = [
                'audits', 'building_structures', 'heating_systems',
                'hot_water_systems', 'ventilation_systems', 'energy_consumption',
                'energy_certificates', 'improvement_measures'
            ]
            
            for table in expected_tables:
                self.assertIn(table, tables, f"Tabuľka {table} neexistuje")
    
    def test_create_audit(self):
        """Test vytvorenia auditu"""
        audit_data = {
            'audit_name': 'Test audit',
            'building_name': 'Test budova',
            'building_type': 'Rodinný dom',
            'total_area': 100.0,
            'heated_area': 90.0,
            'construction_year': 2020
        }
        
        audit_id = self.db_manager.create_audit(audit_data)
        self.assertIsNotNone(audit_id)
        self.assertGreater(audit_id, 0)
        
        # Načítanie auditu
        retrieved_audit = self.db_manager.get_audit(audit_id)
        self.assertIsNotNone(retrieved_audit)
        self.assertEqual(retrieved_audit['audit_name'], 'Test audit')
        self.assertEqual(retrieved_audit['building_name'], 'Test budova')
    
    def test_update_audit(self):
        """Test aktualizácie auditu"""
        # Vytvorenie auditu
        audit_data = {
            'audit_name': 'Pôvodný audit',
            'building_name': 'Test budova',
            'building_type': 'Rodinný dom',
            'total_area': 100.0,
            'heated_area': 90.0
        }
        
        audit_id = self.db_manager.create_audit(audit_data)
        
        # Aktualizácia
        updated_data = {'audit_name': 'Aktualizovaný audit'}
        success = self.db_manager.update_audit(audit_id, updated_data)
        self.assertTrue(success)
        
        # Kontrola aktualizácie
        retrieved_audit = self.db_manager.get_audit(audit_id)
        self.assertEqual(retrieved_audit['audit_name'], 'Aktualizovaný audit')
    
    def test_delete_audit(self):
        """Test vymazania auditu"""
        audit_data = {
            'audit_name': 'Test audit na vymazanie',
            'building_name': 'Test budova',
            'building_type': 'Rodinný dom',
            'total_area': 100.0,
            'heated_area': 90.0
        }
        
        audit_id = self.db_manager.create_audit(audit_data)
        
        # Vymazanie
        success = self.db_manager.delete_audit(audit_id)
        self.assertTrue(success)
        
        # Kontrola vymazania
        retrieved_audit = self.db_manager.get_audit(audit_id)
        self.assertIsNone(retrieved_audit)
    
    def test_get_all_audits(self):
        """Test načítania všetkých auditov"""
        # Vytvorenie niekoľkých auditov
        for i in range(3):
            audit_data = {
                'audit_name': f'Test audit {i+1}',
                'building_name': f'Budova {i+1}',
                'building_type': 'Rodinný dom',
                'total_area': 100.0 + i*10,
                'heated_area': 90.0 + i*10
            }
            self.db_manager.create_audit(audit_data)
        
        audits = self.db_manager.get_all_audits()
        self.assertEqual(len(audits), 3)
        
        # Kontrola zoradenia (najnovší prvý)
        self.assertGreaterEqual(audits[0]['modified_date'], audits[1]['modified_date'])
    
    def test_database_info(self):
        """Test získania informácií o databáze"""
        info = self.db_manager.get_database_info()
        
        self.assertIn('database_path', info)
        self.assertIn('audit_count', info)
        self.assertIn('database_size_bytes', info)
        self.assertIn('database_size_mb', info)
        
        self.assertEqual(info['audit_count'], 0)  # Prázdna databáza
        self.assertGreater(info['database_size_bytes'], 0)


class TestEnergyCalculator(unittest.TestCase):
    """Testy pre energetický kalkulátor"""
    
    def setUp(self):
        """Nastavenie pre každý test"""
        self.calculator = EnergyCalculator()
    
    def test_initialization(self):
        """Test inicializácie kalkulátora"""
        self.assertIsNotNone(self.calculator.thermal_constants)
        self.assertIsNotNone(self.calculator.energy_classes)
        self.assertEqual(self.calculator.internal_temp_heating, 20.0)
    
    def test_energy_classification(self):
        """Test klasifikácie energetickej efektívnosti"""
        # Test rôznych hodnôt
        test_cases = [
            (20, 'A1'),   # Extrémne úsporná
            (40, 'A2'),   # Veľmi úsporná
            (60, 'B'),    # Úsporná
            (90, 'C'),    # Mierne úsporná
            (120, 'D'),   # Menej úsporná
            (180, 'E'),   # Nehospodárna
            (220, 'F'),   # Veľmi nehospodárna
            (300, 'G'),   # Mimoriadne nehospodárna
        ]
        
        for energy_value, expected_class in test_cases:
            result = self.calculator.classify_energy_efficiency(energy_value)
            self.assertEqual(result['energy_class'], expected_class)
            self.assertEqual(result['specific_primary_energy'], energy_value)
    
    def test_heating_demand_calculation(self):
        """Test výpočtu potreby tepla na vykurovanie"""
        # Vzorové údaje
        transmission_losses = {'annual_transmission_losses': 5000}
        ventilation_losses = {'annual_ventilation_losses': 3000}
        internal_gains = {'annual_internal_gains': 2000}
        solar_gains = {'annual_solar_gains': 1000}
        floor_area = 120.0
        
        result = self.calculator.calculate_heating_demand(
            transmission_losses, ventilation_losses, internal_gains, solar_gains, floor_area
        )
        
        self.assertIn('heating_demand', result)
        self.assertIn('specific_heating_demand', result)
        self.assertIn('total_losses', result)
        self.assertIn('total_gains', result)
        
        # Základné kontroly
        self.assertEqual(result['total_losses'], 8000)  # 5000 + 3000
        self.assertEqual(result['total_gains'], 3000)   # 2000 + 1000
        self.assertGreater(result['heating_demand'], 0)
        self.assertGreater(result['specific_heating_demand'], 0)
    
    def test_hot_water_demand_calculation(self):
        """Test výpočtu potreby tepla na teplú vodu"""
        floor_area = 120.0
        building_type = 'Rodinný dom'
        
        result = self.calculator.calculate_hot_water_demand(floor_area, building_type)
        
        self.assertIn('hot_water_demand', result)
        self.assertIn('specific_hot_water_demand', result)
        self.assertIn('annual_hot_water_consumption', result)
        
        self.assertGreater(result['hot_water_demand'], 0)
        self.assertGreater(result['specific_hot_water_demand'], 0)
        self.assertGreater(result['annual_hot_water_consumption'], 0)
    
    def test_complete_building_assessment(self):
        """Test kompletného hodnotenia budovy"""
        building_data = create_sample_building_data()
        
        result = self.calculator.complete_building_assessment(building_data)
        
        # Kontrola prítomnosti všetkých sekcií
        expected_sections = [
            'transmission', 'ventilation', 'internal_gains', 'solar_gains',
            'heating_demand', 'hot_water_demand', 'primary_energy',
            'energy_classification', 'summary'
        ]
        
        for section in expected_sections:
            self.assertIn(section, result)
        
        # Kontrola súhrnu
        summary = result['summary']
        self.assertIn('energy_class', summary)
        self.assertIn('specific_primary_energy', summary)
        self.assertIn('floor_area', summary)
        
        # Kontrola, že energetická trieda je platná
        self.assertIn(summary['energy_class'], ENERGY_CLASSES.keys())


class TestConfiguration(unittest.TestCase):
    """Testy pre konfiguráciu"""
    
    def test_energy_classes(self):
        """Test energetických tried"""
        self.assertIsInstance(ENERGY_CLASSES, dict)
        self.assertIn('A1', ENERGY_CLASSES)
        self.assertIn('G', ENERGY_CLASSES)
        
        for class_name, class_data in ENERGY_CLASSES.items():
            self.assertIn('max_consumption', class_data)
            self.assertIn('color', class_data)
            self.assertIn('description', class_data)
    
    def test_building_types(self):
        """Test typov budov"""
        self.assertIsInstance(BUILDING_TYPES, list)
        self.assertIn('Rodinný dom', BUILDING_TYPES)
        self.assertIn('Bytový dom', BUILDING_TYPES)
        self.assertGreater(len(BUILDING_TYPES), 5)
    
    def test_heating_types(self):
        """Test typov vykurovania"""
        self.assertIsInstance(HEATING_TYPES, list)
        self.assertIn('Plynový kotol', HEATING_TYPES)
        self.assertIn('Elektrické vykurovanie', HEATING_TYPES)
        self.assertGreater(len(HEATING_TYPES), 5)


class TestIntegration(unittest.TestCase):
    """Integračné testy"""
    
    def setUp(self):
        """Nastavenie pre každý test"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db_manager = DatabaseManager(Path(self.temp_db.name))
        self.calculator = EnergyCalculator()
    
    def tearDown(self):
        """Vyčistenie po každom teste"""
        os.unlink(self.temp_db.name)
    
    def test_complete_workflow(self):
        """Test kompletného pracovného toku"""
        # 1. Vytvorenie auditu
        audit_data = {
            'audit_name': 'Integračný test audit',
            'building_name': 'Testovacia budova',
            'building_type': 'Rodinný dom',
            'total_area': 150.0,
            'heated_area': 120.0,
            'construction_year': 2000,
            'auditor_name': 'Test Audítor',
            'status': 'completed'
        }
        
        audit_id = self.db_manager.create_audit(audit_data)
        self.assertIsNotNone(audit_id)
        
        # 2. Pridanie stavebných konštrukcií
        structures_data = [
            {
                'structure_type': 'wall',
                'name': 'Obvodová stena',
                'area': 100.0,
                'u_value': 0.8,
                'thermal_bridges': 5.0
            },
            {
                'structure_type': 'roof',
                'name': 'Strecha',
                'area': 120.0,
                'u_value': 0.4,
                'thermal_bridges': 2.0
            }
        ]
        
        for struct_data in structures_data:
            structure_id = self.db_manager.add_building_structure(audit_id, struct_data)
            self.assertIsNotNone(structure_id)
        
        # 3. Načítanie štruktúr
        structures = self.db_manager.get_building_structures(audit_id)
        self.assertEqual(len(structures), 2)
        
        # 4. Energetický výpočet
        building_data = create_sample_building_data()
        building_data['heated_area'] = audit_data['heated_area']
        building_data['building_type'] = audit_data['building_type']
        
        energy_results = self.calculator.complete_building_assessment(building_data)
        self.assertIsNotNone(energy_results)
        self.assertIn('energy_classification', energy_results)
        
        # 5. Kontrola výsledkov
        classification = energy_results['energy_classification']
        self.assertIn('energy_class', classification)
        self.assertIn('specific_primary_energy', classification)
        
        # Energia by mala byť rozumná hodnota (nie nula alebo nekonečno)
        self.assertGreater(classification['specific_primary_energy'], 0)
        self.assertLess(classification['specific_primary_energy'], 1000)


def run_tests():
    """Spustenie všetkých testov"""
    # Vytvorenie test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Pridanie testových tried
    test_classes = [
        TestDatabaseManager,
        TestEnergyCalculator,
        TestConfiguration,
        TestIntegration
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Spustenie testov
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    print("Spúšťam testy pre Energy Audit Desktop Application...")
    print("=" * 60)
    
    success = run_tests()
    
    print("=" * 60)
    if success:
        print("✅ Všetky testy prešli úspešne!")
    else:
        print("❌ Niektoré testy zlyhali!")
        sys.exit(1)