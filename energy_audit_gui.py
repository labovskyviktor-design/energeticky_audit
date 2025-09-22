#!/usr/bin/env python3
"""
ENERGY AUDIT DESKTOP APPLICATION
Profesionálny desktop interface pre energetický audit systém
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import json
from datetime import datetime
import os
import sys
from pathlib import Path

# Pridanie src do path
sys.path.append(str(Path(__file__).parent / 'src'))

class EnergyAuditGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🏢 Profesionálny Energetický Audit Systém")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        self.root.state('zoomed')  # Maximalizovať okno na Windows
        
        # Dáta auditu
        self.audit_data = {}
        self.results = {}
        
        # Vytvorenie GUI
        self.create_widgets()
        self.create_status_bar()
        
    def create_widgets(self):
        """Vytvorenie hlavných GUI komponentov"""
        
        # Hlavný nadpis
        self.create_header()
        
        # Notebook pre taby
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Vytvorenie jednotlivých tabov
        self.create_building_tab()
        self.create_envelope_tab()
        self.create_systems_tab()
        self.create_usage_tab()
        self.create_results_tab()
        self.create_report_tab()
        
        # Bottom panel s tlačidlami
        self.create_bottom_panel()
        
    def create_header(self):
        """Vytvorenie hlavičky"""
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        header_frame.pack(fill=tk.X, padx=10, pady=5)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, 
                              text="🏢 PROFESIONÁLNY ENERGETICKÝ AUDIT SYSTÉM",
                              font=('Arial', 18, 'bold'), 
                              fg='white', bg='#2c3e50')
        title_label.pack(pady=15)
        
        subtitle_label = tk.Label(header_frame,
                                 text="📋 Podľa STN EN 16247 a slovenských noriem",
                                 font=('Arial', 10), 
                                 fg='#ecf0f1', bg='#2c3e50')
        subtitle_label.pack()
        
    def create_building_tab(self):
        """Tab pre základné údaje budovy"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🏢 Základné údaje")
        
        # Scroll frame
        canvas = tk.Canvas(tab)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Základné informácie
        info_frame = ttk.LabelFrame(scrollable_frame, text="📋 Základné informácie", padding=10)
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Názov budovy
        ttk.Label(info_frame, text="Názov budovy:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.building_name = ttk.Entry(info_frame, width=40)
        self.building_name.grid(row=0, column=1, padx=5, pady=5)
        
        # Adresa
        ttk.Label(info_frame, text="Adresa:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.building_address = ttk.Entry(info_frame, width=40)
        self.building_address.grid(row=1, column=1, padx=5, pady=5)
        
        # Typ budovy
        ttk.Label(info_frame, text="Typ budovy:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.building_type = ttk.Combobox(info_frame, values=[
            "Rodinný dom", "Bytový dom", "Administratívna budova", 
            "Priemyselná budova", "Škola", "Nemocnica", "Hotel", "Obchodné centrum"
        ], width=37, state="readonly")
        self.building_type.grid(row=2, column=1, padx=5, pady=5)
        self.building_type.set("Rodinný dom")
        
        # Rok výstavby
        ttk.Label(info_frame, text="Rok výstavby:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.construction_year = ttk.Entry(info_frame, width=40)
        self.construction_year.grid(row=3, column=1, padx=5, pady=5)
        self.construction_year.insert(0, "2000")
        
        # Geometrické parametre
        geom_frame = ttk.LabelFrame(scrollable_frame, text="📐 Geometrické parametre", padding=10)
        geom_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Podlahová plocha
        ttk.Label(geom_frame, text="Podlahová plocha [m²]:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.floor_area = ttk.Entry(geom_frame, width=20)
        self.floor_area.grid(row=0, column=1, padx=5, pady=5)
        self.floor_area.insert(0, "120")
        
        # Vykurovaná plocha
        ttk.Label(geom_frame, text="Vykurovaná plocha [m²]:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.heated_area = ttk.Entry(geom_frame, width=20)
        self.heated_area.grid(row=0, column=3, padx=5, pady=5)
        self.heated_area.insert(0, "115")
        
        # Objem
        ttk.Label(geom_frame, text="Objem budovy [m³]:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.volume = ttk.Entry(geom_frame, width=20)
        self.volume.grid(row=1, column=1, padx=5, pady=5)
        self.volume.insert(0, "350")
        
        # Výška
        ttk.Label(geom_frame, text="Výška budovy [m]:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        self.height = ttk.Entry(geom_frame, width=20)
        self.height.grid(row=1, column=3, padx=5, pady=5)
        self.height.insert(0, "8.5")
        
        # Počet podlaží
        ttk.Label(geom_frame, text="Počet podlaží:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.floors = ttk.Entry(geom_frame, width=20)
        self.floors.grid(row=2, column=1, padx=5, pady=5)
        self.floors.insert(0, "2")
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_envelope_tab(self):
        """Tab pre obálku budovy"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🏠 Obálka budovy")
        
        # Scroll frame
        canvas = tk.Canvas(tab)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Obvodové steny
        wall_frame = ttk.LabelFrame(scrollable_frame, text="🧱 Obvodové steny", padding=10)
        wall_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(wall_frame, text="Plocha stien [m²]:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.wall_area = ttk.Entry(wall_frame, width=20)
        self.wall_area.grid(row=0, column=1, padx=5, pady=5)
        self.wall_area.insert(0, "150")
        
        ttk.Label(wall_frame, text="Typ konštrukcie:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.wall_type = ttk.Combobox(wall_frame, values=[
            "Muriva s kontaktnou izoláciou",
            "Sendvičová murovaná",
            "Železobetónová s izoláciou", 
            "Drevená konštrukcia"
        ], width=30, state="readonly")
        self.wall_type.grid(row=0, column=3, padx=5, pady=5)
        self.wall_type.set("Muriva s kontaktnou izoláciou")
        
        ttk.Label(wall_frame, text="U-hodnota [W/m²K]:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.wall_u = ttk.Entry(wall_frame, width=20)
        self.wall_u.grid(row=1, column=1, padx=5, pady=5)
        self.wall_u.insert(0, "0.25")
        
        # Strecha
        roof_frame = ttk.LabelFrame(scrollable_frame, text="🏠 Strecha", padding=10)
        roof_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(roof_frame, text="Plocha strechy [m²]:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.roof_area = ttk.Entry(roof_frame, width=20)
        self.roof_area.grid(row=0, column=1, padx=5, pady=5)
        self.roof_area.insert(0, "80")
        
        ttk.Label(roof_frame, text="U-hodnota [W/m²K]:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.roof_u = ttk.Entry(roof_frame, width=20)
        self.roof_u.grid(row=0, column=3, padx=5, pady=5)
        self.roof_u.insert(0, "0.20")
        
        # Podlaha
        floor_frame = ttk.LabelFrame(scrollable_frame, text="🔲 Podlaha", padding=10)
        floor_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(floor_frame, text="Plocha podlahy [m²]:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.floor_envelope_area = ttk.Entry(floor_frame, width=20)
        self.floor_envelope_area.grid(row=0, column=1, padx=5, pady=5)
        self.floor_envelope_area.insert(0, "80")
        
        ttk.Label(floor_frame, text="U-hodnota [W/m²K]:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.floor_u = ttk.Entry(floor_frame, width=20)
        self.floor_u.grid(row=0, column=3, padx=5, pady=5)
        self.floor_u.insert(0, "0.30")
        
        # Okná
        window_frame = ttk.LabelFrame(scrollable_frame, text="🪟 Okná", padding=10)
        window_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(window_frame, text="Plocha okien [m²]:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.window_area = ttk.Entry(window_frame, width=20)
        self.window_area.grid(row=0, column=1, padx=5, pady=5)
        self.window_area.insert(0, "25")
        
        ttk.Label(window_frame, text="Typ okien:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.window_type = ttk.Combobox(window_frame, values=[
            "Jednosklo (U=5.0)",
            "Dvojsklo (U=2.8)", 
            "Trojsklo (U=1.1)",
            "Pasívne okná (U=0.8)"
        ], width=25, state="readonly")
        self.window_type.grid(row=0, column=3, padx=5, pady=5)
        self.window_type.set("Trojsklo (U=1.1)")
        
        ttk.Label(window_frame, text="U-hodnota [W/m²K]:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.window_u = ttk.Entry(window_frame, width=20)
        self.window_u.grid(row=1, column=1, padx=5, pady=5)
        self.window_u.insert(0, "1.1")
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_systems_tab(self):
        """Tab pre technické systémy"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="⚙️ Technické systémy")
        
        # Scroll frame
        canvas = tk.Canvas(tab)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Vykurovanie
        heating_frame = ttk.LabelFrame(scrollable_frame, text="🔥 Vykurovací systém", padding=10)
        heating_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(heating_frame, text="Typ systému:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.heating_type = ttk.Combobox(heating_frame, values=[
            "Plynový kotol",
            "Elektrické vykurovanie",
            "Tepelné čerpadlo",
            "Biomasa",
            "Diaľkové vykurovanie"
        ], width=25, state="readonly")
        self.heating_type.grid(row=0, column=1, padx=5, pady=5)
        self.heating_type.set("Plynový kotol")
        
        ttk.Label(heating_frame, text="Účinnosť [%]:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.heating_efficiency = ttk.Entry(heating_frame, width=15)
        self.heating_efficiency.grid(row=0, column=3, padx=5, pady=5)
        self.heating_efficiency.insert(0, "90")
        
        # Teplá voda
        dhw_frame = ttk.LabelFrame(scrollable_frame, text="🚿 Príprava teplej vody", padding=10)
        dhw_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(dhw_frame, text="Typ systému:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.dhw_type = ttk.Combobox(dhw_frame, values=[
            "Plynový kotol",
            "Elektrické vykurovanie",
            "Tepelné čerpadlo",
            "Biomasa",
            "Diaľkové vykurovanie"
        ], width=25, state="readonly")
        self.dhw_type.grid(row=0, column=1, padx=5, pady=5)
        self.dhw_type.set("Elektrické vykurovanie")
        
        ttk.Label(dhw_frame, text="Účinnosť [%]:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.dhw_efficiency = ttk.Entry(dhw_frame, width=15)
        self.dhw_efficiency.grid(row=0, column=3, padx=5, pady=5)
        self.dhw_efficiency.insert(0, "100")
        
        # Vetranie
        vent_frame = ttk.LabelFrame(scrollable_frame, text="🌬️ Vetranie", padding=10)
        vent_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(vent_frame, text="Typ vetrania:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.ventilation_type = ttk.Combobox(vent_frame, values=[
            "Prirodzené vetranie",
            "Mechanické vetranie",
            "Rekuperácia (účinnosť 70%)",
            "Rekuperácia (účinnosť 85%)"
        ], width=30, state="readonly")
        self.ventilation_type.grid(row=0, column=1, padx=5, pady=5)
        self.ventilation_type.set("Prirodzené vetranie")
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_usage_tab(self):
        """Tab pre užívanie budovy"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="👥 Užívanie")
        
        # Scroll frame
        canvas = tk.Canvas(tab)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Užívatelia
        users_frame = ttk.LabelFrame(scrollable_frame, text="👥 Užívatelia", padding=10)
        users_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(users_frame, text="Počet obyvateľov/užívateľov:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.occupants = ttk.Entry(users_frame, width=15)
        self.occupants.grid(row=0, column=1, padx=5, pady=5)
        self.occupants.insert(0, "4")
        
        # Teploty
        temps_frame = ttk.LabelFrame(scrollable_frame, text="🌡️ Teploty", padding=10)
        temps_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(temps_frame, text="Teplota vykurovania [°C]:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.heating_temp = ttk.Entry(temps_frame, width=15)
        self.heating_temp.grid(row=0, column=1, padx=5, pady=5)
        self.heating_temp.insert(0, "20")
        
        ttk.Label(temps_frame, text="Teplota TUV [°C]:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.dhw_temp = ttk.Entry(temps_frame, width=15)
        self.dhw_temp.grid(row=0, column=3, padx=5, pady=5)
        self.dhw_temp.insert(0, "55")
        
        # Klíma
        climate_frame = ttk.LabelFrame(scrollable_frame, text="🌍 Klimatická lokalita", padding=10)
        climate_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(climate_frame, text="Lokalita:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.climate_zone = ttk.Combobox(climate_frame, values=[
            "Bratislava a okolie",
            "Západné Slovensko",
            "Stredné Slovensko",
            "Východné Slovensko", 
            "Horské oblasti"
        ], width=25, state="readonly")
        self.climate_zone.grid(row=0, column=1, padx=5, pady=5)
        self.climate_zone.set("Bratislava a okolie")
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_results_tab(self):
        """Tab pre výsledky"""
        self.results_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.results_tab, text="📊 Výsledky")
        
        # Výsledkový text
        self.results_text = scrolledtext.ScrolledText(self.results_tab, 
                                                     width=100, height=40,
                                                     font=('Consolas', 10))
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.results_text.insert(tk.END, "🔬 Kliknite na 'VYKONAŤ AUDIT' pre výpočet výsledkov...\n")
        
    def create_report_tab(self):
        """Tab pre report"""
        self.report_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.report_tab, text="📄 Report")
        
        # Report text
        self.report_text = scrolledtext.ScrolledText(self.report_tab,
                                                    width=100, height=40,
                                                    font=('Consolas', 10))
        self.report_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.report_text.insert(tk.END, "📄 Report bude vygenerovaný po dokončení auditu...\n")
        
    def create_bottom_panel(self):
        """Bottom panel s tlačidlami"""
        bottom_frame = tk.Frame(self.root, bg='#ecf0f1', height=100)
        bottom_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=10)
        bottom_frame.pack_propagate(False)
        
        # Progress bar
        progress_frame = tk.Frame(bottom_frame, bg='#ecf0f1')
        progress_frame.pack(fill=tk.X, pady=(5, 10))
        
        tk.Label(progress_frame, text="Priebeh:", bg='#ecf0f1', font=('Arial', 9)).pack(side=tk.LEFT)
        self.progress = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress.pack(fill=tk.X, padx=(10, 0))
        
        # Tlačidlá
        button_frame = tk.Frame(bottom_frame, bg='#ecf0f1')
        button_frame.pack(fill=tk.X, pady=5)
        
        # Vykonať audit - veľké zelené tlačidlo
        self.audit_btn = tk.Button(button_frame, text="🔬 VYKONAŤ AUDIT",
                                  command=self.perform_audit,
                                  bg='#27ae60', fg='white',
                                  font=('Arial', 14, 'bold'),
                                  width=18, height=2,
                                  relief=tk.RAISED, bd=3)
        self.audit_btn.pack(side=tk.LEFT, padx=10)
        
        # Ostatné tlačidlá
        buttons_data = [
            ("💾 ULOŽIŤ", self.save_project, '#3498db'),
            ("📂 NAČÍTAŤ", self.load_project, '#f39c12'),
            ("🏅 CERTIFIKÁT", self.generate_certificate, '#9b59b6'),
            ("📤 EXPORT", self.export_results, '#34495e'),
        ]
        
        for text, command, color in buttons_data:
            btn = tk.Button(button_frame, text=text,
                           command=command,
                           bg=color, fg='white',
                           font=('Arial', 10, 'bold'),
                           width=12, height=2)
            btn.pack(side=tk.LEFT, padx=3)
        
        # Exit tlačidlo vpravo
        exit_btn = tk.Button(button_frame, text="❌ UKONČIŤ",
                            command=self.root.quit,
                            bg='#e74c3c', fg='white',
                            font=('Arial', 10, 'bold'),
                            width=12, height=2)
        exit_btn.pack(side=tk.RIGHT, padx=10)
        
    def create_status_bar(self):
        """Vytvorenie status baru"""
        self.status_frame = tk.Frame(self.root, bg='#34495e', height=25)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        self.status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(self.status_frame, 
                                    text="🟢 Pripravený na audit - Zadajte údaje a kliknite na 'VYKONAŤ AUDIT'",
                                    bg='#34495e', fg='white',
                                    font=('Arial', 10),
                                    anchor=tk.W)
        self.status_label.pack(fill=tk.X, padx=10, pady=2)
        
    def update_status(self, message, color='#2ecc71'):
        """Aktualizácia status baru"""
        self.status_label.config(text=message)
        self.status_frame.config(bg=color)
        self.status_label.config(bg=color)
        self.root.update()
        
    def collect_data(self):
        """Zber dát z GUI"""
        try:
            # Základné údaje
            building_data = {
                'name': self.building_name.get(),
                'address': self.building_address.get(),
                'type': self.building_type.get(),
                'construction_year': int(self.construction_year.get()),
                'floor_area': float(self.floor_area.get()),
                'heated_area': float(self.heated_area.get()),
                'volume': float(self.volume.get()),
                'height': float(self.height.get()),
                'floors': int(self.floors.get())
            }
            
            # Obálka
            envelope_data = {
                'constructions': [
                    {
                        'name': 'Obvodová stena',
                        'type': 'wall',
                        'area': float(self.wall_area.get()),
                        'u_value': float(self.wall_u.get())
                    },
                    {
                        'name': 'Strecha', 
                        'type': 'roof',
                        'area': float(self.roof_area.get()),
                        'u_value': float(self.roof_u.get())
                    },
                    {
                        'name': 'Podlaha',
                        'type': 'floor', 
                        'area': float(self.floor_envelope_area.get()),
                        'u_value': float(self.floor_u.get())
                    },
                    {
                        'name': 'Okná',
                        'type': 'window',
                        'area': float(self.window_area.get()),
                        'u_value': float(self.window_u.get())
                    }
                ]
            }
            
            # Systémy
            systems_data = {
                'heating': {
                    'name': self.heating_type.get(),
                    'efficiency': float(self.heating_efficiency.get()) / 100,
                    'fuel': self.get_fuel_type(self.heating_type.get())
                },
                'dhw': {
                    'name': self.dhw_type.get(),
                    'efficiency': float(self.dhw_efficiency.get()) / 100,
                    'fuel': self.get_fuel_type(self.dhw_type.get())
                },
                'ventilation': {
                    'name': self.ventilation_type.get(),
                    'recovery_efficiency': self.get_recovery_efficiency(self.ventilation_type.get())
                }
            }
            
            # Užívanie
            usage_data = {
                'occupants': int(self.occupants.get()),
                'heating_temp': float(self.heating_temp.get()),
                'dhw_temp': float(self.dhw_temp.get()),
                'climate': self.get_climate_data(self.climate_zone.get())
            }
            
            self.audit_data = {
                'building': building_data,
                'envelope': envelope_data,
                'systems': systems_data,
                'usage': usage_data
            }
            
            return True
            
        except ValueError as e:
            messagebox.showerror("Chyba", f"Neplatné vstupné údaje: {e}")
            return False
        except Exception as e:
            messagebox.showerror("Chyba", f"Chyba pri zbere údajov: {e}")
            return False
    
    def get_fuel_type(self, system_type):
        """Určenie typu paliva"""
        fuel_mapping = {
            'Plynový kotol': 'natural_gas',
            'Elektrické vykurovanie': 'electricity', 
            'Tepelné čerpadlo': 'electricity',
            'Biomasa': 'biomass',
            'Diaľkové vykurovanie': 'district_heating'
        }
        return fuel_mapping.get(system_type, 'natural_gas')
    
    def get_recovery_efficiency(self, vent_type):
        """Určenie účinnosti rekuperácie"""
        if '70%' in vent_type:
            return 0.70
        elif '85%' in vent_type:
            return 0.85
        else:
            return 0.0
    
    def get_climate_data(self, zone):
        """Klimatické údaje"""
        climate_zones = {
            'Bratislava a okolie': {'name': 'Bratislava', 'hdd': 2800, 'avg_temp': 10.5},
            'Západné Slovensko': {'name': 'Západné SK', 'hdd': 3000, 'avg_temp': 9.8},
            'Stredné Slovensko': {'name': 'Stredné SK', 'hdd': 3200, 'avg_temp': 8.5},
            'Východné Slovensko': {'name': 'Východné SK', 'hdd': 3100, 'avg_temp': 9.0},
            'Horské oblasti': {'name': 'Horské oblasti', 'hdd': 3800, 'avg_temp': 6.5}
        }
        return climate_zones.get(zone, climate_zones['Bratislava a okolie'])
    
    def perform_audit(self):
        """Vykonanie energetického auditu"""
        self.update_status("🔄 Zbieram údaje...", '#f39c12')
        
        if not self.collect_data():
            self.update_status("🔴 Chyba pri zbere údajov", '#e74c3c')
            return
            
        self.progress['value'] = 0
        self.update_status("🔬 Spúšťam energetický audit...", '#3498db')
        
        # Výpočet
        try:
            self.progress['value'] = 20
            self.update_status("📈 Počítam tepelné straty obálky...", '#3498db')
            
            self.results = self.calculate_energy_performance()
            
            self.progress['value'] = 80
            self.update_status("📄 Generujem výsledky a report...", '#3498db')
            
            self.display_results()
            self.generate_report()
            
            self.progress['value'] = 100
            self.update_status("✅ Energetický audit úspešne dokončený!", '#27ae60')
            
            messagebox.showinfo("Úspéch", "✅ Energetický audit dokončený!")
            
        except Exception as e:
            self.update_status(f"🔴 Chyba pri audité: {str(e)[:50]}...", '#e74c3c')
            messagebox.showerror("Chyba", f"Chyba pri výpočte: {e}")
        finally:
            self.progress['value'] = 0
    
    def calculate_energy_performance(self):
        """Výpočet energetických vlastností (rovnaký ako v konzole)"""
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
        if systems_data['ventilation']['name'] == 'Mechanické vetranie':
            air_change_rate = 0.8
        elif 'Rekuperácia' in systems_data['ventilation']['name']:
            air_change_rate = 0.8 * (1 - systems_data['ventilation']['recovery_efficiency'])
        
        ventilation_loss = building_data['volume'] * air_change_rate * 0.34 * hdd * 24 / 1000
        
        total_heating_need = heating_need + ventilation_loss
        
        # Solárne a vnútorné zisky
        window_area = next((c['area'] for c in envelope_data['constructions'] if c['type'] == 'window'), 20)
        solar_gains = window_area * 150  # kWh/rok
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
        
        # Výpočet spotreby energie
        heating_energy = net_heating_need / systems_data['heating']['efficiency']
        dhw_need = usage_data['occupants'] * 25 * 365 / 1000  # kWh/rok
        dhw_energy = dhw_need / systems_data['dhw']['efficiency']
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
        
        return results
    
    def display_results(self):
        """Zobrazenie výsledkov"""
        self.results_text.delete(1.0, tk.END)
        
        building = self.audit_data['building']
        results = self.results
        
        output = f"""
{'='*80}
📋 SÚHRNNÝ ENERGETICKÝ AUDIT
{'='*80}
🏢 Budova: {building['name']}
📍 Adresa: {building['address']}
🏗️  Typ: {building['type']}
📐 Podlahová plocha: {building['floor_area']:.0f} m²
📅 Rok výstavby: {building['construction_year']}

⚡ ENERGETICKÁ BILANCIA:
├─ Potreba tepla na vykurovanie: {results['heating_analysis']['net_heating_need']:.0f} kWh/rok
├─ Spotreba na vykurovanie: {results['energy_consumption']['heating_energy']:.0f} kWh/rok
├─ Spotreba na TUV: {results['energy_consumption']['dhw_energy']:.0f} kWh/rok
├─ Elektrická energia: {results['energy_consumption']['electricity']:.0f} kWh/rok
└─ Celková spotreba: {results['energy_consumption']['total_energy']:.0f} kWh/rok

🎯 ENERGETICKÉ HODNOTENIE:
├─ Energetická trieda: {results['energy_class']['class']}
├─ Primárna energia: {results['primary_energy']['specific']:.1f} kWh/m²rok
├─ CO2 emisie: {results['co2_emissions']['specific']:.1f} kg CO2/m²rok
└─ Špecifická spotreba: {results['energy_consumption']['specific_total']:.1f} kWh/m²rok

🏠 OBÁLKA BUDOVY:
"""
        
        for detail in results['envelope_analysis']['details']:
            output += f"├─ {detail['name']}: {detail['area']:.0f} m², U={detail['u_value']:.2f} W/m²K\n"
        
        output += f"└─ Celkový súčiniteľ prestupu: {results['envelope_analysis']['total_heat_loss_coefficient']:.1f} W/K\n"
        
        # Odporúčania
        recommendations = self.generate_recommendations()
        if recommendations:
            output += "\n💡 HLAVNÉ ODPORÚČANIA:\n"
            for i, rec in enumerate(recommendations[:3], 1):
                output += f"{i}. {rec['title']} - {rec['estimated_savings']} úspory\n"
        
        self.results_text.insert(tk.END, output)
        
        # Prepnúť na tab s výsledkami
        self.notebook.select(self.results_tab)
    
    def generate_recommendations(self):
        """Generovanie odporúčaní"""
        recommendations = []
        results = self.results
        
        # Hodnotenie obálky
        envelope = results['envelope_analysis']['details']
        
        for element in envelope:
            if element['name'] == 'Obvodová stena' and element['u_value'] > 0.30:
                recommendations.append({
                    'category': 'Tepelná izolácia',
                    'title': 'Zateplenie obvodových stien',
                    'description': f'Aktuálna U-hodnota {element["u_value"]:.2f} W/m²K je vysoká.',
                    'priority': 'Vysoká',
                    'estimated_savings': '25-35%'
                })
                
            if element['name'] == 'Okná' and element['u_value'] > 2.0:
                recommendations.append({
                    'category': 'Výplne otvorov',
                    'title': 'Výmena okien',
                    'description': f'Aktuálna U-hodnota okien {element["u_value"]:.1f} W/m²K.',
                    'priority': 'Stredná',
                    'estimated_savings': '15-20%'
                })
        
        # Hodnotenie systémov
        if self.audit_data['systems']['heating']['efficiency'] < 0.85:
            recommendations.append({
                'category': 'Vykurovací systém',
                'title': 'Modernizácia vykurovacieho systému',
                'description': 'Nízka účinnosť vykurovacieho systému.',
                'priority': 'Vysoká',
                'estimated_savings': '20-30%'
            })
            
        if 'Rekuperácia' not in self.audit_data['systems']['ventilation']['name']:
            recommendations.append({
                'category': 'Vetranie',
                'title': 'Inštalácia rekuperačnej jednotky',
                'description': 'Rekuperácia tepla z odvádzaného vzduchu.',
                'priority': 'Stredná',
                'estimated_savings': '10-15%'
            })
            
        return recommendations
    
    def generate_report(self):
        """Generovanie reportu"""
        self.report_text.delete(1.0, tk.END)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        building = self.audit_data['building']
        results = self.results
        
        report = f"""
{'='*80}
📄 ENERGETICKÝ AUDIT BUDOVY
{'='*80}
Energetické hodnotenie budovy {building['name']}

📋 ZÁKLADNÉ ÚDAJE:
• Dátum auditu: {timestamp}
• Audítor: Ing. Energetický Audítor
• Štandard: STN EN 16247-1, STN EN ISO 52016

🏢 BUDOVA:
• Názov: {building['name']}
• Adresa: {building['address']}
• Typ: {building['type']}
• Rok výstavby: {building['construction_year']}
• Podlahová plocha: {building['floor_area']:.0f} m²

⚡ ENERGETICKÉ VÝSLEDKY:
• Energetická trieda: {results['energy_class']['class']}
• Primárna energia: {results['primary_energy']['specific']:.1f} kWh/m²rok
• CO2 emisie: {results['co2_emissions']['specific']:.1f} kg CO2/m²rok
• Celková spotreba: {results['energy_consumption']['total_energy']:.0f} kWh/rok

🏠 OBÁLKA BUDOVY:
"""
        
        for detail in results['envelope_analysis']['details']:
            report += f"• {detail['name']}: {detail['area']:.0f} m², U={detail['u_value']:.2f} W/m²K\n"
        
        # Odporúčania
        recommendations = self.generate_recommendations()
        if recommendations:
            report += "\n💡 ODPORÚČANIA:\n"
            for i, rec in enumerate(recommendations[:5], 1):
                report += f"{i}. {rec['title']}\n"
                report += f"   Kategória: {rec['category']}\n"
                report += f"   Priorita: {rec['priority']}\n"
                report += f"   Očakávané úspory: {rec['estimated_savings']}\n\n"
        
        report += f"\n📋 CERTIFIKÁCIA:\n"
        report += f"• Energetická trieda: {results['energy_class']['class']}\n"
        report += f"• Primárna energia: {results['energy_class']['specific_primary_energy']:.1f} kWh/m²rok\n"
        report += f"• CO2 emisie: {results['co2_emissions']['specific']:.1f} kg CO2/m²rok\n"
        
        self.report_text.insert(tk.END, report)
        
        # Prepnúť na tab s reportom
        self.notebook.select(self.report_tab)
    
    def save_project(self):
        """Uloženie projektu"""
        if not self.audit_data:
            messagebox.showwarning("Upozornenie", "Nie je čo uložiť. Najprv zadajte údaje.")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON súbory", "*.json"), ("Všetky súbory", "*.*")],
            title="Uložiť projekt"
        )
        
        if filename:
            try:
                project_data = {
                    'audit_data': self.audit_data,
                    'results': self.results,
                    'timestamp': datetime.now().isoformat()
                }
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(project_data, f, ensure_ascii=False, indent=2, default=str)
                
                messagebox.showinfo("Úspech", f"Projekt uložený: {filename}")
                
            except Exception as e:
                messagebox.showerror("Chyba", f"Chyba pri ukladaní: {e}")
    
    def load_project(self):
        """Načítanie projektu"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON súbory", "*.json"), ("Všetky súbory", "*.*")],
            title="Načítať projekt"
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    project_data = json.load(f)
                
                self.audit_data = project_data.get('audit_data', {})
                self.results = project_data.get('results', {})
                
                # Načítanie dát do GUI
                self.load_data_to_gui()
                
                if self.results:
                    self.display_results()
                    self.generate_report()
                
                messagebox.showinfo("Úspech", f"Projekt načítaný: {filename}")
                
            except Exception as e:
                messagebox.showerror("Chyba", f"Chyba pri načítaní: {e}")
    
    def load_data_to_gui(self):
        """Načítanie dát do GUI formulárov"""
        if not self.audit_data:
            return
            
        try:
            building = self.audit_data.get('building', {})
            
            # Základné údaje
            self.building_name.delete(0, tk.END)
            self.building_name.insert(0, building.get('name', ''))
            
            self.building_address.delete(0, tk.END)
            self.building_address.insert(0, building.get('address', ''))
            
            self.building_type.set(building.get('type', 'Rodinný dom'))
            
            self.construction_year.delete(0, tk.END)
            self.construction_year.insert(0, str(building.get('construction_year', 2000)))
            
            # Geometria
            self.floor_area.delete(0, tk.END)
            self.floor_area.insert(0, str(building.get('floor_area', 120)))
            
            self.heated_area.delete(0, tk.END)
            self.heated_area.insert(0, str(building.get('heated_area', 115)))
            
            # ... ostatné polia podľa potreby
            
        except Exception as e:
            messagebox.showwarning("Upozornenie", f"Nie všetky údaje sa podarilo načítať: {e}")
    
    def generate_certificate(self):
        """Generovanie certifikátu"""
        if not self.results:
            messagebox.showwarning("Upozornenie", "Najprv vykonajte audit.")
            return
            
        try:
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
            
            certificate = {
                'certificate_type': 'Energetický certifikát budovy',
                'validity': 'Validácia podľa STN EN 16247',
                'energy_performance': {
                    'class': certificate_data['energy_class'],
                    'primary_energy': certificate_data['primary_energy'],
                    'co2_emissions': certificate_data['co2_emissions']
                }
            }
            
            filename = f"certifikat_{building['name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    'certificate_data': certificate_data,
                    'certificate': certificate
                }, f, ensure_ascii=False, indent=2, default=str)
            
            messagebox.showinfo("Úspech", 
                               f"✅ Energetický certifikát vygenerovaný!\n\n"
                               f"📁 Súbor: {filename}\n"
                               f"📋 Číslo: {certificate_data['certificate_number']}\n"
                               f"🏅 Trieda: {certificate_data['energy_class']}\n"
                               f"⚡ Primárna energia: {certificate_data['primary_energy']:.1f} kWh/m²rok")
        
        except Exception as e:
            messagebox.showerror("Chyba", f"Chyba pri generovaní certifikátu: {e}")
    
    def export_results(self):
        """Export výsledkov"""
        if not self.results:
            messagebox.showwarning("Upozornenie", "Najprv vykonajte audit.")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[
                ("JSON súbory", "*.json"),
                ("Text súbory", "*.txt"),
                ("Všetky súbory", "*.*")
            ],
            title="Export výsledkov"
        )
        
        if filename:
            try:
                if filename.endswith('.txt'):
                    # Export do textového súboru
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(self.results_text.get(1.0, tk.END))
                else:
                    # Export do JSON
                    export_data = {
                        'audit_data': self.audit_data,
                        'results': self.results,
                        'recommendations': self.generate_recommendations(),
                        'export_timestamp': datetime.now().isoformat()
                    }
                    
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(export_data, f, ensure_ascii=False, indent=2, default=str)
                
                messagebox.showinfo("Úspech", f"Výsledky exportované: {filename}")
                
            except Exception as e:
                messagebox.showerror("Chyba", f"Chyba pri exporte: {e}")

def main():
    """Hlavná funkcia"""
    root = tk.Tk()
    app = EnergyAuditGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()