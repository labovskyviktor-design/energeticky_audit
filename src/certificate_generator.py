"""
Generátor certifikátov energetickej efektívnosti
Vytvára PDF certifikáty v slovenčine podľa európskych štandardov
"""

import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional
import uuid

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.colors import Color, HexColor, black, white
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm, mm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
    from reportlab.platypus.flowables import BalancedColumns, KeepTogether
    from reportlab.graphics.shapes import Drawing, Rect, String
    from reportlab.graphics.charts.barcharts import VerticalBarChart
    from reportlab.graphics import renderPDF
    REPORTLAB_AVAILABLE = True
except ImportError:
    print("Upozornenie: reportlab nie je nainštalovaný. Nainštalujte ho príkazom: pip install reportlab")
    # Fallback pre prípad chýbajúcej knižnice
    A4 = (595.27, 841.89)
    REPORTLAB_AVAILABLE = False
    
    # Dummy classes pre compatibility
    class Drawing: pass
    class HexColor: 
        def __init__(self, color): self.color = color
    class ParagraphStyle: pass
    class SimpleDocTemplate: pass
    class Paragraph: pass
    class Spacer: pass
    class Table: pass
    class TableStyle: pass
    class Rect: pass
    class String: pass
    def getSampleStyleSheet(): return {}
    cm = 28.35
    black = "#000000"
    white = "#FFFFFF"

try:
    from .config import ENERGY_CLASSES, EXPORT_DIR, ensure_directories
    from .database import get_db_manager
    from .energy_calculations import get_energy_calculator
except ImportError:
    from config import ENERGY_CLASSES, EXPORT_DIR, ensure_directories
    from database import get_db_manager
    from energy_calculations import get_energy_calculator


class CertificateGenerator:
    """Generátor energetických certifikátov"""
    
    def __init__(self):
        """Inicializácia generátora"""
        ensure_directories()
        self.db_manager = get_db_manager()
        self.calculator = get_energy_calculator()
        
        if REPORTLAB_AVAILABLE:
            # Nastavenie základných vlastností certifikátu
            self.page_width, self.page_height = A4
            self.margin = 2.5 * cm
            self.content_width = self.page_width - 2 * self.margin
            
            # Farby pre energetické triedy
            self.energy_class_colors = {
                class_name: HexColor(class_data["color"])
                for class_name, class_data in ENERGY_CLASSES.items()
            }
            
            # Štýly pre text
            self.setup_styles()
        else:
            # Dummy inicializácia ak reportlab nie je dostupný
            self.page_width, self.page_height = A4
            self.margin = 2.5 * 28.35  # cm fallback
            self.content_width = self.page_width - 2 * self.margin
            self.energy_class_colors = {}
            self.styles = {}
    
    def setup_styles(self):
        """Nastavenie textových štýlov"""
        if not REPORTLAB_AVAILABLE:
            self.styles = {}
            return
            
        self.styles = getSampleStyleSheet()
        
        # Hlavný nadpis
        self.styles.add(ParagraphStyle(
            name='MainTitle',
            parent=self.styles['Title'],
            fontSize=18,
            spaceAfter=20,
            textColor=black,
            alignment=1,  # CENTER
            fontName='Helvetica-Bold'
        ))
        
        # Podnadpis
        self.styles.add(ParagraphStyle(
            name='SubTitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            textColor=HexColor('#2E5984'),
            alignment=1,
            fontName='Helvetica-Bold'
        ))
        
        # Nadpis sekcie
        self.styles.add(ParagraphStyle(
            name='SectionTitle',
            parent=self.styles['Heading3'],
            fontSize=12,
            spaceAfter=8,
            spaceBefore=12,
            textColor=HexColor('#2E5984'),
            fontName='Helvetica-Bold'
        ))
        
        # Normálny text
        self.styles.add(ParagraphStyle(
            name='NormalText',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            fontName='Helvetica'
        ))
        
        # Dôležitý text
        self.styles.add(ParagraphStyle(
            name='ImportantText',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            fontName='Helvetica-Bold',
            textColor=HexColor('#C41E3A')
        ))
    
    def create_energy_class_chart(self, energy_class: str, specific_energy: float) -> Drawing:
        """Vytvorenie grafiku energetickej triedy"""
        drawing = Drawing(400, 300)
        
        # Pozície a rozmery pre energetické triedy
        class_height = 25
        class_width = 200
        start_y = 250
        
        y_pos = start_y
        for class_name, class_data in ENERGY_CLASSES.items():
            # Farba triedy
            color = HexColor(class_data["color"])
            
            # Obdĺžnik triedy
            rect = Rect(50, y_pos, class_width, class_height)
            rect.fillColor = color
            rect.strokeColor = black
            rect.strokeWidth = 1
            drawing.add(rect)
            
            # Text triedy
            class_text = String(60, y_pos + 8, f"{class_name} - {class_data['description']}")
            class_text.fontName = 'Helvetica-Bold' if class_name == energy_class else 'Helvetica'
            class_text.fontSize = 10
            class_text.fillColor = white if class_name in ['E', 'F', 'G'] else black
            drawing.add(class_text)
            
            # Označenie aktuálnej triedy
            if class_name == energy_class:
                arrow = Rect(270, y_pos + 8, 100, 9)
                arrow.fillColor = HexColor('#FF6B00')
                arrow.strokeColor = black
                drawing.add(arrow)
                
                arrow_text = String(275, y_pos + 8, f"{specific_energy:.1f} kWh/m²rok")
                arrow_text.fontName = 'Helvetica-Bold'
                arrow_text.fontSize = 8
                arrow_text.fillColor = white
                drawing.add(arrow_text)
            
            y_pos -= 30
        
        # Popis osi
        axis_label = String(50, 20, "Špecifická spotreba primárnej energie (kWh/m²rok)")
        axis_label.fontName = 'Helvetica'
        axis_label.fontSize = 9
        drawing.add(axis_label)
        
        return drawing
    
    def generate_certificate(self, audit_id: int, output_path: Optional[Path] = None) -> Optional[Path]:
        """
        Generovanie certifikátu pre daný audit
        
        Args:
            audit_id: ID auditu
            output_path: Cesta pre výstupný súbor (voľiteľné)
            
        Returns:
            Cesta k vygenerovanému certifikátu alebo None pri chybe
        """
        if not REPORTLAB_AVAILABLE:
            print("Chyba: Reportlab nie je k dispozícii. Certifikáty nemôžu byť generované.")
            return None
            
        try:
            # Načítanie údajov auditu
            audit_data = self.db_manager.get_audit(audit_id)
            if not audit_data:
                raise ValueError(f"Audit s ID {audit_id} neexistuje")
            
            # Výpočet energetických parametrov
            building_data = self._prepare_building_data(audit_id, audit_data)
            energy_results = self.calculator.complete_building_assessment(building_data)
            
            # Nastavenie výstupného súboru
            if not output_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"certifikat_audit_{audit_id}_{timestamp}.pdf"
                output_path = EXPORT_DIR / filename
            
            # Vytvorenie PDF dokumentu
            doc = SimpleDocTemplate(
                str(output_path),
                pagesize=A4,
                rightMargin=self.margin,
                leftMargin=self.margin,
                topMargin=self.margin,
                bottomMargin=self.margin
            )
            
            # Obsah certifikátu
            story = []
            
            # Hlavička
            story.extend(self._create_header())
            
            # Základné informácie o budove
            story.extend(self._create_building_info_section(audit_data))
            
            # Energetické hodnotenie
            story.extend(self._create_energy_assessment_section(energy_results))
            
            # Graf energetickej triedy
            story.append(Spacer(1, 12))
            story.append(Paragraph("Energetická klasifikácia", self.styles['SectionTitle']))
            chart = self.create_energy_class_chart(
                energy_results['energy_classification']['energy_class'],
                energy_results['energy_classification']['specific_primary_energy']
            )
            story.append(chart)
            
            # Technické údaje
            story.extend(self._create_technical_data_section(energy_results))
            
            # Odporúčania
            story.extend(self._create_recommendations_section(energy_results))
            
            # Päta certifikátu
            story.extend(self._create_footer(audit_data))
            
            # Generovanie PDF
            doc.build(story)
            
            # Uloženie certifikátu do databázy
            self._save_certificate_to_db(audit_id, output_path, energy_results)
            
            return output_path
            
        except Exception as e:
            print(f"Chyba pri generovaní certifikátu: {e}")
            return None
    
    def _prepare_building_data(self, audit_id: int, audit_data: Dict[str, Any]) -> Dict[str, Any]:
        """Príprava údajov budovy pre výpočet"""
        building_data = {
            'heated_area': audit_data.get('heated_area', 100),
            'building_type': audit_data.get('building_type', 'Rodinný dom'),
            'structures': [],
            'heating_system': {}
        }
        
        # Načítanie stavebných konštrukcií
        structures = self.db_manager.get_building_structures(audit_id)
        for struct in structures:
            building_data['structures'].append({
                'name': struct.get('name', ''),
                'structure_type': struct.get('structure_type', 'wall'),
                'area': struct.get('area', 0),
                'u_value': struct.get('u_value', 1.0),
                'thermal_bridges': struct.get('thermal_bridges', 0)
            })
        
        # Ak nie sú definované konštrukcie, použijú sa predvolené hodnoty
        if not building_data['structures']:
            building_data['structures'] = [
                {'name': 'Obvodová stena', 'structure_type': 'wall', 'area': 100, 'u_value': 1.0, 'thermal_bridges': 0},
                {'name': 'Strecha', 'structure_type': 'roof', 'area': audit_data.get('heated_area', 100), 'u_value': 0.8, 'thermal_bridges': 0},
                {'name': 'Podlaha', 'structure_type': 'floor', 'area': audit_data.get('heated_area', 100), 'u_value': 0.8, 'thermal_bridges': 0},
                {'name': 'Okná', 'structure_type': 'window', 'area': 20, 'u_value': 1.5, 'thermal_bridges': 0}
            ]
        
        # Vykurovací systém (predvolené hodnoty ak nie sú definované)
        building_data['heating_system'] = {
            'system_type': 'Plynový kotol',
            'fuel_type': 'Zemný plyn',
            'efficiency': 85.0
        }
        
        return building_data
    
    def _create_header(self) -> list:
        """Vytvorenie hlavičky certifikátu"""
        header = []
        
        # Hlavný názov
        header.append(Paragraph("CERTIFIKÁT ENERGETICKEJ EFEKTÍVNOSTI BUDOVY", self.styles['MainTitle']))
        header.append(Spacer(1, 6))
        
        # Podnázov
        header.append(Paragraph("v súlade so zákonom č. 321/2014 Z.z.", self.styles['SubTitle']))
        header.append(Spacer(1, 20))
        
        return header
    
    def _create_building_info_section(self, audit_data: Dict[str, Any]) -> list:
        """Vytvorenie sekcie s informáciami o budove"""
        section = []
        
        section.append(Paragraph("Základné údaje o budove", self.styles['SectionTitle']))
        
        # Tabuľka s údajmi
        data = [
            ["Názov budovy:", audit_data.get('building_name', 'Neuvedené')],
            ["Adresa:", audit_data.get('building_address', 'Neuvedená')],
            ["Typ budovy:", audit_data.get('building_type', 'Neuvedený')],
            ["Rok výstavby:", str(audit_data.get('construction_year', 'Neuvedený'))],
            ["Celková podlahová plocha:", f"{audit_data.get('total_area', 0):.1f} m²"],
            ["Vykurovaná plocha:", f"{audit_data.get('heated_area', 0):.1f} m²"],
            ["Počet podlaží:", str(audit_data.get('number_of_floors', 'Neuvedený'))],
        ]
        
        table = Table(data, colWidths=[6*cm, 8*cm])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, black),
            ('BACKGROUND', (0, 0), (0, -1), HexColor('#F0F0F0')),
        ]))
        
        section.append(table)
        section.append(Spacer(1, 20))
        
        return section
    
    def _create_energy_assessment_section(self, energy_results: Dict[str, Any]) -> list:
        """Vytvorenie sekcie s energetickým hodnotením"""
        section = []
        
        section.append(Paragraph("Energetické hodnotenie", self.styles['SectionTitle']))
        
        summary = energy_results['summary']
        classification = energy_results['energy_classification']
        
        # Hlavné výsledky
        main_results = [
            ["Špecifická potreba tepla na vykurovanie:", f"{summary['specific_heating_demand']:.1f} kWh/m²rok"],
            ["Špecifická potreba tepla na teplú vodu:", f"{summary['specific_hot_water_demand']:.1f} kWh/m²rok"],
            ["Špecifická spotreba primárnej energie:", f"{summary['specific_primary_energy']:.1f} kWh/m²rok"],
            ["Špecifické emisie CO₂:", f"{summary['specific_co2_emissions']:.1f} kg/m²rok"],
            ["Energetická trieda:", classification['energy_class']],
            ["Popis energetickej triedy:", classification['class_description']],
        ]
        
        table = Table(main_results, colWidths=[8*cm, 6*cm])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, black),
            ('BACKGROUND', (0, 0), (0, -1), HexColor('#E6F3FF')),
            # Zvýraznenie energetickej triedy
            ('BACKGROUND', (0, 4), (-1, 5), self.energy_class_colors.get(classification['energy_class'], HexColor('#FFFFFF'))),
            ('FONTNAME', (0, 4), (-1, 5), 'Helvetica-Bold'),
        ]))
        
        section.append(table)
        section.append(Spacer(1, 12))
        
        return section
    
    def _create_technical_data_section(self, energy_results: Dict[str, Any]) -> list:
        """Vytvorenie sekcie s technickými údajmi"""
        section = []
        
        section.append(Paragraph("Podrobné technické údaje", self.styles['SectionTitle']))
        
        # Tepelné straty a zisky
        transmission = energy_results.get('transmission', {})
        ventilation = energy_results.get('ventilation', {})
        internal_gains = energy_results.get('internal_gains', {})
        solar_gains = energy_results.get('solar_gains', {})
        
        technical_data = [
            ["Tepelné straty prechodom:", f"{transmission.get('annual_transmission_losses', 0):.0f} kWh/rok"],
            ["Tepelné straty vetraním:", f"{ventilation.get('annual_ventilation_losses', 0):.0f} kWh/rok"],
            ["Vnútorné tepelné zisky:", f"{internal_gains.get('annual_internal_gains', 0):.0f} kWh/rok"],
            ["Solárne zisky:", f"{solar_gains.get('annual_solar_gains', 0):.0f} kWh/rok"],
            ["Potreba tepla na vykurovanie:", f"{energy_results['heating_demand'].get('heating_demand', 0):.0f} kWh/rok"],
            ["Potreba tepla na teplú vodu:", f"{energy_results['hot_water_demand'].get('hot_water_demand', 0):.0f} kWh/rok"],
        ]
        
        table = Table(technical_data, colWidths=[8*cm, 6*cm])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, black),
            ('BACKGROUND', (0, 0), (0, -1), HexColor('#F5F5F5')),
        ]))
        
        section.append(table)
        section.append(Spacer(1, 12))
        
        return section
    
    def _create_recommendations_section(self, energy_results: Dict[str, Any]) -> list:
        """Vytvorenie sekcie s odporúčaniami"""
        section = []
        
        section.append(Paragraph("Odporúčania na zlepšenie energetickej efektívnosti", self.styles['SectionTitle']))
        
        energy_class = energy_results['energy_classification']['energy_class']
        
        # Základné odporúčania podľa energetickej triedy
        if energy_class in ['A1', 'A2']:
            recommendations = [
                "Budova má výbornú energetickú efektívnosť.",
                "Odporúča sa pravidelná údržba technických zariadení.",
                "Zvážte inštaláciu obnoviteľných zdrojov energie."
            ]
        elif energy_class in ['B', 'C']:
            recommendations = [
                "Budova má dobrú energetickú efektívnosť.",
                "Zvážte modernizáciu vykurovacieho systému.",
                "Optimalizujte prevádzku technických zariadení.",
                "Zvážte zlepšenie tepelnej izolácie."
            ]
        elif energy_class in ['D', 'E']:
            recommendations = [
                "Budova potrebuje energetické zlepšenia.",
                "Priorita: zlepšenie tepelnej izolácie obálky budovy.",
                "Modernizácia vykurovacieho systému.",
                "Inštalácia efektívneho vetrania s rekuperáciou.",
                "Výmena okien za energeticky efektívne."
            ]
        else:  # F, G
            recommendations = [
                "Budova má veľmi nízku energetickú efektívnosť.",
                "Urgentne odporúčané komplexné energetické zlepšenia:",
                "• Zateplenie obálky budovy (steny, strecha, podlaha)",
                "• Výmena všetkých okien a dverí",
                "• Modernizácia celého vykurovacieho systému",
                "• Inštalácia riadených vetracích systémov",
                "• Zváženie obnoviteľných zdrojov energie"
            ]
        
        for rec in recommendations:
            section.append(Paragraph(rec, self.styles['NormalText']))
        
        section.append(Spacer(1, 12))
        
        return section
    
    def _create_footer(self, audit_data: Dict[str, Any]) -> list:
        """Vytvorenie päty certifikátu"""
        footer = []
        
        footer.append(Spacer(1, 20))
        footer.append(Paragraph("Informácie o certifikáte", self.styles['SectionTitle']))
        
        # Údaje o certifikáte
        issue_date = datetime.now()
        valid_until = issue_date + timedelta(days=3650)  # 10 rokov platnosť
        certificate_number = f"EE-{datetime.now().year}-{uuid.uuid4().hex[:8].upper()}"
        
        cert_info = [
            ["Číslo certifikátu:", certificate_number],
            ["Dátum vydania:", issue_date.strftime("%d.%m.%Y")],
            ["Platnosť do:", valid_until.strftime("%d.%m.%Y")],
            ["Audítor:", audit_data.get('auditor_name', 'Neuvedený')],
            ["Licencia audítora:", audit_data.get('auditor_license', 'Neuvedená')],
        ]
        
        table = Table(cert_info, colWidths=[6*cm, 8*cm])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, black),
            ('BACKGROUND', (0, 0), (0, -1), HexColor('#F0F0F0')),
        ]))
        
        footer.append(table)
        footer.append(Spacer(1, 20))
        
        # Poznámka
        footer.append(Paragraph(
            "Tento certifikát bol vygenerovaný automaticky pomocou Energy Audit Desktop Application.",
            self.styles['NormalText']
        ))
        
        return footer
    
    def _save_certificate_to_db(self, audit_id: int, certificate_path: Path, 
                               energy_results: Dict[str, Any]) -> None:
        """Uloženie certifikátu do databázy"""
        try:
            issue_date = datetime.now()
            valid_until = issue_date + timedelta(days=3650)
            certificate_number = f"EE-{issue_date.year}-{uuid.uuid4().hex[:8].upper()}"
            
            certificate_data = {
                'certificate_number': certificate_number,
                'energy_class': energy_results['energy_classification']['energy_class'],
                'total_primary_energy': energy_results['energy_classification']['specific_primary_energy'],
                'co2_emissions_total': energy_results['summary']['specific_co2_emissions'],
                'issue_date': issue_date.isoformat(),
                'valid_until': valid_until.isoformat(),
                'certificate_file_path': str(certificate_path)
            }
            
            self.db_manager.create_energy_certificate(audit_id, certificate_data)
            
        except Exception as e:
            print(f"Chyba pri ukladaní certifikátu do databázy: {e}")


# Globálna inštancia generátora
certificate_generator = CertificateGenerator()


def get_certificate_generator() -> CertificateGenerator:
    """Získanie globálnej inštancie generátora certifikátov"""
    return certificate_generator


def generate_sample_certificate() -> Optional[Path]:
    """Vygeneruje vzorový certifikát pre testovacie účely"""
    try:
        # Vytvorenie vzorového auditu
        sample_audit_data = {
            'audit_name': 'Vzorový audit - testovanie',
            'building_name': 'Vzorový rodinný dom',
            'building_address': 'Testovacia ulica 123, Bratislava',
            'building_type': 'Rodinný dom',
            'construction_year': 1995,
            'total_area': 150.0,
            'heated_area': 120.0,
            'number_of_floors': 2,
            'auditor_name': 'Ing. Testovací Audítor',
            'auditor_license': 'EA-12345',
            'status': 'completed',
            'notes': 'Vzorový audit pre testovanie generátora certifikátov.'
        }
        
        db_manager = get_db_manager()
        audit_id = db_manager.create_audit(sample_audit_data)
        
        # Generovanie certifikátu
        generator = get_certificate_generator()
        certificate_path = generator.generate_certificate(audit_id)
        
        return certificate_path
        
    except Exception as e:
        print(f"Chyba pri generovaní vzorového certifikátu: {e}")
        return None