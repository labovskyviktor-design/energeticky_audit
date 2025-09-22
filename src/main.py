#!/usr/bin/env python3
"""
Energy Audit Desktop Application
Hlavný vstupný bod aplikácie pre energetický audit a certifikáciu budov.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
from pathlib import Path
import logging

# Pridanie src adresára do Python cesty
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import modulov aplikácie
try:
    from .database import get_db_manager
    from .audit_forms import AuditFormDialog, AuditListFrame, show_audit_form
    from .energy_calculations import get_energy_calculator
    from .certificate_generator import get_certificate_generator
except ImportError:
    # Fallback pre spustenie bez relative importov
    from database import get_db_manager
    from audit_forms import AuditFormDialog, AuditListFrame, show_audit_form
    from energy_calculations import get_energy_calculator
    from certificate_generator import get_certificate_generator

class EnergyAuditApp:
    """Hlavná trieda aplikácie pre energetický audit"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Energy Audit - Energetický Audit Budov")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Inicializácia databázy a kalkulatora
        self.db_manager = get_db_manager()
        self.energy_calculator = get_energy_calculator()
        self.certificate_generator = get_certificate_generator()
        
        # Aktuálny audit
        self.current_audit_id = None
        
        # Nastavenie štýlu
        self.setup_styles()
        
        # Vytvorenie hlavného menu
        self.create_menu()
        
        # Vytvorenie hlavného rozloženia
        self.create_main_layout()
        
    def setup_styles(self):
        """Nastavenie štýlov pre aplikáciu"""
        style = ttk.Style()
        style.theme_use('clam')
        
    def create_menu(self):
        """Vytvorenie menu baru"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Súbor menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Súbor", menu=file_menu)
        file_menu.add_command(label="Nový audit", command=self.new_audit)
        file_menu.add_command(label="Otvoriť audit", command=self.open_audit)
        file_menu.add_command(label="Uložiť audit", command=self.save_audit)
        file_menu.add_separator()
        file_menu.add_command(label="Ukončiť", command=self.root.quit)
        
        # Nástroje menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Nástroje", menu=tools_menu)
        tools_menu.add_command(label="Kalkulačka energií", command=self.energy_calculator)
        tools_menu.add_command(label="Generátor certifikátu", command=self.certificate_generator)
        
        # Pomoc menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Pomoc", menu=help_menu)
        help_menu.add_command(label="O aplikácii", command=self.about)
        
    def create_main_layout(self):
        """Vytvorenie hlavného rozloženia aplikácie"""
        # Hlavný frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Konfigurácia grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        # Ľavý panel s nástrojmi
        left_panel = ttk.LabelFrame(main_frame, text="Nástroje", padding="5")
        left_panel.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Tlačidlá v ľavom paneli
        ttk.Button(left_panel, text="Nový Audit", command=self.new_audit).pack(fill=tk.X, pady=2)
        ttk.Button(left_panel, text="Otvoriť Audit", command=self.open_audit).pack(fill=tk.X, pady=2)
        ttk.Button(left_panel, text="Uložiť Audit", command=self.save_audit).pack(fill=tk.X, pady=2)
        ttk.Separator(left_panel, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        ttk.Button(left_panel, text="Kalkulačka", command=self.energy_calculator).pack(fill=tk.X, pady=2)
        ttk.Button(left_panel, text="Certifikát", command=self.certificate_generator).pack(fill=tk.X, pady=2)
        
        # Hlavný pracovný priestor
        work_area = ttk.LabelFrame(main_frame, text="Pracovný priestor", padding="5")
        work_area.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        work_area.columnconfigure(0, weight=1)
        work_area.rowconfigure(0, weight=1)
        
        # Notebook pre taby
        self.notebook = ttk.Notebook(work_area)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Tab so zoznamom auditov
        audit_list_frame = ttk.Frame(self.notebook, padding="5")
        self.notebook.add(audit_list_frame, text="Zoznam auditov")
        
        # Vytvorenie zoznamu auditov
        self.audit_list = AuditListFrame(audit_list_frame, on_audit_select=self.open_audit_details)
        self.audit_list.pack(fill=tk.BOTH, expand=True)
        
    # Metódy pre menu akcie
    def new_audit(self):
        """Vytvorenie nového auditu"""
        try:
            result = show_audit_form(self.root, on_save_callback=self.on_audit_saved)
        except Exception as e:
            messagebox.showerror("Chyba", f"Nepodarilo sa otvoriť formulár auditu: {str(e)}")
        
    def open_audit(self):
        """Otvorenie existujúceho auditu"""
        # Refresh audit list to show any changes
        if hasattr(self, 'audit_list'):
            self.audit_list.refresh_list()
        messagebox.showinfo("Info", "Pre otvorenie auditu dvojkliknite na audit v zozname")
        
    def save_audit(self):
        """Uloženie aktuálneho auditu"""
        if self.current_audit_id:
            messagebox.showinfo("Info", f"Audit s ID {self.current_audit_id} je automaticky uložený")
        else:
            messagebox.showinfo("Info", "Žadny audit nie je aktuálne otvorený")
        
    def energy_calculator(self):
        """Spustenie kalkulačky energií"""
        if not self.current_audit_id:
            messagebox.showwarning("Upozornenie", "Najprv vyberte alebo vytvorte audit")
            return
        
        try:
            # Načítanie údajov auditu
            audit_data = self.db_manager.get_audit(self.current_audit_id)
            if not audit_data:
                messagebox.showerror("Chyba", "Nepodarilo sa načítať audit")
                return
            
            # Prvý prepáračný výpočet
            building_data = {
                'heated_area': audit_data.get('heated_area', 100),
                'building_type': audit_data.get('building_type', 'Rodinný dom'),
                'structures': [
                    {'name': 'Obvodová stena', 'structure_type': 'wall', 'area': 100, 'u_value': 1.0, 'thermal_bridges': 0},
                    {'name': 'Strecha', 'structure_type': 'roof', 'area': audit_data.get('heated_area', 100), 'u_value': 0.8, 'thermal_bridges': 0},
                    {'name': 'Podlaha', 'structure_type': 'floor', 'area': audit_data.get('heated_area', 100), 'u_value': 0.8, 'thermal_bridges': 0},
                    {'name': 'Okná', 'structure_type': 'window', 'area': 20, 'u_value': 1.5, 'thermal_bridges': 0}
                ],
                'heating_system': {'system_type': 'Plynový kotol', 'fuel_type': 'Zemný plyn', 'efficiency': 85.0}
            }
            
            results = self.energy_calculator.complete_building_assessment(building_data)
            
            # Zobrazenie výsledkov
            summary = results['summary']
            classification = results['energy_classification']
            
            result_text = (
                f"Výsledky energetického výpočtu:\n\n"
                f"Energetická trieda: {classification['energy_class']}\n"
                f"Popis: {classification['class_description']}\n\n"
                f"Špecifická potreba tepla na vykurovanie: {summary['specific_heating_demand']:.1f} kWh/m²rok\n"
                f"Špecifická potreba tepla na teplú vodu: {summary['specific_hot_water_demand']:.1f} kWh/m²rok\n"
                f"Špecifická spotreba primárnej energie: {summary['specific_primary_energy']:.1f} kWh/m²rok\n"
                f"Špecifické emisie CO₂: {summary['specific_co2_emissions']:.1f} kg/m²rok"
            )
            
            messagebox.showinfo("Výsledky výpočtu", result_text)
            
        except Exception as e:
            messagebox.showerror("Chyba", f"Chyba pri výpočte: {str(e)}")
        
    def certificate_generator(self):
        """Spustenie generátora certifikátu"""
        if not self.current_audit_id:
            messagebox.showwarning("Upozornenie", "Najprv vyberte alebo vytvorte audit")
            return
        
        try:
            # Generovanie certifikátu
            certificate_path = self.certificate_generator.generate_certificate(self.current_audit_id)
            
            if certificate_path:
                result = messagebox.askyesno(
                    "Úspech", 
                    f"Certifikát bol úspešne vygenerovaný:\n{certificate_path}\n\nChcete otvoriť adresár s certifikátom?"
                )
                
                if result:
                    # Otvorenie adresára s certifikátom
                    import subprocess
                    subprocess.run(["explorer", str(certificate_path.parent)], check=False)
            else:
                messagebox.showerror("Chyba", "Nepodarilo sa vygenerovať certifikát")
                
        except Exception as e:
            messagebox.showerror("Chyba", f"Chyba pri generovaní certifikátu: {str(e)}")
        
    def about(self):
        """Zobrazenie informácií o aplikácii"""
        db_info = self.db_manager.get_database_info()
        info_text = (
            "Energy Audit Desktop Application\n"
            "Verzia 1.0.0\n\n"
            "Aplikácia na vykonávanie energetického auditu\n"
            "a certifikáciu budov.\n\n"
            f"Databáza: {db_info['audit_count']} auditov\n"
            f"Veľkosť DB: {db_info['database_size_mb']} MB"
        )
        messagebox.showinfo("O aplikácii", info_text)
    
    def on_audit_saved(self, result):
        """Callback po uložení auditu"""
        if hasattr(self, 'audit_list'):
            self.audit_list.refresh_list()
        
        if result and result.get('action') == 'created':
            self.current_audit_id = result.get('id')
    
    def open_audit_details(self, audit_id):
        """Otvorenie detailov auditu"""
        self.current_audit_id = audit_id
        
        # Načítanie údajov auditu
        audit_data = self.db_manager.get_audit(audit_id)
        if audit_data:
            # Zobrazenie informácií o audite
            info_text = (
                f"Audit: {audit_data.get('audit_name', 'Bez názvu')}\n"
                f"Budova: {audit_data.get('building_name', 'Bez názvu')}\n"
                f"Typ: {audit_data.get('building_type', 'Neuvedený')}\n"
                f"Plocha: {audit_data.get('total_area', 0)} m²\n"
                f"Stav: {audit_data.get('status', 'draft')}"
            )
            messagebox.showinfo("Detail auditu", info_text)
        else:
            messagebox.showerror("Chyba", "Nepodarilo sa načítať audit")

def main():
    """Hlavná funkcia aplikácie"""
    root = tk.Tk()
    app = EnergyAuditApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()