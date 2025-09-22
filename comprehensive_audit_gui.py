#!/usr/bin/env python3
"""
KOMPLETNÁ ENERGY AUDIT GUI APLIKÁCIA
S rozšíreným zberom údajov pre profesionálny energetický audit
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
from datetime import datetime
import json

class ComprehensiveEnergyAuditGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🏢 Kompletný Energetický Audit Systém")
        self.root.geometry("1200x800")
        self.root.configure(bg='white')
        
        # Dáta
        self.audit_data = {}
        self.results = {}
        
        self.create_gui()
        
    def create_gui(self):
        """Vytvorenie kompletného GUI s tabmi"""
        
        # HLAVIČKA
        header = tk.Frame(self.root, bg='#2c3e50', height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="🏢 KOMPLETNÝ ENERGETICKÝ AUDIT SYSTÉM", 
                font=('Arial', 16, 'bold'), fg='white', bg='#2c3e50').pack(pady=15)
        
        # NOTEBOOK S TABMI
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # TABY
        self.create_basic_info_tab()
        self.create_building_envelope_tab()
        self.create_heating_systems_tab()
        self.create_cooling_ventilation_tab()
        self.create_lighting_equipment_tab()
        self.create_water_heating_tab()
        self.create_usage_occupancy_tab()
        self.create_results_tab()
        
        # SPODNÝ PANEL
        self.create_bottom_panel()
        
    def create_basic_info_tab(self):
        """Tab 1: Základné informácie o budove"""
        tab1 = ttk.Frame(self.notebook)
        self.notebook.add(tab1, text="📋 Základné údaje")
        
        canvas = tk.Canvas(tab1)
        scrollbar = ttk.Scrollbar(tab1, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # IDENTIFIKAČNÉ ÚDAJE
        id_frame = tk.LabelFrame(scrollable_frame, text="🏢 Identifikácia budovy", font=('Arial', 11, 'bold'))
        id_frame.pack(fill=tk.X, padx=10, pady=5)
        
        row = 0
        tk.Label(id_frame, text="Názov budovy:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=3)
        self.building_name = tk.Entry(id_frame, width=40)
        self.building_name.grid(row=row, column=1, padx=5, pady=3)
        
        row += 1
        tk.Label(id_frame, text="Adresa:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=3)
        self.address = tk.Entry(id_frame, width=40)
        self.address.grid(row=row, column=1, padx=5, pady=3)
        
        row += 1
        tk.Label(id_frame, text="Katastrálne územie:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=3)
        self.cadastral = tk.Entry(id_frame, width=40)
        self.cadastral.grid(row=row, column=1, padx=5, pady=3)
        
        row += 1
        tk.Label(id_frame, text="Vlastník/Správca:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=3)
        self.owner = tk.Entry(id_frame, width=40)
        self.owner.grid(row=row, column=1, padx=5, pady=3)
        
        # TECHNICKÉ PARAMETRE
        tech_frame = tk.LabelFrame(scrollable_frame, text="📐 Technické parametre", font=('Arial', 11, 'bold'))
        tech_frame.pack(fill=tk.X, padx=10, pady=5)
        
        row = 0
        tk.Label(tech_frame, text="Rok výstavby:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=3)
        self.construction_year = tk.Entry(tech_frame, width=20)
        self.construction_year.grid(row=row, column=1, padx=5, pady=3)
        
        tk.Label(tech_frame, text="Rok rekonštrukcie:").grid(row=row, column=2, sticky=tk.W, padx=5, pady=3)
        self.renovation_year = tk.Entry(tech_frame, width=20)
        self.renovation_year.grid(row=row, column=3, padx=5, pady=3)
        
        row += 1
        tk.Label(tech_frame, text="Počet podlaží:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=3)
        self.floors_count = tk.Entry(tech_frame, width=20)
        self.floors_count.grid(row=row, column=1, padx=5, pady=3)
        
        tk.Label(tech_frame, text="Výška budovy [m]:").grid(row=row, column=2, sticky=tk.W, padx=5, pady=3)
        self.building_height = tk.Entry(tech_frame, width=20)
        self.building_height.grid(row=row, column=3, padx=5, pady=3)
        
        row += 1
        tk.Label(tech_frame, text="Podlahová plocha [m²]:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=3)
        self.floor_area = tk.Entry(tech_frame, width=20)
        self.floor_area.grid(row=row, column=1, padx=5, pady=3)
        
        tk.Label(tech_frame, text="Obostavaný priestor [m³]:").grid(row=row, column=2, sticky=tk.W, padx=5, pady=3)
        self.volume = tk.Entry(tech_frame, width=20)
        self.volume.grid(row=row, column=3, padx=5, pady=3)
        
        row += 1
        tk.Label(tech_frame, text="Typ budovy:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=3)
        self.building_type = ttk.Combobox(tech_frame, width=18, values=[
            "Rodinný dom", "Bytový dom", "Administratívna budova", "Škola", 
            "Nemocnica", "Hotel", "Obchod", "Priemyselná budova", "Ostatné"
        ])
        self.building_type.grid(row=row, column=1, padx=5, pady=3)
        
        tk.Label(tech_frame, text="Konštrukčný systém:").grid(row=row, column=2, sticky=tk.W, padx=5, pady=3)
        self.construction_system = ttk.Combobox(tech_frame, width=18, values=[
            "Murovaný", "Montovaný betón", "Skelet", "Drevostavba", "Ostatné"
        ])
        self.construction_system.grid(row=row, column=3, padx=5, pady=3)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_building_envelope_tab(self):
        """Tab 2: Obálka budovy"""
        tab2 = ttk.Frame(self.notebook)
        self.notebook.add(tab2, text="🏠 Obálka budovy")
        
        canvas = tk.Canvas(tab2)
        scrollbar = ttk.Scrollbar(tab2, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # VONKAJŠIE STENY
        walls_frame = tk.LabelFrame(scrollable_frame, text="🧱 Vonkajšie steny", font=('Arial', 11, 'bold'))
        walls_frame.pack(fill=tk.X, padx=10, pady=5)
        
        row = 0
        tk.Label(walls_frame, text="Celková plocha stien [m²]:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=3)
        self.wall_area = tk.Entry(walls_frame, width=20)
        self.wall_area.grid(row=row, column=1, padx=5, pady=3)
        
        tk.Label(walls_frame, text="U-hodnota stien [W/m²K]:").grid(row=row, column=2, sticky=tk.W, padx=5, pady=3)
        self.wall_u = tk.Entry(walls_frame, width=20)
        self.wall_u.grid(row=row, column=3, padx=5, pady=3)
        
        row += 1
        tk.Label(walls_frame, text="Typ izolácie:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=3)
        self.wall_insulation = ttk.Combobox(walls_frame, width=18, values=[
            "Bez izolácie", "Kontaktný zateplovací systém", "Vnútorná izolácia", 
            "Dutinová izolácia", "Iná"
        ])
        self.wall_insulation.grid(row=row, column=1, padx=5, pady=3)
        
        tk.Label(walls_frame, text="Hrúbka izolácie [cm]:").grid(row=row, column=2, sticky=tk.W, padx=5, pady=3)
        self.wall_insulation_thickness = tk.Entry(walls_frame, width=20)
        self.wall_insulation_thickness.grid(row=row, column=3, padx=5, pady=3)
        
        # OKNÁ
        windows_frame = tk.LabelFrame(scrollable_frame, text="🪟 Okná a dvere", font=('Arial', 11, 'bold'))
        windows_frame.pack(fill=tk.X, padx=10, pady=5)
        
        row = 0
        tk.Label(windows_frame, text="Celková plocha okien [m²]:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=3)
        self.window_area = tk.Entry(windows_frame, width=20)
        self.window_area.grid(row=row, column=1, padx=5, pady=3)
        
        tk.Label(windows_frame, text="U-hodnota okien [W/m²K]:").grid(row=row, column=2, sticky=tk.W, padx=5, pady=3)
        self.window_u = tk.Entry(windows_frame, width=20)
        self.window_u.grid(row=row, column=3, padx=5, pady=3)
        
        row += 1
        tk.Label(windows_frame, text="Typ okien:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=3)
        self.window_type = ttk.Combobox(windows_frame, width=18, values=[
            "Jednoduché sklo", "Dvojsklo", "Trojsklo", "Nízkoenergetické", "Pasívne"
        ])
        self.window_type.grid(row=row, column=1, padx=5, pady=3)
        
        tk.Label(windows_frame, text="Typ rámu:").grid(row=row, column=2, sticky=tk.W, padx=5, pady=3)
        self.window_frame = ttk.Combobox(windows_frame, width=18, values=[
            "Drevený", "Plastový", "Hliníkový", "Hliník s tepelným mostom"
        ])
        self.window_frame.grid(row=row, column=3, padx=5, pady=3)
        
        # STRECHA
        roof_frame = tk.LabelFrame(scrollable_frame, text="🏠 Strecha", font=('Arial', 11, 'bold'))
        roof_frame.pack(fill=tk.X, padx=10, pady=5)
        
        row = 0
        tk.Label(roof_frame, text="Plocha strechy [m²]:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=3)
        self.roof_area = tk.Entry(roof_frame, width=20)
        self.roof_area.grid(row=row, column=1, padx=5, pady=3)
        
        tk.Label(roof_frame, text="U-hodnota strechy [W/m²K]:").grid(row=row, column=2, sticky=tk.W, padx=5, pady=3)
        self.roof_u = tk.Entry(roof_frame, width=20)
        self.roof_u.grid(row=row, column=3, padx=5, pady=3)
        
        row += 1
        tk.Label(roof_frame, text="Typ strechy:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=3)
        self.roof_type = ttk.Combobox(roof_frame, width=18, values=[
            "Plochá strecha", "Šikmá strecha", "Sedlová strecha", "Valbová strecha"
        ])
        self.roof_type.grid(row=row, column=1, padx=5, pady=3)
        
        tk.Label(roof_frame, text="Hrúbka izolácie [cm]:").grid(row=row, column=2, sticky=tk.W, padx=5, pady=3)
        self.roof_insulation = tk.Entry(roof_frame, width=20)
        self.roof_insulation.grid(row=row, column=3, padx=5, pady=3)
        
        # PODLAHA
        floor_frame = tk.LabelFrame(scrollable_frame, text="🔳 Podlaha", font=('Arial', 11, 'bold'))
        floor_frame.pack(fill=tk.X, padx=10, pady=5)
        
        row = 0
        tk.Label(floor_frame, text="Plocha podlahy [m²]:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=3)
        self.floor_area_envelope = tk.Entry(floor_frame, width=20)
        self.floor_area_envelope.grid(row=row, column=1, padx=5, pady=3)
        
        tk.Label(floor_frame, text="U-hodnota podlahy [W/m²K]:").grid(row=row, column=2, sticky=tk.W, padx=5, pady=3)
        self.floor_u = tk.Entry(floor_frame, width=20)
        self.floor_u.grid(row=row, column=3, padx=5, pady=3)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_heating_systems_tab(self):
        """Tab 3: Vykurovacie systémy"""
        tab3 = ttk.Frame(self.notebook)
        self.notebook.add(tab3, text="🔥 Vykurovanie")
        
        canvas = tk.Canvas(tab3)
        scrollbar = ttk.Scrollbar(tab3, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # ZDROJ TEPLA
        source_frame = tk.LabelFrame(scrollable_frame, text="🔥 Zdroj tepla", font=('Arial', 11, 'bold'))
        source_frame.pack(fill=tk.X, padx=10, pady=5)
        
        row = 0
        tk.Label(source_frame, text="Typ vykurovania:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=3)
        self.heating_type = ttk.Combobox(source_frame, width=25, values=[
            "Plynový kotol kondenzačný", "Plynový kotol klasický", "Elektrický kotol",
            "Tepelné čerpadlo vzduch-voda", "Tepelné čerpadlo zem-voda", "Tepelné čerpadlo voda-voda",
            "Biomasa (pelety)", "Biomasa (drevo)", "Solárne kolektory", "Kombinovaný systém"
        ])
        self.heating_type.grid(row=row, column=1, columnspan=3, padx=5, pady=3)
        
        row += 1
        tk.Label(source_frame, text="Výkon zdroja [kW]:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=3)
        self.heating_power = tk.Entry(source_frame, width=20)
        self.heating_power.grid(row=row, column=1, padx=5, pady=3)
        
        tk.Label(source_frame, text="Účinnosť [%]:").grid(row=row, column=2, sticky=tk.W, padx=5, pady=3)
        self.heating_efficiency = tk.Entry(source_frame, width=20)
        self.heating_efficiency.grid(row=row, column=3, padx=5, pady=3)
        
        row += 1
        tk.Label(source_frame, text="Rok inštalácie:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=3)
        self.heating_installation = tk.Entry(source_frame, width=20)
        self.heating_installation.grid(row=row, column=1, padx=5, pady=3)
        
        tk.Label(source_frame, text="Palivo:").grid(row=row, column=2, sticky=tk.W, padx=5, pady=3)
        self.fuel_type = ttk.Combobox(source_frame, width=18, values=[
            "Zemný plyn", "Elektrina", "LPG", "Pelety", "Drevo", "Slnečná energia"
        ])
        self.fuel_type.grid(row=row, column=3, padx=5, pady=3)
        
        # DISTRIBÚCIA TEPLA
        distribution_frame = tk.LabelFrame(scrollable_frame, text="🌡️ Distribúcia tepla", font=('Arial', 11, 'bold'))
        distribution_frame.pack(fill=tk.X, padx=10, pady=5)
        
        row = 0
        tk.Label(distribution_frame, text="Typ distribúcie:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=3)
        self.distribution_type = ttk.Combobox(distribution_frame, width=25, values=[
            "Podlahové kúrenie", "Radiátory", "Konvektory", "Teplovzdušné kúrenie"
        ])
        self.distribution_type.grid(row=row, column=1, columnspan=3, padx=5, pady=3)
        
        row += 1
        tk.Label(distribution_frame, text="Izolácia potrubí [%]:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=3)
        self.pipe_insulation = tk.Entry(distribution_frame, width=20)
        self.pipe_insulation.grid(row=row, column=1, padx=5, pady=3)
        
        tk.Label(distribution_frame, text="Regulácia:").grid(row=row, column=2, sticky=tk.W, padx=5, pady=3)
        self.heating_control = ttk.Combobox(distribution_frame, width=18, values=[
            "Bez regulácie", "Termostatické hlavice", "Ekvitermická regulácia", "Inteligentný systém"
        ])
        self.heating_control.grid(row=row, column=3, padx=5, pady=3)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_cooling_ventilation_tab(self):
        """Tab 4: Chladenie a vetranie"""
        tab4 = ttk.Frame(self.notebook)
        self.notebook.add(tab4, text="❄️ Chladenie/Vetranie")
        
        canvas = tk.Canvas(tab4)
        scrollbar = ttk.Scrollbar(tab4, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # CHLADENIE
        cooling_frame = tk.LabelFrame(scrollable_frame, text="❄️ Chladenie", font=('Arial', 11, 'bold'))
        cooling_frame.pack(fill=tk.X, padx=10, pady=5)
        
        row = 0
        tk.Label(cooling_frame, text="Typ chladenia:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=3)
        self.cooling_type = ttk.Combobox(cooling_frame, width=25, values=[
            "Bez chladenia", "Split systém", "VRV/VRF systém", "Centrálna klimatizácia", "Pasívne chladenie"
        ])
        self.cooling_type.grid(row=row, column=1, columnspan=3, padx=5, pady=3)
        
        row += 1
        tk.Label(cooling_frame, text="Chladiaci výkon [kW]:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=3)
        self.cooling_power = tk.Entry(cooling_frame, width=20)
        self.cooling_power.grid(row=row, column=1, padx=5, pady=3)
        
        tk.Label(cooling_frame, text="SEER [-]:").grid(row=row, column=2, sticky=tk.W, padx=5, pady=3)
        self.cooling_seer = tk.Entry(cooling_frame, width=20)
        self.cooling_seer.grid(row=row, column=3, padx=5, pady=3)
        
        # VETRANIE
        ventilation_frame = tk.LabelFrame(scrollable_frame, text="💨 Vetranie", font=('Arial', 11, 'bold'))
        ventilation_frame.pack(fill=tk.X, padx=10, pady=5)
        
        row = 0
        tk.Label(ventilation_frame, text="Typ vetrania:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=3)
        self.ventilation_type = ttk.Combobox(ventilation_frame, width=25, values=[
            "Prirodzené vetranie", "Mechanické odvetranie", "Mechanické privetranie", 
            "Vyvážené vetranie", "Vetranie so spätným získavaním tepla"
        ])
        self.ventilation_type.grid(row=row, column=1, columnspan=3, padx=5, pady=3)
        
        row += 1
        tk.Label(ventilation_frame, text="Prietok vzduchu [m³/h]:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=3)
        self.air_flow = tk.Entry(ventilation_frame, width=20)
        self.air_flow.grid(row=row, column=1, padx=5, pady=3)
        
        tk.Label(ventilation_frame, text="Účinnosť ZZT [%]:").grid(row=row, column=2, sticky=tk.W, padx=5, pady=3)
        self.heat_recovery = tk.Entry(ventilation_frame, width=20)
        self.heat_recovery.grid(row=row, column=3, padx=5, pady=3)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_lighting_equipment_tab(self):
        """Tab 5: Osvetlenie a zariadenia"""
        tab5 = ttk.Frame(self.notebook)
        self.notebook.add(tab5, text="💡 Osvetlenie/Zariadenia")
        
        canvas = tk.Canvas(tab5)
        scrollbar = ttk.Scrollbar(tab5, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # OSVETLENIE
        lighting_frame = tk.LabelFrame(scrollable_frame, text="💡 Osvetlenie", font=('Arial', 11, 'bold'))
        lighting_frame.pack(fill=tk.X, padx=10, pady=5)
        
        row = 0
        tk.Label(lighting_frame, text="Typ svietidiel:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=3)
        self.lighting_type = ttk.Combobox(lighting_frame, width=25, values=[
            "LED", "Úsporné žiarovky", "Halogénové", "Klasické žiarovky", "Zmiešané"
        ])
        self.lighting_type.grid(row=row, column=1, columnspan=3, padx=5, pady=3)
        
        row += 1
        tk.Label(lighting_frame, text="Inštal. výkon osvet. [W]:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=3)
        self.lighting_power = tk.Entry(lighting_frame, width=20)
        self.lighting_power.grid(row=row, column=1, padx=5, pady=3)
        
        tk.Label(lighting_frame, text="Regulácia osvetlenia:").grid(row=row, column=2, sticky=tk.W, padx=5, pady=3)
        self.lighting_control = ttk.Combobox(lighting_frame, width=18, values=[
            "Manuálne", "Časové spínače", "Senzory pohybu", "Denné svetlo", "Inteligentný systém"
        ])
        self.lighting_control.grid(row=row, column=3, padx=5, pady=3)
        
        # ELEKTRICKÉ ZARIADENIA
        appliances_frame = tk.LabelFrame(scrollable_frame, text="⚡ Elektrické zariadenia", font=('Arial', 11, 'bold'))
        appliances_frame.pack(fill=tk.X, padx=10, pady=5)
        
        row = 0
        tk.Label(appliances_frame, text="IT zariadenia [W]:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=3)
        self.it_equipment = tk.Entry(appliances_frame, width=20)
        self.it_equipment.grid(row=row, column=1, padx=5, pady=3)
        
        tk.Label(appliances_frame, text="Kuchynské spotrebiče [W]:").grid(row=row, column=2, sticky=tk.W, padx=5, pady=3)
        self.kitchen_appliances = tk.Entry(appliances_frame, width=20)
        self.kitchen_appliances.grid(row=row, column=3, padx=5, pady=3)
        
        row += 1
        tk.Label(appliances_frame, text="Ostatné zariadenia [W]:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=3)
        self.other_appliances = tk.Entry(appliances_frame, width=20)
        self.other_appliances.grid(row=row, column=1, padx=5, pady=3)
        
        tk.Label(appliances_frame, text="Energie štítok:").grid(row=row, column=2, sticky=tk.W, padx=5, pady=3)
        self.energy_label = ttk.Combobox(appliances_frame, width=18, values=[
            "A+++", "A++", "A+", "A", "B", "C", "D", "E", "F", "G"
        ])
        self.energy_label.grid(row=row, column=3, padx=5, pady=3)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_water_heating_tab(self):
        """Tab 6: Ohrev teplej vody"""
        tab6 = ttk.Frame(self.notebook)
        self.notebook.add(tab6, text="🚿 Teplá voda")
        
        canvas = tk.Canvas(tab6)
        scrollbar = ttk.Scrollbar(tab6, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # OHREV TEPLEJ VODY
        dhw_frame = tk.LabelFrame(scrollable_frame, text="🚿 Systém ohrevu teplej vody", font=('Arial', 11, 'bold'))
        dhw_frame.pack(fill=tk.X, padx=10, pady=5)
        
        row = 0
        tk.Label(dhw_frame, text="Typ ohrevu:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=3)
        self.dhw_type = ttk.Combobox(dhw_frame, width=25, values=[
            "Elektrický bojler", "Plynový bojler", "Kombinovaný kotol", 
            "Solárne kolektory", "Tepelné čerpadlo", "Centrálny ohrev"
        ])
        self.dhw_type.grid(row=row, column=1, columnspan=3, padx=5, pady=3)
        
        row += 1
        tk.Label(dhw_frame, text="Objem zásobníka [l]:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=3)
        self.dhw_volume = tk.Entry(dhw_frame, width=20)
        self.dhw_volume.grid(row=row, column=1, padx=5, pady=3)
        
        tk.Label(dhw_frame, text="Účinnosť ohrevu [%]:").grid(row=row, column=2, sticky=tk.W, padx=5, pady=3)
        self.dhw_efficiency = tk.Entry(dhw_frame, width=20)
        self.dhw_efficiency.grid(row=row, column=3, padx=5, pady=3)
        
        row += 1
        tk.Label(dhw_frame, text="Izolácia zásobníka:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=3)
        self.dhw_insulation = ttk.Combobox(dhw_frame, width=18, values=[
            "Bez izolácie", "Štandardná", "Vylepšená", "Vysoká"
        ])
        self.dhw_insulation.grid(row=row, column=1, padx=5, pady=3)
        
        tk.Label(dhw_frame, text="Cirkulácia:").grid(row=row, column=2, sticky=tk.W, padx=5, pady=3)
        self.dhw_circulation = ttk.Combobox(dhw_frame, width=18, values=[
            "Bez cirkulácie", "Neprerušovaná", "Časová", "Termostatická"
        ])
        self.dhw_circulation.grid(row=row, column=3, padx=5, pady=3)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_usage_occupancy_tab(self):
        """Tab 7: Užívanie a obsadenosť"""
        tab7 = ttk.Frame(self.notebook)
        self.notebook.add(tab7, text="👥 Užívanie")
        
        canvas = tk.Canvas(tab7)
        scrollbar = ttk.Scrollbar(tab7, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # OBSADENOSŤ
        occupancy_frame = tk.LabelFrame(scrollable_frame, text="👥 Obsadenosť budovy", font=('Arial', 11, 'bold'))
        occupancy_frame.pack(fill=tk.X, padx=10, pady=5)
        
        row = 0
        tk.Label(occupancy_frame, text="Počet obyvateľov/užívateľov:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=3)
        self.occupants = tk.Entry(occupancy_frame, width=20)
        self.occupants.grid(row=row, column=1, padx=5, pady=3)
        
        tk.Label(occupancy_frame, text="Prevádzkové hodiny/deň:").grid(row=row, column=2, sticky=tk.W, padx=5, pady=3)
        self.operating_hours = tk.Entry(occupancy_frame, width=20)
        self.operating_hours.grid(row=row, column=3, padx=5, pady=3)
        
        row += 1
        tk.Label(occupancy_frame, text="Prevádzkové dni/rok:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=3)
        self.operating_days = tk.Entry(occupancy_frame, width=20)
        self.operating_days.grid(row=row, column=1, padx=5, pady=3)
        
        tk.Label(occupancy_frame, text="Vnút. teplota zima [°C]:").grid(row=row, column=2, sticky=tk.W, padx=5, pady=3)
        self.winter_temperature = tk.Entry(occupancy_frame, width=20)
        self.winter_temperature.grid(row=row, column=3, padx=5, pady=3)
        
        row += 1
        tk.Label(occupancy_frame, text="Vnút. teplota leto [°C]:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=3)
        self.summer_temperature = tk.Entry(occupancy_frame, width=20)
        self.summer_temperature.grid(row=row, column=1, padx=5, pady=3)
        
        # SPOTREBA
        consumption_frame = tk.LabelFrame(scrollable_frame, text="📊 Aktuálna spotreba", font=('Arial', 11, 'bold'))
        consumption_frame.pack(fill=tk.X, padx=10, pady=5)
        
        row = 0
        tk.Label(consumption_frame, text="Ročná spotreba plynu [m³]:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=3)
        self.gas_consumption = tk.Entry(consumption_frame, width=20)
        self.gas_consumption.grid(row=row, column=1, padx=5, pady=3)
        
        tk.Label(consumption_frame, text="Ročná spotreba elektriny [kWh]:").grid(row=row, column=2, sticky=tk.W, padx=5, pady=3)
        self.electricity_consumption = tk.Entry(consumption_frame, width=20)
        self.electricity_consumption.grid(row=row, column=3, padx=5, pady=3)
        
        row += 1
        tk.Label(consumption_frame, text="Cena plynu [€/m³]:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=3)
        self.gas_price = tk.Entry(consumption_frame, width=20)
        self.gas_price.grid(row=row, column=1, padx=5, pady=3)
        
        tk.Label(consumption_frame, text="Cena elektriny [€/kWh]:").grid(row=row, column=2, sticky=tk.W, padx=5, pady=3)
        self.electricity_price = tk.Entry(consumption_frame, width=20)
        self.electricity_price.grid(row=row, column=3, padx=5, pady=3)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_results_tab(self):
        """Tab 8: Výsledky"""
        tab8 = ttk.Frame(self.notebook)
        self.notebook.add(tab8, text="📊 Výsledky")
        
        self.results_text = scrolledtext.ScrolledText(tab8, font=('Consolas', 10), 
                                                      bg='#f8f9fa', wrap=tk.WORD)
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.results_text.insert(tk.END, "Výsledky sa zobrazia po vykonaní energetického auditu...")
        
    def create_bottom_panel(self):
        """Spodný panel s tlačidlami"""
        bottom_frame = tk.Frame(self.root, bg='#ecf0f1', height=120)
        bottom_frame.pack(fill=tk.X, side=tk.BOTTOM)
        bottom_frame.pack_propagate(False)
        
        # PROGRESS BAR
        progress_frame = tk.Frame(bottom_frame, bg='#ecf0f1')
        progress_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(progress_frame, text="Priebeh:", bg='#ecf0f1', font=('Arial', 10)).pack(side=tk.LEFT, padx=10)
        self.progress = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress.pack(fill=tk.X, padx=10)
        
        # TLAČIDLÁ
        buttons_frame = tk.Frame(bottom_frame, bg='#ecf0f1')
        buttons_frame.pack(fill=tk.X, pady=5)
        
        # HLAVNÉ TLAČIDLO
        self.audit_button = tk.Button(buttons_frame, 
                                     text="🔬 VYKONAŤ KOMPLETNÝ AUDIT",
                                     command=self.perform_comprehensive_audit,
                                     bg='#27ae60', fg='white',
                                     font=('Arial', 14, 'bold'),
                                     width=25, height=2,
                                     relief=tk.RAISED, bd=5)
        self.audit_button.pack(side=tk.LEFT, padx=20)
        
        # OSTATNÉ TLAČIDLÁ
        tk.Button(buttons_frame, text="💾 ULOŽIŤ",
                 command=self.save_project, bg='#3498db', fg='white',
                 font=('Arial', 10, 'bold'), width=12, height=2).pack(side=tk.LEFT, padx=5)
        
        tk.Button(buttons_frame, text="📂 NAČÍTAŤ",
                 command=self.load_project, bg='#9b59b6', fg='white',
                 font=('Arial', 10, 'bold'), width=12, height=2).pack(side=tk.LEFT, padx=5)
        
        tk.Button(buttons_frame, text="🧮 POZRIEŤ VÝPOČET",
                 command=self.show_calculation_details, bg='#f39c12', fg='white',
                 font=('Arial', 10, 'bold'), width=15, height=2).pack(side=tk.LEFT, padx=5)
        
        tk.Button(buttons_frame, text="🏅 CERTIFIKÁT",
                 command=self.generate_certificate, bg='#e67e22', fg='white',
                 font=('Arial', 10, 'bold'), width=12, height=2).pack(side=tk.LEFT, padx=5)
        
        tk.Button(buttons_frame, text="❌ UKONČIŤ",
                 command=self.root.quit, bg='#e74c3c', fg='white',
                 font=('Arial', 10, 'bold'), width=12, height=2).pack(side=tk.RIGHT, padx=20)
                 
    def collect_comprehensive_data(self):
        """Zber všetkých údajov z formulárov"""
        try:
            self.audit_data = {
                'basic_info': {
                    'building_name': self.building_name.get() or "Test budova",
                    'address': self.address.get() or "",
                    'cadastral': self.cadastral.get() or "",
                    'owner': self.owner.get() or "",
                    'construction_year': int(self.construction_year.get() or 2000),
                    'renovation_year': int(self.renovation_year.get() or 0) if self.renovation_year.get() else None,
                    'floors_count': int(self.floors_count.get() or 1),
                    'building_height': float(self.building_height.get() or 3),
                    'floor_area': float(self.floor_area.get() or 120),
                    'volume': float(self.volume.get() or 360),
                    'building_type': self.building_type.get() or "Rodinný dom",
                    'construction_system': self.construction_system.get() or "Murovaný"
                },
                'envelope': {
                    'wall_area': float(self.wall_area.get() or 150),
                    'wall_u': float(self.wall_u.get() or 0.25),
                    'wall_insulation': self.wall_insulation.get() or "",
                    'wall_insulation_thickness': float(self.wall_insulation_thickness.get() or 0) if self.wall_insulation_thickness.get() else 0,
                    'window_area': float(self.window_area.get() or 25),
                    'window_u': float(self.window_u.get() or 1.1),
                    'window_type': self.window_type.get() or "",
                    'window_frame': self.window_frame.get() or "",
                    'roof_area': float(self.roof_area.get() or 120),
                    'roof_u': float(self.roof_u.get() or 0.2),
                    'roof_type': self.roof_type.get() or "",
                    'roof_insulation': float(self.roof_insulation.get() or 0) if self.roof_insulation.get() else 0,
                    'floor_area_envelope': float(self.floor_area_envelope.get() or 120),
                    'floor_u': float(self.floor_u.get() or 0.3)
                },
                'heating': {
                    'type': self.heating_type.get() or "Plynový kotol klasický",
                    'power': float(self.heating_power.get() or 15),
                    'efficiency': float(self.heating_efficiency.get() or 90) / 100,
                    'installation_year': int(self.heating_installation.get() or 2000) if self.heating_installation.get() else None,
                    'fuel_type': self.fuel_type.get() or "Zemný plyn",
                    'distribution_type': self.distribution_type.get() or "Radiátory",
                    'pipe_insulation': float(self.pipe_insulation.get() or 50) if self.pipe_insulation.get() else 50,
                    'control': self.heating_control.get() or "Termostatické hlavice"
                },
                'cooling_ventilation': {
                    'cooling_type': self.cooling_type.get() or "Bez chladenia",
                    'cooling_power': float(self.cooling_power.get() or 0) if self.cooling_power.get() else 0,
                    'cooling_seer': float(self.cooling_seer.get() or 3.5) if self.cooling_seer.get() else 3.5,
                    'ventilation_type': self.ventilation_type.get() or "Prirodzené vetranie",
                    'air_flow': float(self.air_flow.get() or 0) if self.air_flow.get() else 0,
                    'heat_recovery': float(self.heat_recovery.get() or 0) if self.heat_recovery.get() else 0
                },
                'lighting_equipment': {
                    'lighting_type': self.lighting_type.get() or "LED",
                    'lighting_power': float(self.lighting_power.get() or 500) if self.lighting_power.get() else 500,
                    'lighting_control': self.lighting_control.get() or "Manuálne",
                    'it_equipment': float(self.it_equipment.get() or 200) if self.it_equipment.get() else 200,
                    'kitchen_appliances': float(self.kitchen_appliances.get() or 300) if self.kitchen_appliances.get() else 300,
                    'other_appliances': float(self.other_appliances.get() or 100) if self.other_appliances.get() else 100,
                    'energy_label': self.energy_label.get() or "A"
                },
                'dhw': {
                    'type': self.dhw_type.get() or "Elektrický bojler",
                    'volume': float(self.dhw_volume.get() or 200) if self.dhw_volume.get() else 200,
                    'efficiency': float(self.dhw_efficiency.get() or 85) / 100 if self.dhw_efficiency.get() else 0.85,
                    'insulation': self.dhw_insulation.get() or "Štandardná",
                    'circulation': self.dhw_circulation.get() or "Bez cirkulácie"
                },
                'usage': {
                    'occupants': int(self.occupants.get() or 4),
                    'operating_hours': float(self.operating_hours.get() or 12),
                    'operating_days': int(self.operating_days.get() or 250),
                    'winter_temperature': float(self.winter_temperature.get() or 21),
                    'summer_temperature': float(self.summer_temperature.get() or 25),
                    'gas_consumption': float(self.gas_consumption.get() or 0) if self.gas_consumption.get() else 0,
                    'electricity_consumption': float(self.electricity_consumption.get() or 0) if self.electricity_consumption.get() else 0,
                    'gas_price': float(self.gas_price.get() or 0.8) if self.gas_price.get() else 0.8,
                    'electricity_price': float(self.electricity_price.get() or 0.15) if self.electricity_price.get() else 0.15
                }
            }
            return True
        except ValueError as e:
            messagebox.showerror("Chyba", f"Neplatné údaje: {e}")
            return False
            
    def perform_comprehensive_audit(self):
        """Vykonanie kompletného energetického auditu"""
        
        # Zber údajov
        if not self.collect_comprehensive_data():
            return
            
        self.audit_button.config(text="⏳ PREBIEHA KOMPLETNÝ AUDIT...", state=tk.DISABLED)
        self.progress['value'] = 0
        self.root.update()
        
        try:
            # Postupné výpočty s progress barom
            self.progress['value'] = 10
            self.root.update()
            
            # Základné údaje
            basic = self.audit_data['basic_info']
            envelope = self.audit_data['envelope']
            heating = self.audit_data['heating']
            usage = self.audit_data['usage']
            
            self.progress['value'] = 20
            self.root.update()
            
            # VÝPOČET TEPELNÝCH STRÁT
            # Steny
            wall_losses = envelope['wall_area'] * envelope['wall_u']
            # Okná
            window_losses = envelope['window_area'] * envelope['window_u']
            # Strecha
            roof_losses = envelope['roof_area'] * envelope['roof_u']
            # Podlaha
            floor_losses = envelope['floor_area_envelope'] * envelope['floor_u']
            
            total_losses = wall_losses + window_losses + roof_losses + floor_losses
            
            self.progress['value'] = 35
            self.root.update()
            
            # POTREBA TEPLA
            hdd = 2800  # Bratislava
            heating_need = total_losses * hdd * 24 / 1000  # kWh/rok
            
            self.progress['value'] = 50
            self.root.update()
            
            # SPOTREBA ENERGIE NA VYKUROVANIE
            heating_energy = heating_need / heating['efficiency']
            
            # ELEKTRICKÁ ENERGIA
            # Osvetlenie
            lighting = self.audit_data['lighting_equipment']
            lighting_energy = (lighting['lighting_power'] * usage['operating_hours'] * usage['operating_days']) / 1000
            
            # Zariadenia
            equipment_energy = ((lighting['it_equipment'] + lighting['kitchen_appliances'] + 
                               lighting['other_appliances']) * usage['operating_hours'] * usage['operating_days']) / 1000
            
            # Teplá voda
            dhw = self.audit_data['dhw']
            dhw_energy = usage['occupants'] * 40 * 365 * 1.163 / 1000  # kWh/rok (40l/osoba/deň)
            dhw_final_energy = dhw_energy / dhw['efficiency']
            
            total_electricity = lighting_energy + equipment_energy + dhw_final_energy
            
            self.progress['value'] = 70
            self.root.update()
            
            # CELKOVÁ ENERGIA
            total_energy = heating_energy + total_electricity
            
            # PRIMÁRNA ENERGIA
            primary_heating = heating_energy * 1.1  # faktor pre plyn
            primary_electricity = total_electricity * 3.0  # faktor pre elektrinu
            primary_energy = primary_heating + primary_electricity
            
            specific_primary = primary_energy / basic['floor_area']
            
            self.progress['value'] = 85
            self.root.update()
            
            # ENERGETICKÁ TRIEDA
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
                
            # CO2 EMISIE
            co2_heating = heating_energy * 0.202  # kg CO2/kWh pre plyn
            co2_electricity = total_electricity * 0.486  # kg CO2/kWh pre elektrinu
            co2_emissions = co2_heating + co2_electricity
            specific_co2 = co2_emissions / basic['floor_area']
            
            # EKONOMICKÉ HODNOTENIE
            annual_cost = heating_energy * 0.8 + total_electricity * 0.15  # €/rok
            
            self.progress['value'] = 100
            self.root.update()
            
            # Uloženie výsledkov
            self.results = {
                'heating_need': heating_need,
                'heating_energy': heating_energy,
                'lighting_energy': lighting_energy,
                'equipment_energy': equipment_energy,
                'dhw_energy': dhw_final_energy,
                'total_electricity': total_electricity,
                'total_energy': total_energy,
                'primary_energy': primary_energy,
                'specific_primary': specific_primary,
                'energy_class': energy_class,
                'co2_emissions': co2_emissions,
                'specific_co2': specific_co2,
                'annual_cost': annual_cost,
                'wall_losses': wall_losses,
                'window_losses': window_losses,
                'roof_losses': roof_losses,
                'floor_losses': floor_losses,
                'total_losses': total_losses
            }
            
            # Zobrazenie výsledkov
            self.display_comprehensive_results()
            
            messagebox.showinfo("Úspech", "✅ Kompletný energetický audit dokončený!")
            
        except Exception as e:
            messagebox.showerror("Chyba", f"Chyba pri výpočte: {e}")
        finally:
            self.audit_button.config(text="🔬 VYKONAŤ KOMPLETNÝ AUDIT", state=tk.NORMAL)
            self.progress['value'] = 0
            
    def display_comprehensive_results(self):
        """Zobrazenie kompletných výsledkov"""
        self.results_text.delete(1.0, tk.END)
        
        basic = self.audit_data['basic_info']
        results = self.results
        
        output = f"""
{'='*80}
📋 KOMPLETNÝ ENERGETICKÝ AUDIT - VÝSLEDKY
{'='*80}

🏢 BUDOVA: {basic['building_name']}
📍 Adresa: {basic['address']}
📐 Podlahová plocha: {basic['floor_area']:.0f} m²
📐 Obostavaný priestor: {basic['volume']:.0f} m³
📅 Rok výstavby: {basic['construction_year']}
🏗️  Typ budovy: {basic['building_type']}

{'='*80}
🔥 TEPELNÉ STRATY OBÁLKY BUDOVY
{'='*80}

🧱 Straty stenami: {results['wall_losses']:.2f} W/K
🪟 Straty oknami: {results['window_losses']:.2f} W/K  
🏠 Straty strechou: {results['roof_losses']:.2f} W/K
🔳 Straty podlahou: {results['floor_losses']:.2f} W/K
📊 CELKOVÉ STRATY: {results['total_losses']:.2f} W/K

{'='*80}
⚡ ENERGETICKÁ BILANCIA
{'='*80}

🔥 Potreba tepla na vykurovanie: {results['heating_need']:.0f} kWh/rok
🔥 Spotreba na vykurovanie: {results['heating_energy']:.0f} kWh/rok
💡 Spotreba na osvetlenie: {results['lighting_energy']:.0f} kWh/rok
⚙️  Spotreba zariadení: {results['equipment_energy']:.0f} kWh/rok
🚿 Spotreba na teplú vodu: {results['dhw_energy']:.0f} kWh/rok
📊 Celková elektrina: {results['total_electricity']:.0f} kWh/rok
⚡ CELKOVÁ SPOTREBA: {results['total_energy']:.0f} kWh/rok

{'='*80}
🎯 ENERGETICKÉ HODNOTENIE
{'='*80}

🔢 Primárna energia: {results['primary_energy']:.0f} kWh/rok
📐 Špecifická primárna energia: {results['specific_primary']:.1f} kWh/m²rok
🏅 ENERGETICKÁ TRIEDA: {results['energy_class']}

Klasifikácia:
A: ≤ 50 kWh/m²rok    B: ≤ 75 kWh/m²rok    C: ≤ 110 kWh/m²rok
D: ≤ 150 kWh/m²rok   E: ≤ 200 kWh/m²rok   F: ≤ 250 kWh/m²rok

{'='*80}
🌍 ENVIRONMENTÁLNY DOPAD
{'='*80}

🌱 CO2 emisie: {results['co2_emissions']:.0f} kg CO2/rok
📐 Špecifické CO2 emisie: {results['specific_co2']:.1f} kg CO2/m²rok

{'='*80}
💰 EKONOMICKÉ HODNOTENIE
{'='*80}

💵 Odhadované ročné náklady: {results['annual_cost']:.0f} €/rok
📐 Náklady na m²: {results['annual_cost'] / basic['floor_area']:.2f} €/m²rok

{'='*80}
💡 ODPORÚČANIA NA ZLEPŠENIE
{'='*80}

"""
        
        # Generovanie odporúčaní
        envelope = self.audit_data['envelope']
        recommendations = []
        
        if envelope['wall_u'] > 0.30:
            recommendations.append("🧱 Zateplenie vonkajších stien - úspory 20-30%")
        if envelope['window_u'] > 2.0:
            recommendations.append("🪟 Výmena okien za kvalitnejšie - úspory 10-20%")
        if envelope['roof_u'] > 0.25:
            recommendations.append("🏠 Zateplenie strechy - úspory 15-25%")
        if self.audit_data['heating']['efficiency'] < 0.85:
            recommendations.append("🔥 Modernizácia vykurovacieho systému - úspory 20-40%")
        if self.audit_data['lighting_equipment']['lighting_type'] != "LED":
            recommendations.append("💡 Prechod na LED osvetlenie - úspory 50-70%")
        if self.audit_data['cooling_ventilation']['ventilation_type'] == "Prirodzené vetranie":
            recommendations.append("💨 Inštalácia rekuperácie - úspory 20-30%")
            
        if recommendations:
            for rec in recommendations:
                output += f"{rec}\n"
        else:
            output += "✅ Budova je v dobrom energetickom stave\n"
            
        output += f"""
{'='*80}
📚 POUŽITÉ NORMY A ŠTANDARDY
{'='*80}

• STN EN 16247-1: Energetické audity - Časť 1: Všeobecné požiadavky
• STN EN ISO 13790: Energetická náročnosť budov - Výpočet spotreby energie
• Vyhláška MH SR č. 364/2012 Z. z. o energetickej náročnosti budov
• STN 73 0540: Tepelná ochrana budov
• STN EN 15603: Energetická náročnosť budov - Celková spotreba energie

📋 Audit vypracovaný: {datetime.now().strftime('%d.%m.%Y %H:%M')}
👨‍💼 Energetický audítor: Systém EA v1.0

{'='*80}
"""
        
        self.results_text.insert(tk.END, output)
        
        # Prepnutie na tab s výsledkami
        self.notebook.select(7)  # Index tabu výsledkov
        
    def show_calculation_details(self):
        """Zobrazenie detailných výpočtov - podobne ako v simple_audit_gui"""
        if not self.audit_data or not self.results:
            messagebox.showwarning("Upozornenie", "Najprv vykonajte audit pre zobrazenie výpočtov.")
            return
        messagebox.showinfo("Info", "Detailné výpočty budú implementované v ďalšej verzii.")
        
    def save_project(self):
        """Uloženie projektu do JSON"""
        if not self.audit_data:
            messagebox.showwarning("Upozornenie", "Nie je čo uložiť.")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON súbory", "*.json"), ("Všetky súbory", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump({
                        'audit_data': self.audit_data,
                        'results': self.results,
                        'timestamp': datetime.now().isoformat()
                    }, f, ensure_ascii=False, indent=2)
                messagebox.showinfo("Úspech", f"Projekt uložený: {filename}")
            except Exception as e:
                messagebox.showerror("Chyba", f"Chyba pri ukladaní: {e}")
                
    def load_project(self):
        """Načítanie projektu z JSON"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON súbory", "*.json"), ("Všetky súbory", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                self.audit_data = data.get('audit_data', {})
                self.results = data.get('results', {})
                
                # Načítanie údajov do formulárov
                self.load_data_to_forms()
                
                if self.results:
                    self.display_comprehensive_results()
                    
                messagebox.showinfo("Úspech", f"Projekt načítaný: {filename}")
            except Exception as e:
                messagebox.showerror("Chyba", f"Chyba pri načítavaní: {e}")
                
    def load_data_to_forms(self):
        """Načítanie údajov do formulárov"""
        # Implementácia načítania údajov do všetkých polí
        try:
            if 'basic_info' in self.audit_data:
                basic = self.audit_data['basic_info']
                self.building_name.delete(0, tk.END)
                self.building_name.insert(0, basic.get('building_name', ''))
                # ... a tak ďalej pre všetky polia
        except Exception as e:
            print(f"Chyba pri načítavaní do formulárov: {e}")
        
    def generate_certificate(self):
        """Generovanie certifikátu"""
        if not self.results:
            messagebox.showwarning("Upozornenie", "Najprv vykonajte audit.")
            return
            
        basic = self.audit_data['basic_info']
        results = self.results
        
        certificate_info = f"""
🏅 ENERGETICKÝ CERTIFIKÁT

Budova: {basic['building_name']}
Číslo certifikátu: EC-{datetime.now().strftime('%Y%m%d%H%M')}

Energetická trieda: {results['energy_class']}
Špecifická primárna energia: {results['specific_primary']:.1f} kWh/m²rok
CO2 emisie: {results['specific_co2']:.1f} kg CO2/m²rok

Dátum vydania: {datetime.now().strftime('%d.%m.%Y')}
Platnosť do: {datetime.now().replace(year=datetime.now().year + 10).strftime('%d.%m.%Y')}

Certifikát vystavil: EA Systém v1.0
"""
        
        messagebox.showinfo("Certifikát", certificate_info)

def main():
    """Spustenie aplikácie"""
    root = tk.Tk()
    app = ComprehensiveEnergyAuditGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()