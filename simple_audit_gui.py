#!/usr/bin/env python3
"""
JEDNODUCHÁ ENERGY AUDIT GUI APLIKÁCIA
S jasne viditeľným tlačidlom VYKONAŤ AUDIT
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime

class SimpleEnergyAuditGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🏢 Energetický Audit Systém")
        self.root.geometry("1000x700")
        self.root.configure(bg='white')
        
        # Dáta
        self.audit_data = {}
        self.results = {}
        
        self.create_gui()
        
    def create_gui(self):
        """Vytvorenie jednoduchého GUI"""
        
        # HLAVIČKY
        header = tk.Frame(self.root, bg='#2c3e50', height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="🏢 ENERGETICKÝ AUDIT SYSTÉM", 
                font=('Arial', 16, 'bold'), fg='white', bg='#2c3e50').pack(pady=15)
        
        # HLAVNÝ OBSAH
        main_frame = tk.Frame(self.root, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # ĽAVÝ PANEL - FORMULÁR
        left_frame = tk.LabelFrame(main_frame, text="📋 ZADANIE ÚDAJOV", 
                                  font=('Arial', 12, 'bold'), bg='white')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.create_input_form(left_frame)
        
        # PRAVÝ PANEL - VÝSLEDKY
        right_frame = tk.LabelFrame(main_frame, text="📊 VÝSLEDKY", 
                                   font=('Arial', 12, 'bold'), bg='white')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.results_text = scrolledtext.ScrolledText(right_frame, height=25, width=50)
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.results_text.insert(tk.END, "Výsledky sa zobrazia po vykonaní auditu...")
        
        # SPODNÝ PANEL - VEĽKÉ TLAČIDLÁ
        self.create_bottom_buttons()
        
    def create_input_form(self, parent):
        """Vytvorenie formulára pre vstupné údaje"""
        
        # Scrollable frame
        canvas = tk.Canvas(parent, bg='white')
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 1. ZÁKLADNÉ ÚDAJE
        basic_frame = tk.LabelFrame(scrollable_frame, text="🏢 Základné údaje", bg='white')
        basic_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(basic_frame, text="Názov budovy:", bg='white').grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.building_name = tk.Entry(basic_frame, width=30)
        self.building_name.grid(row=0, column=1, padx=5, pady=3)
        self.building_name.insert(0, "Testovacia budova")
        
        tk.Label(basic_frame, text="Podlahová plocha [m²]:", bg='white').grid(row=1, column=0, sticky=tk.W, padx=5, pady=3)
        self.floor_area = tk.Entry(basic_frame, width=30)
        self.floor_area.grid(row=1, column=1, padx=5, pady=3)
        self.floor_area.insert(0, "120")
        
        tk.Label(basic_frame, text="Rok výstavby:", bg='white').grid(row=2, column=0, sticky=tk.W, padx=5, pady=3)
        self.construction_year = tk.Entry(basic_frame, width=30)
        self.construction_year.grid(row=2, column=1, padx=5, pady=3)
        self.construction_year.insert(0, "2000")
        
        # 2. OBÁLKA BUDOVY
        envelope_frame = tk.LabelFrame(scrollable_frame, text="🏠 Obálka budovy", bg='white')
        envelope_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(envelope_frame, text="Plocha stien [m²]:", bg='white').grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.wall_area = tk.Entry(envelope_frame, width=30)
        self.wall_area.grid(row=0, column=1, padx=5, pady=3)
        self.wall_area.insert(0, "150")
        
        tk.Label(envelope_frame, text="U-hodnota stien [W/m²K]:", bg='white').grid(row=1, column=0, sticky=tk.W, padx=5, pady=3)
        self.wall_u = tk.Entry(envelope_frame, width=30)
        self.wall_u.grid(row=1, column=1, padx=5, pady=3)
        self.wall_u.insert(0, "0.25")
        
        tk.Label(envelope_frame, text="Plocha okien [m²]:", bg='white').grid(row=2, column=0, sticky=tk.W, padx=5, pady=3)
        self.window_area = tk.Entry(envelope_frame, width=30)
        self.window_area.grid(row=2, column=1, padx=5, pady=3)
        self.window_area.insert(0, "25")
        
        tk.Label(envelope_frame, text="U-hodnota okien [W/m²K]:", bg='white').grid(row=3, column=0, sticky=tk.W, padx=5, pady=3)
        self.window_u = tk.Entry(envelope_frame, width=30)
        self.window_u.grid(row=3, column=1, padx=5, pady=3)
        self.window_u.insert(0, "1.1")
        
        # 3. SYSTÉMY
        systems_frame = tk.LabelFrame(scrollable_frame, text="⚙️ Systémy", bg='white')
        systems_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(systems_frame, text="Typ vykurovania:", bg='white').grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.heating_type = ttk.Combobox(systems_frame, values=["Plynový kotol", "Elektrické", "Tepelné čerpadlo"])
        self.heating_type.grid(row=0, column=1, padx=5, pady=3)
        self.heating_type.set("Plynový kotol")
        
        tk.Label(systems_frame, text="Účinnosť vykurovania [%]:", bg='white').grid(row=1, column=0, sticky=tk.W, padx=5, pady=3)
        self.heating_efficiency = tk.Entry(systems_frame, width=30)
        self.heating_efficiency.grid(row=1, column=1, padx=5, pady=3)
        self.heating_efficiency.insert(0, "90")
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_bottom_buttons(self):
        """Vytvorenie spodných tlačidiel"""
        
        # VEĽKÝ SPODNÝ PANEL
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
        
        # HLAVNÉ TLAČIDLO - VEĽKÉ A ZELENÉ
        self.audit_button = tk.Button(buttons_frame, 
                                     text="🔬 VYKONAŤ ENERGETICKÝ AUDIT",
                                     command=self.perform_audit,
                                     bg='#27ae60', fg='white',
                                     font=('Arial', 16, 'bold'),
                                     width=25, height=2,
                                     relief=tk.RAISED, bd=5)
        self.audit_button.pack(side=tk.LEFT, padx=20)
        
        # OSTATNÉ TLAČIDLÁ
        tk.Button(buttons_frame, text="💾 ULOŽIŤ",
                 command=self.save_project, bg='#3498db', fg='white',
                 font=('Arial', 10, 'bold'), width=12, height=2).pack(side=tk.LEFT, padx=5)
        
        tk.Button(buttons_frame, text="🏅 CERTIFIKÁT", 
                 command=self.generate_certificate, bg='#9b59b6', fg='white',
                 font=('Arial', 10, 'bold'), width=12, height=2).pack(side=tk.LEFT, padx=5)
        
        tk.Button(buttons_frame, text="❌ UKONČIŤ",
                 command=self.root.quit, bg='#e74c3c', fg='white',
                 font=('Arial', 10, 'bold'), width=12, height=2).pack(side=tk.RIGHT, padx=20)
        
    def collect_data(self):
        """Zber údajov z formulára"""
        try:
            self.audit_data = {
                'building': {
                    'name': self.building_name.get() or "Test budova",
                    'floor_area': float(self.floor_area.get() or 120),
                    'construction_year': int(self.construction_year.get() or 2000)
                },
                'envelope': {
                    'wall_area': float(self.wall_area.get() or 150),
                    'wall_u': float(self.wall_u.get() or 0.25),
                    'window_area': float(self.window_area.get() or 25),
                    'window_u': float(self.window_u.get() or 1.1)
                },
                'systems': {
                    'heating_type': self.heating_type.get() or "Plynový kotol",
                    'heating_efficiency': float(self.heating_efficiency.get() or 90) / 100
                }
            }
            return True
        except ValueError as e:
            messagebox.showerror("Chyba", f"Neplatné údaje: {e}")
            return False
        
    def perform_audit(self):
        """HLAVNÁ FUNKCIA - Vykonanie auditu"""
        
        # Zber údajov
        if not self.collect_data():
            return
            
        self.audit_button.config(text="⏳ PREBIEHA AUDIT...", state=tk.DISABLED)
        self.progress['value'] = 0
        self.root.update()
        
        try:
            # Simulácia výpočtu
            self.progress['value'] = 25
            self.root.update()
            
            # Základné výpočty
            building = self.audit_data['building']
            envelope = self.audit_data['envelope']
            systems = self.audit_data['systems']
            
            # Tepelné straty
            wall_losses = envelope['wall_area'] * envelope['wall_u']
            window_losses = envelope['window_area'] * envelope['window_u'] 
            total_losses = wall_losses + window_losses
            
            self.progress['value'] = 50
            self.root.update()
            
            # Potreba tepla
            hdd = 2800  # Bratislava
            heating_need = total_losses * hdd * 24 / 1000  # kWh/rok
            
            # Spotreba energie
            heating_energy = heating_need / systems['heating_efficiency']
            electricity = building['floor_area'] * 15  # kWh/m²rok
            total_energy = heating_energy + electricity
            
            self.progress['value'] = 75
            self.root.update()
            
            # Primárna energia a trieda
            primary_energy = heating_energy * 1.1 + electricity * 3.0
            specific_primary = primary_energy / building['floor_area']
            
            # Určenie triedy
            if specific_primary <= 50:
                energy_class = 'A'
            elif specific_primary <= 110:
                energy_class = 'C'  
            elif specific_primary <= 150:
                energy_class = 'D'
            elif specific_primary <= 200:
                energy_class = 'E'
            else:
                energy_class = 'F'
                
            # CO2 emisie
            co2_emissions = heating_energy * 0.202 + electricity * 0.486
            specific_co2 = co2_emissions / building['floor_area']
            
            self.progress['value'] = 100
            self.root.update()
            
            # Uloženie výsledkov
            self.results = {
                'total_energy': total_energy,
                'heating_energy': heating_energy, 
                'electricity': electricity,
                'primary_energy': primary_energy,
                'specific_primary': specific_primary,
                'energy_class': energy_class,
                'co2_emissions': co2_emissions,
                'specific_co2': specific_co2,
                'total_losses': total_losses
            }
            
            # Zobrazenie výsledkov
            self.display_results()
            
            messagebox.showinfo("Úspech", "✅ Energetický audit dokončený!")
            
        except Exception as e:
            messagebox.showerror("Chyba", f"Chyba pri výpočte: {e}")
        finally:
            self.audit_button.config(text="🔬 VYKONAŤ ENERGETICKÝ AUDIT", state=tk.NORMAL)
            self.progress['value'] = 0
            
    def display_results(self):
        """Zobrazenie výsledkov"""
        self.results_text.delete(1.0, tk.END)
        
        building = self.audit_data['building']
        results = self.results
        
        output = f"""
{'='*50}
📋 ENERGETICKÝ AUDIT - VÝSLEDKY
{'='*50}

🏢 BUDOVA: {building['name']}
📐 Podlahová plocha: {building['floor_area']:.0f} m²
📅 Rok výstavby: {building['construction_year']}

⚡ ENERGETICKÁ BILANCIA:
├─ Vykurovanie: {results['heating_energy']:.0f} kWh/rok
├─ Elektrina: {results['electricity']:.0f} kWh/rok  
└─ CELKOM: {results['total_energy']:.0f} kWh/rok

🎯 ENERGETICKÉ HODNOTENIE:
├─ Energetická trieda: {results['energy_class']}
├─ Primárna energia: {results['specific_primary']:.1f} kWh/m²rok
├─ CO2 emisie: {results['specific_co2']:.1f} kg/m²rok
└─ Tepelné straty: {results['total_losses']:.1f} W/K

💡 ODPORÚČANIA:
"""
        
        # Generovanie odporúčaní
        recommendations = []
        envelope = self.audit_data['envelope']
        
        if envelope['wall_u'] > 0.30:
            recommendations.append("• Zateplenie stien (úspory 25-35%)")
        if envelope['window_u'] > 2.0:
            recommendations.append("• Výmena okien (úspory 15-20%)")
        if self.audit_data['systems']['heating_efficiency'] < 0.85:
            recommendations.append("• Modernizácia vykurovania (úspory 20-30%)")
        
        if recommendations:
            output += "\n".join(recommendations)
        else:
            output += "• Budova je v dobrom energetikom stave"
            
        output += f"\n\n📋 CERTIFIKÁCIA:\n"
        output += f"🏅 Energetická trieda: {results['energy_class']}\n"
        output += f"⚡ Primárna energia: {results['specific_primary']:.1f} kWh/m²rok\n"
        output += f"🌍 CO2 emisie: {results['specific_co2']:.1f} kg CO2/m²rok\n"
        
        self.results_text.insert(tk.END, output)
        
    def save_project(self):
        """Uloženie projektu"""
        if not self.audit_data:
            messagebox.showwarning("Upozornenie", "Nie je čo uložiť.")
            return
        messagebox.showinfo("Info", "Funkcionalita ukladania bude implementovaná.")
        
    def generate_certificate(self):
        """Generovanie certifikátu"""
        if not self.results:
            messagebox.showwarning("Upozornenie", "Najprv vykonajte audit.")
            return
            
        # Vytvorenie certifikátu
        building = self.audit_data['building']
        results = self.results
        
        certificate_info = f"""
🏅 ENERGETICKÝ CERTIFIKÁT

Budova: {building['name']}
Číslo certifikátu: EC-{datetime.now().strftime('%Y%m%d%H%M')}

Energetická trieda: {results['energy_class']}
Primárna energia: {results['specific_primary']:.1f} kWh/m²rok
CO2 emisie: {results['specific_co2']:.1f} kg CO2/m²rok

Dátum vydania: {datetime.now().strftime('%d.%m.%Y')}
Platnosť do: {datetime.now().replace(year=datetime.now().year + 10).strftime('%d.%m.%Y')}
"""
        
        messagebox.showinfo("Certifikát", certificate_info)

def main():
    """Spustenie aplikácie"""
    root = tk.Tk()
    app = SimpleEnergyAuditGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()