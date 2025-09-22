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

# Pridanie src adresára do Python cesty
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

class EnergyAuditApp:
    """Hlavná trieda aplikácie pre energetický audit"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Energy Audit - Energetický Audit Budov")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
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
        
        # Uvítací tab
        welcome_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(welcome_frame, text="Úvod")
        
        welcome_label = ttk.Label(welcome_frame, 
                                text="Vitajte v aplikácii Energy Audit\n\n"
                                     "Táto aplikácia vám pomôže:\n"
                                     "• Vykonať energetický audit budovy\n"
                                     "• Vygenerovať certifikát energetickej efektívnosti\n"
                                     "• Spravovať databázu auditov\n\n"
                                     "Pre začatie vyberte 'Nový Audit' z menu alebo použite tlačidlo v ľavom paneli.",
                                font=('Arial', 12))
        welcome_label.pack(expand=True)
        
    # Metódy pre menu akcie
    def new_audit(self):
        """Vytvorenie nového auditu"""
        messagebox.showinfo("Nový Audit", "Funkcia 'Nový Audit' bude implementovaná.")
        
    def open_audit(self):
        """Otvorenie existujúceho auditu"""
        messagebox.showinfo("Otvoriť Audit", "Funkcia 'Otvoriť Audit' bude implementovaná.")
        
    def save_audit(self):
        """Uloženie aktuálneho auditu"""
        messagebox.showinfo("Uložiť Audit", "Funkcia 'Uložiť Audit' bude implementovaná.")
        
    def energy_calculator(self):
        """Spustenie kalkulačky energií"""
        messagebox.showinfo("Kalkulačka", "Funkcia 'Kalkulačka energií' bude implementovaná.")
        
    def certificate_generator(self):
        """Spustenie generátora certifikátu"""
        messagebox.showinfo("Certifikát", "Funkcia 'Generátor certifikátu' bude implementovaná.")
        
    def about(self):
        """Zobrazenie informácií o aplikácii"""
        messagebox.showinfo("O aplikácii", 
                          "Energy Audit Desktop Application\n"
                          "Verzia 1.0.0\n\n"
                          "Aplikácia na vykonávanie energetického auditu\n"
                          "a certifikáciu budov.")

def main():
    """Hlavná funkcia aplikácie"""
    root = tk.Tk()
    app = EnergyAuditApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()