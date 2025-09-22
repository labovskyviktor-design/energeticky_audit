"""
Databázový modul pre Energy Audit aplikáciu
Obsahuje SQLite schému a základné databázové operácie
"""

import sqlite3
import os
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any

try:
    from .config import DATABASE_PATH, ensure_directories
except ImportError:
    from config import DATABASE_PATH, ensure_directories


class DatabaseManager:
    """Správca databázy pre energetický audit"""
    
    def __init__(self, db_path: Optional[Path] = None):
        """
        Inicializácia databázového manažéra
        
        Args:
            db_path: Cesta k databáze (použije sa predvolená ak nie je špecifikovaná)
        """
        self.db_path = db_path or DATABASE_PATH
        ensure_directories()
        self.init_database()
    
    def get_connection(self) -> sqlite3.Connection:
        """Vytvorenie nového pripojenia k databáze"""
        conn = sqlite3.Connection(str(self.db_path))
        conn.row_factory = sqlite3.Row  # Umožňuje pristup k stĺpcom podľa názvu
        return conn
    
    def init_database(self):
        """Inicializácia databázy a vytvorenie tabuliek"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Tabulka pre základné informácie o auditoch
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS audits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    audit_name TEXT NOT NULL,
                    building_name TEXT NOT NULL,
                    building_address TEXT,
                    building_type TEXT,
                    construction_year INTEGER,
                    total_area REAL NOT NULL,
                    heated_area REAL NOT NULL,
                    number_of_floors INTEGER,
                    created_date TEXT NOT NULL,
                    modified_date TEXT NOT NULL,
                    auditor_name TEXT,
                    auditor_license TEXT,
                    status TEXT DEFAULT 'draft',
                    notes TEXT
                )
            """)
            
            # Tabulka pre stavebné konštrukcie
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS building_structures (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    audit_id INTEGER NOT NULL,
                    structure_type TEXT NOT NULL, -- 'wall', 'roof', 'floor', 'window', 'door'
                    name TEXT NOT NULL,
                    area REAL NOT NULL,
                    u_value REAL NOT NULL, -- súčiniteľ prestupu tepla [W/m²K]
                    material_layers TEXT, -- JSON s vrstvami materiálov
                    thermal_bridges REAL DEFAULT 0,
                    notes TEXT,
                    FOREIGN KEY (audit_id) REFERENCES audits (id) ON DELETE CASCADE
                )
            """)
            
            # Tabulka pre vykurovacie systémy
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS heating_systems (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    audit_id INTEGER NOT NULL,
                    system_type TEXT NOT NULL,
                    fuel_type TEXT NOT NULL,
                    efficiency REAL NOT NULL, -- účinnosť systému [%]
                    nominal_power REAL, -- nominálny výkon [kW]
                    installation_year INTEGER,
                    maintenance_status TEXT,
                    notes TEXT,
                    FOREIGN KEY (audit_id) REFERENCES audits (id) ON DELETE CASCADE
                )
            """)
            
            # Tabulka pre systémy teplej vody
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS hot_water_systems (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    audit_id INTEGER NOT NULL,
                    system_type TEXT NOT NULL,
                    fuel_type TEXT NOT NULL,
                    efficiency REAL NOT NULL,
                    storage_volume REAL, -- objem zásobníka [l]
                    distribution_losses REAL DEFAULT 0, -- straty distribúciou [%]
                    notes TEXT,
                    FOREIGN KEY (audit_id) REFERENCES audits (id) ON DELETE CASCADE
                )
            """)
            
            # Tabulka pre ventilačné systémy
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ventilation_systems (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    audit_id INTEGER NOT NULL,
                    system_type TEXT NOT NULL, -- 'natural', 'mechanical', 'heat_recovery'
                    air_flow_rate REAL, -- prietok vzduchu [m³/h]
                    heat_recovery_efficiency REAL DEFAULT 0, -- účinnosť rekuperácie [%]
                    specific_fan_power REAL, -- špecifický výkon ventilátora [W/(m³/h)]
                    notes TEXT,
                    FOREIGN KEY (audit_id) REFERENCES audits (id) ON DELETE CASCADE
                )
            """)
            
            # Tabulka pre spotrebu energie
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS energy_consumption (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    audit_id INTEGER NOT NULL,
                    energy_type TEXT NOT NULL, -- 'heating', 'hot_water', 'electricity', 'cooling'
                    consumption_value REAL NOT NULL, -- spotreba [kWh/rok]
                    measurement_period TEXT, -- obdobie merania
                    normalized_consumption REAL, -- normalizovaná spotreba [kWh/m²rok]
                    primary_energy REAL, -- primárna energia [kWh/m²rok]
                    co2_emissions REAL, -- emisie CO2 [kg/m²rok]
                    cost REAL, -- náklady [€/rok]
                    notes TEXT,
                    FOREIGN KEY (audit_id) REFERENCES audits (id) ON DELETE CASCADE
                )
            """)
            
            # Tabulka pre energetické certifikáty
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS energy_certificates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    audit_id INTEGER NOT NULL,
                    certificate_number TEXT UNIQUE,
                    energy_class TEXT NOT NULL,
                    total_primary_energy REAL NOT NULL, -- celková primárna energia [kWh/m²rok]
                    co2_emissions_total REAL NOT NULL, -- celkové emisie CO2 [kg/m²rok]
                    issue_date TEXT NOT NULL,
                    valid_until TEXT NOT NULL,
                    certificate_file_path TEXT,
                    FOREIGN KEY (audit_id) REFERENCES audits (id) ON DELETE CASCADE
                )
            """)
            
            # Tabulka pre návrhy opatrení na zlepšenie
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS improvement_measures (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    audit_id INTEGER NOT NULL,
                    measure_category TEXT NOT NULL, -- 'insulation', 'windows', 'heating', 'ventilation'
                    measure_description TEXT NOT NULL,
                    investment_cost REAL NOT NULL, -- investičné náklady [€]
                    annual_savings REAL NOT NULL, -- ročné úspory [€/rok]
                    energy_savings REAL NOT NULL, -- úspora energie [kWh/rok]
                    payback_period REAL, -- doba návratnosti [roky]
                    priority INTEGER DEFAULT 1, -- priorita (1=vysoká, 3=nízka)
                    implementation_notes TEXT,
                    FOREIGN KEY (audit_id) REFERENCES audits (id) ON DELETE CASCADE
                )
            """)
            
            conn.commit()
            
        logging.info(f"Databáza inicializovaná: {self.db_path}")
    
    def create_audit(self, audit_data: Dict[str, Any]) -> int:
        """
        Vytvorenie nového auditu
        
        Args:
            audit_data: Slovník s údajmi o audite
            
        Returns:
            ID nového auditu
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            now = datetime.now().isoformat()
            audit_data.update({
                'created_date': now,
                'modified_date': now
            })
            
            columns = ', '.join(audit_data.keys())
            placeholders = ', '.join(['?' for _ in audit_data])
            
            cursor.execute(
                f"INSERT INTO audits ({columns}) VALUES ({placeholders})",
                list(audit_data.values())
            )
            
            audit_id = cursor.lastrowid
            conn.commit()
            
        logging.info(f"Vytvorený nový audit s ID: {audit_id}")
        return audit_id
    
    def get_audit(self, audit_id: int) -> Optional[Dict[str, Any]]:
        """Načítanie auditu podľa ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM audits WHERE id = ?", (audit_id,))
            row = cursor.fetchone()
            
            if row:
                return dict(row)
            return None
    
    def get_all_audits(self) -> List[Dict[str, Any]]:
        """Načítanie všetkých auditov"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, audit_name, building_name, building_type, 
                       created_date, modified_date, status
                FROM audits 
                ORDER BY modified_date DESC
            """)
            return [dict(row) for row in cursor.fetchall()]
    
    def update_audit(self, audit_id: int, audit_data: Dict[str, Any]) -> bool:
        """Aktualizácia existujúceho auditu"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            audit_data['modified_date'] = datetime.now().isoformat()
            
            columns = ', '.join([f"{key} = ?" for key in audit_data.keys()])
            values = list(audit_data.values()) + [audit_id]
            
            cursor.execute(
                f"UPDATE audits SET {columns} WHERE id = ?",
                values
            )
            
            affected_rows = cursor.rowcount
            conn.commit()
            
        return affected_rows > 0
    
    def delete_audit(self, audit_id: int) -> bool:
        """Vymazanie auditu a všetkých súvisiacich údajov"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM audits WHERE id = ?", (audit_id,))
            affected_rows = cursor.rowcount
            conn.commit()
            
        logging.info(f"Vymazaný audit ID: {audit_id}")
        return affected_rows > 0
    
    def add_building_structure(self, audit_id: int, structure_data: Dict[str, Any]) -> int:
        """Pridanie stavebnej konštrukcie k auditu"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            structure_data['audit_id'] = audit_id
            columns = ', '.join(structure_data.keys())
            placeholders = ', '.join(['?' for _ in structure_data])
            
            cursor.execute(
                f"INSERT INTO building_structures ({columns}) VALUES ({placeholders})",
                list(structure_data.values())
            )
            
            structure_id = cursor.lastrowid
            conn.commit()
            
        return structure_id
    
    def get_building_structures(self, audit_id: int) -> List[Dict[str, Any]]:
        """Načítanie stavebných konštrukcií pre audit"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM building_structures WHERE audit_id = ? ORDER BY structure_type, name",
                (audit_id,)
            )
            return [dict(row) for row in cursor.fetchall()]
    
    def add_energy_consumption(self, audit_id: int, consumption_data: Dict[str, Any]) -> int:
        """Pridanie záznamu o spotrebe energie"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            consumption_data['audit_id'] = audit_id
            columns = ', '.join(consumption_data.keys())
            placeholders = ', '.join(['?' for _ in consumption_data])
            
            cursor.execute(
                f"INSERT INTO energy_consumption ({columns}) VALUES ({placeholders})",
                list(consumption_data.values())
            )
            
            consumption_id = cursor.lastrowid
            conn.commit()
            
        return consumption_id
    
    def get_energy_consumption(self, audit_id: int) -> List[Dict[str, Any]]:
        """Načítanie záznamov o spotrebe energie pre audit"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM energy_consumption WHERE audit_id = ? ORDER BY energy_type",
                (audit_id,)
            )
            return [dict(row) for row in cursor.fetchall()]
    
    def create_energy_certificate(self, audit_id: int, certificate_data: Dict[str, Any]) -> int:
        """Vytvorenie energetického certifikátu"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            certificate_data['audit_id'] = audit_id
            columns = ', '.join(certificate_data.keys())
            placeholders = ', '.join(['?' for _ in certificate_data])
            
            cursor.execute(
                f"INSERT INTO energy_certificates ({columns}) VALUES ({placeholders})",
                list(certificate_data.values())
            )
            
            certificate_id = cursor.lastrowid
            conn.commit()
            
        return certificate_id
    
    def get_database_info(self) -> Dict[str, Any]:
        """Získanie informácií o databáze"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Počet auditov
            cursor.execute("SELECT COUNT(*) FROM audits")
            audit_count = cursor.fetchone()[0]
            
            # Najnovší audit
            cursor.execute("SELECT audit_name, created_date FROM audits ORDER BY created_date DESC LIMIT 1")
            latest_audit = cursor.fetchone()
            
            # Veľkosť databázového súboru
            db_size = os.path.getsize(self.db_path) if self.db_path.exists() else 0
            
            return {
                'database_path': str(self.db_path),
                'audit_count': audit_count,
                'latest_audit': dict(latest_audit) if latest_audit else None,
                'database_size_bytes': db_size,
                'database_size_mb': round(db_size / (1024 * 1024), 2)
            }


# Globálna inštancia databázového manažéra
db_manager = DatabaseManager()


def get_db_manager() -> DatabaseManager:
    """Získanie globálnej inštancie databázového manažéra"""
    return db_manager