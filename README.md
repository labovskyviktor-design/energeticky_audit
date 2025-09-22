# 🏠 Energetická Audítorská Aplikácia

Komplexná desktopová aplikácia pre energetické audity budov implementovaná v Pythone s GUI rozhraním.

## 📋 Prehľad

Táto aplikácia poskytuje kompletný ekosystém nástrojov pre energetické hodnotenie budov od základných výpočtov až po pokročilé analýzy a detailné reporty s investičnými odporúčaniami.

## ✨ Kľúčové funkcionality

### 🏗️ Základné moduly
- **GUI formuláre** - Používateľsky prívetivé rozhranie pre zadávanie údajov
- **Databáza** - SQLite databáza pre ukladanie auditov a výsledkov
- **Energetické výpočty** - Komplexné výpočty podľa STN noriem
- **Generátor certifikátov** - Automatické vytváranie energetických certifikátov

### 🔬 Pokročilé analýzy
- **Tepelno-technické výpočty** - Detailná analýza tepelných strát a mostíkov
- **Diagnostika budov** - Termovízia, blower door testy, monitorovanie
- **Posudzovania konštrukcií** - Hodnotenie stavebných konštrukcií a materiálov
- **Pokročilé reporty** - Komplexné správy s grafmi a odporúčaniami

## 📊 Podporované štandardy

- **STN 73 0540-2:2012** - Tepelná ochrana budov
- **Pasívny dom** - Štandard nízkoenergetických budov  
- **nZEB** - Takmer nulovej potreby energie
- **Energetická klasifikácia** - Triedy A1 až G

## 🧮 Výpočtové funkcie

- Tepelné straty cez konštrukcie
- Tepelné mostíky a ich vplyv
- Potreba tepla na vykurovanie a ohrev TÚV
- Primárna energia a CO₂ emisie
- Sezónne energetické bilancie
- Kondenzácia a letná stabilita

## 📈 Analytické nástroje

- **Benchmark analýzy** - Porovnanie s typickými hodnotami
- **Finančné analýzy** - NPV, IRR, doba návratnosti
- **Priority matrix** - Optimalizácia investičných rozhodnutí
- **Environmentálny dopad** - Výpočet CO₂ úspor
- **Compliance check** - Kontrola súladu s normami

## 🛠️ Technické špecifikácie

### Požiadavky
- Python 3.8+
- tkinter (GUI)
- sqlite3 (databáza)
- reportlab (PDF generovanie)
- Ďalšie závislosti v `requirements.txt`

### Štruktúra projektu

```
energy-audit-app/
├── src/                          # Zdrojové súbory
│   ├── main.py                   # Hlavná aplikácia
│   ├── config.py                 # Konfigurácia
│   ├── database.py               # Databázové operácie
│   ├── energy_calculations.py    # Energetické výpočty
│   ├── thermal_analysis.py       # Tepelno-technické analýzy
│   ├── building_diagnostics.py   # Diagnostické nástroje
│   ├── construction_assessment.py # Posudzovania konštrukcií
│   ├── advanced_reports.py       # Pokročilé reporty
│   ├── audit_forms.py            # GUI formuláre
│   └── certificate_generator.py  # Generátor certifikátov
├── tests/                        # Testy
├── docs/                         # Dokumentácia
├── scripts/                      # Pomocné skripty a PDF materiály
└── data/                         # Údajové súbory
```

## 🚀 Inštalácia a spustenie

```bash
# Klonovanie repository
git clone https://github.com/labovskyviktor-design/energeticky_audit.git
cd energeticky_audit

# Inštalácia závislostí
pip install -r requirements.txt

# Spustenie aplikácie
python src/main.py
```

## 📝 Použitie

1. **Vytvorenie auditu** - Zadanie základných údajov o budove
2. **Analýza konštrukcií** - Definovanie stavebných konštrukcií
3. **Energetické výpočty** - Automatické výpočty potrieb energie
4. **Diagnostika** - Vykonanie meraní a testov
5. **Generovanie reportov** - Vytvorenie komplexných správ
6. **Export certifikátov** - PDF certifikáty a dokumentácia

## 🧪 Testovanie

```bash
# Spustenie všetkých testov
python run_tests.py

# Jednotlivé testy modulov
python -m pytest tests/
```

## 📚 Dokumentácia

Podrobná dokumentácia je dostupná v priečinku `docs/` vrátane:
- Technickej dokumentácie modulov
- Užívateľskej príručky
- Príkladov použitia
- Referenčných materiálov (PDF)

## 🤝 Prispievanie

1. Vytvorte fork repository
2. Vytvorte feature branch (`git checkout -b feature/AmazingFeature`)
3. Commitnite zmeny (`git commit -m 'Add some AmazingFeature'`)
4. Push do branch (`git push origin feature/AmazingFeature`)
5. Otvorte Pull Request

## 📄 Licencia

Tento projekt je licencovaný pod MIT licenciou - pozrite súbor `LICENSE` pre detaily.

## 👥 Autori

- **Viktor Labovský** - *Inicálna práca* - [labovskyviktor-design](https://github.com/labovskyviktor-design)

## 🙏 Poďakovanie

- STN normy pre energetické hodnotenie budov
- Python komunita za výborné nástroje
- Všetkým prispievateľom a testerom

---

**⚡ Energetická efektívnosť začína správnym meraním a analýzou!**
