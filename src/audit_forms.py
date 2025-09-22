"""
Formuláre a GUI komponenty pre správu energetických auditov
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, date
from typing import Dict, Any, Optional, Callable
import json

try:
    from .config import BUILDING_TYPES, HEATING_TYPES, ENERGY_CLASSES
    from .database import get_db_manager
except ImportError:
    from config import BUILDING_TYPES, HEATING_TYPES, ENERGY_CLASSES
    from database import get_db_manager


class AuditFormDialog:
    """Dialógové okno pre vytvorenie/editáciu auditu"""
    
    def __init__(self, parent, audit_data=None, on_save_callback=None):
        """
        Inicializácia dialógu
        
        Args:
            parent: Rodičovské okno
            audit_data: Existujúce údaje auditu (pre editáciu)
            on_save_callback: Callback funkcia po uložení
        """
        self.parent = parent
        self.audit_data = audit_data or {}
        self.on_save_callback = on_save_callback
        self.result = None
        self.db_manager = get_db_manager()
        
        self.setup_dialog()
        self.create_form()
        self.populate_form()
    
    def setup_dialog(self):
        """Nastavenie dialógového okna"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Nový audit" if not self.audit_data else "Upraviť audit")
        self.dialog.geometry("800x700")
        self.dialog.resizable(True, True)
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Centrovanie okna
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (700 // 2)
        self.dialog.geometry(f"800x700+{x}+{y}")
    
    def create_form(self):
        """Vytvorenie formuláru"""
        # Hlavný frame s posuvníkom
        main_canvas = tk.Canvas(self.dialog)
        scrollbar = ttk.Scrollbar(self.dialog, orient="vertical", command=main_canvas.yview)
        scrollable_frame = ttk.Frame(main_canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Notebook pre záložky
        self.notebook = ttk.Notebook(scrollable_frame, padding="10")
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Záložka základných informácií
        self.create_basic_info_tab()
        
        # Záložka stavebných údajov
        self.create_building_info_tab()
        
        # Záložka systémov
        self.create_systems_tab()
        
        # Záložka audítora
        self.create_auditor_tab()
        
        # Tlačidlá
        self.create_buttons(scrollable_frame)
        
        # Packing
        main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_basic_info_tab(self):
        """Záložka základných informácií"""
        basic_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(basic_frame, text="Základné údaje")
        
        # Názov auditu
        ttk.Label(basic_frame, text="Názov auditu:*").grid(row=0, column=0, sticky="w", pady=2)
        self.audit_name_var = tk.StringVar()
        ttk.Entry(basic_frame, textvariable=self.audit_name_var, width=50).grid(row=0, column=1, sticky="ew", padx=(5,0), pady=2)
        
        # Názov budovy
        ttk.Label(basic_frame, text="Názov budovy:*").grid(row=1, column=0, sticky="w", pady=2)
        self.building_name_var = tk.StringVar()
        ttk.Entry(basic_frame, textvariable=self.building_name_var, width=50).grid(row=1, column=1, sticky="ew", padx=(5,0), pady=2)
        
        # Adresa budovy
        ttk.Label(basic_frame, text="Adresa budovy:").grid(row=2, column=0, sticky="w", pady=2)
        self.building_address_var = tk.StringVar()
        ttk.Entry(basic_frame, textvariable=self.building_address_var, width=50).grid(row=2, column=1, sticky="ew", padx=(5,0), pady=2)
        
        # Typ budovy
        ttk.Label(basic_frame, text="Typ budovy:").grid(row=3, column=0, sticky="w", pady=2)
        self.building_type_var = tk.StringVar()
        building_type_combo = ttk.Combobox(basic_frame, textvariable=self.building_type_var, values=BUILDING_TYPES, width=47)
        building_type_combo.grid(row=3, column=1, sticky="ew", padx=(5,0), pady=2)
        building_type_combo.state(['readonly'])
        
        # Rok výstavby
        ttk.Label(basic_frame, text="Rok výstavby:").grid(row=4, column=0, sticky="w", pady=2)
        self.construction_year_var = tk.IntVar()
        year_spinbox = ttk.Spinbox(basic_frame, from_=1800, to=datetime.now().year, textvariable=self.construction_year_var, width=48)
        year_spinbox.grid(row=4, column=1, sticky="ew", padx=(5,0), pady=2)
        
        basic_frame.columnconfigure(1, weight=1)
    
    def create_building_info_tab(self):
        """Záložka stavebných údajov"""
        building_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(building_frame, text="Stavebné údaje")
        
        # Celková podlahová plocha
        ttk.Label(building_frame, text="Celková podlahová plocha (m²):*").grid(row=0, column=0, sticky="w", pady=2)
        self.total_area_var = tk.DoubleVar()
        ttk.Entry(building_frame, textvariable=self.total_area_var, width=20).grid(row=0, column=1, sticky="w", padx=(5,0), pady=2)
        
        # Vykurovaná plocha
        ttk.Label(building_frame, text="Vykurovaná plocha (m²):*").grid(row=1, column=0, sticky="w", pady=2)
        self.heated_area_var = tk.DoubleVar()
        ttk.Entry(building_frame, textvariable=self.heated_area_var, width=20).grid(row=1, column=1, sticky="w", padx=(5,0), pady=2)
        
        # Počet podlaží
        ttk.Label(building_frame, text="Počet podlaží:").grid(row=2, column=0, sticky="w", pady=2)
        self.number_of_floors_var = tk.IntVar()
        ttk.Spinbox(building_frame, from_=1, to=20, textvariable=self.number_of_floors_var, width=18).grid(row=2, column=1, sticky="w", padx=(5,0), pady=2)
        
        # Poznámky
        ttk.Label(building_frame, text="Poznámky:").grid(row=3, column=0, sticky="nw", pady=(10,2))
        self.notes_text = tk.Text(building_frame, width=60, height=10, wrap=tk.WORD)
        self.notes_text.grid(row=3, column=1, columnspan=2, sticky="ew", padx=(5,0), pady=(10,2))
        
        # Scrollbar pre poznámky
        notes_scrollbar = ttk.Scrollbar(building_frame, orient="vertical", command=self.notes_text.yview)
        notes_scrollbar.grid(row=3, column=3, sticky="ns", pady=(10,2))
        self.notes_text.configure(yscrollcommand=notes_scrollbar.set)
        
        building_frame.columnconfigure(1, weight=1)
    
    def create_systems_tab(self):
        """Záložka technických systémov"""
        systems_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(systems_frame, text="Technické systémy")
        
        # Frame pre vykurovanie
        heating_frame = ttk.LabelFrame(systems_frame, text="Vykurovací systém", padding="5")
        heating_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0,10))
        
        ttk.Label(heating_frame, text="Typ vykurovania:").grid(row=0, column=0, sticky="w", pady=2)
        self.heating_type_var = tk.StringVar()
        heating_combo = ttk.Combobox(heating_frame, textvariable=self.heating_type_var, values=HEATING_TYPES, width=30)
        heating_combo.grid(row=0, column=1, sticky="ew", padx=(5,0), pady=2)
        heating_combo.state(['readonly'])
        
        ttk.Label(heating_frame, text="Účinnosť (%):").grid(row=1, column=0, sticky="w", pady=2)
        self.heating_efficiency_var = tk.DoubleVar()
        ttk.Entry(heating_frame, textvariable=self.heating_efficiency_var, width=15).grid(row=1, column=1, sticky="w", padx=(5,0), pady=2)
        
        heating_frame.columnconfigure(1, weight=1)
        
        # Frame pre teplú vodu
        hotwater_frame = ttk.LabelFrame(systems_frame, text="Systém teplej vody", padding="5")
        hotwater_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0,10))
        
        ttk.Label(hotwater_frame, text="Typ systému:").grid(row=0, column=0, sticky="w", pady=2)
        self.hotwater_type_var = tk.StringVar()
        hotwater_combo = ttk.Combobox(hotwater_frame, textvariable=self.hotwater_type_var, values=["Elektrický bojler", "Plynový bojler", "Solárny systém", "Kombinovaný systém"], width=30)
        hotwater_combo.grid(row=0, column=1, sticky="ew", padx=(5,0), pady=2)
        
        ttk.Label(hotwater_frame, text="Objem zásobníka (l):").grid(row=1, column=0, sticky="w", pady=2)
        self.hotwater_volume_var = tk.DoubleVar()
        ttk.Entry(hotwater_frame, textvariable=self.hotwater_volume_var, width=15).grid(row=1, column=1, sticky="w", padx=(5,0), pady=2)
        
        hotwater_frame.columnconfigure(1, weight=1)
        
        systems_frame.columnconfigure(0, weight=1)
    
    def create_auditor_tab(self):
        """Záložka údajov o audítorovi"""
        auditor_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(auditor_frame, text="Audítor")
        
        # Meno audítora
        ttk.Label(auditor_frame, text="Meno audítora:").grid(row=0, column=0, sticky="w", pady=2)
        self.auditor_name_var = tk.StringVar()
        ttk.Entry(auditor_frame, textvariable=self.auditor_name_var, width=50).grid(row=0, column=1, sticky="ew", padx=(5,0), pady=2)
        
        # Číslo licencie
        ttk.Label(auditor_frame, text="Číslo licencie:").grid(row=1, column=0, sticky="w", pady=2)
        self.auditor_license_var = tk.StringVar()
        ttk.Entry(auditor_frame, textvariable=self.auditor_license_var, width=50).grid(row=1, column=1, sticky="ew", padx=(5,0), pady=2)
        
        # Stav auditu
        ttk.Label(auditor_frame, text="Stav auditu:").grid(row=2, column=0, sticky="w", pady=2)
        self.status_var = tk.StringVar(value="draft")
        status_combo = ttk.Combobox(auditor_frame, textvariable=self.status_var, 
                                  values=["draft", "in_progress", "completed", "certified"], width=47)
        status_combo.grid(row=2, column=1, sticky="ew", padx=(5,0), pady=2)
        status_combo.state(['readonly'])
        
        auditor_frame.columnconfigure(1, weight=1)
    
    def create_buttons(self, parent):
        """Vytvorenie tlačidiel"""
        button_frame = ttk.Frame(parent, padding="10")
        button_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        ttk.Button(button_frame, text="Zrušiť", command=self.cancel).pack(side=tk.RIGHT, padx=(5,0))
        ttk.Button(button_frame, text="Uložiť", command=self.save).pack(side=tk.RIGHT)
    
    def populate_form(self):
        """Naplnenie formuláru existujúcimi údajmi"""
        if not self.audit_data:
            return
            
        # Základné údaje
        self.audit_name_var.set(self.audit_data.get('audit_name', ''))
        self.building_name_var.set(self.audit_data.get('building_name', ''))
        self.building_address_var.set(self.audit_data.get('building_address', ''))
        self.building_type_var.set(self.audit_data.get('building_type', ''))
        self.construction_year_var.set(self.audit_data.get('construction_year', datetime.now().year))
        
        # Stavebné údaje
        self.total_area_var.set(self.audit_data.get('total_area', 0.0))
        self.heated_area_var.set(self.audit_data.get('heated_area', 0.0))
        self.number_of_floors_var.set(self.audit_data.get('number_of_floors', 1))
        
        # Poznámky
        self.notes_text.insert('1.0', self.audit_data.get('notes', ''))
        
        # Audítor
        self.auditor_name_var.set(self.audit_data.get('auditor_name', ''))
        self.auditor_license_var.set(self.audit_data.get('auditor_license', ''))
        self.status_var.set(self.audit_data.get('status', 'draft'))
    
    def validate_form(self) -> bool:
        """Validácia formuláru"""
        errors = []
        
        if not self.audit_name_var.get().strip():
            errors.append("Názov auditu je povinný")
        
        if not self.building_name_var.get().strip():
            errors.append("Názov budovy je povinný")
        
        if self.total_area_var.get() <= 0:
            errors.append("Celková plocha musí byť väčšia ako 0")
        
        if self.heated_area_var.get() <= 0:
            errors.append("Vykurovaná plocha musí byť väčšia ako 0")
        
        if self.heated_area_var.get() > self.total_area_var.get():
            errors.append("Vykurovaná plocha nemôže byť väčšia ako celková plocha")
        
        if errors:
            messagebox.showerror("Chyby vo formulári", "\\n".join(errors))
            return False
        
        return True
    
    def collect_form_data(self) -> Dict[str, Any]:
        """Zber údajov z formuláru"""
        return {
            'audit_name': self.audit_name_var.get().strip(),
            'building_name': self.building_name_var.get().strip(),
            'building_address': self.building_address_var.get().strip(),
            'building_type': self.building_type_var.get(),
            'construction_year': self.construction_year_var.get(),
            'total_area': self.total_area_var.get(),
            'heated_area': self.heated_area_var.get(),
            'number_of_floors': self.number_of_floors_var.get(),
            'notes': self.notes_text.get('1.0', tk.END).strip(),
            'auditor_name': self.auditor_name_var.get().strip(),
            'auditor_license': self.auditor_license_var.get().strip(),
            'status': self.status_var.get()
        }
    
    def save(self):
        """Uloženie auditu"""
        if not self.validate_form():
            return
        
        try:
            form_data = self.collect_form_data()
            
            if self.audit_data and 'id' in self.audit_data:
                # Aktualizácia existujúceho auditu
                success = self.db_manager.update_audit(self.audit_data['id'], form_data)
                if success:
                    messagebox.showinfo("Úspech", "Audit bol úspešne aktualizovaný")
                    self.result = {'action': 'updated', 'id': self.audit_data['id'], 'data': form_data}
                else:
                    messagebox.showerror("Chyba", "Nepodarilo sa aktualizovať audit")
                    return
            else:
                # Vytvorenie nového auditu
                audit_id = self.db_manager.create_audit(form_data)
                messagebox.showinfo("Úspech", f"Audit bol úspešne vytvorený s ID: {audit_id}")
                self.result = {'action': 'created', 'id': audit_id, 'data': form_data}
            
            if self.on_save_callback:
                self.on_save_callback(self.result)
            
            self.dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("Chyba", f"Nepodarilo sa uložiť audit: {str(e)}")
    
    def cancel(self):
        """Zrušenie dialógu"""
        self.dialog.destroy()


class AuditListFrame:
    """Frame pre zobrazenie zoznamu auditov"""
    
    def __init__(self, parent, on_audit_select=None):
        """
        Inicializácia zoznamu auditov
        
        Args:
            parent: Rodičovský widget
            on_audit_select: Callback pri výbere auditu
        """
        self.parent = parent
        self.on_audit_select = on_audit_select
        self.db_manager = get_db_manager()
        
        self.create_widgets()
        self.refresh_list()
    
    def create_widgets(self):
        """Vytvorenie widgetov"""
        # Hlavný frame
        self.frame = ttk.Frame(self.parent, padding="5")
        
        # Toolbar
        toolbar = ttk.Frame(self.frame)
        toolbar.pack(fill=tk.X, pady=(0,5))
        
        ttk.Button(toolbar, text="Nový audit", command=self.new_audit).pack(side=tk.LEFT, padx=(0,5))
        ttk.Button(toolbar, text="Upraviť", command=self.edit_audit).pack(side=tk.LEFT, padx=(0,5))
        ttk.Button(toolbar, text="Vymazať", command=self.delete_audit).pack(side=tk.LEFT, padx=(0,5))
        ttk.Button(toolbar, text="Obnoviť", command=self.refresh_list).pack(side=tk.LEFT, padx=(10,0))
        
        # Treeview pre zoznam auditov
        columns = ("ID", "Názov auditu", "Budova", "Typ", "Vytvorené", "Stav")
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings", height=15)
        
        # Nastavenie stĺpcov
        self.tree.heading("ID", text="ID")
        self.tree.heading("Názov auditu", text="Názov auditu")
        self.tree.heading("Budova", text="Budova")
        self.tree.heading("Typ", text="Typ")
        self.tree.heading("Vytvorené", text="Vytvorené")
        self.tree.heading("Stav", text="Stav")
        
        self.tree.column("ID", width=50)
        self.tree.column("Názov auditu", width=200)
        self.tree.column("Budova", width=150)
        self.tree.column("Typ", width=120)
        self.tree.column("Vytvorené", width=100)
        self.tree.column("Stav", width=80)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(self.frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Packing
        self.tree.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        
        # Bind events
        self.tree.bind("<Double-1>", self.on_double_click)
        self.tree.bind("<Button-3>", self.show_context_menu)  # Pravé tlačidlo myši
    
    def refresh_list(self):
        """Obnovenie zoznamu auditov"""
        # Vyčistenie existujúcich položiek
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Načítanie auditov z databázy
        audits = self.db_manager.get_all_audits()
        
        for audit in audits:
            # Formátovanie dátumu
            created_date = audit.get('created_date', '')
            if created_date:
                try:
                    date_obj = datetime.fromisoformat(created_date)
                    formatted_date = date_obj.strftime('%d.%m.%Y')
                except:
                    formatted_date = created_date[:10]  # Fallback
            else:
                formatted_date = ""
            
            # Pridanie položky do stromu
            self.tree.insert("", "end", values=(
                audit.get('id', ''),
                audit.get('audit_name', ''),
                audit.get('building_name', ''),
                audit.get('building_type', ''),
                formatted_date,
                audit.get('status', '')
            ))
    
    def get_selected_audit_id(self) -> Optional[int]:
        """Získanie ID vybraného auditu"""
        selection = self.tree.selection()
        if not selection:
            return None
        
        item = self.tree.item(selection[0])
        return int(item['values'][0]) if item['values'] else None
    
    def new_audit(self):
        """Vytvorenie nového auditu"""
        dialog = AuditFormDialog(self.parent, on_save_callback=self.on_audit_saved)
    
    def edit_audit(self):
        """Úprava vybraného auditu"""
        audit_id = self.get_selected_audit_id()
        if not audit_id:
            messagebox.showwarning("Upozornenie", "Prosím vyberte audit na úpravu")
            return
        
        # Načítanie údajov auditu
        audit_data = self.db_manager.get_audit(audit_id)
        if not audit_data:
            messagebox.showerror("Chyba", "Nepodarilo sa načítať audit")
            return
        
        dialog = AuditFormDialog(self.parent, audit_data=audit_data, on_save_callback=self.on_audit_saved)
    
    def delete_audit(self):
        """Vymazanie vybraného auditu"""
        audit_id = self.get_selected_audit_id()
        if not audit_id:
            messagebox.showwarning("Upozornenie", "Prosím vyberte audit na vymazanie")
            return
        
        # Potvrdenie vymazania
        result = messagebox.askyesno("Potvrdenie", 
                                   "Naozaj chcete vymazať tento audit?\\n\\n"
                                   "Táto operácia je nevratná a vymaže aj všetky súvisiace údaje.")
        
        if result:
            try:
                success = self.db_manager.delete_audit(audit_id)
                if success:
                    messagebox.showinfo("Úspech", "Audit bol úspešne vymazaný")
                    self.refresh_list()
                else:
                    messagebox.showerror("Chyba", "Nepodarilo sa vymazať audit")
            except Exception as e:
                messagebox.showerror("Chyba", f"Nepodarilo sa vymazať audit: {str(e)}")
    
    def on_double_click(self, event):
        """Obsluha dvojkliku na audit"""
        audit_id = self.get_selected_audit_id()
        if audit_id and self.on_audit_select:
            self.on_audit_select(audit_id)
    
    def on_audit_saved(self, result):
        """Callback po uložení auditu"""
        self.refresh_list()
    
    def show_context_menu(self, event):
        """Zobrazenie kontextového menu"""
        # TODO: Implementovať kontextové menu
        pass
    
    def pack(self, **kwargs):
        """Pack metóda pre frame"""
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        """Grid metóda pre frame"""
        self.frame.grid(**kwargs)


def show_audit_form(parent, audit_data=None, on_save_callback=None):
    """
    Zobrazenie formuláru auditu
    
    Args:
        parent: Rodičovské okno
        audit_data: Existujúce údaje auditu (pre editáciu)
        on_save_callback: Callback funkcia po uložení
        
    Returns:
        Výsledok z dialógu
    """
    dialog = AuditFormDialog(parent, audit_data, on_save_callback)
    parent.wait_window(dialog.dialog)
    return dialog.result