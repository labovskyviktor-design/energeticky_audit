# 🏢 Professional Energy Audit System v2.0

**Profesionálny systém pre energetické audity budov podľa slovenských noriem**

## 📋 Popis

Komplexná aplikácia pre vykonávanie energetických auditov budov v súlade s:
- **STN EN 16247-1** (Energetické audity - Všeobecné požiadavky)
- **STN EN ISO 13790** (Energetická náročnosť budov)
- **STN 73 0540-2 Z2/2019** (Tepelná ochrana budov)
- **Vyhláška MH SR č. 364/2012 Z. z.** o energetickej náročnosti budov


## ✨ Hlavné funkcie

### 🔍 Kompletný energetický audit
- **Detailný popis budovy** - identifikácia, typológia, funkcie
- **Obálka budovy** - steny, okná, strecha, podlaha s tepelno-technickým posúdením
- **Vykurovací systém** - zdroje tepla, distribúcia, regulácia
- **Teplá úžitková voda (TUV)** - samostatný tab s kompletným systémom
- **Elektrické systémy** - osvetlenie a elektrické zariadenia
- **Užívanie budovy** - prevádzkové parametre

### 🧮 Pokročilé výpočty
- **Mesačná energetická bilancia** podľa STN EN ISO 13790
- **Solárne a vnútorné tepelné zisky** s koeficientom využiteľnosti
- **Transmisné straty** včítane tepelných mostov
- **Ventilačné straty** s n50 testnosťou budovy
- **Primárna energia** podľa aktuálnych konverzných faktorov SR
- **CO2 emisie** podľa emisných faktorov SEPS/SHMU 2024

### 📊 Výstupy a hodnotenie
- **Energetické triedy A0-G** podľa vyhlášky 364/2012
- **Detailné výpočty** krok za krokom
- **Súhrnné tabuľky** nepriehľadných a priehľadných konštrukcií
- **Odporúčania na zlepšenie** energetickej účinnosti
- **Energetické certifikáty** na export
- **Projekty** uloženie/načítanie vo formáte JSON


## 🛠️ Technické špecifikácie

### Požiadavky na systém
- **Python 3.8+**
- **Tkinter** (GUI framework)
- **Operačný systém:** Windows, macOS, Linux

### Inštalácia a spustenie
```bash
# Spustenie hlavnej aplikácie
python working_energy_audit.py
```

### Štruktúra súborov
- `working_energy_audit.py` - **Hlavná aplikácia** (odporúčané)
- `energy_audit_gui.py` - Pôvodná verzia
- `simple_audit_gui.py` - Zjednodušená verzia
- `comprehensive_audit_gui.py` - Rozšírená verzia

## 📈 Validované výpočty

### Klimatické údaje SR
- **Bratislava:** HDD 2800 K·deň/rok
- **Košice:** HDD 3100 K·deň/rok  
- **Poprad:** HDD 3200 K·deň/rok

### Konverzné faktory (2024)
- **Zemný plyn:** 1.1
- **Elektrina:** 2.5
- **Celenné vykurovanie:** 1.0
- **Tepelné čerpadlo:** 2.5

### CO2 emisné faktory (2024)
- **Elektrina SR:** 0.218 kg CO2/kWh
- **Zemný plyn:** 0.202 kg CO2/kWh
- **Biomasa:** 0.039 kg CO2/kWh

## 🎯 Cieľové skupiny

- **Energetickí audítori** - certifikovaní odborníci
- **Projektanti** - návrh energeticky efektívnych budov
- **Správcovia nehnuteľností** - optimalizácia energetických nákladov
- **Developeri** - hodnotenie energetickej náročnosti projektov

## 📞 Kontakt a podpora

**Aplikácia je určená výlučne pre profesionálne použitie.**

Pre získanie prístupu alebo technickú podporu kontaktujte vlastníka.

---

## 📄 Licencia

**Copyright © 2024 - Všetky práva vyhradené**

Táto aplikácia je vlastníctvom jej autora. Akékoľvek použitie, kopírovanie, modifikácia alebo distribúcia je **prísne zakázaná** bez písomného súhlasu vlastníka.

### ⚠️ Dôležité upozornenie:
- Neautorizované použitie je **trestným činom**
- Všetky výpočty a metodiky jsou chránené autorskými právami
- Pre komerčné použitie je potrebná licenčná zmluva

---

*Posledná aktualizácia: 22. september 2024*
