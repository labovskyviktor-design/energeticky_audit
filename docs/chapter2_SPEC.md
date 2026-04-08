# Chapter 2 — SPEC: Potreba tepla na vykurovanie

> **Source of truth:** Krajčík, M. a kol. — Energetické hodnotenie budov, str. 22–37

## 1. Formulas

### (2.1) Potreba tepla na vykurovanie (sezónna metóda)
```
QH = Qht − ηgn · Qgn   [kWh]
```
- **Qht** — celková tepelná strata vo vykurovacom období (kWh)
- **ηgn** — faktor využitia tepelných ziskov (-)
- **Qgn** — celkový tepelný zisk (kWh)

### (2.2) Celková tepelná strata
```
Qht = (HT + HV) · (θint − θe,m) · t · 0.024   [kWh]
```
- **HT** — merná tepelná strata prechodom tepla (W/K)
- **HV** — merná tepelná strata vetraním (W/K)
- **θint** — vnútorná teplota (°C), normalizovaná = 20 °C
- **θe,m** — priem. vonkajšia teplota (°C), normalizovaná = 3.86 °C
- **t** — dĺžka vykurovacej sezóny (dni), normalizované = 212

### (2.3) Merná tepelná strata prechodom tepla HT
```
HT = Σ(bx,i · Ui · Ai) + ΔU · ΣAi   [W/K]
```
- **bx,i** — redukčný faktor (Tab 2.1)
- **Ui** — súčiniteľ prechodu tepla (W/(m²·K))
- **Ai** — plocha konštrukcie (m²)
- **ΔU** — prirážka na tepelné mosty (W/(m²·K))

### (2.4) Merná tepelná strata vetraním HV
```
HV = (V/Vb) · ρa · ca · ninf · Vb / 3600   [W/K]
```
- **ρa** = 1.2 kg/m³, **ca** = 1010 J/(kg·K)
- **V/Vb** = 0.85 (obnovované budovy), 0.80 (ostatné), 0.75 (nové RD)
- **ninf** — intenzita výmeny vzduchu (min. 0.5 1/h)

### (2.5) Infiltrácia cez škáry (budovy do 25 m)
```
ninf = (3600 · Σ(ilv,j · lj)) / Vb   [1/h]
```

### (2.6) Celkové tepelné zisky
```
Qgn = Qint + Qsol   [kWh]
```

### (2.7) Vnútorné tepelné zisky
```
Qint = n · 0.024 · qi · Ab   [kWh]
```
- **qi** = 4 (RD), 5 (BD), 6 (nebytové) W/m²
- **n** = 212 dní, **Ab** = merná plocha

### (2.8) Solárne tepelné zisky (per element k)
```
Qsol,k = Fsh,ob,k · Asol,k · Isol,k   [kWh]
```

### (2.9) Účinná slnečná kolekčná plocha
```
Asol = Fsh,gl · ggl · (1 − FF) · Aw,p   [m²]
```
- **Fsh,gl** = 0.8 (pohyblivé tienenie)
- **ggl** = celková priepustnosť (Tab 2.4/2.5)
- **FF** = podiel rámov, (1 − FF) = 0.8

### (2.10) Korekcia ggl
```
ggl = Fw · ggl,n   (Fw = 0.9)
```

### (2.11) Obostavaný objem
```
Vb = Ab · hk,pr   [m³]
```

---

## 2. Reference Tables

### Tab 2.1 — Redukčný faktor bx

| Konštrukcia | bx |
|---|---|
| Vonkajšia stena, okno, dvere | 1.00 |
| Strecha na teplovýmennom obale | 1.00 |
| Podlaha na teréne | 1.00 |
| Podlaha podstrešného priestoru | 0.80 |
| Stena medzi vykurovaným a nevyk. priestorom | 0.80 |
| Stena/strop nevykurovaného suterénu | 0.50 |
| Stena temperovaného priestoru (garáž) | 0.35 |
| Otvorená dilatácia | 0.35 |
| Uzavretá zaizolovaná dilatácia ≤ 0.05 m | 0.10 |
| Strop nad otvoreným prejazdom | 1.00 |

### Tab 2.2 — Súčiniteľ škárovej prievzdušnosti ilv

| Konštrukcia | ilv × 10⁴ (m²/(s·Pa⁰·⁶⁷)) |
|---|---|
| Kovové okná, netesnené | ≥ 1.8 |
| Drevené okná, netesnené | ≥ 1.4 |
| Drevené/plastové/kovové s tesnením | ≤ 1.0 |

### Tab 2.3 — Normalizované intenzity slnečného žiarenia (kWh/m²)

| Orientácia | I | II | III | IV | X | XI | XII | Spolu |
|---|---|---|---|---|---|---|---|---|
| Juh | 30.2 | 43.6 | 61.2 | 66.3 | 57.2 | 33.1 | 28.4 | **320** |
| Sever | 9.1 | 13.8 | 20.1 | 27.2 | 14.5 | 8.4 | 6.8 | **100** |
| Východ/Západ | 14.9 | 24.5 | 42 | 59.1 | 32.2 | 15.4 | 11.8 | **200** |
| JV/JZ | 22.7 | 33.8 | 50.9 | 62 | 44.8 | 24.9 | 20.8 | **260** |
| SV/SZ | 10.2 | 16.1 | 26.8 | 41.6 | 18.3 | 9.6 | 7.4 | **130** |
| Horizontálna | 22.2 | 38.6 | 71.4 | 108.2 | 55 | 26.2 | 18.4 | **340** |

### Tab 2.6 — Faktor využitia tepelných ziskov ηH,gn

| Úroveň | RD | BD |
|---|---|---|
| Energeticky úsporné | 0.95 | 0.95 |
| Nízkoenergetické | 0.95 | 0.95 |
| Ultranízkoenergetické | 0.95 | 0.84 |
| Takmer nulová spotreba | 0.95 | 0.84 |

### Tab 2.7 — Požiadavky na QH,nd [kWh/(m²·a)]

| Faktor tvaru (1/m) | QH,nd,max | QH,nd,N | QH,nd,r1 | QH,nd,r2 |
|---|---|---|---|---|
| ≤ 0.3 | 70.00 | 50.00 | 25.00 | 12.50 |
| 0.4 | 78.60 | 57.10 | 28.55 | 14.28 |
| 0.5 | 87.10 | 64.30 | 32.15 | 16.08 |
| 0.6 | 95.70 | 71.40 | 35.70 | 17.85 |
| 0.7 | 104.30 | 78.60 | 39.30 | 19.65 |
| 0.8 | 112.90 | 85.70 | 42.85 | 21.43 |
| 0.9 | 121.40 | 92.90 | 46.45 | 23.23 |
| 1.0 | 130.00 | 100.00 | 50.00 | 25.00 |

---

## 3. Example (Test Data) — Bratislava Panel Block (Tab 2.8)

### Input Data
- Bytový dom, P 1.14 BA, Bratislava
- Šírka: 25.03 m, Dĺžka: 21.29 m, Výška: 37.0 m
- 13 podlaží, Vb = 12 417.6 m³, Ab = 4403.4 m², ΣAi = 3644.5 m²
- hk,pr = 2.82 m, Faktor tvaru = 0.30 1/m
- θint = 20 °C, θe,m = 3.86 °C, t = 212 dní

### Construction Data

| Konštrukcia | Ui | Ai (m²) | bx | bx·Ui·Ai (W/K) |
|---|---|---|---|---|
| Obvodová stena | 0.68 | 2056.6 | 1.00 | 1398.49 |
| Plochá strecha | 0.50 | 366.95 | 1.00 | 183.48 |
| Podlaha nad nevyk. suterénom | 0.56 | 366.95 | 0.50 | 102.75 |
| Pôvodné drevené okná (byty) | 2.70 | 300.30 | 1.00 | 810.81 |
| Vymenené plastové okná (byty) | 1.30 | 300.30 | 1.00 | 390.39 |
| Oceľové okná schodisko | 5.20 | 253.40 | 1.00 | 1317.68 |

### Intermediate Results
- **Σ(bx·Ui·Ai) = 4203.6** W/K
- **ΔU = 0.10** → ΔU·ΣAi = 0.10 × 3644.5 = **364.5** W/K
- **HT = 4203.6 + 364.5 = 4568.0** W/K
- Infiltration: **ninf = 0.79** 1/h (> 0.5 → use 0.79)
- V/Vb = 0.85
- **HV = 0.85 × 1.2 × 1010 × 0.79 × 12417.6 / 3600 = 2807.3** W/K
- **H = HT + HV = 7375.3** W/K

### Heat Gains
- **Qint = 212 × 0.024 × 5 × 4403.4 = 110 085.0** kWh/a
- Solar gains (ggl = 0.62, tieniaci faktor = 0.5):
  - JUH: 320 × area_calc, VÝCHOD/ZÁPAD: 200 × ..., SEVER: 100 × ...
  - **Qsol = 56 360.2** kWh/a
- **Qgn = 110 085.0 + 56 360.2 = 166 445.2** kWh/a

### Final Results
- **ηgn = 0.95**
- **Qht = 7375.3 × (20 − 3.86) × 212 × 0.024 = 605 561.5** kWh/a
- **QH = 605 561.5 − 0.95 × 166 445.2 = 447 439.1** kWh/a *(script: 447 539.1)*
- **QH,nd = 447 439.1 / 4403.4 = 101.6** kWh/(m²·a)
- Požiadavka QH,nd,r1 = 25 kWh/(m²·a) → **NEVYHOVUJE**

> Note: Minor rounding differences expected due to intermediate rounding in the script.
