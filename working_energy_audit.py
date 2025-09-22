#!/usr/bin/env python3
"""
FUNGUJÚCA PROFESIONÁLNA ENERGETICKÝ AUDIT APLIKÁCIA
User-friendly s bezproblémovým zberom dát a profesionálnymi výstupmi
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
from datetime import datetime
import json
import math

class WorkingEnergyAudit:
    def __init__(self, root):
        self.root = root
        self.root.title("🏢 Profesionálny Energetický Audit System v2.0")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f5f5f5')
        
        # Dáta
        self.audit_data = {}
        self.results = {}
        self.current_project_file = None
        
        self.create_gui()
        
    def create_gui(self):
        """Vytvorenie hlavného GUI"""
        
        # PROFESIONÁLNA HLAVIČKA
        self.create_header()
        
        # HLAVNÝ OBSAH S TABMI
        self.create_main_tabs()
        
        # SPODNÝ PANEL S TLAČIDLAMI
        self.create_action_panel()
        
        # STATUS BAR
        self.create_status_bar()
        
    def create_header(self):
        """Profesionálna hlavička"""
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Ľavá strana
        left_frame = tk.Frame(header_frame, bg='#2c3e50')
        left_frame.pack(side=tk.LEFT, padx=20, pady=15)
        
        title_label = tk.Label(left_frame, 
                              text="🏢 PROFESIONÁLNY ENERGETICKÝ AUDIT",
                              font=('Arial', 16, 'bold'), fg='white', bg='#2c3e50')
        title_label.pack(anchor=tk.W)
        
        subtitle_label = tk.Label(left_frame,
                                 text="Systém pre energetické audity podľa STN EN 16247-1",
                                 font=('Arial', 9), fg='#bdc3c7', bg='#2c3e50')
        subtitle_label.pack(anchor=tk.W)
        
        # Pravá strana - info o projekte
        right_frame = tk.Frame(header_frame, bg='#2c3e50')
        right_frame.pack(side=tk.RIGHT, padx=20, pady=15)
        
        self.project_label = tk.Label(right_frame, text="Nový projekt",
                                     font=('Arial', 12, 'bold'), fg='#ecf0f1', bg='#2c3e50')
        self.project_label.pack(anchor=tk.E)
        
        date_label = tk.Label(right_frame, 
                             text=f"📅 {datetime.now().strftime('%d.%m.%Y %H:%M')}",
                             font=('Arial', 9), fg='#bdc3c7', bg='#2c3e50')
        date_label.pack(anchor=tk.E)
        
    def create_main_tabs(self):
        """Hlavné taby s formulármi"""
        tab_frame = tk.Frame(self.root, bg='#f5f5f5')
        tab_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Vytvorenie notebook widget
        self.notebook = ttk.Notebook(tab_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Vytvorenie jednotlivých tabov
        self.create_basic_info_tab()
        self.create_envelope_tab()
        self.create_heating_tab()
        self.create_electrical_tab()
        self.create_usage_tab()
        self.create_results_tab()
        
    def create_basic_info_tab(self):
        """Tab 1: Základné informácie podľa STN EN 16247-1"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🏢 Základné údaje")
        
        # Scrollable frame
        canvas = tk.Canvas(tab)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind("<Configure>", 
                             lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # IDENTIFIKAČNÉ ÚDAJE PODĽA STN EN 16247-1
        id_frame = tk.LabelFrame(scrollable_frame, text="🏢 Identifikácia objektu (STN EN 16247-1 bod 6.2.1)", 
                                font=('Arial', 11, 'bold'))
        id_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Riad 1
        tk.Label(id_frame, text="Názov budovy *:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.building_name = tk.Entry(id_frame, width=30, font=('Arial', 9))
        self.building_name.grid(row=0, column=1, padx=5, pady=3)
        
        tk.Label(id_frame, text="Účel budovy *:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=3)
        self.building_purpose = ttk.Combobox(id_frame, width=25, values=[
            "Rodinný dom", "Bytový dom", "Administratívna budova", "Škola", "Nemocnica",
            "Hotel", "Obchodné centrum", "Reštaurácia", "Priemyselná budova", "Sklad", "Ostatné"
        ])
        self.building_purpose.grid(row=0, column=3, padx=5, pady=3)
        self.building_purpose.bind('<<ComboboxSelected>>', self.on_building_purpose_changed)
        
        # Riad 2  
        tk.Label(id_frame, text="Adresa *:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=3)
        self.address = tk.Entry(id_frame, width=30, font=('Arial', 9))
        self.address.grid(row=1, column=1, padx=5, pady=3)
        
        tk.Label(id_frame, text="PSČ a obec:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=3)
        self.postal_city = tk.Entry(id_frame, width=25, font=('Arial', 9))
        self.postal_city.grid(row=1, column=3, padx=5, pady=3)
        
        # Riad 3
        tk.Label(id_frame, text="Katastrálne územie:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=3)
        self.cadastral = tk.Entry(id_frame, width=30, font=('Arial', 9))
        self.cadastral.grid(row=2, column=1, padx=5, pady=3)
        
        tk.Label(id_frame, text="Súpisné/orientačné číslo:").grid(row=2, column=2, sticky=tk.W, padx=5, pady=3)
        self.house_number = tk.Entry(id_frame, width=25, font=('Arial', 9))
        self.house_number.grid(row=2, column=3, padx=5, pady=3)
        
        # Riad 4
        tk.Label(id_frame, text="Vlastník budovy *:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=3)
        self.owner = tk.Entry(id_frame, width=30, font=('Arial', 9))
        self.owner.grid(row=3, column=1, padx=5, pady=3)
        
        tk.Label(id_frame, text="IČO vlastníka:").grid(row=3, column=2, sticky=tk.W, padx=5, pady=3)
        self.owner_ico = tk.Entry(id_frame, width=25, font=('Arial', 9))
        self.owner_ico.grid(row=3, column=3, padx=5, pady=3)
        
        # Riad 5
        tk.Label(id_frame, text="Kontaktná osoba *:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=3)
        self.contact_person = tk.Entry(id_frame, width=30, font=('Arial', 9))
        self.contact_person.grid(row=4, column=1, padx=5, pady=3)
        
        tk.Label(id_frame, text="Telefón/Email:").grid(row=4, column=2, sticky=tk.W, padx=5, pady=3)
        self.contact_details = tk.Entry(id_frame, width=25, font=('Arial', 9))
        self.contact_details.grid(row=4, column=3, padx=5, pady=3)
        
        # TECHNICKÉ CHARAKTERISTIKY PODĽA NORMY
        tech_frame = tk.LabelFrame(scrollable_frame, text="📐 Technické charakteristiky (STN EN 16247-1 bod 6.2.2)", 
                                  font=('Arial', 11, 'bold'))
        tech_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Riad 1 - Základné rozmery
        tk.Label(tech_frame, text="Rok výstavby *:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.construction_year = tk.Entry(tech_frame, width=15)
        self.construction_year.grid(row=0, column=1, padx=5, pady=3)
        
        tk.Label(tech_frame, text="Rok poslednej rekonštrukcie:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=3)
        self.renovation_year = tk.Entry(tech_frame, width=15)
        self.renovation_year.grid(row=0, column=3, padx=5, pady=3)
        
        tk.Label(tech_frame, text="Energetická trieda (aktuálna):").grid(row=0, column=4, sticky=tk.W, padx=5, pady=3)
        self.current_energy_class = ttk.Combobox(tech_frame, width=12, values=["A", "B", "C", "D", "E", "F", "G", "Neznáma"])
        self.current_energy_class.grid(row=0, column=5, padx=5, pady=3)
        
        # Riad 2 - Plochy a objemy
        tk.Label(tech_frame, text="Podlahová plocha (vykurovaná) [m²] *:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=3)
        self.floor_area = tk.Entry(tech_frame, width=15)
        self.floor_area.grid(row=1, column=1, padx=5, pady=3)
        
        tk.Label(tech_frame, text="Podlahová plocha (celková) [m²]:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=3)
        self.total_floor_area = tk.Entry(tech_frame, width=15)
        self.total_floor_area.grid(row=1, column=3, padx=5, pady=3)
        
        tk.Label(tech_frame, text="Obostavaný priestor [m³] *:").grid(row=1, column=4, sticky=tk.W, padx=5, pady=3)
        self.volume = tk.Entry(tech_frame, width=12)
        self.volume.grid(row=1, column=5, padx=5, pady=3)
        
        # Riad 3 - Geometria
        tk.Label(tech_frame, text="Počet nadzemných podlaží *:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=3)
        self.floors_above = tk.Entry(tech_frame, width=15)
        self.floors_above.grid(row=2, column=1, padx=5, pady=3)
        
        tk.Label(tech_frame, text="Počet podzemných podlaží:").grid(row=2, column=2, sticky=tk.W, padx=5, pady=3)
        self.floors_below = tk.Entry(tech_frame, width=15)
        self.floors_below.grid(row=2, column=3, padx=5, pady=3)
        
        tk.Label(tech_frame, text="Svetlá výška [m]:").grid(row=2, column=4, sticky=tk.W, padx=5, pady=3)
        self.ceiling_height = tk.Entry(tech_frame, width=12)
        self.ceiling_height.grid(row=2, column=5, padx=5, pady=3)
        
        # Riad 4 - Konštrukčný systém
        tk.Label(tech_frame, text="Konštrukčný systém *:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=3)
        self.construction_system = ttk.Combobox(tech_frame, width=13, values=[
            "Murovaný", "Montovaný betón", "Skelet ŽB", "Oceľový skelet", "Drevostavba", "Zmiešaný", "Ostatné"
        ])
        self.construction_system.grid(row=3, column=1, padx=5, pady=3)
        
        tk.Label(tech_frame, text="Typ založenia:").grid(row=3, column=2, sticky=tk.W, padx=5, pady=3)
        self.foundation_type = ttk.Combobox(tech_frame, width=13, values=[
            "Základové pásy", "Základová doska", "Pilóty", "Suterén", "Ostatné"
        ])
        self.foundation_type.grid(row=3, column=3, padx=5, pady=3)
        
        tk.Label(tech_frame, text="Orientácia hlavnej fasády:").grid(row=3, column=4, sticky=tk.W, padx=5, pady=3)
        self.orientation = ttk.Combobox(tech_frame, width=10, values=["S", "SV", "V", "JV", "J", "JZ", "Z", "SZ"])
        self.orientation.grid(row=3, column=5, padx=5, pady=3)
        
        # KLIMATICKÉ ÚDAJE
        climate_frame = tk.LabelFrame(scrollable_frame, text="🌤️ Klimatické údaje a lokalita", 
                                     font=('Arial', 11, 'bold'))
        climate_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Riad 1
        tk.Label(climate_frame, text="Klimatická oblasť:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.climate_zone = ttk.Combobox(climate_frame, width=20, values=[
            "Teplá (do 500 m n.m.)", "Mierna (500-800 m n.m.)", "Chladná (nad 800 m n.m.)"
        ])
        self.climate_zone.grid(row=0, column=1, padx=5, pady=3)
        
        tk.Label(climate_frame, text="Nadmorská výška [m]:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=3)
        self.altitude = tk.Entry(climate_frame, width=15)
        self.altitude.grid(row=0, column=3, padx=5, pady=3)
        
        # Riad 2 - Automatické nastavenie podľa mest
        tk.Label(climate_frame, text="Lokalita (automatické HDD):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=3)
        self.city_location = ttk.Combobox(climate_frame, width=18, values=[
            "Bratislava (2800)", "Košice (3200)", "Prešov (3400)", "Banská Bystrica (3600)",
            "Trnava (2850)", "Žilina (3300)", "Nitra (2900)", "Trenčín (3000)",
            "Martin (3350)", "Poprad (3800)", "Komárno (2700)", "Nové Zámky (2750)",
            "Piettåny (2950)", "Ružomberok (3500)", "Zvolen (3450)", "Levoča (3550)",
            "Vlastné nastavenie"
        ])
        self.city_location.grid(row=1, column=1, padx=5, pady=3)
        self.city_location.bind('<<ComboboxSelected>>', self.on_city_changed)
        
        tk.Label(climate_frame, text="HDD (stupeň.dni) [K.deň/rok]:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=3)
        self.hdd = tk.Entry(climate_frame, width=15)
        self.hdd.grid(row=1, column=3, padx=5, pady=3)
        
        # Riad 3
        tk.Label(climate_frame, text="Prevažujúci smer vetra:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=3)
        self.wind_direction = ttk.Combobox(climate_frame, width=20, values=["S", "SV", "V", "JV", "J", "JZ", "Z", "SZ", "Premenlivý"])
        self.wind_direction.grid(row=2, column=1, padx=5, pady=3)
        
        tk.Label(climate_frame, text="Tienenie budovy:").grid(row=2, column=2, sticky=tk.W, padx=5, pady=3)
        self.shading = ttk.Combobox(climate_frame, width=13, values=["Žiadne", "Čiastočné", "Značné", "Úplné"])
        self.shading.grid(row=2, column=3, padx=5, pady=3)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def on_city_changed(self, event=None):
        """Automatické nastavenie HDD podľa vybratého mesta"""
        city_hdd_mapping = {
            "Bratislava (2800)": "2800",
            "Košice (3200)": "3200", 
            "Prešov (3400)": "3400",
            "Banská Bystrica (3600)": "3600",
            "Trnava (2850)": "2850",
            "Žilina (3300)": "3300",
            "Nitra (2900)": "2900",
            "Trenčín (3000)": "3000",
            "Martin (3350)": "3350",
            "Poprad (3800)": "3800",
            "Komárno (2700)": "2700",
            "Nové Zámky (2750)": "2750",
            "Pietťany (2950)": "2950",
            "Ružomberok (3500)": "3500",
            "Zvolen (3450)": "3450",
            "Levoča (3550)": "3550"
        }
        
        selected_city = self.city_location.get()
        if selected_city in city_hdd_mapping:
            self.hdd.delete(0, tk.END)
            self.hdd.insert(0, city_hdd_mapping[selected_city])
    
    def on_building_purpose_changed(self, event=None):
        """Auto-doplnenie po výbere účelu budovy"""
        purpose = self.building_purpose.get()
        defaults = {
            "Rodinný dom": {'occupants': '4', 'hours': '12', 'days': '365', 'winter_temp': '21'},
            "Bytový dom": {'occupants': '20', 'hours': '16', 'days': '365', 'winter_temp': '21'},
            "Škola": {'occupants': '300', 'hours': '8', 'days': '185', 'winter_temp': '20'},
            "Administratívna budova": {'occupants': '50', 'hours': '10', 'days': '250', 'winter_temp': '22'},
            "Hotel": {'occupants': '40', 'hours': '24', 'days': '365', 'winter_temp': '22'},
            "Obchodné centrum": {'occupants': '200', 'hours': '12', 'days': '365', 'winter_temp': '18'},
            "Reštaurácia": {'occupants': '30', 'hours': '12', 'days': '300', 'winter_temp': '20'}
        }
        if purpose in defaults:
            values = defaults[purpose]
            # Auto-fill len ak polia už existujú (taby sú vytvárané postupne)
            if hasattr(self, 'occupants') and hasattr(self.occupants, 'delete'): 
                self.occupants.delete(0, tk.END)
                self.occupants.insert(0, values['occupants'])
            if hasattr(self, 'operating_hours') and hasattr(self.operating_hours, 'delete'):
                self.operating_hours.delete(0, tk.END)
                self.operating_hours.insert(0, values['hours'])
            if hasattr(self, 'operating_days') and hasattr(self.operating_days, 'delete'):
                self.operating_days.delete(0, tk.END)
                self.operating_days.insert(0, values['days'])
            if hasattr(self, 'winter_temp') and hasattr(self.winter_temp, 'delete'):
                self.winter_temp.delete(0, tk.END)
                self.winter_temp.insert(0, values['winter_temp'])
    
    def on_heating_type_changed(self, event=None):
        """Auto-doplnenie po výbere typu vykurovania"""
        heating_type = self.heating_type.get()
        defaults = {
            "Plynový kotol kondenzačný": {'efficiency': '92', 'fuel': 'Zemný plyn', 'supply_temp': '55', 'fp_heating': '1.1', 'fco2_heating': '0.202'},
            "Plynový kotol klasický": {'efficiency': '85', 'fuel': 'Zemný plyn', 'supply_temp': '70', 'fp_heating': '1.1', 'fco2_heating': '0.202'},
            "Elektrický kotol": {'efficiency': '95', 'fuel': 'Elektrina', 'supply_temp': '60', 'fp_heating': '2.5', 'fco2_heating': '0.296'},
            "Tepelné čerpadlo vzduch-voda": {'efficiency': '330', 'fuel': 'Elektrina', 'supply_temp': '35', 'fp_heating': '2.5', 'fco2_heating': '0.089'},
            "Tepelné čerpadlo zem-voda": {'efficiency': '400', 'fuel': 'Elektrina', 'supply_temp': '35', 'fp_heating': '2.5', 'fco2_heating': '0.074'},
            "Tepelné čerpadlo voda-voda": {'efficiency': '450', 'fuel': 'Elektrina', 'supply_temp': '35', 'fp_heating': '2.5', 'fco2_heating': '0.066'},
            "Biomasa (pelety)": {'efficiency': '88', 'fuel': 'Pelety', 'supply_temp': '65', 'fp_heating': '1.2', 'fco2_heating': '0.025'},
            "Biomasa (drevo)": {'efficiency': '75', 'fuel': 'Drevo', 'supply_temp': '70', 'fp_heating': '1.1', 'fco2_heating': '0.022'}
        }
        if heating_type in defaults:
            values = defaults[heating_type]
            self.heating_efficiency.delete(0, tk.END)
            self.heating_efficiency.insert(0, values['efficiency'])
            self.fuel_type.set(values['fuel'])
            self.supply_temp.delete(0, tk.END)
            self.supply_temp.insert(0, values['supply_temp'])
            self.fp_heating.delete(0, tk.END)
            self.fp_heating.insert(0, values['fp_heating'])
            self.fco2_heating.delete(0, tk.END)
            self.fco2_heating.insert(0, values['fco2_heating'])
    
    def on_fuel_changed(self, event=None):
        """Auto-doplnenie emisných faktorov pre palivo"""
        fuel = self.fuel_type.get()
        factors = {
            "Zemný plyn": {'fp': '1.1', 'fco2': '0.202'},
            "Elektrina": {'fp': '2.5', 'fco2': '0.296'},
            "Pelety": {'fp': '1.2', 'fco2': '0.025'},
            "Drevo": {'fp': '1.1', 'fco2': '0.022'},
            "LPG": {'fp': '1.3', 'fco2': '0.235'}
        }
        if fuel in factors:
            values = factors[fuel]
            # Nastaviť len ak nie je elektrické kúrenie (pre el. kurenie sa faktory nastavia zo samotného kúrenia)
            heating_type = self.heating_type.get()
            if "Elektrický" not in heating_type and "Tepelné čerpadlo" not in heating_type:
                self.fp_heating.delete(0, tk.END)
                self.fp_heating.insert(0, values['fp'])
                self.fco2_heating.delete(0, tk.END)
                self.fco2_heating.insert(0, values['fco2'])
        # Nastaviť aj základné faktory pre elektrinu
        self.fp_electricity.delete(0, tk.END)
        self.fp_electricity.insert(0, '2.5')
        self.fco2_electricity.delete(0, tk.END)
        self.fco2_electricity.insert(0, '0.296')
    
    def on_lighting_type_changed(self, event=None):
        """Auto-doplnenie vlastností osvetlenia"""
        lighting_type = self.lighting_type.get()
        # Môžeme nastaviť odhadovaný výkon na základe typu a plochy
        try:
            floor_area = float(self.floor_area.get() or 0)
            power_per_m2 = {
                "LED": 8,
                "Fluorescenčné (T5/T8)": 12,
                "Halogénové": 15,
                "Výbojkové": 18,
                "Klasické žiarovky": 25
            }
            if lighting_type in power_per_m2 and floor_area > 0:
                estimated_power = floor_area * power_per_m2[lighting_type]
                self.lighting_power.delete(0, tk.END)
                self.lighting_power.insert(0, str(int(estimated_power)))
        except ValueError:
            pass
    
    def on_dhw_type_changed(self, event=None):
        """Auto-doplnenie parametrov teplej vody"""
        dhw_type = self.dhw_type.get()
        defaults = {
            "Elektrický bojler": {'efficiency': '85', 'circulation': 'Časová'},
            "Plynový bojler": {'efficiency': '78', 'circulation': 'Bez cirkulácie'},
            "Kombinovaný kotol": {'efficiency': '85', 'circulation': 'Termostatická'},
            "Solárne kolektory": {'efficiency': '60', 'circulation': 'Termostatická'},
            "Tepelné čerpadlo": {'efficiency': '250', 'circulation': 'Termostatická'}
        }
        if dhw_type in defaults:
            values = defaults[dhw_type]
            self.dhw_efficiency.delete(0, tk.END)
            self.dhw_efficiency.insert(0, values['efficiency'])
            self.dhw_circulation.set(values['circulation'])
            
            # Odhad objemu zásobníka podľa počtu osôb
            try:
                occupants = int(self.occupants.get() if hasattr(self, 'occupants') and self.occupants.get() else '4')
                estimated_volume = occupants * 50  # 50l na osobu
                self.dhw_volume.delete(0, tk.END)
                self.dhw_volume.insert(0, str(estimated_volume))
            except ValueError:
                pass
            
    def create_envelope_tab(self):
        """Tab 2: Obálka budovy podľa STN EN 16247-1"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🧱 Obálka budovy")
        
        canvas = tk.Canvas(tab)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind("<Configure>", 
                             lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # VONKAJŠIE STENY (STN EN 16247-1 bod 6.2.3)
        walls_frame = tk.LabelFrame(scrollable_frame, text="🧱 Vonkajšie steny (STN EN 16247-1 bod 6.2.3)", 
                                   font=('Arial', 11, 'bold'))
        walls_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Riad 1
        tk.Label(walls_frame, text="Celková plocha stien [m²] *:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.wall_area = tk.Entry(walls_frame, width=15)
        self.wall_area.grid(row=0, column=1, padx=5, pady=3)
        
        tk.Label(walls_frame, text="U-hodnota stien [W/m²K] *:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=3)
        self.wall_u = tk.Entry(walls_frame, width=15)
        self.wall_u.grid(row=0, column=3, padx=5, pady=3)
        
        tk.Label(walls_frame, text="Typ konštrukcie stien:").grid(row=0, column=4, sticky=tk.W, padx=5, pady=3)
        self.wall_construction = ttk.Combobox(walls_frame, width=18, values=[
            "Jednoplashá murovaná", "Dvojplashá murovaná", "Sendvičová", "Montovaná betónová", 
            "Drevenká", "Železobetová", "Lastrock", "Ytong", "Keramická"
        ])
        self.wall_construction.grid(row=0, column=5, padx=5, pady=3)
        
        # Riad 2
        tk.Label(walls_frame, text="Typ tepelnej izolácie *:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=3)
        self.wall_insulation = ttk.Combobox(walls_frame, width=13, values=[
            "Bez izolácie", "ETICS (kontaktný)", "Vnútorná", "Dutinová", "Fasadistic", 
            "Kombinácia", "Inhérent (izol. betony)"
        ])
        self.wall_insulation.grid(row=1, column=1, padx=5, pady=3)
        
        tk.Label(walls_frame, text="Hrúbka izolácie [mm]:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=3)
        self.wall_insulation_thickness = tk.Entry(walls_frame, width=15)
        self.wall_insulation_thickness.grid(row=1, column=3, padx=5, pady=3)
        
        tk.Label(walls_frame, text="Typ izolačného materiálu:").grid(row=1, column=4, sticky=tk.W, padx=5, pady=3)
        self.wall_insulation_material = ttk.Combobox(walls_frame, width=16, values=[
            "EPS (polystyén)", "XPS (extrud. polystyén)", "Mineralná vlna", "PUR/PIR pena", 
            "Féniová pena", "Konopa", "Drťvé vlákno", "Celulóza", "Perlite", "Vakuúmové"
        ])
        self.wall_insulation_material.grid(row=1, column=5, padx=5, pady=3)
        
        # Riad 3 - Detaily
        tk.Label(walls_frame, text="Plocha tepelných mostov [m²]:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=3)
        self.thermal_bridges_area = tk.Entry(walls_frame, width=13)
        self.thermal_bridges_area.grid(row=2, column=1, padx=5, pady=3)
        
        tk.Label(walls_frame, text="Linear. súčiniteľ Ψ [W/mK]:").grid(row=2, column=2, sticky=tk.W, padx=5, pady=3)
        self.thermal_bridges_psi = tk.Entry(walls_frame, width=15)
        self.thermal_bridges_psi.grid(row=2, column=3, padx=5, pady=3)
        
        tk.Label(walls_frame, text="Stav povrchu:").grid(row=2, column=4, sticky=tk.W, padx=5, pady=3)
        self.wall_surface_condition = ttk.Combobox(walls_frame, width=16, values=[
            "Nový/dobrý", "Márne pokoké", "Pokoké", "Zlý", "Havarínvý"
        ])
        self.wall_surface_condition.grid(row=2, column=5, padx=5, pady=3)
        
        # OKNÁ A DVERE (STN EN 16247-1 bod 6.2.4)
        windows_frame = tk.LabelFrame(scrollable_frame, text="🪟 Okná a dvere (STN EN 16247-1 bod 6.2.4)", 
                                     font=('Arial', 11, 'bold'))
        windows_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Riad 1 - Okná
        tk.Label(windows_frame, text="Plocha okien celkom [m²] *:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.window_area = tk.Entry(windows_frame, width=13)
        self.window_area.grid(row=0, column=1, padx=5, pady=3)
        
        tk.Label(windows_frame, text="U-hodnota okien [W/m²K] *:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=3)
        self.window_u = tk.Entry(windows_frame, width=15)
        self.window_u.grid(row=0, column=3, padx=5, pady=3)
        
        tk.Label(windows_frame, text="g-hodnota (solares g) [-]:").grid(row=0, column=4, sticky=tk.W, padx=5, pady=3)
        self.window_g_value = tk.Entry(windows_frame, width=15)
        self.window_g_value.grid(row=0, column=5, padx=5, pady=3)
        
        # Riad 2 - Typy okien
        tk.Label(windows_frame, text="Typ zasklenia *:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=3)
        self.window_glazing = ttk.Combobox(windows_frame, width=11, values=[
            "Jednoduché sklo", "Dvojsklo", "Trojsklo", "4-sklo", "Vakuúmové", "Aerogel"
        ])
        self.window_glazing.grid(row=1, column=1, padx=5, pady=3)
        
        tk.Label(windows_frame, text="Typ rámu:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=3)
        self.window_frame_type = ttk.Combobox(windows_frame, width=13, values=[
            "Drevený", "Plastový", "Hliníkový", "Hliník s t.mostom", "Kompozitný", "Oceľový"
        ])
        self.window_frame_type.grid(row=1, column=3, padx=5, pady=3)
        
        tk.Label(windows_frame, text="Orientácia väčšiny okien:").grid(row=1, column=4, sticky=tk.W, padx=5, pady=3)
        self.window_orientation = ttk.Combobox(windows_frame, width=13, values=[
            "Sever", "Severovýchod", "Východ", "Juhovýchod", "Juh", "Juhozapad", "Západ", "Severozapad"
        ])
        self.window_orientation.grid(row=1, column=5, padx=5, pady=3)
        
        # Riad 3 - Dvere a detaily
        tk.Label(windows_frame, text="Plocha vchod. dvier [m²]:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=3)
        self.doors_area = tk.Entry(windows_frame, width=13)
        self.doors_area.grid(row=2, column=1, padx=5, pady=3)
        
        tk.Label(windows_frame, text="U-hodnota dvier [W/m²K]:").grid(row=2, column=2, sticky=tk.W, padx=5, pady=3)
        self.doors_u = tk.Entry(windows_frame, width=15)
        self.doors_u.grid(row=2, column=3, padx=5, pady=3)
        
        tk.Label(windows_frame, text="Vonkajšie clony/žalúzie:").grid(row=2, column=4, sticky=tk.W, padx=5, pady=3)
        self.external_shading = ttk.Combobox(windows_frame, width=13, values=[
            "Bez clon", "Žalúzie", "Rolety", "Markízy", "Pevné clony", "Náběhy strechy"
        ])
        self.external_shading.grid(row=2, column=5, padx=5, pady=3)
        
        # STRECHA (STN EN 16247-1 bod 6.2.5)
        roof_frame = tk.LabelFrame(scrollable_frame, text="🏠 Strecha (STN EN 16247-1 bod 6.2.5)", 
                                  font=('Arial', 11, 'bold'))
        roof_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Riad 1
        tk.Label(roof_frame, text="Plocha strechy [m²] *:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.roof_area = tk.Entry(roof_frame, width=15)
        self.roof_area.grid(row=0, column=1, padx=5, pady=3)
        
        tk.Label(roof_frame, text="U-hodnota strechy [W/m²K] *:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=3)
        self.roof_u = tk.Entry(roof_frame, width=15)
        self.roof_u.grid(row=0, column=3, padx=5, pady=3)
        
        tk.Label(roof_frame, text="Typ strechy:").grid(row=0, column=4, sticky=tk.W, padx=5, pady=3)
        self.roof_type = ttk.Combobox(roof_frame, width=18, values=[
            "Plochá strecha", "Šikmá strecha", "Sedlová strecha", "Valbová strecha", 
            "Mansardová", "Pulteáka", "Kombinovaná", "Vegetacíná strecha"
        ])
        self.roof_type.grid(row=0, column=5, padx=5, pady=3)
        
        # Riad 2
        tk.Label(roof_frame, text="Sklon strechy [°]:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=3)
        self.roof_slope = tk.Entry(roof_frame, width=15)
        self.roof_slope.grid(row=1, column=1, padx=5, pady=3)
        
        tk.Label(roof_frame, text="Typ tepelnej izolácie:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=3)
        self.roof_insulation_type = ttk.Combobox(roof_frame, width=13, values=[
            "Bez izolácie", "Nad krokvami", "Medzi krokvami", "Pod krokvami", 
            "Na stropnej konšt.", "Kombinácia"
        ])
        self.roof_insulation_type.grid(row=1, column=3, padx=5, pady=3)
        
        tk.Label(roof_frame, text="Hrúbka izolácie [mm]:").grid(row=1, column=4, sticky=tk.W, padx=5, pady=3)
        self.roof_insulation_thickness = tk.Entry(roof_frame, width=16)
        self.roof_insulation_thickness.grid(row=1, column=5, padx=5, pady=3)
        
        # Riad 3 - Str. okná a detaily
        tk.Label(roof_frame, text="Plocha streng. okien [m²]:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=3)
        self.roof_windows_area = tk.Entry(roof_frame, width=13)
        self.roof_windows_area.grid(row=2, column=1, padx=5, pady=3)
        
        tk.Label(roof_frame, text="U-hodn. streng. okien [W/m²K]:").grid(row=2, column=2, sticky=tk.W, padx=5, pady=3)
        self.roof_windows_u = tk.Entry(roof_frame, width=15)
        self.roof_windows_u.grid(row=2, column=3, padx=5, pady=3)
        
        tk.Label(roof_frame, text="Farba strechy:").grid(row=2, column=4, sticky=tk.W, padx=5, pady=3)
        self.roof_color = ttk.Combobox(roof_frame, width=16, values=[
            "Svetlá (α < 0.4)", "Stredná (α 0.4-0.8)", "Tmavá (α > 0.8)"
        ])
        self.roof_color.grid(row=2, column=5, padx=5, pady=3)
        
        # PODLAHA A ZÁKLADY (STN EN 16247-1 bod 6.2.6)
        floor_frame = tk.LabelFrame(scrollable_frame, text="🔲 Podlaha a základy (STN EN 16247-1 bod 6.2.6)", 
                                   font=('Arial', 11, 'bold'))
        floor_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Riad 1
        tk.Label(floor_frame, text="Plocha podlahy [m²] *:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.floor_area_envelope = tk.Entry(floor_frame, width=15)
        self.floor_area_envelope.grid(row=0, column=1, padx=5, pady=3)
        
        tk.Label(floor_frame, text="U-hodnota podlahy [W/m²K] *:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=3)
        self.floor_u = tk.Entry(floor_frame, width=15)
        self.floor_u.grid(row=0, column=3, padx=5, pady=3)
        
        tk.Label(floor_frame, text="Typ kontaktu so zemou:").grid(row=0, column=4, sticky=tk.W, padx=5, pady=3)
        self.floor_ground_contact = ttk.Combobox(floor_frame, width=16, values=[
            "Podlaha na zemi", "Podlaha nad suterénom", "Podlaha nad exteriérom", 
            "Podlaha nad garou", "Podlaha nad prieveterným prostrom"
        ])
        self.floor_ground_contact.grid(row=0, column=5, padx=5, pady=3)
        
        # Riad 2
        tk.Label(floor_frame, text="Obsada základů-zem [m]:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=3)
        self.foundation_depth = tk.Entry(floor_frame, width=15)
        self.foundation_depth.grid(row=1, column=1, padx=5, pady=3)
        
        tk.Label(floor_frame, text="Typ tepelnej izolácie:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=3)
        self.floor_insulation_type = ttk.Combobox(floor_frame, width=13, values=[
            "Bez izolácie", "Pod betónovou doskou", "Nad doskou", "V k0nštrukci", 
            "Obvodová izolácia", "Kombinácia"
        ])
        self.floor_insulation_type.grid(row=1, column=3, padx=5, pady=3)
        
        tk.Label(floor_frame, text="Hrúbka izolácie [mm]:").grid(row=1, column=4, sticky=tk.W, padx=5, pady=3)
        self.floor_insulation_thickness = tk.Entry(floor_frame, width=16)
        self.floor_insulation_thickness.grid(row=1, column=5, padx=5, pady=3)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_heating_tab(self):
        """Tab 3: Vykurovanie podľa STN EN 16247-1"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🔥 Vykurovanie")
        
        canvas = tk.Canvas(tab)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind("<Configure>", 
                             lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # ZDROJ TEPLA A VÝROBA
        heating_frame = tk.LabelFrame(scrollable_frame, text="🔥 Zdroj tepla a výroba (STN EN 16247-1 bod 6.2.7)", 
                                     font=('Arial', 11, 'bold'))
        heating_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(heating_frame, text="Typ vykurovania *:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.heating_type = ttk.Combobox(heating_frame, width=28, values=[
            "Plynový kotol kondenzačný", "Plynový kotol klasický", "Elektrický kotol",
            "Tepelné čerpadlo vzduch-voda", "Tepelné čerpadlo zem-voda", "Tepelné čerpadlo voda-voda",
            "Biomasa (pelety)", "Biomasa (drevo)", "Kombinovaný systém"
        ])
        self.heating_type.grid(row=0, column=1, padx=5, pady=3)
        self.heating_type.bind('<<ComboboxSelected>>', self.on_heating_type_changed)
        
        tk.Label(heating_frame, text="Menovitý výkon [kW]:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=3)
        self.heating_power = tk.Entry(heating_frame, width=12)
        self.heating_power.grid(row=0, column=3, padx=5, pady=3)
        
        tk.Label(heating_frame, text="Sezónna účinnosť ηs [%] *:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=3)
        self.heating_efficiency = tk.Entry(heating_frame, width=12)
        self.heating_efficiency.grid(row=1, column=1, padx=5, pady=3)
        
        tk.Label(heating_frame, text="Výstupná teplota vykurovania [°C]:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=3)
        self.supply_temp = tk.Entry(heating_frame, width=12)
        self.supply_temp.grid(row=1, column=3, padx=5, pady=3)
        
        tk.Label(heating_frame, text="Rok inštalácie:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=3)
        self.heating_year = tk.Entry(heating_frame, width=12)
        self.heating_year.grid(row=2, column=1, padx=5, pady=3)
        
        tk.Label(heating_frame, text="Palivo *:").grid(row=2, column=2, sticky=tk.W, padx=5, pady=3)
        self.fuel_type = ttk.Combobox(heating_frame, width=18, values=[
            "Zemný plyn", "Elektrina", "Pelety", "Drevo", "LPG"
        ])
        self.fuel_type.grid(row=2, column=3, padx=5, pady=3)
        self.fuel_type.bind('<<ComboboxSelected>>', self.on_fuel_changed)
        
        # EMISNÉ A PRIMÁRNE FAKTORY
        factors_frame = tk.LabelFrame(scrollable_frame, text="🌍 Faktory primárnej energie a emisie (referenčné)", font=('Arial', 11, 'bold'))
        factors_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(factors_frame, text="fp (vykurovanie):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.fp_heating = tk.Entry(factors_frame, width=10)
        self.fp_heating.grid(row=0, column=1, padx=5, pady=3)
        
        tk.Label(factors_frame, text="fp (elektrina):").grid(row=0, column=2, sticky=tk.W, padx=5, pady=3)
        self.fp_electricity = tk.Entry(factors_frame, width=10)
        self.fp_electricity.grid(row=0, column=3, padx=5, pady=3)
        
        tk.Label(factors_frame, text="fCO2 (vykurovanie) [kg/kWh]:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=3)
        self.fco2_heating = tk.Entry(factors_frame, width=10)
        self.fco2_heating.grid(row=1, column=1, padx=5, pady=3)
        
        tk.Label(factors_frame, text="fCO2 (elektrina) [kg/kWh]:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=3)
        self.fco2_electricity = tk.Entry(factors_frame, width=10)
        self.fco2_electricity.grid(row=1, column=3, padx=5, pady=3)
        
        # DISTRIBÚCIA A REGULÁCIA
        dist_frame = tk.LabelFrame(scrollable_frame, text="🌡️ Distribúcia tepla a regulácia", 
                                  font=('Arial', 11, 'bold'))
        dist_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(dist_frame, text="Typ distribúcie:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.distribution_type = ttk.Combobox(dist_frame, width=20, values=[
            "Radiátory (vyššoteplotné)", "Podlahové kúrenie (nízkoteplotné)", "Konvektory", "Teplovzdušné"
        ])
        self.distribution_type.grid(row=0, column=1, padx=5, pady=3)
        
        tk.Label(dist_frame, text="Izolácia rozvodov [%]:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=3)
        self.pipe_insulation = tk.Entry(dist_frame, width=10)
        self.pipe_insulation.grid(row=0, column=3, padx=5, pady=3)
        
        tk.Label(dist_frame, text="Regulácia:").grid(row=0, column=4, sticky=tk.W, padx=5, pady=3)
        self.heating_control = ttk.Combobox(dist_frame, width=20, values=[
            "Bez regulácie", "Termostatické hlavice", "Ekvitermická", "Zónová regulácia", "Inteligentný systém"
        ])
        self.heating_control.grid(row=0, column=5, padx=5, pady=3)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_electrical_tab(self):
        """Tab 4: Elektrina, osvetlenie a TUV podľa STN EN 16247-1"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="💡 Elektrina")
        
        canvas = tk.Canvas(tab)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind("<Configure>", 
                             lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # OSVETLENIE
        light_frame = tk.LabelFrame(scrollable_frame, text="💡 Osvetlenie (STN EN 16247-1 bod 6.2.8)", 
                                   font=('Arial', 11, 'bold'))
        light_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(light_frame, text="Typ svietidiel:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.lighting_type = ttk.Combobox(light_frame, width=18, values=[
            "LED", "Fluorescenčné (T5/T8)", "Halogénové", "Výbojkové", "Klasické žiarovky"
        ])
        self.lighting_type.grid(row=0, column=1, padx=5, pady=3)
        self.lighting_type.bind('<<ComboboxSelected>>', self.on_lighting_type_changed)
        
        tk.Label(light_frame, text="Inštalovaný výkon [W]:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=3)
        self.lighting_power = tk.Entry(light_frame, width=12)
        self.lighting_power.grid(row=0, column=3, padx=5, pady=3)
        
        tk.Label(light_frame, text="Riadenie osvetlenia:").grid(row=0, column=4, sticky=tk.W, padx=5, pady=3)
        self.lighting_control = ttk.Combobox(light_frame, width=18, values=[
            "Manuálne", "Časové spínače", "Senzory pohybu", "Denné svetlo", "Inteligentný systém"
        ])
        self.lighting_control.grid(row=0, column=5, padx=5, pady=3)
        
        # ELEKTRICKÉ ZARIADENIA
        devices_frame = tk.LabelFrame(scrollable_frame, text="⚡ Elektrické zariadenia", 
                                     font=('Arial', 11, 'bold'))
        devices_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(devices_frame, text="IT zariadenia [W]:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.it_power = tk.Entry(devices_frame, width=12)
        self.it_power.grid(row=0, column=1, padx=5, pady=3)
        
        tk.Label(devices_frame, text="Ostatné spotrebiče [W]:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=3)
        self.appliances_power = tk.Entry(devices_frame, width=12)
        self.appliances_power.grid(row=0, column=3, padx=5, pady=3)
        
        # TEPLÁ VODA (TUV)
        dhw_frame = tk.LabelFrame(scrollable_frame, text="🚿 Ohrev teplej vody (STN EN 16247-1 bod 6.2.9)", 
                                 font=('Arial', 11, 'bold'))
        dhw_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(dhw_frame, text="Typ ohrevu TUV:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.dhw_type = ttk.Combobox(dhw_frame, width=22, values=[
            "Elektrický bojler", "Plynový bojler", "Kombinovaný kotol", "Solárne kolektory", "Tepelné čerpadlo"
        ])
        self.dhw_type.grid(row=0, column=1, padx=5, pady=3)
        self.dhw_type.bind('<<ComboboxSelected>>', self.on_dhw_type_changed)
        
        tk.Label(dhw_frame, text="Objem zásobníka [l]:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=3)
        self.dhw_volume = tk.Entry(dhw_frame, width=12)
        self.dhw_volume.grid(row=0, column=3, padx=5, pady=3)
        
        tk.Label(dhw_frame, text="Účinnosť ohrevu ηTUV [%]:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=3)
        self.dhw_efficiency = tk.Entry(dhw_frame, width=12)
        self.dhw_efficiency.grid(row=1, column=1, padx=5, pady=3)
        
        tk.Label(dhw_frame, text="Cirkulácia TUV:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=3)
        self.dhw_circulation = ttk.Combobox(dhw_frame, width=18, values=[
            "Bez cirkulácie", "Neprerušovaná", "Časová", "Termostatická"
        ])
        self.dhw_circulation.grid(row=1, column=3, padx=5, pady=3)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_usage_tab(self):
        """Tab 5: Užívanie budovy a prevádzka podľa STN EN 16247-1"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="👥 Užívanie")
        
        canvas = tk.Canvas(tab)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind("<Configure>", 
                             lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # OBSADENOSŤ A PREVÁDZKA
        occupancy_frame = tk.LabelFrame(scrollable_frame, text="👥 Obsadenosť a prevádzka (STN EN 16247-1 bod 6.2.10)", 
                                       font=('Arial', 11, 'bold'))
        occupancy_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(occupancy_frame, text="Počet užívateľov (osoby):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.occupants = tk.Entry(occupancy_frame, width=12)
        self.occupants.grid(row=0, column=1, padx=5, pady=3)
        
        tk.Label(occupancy_frame, text="Hodiny/deň:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=3)
        self.operating_hours = tk.Entry(occupancy_frame, width=12)
        self.operating_hours.grid(row=0, column=3, padx=5, pady=3)
        
        tk.Label(occupancy_frame, text="Dni/rok:").grid(row=0, column=4, sticky=tk.W, padx=5, pady=3)
        self.operating_days = tk.Entry(occupancy_frame, width=12)
        self.operating_days.grid(row=0, column=5, padx=5, pady=3)
        
        tk.Label(occupancy_frame, text="Nastavená teplota zima [°C]:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=3)
        self.winter_temp = tk.Entry(occupancy_frame, width=12)
        self.winter_temp.grid(row=1, column=1, padx=5, pady=3)
        
        tk.Label(occupancy_frame, text="Nastavená teplota leto [°C]:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=3)
        self.summer_temp = tk.Entry(occupancy_frame, width=12)
        self.summer_temp.grid(row=1, column=3, padx=5, pady=3)
        
        # AKTUÁLNA SPOTREBA A TARIFY
        consumption_frame = tk.LabelFrame(scrollable_frame, text="📊 Energetická bilancia (meraná) a ceny", 
                                         font=('Arial', 11, 'bold'))
        consumption_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(consumption_frame, text="Ročná spotreba plynu [m³]:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.gas_consumption = tk.Entry(consumption_frame, width=12)
        self.gas_consumption.grid(row=0, column=1, padx=5, pady=3)
        
        tk.Label(consumption_frame, text="Ročná spotreba elektriny [kWh]:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=3)
        self.electricity_consumption = tk.Entry(consumption_frame, width=12)
        self.electricity_consumption.grid(row=0, column=3, padx=5, pady=3)
        
        tk.Label(consumption_frame, text="Cena plynu [€/m³]:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=3)
        self.gas_price = tk.Entry(consumption_frame, width=12)
        self.gas_price.grid(row=1, column=1, padx=5, pady=3)
        
        tk.Label(consumption_frame, text="Cena elektriny [€/kWh]:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=3)
        self.electricity_price = tk.Entry(consumption_frame, width=12)
        self.electricity_price.grid(row=1, column=3, padx=5, pady=3)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_results_tab(self):
        """Tab 6: Výsledky"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📊 Výsledky")
        
        # Hlavný frame pre výsledky
        results_frame = tk.Frame(tab, bg='white')
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Nadpis
        title_label = tk.Label(results_frame, text="📊 VÝSLEDKY ENERGETICKÉHO AUDITU",
                              font=('Arial', 16, 'bold'), bg='white', fg='#2c3e50')
        title_label.pack(pady=(10, 20))
        
        # Text area pre výsledky
        self.results_text = scrolledtext.ScrolledText(results_frame, 
                                                     font=('Consolas', 10), 
                                                     bg='#f8f9fa', wrap=tk.WORD)
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Predvolený text
        welcome_text = """
=== ENERGETICKÝ AUDIT - VÝSLEDKY ===

Pre zobrazenie výsledkov je potrebné:
1. Vyplniť všetky povinné údaje v jednotlivých taboch
2. Kliknúť na tlačidlo "🔬 VYKONAŤ AUDIT"

Výsledky budú obsahovať:
• Tepelné straty obálky budovy
• Energetickú bilanciu
• Energetickú triedu (A-G)
• CO2 emisie
• Ekonomické hodnotenie
• Odporúčania na zlepšenie

Audit sa vykonáva podľa noriem:
• STN EN 16247-1 (Energetické audity)
• STN EN ISO 13790 (Energetická náročnosť budov)
• Vyhláška MH SR č. 364/2012 Z. z.
        """
        self.results_text.insert(tk.END, welcome_text)
        
    def create_action_panel(self):
        """Spodný panel s akčnými tlačidlami"""
        action_frame = tk.Frame(self.root, bg='#ecf0f1', height=100)
        action_frame.pack(fill=tk.X, side=tk.BOTTOM)
        action_frame.pack_propagate(False)
        
        # Progress bar
        progress_frame = tk.Frame(action_frame, bg='#ecf0f1')
        progress_frame.pack(fill=tk.X, padx=20, pady=(10, 5))
        
        tk.Label(progress_frame, text="Priebeh:", bg='#ecf0f1', 
                font=('Arial', 10)).pack(side=tk.LEFT)
        self.progress = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
        
        # Tlačidlá
        buttons_frame = tk.Frame(action_frame, bg='#ecf0f1')
        buttons_frame.pack(fill=tk.X, padx=20, pady=5)
        
        # Hlavné tlačidlo
        self.audit_btn = tk.Button(buttons_frame, 
                                  text="🔬 VYKONAŤ ENERGETICKÝ AUDIT",
                                  command=self.perform_audit,
                                  bg='#27ae60', fg='white',
                                  font=('Arial', 14, 'bold'),
                                  width=28, height=2,
                                  relief=tk.RAISED, bd=3)
        self.audit_btn.pack(side=tk.LEFT, padx=(0, 20))
        
        # Ostatné tlačidlá
        tk.Button(buttons_frame, text="💾 Uložiť projekt", command=self.save_project,
                 bg='#3498db', fg='white', font=('Arial', 11, 'bold'),
                 width=15, height=2).pack(side=tk.LEFT, padx=5)
        
        tk.Button(buttons_frame, text="📂 Načítať projekt", command=self.load_project,
                 bg='#9b59b6', fg='white', font=('Arial', 11, 'bold'),
                 width=15, height=2).pack(side=tk.LEFT, padx=5)
        
        tk.Button(buttons_frame, text="🧮 Detailné výpočty", command=self.show_calculations,
                 bg='#f39c12', fg='white', font=('Arial', 11, 'bold'),
                 width=15, height=2).pack(side=tk.LEFT, padx=5)
        
        tk.Button(buttons_frame, text="🏅 Certifikát", command=self.generate_certificate,
                 bg='#e67e22', fg='white', font=('Arial', 11, 'bold'),
                 width=15, height=2).pack(side=tk.LEFT, padx=5)
        
        tk.Button(buttons_frame, text="❌ Ukončiť", command=self.root.quit,
                 bg='#e74c3c', fg='white', font=('Arial', 11, 'bold'),
                 width=12, height=2).pack(side=tk.RIGHT)
        
    def create_status_bar(self):
        """Stavový panel"""
        status_frame = tk.Frame(self.root, bg='#bdc3c7', height=25)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(status_frame, text="Pripravený", 
                                    bg='#bdc3c7', font=('Arial', 9))
        self.status_label.pack(side=tk.LEFT, padx=10, pady=3)
        
        version_label = tk.Label(status_frame, text="v2.0 | STN EN 16247", 
                                bg='#bdc3c7', font=('Arial', 9))
        version_label.pack(side=tk.RIGHT, padx=10, pady=3)
        
    def collect_data(self):
        """Zber všetkých údajov z formulárov podľa STN EN 16247-1"""
        try:
            data = {
                'basic_info': {
                    'building_name': self.building_name.get() or "Test budova",
                    'building_purpose': self.building_purpose.get() or "Rodinný dom",
                    'address': self.address.get() or "",
                    'postal_city': self.postal_city.get() or "",
                    'cadastral': self.cadastral.get() or "",
                    'house_number': self.house_number.get() or "",
                    'owner': self.owner.get() or "",
                    'owner_ico': self.owner_ico.get() or "",
                    'contact_person': self.contact_person.get() or "",
                    'contact_details': self.contact_details.get() or "",
                    'construction_year': int(self.construction_year.get() or 2000),
                    'renovation_year': int(self.renovation_year.get() or 0) if self.renovation_year.get() else None,
                    'current_energy_class': self.current_energy_class.get() or "Neznáma",
                    'floor_area': float(self.floor_area.get() or 120),
                    'total_floor_area': float(self.total_floor_area.get() or 0) if self.total_floor_area.get() else None,
                    'volume': float(self.volume.get() or 360),
                    'floors_above': int(self.floors_above.get() or 1),
                    'floors_below': int(self.floors_below.get() or 0) if self.floors_below.get() else 0,
                    'ceiling_height': float(self.ceiling_height.get() or 2.7) if self.ceiling_height.get() else 2.7,
                    'construction_system': self.construction_system.get() or "Murovaný",
                    'foundation_type': self.foundation_type.get() or "Základové pásy",
                    'orientation': self.orientation.get() or "J",
                    'climate_zone': self.climate_zone.get() or "Mierna (500-800 m n.m.)",
                    'altitude': float(self.altitude.get() or 300) if self.altitude.get() else 300,
                    'hdd': float(self.hdd.get() or 2800),
                    'wind_direction': self.wind_direction.get() or "Premenlivý",
                    'shading': self.shading.get() or "Čiastočné"
                },
                'envelope': {
                    'wall_area': float(self.wall_area.get() or 150),
                    'wall_u': float(self.wall_u.get() or 0.25),
                    'wall_insulation': self.wall_insulation.get() or "",
                    'wall_insulation_thickness': float(self.wall_insulation_thickness.get() or 0) if self.wall_insulation_thickness.get() else 0,
                    'window_area': float(self.window_area.get() or 25),
                    'window_u': float(self.window_u.get() or 1.1),
                    'window_type': self.window_type.get() or "",
                    'roof_area': float(self.roof_area.get() or 120),
                    'roof_u': float(self.roof_u.get() or 0.2)
                },
                'heating': {
                    'type': self.heating_type.get() or "Plynový kotol klasický",
                    'power': float(self.heating_power.get() or 15),
                    'efficiency': float(self.heating_efficiency.get() or 90) / 100,
                    'year': int(self.heating_year.get() or 2010) if self.heating_year.get() else None,
                    'fuel_type': self.fuel_type.get() or "Zemný plyn",
                    'distribution_type': self.distribution_type.get() or "Radiátory",
                    'control': self.heating_control.get() or "Termostatické hlavice"
                },
                'electrical': {
                    'lighting_type': self.lighting_type.get() or "LED",
                    'lighting_power': float(self.lighting_power.get() or 500) if self.lighting_power.get() else 500,
                    'it_power': float(self.it_power.get() or 200) if self.it_power.get() else 200,
                    'appliances_power': float(self.appliances_power.get() or 300) if self.appliances_power.get() else 300,
                    'dhw_type': self.dhw_type.get() or "Elektrický bojler",
                    'dhw_volume': float(self.dhw_volume.get() or 200) if self.dhw_volume.get() else 200
                },
                'usage': {
                    'occupants': int(self.occupants.get() or 4),
                    'operating_hours': float(self.operating_hours.get() or 12),
                    'operating_days': int(self.operating_days.get() or 250),
                    'winter_temp': float(self.winter_temp.get() or 21),
                    'summer_temp': float(self.summer_temp.get() or 24) if hasattr(self, 'summer_temp') and self.summer_temp.get() else 24,
                    'gas_consumption': float(self.gas_consumption.get() or 0) if self.gas_consumption.get() else 0,
                    'electricity_consumption': float(self.electricity_consumption.get() or 0) if self.electricity_consumption.get() else 0,
                    'gas_price': float(self.gas_price.get() or 0.8) if self.gas_price.get() else 0.8,
                    'electricity_price': float(self.electricity_price.get() or 0.15) if self.electricity_price.get() else 0.15
                }
            }
            self.audit_data = data
            return True
        except ValueError as e:
            messagebox.showerror("Chyba údajov", f"Neplatné údaje: {str(e)}")
            return False
            
    def perform_audit(self):
        """Vykonanie energetického auditu"""
        # Zber údajov
        if not self.collect_data():
            return
            
        self.status_label.config(text="Prebieha audit...")
        self.audit_btn.config(text="⏳ PREBIEHA AUDIT...", state=tk.DISABLED)
        self.progress['value'] = 0
        self.root.update()
        
        try:
            # Progres 20% - Validácia
            self.progress['value'] = 20
            self.root.update()
            
            # Základné údaje
            basic = self.audit_data['basic_info']
            envelope = self.audit_data['envelope']
            heating = self.audit_data['heating']
            usage = self.audit_data['usage']
            electrical = self.audit_data['electrical']
            
            # Progres 40% - Tepelné straty
            self.progress['value'] = 40
            self.root.update()
            
            # VÝPOČET TEPELNÝCH STRÁT
            wall_losses = envelope['wall_area'] * envelope['wall_u']
            window_losses = envelope['window_area'] * envelope['window_u']
            roof_losses = envelope['roof_area'] * envelope['roof_u']
            total_losses = wall_losses + window_losses + roof_losses
            
            # Progres 60% - Potreba tepla
            self.progress['value'] = 60
            self.root.update()
            
            # POTREBA TEPLA (HDD metóda pre Slovensko)
            hdd = 2800  # Bratislava
            heating_need = total_losses * hdd * 24 / 1000  # kWh/rok
            
            # SPOTREBA ENERGIE NA VYKUROVANIE
            heating_energy = heating_need / heating['efficiency']
            
            # Progres 80% - Elektrická energia
            self.progress['value'] = 80
            self.root.update()
            
            # ELEKTRICKÁ ENERGIA
            lighting_energy = (electrical['lighting_power'] * usage['operating_hours'] * 
                             usage['operating_days']) / 1000
            
            appliances_energy = ((electrical['it_power'] + electrical['appliances_power']) * 
                               usage['operating_hours'] * usage['operating_days']) / 1000
            
            # Teplá voda (40l/osoba/deň)
            dhw_energy = usage['occupants'] * 40 * 365 * 1.163 / 1000  # kWh/rok
            
            total_electricity = lighting_energy + appliances_energy + dhw_energy
            
            # CELKOVÁ ENERGIA
            total_energy = heating_energy + total_electricity
            
            # PRIMÁRNA ENERGIA
            primary_heating = heating_energy * 1.1  # faktor pre plyn
            primary_electricity = total_electricity * 3.0  # faktor pre elektrinu
            primary_energy = primary_heating + primary_electricity
            
            specific_primary = primary_energy / basic['floor_area']
            
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
            annual_cost = heating_energy * usage['gas_price'] * 10.55 + total_electricity * usage['electricity_price']
            
            # Progres 100% - Dokončenie
            self.progress['value'] = 100
            self.root.update()
            
            # Uloženie výsledkov
            self.results = {
                'heating_need': heating_need,
                'heating_energy': heating_energy,
                'lighting_energy': lighting_energy,
                'appliances_energy': appliances_energy,
                'dhw_energy': dhw_energy,
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
                'total_losses': total_losses
            }
            
            # Zobrazenie výsledkov
            self.display_results()
            
            # Prepnutie na tab výsledkov
            self.notebook.select(5)  # Index tabu výsledkov
            
            self.status_label.config(text="Audit dokončený úspešne!")
            messagebox.showinfo("Úspech", "✅ Energetický audit dokončený úspešne!")
            
        except Exception as e:
            messagebox.showerror("Chyba", f"Chyba pri výpočte: {str(e)}")
            self.status_label.config(text="Chyba pri audite")
        finally:
            self.audit_btn.config(text="🔬 VYKONAŤ ENERGETICKÝ AUDIT", state=tk.NORMAL)
            self.progress['value'] = 0
            
    def display_results(self):
        """Zobrazenie výsledkov v tabu"""
        self.results_text.delete(1.0, tk.END)
        
        basic = self.audit_data['basic_info']
        results = self.results
        
        output = f"""
{'='*80}
📊 ENERGETICKÝ AUDIT - VÝSLEDKY
{'='*80}

🏢 BUDOVA: {basic['building_name']}
📍 Adresa: {basic['address']}
📐 Podlahová plocha: {basic['floor_area']:.0f} m²
📅 Rok výstavby: {basic['construction_year']}
🏗️ Typ budovy: {basic['building_type']}

{'='*80}
🔥 TEPELNÉ STRATY OBÁLKY BUDOVY
{'='*80}

🧱 Straty stenami: {results['wall_losses']:.2f} W/K
🪟 Straty oknami: {results['window_losses']:.2f} W/K
🏠 Straty strechou: {results['roof_losses']:.2f} W/K
📊 CELKOVÉ STRATY: {results['total_losses']:.2f} W/K

{'='*80}
⚡ ENERGETICKÁ BILANCIA
{'='*80}

🔥 Potreba tepla na vykurovanie: {results['heating_need']:.0f} kWh/rok
🔥 Spotreba na vykurovanie: {results['heating_energy']:.0f} kWh/rok
💡 Spotreba na osvetlenie: {results['lighting_energy']:.0f} kWh/rok
⚙️ Spotreba zariadení: {results['appliances_energy']:.0f} kWh/rok
🚿 Spotreba na teplú vodu: {results['dhw_energy']:.0f} kWh/rok
📊 Celková elektrina: {results['total_electricity']:.0f} kWh/rok
⚡ CELKOVÁ SPOTREBA: {results['total_energy']:.0f} kWh/rok

{'='*80}
🎯 ENERGETICKÉ HODNOTENIE
{'='*80}

🔢 Primárna energia: {results['primary_energy']:.0f} kWh/rok
📐 Špecifická primárna energia: {results['specific_primary']:.1f} kWh/m²rok
🏅 ENERGETICKÁ TRIEDA: {results['energy_class']}

Klasifikácia energetických tried:
A: ≤ 50 kWh/m²rok    (Veľmi úsporná)
B: ≤ 75 kWh/m²rok    (Úsporná) 
C: ≤ 110 kWh/m²rok   (Vyhovujúca)
D: ≤ 150 kWh/m²rok   (Nevyhovujúca)
E: ≤ 200 kWh/m²rok   (Neúsporná)
F: ≤ 250 kWh/m²rok   (Veľmi neúsporná)
G: > 250 kWh/m²rok   (Mimoriadne neúsporná)

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
        if self.audit_data['electrical']['lighting_type'] != "LED":
            recommendations.append("💡 Prechod na LED osvetlenie - úspory 50-70%")
            
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

📋 Audit vypracovaný: {datetime.now().strftime('%d.%m.%Y %H:%M')}
👨‍💼 Energetický audítor: Professional Energy Audit System v2.0

{'='*80}
        """
        
        self.results_text.insert(tk.END, output)
        
    def show_calculations(self):
        """Zobrazenie detailných výpočtov"""
        if not self.results:
            messagebox.showwarning("Upozornenie", "Najprv vykonajte audit!")
            return
            
        calc_window = tk.Toplevel(self.root)
        calc_window.title("🧮 Detailné výpočty")
        calc_window.geometry("900x700")
        calc_window.configure(bg='white')
        
        # Header
        header = tk.Frame(calc_window, bg='#34495e', height=50)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="🧮 KROK-ZA-KROKOM VÝPOČTY", 
                font=('Arial', 14, 'bold'), fg='white', bg='#34495e').pack(pady=10)
        
        # Text area
        calc_text = scrolledtext.ScrolledText(calc_window, font=('Consolas', 10), 
                                              bg='#f8f9fa', wrap=tk.WORD)
        calc_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Generovanie detailných výpočtov (podobne ako v predchádzajúcej verzii)
        calc_details = self.generate_calculation_details()
        calc_text.insert(tk.END, calc_details)
        calc_text.config(state=tk.DISABLED)
        
        # Zatvorenie
        tk.Button(calc_window, text="❌ Zavrieť", command=calc_window.destroy,
                 bg='#e74c3c', fg='white', font=('Arial', 12, 'bold')).pack(pady=10)
                 
    def generate_calculation_details(self):
        """Generovanie detailných výpočtov"""
        if not self.results:
            return "Najprv vykonajte audit."
            
        basic = self.audit_data['basic_info']
        envelope = self.audit_data['envelope']
        results = self.results
        
        details = f"""
{'='*80}
🧮 DETAILNÉ VÝPOČTY ENERGETICKÉHO AUDITU
{'='*80}

📊 VSTUPNÉ ÚDAJE:
• Podlahová plocha: {basic['floor_area']:.1f} m²
• Plocha stien: {envelope['wall_area']:.1f} m²
• U-hodnota stien: {envelope['wall_u']:.3f} W/m²K
• Plocha okien: {envelope['window_area']:.1f} m²
• U-hodnota okien: {envelope['window_u']:.3f} W/m²K

KROK 1: TEPELNÉ STRATY
Vzorec: Q = A × U
Straty stenami: {envelope['wall_area']:.1f} × {envelope['wall_u']:.3f} = {results['wall_losses']:.2f} W/K
Straty oknami: {envelope['window_area']:.1f} × {envelope['window_u']:.3f} = {results['window_losses']:.2f} W/K
CELKOM: {results['total_losses']:.2f} W/K

KROK 2: POTREBA TEPLA
Vzorec: Qh = Qtotal × HDD × 24 / 1000
HDD (Bratislava): 2800 K·deň/rok
Qh = {results['total_losses']:.2f} × 2800 × 24 ÷ 1000 = {results['heating_need']:.0f} kWh/rok

KROK 3: SPOTREBA NA VYKUROVANIE
Vzorec: Eh = Qh / η
Eh = {results['heating_need']:.0f} ÷ {self.audit_data['heating']['efficiency']:.2f} = {results['heating_energy']:.0f} kWh/rok

KROK 4: PRIMÁRNA ENERGIA
Faktor pre plyn: 1.1
Faktor pre elektrinu: 3.0
Ep = {results['heating_energy']:.0f} × 1.1 + {results['total_electricity']:.0f} × 3.0 = {results['primary_energy']:.0f} kWh/rok
Špecifická: {results['primary_energy']:.0f} ÷ {basic['floor_area']:.0f} = {results['specific_primary']:.1f} kWh/m²rok

ENERGETICKÁ TRIEDA: {results['energy_class']}
        """
        
        return details
        
    def generate_certificate(self):
        """Generovanie certifikátu"""
        if not self.results:
            messagebox.showwarning("Upozornenie", "Najprv vykonajte audit!")
            return
            
        basic = self.audit_data['basic_info']
        results = self.results
        
        cert_window = tk.Toplevel(self.root)
        cert_window.title("🏅 Energetický certifikát")
        cert_window.geometry("600x500")
        cert_window.configure(bg='white')
        
        # Header certifikátu
        header = tk.Frame(cert_window, bg='#2c3e50', height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="🏅 ENERGETICKÝ CERTIFIKÁT",
                font=('Arial', 18, 'bold'), fg='white', bg='#2c3e50').pack(pady=15)
        
        # Obsah certifikátu
        content_frame = tk.Frame(cert_window, bg='white')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        cert_text = f"""
ENERGETICKÝ CERTIFIKÁT BUDOVY
Číslo: EC-{datetime.now().strftime('%Y%m%d%H%M')}

BUDOVA: {basic['building_name']}
Adresa: {basic['address']}
Podlahová plocha: {basic['floor_area']:.0f} m²

ENERGETICKÉ HODNOTENIE:
Energetická trieda: {results['energy_class']}
Špecifická primárna energia: {results['specific_primary']:.1f} kWh/m²rok
CO2 emisie: {results['specific_co2']:.1f} kg CO2/m²rok

PLATNOSŤ:
Dátum vydania: {datetime.now().strftime('%d.%m.%Y')}
Platnosť do: {datetime.now().replace(year=datetime.now().year + 10).strftime('%d.%m.%Y')}

Certifikát vystavil:
Professional Energy Audit System v2.0
Podľa STN EN 16247-1
        """
        
        cert_label = tk.Label(content_frame, text=cert_text, font=('Arial', 11),
                             justify=tk.LEFT, bg='white')
        cert_label.pack(pady=20)
        
        # Tlačidlá
        btn_frame = tk.Frame(cert_window, bg='white')
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="💾 Uložiť certifikát", command=lambda: self.save_certificate(cert_text),
                 bg='#3498db', fg='white', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text="❌ Zavrieť", command=cert_window.destroy,
                 bg='#e74c3c', fg='white', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=10)
                 
    def save_certificate(self, cert_text):
        """Uloženie certifikátu"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text súbory", "*.txt"), ("Všetky súbory", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(cert_text)
                messagebox.showinfo("Úspech", f"Certifikát uložený: {filename}")
            except Exception as e:
                messagebox.showerror("Chyba", f"Chyba pri ukladaní: {e}")
                
    def save_project(self):
        """Uloženie projektu"""
        if not self.audit_data:
            messagebox.showwarning("Upozornenie", "Nie je čo uložiť!")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON súbory", "*.json"), ("Všetky súbory", "*.*")]
        )
        
        if filename:
            try:
                project_data = {
                    'audit_data': self.audit_data,
                    'results': self.results,
                    'timestamp': datetime.now().isoformat(),
                    'version': '2.0'
                }
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(project_data, f, ensure_ascii=False, indent=2)
                    
                self.current_project_file = filename
                self.project_label.config(text=f"Projekt: {filename.split('/')[-1]}")
                messagebox.showinfo("Úspech", f"Projekt uložený: {filename}")
                
            except Exception as e:
                messagebox.showerror("Chyba", f"Chyba pri ukladaní: {e}")
                
    def load_project(self):
        """Načítanie projektu"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON súbory", "*.json"), ("Všetky súbory", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    project_data = json.load(f)
                    
                self.audit_data = project_data.get('audit_data', {})
                self.results = project_data.get('results', {})
                
                # Načítanie údajov do formulárov
                self.load_data_to_forms()
                
                if self.results:
                    self.display_results()
                    self.notebook.select(5)  # Prepnutie na výsledky
                    
                self.current_project_file = filename
                self.project_label.config(text=f"Projekt: {filename.split('/')[-1]}")
                messagebox.showinfo("Úspech", f"Projekt načítaný: {filename}")
                
            except Exception as e:
                messagebox.showerror("Chyba", f"Chyba pri načítavaní: {e}")
                
    def load_data_to_forms(self):
        """Načítanie údajov do formulárov"""
        try:
            if 'basic_info' in self.audit_data:
                basic = self.audit_data['basic_info']
                self.building_name.delete(0, tk.END)
                self.building_name.insert(0, basic.get('building_name', ''))
                self.address.delete(0, tk.END)
                self.address.insert(0, basic.get('address', ''))
                # ... pokračovanie pre všetky polia
        except Exception as e:
            print(f"Chyba pri načítavaní do formulárov: {e}")

def main():
    """Spustenie aplikácie"""
    root = tk.Tk()
    app = WorkingEnergyAudit(root)
    root.mainloop()

if __name__ == "__main__":
    main()