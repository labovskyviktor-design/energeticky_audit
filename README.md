# 🏠 Energetický Audit a Certifikácia Budov — Príloha k Školskej Práci

Tento dokument slúži ako **podrobný návod na inštaláciu a spustenie softvéru**, ktorý bol vytvorený ako praktická časť školskej práce. Softvér je vyvinutý podľa platných slovenských technických noriem (**STN**) pre výpočet energetickej náročnosti budov.

---

## 👨‍💻 Základné informácie
- **Autor:** Viktor Labovský
- **GitHub Profil:** [labovskyviktor-design](https://github.com/labovskyviktor-design)
- **Repozitár:** [energy-audit](https://github.com/labovskyviktor-design/energy-audit)
- **Rok vzniku:** 2026

## 🛠 Technický stack
Softvér je postavený na moderných technológiách, ktoré zabezpečujú vysoký výkon, bezpečnosť a škálovateľnosť:

- **Backend:** Python 3.12+ · FastAPI (Moderné, rýchle webové API) · Pydantic (Striktná validácia dát)
- **Frontend:** HTML5 · Vanilla JavaScript · CSS3 (Servované priamo cez FastAPI pre jednoduchosť nasadenia)
- **Architektúra:** Hexagonálna architektúra (Clean Architecture) — zabezpečuje nezávislosť výpočtového jadra od sieťovej vrstvy a UI.
- **Štandardy:** Implementácia vzorcov a metodiky podľa STN 73 0540-3 a ďalších relevantných noriem pre energetickú certifikáciu.

---

## 🚀 Podrobný návod na inštaláciu (pre programátorov)

Ak chcete softvér spustiť manuálne, uistite sa, že máte nainštalovaný **Python 3.11 alebo novší**. Postupujte podľa týchto detailných krokov:

### 1. Príprava prostredia
Otvorte terminál (Command Prompt, PowerShell alebo Terminal v macOS/Linux) a prejdite do adresára, kde chcete projekt uložiť.

### 2. Klonovanie repozitára
Stiahnite si zdrojový kód z GitHubu:
```bash
git clone https://github.com/labovskyviktor-design/energy-audit.git
cd energy-audit
```

### 3. Konfigurácia Backend-u
Prejdite do priečinka `backend`, vytvorte virtuálne prostredie a nainštalujte potrebné knižnice:
```bash
# Vstup do priečinka backend
cd backend

# Vytvorenie virtuálneho prostredia (oddelí knižnice projektu od systému)
python -m venv venv

# Aktivácia virtuálneho prostredia:
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Inštalácia všetkých potrebných komponentov (FastAPI, Uvicorn, atď.)
pip install -r requirements.txt
```

### 4. Spustenie aplikácie
Keď sú všetky závislosti nainštalované, spustite vývojový server:
```bash
python -m uvicorn app.main:app --reload
```
Aplikácia sa úspešne spustí a bude dostupná v akomkoľvek webovom prehliadači na adrese:
👉 **[http://localhost:8000](http://localhost:8000)**

---

## 🤖 Odporúčaný spôsob inštalácie (pre užívateľov bez skúseností s kódovaním)

> [!IMPORTANT]
> **POZNÁMKA:** Ak nie ste programátor alebo nemáte skúsenosti s inštaláciou softvéru cez príkazový riadok, **vyslovene odporúčam** použiť pri inštalácii pomoc **AI agenta** (napr. **Antigravity**).

Moderné AI nástroje ako Antigravity dokážu automaticky:
1. Detegovať váš operačný systém a upraviť príkazy.
2. Vyriešiť prípadné konflikty verzií Python-u.
3. Automaticky vytvoriť a spravovať virtuálne prostredia.
4. Spustiť aplikáciu jedným príkazom bez nutnosti manuálneho prepínania priečinkov.

Jednoducho vložte tento repozitár do vášho AI prostredia a požiadajte agenta: *"Spusti túto aplikáciu na localhoste."*

---

## 📐 Rozsah funkčnosti (Kapitoly výpočtu)

| Modul | Kapitola | Popis |
|---|---|---|
| **Fyzika a Obálka** | Kap. 1 | Geometria, U-hodnoty, tepelné straty HT, HV |
| **Energetická Bilancia** | Kap. 2 | Sezónna metóda, solárne/vnútorné zisky, QH,nd |
| **Technické Systémy** | Kap. 3–4 | Straty systémov (vykurovanie, TV), dodaná energia |
| **Certifikácia** | Kap. 9 | Primárna energia, CO2, energetické triedy A0–G |
| **Audit & Obnova** | Kap. 5–8, 10 | Simulácia opatrení, ROI, NPV, Cashflow |

---

## 📚 Zdroj pravdy
Celá výpočtová logika, vzorce, koeficienty a metodika sa riadia výhradne podľa metodiky energetickej certifikácie budov a príslušných STN.

---

## ⚖️ Licencovanie a vlastníctvo
© 2026 **Viktor Labovský**. Všetky práva vyhradené.

Tento softvér je výhradným duševným vlastníctvom autora a bol vytvorený ako súčasť školskej práce. Akékoľvek kopírovanie, šírenie, úprava alebo komerčné využitie bez predchádzajúceho písomného súhlasu autora je prísne zakázané.
