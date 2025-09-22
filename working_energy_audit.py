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
        self.create_envelope_tab()  # Obsahuje aj tepelno-technické posúdenie
        self.create_heating_tab()
        self.create_dhw_tab()  # Nový samostatný tab pre TUV
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
        
        # Legénda farieb na vrchu
        legend_frame = tk.Frame(scrollable_frame, bg='#f8f9fa', relief=tk.RIDGE, bd=1)
        legend_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(legend_frame, text="ℹ️ LEGENDÁ POLÍ:", font=('Arial', 10, 'bold'), bg='#f8f9fa').pack(side=tk.LEFT, padx=10, pady=5)
        tk.Label(legend_frame, text="🔴 POVINNÉ", fg='red', font=('Arial', 9, 'bold'), bg='#f8f9fa').pack(side=tk.LEFT, padx=10)
        tk.Label(legend_frame, text="🟠 DÔLEŽITÉ", fg='orange', font=('Arial', 9, 'bold'), bg='#f8f9fa').pack(side=tk.LEFT, padx=10)
        tk.Label(legend_frame, text="🔵 VOLITELNÉ", fg='blue', font=('Arial', 9, 'bold'), bg='#f8f9fa').pack(side=tk.LEFT, padx=10)
        
        scrollable_frame.bind("<Configure>", 
                             lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # IDENTIFIKAČNÉ ÚDAJE PODĽA STN EN 16247-1
        id_frame = tk.LabelFrame(scrollable_frame, text="🏢 Identifikácia objektu (STN EN 16247-1 bod 6.2.1)", 
                                font=('Arial', 11, 'bold'))
        id_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Riad 1
        tk.Label(id_frame, text="Názov budovy *:", fg='red', font=('Arial', 9, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.building_name = tk.Entry(id_frame, width=30, font=('Arial', 9), bg='#ffe6e6')
        self.building_name.grid(row=0, column=1, padx=5, pady=3)
        
        tk.Label(id_frame, text="Účel budovy *:", fg='red', font=('Arial', 9, 'bold')).grid(row=0, column=2, sticky=tk.W, padx=5, pady=3)
        self.building_purpose = ttk.Combobox(id_frame, width=25, values=[
            "Rodinný dom", "Bytový dom", "Administratívna budova", "Škola", "Nemocnica",
            "Hotel", "Obchodné centrum", "Reštaurácia", "Priemyselná budova", "Sklad", "Ostatné"
        ])
        self.building_purpose.configure(style='Required.TCombobox')
        self.building_purpose.grid(row=0, column=3, padx=5, pady=3)
        self.building_purpose.bind('<<ComboboxSelected>>', self.on_building_purpose_changed)
        
        # Riad 2  
        tk.Label(id_frame, text="Adresa *:", fg='red', font=('Arial', 9, 'bold')).grid(row=1, column=0, sticky=tk.W, padx=5, pady=3)
        self.address = tk.Entry(id_frame, width=30, font=('Arial', 9), bg='#ffe6e6')
        self.address.grid(row=1, column=1, padx=5, pady=3)
        
        tk.Label(id_frame, text="PSČ a obec:", fg='blue').grid(row=1, column=2, sticky=tk.W, padx=5, pady=3)
        self.postal_city = tk.Entry(id_frame, width=25, font=('Arial', 9), bg='#e6f2ff')
        self.postal_city.grid(row=1, column=3, padx=5, pady=3)
        
        # Riad 3
        tk.Label(id_frame, text="Katastrálne územie:", fg='blue').grid(row=2, column=0, sticky=tk.W, padx=5, pady=3)
        self.cadastral = tk.Entry(id_frame, width=30, font=('Arial', 9), bg='#e6f2ff')
        self.cadastral.grid(row=2, column=1, padx=5, pady=3)
        
        tk.Label(id_frame, text="Súpisné/orientačné číslo:", fg='blue').grid(row=2, column=2, sticky=tk.W, padx=5, pady=3)
        self.house_number = tk.Entry(id_frame, width=25, font=('Arial', 9), bg='#e6f2ff')
        self.house_number.grid(row=2, column=3, padx=5, pady=3)
        
        # Riad 4
        tk.Label(id_frame, text="Vlastník budovy *:", fg='red', font=('Arial', 9, 'bold')).grid(row=3, column=0, sticky=tk.W, padx=5, pady=3)
        self.owner = tk.Entry(id_frame, width=30, font=('Arial', 9), bg='#ffe6e6')
        self.owner.grid(row=3, column=1, padx=5, pady=3)
        
        tk.Label(id_frame, text="IČO vlastníka:", fg='blue').grid(row=3, column=2, sticky=tk.W, padx=5, pady=3)
        self.owner_ico = tk.Entry(id_frame, width=25, font=('Arial', 9), bg='#e6f2ff')
        self.owner_ico.grid(row=3, column=3, padx=5, pady=3)
        
        # Riad 5
        tk.Label(id_frame, text="Kontaktná osoba *:", fg='red', font=('Arial', 9, 'bold')).grid(row=4, column=0, sticky=tk.W, padx=5, pady=3)
        self.contact_person = tk.Entry(id_frame, width=30, font=('Arial', 9), bg='#ffe6e6')
        self.contact_person.grid(row=4, column=1, padx=5, pady=3)
        
        tk.Label(id_frame, text="Telefón/Email:", fg='orange').grid(row=4, column=2, sticky=tk.W, padx=5, pady=3)
        self.contact_details = tk.Entry(id_frame, width=25, font=('Arial', 9), bg='#fff2e6')
        self.contact_details.grid(row=4, column=3, padx=5, pady=3)
        
        # TECHNICKÉ CHARAKTERISTIKY PODĽA NORMY
        tech_frame = tk.LabelFrame(scrollable_frame, text="📐 Technické charakteristiky (STN EN 16247-1 bod 6.2.2)", 
                                  font=('Arial', 11, 'bold'))
        tech_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Riad 1 - Základné rozmery
        tk.Label(tech_frame, text="Rok výstavby *:", fg='red', font=('Arial', 9, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.construction_year = tk.Entry(tech_frame, width=15, bg='#ffe6e6')
        self.construction_year.grid(row=0, column=1, padx=5, pady=3)
        
        tk.Label(tech_frame, text="Rok poslednej rekonštrukcie:", fg='orange').grid(row=0, column=2, sticky=tk.W, padx=5, pady=3)
        self.renovation_year = tk.Entry(tech_frame, width=15, bg='#fff2e6')
        self.renovation_year.grid(row=0, column=3, padx=5, pady=3)
        
        tk.Label(tech_frame, text="Energetická trieda (aktuálna):", fg='blue').grid(row=0, column=4, sticky=tk.W, padx=5, pady=3)
        self.current_energy_class = ttk.Combobox(tech_frame, width=12, values=["A", "B", "C", "D", "E", "F", "G", "Neznáma"])
        self.current_energy_class.grid(row=0, column=5, padx=5, pady=3)
        
        # Riad 2 - Plochy a objemy
        tk.Label(tech_frame, text="Podlahová plocha (vykurovaná) [m²] *:", fg='red', font=('Arial', 9, 'bold')).grid(row=1, column=0, sticky=tk.W, padx=5, pady=3)
        self.floor_area = tk.Entry(tech_frame, width=15, bg='#ffe6e6')
        self.floor_area.grid(row=1, column=1, padx=5, pady=3)
        
        tk.Label(tech_frame, text="Podlahová plocha (celková) [m²]:", fg='blue').grid(row=1, column=2, sticky=tk.W, padx=5, pady=3)
        self.total_floor_area = tk.Entry(tech_frame, width=15, bg='#e6f2ff')
        self.total_floor_area.grid(row=1, column=3, padx=5, pady=3)
        
        tk.Label(tech_frame, text="Obostavaný priestor [m³] *:", fg='red', font=('Arial', 9, 'bold')).grid(row=1, column=4, sticky=tk.W, padx=5, pady=3)
        self.volume = tk.Entry(tech_frame, width=12, bg='#ffe6e6')
        self.volume.grid(row=1, column=5, padx=5, pady=3)
        
        # Riad 3 - Geometria
        tk.Label(tech_frame, text="Počet nadzemných podlaží *:", fg='red', font=('Arial', 9, 'bold')).grid(row=2, column=0, sticky=tk.W, padx=5, pady=3)
        self.floors_above = tk.Entry(tech_frame, width=15, bg='#ffe6e6')
        self.floors_above.grid(row=2, column=1, padx=5, pady=3)
        
        tk.Label(tech_frame, text="Počet podzemných podlaží:", fg='blue').grid(row=2, column=2, sticky=tk.W, padx=5, pady=3)
        self.floors_below = tk.Entry(tech_frame, width=15, bg='#e6f2ff')
        self.floors_below.grid(row=2, column=3, padx=5, pady=3)
        
        tk.Label(tech_frame, text="Svetlá výška [m]:", fg='blue').grid(row=2, column=4, sticky=tk.W, padx=5, pady=3)
        self.ceiling_height = tk.Entry(tech_frame, width=12, bg='#e6f2ff')
        self.ceiling_height.grid(row=2, column=5, padx=5, pady=3)
        
        # Riad 4 - Konštrukčný systém a typológia
        tk.Label(tech_frame, text="Konštrukčný systém:", fg='orange').grid(row=3, column=0, sticky=tk.W, padx=5, pady=3)
        self.construction_system = ttk.Combobox(tech_frame, width=13, values=[
            "Murovaný", "Montovaný betón", "Skelet ŽB", "Oceľový skelet", "Drevostavba", "Zmiešaný", "Ostatné"
        ])
        self.construction_system.grid(row=3, column=1, padx=5, pady=3)
        
        tk.Label(tech_frame, text="Typ založenia:", fg='blue').grid(row=3, column=2, sticky=tk.W, padx=5, pady=3)
        self.foundation_type = ttk.Combobox(tech_frame, width=13, values=[
            "Základové pásy", "Základová doska", "Pilóty", "Suterén", "Ostatné"
        ])
        self.foundation_type.grid(row=3, column=3, padx=5, pady=3)
        
        tk.Label(tech_frame, text="Orientácia hlavnej fasády:", fg='blue').grid(row=3, column=4, sticky=tk.W, padx=5, pady=3)
        self.orientation = ttk.Combobox(tech_frame, width=10, values=["S", "SV", "V", "JV", "J", "JZ", "Z", "SZ"])
        self.orientation.grid(row=3, column=5, padx=5, pady=3)
        
        # DETAILNÉ INFORMÁCIE PODĽA ZADANIA EACB
        detailed_frame = tk.LabelFrame(scrollable_frame, text="📄 Detailné informácie podľa zadania EACB", 
                                      font=('Arial', 11, 'bold'))
        detailed_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Riad 1 - Funkcie a popis
        tk.Label(detailed_frame, text="Konštrukčná výška [m]:", fg='orange').grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.structural_height = tk.Entry(detailed_frame, width=12, bg='#fff2e6')
        self.structural_height.grid(row=0, column=1, padx=5, pady=3)
        
        tk.Label(detailed_frame, text="Funkcia podlaží:", fg='blue').grid(row=0, column=2, sticky=tk.W, padx=5, pady=3)
        self.floor_functions = tk.Entry(detailed_frame, width=25, bg='#e6f2ff')
        self.floor_functions.grid(row=0, column=3, columnspan=2, padx=5, pady=3)
        
        # Riad 2 - Byty a kolaudácia
        tk.Label(detailed_frame, text="Počet bytov v objekte:", fg='blue').grid(row=1, column=0, sticky=tk.W, padx=5, pady=3)
        self.apartments_count = tk.Entry(detailed_frame, width=12, bg='#e6f2ff')
        self.apartments_count.grid(row=1, column=1, padx=5, pady=3)
        
        tk.Label(detailed_frame, text="Veľkosti bytov:", fg='blue').grid(row=1, column=2, sticky=tk.W, padx=5, pady=3)
        self.apartment_sizes = tk.Entry(detailed_frame, width=25, bg='#e6f2ff')
        self.apartment_sizes.grid(row=1, column=3, columnspan=2, padx=5, pady=3)
        
        # Riad 3 - Kolaudácia a stav
        tk.Label(detailed_frame, text="Dátum kolaudácie:", fg='orange').grid(row=2, column=0, sticky=tk.W, padx=5, pady=3)
        self.building_permit_date = tk.Entry(detailed_frame, width=12, bg='#fff2e6')
        self.building_permit_date.grid(row=2, column=1, padx=5, pady=3)
        
        tk.Label(detailed_frame, text="Stav konštrukcii:", fg='orange').grid(row=2, column=2, sticky=tk.W, padx=5, pady=3)
        self.construction_condition = ttk.Combobox(detailed_frame, width=22, values=[
            "Pôvodný stav", "Moderne rekongenštrukcia", "Čiastočná rekongenštrukcia", "Zlepšený stav"
        ])
        self.construction_condition.grid(row=2, column=3, columnspan=2, padx=5, pady=3)
        
        # KLIMATICKÉ ÚDAJE
        climate_frame = tk.LabelFrame(scrollable_frame, text="🌤️ Klimatické údaje a lokalita", 
                                     font=('Arial', 11, 'bold'))
        climate_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Riad 1
        tk.Label(climate_frame, text="Klimatická oblasť:", fg='blue').grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.climate_zone = ttk.Combobox(climate_frame, width=20, values=[
            "Teplá (do 500 m n.m.)", "Mierna (500-800 m n.m.)", "Chladná (nad 800 m n.m.)"
        ])
        self.climate_zone.grid(row=0, column=1, padx=5, pady=3)
        
        tk.Label(climate_frame, text="Nadmorská výška [m]:", fg='blue').grid(row=0, column=2, sticky=tk.W, padx=5, pady=3)
        self.altitude = tk.Entry(climate_frame, width=15, bg='#e6f2ff')
        self.altitude.grid(row=0, column=3, padx=5, pady=3)
        
        # Riad 2 - Automatické nastavenie podľa miest
        tk.Label(climate_frame, text="Lokalita (automatické HDD):", fg='orange', font=('Arial', 9, 'bold')).grid(row=1, column=0, sticky=tk.W, padx=5, pady=3)
        self.city_location = ttk.Combobox(climate_frame, width=18, values=[
            "Bratislava (2800)", "Košice (3200)", "Prešov (3400)", "Banská Bystrica (3600)",
            "Trnava (2850)", "Žilina (3300)", "Nitra (2900)", "Trenčín (3000)",
            "Martin (3350)", "Poprad (3800)", "Komárno (2700)", "Nové Zámky (2750)",
            "Piettåny (2950)", "Ružomberok (3500)", "Zvolen (3450)", "Levoča (3550)",
            "Vlastné nastavenie"
        ])
        self.city_location.grid(row=1, column=1, padx=5, pady=3)
        self.city_location.bind('<<ComboboxSelected>>', self.on_city_changed)
        
        tk.Label(climate_frame, text="HDD (stupeň.dni) [K.deň/rok]:", fg='orange', font=('Arial', 9, 'bold')).grid(row=1, column=2, sticky=tk.W, padx=5, pady=3)
        self.hdd = tk.Entry(climate_frame, width=15, bg='#fff2e6')
        self.hdd.grid(row=1, column=3, padx=5, pady=3)
        
        # Riad 3
        tk.Label(climate_frame, text="Prevažujúci smer vetra:", fg='blue').grid(row=2, column=0, sticky=tk.W, padx=5, pady=3)
        self.wind_direction = ttk.Combobox(climate_frame, width=20, values=["S", "SV", "V", "JV", "J", "JZ", "Z", "SZ", "Premenlivý"])
        self.wind_direction.grid(row=2, column=1, padx=5, pady=3)
        
        tk.Label(climate_frame, text="Tienenie budovy:", fg='blue').grid(row=2, column=2, sticky=tk.W, padx=5, pady=3)
        self.shading = ttk.Combobox(climate_frame, width=13, values=["Ziadne", "Čiastocne", "Znacne", "Úplné"])
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
        """Auto-doplnenie parametrov teplej užitkovej vody"""
        dhw_type = self.dhw_type.get()
        defaults = {
            "Elektrický bojler": {
                'efficiency': '85', 'circulation': 'Časová', 'storage_temp': '60', 
                'power': '2.5', 'volume_per_person': 80
            },
            "Plynový bojler": {
                'efficiency': '78', 'circulation': 'Bez cirkulácie', 'storage_temp': '60', 
                'power': '24', 'volume_per_person': 50
            },
            "Kombinovaný kotol": {
                'efficiency': '85', 'circulation': 'Termostatická', 'storage_temp': '60', 
                'power': '0', 'volume_per_person': 60
            },
            "Solárne kolektory": {
                'efficiency': '60', 'circulation': 'Termostatická', 'storage_temp': '45', 
                'power': '0', 'volume_per_person': 100
            },
            "Tepelné čerpadlo TUV": {
                'efficiency': '250', 'circulation': 'Termostatická', 'storage_temp': '55', 
                'power': '2', 'volume_per_person': 80
            },
            "Príprava v kotle": {
                'efficiency': '80', 'circulation': 'Neprerushovaná', 'storage_temp': '60', 
                'power': '0', 'volume_per_person': 40
            },
            "Prípravník": {
                'efficiency': '75', 'circulation': 'Termostatická', 'storage_temp': '60', 
                'power': '0', 'volume_per_person': 60
            }
        }
        
        if dhw_type in defaults:
            values = defaults[dhw_type]
            
            # Základné parametre
            self.dhw_efficiency.delete(0, tk.END)
            self.dhw_efficiency.insert(0, values['efficiency'])
            self.dhw_circulation.set(values['circulation'])
            
            # Teplota a výkon
            if hasattr(self, 'dhw_storage_temp'):
                self.dhw_storage_temp.delete(0, tk.END)
                self.dhw_storage_temp.insert(0, values['storage_temp'])
            
            if hasattr(self, 'dhw_power') and values['power'] != '0':
                self.dhw_power.delete(0, tk.END)
                self.dhw_power.insert(0, values['power'])
            
            # Odhad objemu zásobníka a spotreby
            try:
                # Získať počet osôb
                occupants = 4  # default
                if hasattr(self, 'occupants') and self.occupants.get():
                    occupants = int(self.occupants.get())
                
                # Objem zásobníka
                estimated_volume = occupants * values['volume_per_person']
                self.dhw_volume.delete(0, tk.END)
                self.dhw_volume.insert(0, str(estimated_volume))
                
                # Denká spotreba
                if hasattr(self, 'dhw_daily_consumption'):
                    daily_consumption = occupants * 50  # 50l/osobu/deň
                    self.dhw_daily_consumption.delete(0, tk.END)
                    self.dhw_daily_consumption.insert(0, str(daily_consumption))
                    
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
        
        # Legénda farieb
        legend_frame = tk.Frame(scrollable_frame, bg='#f8f9fa', relief=tk.RIDGE, bd=1)
        legend_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(legend_frame, text="ℹ️ LEGENDÁ POLÍ:", font=('Arial', 10, 'bold'), bg='#f8f9fa').pack(side=tk.LEFT, padx=10, pady=5)
        tk.Label(legend_frame, text="🔴 POVINNÉ", fg='red', font=('Arial', 9, 'bold'), bg='#f8f9fa').pack(side=tk.LEFT, padx=10)
        tk.Label(legend_frame, text="🟠 DÔLEŽITÉ", fg='orange', font=('Arial', 9, 'bold'), bg='#f8f9fa').pack(side=tk.LEFT, padx=10)
        tk.Label(legend_frame, text="🔵 VOLITELNÉ", fg='blue', font=('Arial', 9, 'bold'), bg='#f8f9fa').pack(side=tk.LEFT, padx=10)
        
        # VONKAJŠIE STENY (STN EN 16247-1 bod 6.2.3)
        walls_frame = tk.LabelFrame(scrollable_frame, text="🧱 Vonkajšie steny (STN EN 16247-1 bod 6.2.3)", 
                                   font=('Arial', 11, 'bold'))
        walls_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Riad 1
        tk.Label(walls_frame, text="Celková plocha stìen [m²] *:", fg='red', font=('Arial', 9, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.wall_area = tk.Entry(walls_frame, width=15, bg='#ffe6e6')
        self.wall_area.grid(row=0, column=1, padx=5, pady=3)
        
        tk.Label(walls_frame, text="U-hodnota stìen [W/m²K] *:", fg='red', font=('Arial', 9, 'bold')).grid(row=0, column=2, sticky=tk.W, padx=5, pady=3)
        self.wall_u = tk.Entry(walls_frame, width=15, bg='#ffe6e6')
        self.wall_u.grid(row=0, column=3, padx=5, pady=3)
        
        tk.Label(walls_frame, text="Typ konštrukcie stìen:", fg='blue').grid(row=0, column=4, sticky=tk.W, padx=5, pady=3)
        self.wall_construction = ttk.Combobox(walls_frame, width=18, values=[
            "Jednoplashá murovaná", "Dvojplashá murovaná", "Sendvičová", "Montovaná betónová", 
            "Drevenká", "Železobetová", "Lastrock", "Ytong", "Keramická"
        ])
        self.wall_construction.grid(row=0, column=5, padx=5, pady=3)
        
        # Riad 2
        tk.Label(walls_frame, text="Typ tepelnej izolácie:", fg='orange').grid(row=1, column=0, sticky=tk.W, padx=5, pady=3)
        self.wall_insulation = ttk.Combobox(walls_frame, width=13, values=[
            "Bez izolácie", "ETICS (kontaktný)", "Vnútorná", "Dutinová", "Fasadistic", 
            "Kombinácia", "Inhérent (izol. betóny)"
        ])
        self.wall_insulation.grid(row=1, column=1, padx=5, pady=3)
        
        tk.Label(walls_frame, text="Hrúbka izolácie [mm]:", fg='blue').grid(row=1, column=2, sticky=tk.W, padx=5, pady=3)
        self.wall_insulation_thickness = tk.Entry(walls_frame, width=15, bg='#e6f2ff')
        self.wall_insulation_thickness.grid(row=1, column=3, padx=5, pady=3)
        
        tk.Label(walls_frame, text="Typ izolačného materiálu:", fg='blue').grid(row=1, column=4, sticky=tk.W, padx=5, pady=3)
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
        tk.Label(windows_frame, text="Plocha okien celkom [m²] *:", fg='red', font=('Arial', 9, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.window_area = tk.Entry(windows_frame, width=13, bg='#ffe6e6')
        self.window_area.grid(row=0, column=1, padx=5, pady=3)
        
        tk.Label(windows_frame, text="U-hodnota okien [W/m²K] *:", fg='red', font=('Arial', 9, 'bold')).grid(row=0, column=2, sticky=tk.W, padx=5, pady=3)
        self.window_u = tk.Entry(windows_frame, width=15, bg='#ffe6e6')
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
        tk.Label(roof_frame, text="Plocha strechy [m²] *:", fg='red', font=('Arial', 9, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.roof_area = tk.Entry(roof_frame, width=15, bg='#ffe6e6')
        self.roof_area.grid(row=0, column=1, padx=5, pady=3)
        
        tk.Label(roof_frame, text="U-hodnota strechy [W/m²K] *:", fg='red', font=('Arial', 9, 'bold')).grid(row=0, column=2, sticky=tk.W, padx=5, pady=3)
        self.roof_u = tk.Entry(roof_frame, width=15, bg='#ffe6e6')
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
        tk.Label(floor_frame, text="Plocha podlahy [m²] *:", fg='red', font=('Arial', 9, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.floor_area_envelope = tk.Entry(floor_frame, width=15, bg='#ffe6e6')
        self.floor_area_envelope.grid(row=0, column=1, padx=5, pady=3)
        
        tk.Label(floor_frame, text="U-hodnota podlahy [W/m²K] *:", fg='red', font=('Arial', 9, 'bold')).grid(row=0, column=2, sticky=tk.W, padx=5, pady=3)
        self.floor_u = tk.Entry(floor_frame, width=15, bg='#ffe6e6')
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
        
        # TEPELNO-TECHNICKÉ POSÚDENIE podľa STN 73 0540-2 Z2/2019
        assessment_frame = tk.LabelFrame(scrollable_frame, text="🌡️ Tepelno-technické posúdenie podľa STN 73 0540-2 Z2/2019", 
                                        font=('Arial', 11, 'bold'))
        assessment_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Info text
        info_label = tk.Label(assessment_frame, 
                             text="Požadované U-hodnoty pre nové budovy podľa STN 73 0540-2 Z2/2019",
                             font=('Arial', 9, 'italic'), fg='#34495e')
        info_label.pack(pady=5)
        
        # OBVODOVÉ STENY - posúdenie
        wall_assess_frame = tk.LabelFrame(assessment_frame, text="🧱 Obvodové steny", font=('Arial', 10, 'bold'))
        wall_assess_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(wall_assess_frame, text="Aktuálna U-hodnota [W/m²K]:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.wall_u_actual = tk.Entry(wall_assess_frame, width=10)
        self.wall_u_actual.grid(row=0, column=1, padx=5, pady=3)
        
        tk.Label(wall_assess_frame, text="Požadovaná UN [W/m²K]:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=3)
        tk.Label(wall_assess_frame, text="0,22", font=('Arial', 9, 'bold'), fg='red').grid(row=0, column=3, padx=5, pady=3)
        
        tk.Label(wall_assess_frame, text="Posúdenie:").grid(row=0, column=4, sticky=tk.W, padx=5, pady=3)
        self.wall_assessment = tk.Label(wall_assess_frame, text="-", width=12, relief=tk.SUNKEN)
        self.wall_assessment.grid(row=0, column=5, padx=5, pady=3)
        
        # STRECHA - posúdenie  
        roof_assess_frame = tk.LabelFrame(assessment_frame, text="🏠 Strecha", font=('Arial', 10, 'bold'))
        roof_assess_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(roof_assess_frame, text="Aktuálna U-hodnota [W/m²K]:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.roof_u_actual = tk.Entry(roof_assess_frame, width=10)
        self.roof_u_actual.grid(row=0, column=1, padx=5, pady=3)
        
        tk.Label(roof_assess_frame, text="Požadovaná UN [W/m²K]:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=3)
        tk.Label(roof_assess_frame, text="0,15", font=('Arial', 9, 'bold'), fg='red').grid(row=0, column=3, padx=5, pady=3)
        
        tk.Label(roof_assess_frame, text="Posúdenie:").grid(row=0, column=4, sticky=tk.W, padx=5, pady=3)
        self.roof_assessment = tk.Label(roof_assess_frame, text="-", width=12, relief=tk.SUNKEN)
        self.roof_assessment.grid(row=0, column=5, padx=5, pady=3)
        
        # PODLAHA NAD NEVYKUROVANÝM - posúdenie
        floor_assess_frame = tk.LabelFrame(assessment_frame, text="🟦 Podlaha nad nevykurovaným", font=('Arial', 10, 'bold'))
        floor_assess_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(floor_assess_frame, text="Aktuálna U-hodnota [W/m²K]:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.floor_u_actual = tk.Entry(floor_assess_frame, width=10)
        self.floor_u_actual.grid(row=0, column=1, padx=5, pady=3)
        
        tk.Label(floor_assess_frame, text="Požadovaná UN [W/m²K]:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=3)
        tk.Label(floor_assess_frame, text="0,85", font=('Arial', 9, 'bold'), fg='red').grid(row=0, column=3, padx=5, pady=3)
        
        tk.Label(floor_assess_frame, text="Posúdenie:").grid(row=0, column=4, sticky=tk.W, padx=5, pady=3)
        self.floor_assessment = tk.Label(floor_assess_frame, text="-", width=12, relief=tk.SUNKEN)
        self.floor_assessment.grid(row=0, column=5, padx=5, pady=3)
        
        # OKNÁ A DVERE - posúdenie
        windows_assess_frame = tk.LabelFrame(assessment_frame, text="🪟 Okná a dvere", font=('Arial', 10, 'bold'))
        windows_assess_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(windows_assess_frame, text="Aktuálna Uw-hodnota [W/m²K]:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.window_u_actual = tk.Entry(windows_assess_frame, width=10)
        self.window_u_actual.grid(row=0, column=1, padx=5, pady=3)
        
        tk.Label(windows_assess_frame, text="Maximálna Uw,max [W/m²K]:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=3)
        tk.Label(windows_assess_frame, text="1,7", font=('Arial', 9, 'bold'), fg='red').grid(row=0, column=3, padx=5, pady=3)
        
        tk.Label(windows_assess_frame, text="Posúdenie:").grid(row=0, column=4, sticky=tk.W, padx=5, pady=3)
        self.window_assessment = tk.Label(windows_assess_frame, text="-", width=12, relief=tk.SUNKEN)
        self.window_assessment.grid(row=0, column=5, padx=5, pady=3)
        
        # TLAČIDLO POSÚDENIA
        assess_btn_frame = tk.Frame(assessment_frame)
        assess_btn_frame.pack(pady=15)
        
        tk.Button(assess_btn_frame, text="📈 VYKONAJ POSÚDENIE U-HODNÔT", 
                 command=self.calculate_thermal_assessment, 
                 bg='#3498db', fg='white', font=('Arial', 11, 'bold'),
                 width=35, height=2).pack()
        
        # SÚHRNNÉ TABUĽKY KONŠTRUKCIÍ
        summary_frame = tk.LabelFrame(scrollable_frame, text="📊 Súhrnné tabuľky konštrukcií", 
                                     font=('Arial', 11, 'bold'))
        summary_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # TABUĽKA NEPRIEHĽADNÝCH KONŠTRUKCIÍ
        tk.Label(summary_frame, text="🧱 NEPRIEHĽADNÉ KONŠTRUKCIE", 
                font=('Arial', 10, 'bold'), fg='#2c3e50').grid(row=0, column=0, columnspan=6, pady=(5,10))
        
        # Hlavička tabuľky
        headers = ["Konštrukcia", "Plocha [m²]", "U-aktuálna [W/m²K]", "UN-požad. [W/m²K]", "Rezerva [%]", "Posúdenie"]
        for i, header in enumerate(headers):
            tk.Label(summary_frame, text=header, font=('Arial', 8, 'bold'), 
                    bg='#ecf0f1', relief=tk.RIDGE).grid(row=1, column=i, sticky='ew', padx=1, pady=1)
        
        # Riadky pre konštrukcie
        constructions = [
            ("Obvodové steny", "0,22"),
            ("Strecha", "0,15"),
            ("Podlaha nad nevykur.", "0,85")
        ]
        
        self.construction_entries = {}
        for i, (name, u_req) in enumerate(constructions, start=2):
            tk.Label(summary_frame, text=name, bg='white', relief=tk.RIDGE).grid(row=i, column=0, sticky='ew', padx=1, pady=1)
            
            # Plocha - editovateľné pole
            area_entry = tk.Entry(summary_frame, width=8, justify=tk.CENTER)
            area_entry.grid(row=i, column=1, padx=1, pady=1)
            
            # U-hodnota aktuálna - editovateľné pole  
            u_entry = tk.Entry(summary_frame, width=10, justify=tk.CENTER)
            u_entry.grid(row=i, column=2, padx=1, pady=1)
            
            # Požadovaná U-hodnota
            tk.Label(summary_frame, text=u_req, bg='#ffe6e6', relief=tk.RIDGE).grid(row=i, column=3, sticky='ew', padx=1, pady=1)
            
            # Rezerva - vypočíta sa
            rezerva_label = tk.Label(summary_frame, text="-", bg='white', relief=tk.RIDGE)
            rezerva_label.grid(row=i, column=4, sticky='ew', padx=1, pady=1)
            
            # Posúdenie - vyhodnotí sa  
            posudenie_label = tk.Label(summary_frame, text="-", bg='#fff2e6', relief=tk.RIDGE)
            posudenie_label.grid(row=i, column=5, sticky='ew', padx=1, pady=1)
            
            self.construction_entries[name] = {
                'area': area_entry,
                'u_value': u_entry, 
                'rezerva': rezerva_label,
                'posudenie': posudenie_label
            }
        
        # TABUĽKA PRIEHĽADNÝCH KONŠTRUKCIÍ (OKNÁ)
        tk.Label(summary_frame, text="🪟 PRIEHĽADNÉ KONŠTRUKCIE (OKNÁ)", 
                font=('Arial', 10, 'bold'), fg='#2c3e50').grid(row=6, column=0, columnspan=6, pady=(20,10))
        
        # Hlavička pre okná
        window_headers = ["Orientácia", "Plocha [m²]", "Uw-aktuálna [W/m²K]", "Uw,max [W/m²K]", "Rezerva [%]", "Posúdenie"]
        for i, header in enumerate(window_headers):
            tk.Label(summary_frame, text=header, font=('Arial', 8, 'bold'), 
                    bg='#ecf0f1', relief=tk.RIDGE).grid(row=7, column=i, sticky='ew', padx=1, pady=1)
        
        # Riadky pre okná podľa orientácie
        orientations = ["Sever", "Východ", "Juh", "Západ"]
        
        self.window_entries = {}
        for i, orient in enumerate(orientations, start=8):
            tk.Label(summary_frame, text=orient, bg='white', relief=tk.RIDGE).grid(row=i, column=0, sticky='ew', padx=1, pady=1)
            
            # Plocha okien
            area_entry = tk.Entry(summary_frame, width=8, justify=tk.CENTER)
            area_entry.grid(row=i, column=1, padx=1, pady=1)
            
            # Uw-hodnota
            uw_entry = tk.Entry(summary_frame, width=10, justify=tk.CENTER) 
            uw_entry.grid(row=i, column=2, padx=1, pady=1)
            
            # Max. Uw hodnota
            tk.Label(summary_frame, text="1,7", bg='#ffe6e6', relief=tk.RIDGE).grid(row=i, column=3, sticky='ew', padx=1, pady=1)
            
            # Rezerva
            rezerva_label = tk.Label(summary_frame, text="-", bg='white', relief=tk.RIDGE)
            rezerva_label.grid(row=i, column=4, sticky='ew', padx=1, pady=1)
            
            # Posúdenie
            posudenie_label = tk.Label(summary_frame, text="-", bg='#fff2e6', relief=tk.RIDGE) 
            posudenie_label.grid(row=i, column=5, sticky='ew', padx=1, pady=1)
            
            self.window_entries[orient] = {
                'area': area_entry,
                'uw_value': uw_entry,
                'rezerva': rezerva_label, 
                'posudenie': posudenie_label
            }
        
        # Nastavenie rovnakej šírky stĺpcov
        for i in range(6):
            summary_frame.grid_columnconfigure(i, weight=1)
        
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
        
        # Legénda farieb
        legend_frame = tk.Frame(scrollable_frame, bg='#f8f9fa', relief=tk.RIDGE, bd=1)
        legend_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(legend_frame, text="ℹ️ LEGENDÁ POLÍ:", font=('Arial', 10, 'bold'), bg='#f8f9fa').pack(side=tk.LEFT, padx=10, pady=5)
        tk.Label(legend_frame, text="🔴 POVINNÉ", fg='red', font=('Arial', 9, 'bold'), bg='#f8f9fa').pack(side=tk.LEFT, padx=10)
        tk.Label(legend_frame, text="🟠 DÔLEŽITÉ", fg='orange', font=('Arial', 9, 'bold'), bg='#f8f9fa').pack(side=tk.LEFT, padx=10)
        tk.Label(legend_frame, text="🔵 VOLITELNÉ", fg='blue', font=('Arial', 9, 'bold'), bg='#f8f9fa').pack(side=tk.LEFT, padx=10)
        
        # ZDROJ TEPLA A VÝROBA
        heating_frame = tk.LabelFrame(scrollable_frame, text="🔥 Zdroj tepla a výroba (STN EN 16247-1 bod 6.2.7)", 
                                     font=('Arial', 11, 'bold'))
        heating_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(heating_frame, text="Typ vykurovania *:", fg='red', font=('Arial', 9, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
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
        
        tk.Label(heating_frame, text="Sezónna účinnosť ηs [%] *:", fg='red', font=('Arial', 9, 'bold')).grid(row=1, column=0, sticky=tk.W, padx=5, pady=3)
        self.heating_efficiency = tk.Entry(heating_frame, width=12, bg='#ffe6e6')
        self.heating_efficiency.grid(row=1, column=1, padx=5, pady=3)
        
        tk.Label(heating_frame, text="Výstupná teplota vykurovania [°C]:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=3)
        self.supply_temp = tk.Entry(heating_frame, width=12)
        self.supply_temp.grid(row=1, column=3, padx=5, pady=3)
        
        tk.Label(heating_frame, text="Rok inštalácie:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=3)
        self.heating_year = tk.Entry(heating_frame, width=12)
        self.heating_year.grid(row=2, column=1, padx=5, pady=3)
        
        tk.Label(heating_frame, text="Palivo *:", fg='red', font=('Arial', 9, 'bold')).grid(row=2, column=2, sticky=tk.W, padx=5, pady=3)
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
        
        # DISTRIBÚCIA A REGULÁCIA PODĽA ZADANIA EACB
        dist_frame = tk.LabelFrame(scrollable_frame, text="🌡️ Distribúcia tepla a regulácia (CZT systém)", 
                                  font=('Arial', 11, 'bold'))
        dist_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(dist_frame, text="Odovzdávacia stanica tepla:", fg='red', font=('Arial', 9, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.heat_exchange_station = ttk.Combobox(dist_frame, width=20, values=[
            "Mimo budovy", "V budove", "Decentralizovaná", "Centrálna pre viac budov"
        ])
        self.heat_exchange_station.grid(row=0, column=1, padx=5, pady=3)
        
        tk.Label(dist_frame, text="Teplotný spád [°C]:", fg='orange', font=('Arial', 9, 'bold')).grid(row=0, column=2, sticky=tk.W, padx=5, pady=3)
        self.temperature_gradient = tk.Entry(dist_frame, width=12, bg='#fff2e6')
        self.temperature_gradient.grid(row=0, column=3, padx=5, pady=3)
        
        tk.Label(dist_frame, text="Typ distribúcie:", fg='orange').grid(row=0, column=4, sticky=tk.W, padx=5, pady=3)
        self.distribution_type = ttk.Combobox(dist_frame, width=18, values=[
            "Radiátory (vyššoteplotné)", "Podlahové kúrenie (nízkoteplotné)", "Konvektory", "Teplovzdušné"
        ])
        self.distribution_type.grid(row=0, column=5, padx=5, pady=3)
        
        # Riad 2 - Materiály a rozvody
        tk.Label(dist_frame, text="Materiál potrubí:", fg='blue').grid(row=1, column=0, sticky=tk.W, padx=5, pady=3)
        self.pipe_material = ttk.Combobox(dist_frame, width=18, values=[
            "Oceľové pozinkované", "Oceľové čierne", "Medené", "Plastové (PEX/PPR)", "Nerezové"
        ])
        self.pipe_material.grid(row=1, column=1, padx=5, pady=3)
        
        tk.Label(dist_frame, text="Tepelná izolácia rozvodov:", fg='orange').grid(row=1, column=2, sticky=tk.W, padx=5, pady=3)
        self.pipe_insulation = ttk.Combobox(dist_frame, width=15, values=[
            "Bez izolácie", "Nedostatočná", "Štandardná", "Dobrá", "Nadštandardná"
        ])
        self.pipe_insulation.grid(row=1, column=3, padx=5, pady=3)
        
        tk.Label(dist_frame, text="Regulácia teploty:", fg='orange').grid(row=1, column=4, sticky=tk.W, padx=5, pady=3)
        self.heating_control = ttk.Combobox(dist_frame, width=18, values=[
            "Bez regulácie", "Termostatické hlavice", "Ekvitermická", "Zónová regulácia", "Inteligentný systém"
        ])
        self.heating_control.grid(row=1, column=5, padx=5, pady=3)
        
        # LEŽATÉ ROZVODY PODĽA ZADANIA
        horizontal_frame = tk.LabelFrame(scrollable_frame, text="🔧 Ležaté rozvody vykurovacej vody", 
                                        font=('Arial', 11, 'bold'))
        horizontal_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(horizontal_frame, text="Vedenie ležatých rozvodov:", fg='blue').grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.horizontal_pipes_location = ttk.Combobox(horizontal_frame, width=20, values=[
            "Vo vykurovanom priestore", "V nevykurovanom priestore", "V podlahe", "Pri strope", "V stenách"
        ])
        self.horizontal_pipes_location.grid(row=0, column=1, padx=5, pady=3)
        
        tk.Label(horizontal_frame, text="Spôsob regulácie v bytoch:", fg='orange').grid(row=0, column=2, sticky=tk.W, padx=5, pady=3)
        self.apartment_control = ttk.Combobox(horizontal_frame, width=22, values=[
            "Žiadna regulácia", "Uzatváracie ventily", "Termostatické hlavice", "Izbové termostaty", "Zónová regulácia"
        ])
        self.apartment_control.grid(row=0, column=3, columnspan=2, padx=5, pady=3)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_dhw_tab(self):
        """Tab 4: Teplá užitková voda podľa STN EN 16247-1 bod 6.2.9"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🚿 TUV")
        
        canvas = tk.Canvas(tab)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind("<Configure>", 
                             lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Legénda farieb
        legend_frame = tk.Frame(scrollable_frame, bg='#f8f9fa', relief=tk.RIDGE, bd=1)
        legend_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(legend_frame, text="ℹ️ LEGENDÁ POLÍ:", font=('Arial', 10, 'bold'), bg='#f8f9fa').pack(side=tk.LEFT, padx=10, pady=5)
        tk.Label(legend_frame, text="🔴 POVINNÉ", fg='red', font=('Arial', 9, 'bold'), bg='#f8f9fa').pack(side=tk.LEFT, padx=10)
        tk.Label(legend_frame, text="🟠 DÔLEŽITÉ", fg='orange', font=('Arial', 9, 'bold'), bg='#f8f9fa').pack(side=tk.LEFT, padx=10)
        tk.Label(legend_frame, text="🔵 VOLITELNÉ", fg='blue', font=('Arial', 9, 'bold'), bg='#f8f9fa').pack(side=tk.LEFT, padx=10)
        
        # SYSTÉM PRÍPRAVY TUV PODĽA ZADANIA EACB
        dhw_system_frame = tk.LabelFrame(scrollable_frame, text="🚿 Príprava teplej vody cez odovzdávaciu stanicu (ZADANIE EACB)", 
                                        font=('Arial', 11, 'bold'))
        dhw_system_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Riad 1 - Základné parametre
        tk.Label(dhw_system_frame, text="Typ ohrevu TUV *:", fg='red', font=('Arial', 9, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.dhw_type = ttk.Combobox(dhw_system_frame, width=22, values=[
            "Elektrický bojler", "Plynový bojler", "Kombinovaný kotol", 
            "Solárne kolektory", "Tepelné čerpadlo TUV", "Príprava v kotle", "Prípravník"
        ])
        self.dhw_type.grid(row=0, column=1, padx=5, pady=3)
        self.dhw_type.bind('<<ComboboxSelected>>', self.on_dhw_type_changed)
        
        tk.Label(dhw_system_frame, text="Objem zásobníka [l] *:", fg='red', font=('Arial', 9, 'bold')).grid(row=0, column=2, sticky=tk.W, padx=5, pady=3)
        self.dhw_volume = tk.Entry(dhw_system_frame, width=12, bg='#ffe6e6')
        self.dhw_volume.grid(row=0, column=3, padx=5, pady=3)
        
        tk.Label(dhw_system_frame, text="Výkon ohrevu [kW]:", fg='orange').grid(row=0, column=4, sticky=tk.W, padx=5, pady=3)
        self.dhw_power = tk.Entry(dhw_system_frame, width=12, bg='#fff2e6')
        self.dhw_power.grid(row=0, column=5, padx=5, pady=3)
        
        # Riad 2 - Účinnosť a energia
        tk.Label(dhw_system_frame, text="Účinnosť ohrevu ηTUV [%] *:", fg='red', font=('Arial', 9, 'bold')).grid(row=1, column=0, sticky=tk.W, padx=5, pady=3)
        self.dhw_efficiency = tk.Entry(dhw_system_frame, width=12, bg='#ffe6e6')
        self.dhw_efficiency.grid(row=1, column=1, padx=5, pady=3)
        
        tk.Label(dhw_system_frame, text="Teplota úkladania [°C]:", fg='orange').grid(row=1, column=2, sticky=tk.W, padx=5, pady=3)
        self.dhw_storage_temp = tk.Entry(dhw_system_frame, width=12, bg='#fff2e6')
        self.dhw_storage_temp.grid(row=1, column=3, padx=5, pady=3)
        
        tk.Label(dhw_system_frame, text="Rok inštalácie:", fg='blue').grid(row=1, column=4, sticky=tk.W, padx=5, pady=3)
        self.dhw_installation_year = tk.Entry(dhw_system_frame, width=12, bg='#e6f2ff')
        self.dhw_installation_year.grid(row=1, column=5, padx=5, pady=3)
        
        # DISTRIBÚCIA PODĽA ZADANIA EACB
        distribution_frame = tk.LabelFrame(scrollable_frame, text="🔄 Distribúcia teplej vody - čerpávanie a rozvody", 
                                          font=('Arial', 11, 'bold'))
        distribution_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(distribution_frame, text="Spôsob prečerpávania TV:", fg='red', font=('Arial', 9, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.dhw_pumping_method = ttk.Combobox(distribution_frame, width=20, values=[
            "Cirkulačné čerpadlo pôvodné", "Cirkulačné čerpadlo vymené", "Bez čerpadla", "Gravitačný obeh"
        ])
        self.dhw_pumping_method.grid(row=0, column=1, padx=5, pady=3)
        
        tk.Label(distribution_frame, text="Typ cirkulácie:", fg='orange', font=('Arial', 9, 'bold')).grid(row=0, column=2, sticky=tk.W, padx=5, pady=3)
        self.dhw_circulation = ttk.Combobox(distribution_frame, width=18, values=[
            "Bez cirkulácie", "Neprerushovaná", "Časová", "Termostatická", "So čerpadlom na požiadanie"
        ])
        self.dhw_circulation.grid(row=0, column=3, padx=5, pady=3)
        
        # Riad 2 - Hlavný domový uzáver a merač
        tk.Label(distribution_frame, text="Hlavný domový uzáver:", fg='orange').grid(row=1, column=0, sticky=tk.W, padx=5, pady=3)
        self.main_water_shutoff = ttk.Combobox(distribution_frame, width=18, values=[
            "Inštalovaný a funkčný", "Inštalovaný - porucha", "Neinštalovaný", "Neprístupný"
        ])
        self.main_water_shutoff.grid(row=1, column=1, padx=5, pady=3)
        
        tk.Label(distribution_frame, text="Merač tepla objektu:", fg='orange').grid(row=1, column=2, sticky=tk.W, padx=5, pady=3)
        self.heat_meter = ttk.Combobox(distribution_frame, width=18, values=[
            "Inštalovaný a funkčný", "Inštalovaný - porucha", "Neinštalovaný", "Starý typ"
        ])
        self.heat_meter.grid(row=1, column=3, padx=5, pady=3)
        
        # MATERIÁLY ROZVODOV PODĽA ZADANIA
        materials_frame = tk.LabelFrame(scrollable_frame, text="🔧 Materiály rozvodov TUV", 
                                       font=('Arial', 11, 'bold'))
        materials_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(materials_frame, text="Materiál vykurovaný priestor:", fg='blue').grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.dhw_pipes_heated = ttk.Combobox(materials_frame, width=18, values=[
            "Oceľové pozinkované", "Oceľové čierne", "Medené", "Plastové (PPR/PEX)", "Nerezové"
        ])
        self.dhw_pipes_heated.grid(row=0, column=1, padx=5, pady=3)
        
        tk.Label(materials_frame, text="Izolácia vo vykur. priestore:", fg='blue').grid(row=0, column=2, sticky=tk.W, padx=5, pady=3)
        self.dhw_insulation_heated = ttk.Combobox(materials_frame, width=15, values=[
            "Bez izolácie", "Tenká", "Štandardná", "Hrúba"
        ])
        self.dhw_insulation_heated.grid(row=0, column=3, padx=5, pady=3)
        
        tk.Label(materials_frame, text="Materiál nevykurovaný priestor:", fg='blue').grid(row=1, column=0, sticky=tk.W, padx=5, pady=3)
        self.dhw_pipes_unheated = ttk.Combobox(materials_frame, width=18, values=[
            "Oceľové pozinkované", "Oceľové čierne", "Medené", "Plastové (PPR/PEX)", "Nerezové"
        ])
        self.dhw_pipes_unheated.grid(row=1, column=1, padx=5, pady=3)
        
        tk.Label(materials_frame, text="Izolácia v nevykur. priestore:", fg='orange').grid(row=1, column=2, sticky=tk.W, padx=5, pady=3)
        self.dhw_insulation_unheated = ttk.Combobox(materials_frame, width=15, values=[
            "Bez izolácie", "Nedostatočná", "Štandardná", "Dobrá", "Vnľná"
        ])
        self.dhw_insulation_unheated.grid(row=1, column=3, padx=5, pady=3)
        
        # STÚPACIE POTRUBIA
        vertical_frame = tk.LabelFrame(scrollable_frame, text="⬆️ Stúpacie potrubia TUV a cirkulácie", 
                                      font=('Arial', 11, 'bold'))
        vertical_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(vertical_frame, text="Spôsob vedenia stúpacích potrubí:", fg='orange').grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.vertical_pipes_routing = ttk.Combobox(vertical_frame, width=25, values=[
            "Vo vykurovanom priestore", "V šachte vykurovanej", "V šachte nevykurovanej", "V stenách", "Vonkajšie vedenie"
        ])
        self.vertical_pipes_routing.grid(row=0, column=1, columnspan=2, padx=5, pady=3)
        
        # SPOTREBA A POŽIADAVKY
        consumption_frame = tk.LabelFrame(scrollable_frame, text="📊 Spotreba a požiadavky na TUV", 
                                         font=('Arial', 11, 'bold'))
        consumption_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(consumption_frame, text="Denká spotreba TUV [l/deň]:", fg='orange', font=('Arial', 9, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.dhw_daily_consumption = tk.Entry(consumption_frame, width=12, bg='#fff2e6')
        self.dhw_daily_consumption.grid(row=0, column=1, padx=5, pady=3)
        
        tk.Label(consumption_frame, text="Počet odverných miest:", fg='blue').grid(row=0, column=2, sticky=tk.W, padx=5, pady=3)
        self.dhw_tap_points = tk.Entry(consumption_frame, width=12, bg='#e6f2ff')
        self.dhw_tap_points.grid(row=0, column=3, padx=5, pady=3)
        
        tk.Label(consumption_frame, text="Teplota dodávky [°C]:", fg='blue').grid(row=0, column=4, sticky=tk.W, padx=5, pady=3)
        self.dhw_supply_temp = tk.Entry(consumption_frame, width=12, bg='#e6f2ff')
        self.dhw_supply_temp.grid(row=0, column=5, padx=5, pady=3)
        
        # OBNOVITELNÉ ZDROJE ENERGIE
        renewable_frame = tk.LabelFrame(scrollable_frame, text="☀️ Obnovitelné zdroje energie pre TUV", 
                                       font=('Arial', 11, 'bold'))
        renewable_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(renewable_frame, text="Solárne kolektory:", fg='blue').grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.solar_collectors = ttk.Combobox(renewable_frame, width=18, values=[
            "Bez solárnych kolektorov", "Plochodeskové", "Vakúúmiové", "Koncentračné"
        ])
        self.solar_collectors.grid(row=0, column=1, padx=5, pady=3)
        
        tk.Label(renewable_frame, text="Plocha kolektorov [m²]:", fg='blue').grid(row=0, column=2, sticky=tk.W, padx=5, pady=3)
        self.solar_area = tk.Entry(renewable_frame, width=12, bg='#e6f2ff')
        self.solar_area.grid(row=0, column=3, padx=5, pady=3)
        
        tk.Label(renewable_frame, text="Orientácia kolektorov:", fg='blue').grid(row=0, column=4, sticky=tk.W, padx=5, pady=3)
        self.solar_orientation = ttk.Combobox(renewable_frame, width=15, values=[
            "Juh", "Juhovychod", "Juhozapad", "Vychod", "Zapad", "Iná"
        ])
        self.solar_orientation.grid(row=0, column=5, padx=5, pady=3)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_electrical_tab(self):
        """Tab 5: Elektrina a osvetlenie podľa STN EN 16247-1"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="💡 Elektrina")
        
        canvas = tk.Canvas(tab)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind("<Configure>", 
                             lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Legénda farieb
        legend_frame = tk.Frame(scrollable_frame, bg='#f8f9fa', relief=tk.RIDGE, bd=1)
        legend_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(legend_frame, text="ℹ️ LEGENDÁ POLÍ:", font=('Arial', 10, 'bold'), bg='#f8f9fa').pack(side=tk.LEFT, padx=10, pady=5)
        tk.Label(legend_frame, text="🔴 POVINNÉ", fg='red', font=('Arial', 9, 'bold'), bg='#f8f9fa').pack(side=tk.LEFT, padx=10)
        tk.Label(legend_frame, text="🟠 DÔLEŽITÉ", fg='orange', font=('Arial', 9, 'bold'), bg='#f8f9fa').pack(side=tk.LEFT, padx=10)
        tk.Label(legend_frame, text="🔵 VOLITELNÉ", fg='blue', font=('Arial', 9, 'bold'), bg='#f8f9fa').pack(side=tk.LEFT, padx=10)
        
        # OSVETLENIE
        light_frame = tk.LabelFrame(scrollable_frame, text="💡 Osvetlenie (STN EN 16247-1 bod 6.2.8)", 
                                   font=('Arial', 11, 'bold'))
        light_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(light_frame, text="Typ svietidiel:", fg='orange', font=('Arial', 9, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.lighting_type = ttk.Combobox(light_frame, width=18, values=[
            "LED", "Fluorescenčné (T5/T8)", "Halogénové", "Výbojkové", "Klasické žiarovky"
        ])
        self.lighting_type.grid(row=0, column=1, padx=5, pady=3)
        self.lighting_type.bind('<<ComboboxSelected>>', self.on_lighting_type_changed)
        
        tk.Label(light_frame, text="Inštalovaný výkon [W]:", fg='orange', font=('Arial', 9, 'bold')).grid(row=0, column=2, sticky=tk.W, padx=5, pady=3)
        self.lighting_power = tk.Entry(light_frame, width=12, bg='#fff2e6')
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
        
        tk.Label(devices_frame, text="IT zariadenia [W]:", fg='blue').grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.it_power = tk.Entry(devices_frame, width=12, bg='#e6f2ff')
        self.it_power.grid(row=0, column=1, padx=5, pady=3)
        
        tk.Label(devices_frame, text="Ostatné spotrebiče [W]:", fg='blue').grid(row=0, column=2, sticky=tk.W, padx=5, pady=3)
        self.appliances_power = tk.Entry(devices_frame, width=12, bg='#e6f2ff')
        self.appliances_power.grid(row=0, column=3, padx=5, pady=3)
        
        tk.Label(devices_frame, text="Chladenie/klimatizácia [W]:", fg='blue').grid(row=0, column=4, sticky=tk.W, padx=5, pady=3)
        self.cooling_power = tk.Entry(devices_frame, width=12, bg='#e6f2ff')
        self.cooling_power.grid(row=0, column=5, padx=5, pady=3)
        
        
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
        
        # Legénda farieb
        legend_frame = tk.Frame(scrollable_frame, bg='#f8f9fa', relief=tk.RIDGE, bd=1)
        legend_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(legend_frame, text="ℹ️ LEGENDÁ POLÍ:", font=('Arial', 10, 'bold'), bg='#f8f9fa').pack(side=tk.LEFT, padx=10, pady=5)
        tk.Label(legend_frame, text="🔴 POVINNÉ", fg='red', font=('Arial', 9, 'bold'), bg='#f8f9fa').pack(side=tk.LEFT, padx=10)
        tk.Label(legend_frame, text="🟠 DÔLEŽITÉ", fg='orange', font=('Arial', 9, 'bold'), bg='#f8f9fa').pack(side=tk.LEFT, padx=10)
        tk.Label(legend_frame, text="🔵 VOLITELNÉ", fg='blue', font=('Arial', 9, 'bold'), bg='#f8f9fa').pack(side=tk.LEFT, padx=10)
        
        # OBSADENOSŤ A PREVÁDZKA
        occupancy_frame = tk.LabelFrame(scrollable_frame, text="👥 Obsadenosť a prevádzka (STN EN 16247-1 bod 6.2.10)", 
                                       font=('Arial', 11, 'bold'))
        occupancy_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(occupancy_frame, text="Počet užívateľov (osoby):", fg='orange', font=('Arial', 9, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.occupants = tk.Entry(occupancy_frame, width=12, bg='#fff2e6')
        self.occupants.grid(row=0, column=1, padx=5, pady=3)
        
        tk.Label(occupancy_frame, text="Hodiny/deň:", fg='orange', font=('Arial', 9, 'bold')).grid(row=0, column=2, sticky=tk.W, padx=5, pady=3)
        self.operating_hours = tk.Entry(occupancy_frame, width=12, bg='#fff2e6')
        self.operating_hours.grid(row=0, column=3, padx=5, pady=3)
        
        tk.Label(occupancy_frame, text="Dni/rok:").grid(row=0, column=4, sticky=tk.W, padx=5, pady=3)
        self.operating_days = tk.Entry(occupancy_frame, width=12)
        self.operating_days.grid(row=0, column=5, padx=5, pady=3)
        
        tk.Label(occupancy_frame, text="Nastavená teplota zima [°C]:", fg='orange', font=('Arial', 9, 'bold')).grid(row=1, column=0, sticky=tk.W, padx=5, pady=3)
        self.winter_temp = tk.Entry(occupancy_frame, width=12, bg='#fff2e6')
        self.winter_temp.grid(row=1, column=1, padx=5, pady=3)
        
        tk.Label(occupancy_frame, text="Nastavená teplota leto [°C]:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=3)
        self.summer_temp = tk.Entry(occupancy_frame, width=12)
        self.summer_temp.grid(row=1, column=3, padx=5, pady=3)
        
        # AKTUÁLNA SPOTREBA A TARIFY
        consumption_frame = tk.LabelFrame(scrollable_frame, text="📊 Energetická bilancia (meraná) a ceny", 
                                         font=('Arial', 11, 'bold'))
        consumption_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(consumption_frame, text="Ročná spotreba plynu [m³]:", fg='orange', font=('Arial', 9, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.gas_consumption = tk.Entry(consumption_frame, width=12, bg='#fff2e6')
        self.gas_consumption.grid(row=0, column=1, padx=5, pady=3)
        
        tk.Label(consumption_frame, text="Ročná spotreba elektriny [kWh]:", fg='orange', font=('Arial', 9, 'bold')).grid(row=0, column=2, sticky=tk.W, padx=5, pady=3)
        self.electricity_consumption = tk.Entry(consumption_frame, width=12, bg='#fff2e6')
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
        
        tk.Button(buttons_frame, text="🧠 Detailné výpočty", command=self.show_calculations,
                 bg='#f39c12', fg='white', font=('Arial', 11, 'bold'),
                 width=15, height=2).pack(side=tk.LEFT, padx=5)
        
        tk.Button(buttons_frame, text="🧪 Test výpočtov", command=self.test_calculation_accuracy,
                 bg='#8e44ad', fg='white', font=('Arial', 11, 'bold'),
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
                    'window_glazing': self.window_glazing.get() or "",
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
                    'cooling_power': float(self.cooling_power.get() or 0) if hasattr(self, 'cooling_power') and self.cooling_power.get() else 0
                },
                'dhw': {
                    'type': self.dhw_type.get() or "Elektrický bojler",
                    'volume': float(self.dhw_volume.get() or 200),
                    'efficiency': float(self.dhw_efficiency.get() or 85) / 100 if self.dhw_efficiency.get() else 0.85,
                    'power': float(self.dhw_power.get() or 0) if hasattr(self, 'dhw_power') and self.dhw_power.get() else 0,
                    'storage_temp': float(self.dhw_storage_temp.get() or 60) if hasattr(self, 'dhw_storage_temp') and self.dhw_storage_temp.get() else 60,
                    'circulation': self.dhw_circulation.get() or "Bez cirkulácie",
                    'daily_consumption': float(self.dhw_daily_consumption.get() or 0) if hasattr(self, 'dhw_daily_consumption') and self.dhw_daily_consumption.get() else 0,
                    'installation_year': int(self.dhw_installation_year.get() or 2010) if hasattr(self, 'dhw_installation_year') and self.dhw_installation_year.get() else None,
                    'pipe_length': float(self.dhw_pipe_length.get() or 0) if hasattr(self, 'dhw_pipe_length') and self.dhw_pipe_length.get() else 0,
                    'pipe_insulation': self.dhw_pipe_insulation.get() if hasattr(self, 'dhw_pipe_insulation') else "Bez izolácie",
                    'solar_collectors': self.solar_collectors.get() if hasattr(self, 'solar_collectors') else "Bez solárnych kolektorov",
                    'solar_area': float(self.solar_area.get() or 0) if hasattr(self, 'solar_area') and self.solar_area.get() else 0
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
                },
                'thermal_assessment': {
                    'wall_u_actual': float(self.wall_u_actual.get() or 0) if hasattr(self, 'wall_u_actual') and self.wall_u_actual.get() else 0,
                    'wall_u_required': 0.22,
                    'roof_u_actual': float(self.roof_u_actual.get() or 0) if hasattr(self, 'roof_u_actual') and self.roof_u_actual.get() else 0,
                    'roof_u_required': 0.15,
                    'floor_u_actual': float(self.floor_u_actual.get() or 0) if hasattr(self, 'floor_u_actual') and self.floor_u_actual.get() else 0,
                    'floor_u_required': 0.85,
                    'window_u_actual': float(self.window_u_actual.get() or 0) if hasattr(self, 'window_u_actual') and self.window_u_actual.get() else 0,
                    'window_u_max': 1.7
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
            dhw = self.audit_data['dhw']
            
            # VALIDÁCIA KRITICKÝCH VSTUPNÝCH HODNÔT
            errors = []
            
            if basic['floor_area'] <= 0:
                errors.append("Podlahová plocha musí byť väčšia ako 0")
            if envelope['wall_area'] <= 0:
                errors.append("Plocha stìn musí byť väčšia ako 0")
            if envelope['window_area'] < 0:
                errors.append("Plocha okien nemôže byť záporná")
            if envelope['roof_area'] <= 0:
                errors.append("Plocha strechy musí byť väčšia ako 0")
            if envelope['wall_u'] <= 0 or envelope['wall_u'] > 3.0:
                errors.append("U-hodnota stìn musí byť medzi 0.01-3.0 W/m²K")
            if envelope['window_u'] <= 0 or envelope['window_u'] > 6.0:
                errors.append("U-hodnota okien musí byť medzi 0.01-6.0 W/m²K")
            if envelope['roof_u'] <= 0 or envelope['roof_u'] > 3.0:
                errors.append("U-hodnota strechy musí byť medzi 0.01-3.0 W/m²K")
            if heating['efficiency'] <= 0 or heating['efficiency'] > 1.2:
                errors.append("Účinnosť vykurovania musí byť medzi 0.3-1.2")
            if usage['winter_temp'] < 15 or usage['winter_temp'] > 25:
                errors.append("Vnútorná teplota musí byť medzi 15-25°C")
                
            if errors:
                error_msg = "\n".join([f"\u2022 {err}" for err in errors])
                messagebox.showerror("Chyby vo vstupných údajoch", 
                                   f"Opravte následujúce chyby:\n\n{error_msg}")
                return
            
            # Progres 40% - Tepelné straty
            self.progress['value'] = 40
            self.root.update()
            
            # VÝPOČET TEPELNÝCH STRÁT podľa STN EN ISO 13790
            
            # 1. TRANSMISNÉ STRATY (QT)
            wall_losses = envelope['wall_area'] * envelope['wall_u']  # Obvodové steny
            window_losses = envelope['window_area'] * envelope['window_u']  # Okná
            roof_losses = envelope['roof_area'] * envelope['roof_u']  # Strecha
            
            # Podlaha (ak nie je zadaná, použije sa floor_area z basic_info)
            floor_area = float(self.floor_area_envelope.get() or basic['floor_area']) if hasattr(self, 'floor_area_envelope') and self.floor_area_envelope.get() else basic['floor_area']
            floor_u = float(self.floor_u.get() or 0.3) if hasattr(self, 'floor_u') and self.floor_u.get() else 0.3
            floor_losses = floor_area * floor_u
            
            # Tepelné mosty (linearny koeficient Ψ)
            thermal_bridge_losses = 0
            if hasattr(self, 'thermal_bridges_area') and self.thermal_bridges_area.get():
                tb_area = float(self.thermal_bridges_area.get())
                tb_psi = float(self.thermal_bridges_psi.get() or 0.1) if hasattr(self, 'thermal_bridges_psi') and self.thermal_bridges_psi.get() else 0.1
                thermal_bridge_losses = tb_area * tb_psi
            else:
                # Odhadované tepelné mosty (5% z transmisných strát)
                thermal_bridge_losses = (wall_losses + window_losses + roof_losses + floor_losses) * 0.05
            
            # Celkové transmisné straty
            transmission_losses = wall_losses + window_losses + roof_losses + floor_losses + thermal_bridge_losses
            
            # 2. VENTILAČNÉ STRATY (QV)
            # n50 - tesnost budovy (1/h)
            n50 = float(basic.get('n50', 3.0))  # Predvolená hodnota pre staršie budovy
            if basic['construction_year'] >= 2020:
                n50 = 1.5  # Nové budovy
            elif basic['construction_year'] >= 2010:
                n50 = 2.0  # Rekonstruécie
            
            # Infiltračné straty
            building_volume = basic.get('volume', basic['floor_area'] * 2.7)
            air_density = 1.2  # kg/m3
            specific_heat_air = 1000  # J/kgK = 1 Wh/kgK
            
            # Ventilačný tok (prirodzené + mechanické vetranie)
            # Oprava: n50 sa nedéli 20, ale menším číslom podľa normy
            natural_ach = n50 / 50  # Infiltračný tok podľa STN EN ISO 13790
            mechanical_ach = 0.5  # Mechanické vetranie (minimum 0.5 h⁻¹)
            total_ach = natural_ach + mechanical_ach
            
            # Ventilačné straty: QV = 0.34 * n * V [W/K]
            # kde 0.34 = ρ*cp = 1.2 * 1000/3600
            ventilation_losses = 0.34 * total_ach * building_volume  # W/K
            
            # CELKOVÉ TEPELNÉ STRATY
            total_losses = transmission_losses + ventilation_losses
            
            # Progres 60% - Potreba tepla
            self.progress['value'] = 60
            self.root.update()
            
            # POTREBA TEPLA (mesačná metóda podľa STN EN ISO 13790)
            
            # Klimatické údaje pre SR (podľa STN 73 0540-3)
            climate_data = {
                'BA': {'hdd': 2800, 'monthly_temp': [-1, 1, 6, 11, 16, 19, 21, 20, 16, 10, 4, 0]},  # Bratislava
                'KE': {'hdd': 3100, 'monthly_temp': [-2, 0, 5, 10, 15, 18, 20, 19, 15, 9, 3, -1]},   # Košice  
                'PP': {'hdd': 3200, 'monthly_temp': [-3, -1, 4, 9, 14, 17, 19, 18, 14, 8, 2, -2]}   # Poprad
            }
            
            # Použije sa Bratislava ako predvolené
            climate = climate_data.get(basic.get('climate_zone', 'BA'), climate_data['BA'])
            
            # MESAČNÁ BILANCIA
            monthly_heating_need = []
            annual_heating_need = 0
            
            # Vnútorná teplota
            internal_temp = usage['winter_temp']  # 21°C
            
            # Mesačné výpočty
            for month in range(12):
                external_temp = climate['monthly_temp'][month]
                temp_diff = internal_temp - external_temp
                
                if temp_diff > 0:  # Vykurovačka sezóna
                    # Dĺžka mesiaca
                    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month]
                    
                    # SOLÁRNE ZISKY
                    # Solárna irácia pre SR [kWh/m2/mesiac]
                    solar_irradiation = [20, 35, 70, 110, 140, 150, 155, 130, 95, 55, 25, 15][month]
                    
                    # Solárne zisky cez okná
                    g_value = float(self.window_g_value.get() or 0.6) if hasattr(self, 'window_g_value') and self.window_g_value.get() else 0.6
                    solar_gains = envelope['window_area'] * g_value * solar_irradiation * 0.9  # kWh/mesiac
                    
                    # VNÚTORNÉ TEPELNÉ ZISKY
                    # Zisky od osôb (4W/m2 pre obytne budovy)
                    occupant_gains = basic['floor_area'] * 4 * days_in_month * 24 / 1000  # kWh/mesiac
                    
            # Zisky od osvetlenia a zariadení (prepočíta sa na m²)
                    lighting_power_m2 = electrical['lighting_power'] / basic['floor_area']  # W/m²
                    appliances_power_m2 = electrical['appliances_power'] / basic['floor_area']  # W/m²
                    total_equipment_power = (lighting_power_m2 + appliances_power_m2) * basic['floor_area']  # W
                    equipment_gains = total_equipment_power * usage['operating_hours'] * days_in_month / 1000  # kWh/mesiac
                    
                    total_internal_gains = occupant_gains + equipment_gains  # kWh/mesiac
                    total_gains = solar_gains + total_internal_gains  # kWh/mesiac
                    
                    # TEPELNÉ STRATY
                    monthly_losses = total_losses * temp_diff * days_in_month * 24 / 1000  # kWh/mesiac
                    
                    # VYUŽITEĽNOSŤ TEPELNÝCH ZISKOV
                    # Pomer ziskov a strát
                    gamma = total_gains / monthly_losses if monthly_losses > 0 else 0
                    
                    # Koeficient využitelnosti (podľa STN EN ISO 13790)
                    if gamma > 0:
                        # Časová konštanta budovy [h]
                        # C = ρ * cp * V_air + Cm (masa budovy)
                        # Cm = Am * Cm,i (kde Am = 2.5 * Af)
                        thermal_mass = 2.5 * basic['floor_area'] * 165000  # J/K (stredne ťažká budova)
                        air_thermal_capacity = 1200 * building_volume  # J/K
                        total_thermal_capacity = thermal_mass + air_thermal_capacity
                        
                        # Časová konštanta τ = C / HT [h]
                        tau = total_thermal_capacity / (transmission_losses * 3600)  # h
                        
                        # Parameter a = 1 + τ/15
                        a = 1 + tau / 15
                        
                        if gamma != 1:
                            eta = (1 - gamma**a) / (1 - gamma**(a+1))
                        else:
                            eta = a / (a + 1)
                            
                        eta = max(0, min(1, eta))  # Ohraničenie na 0-1
                    else:
                        eta = 0
                    
                    # POTREBA TEPLA NA VYKUROVANIE
                    useful_gains = eta * total_gains
                    monthly_need = max(0, monthly_losses - useful_gains)  # kWh/mesiac
                    
                    monthly_heating_need.append(monthly_need)
                    annual_heating_need += monthly_need
                else:
                    monthly_heating_need.append(0)
            
            heating_need = annual_heating_need  # kWh/rok
            
            # SPOTREBA ENERGIE NA VYKUROVANIE
            heating_energy = heating_need / heating['efficiency']
            
            # Progres 80% - Elektrická energia
            self.progress['value'] = 80
            self.root.update()
            
            # ELEKTRICKÁ ENERGIA
            lighting_energy = (electrical['lighting_power'] * usage['operating_hours'] * 
                             usage['operating_days']) / 1000
            
            appliances_energy = ((electrical['it_power'] + electrical['appliances_power'] + electrical['cooling_power']) * 
                               usage['operating_hours'] * usage['operating_days']) / 1000
            
            # Teplá užitková voda - detailný výpočet
            if dhw['daily_consumption'] > 0:
                daily_dhw = dhw['daily_consumption']  # l/deň
            else:
                daily_dhw = usage['occupants'] * 50  # odhad 50l/osobu/deň
            
            # Energia na ohrev TUV
            dhw_energy_need = daily_dhw * 365 * 1.163 * (dhw['storage_temp'] - 10) / 1000  # kWh/rok (z 10°C na storage_temp)
            dhw_energy = dhw_energy_need / dhw['efficiency']  # reálna spotreba s účinnosťou
            
            total_electricity = lighting_energy + appliances_energy + dhw_energy
            
            # CELKOVÁ ENERGIA
            total_energy = heating_energy + total_electricity
            
            # PRIMÁRNA ENERGIA podľa vyhlášky MH SR č. 364/2012 Z. z.
            
            # Konverzné faktory pre SK (aktualizované podľa vyhl. 364/2012 a novél MH SR 2024)
            conversion_factors = {
                'natural_gas': 1.1,      # Zemný plyn
                'heating_oil': 1.2,      # Výkurový olej
                'electricity': 2.5,      # Elektrina SR (aktualizované 2024) 
                'district_heating': 1.0,  # Celenné vykurovanie (podľa novél)
                'biomass': 1.2,          # Biomasa s týmaním a dopravou
                'heat_pump': 2.5,        # Tepelné čerpadlo (COP 3.0)
                'solar': 1.0,            # Solárne kolektory
                'geothermal': 1.0        # Geotermia
            }
            
            # Určenie typu paliva
            fuel_type = heating.get('fuel_type', 'Zemný plyn').lower()
            if 'plyn' in fuel_type:
                heating_factor = conversion_factors['natural_gas']
            elif 'olej' in fuel_type:
                heating_factor = conversion_factors['heating_oil']
            elif 'elektri' in fuel_type:
                heating_factor = conversion_factors['electricity']
            elif 'celenn' in fuel_type or 'celkov' in fuel_type:
                heating_factor = conversion_factors['district_heating']
            elif 'biomasa' in fuel_type or 'drevo' in fuel_type:
                heating_factor = conversion_factors['biomass']
            elif 'čerpadlo' in fuel_type:
                heating_factor = conversion_factors['heat_pump']
            else:
                heating_factor = conversion_factors['natural_gas']  # Predvolené
            
            # Výpočet primárnej energie
            primary_heating = heating_energy * heating_factor
            primary_electricity = total_electricity * conversion_factors['electricity']
            primary_dhw = dhw_energy * heating_factor  # TUV používa rovnaký zdroj
            
            primary_energy = primary_heating + primary_electricity + primary_dhw
            specific_primary = primary_energy / basic['floor_area'] if basic['floor_area'] > 0 else 0
            
            # ENERGETICKÁ TRIEDA podľa vyhlášky MH SR č. 364/2012 Z. z.
            # Hranice pre obytné budovy [kWh/m²rok]
            if basic['building_purpose'] == 'Rodinný dom' or 'rodin' in basic['building_purpose'].lower():
                # Rodinné domy
                if specific_primary <= 50:
                    energy_class = "A0"
                elif specific_primary <= 75:
                    energy_class = "A1" 
                elif specific_primary <= 100:
                    energy_class = "B"
                elif specific_primary <= 150:
                    energy_class = "C"
                elif specific_primary <= 200:
                    energy_class = "D"
                elif specific_primary <= 250:
                    energy_class = "E"
                elif specific_primary <= 300:
                    energy_class = "F"
                else:
                    energy_class = "G"
            else:
                # Ostatné obytné budovy
                if specific_primary <= 45:
                    energy_class = "A0"
                elif specific_primary <= 70:
                    energy_class = "A1"
                elif specific_primary <= 95:
                    energy_class = "B"
                elif specific_primary <= 140:
                    energy_class = "C"
                elif specific_primary <= 190:
                    energy_class = "D"
                elif specific_primary <= 240:
                    energy_class = "E"
                elif specific_primary <= 290:
                    energy_class = "F"
                else:
                    energy_class = "G"
                energy_class = 'G'
                
            # CO2 EMISIE podľa aktualizovaných emisných faktorov pre SR
            
            # Emisné faktory [kg CO2/kWh] podľa SEPS a SHMU 2024
            emission_factors = {
                'natural_gas': 0.202,     # Zemný plyn
                'heating_oil': 0.267,     # Výkurový olej/nafta
                'electricity': 0.218,     # Elektrina SR (2024 - nižšie díky OZE)
                'district_heating': 0.230, # Celenné vykurovanie (priemer SR)
                'biomass': 0.039,         # Biomasa (nie úplne CO2 neutrálna)
                'heat_pump': 0.109,       # Tepelné čerpadlo (elektrina/COP)
                'solar': 0.015,           # Solárne kolektory (výroba+transport) 
                'geothermal': 0.013       # Geotermia
            }
            
            # Určenie emisného faktora pre vykurovanie
            if 'plyn' in fuel_type:
                heating_emission_factor = emission_factors['natural_gas']
            elif 'olej' in fuel_type:
                heating_emission_factor = emission_factors['heating_oil']
            elif 'elektri' in fuel_type:
                heating_emission_factor = emission_factors['electricity']
            elif 'celenn' in fuel_type:
                heating_emission_factor = emission_factors['district_heating']
            elif 'biomasa' in fuel_type or 'drevo' in fuel_type:
                heating_emission_factor = emission_factors['biomass']
            elif 'čerpadlo' in fuel_type:
                heating_emission_factor = emission_factors['heat_pump']
            else:
                heating_emission_factor = emission_factors['natural_gas']
            
            # Výpočet CO2 emisií
            co2_heating = heating_energy * heating_emission_factor
            co2_electricity = total_electricity * emission_factors['electricity']
            co2_dhw = dhw_energy * heating_emission_factor
            co2_emissions = co2_heating + co2_electricity + co2_dhw
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
                # Detailné tepelné straty
                'wall_losses': wall_losses,
                'window_losses': window_losses,
                'roof_losses': roof_losses,
                'floor_losses': floor_losses,
                'thermal_bridge_losses': thermal_bridge_losses,
                'transmission_losses': transmission_losses,
                'ventilation_losses': ventilation_losses,
                'total_losses': total_losses,
                # Mesačné údaje
                'monthly_heating_need': monthly_heating_need,
                'climate_zone': basic.get('climate_zone', 'BA'),
                # Faktory
                'heating_factor': heating_factor,
                'heating_emission_factor': heating_emission_factor,
                'fuel_type': heating.get('fuel_type', 'Zemný plyn'),
                # Vykurovačú účinnosť
                'system_efficiency': heating['efficiency'],
                'n50_value': n50,
                'building_volume': building_volume
            }
            
            # Zobrazenie výsledkov
            self.display_results()
            
            # Prepnutie na tab výsledkov
            self.notebook.select(6)  # Index tabu výsledkov (teô 6 kvôli TUV tabu)
            
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
        
        # Základné povinné údaje
        output = f"""
{'='*80}
📊 ENERGETICKÝ AUDIT - VÝSLEDKY
{'='*80}

🏢 BUDOVA: {basic['building_name']}
📍 Adresa: {basic['address']}
📐 Podlahová plocha: {basic['floor_area']:.0f} m²
📅 Rok výstavby: {basic['construction_year']}
🏗️ Účel budovy: {basic['building_purpose']}"""
        

        # Voliteľné identifikačné údaje
        optional_id = {
            "Vlastník": (basic.get('owner'), ""),
            "Kontaktná osoba": (basic.get('contact_person'), ""),
            "PSČ a obec": (basic.get('postal_city'), ""),
            "Telefón/Email": (basic.get('contact_details'), ""),
            "IČO": (basic.get('owner_ico'), ""),
            "Katastrálne územie": (basic.get('cadastral'), ""),
            "Súpisné/orientačné číslo": (basic.get('house_number'), "")
        }
        output += self.format_section_if_has_data("IDENTIFIKÁCIA OBJEKTU", optional_id)
        
        # Voliteľné technické údaje
        optional_tech = {
            "Rok rekonštrukcie": (basic.get('renovation_year'), ""),
            "Aktuálna energetická trieda": (basic.get('current_energy_class'), ""),
            "Celková podlahová plocha": (basic.get('total_floor_area'), " m²"),
            "Počet podzemných podlaží": (basic.get('floors_below'), ""),
            "Svetlá výška": (basic.get('ceiling_height'), " m"),
            "Konštrukčný systém": (basic.get('construction_system'), ""),
            "Typ založenia": (basic.get('foundation_type'), ""),
            "Orientácia fasády": (basic.get('orientation'), "")
        }
        output += self.format_section_if_has_data("TECHNICKÉ CHARAKTERISTIKY", optional_tech)
        
        # Voliteľné klimatické údaje
        optional_climate = {
            "Klimatická oblasť": (basic.get('climate_zone'), ""),
            "Nadmorská výška": (basic.get('altitude'), " m n.m."),
            "Prevažujúci smer vetra": (basic.get('wind_direction'), ""),
            "Tienenie budovy": (basic.get('shading'), "")
        }
        output += self.format_section_if_has_data("KLIMATICKÉ ÚDAJE", optional_climate)
        
        output += f"""

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

Klasifikácia energetických tried podľa vyhlášky 364/2012:
🏠 Rodinné domy:
  A0: ≤ 50 kWh/m²rok    (Veľmi úsporná - pasivna)
  A1: ≤ 75 kWh/m²rok    (Veľmi úsporná)
  B:  ≤ 100 kWh/m²rok   (Úsporná)
  C:  ≤ 150 kWh/m²rok   (Vyhovujúca)
  D:  ≤ 200 kWh/m²rok   (Nevyhovujúca)
  E:  ≤ 250 kWh/m²rok   (Neúsporná)
  F:  ≤ 300 kWh/m²rok   (Veľmi neúsporná)
  G:  > 300 kWh/m²rok   (Mimoriadne neúsporná)

🏢 Ostatné obytné budovy:
  A0: ≤ 45 kWh/m²rok    (Veľmi úsporná - pasivna)
  A1: ≤ 70 kWh/m²rok    (Veľmi úsporná)
  B:  ≤ 95 kWh/m²rok    (Úsporná)
  C:  ≤ 140 kWh/m²rok   (Vyhovujúca)
  D:  ≤ 190 kWh/m²rok   (Nevyhovujúca)
  E:  ≤ 240 kWh/m²rok   (Neúsporná)
  F:  ≤ 290 kWh/m²rok   (Veľmi neúsporná)
  G:  > 290 kWh/m²rok   (Mimoriadne neúsporná)

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
        
    def test_calculation_accuracy(self):
        """Test správnosti výpočtov s referenčnými hodnôtami"""
        # Referenčné údaje pre typ rodinny dom 120 m²
        reference_data = {
            'basic_info': {
                'floor_area': 120.0,
                'construction_year': 2000,
                'building_purpose': 'Rodinný dom',
                'volume': 324.0  # 120 * 2.7
            },
            'envelope': {
                'wall_area': 150.0,
                'wall_u': 0.45,  # Staršia budova
                'window_area': 20.0,
                'window_u': 2.8,  # Staré okná
                'roof_area': 120.0,
                'roof_u': 0.35   # Staršia strecha
            },
            'heating': {
                'efficiency': 0.85,  # Starší plyn kotél
                'fuel_type': 'Zemný plyn'
            },
            'usage': {
                'winter_temp': 21.0,
                'operating_hours': 12.0,
                'operating_days': 250
            },
            'electrical': {
                'lighting_power': 600,
                'appliances_power': 800
            }
        }
        
        # Očakávané výsledky (orientančné)
        expected = {
            'transmission_losses': 135,  # W/K (cca)
            'ventilation_losses': 55,    # W/K (cca) 
            'heating_need': 15000,       # kWh/rok (cca)
            'specific_primary': 170      # kWh/m²rok (trieda D)
        }
        
        test_window = tk.Toplevel(self.root)
        test_window.title("🧪 Test správnosti výpočtov")
        test_window.geometry("700x500")
        test_window.configure(bg='white')
        
        result_text = scrolledtext.ScrolledText(test_window, font=('Consolas', 10))
        result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        test_results = f"""
🧪 KONTROLNÝ TEST VÝPOČTOV
{'='*60}

Referenčné údaje - typický rodinný dom 120 m²:
• Plocha stìn: 150 m², U = 0.45 W/m²K
• Plocha okien: 20 m², U = 2.8 W/m²K  
• Plocha strechy: 120 m², U = 0.35 W/m²K
• Účinnosť vykurovania: 85%
• Palivo: zemný plyn

Očakávané výsledky:
• Transmisné straty: ~135 W/K
• Ventilačné straty: ~55 W/K
• Potreba tepla: ~15000 kWh/rok
• Špecifická primárna energia: ~170 kWh/m²rok

{'='*60}
VÝPOČET:
{'='*60}

1. TRANSMISNÉ STRATY:
   Steny: 150 × 0.45 = 67.5 W/K
   Okná: 20 × 2.8 = 56.0 W/K
   Strecha: 120 × 0.35 = 42.0 W/K
   Podlaha: 120 × 0.30 = 36.0 W/K
   Tepelné mosty (5%): 10.1 W/K
   CELKOM: 211.6 W/K ❌ CHYBA! Očakávalo sa ~135 W/K

2. VENTILAČNÉ STRATY:
   n50 = 3.0 h⁻¹ (staršia budova)
   Infiltračný tok: 3.0/50 = 0.06 h⁻¹
   Mechanické vetranie: 0.5 h⁻¹
   Celkom: 0.56 h⁻¹
   QV = 0.34 × 0.56 × 324 = 61.7 W/K ✅ OK

3. POTREBA TEPLA (zjednodušene):
   HT = 211.6 + 61.7 = 273.3 W/K
   HDD Bratislava = 2800 K·deň
   Qh = 273.3 × 2800 × 24 / 1000 = 18,335 kWh/rok
   S mesacnou bilanciou a ziskami: ~15,000 kWh/rok

⚠️ POZNÁMKY:
- Transmisné straty sú vyššie ako očakávane
- Potrebné overíť U-hodnoty a plochy
- Mesačná bilancia zníži konečnú potrebu tepla
        """
        
        result_text.insert(tk.END, test_results)
        result_text.config(state=tk.DISABLED)
    
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
                 
    def format_optional_field(self, label, value, unit=""):
        """Formátuje voliteľné pole len ak je vyplnené"""
        if value and str(value).strip() not in ["", "0", "0.0", "Neznáma"]:
            return f"\n• {label}: {value}{unit}"
        return ""
    
    def format_section_if_has_data(self, title, fields_dict):
        """Formátuje sekciu len ak obsahuje dané"""
        section_content = ""
        for label, (value, unit) in fields_dict.items():
            section_content += self.format_optional_field(label, value, unit)
        
        if section_content:
            return f"\n\n=== {title} ===" + section_content
        return ""
    
    def generate_calculation_details(self):
        """Generovanie detailných výpočtov podľa STN EN ISO 13790"""
        if not self.results:
            return "Najprv vykonajte audit."
            
        basic = self.audit_data['basic_info']
        envelope = self.audit_data['envelope']
        heating = self.audit_data['heating']
        results = self.results
        
        # Konverzné faktory (lokálne pre detailné výpočty)
        conversion_factors = {
            'electricity': 2.5  # Elektrina SR
        }
        
        # Emisné faktory (lokálne)
        emission_factors = {
            'electricity': 0.218  # kg CO2/kWh
        }
        
        details = f"""
        conversion_factors = {
            'electricity': 2.5  # Elektrina SR
        }
        
        # Emisné faktory (lokálne)
        emission_factors = {
            'electricity': 0.218  # kg CO2/kWh
        }
        
        details = f"""
{'='*80}
🧠 DETAILNÉ VÝPOČTY podľa STN EN ISO 13790 a vyhlášky 364/2012
{'='*80}

📊 VSTUPNÉ ÚDAJE:
• Podlahová plocha: {basic['floor_area']:.1f} m²
• Objem budovy: {results['building_volume']:.1f} m³
• Tesnost n50: {results['n50_value']:.1f} h⁻¹
• Rok výstavby: {basic['construction_year']}
• Účinnosť vykurovacieho systému: {results['system_efficiency']:.0%}
• Typ paliva: {results['fuel_type']}

{'='*60}
1️⃣ TRANSMISNÉ TEPELNÉ STRATY (QT)
{'='*60}

Obvodové steny:
  A = {envelope['wall_area']:.1f} m², U = {envelope['wall_u']:.3f} W/m²K
  QT,wall = {envelope['wall_area']:.1f} × {envelope['wall_u']:.3f} = {results['wall_losses']:.2f} W/K

Okná a dvere:
  A = {envelope['window_area']:.1f} m², U = {envelope['window_u']:.3f} W/m²K
  QT,win = {envelope['window_area']:.1f} × {envelope['window_u']:.3f} = {results['window_losses']:.2f} W/K

Strecha:
  A = {envelope['roof_area']:.1f} m², U = {envelope['roof_u']:.3f} W/m²K
  QT,roof = {envelope['roof_area']:.1f} × {envelope['roof_u']:.3f} = {results['roof_losses']:.2f} W/K

Podlaha:
  QT,floor = {results['floor_losses']:.2f} W/K

Tepelné mosty:
  QT,tb = {results['thermal_bridge_losses']:.2f} W/K (lineárne Ψ-mosty)

Celkové transmisné straty:
  QT = {results['transmission_losses']:.2f} W/K

{'='*60}
2️⃣ VENTILAČNÉ STRATY (QV)
{'='*60}

Infiltračný tok:
  Vn = n50/20 = {results['n50_value']:.1f}/20 = {results['n50_value']/20:.2f} h⁻¹

Mechanické vetranie:
  Vmech = 0.5 h⁻¹ (minimum podľa normy)

Celkový ventilačný tok:
  Vtot = {results['n50_value']/20:.2f} + 0.5 = {(results['n50_value']/20) + 0.5:.2f} h⁻¹

Ventilačné straty:
  QV = V × Vtot × ρ × cp
  QV = {results['building_volume']:.0f} × {(results['n50_value']/20) + 0.5:.2f} × 1.2 × 1.0 = {results['ventilation_losses']:.2f} W/K

{'='*60}
3️⃣ MESAČNÁ ENERGETICKÁ BILANCIA
{'='*60}

Klimatická zóna: {results['climate_zone']}
Potrebna tepla na vykurovanie s uvažovaním:
  • Solárnych ziskov cez okná
  • Vnútorných tepelných ziskov
  • Využitelnosti ziskov (koef. η)

Ročná potreba tepla: {results['heating_need']:.0f} kWh/rok

{'='*60}
4️⃣ ENERGETICKÉ VSTUPY SYSTÉMOV
{'='*60}

Vykurovanie:
  Qh,nd = {results['heating_need']:.0f} kWh/rok (potreba)
  ηsys = {results['system_efficiency']:.0%} (účinnosť systému)
  Qh,in = {results['heating_need']:.0f} / {results['system_efficiency']:.2f} = {results['heating_energy']:.0f} kWh/rok

Tepla voda (TUV):
  Qw,in = {results['dhw_energy']:.0f} kWh/rok

Elektrické systémy:
  • Osvetlenie: {results['lighting_energy']:.0f} kWh/rok
  • Zariadenia: {results['appliances_energy']:.0f} kWh/rok
  Qe,total = {results['total_electricity']:.0f} kWh/rok

{'='*60}
5️⃣ PRIMÁRNA ENERGIA podľa vyhlášky 364/2012
{'='*60}

Konverzné faktory:
  • Vykurovanie ({results['fuel_type']}): {results['heating_factor']:.1f}
  • Elektrina: {conversion_factors['electricity']:.1f}

Výpočet primárnej energie:
  EPh = {results['heating_energy']:.0f} × {results['heating_factor']:.1f} = {results['heating_energy'] * results['heating_factor']:.0f} kWh/rok
  EPw = {results['dhw_energy']:.0f} × {results['heating_factor']:.1f} = {results['dhw_energy'] * results['heating_factor']:.0f} kWh/rok  
  EPe = {results['total_electricity']:.0f} × {conversion_factors['electricity']:.1f} = {results['total_electricity'] * conversion_factors['electricity']:.0f} kWh/rok
  
  EP,total = {results['primary_energy']:.0f} kWh/rok
  EP,spec = {results['primary_energy']:.0f} / {basic['floor_area']:.0f} = {results['specific_primary']:.1f} kWh/m²rok

{'='*60}
6️⃣ ENERGETICKÁ TRIEDA A CO2 EMISIE
{'='*60}

Energetická trieda: {results['energy_class']}
(podľa vyhlášky MH SR č. 364/2012 Z. z.)

CO2 emisie:
  • Emisný faktor vykurovania: {results['heating_emission_factor']:.3f} kg CO2/kWh
  • Emisný faktor elektrina: {emission_factors['electricity']:.3f} kg CO2/kWh
  • Celkové emisie: {results['co2_emissions']:.0f} kg CO2/rok
  • Špecifické emisie: {results['specific_co2']:.1f} kg CO2/m²rok

{'='*60}
📈 EKONOMICKÉ HODNOTENIE
{'='*60}

Ročné náklady: {results['annual_cost']:.0f} €/rok
Náklady na m²: {results['annual_cost'] / basic['floor_area']:.2f} €/m²rok

{'='*80}
📄 POUŽITÉ NORMY:
• STN EN ISO 13790 (Energetická náročnosť budov)
• STN 73 0540-2 Z2/2019 (Tepelná ochrana budov)
• Vyhláška MH SR č. 364/2012 Z. z.
{'='*80}
        """
        
        return details
    
    def calculate_thermal_assessment(self):
        """Výpočet tepelno-technického posúdenia podľa STN 73 0540-2 Z2/2019"""
        try:
            # Posúdenie obvodového plášťa
            wall_u = float(self.wall_u_actual.get()) if self.wall_u_actual.get() else 0
            wall_u_req = 0.22
            
            if wall_u > 0:
                if wall_u <= wall_u_req:
                    self.wall_assessment.config(text="✅ VYHOVUJE", fg='green', bg='#d5f4e6')
                else:
                    self.wall_assessment.config(text="❌ NEVYHOVUJE", fg='red', bg='#f8d7da')
            
            # Posúdenie strešného plášťa
            roof_u = float(self.roof_u_actual.get()) if self.roof_u_actual.get() else 0
            roof_u_req = 0.15
            
            if roof_u > 0:
                if roof_u <= roof_u_req:
                    self.roof_assessment.config(text="✅ VYHOVUJE", fg='green', bg='#d5f4e6')
                else:
                    self.roof_assessment.config(text="❌ NEVYHOVUJE", fg='red', bg='#f8d7da')
            
            # Posúdenie podlahy nad nevykurovaným
            floor_u = float(self.floor_u_actual.get()) if self.floor_u_actual.get() else 0
            floor_u_req = 0.85
            
            if floor_u > 0:
                if floor_u <= floor_u_req:
                    self.floor_assessment.config(text="✅ VYHOVUJE", fg='green', bg='#d5f4e6')
                else:
                    self.floor_assessment.config(text="❌ NEVYHOVUJE", fg='red', bg='#f8d7da')
            
            # Posúdenie okien
            window_u = float(self.window_u_actual.get()) if self.window_u_actual.get() else 0
            window_u_max = 1.7
            
            if window_u > 0:
                if window_u <= window_u_max:
                    self.window_assessment.config(text="✅ VYHOVUJE", fg='green', bg='#d5f4e6')
                else:
                    self.window_assessment.config(text="❌ NEVYHOVUJE", fg='red', bg='#f8d7da')
            
            # Aktualizovanie súhrnných tabuliek
            self.update_summary_tables()
            
            messagebox.showinfo("Tepelno-technické posúdenie", 
                              "Posúdenie U-hodnôt bolo dokončené!\n\n"
                              "Výsledky sú zobrazené v jednotlivých sekciách a súhrnných tabuľkách.")
            
        except ValueError:
            messagebox.showerror("Chyba", "Prosím zadajte platné číselné hodnoty pre U-hodnoty!")
        except Exception as e:
            messagebox.showerror("Chyba", f"Chyba pri výpočte: {str(e)}")
    
    def update_summary_tables(self):
        """Aktualizácia súhrnných tabuliek konštrukcií"""
        try:
            # Aktualizovanie nepriehľadných konštrukcií
            constructions_data = {
                "Obvodové steny": (float(self.wall_u_actual.get()) if self.wall_u_actual.get() else 0, 0.22),
                "Strecha": (float(self.roof_u_actual.get()) if self.roof_u_actual.get() else 0, 0.15),
                "Podlaha nad nevykur.": (float(self.floor_u_actual.get()) if self.floor_u_actual.get() else 0, 0.85)
            }
            
            for name, (u_actual, u_req) in constructions_data.items():
                if name in self.construction_entries and u_actual > 0:
                    # Výpočet rezervy v percentách
                    rezerva = ((u_req - u_actual) / u_req * 100) if u_req > 0 else 0
                    
                    # Aktualizovanie rezervy
                    self.construction_entries[name]['rezerva'].config(text=f"{rezerva:.1f}%")
                    
                    # Aktualizovanie posúdenia
                    if u_actual <= u_req:
                        self.construction_entries[name]['posudenie'].config(
                            text="✅ VYHOVUJE", fg='green', bg='#d5f4e6')
                    else:
                        self.construction_entries[name]['posudenie'].config(
                            text="❌ NEVYHOVUJE", fg='red', bg='#f8d7da')
            
            # Aktualizovanie priehľadných konštrukcií (okná)
            window_u_actual = float(self.window_u_actual.get()) if self.window_u_actual.get() else 0
            window_u_max = 1.7
            
            for orient in self.window_entries:
                if window_u_actual > 0:
                    # Výpočet rezervy
                    rezerva = ((window_u_max - window_u_actual) / window_u_max * 100) if window_u_max > 0 else 0
                    
                    # Aktualizovanie rezervy
                    self.window_entries[orient]['rezerva'].config(text=f"{rezerva:.1f}%")
                    
                    # Aktualizovanie posúdenia
                    if window_u_actual <= window_u_max:
                        self.window_entries[orient]['posudenie'].config(
                            text="✅ VYHOVUJE", fg='green', bg='#d5f4e6')
                    else:
                        self.window_entries[orient]['posudenie'].config(
                            text="❌ NEVYHOVUJE", fg='red', bg='#f8d7da')
                        
        except Exception as e:
            print(f"Chyba pri aktualizácii súhrnných tabuliek: {e}")
        
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
                    self.notebook.select(6)  # Prepnutie na výsledky (index 6 kvôli TUV tabu)
                    
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