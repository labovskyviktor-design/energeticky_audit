# Chapter 3: Potreba energie na vykurovanie
## (Heating Energy Demand — STN EN 15316-1/2/3)

This chapter calculates the **total energy demand for heating** by adding system losses from emission, distribution, pump energy, storage, and generation subsystems to the heating heat demand (QH from Chapter 2).

---

## 3.1 Calculation Chain Overview

```
QH (from Ch.2)
  → + Qem,ls    (emission subsystem losses)
  → + QH,dis,ls (distribution pipe losses)
  → + WH,dis,aux (pump/auxiliary energy)
  → + Qs,ls      (storage losses, same method as DHW §4.1.4)
  → + Qg,ls      (generation losses)
  → - QW,d,i     (recoverable DHW distribution losses)
  = QVYK         (total heating energy demand)
```

**Formula (3.23)**:
```
QVYK = QH + Qem,ls + QH,dis,ls,an + WH,dis,aux,an + Qs,ls + Qg,ls
```

---

## 3.1.1 Emission Subsystem Losses — Qem,ls

### Formula (3.1)
```
Qem,ls = QH · [Δθint,inc / (θint,inc − θe,comb)]   (kWh)
```

Where:
- **QH** = heating heat demand from Ch.2 (kWh)
- **Δθint,inc** = increase in internal temp due to emission system losses (K) 
- **θint,inc** = equivalent internal temperature (°C) = θint,ini + Δθint,inc
- **θe,comb** = mean external temp during heating period (°C); for normative assessment = 3.86°C per STN 73 0540-3

### Formula (3.3) — Δθint,inc decomposition
```
Δθint,inc = Δθhyd + Δθemt,sys + Δθctr,sys   (K)
```

### Formula (3.4) — Emission system temperature change
```
Δθemt,sys = Δθstr + Δθemb + Δθrad + Δθim,emt   (K)
```

### Formula (3.5) — Control system temperature change
```
Δθctr,sys = Δθctr + Δθim,ctr + Δθroomaut   (K)
```

### Table 3.1 — Δθhyd (hydraulic balancing)

| Configuration | One-pipe | Two-pipe (n≤10) | Two-pipe (n>10) |
|---|---|---|---|
| No balancing | 0.7 | 0.6 | 0.6 |
| Static per radiator | 0.4 | 0.3 | 0.4 |
| Static + system balancing | — | 0.2 | 0.3 |
| Dynamic per circuit | 0.3 | 0.1 | 0.2 |
| Dynamic per circuit + return temp control | 0.2 | 0 | 0.1 |
| Dynamic per radiator | — | — | 0 |

### Table 3.2 — Integrated heating surfaces (floor/wall/ceiling), h ≤ 4m

| Regulation type | Δθstr | Δθctr (no cert) | Δθctr (cert) |
|---|---|---|---|
| Unregulated, central | 2.5 | 2.5 | — |
| Reference room control | 2.0 | 1.8 | — |
| Room-level control | 1.8 | 1.6 | — |
| P-controller (pre-1988) | 1.4 | 1.4 | — |
| P-controller / 2-step (hyst ≤ 0.5K) | 1.2 | 0.7 | — |
| PI-controller | 1.2 | 0.7 | — |
| PI-controller with optimization | 0.9 | 0.5 | — |

Δθemb for integrated surfaces — formula (3.6):
```
Δθemb = (Δθemb,1 + Δθemb,2) / 2   (K)
```

Floor heating: wet=0.7/0.7, dry=0.4/0.7, dry low-coverage=0.2/0.7
Wall heating: 1.4/—, Ceiling: 0.5/—
Fixed values: Δθim,ctr=0.0K, Δθim,emt=-0.2K, Δθrad=0K (h≤4m)
Δθroomaut: standalone=-0.5K, adaptive=-1.0K, networked=-1.2K

### Table 3.4 — Free heating surfaces (radiators, convectors), h ≤ 4m

| Regulation type | Δθstr,1 | Δθstr,2 | Δθctr (no cert) | Δθctr (cert) |
|---|---|---|---|---|
| Unregulated, central | — | — | 2.5 | — |
| Reference room control | — | — | 2.0 | — |
| Room-level control | — | — | 1.8 | — |
| P-controller (pre-1988) | — | — | 1.4 | — |
| P-controller | — | — | 1.2 | 1.2 |
| PI-controller | — | — | 1.2 | 0.7 |
| PI with optimization | — | — | 0.9 | 0.5 |

Δθstr for radiators — formula (3.7):
```
Δθstr = (Δθstr,1 + Δθstr,2) / 2   (K)
```

Stratification by system type and temp drop:
- Two-pipe/renovated 1-pipe: 60K→1.2/1.6, 42.5K→0.7/1.2, 30K→0.5/—, 20K→0.4/—
- Original 1-pipe: 60K→1.2/0.2, 42.5K→0.7/0

Δθemb for radiators:
- Internal wall: 0, External wall no radiation protection: 0
- External wall GF no protection: 1.7, GF with protection: 1.2
- Normal external wall: 0.3

Fixed values: Δθim,ctr=0K, Δθim,emt=-0.3K, Δθrad=0K (h≤4m)
Same Δθroomaut values as integrated surfaces.

---

## 3.1.2 Distribution Pipe Losses — QH,dis,ls

### Formula (3.8) — Total pipe losses
```
QH,dis,ls,an = Σⱼ [Ψⱼ · (θm − θi,j) · Lⱼ · top,an]  / 1000   (kWh)
```

Where:
- **Ψ** = linear heat loss coefficient (W/(m·K))
- **θm** = mean water temperature (°C) = (θs + θr) / 2
- **θi** = ambient temperature around pipe (°C)
- **L** = pipe length including equivalent lengths for fittings (m)
- **top,an** = annual heating hours (h)

### Table 3.5 — Equivalent lengths for fittings
| Type | d ≤ 100mm | d > 100mm |
|---|---|---|
| Without insulation | 4 m | 6 m |
| With insulation | 1.5 m | 2.5 m |

### Table 3.6 — Min insulation thickness (λ=0.035 W/(m·K))
| Inner diameter | Min thickness |
|---|---|
| ≤ 22mm | 20mm |
| 23–35mm | 30mm |
| 35–100mm | = inner diameter |
| > 100mm | 100mm |
(50% reduction at crossings, junctions, wall penetrations)

### Formula (3.9) — Linear heat loss coeff. (hanging pipes)
```
Ψ = π / [1/(da·ha) + ln(da/di)/(2·λD)]   (W/(m·K))
```

### Formula (3.10) — Linear heat loss coeff. (embedded pipes)
```
Ψ = π / [ln(da/di)/(2·λD) + ln(4·z/da)/(2·λE)]   (W/(m·K))
```

### Formulas (3.11, 3.12) — Supply/return water temperatures
```
θs = (θs,des − θi) · βdis^(1/n) + θi   (°C)
θr = (θr,des − θi) · βdis^(1/n) + θi   (°C)
```

Where:
- θs,des, θr,des = design supply/return temps (°C)
- n = temperature exponent: 1.33 (radiators), 1.1 (floor heating)
- βdis = average partial distribution load (-)

---

## 3.1.3 Pump/Auxiliary Energy — WH,dis,aux

### Formula (3.13)
```
WH,dis,aux,an = WH,dis,hydr,an · edis   (kWh)
```

### Formula (3.14) — Hydraulic energy demand
```
WH,dis,hydr,an = (Phydr,des / 1000) · βdis · top,an · fNET · fHB · fG,PM   (kWh)
```

### Formula (3.15) — Pump design power
```
Phydr,des = 0.2778 · Δpdes · Vdes   (W)
```

### Formula (3.16) — Design pressure drop
```
Δpdes = 0.13 · Lmax + 2 + ΔpFH + ΔpG   (kPa)
```

### Formula (3.17) — Max circuit length (if unknown)
```
Lmax = 2 · (LL + LW/2 + Nlev · hlev + lc)   (m)
```

Where: lc=10m (two-pipe) or LL+LW (one-pipe)

Defaults: ΔpFH = 25 kPa (floor heating), ΔpG from Tab 3.7

### Table 3.7 — Generator pressure drop
| Type | ΔpG (kPa) |
|---|---|
| Water volume > 0.15 l/kW | 1 |
| Water volume ≤ 0.15 l/kW, Φ < 35kW | 20·Vdes² |
| Water volume ≤ 0.15 l/kW, Φ ≥ 35kW | 80 |

### Formula (3.18) — Design flow rate
```
Vdes = 3600 · ΦH,em,out / (c · ρ · Δϑdis,des)   (m³/h)
```

c=4.18 kJ/(kg·K), ρ=1000 kg/m³

### Formula (3.19) — Average partial load
```
βdis = QH,dis,out / (Φem · top)   (-)
```

Where QH,dis,out = QH + Qem,ls

### Correction factors
- **fNET**: 1.0 (two-pipe), 8.6·kby+0.7 (one-pipe)
- **fHB**: 1.0 (balanced), 1.15 (unbalanced)
- **fG,PM**: 1.0 (standard OTC), 0.75 (wall-mounted OTC), 0.45 (room temp control)

### Formula (3.20) — System power factor
```
edis = fe · (CP1 + CP2 · βdis^(-1))   (-)
```

### Table 3.8 — CP1, CP2 constants
| Pump regulation | CP1 | CP2 |
|---|---|---|
| No regulation | 0.25 | 0.75 |
| Δp constant | 0.75 | 0.25 |
| Δp variable | 0.90 | 0.10 |

**fe** (efficiency factor):
- If Pel,pmp known: fe = Pel,pmp / Phydr,des
- If unknown: fe = (1.25 + (200/Phydr,des)^0.5) · 1.5 · b
  - b=1 (new buildings), b=2 (existing buildings)

---

## 3.1.4 Recoverable Pump Heat — QH,dis,aux,rbl

### Formula (3.21)
```
QH,dis,aux,rbl = faux,rbl · WH,dis,aux,an   (kWh)
```

Where faux,rbl = 0.75 (pump without insulation) or 0.90 (with insulation)

---

## 3.1.5 Generation Losses — Qg,ls

### Formula (3.22) — Boiler generation loss
```
Qg,ls = ((1 − η) / η) · (QH + Qem,ls + QH,dis,ls,an)   (kWh)
```

Where η = boiler/source efficiency from Tab 3.9 or 3.10

### Table 3.9 — Heat exchanger station efficiency
| Medium | η |
|---|---|
| Steam/hot water | 0.97 |
| Hot water/hot water | 0.99 |
| Superheated water/hot water | 0.985 |
| Steam/superheated water | 0.96 |

### Table 3.10 — Transformation factors (Vyhláška 324/2016 Z.z.)

Key fuel types with efficiency, CO2 factor, and primary energy factor:

| Fuel / System | Efficiency η | CO2 (kg/kWh) | fp |
|---|---|---|---|
| **Natural gas** — old standard boiler | 0.83–0.89 | 0.220 | 1.1 |
| **Natural gas** — new standard boiler | 0.89–0.90 | 0.220 | 1.1 |
| **Natural gas** — low-temp boiler | 0.90–0.93 | 0.220 | 1.1 |
| **Natural gas** — condensing boiler | 0.97–1.05 | 0.220 | 1.1 |
| **Natural gas** — CHP | 0.85 | 0.220 | 1.1 |
| **LPG** — new standard | 0.89–0.90 | 0.2484 | 1.35 |
| **LPG** — low-temp | 0.90–0.93 | 0.2484 | 1.35 |
| **LPG** — condensing | 0.97–1.05 | 0.2484 | 1.35 |
| **Black coal** boiler | 0.72–0.75 | 0.360 | 1.1 |
| **Brown coal** boiler | 0.69–0.78 | 0.360 | 1.1 |
| **Light heating oil** boiler | 0.65–0.75 | 0.290 | 1.1 |
| **Wood pellets** — old | 0.82 | 0.020 | 0.20 |
| **Wood pellets** — new | 0.85 | 0.020 | 0.15 |
| **Wood chips** — old | 0.87 | 0.020 | 0.10 |
| **Wood chips** — new | 0.91 | 0.020 | 0.10 |
| **Firewood** boiler | 0.86/0.78 | 0.020 | 0.10 |
| **Firewood** gasification | 0.83 | 0.020 | 0.10 |
| **District heating** (coal) | 0.80 | 0.360 | 1.3 |
| **District heating** (biomass) | 0.72–0.80 | 0.020 | 1.3 |
| **District heating** CHP gas | 0.80–0.84 | 0.220 | 0.7 |
| **District heating** CHP coal | 0.60–0.70 | 0.360 | 0.7 |
| **Electric heating** | 0.99 | 0.167 | 2.2 |
| **HP air-water** radiator | 2.6 COP | 0.167 | 2.2 |
| **HP air-water** low-temp | 2.9 COP | 0.167 | 2.2 |
| **HP ground-water** radiator | 3.4 COP | 0.167 | 2.2 |
| **HP ground-water** low-temp | 3.9 COP | 0.167 | 2.2 |
| **HP water-water** radiator | 4.0 COP | 0.167 | 2.2 |
| **HP water-water** low-temp | 4.4 COP | 0.167 | 2.2 |
| **Photovoltaics** | 1.00 | 0.00 | 0.0 |

---

## 3.2 Worked Example (Panel Block Bratislava)

### Given data
- Building: Bratislava panel block, Ab = 4403.4 m²
- QH = 447,539 kWh (from Ch.2)
- Heating system: two-pipe radiators, 90/70°C
- Heating period: 212 days → top = 5088 h
- θe,comb = 3.86°C (normative)
- Source: district heating substation (outside building)
- Pump: Pel,pmp = 200 W, no regulation, existing building (b=2)

### 3.2.1 Emission losses
```
Δθhyd = 0.2 K   (Tab 3.1: two-pipe, static + system balancing)
Δθemt,sys = Δθstr + Δθemb + Δθrad + Δθim,emt
  Δθstr = (Δθstr,1 + Δθstr,2)/2 = (1.2 + 0.3)/2 = 0.75 K
  Δθemb = 0 K  (radiators, not integrated)
  Δθrad = 0 K  (h ≤ 4m)  
  Δθim,emt = -0.3 K
  → Δθemt,sys = 0.75 + 0 + 0 - 0.3 = 0.45 K

Δθctr,sys = Δθctr + Δθim,ctr + Δθroomaut
  Δθctr = 1.2 K  (Tab 3.4: P-controller/thermostatic head)
  Δθim,ctr = 0 K
  Δθroomaut = 0 K  (no automation)
  → Δθctr,sys = 1.2 + 0 + 0 = 1.2 K

Δθint,inc = 0.2 + 0.45 + 1.2 = 1.85 K
θint,inc = 20 + 1.85 = 21.85°C

Qem,ls = 447,539 · 1.85 / (21.85 - 3.86) = 46,023 kWh ✓
```

### 3.2.2 Distribution losses
```
βdis = QH,dis,out / (Φem · top) = 493,562 / (228.6 · 5088) = 0.42
  where QH,dis,out = QH + Qem,ls = 447,539 + 46,023 = 493,562 kWh

θs = (90-20) · 0.42^(1/1.33) + 20 = 56.5°C
θr = (70-20) · 0.42^(1/1.33) + 20 = 46.1°C
θm = (56.5 + 46.1) / 2 = 51.3°C

Pipe losses (Tab 3.11, θi=10°C, θm=51.3°C):
QH,dis,ls = (0.642·(51.3-10)·14 + 0.524·(51.3-10)·20 
          + 0.445·(51.3-10)·88 + 0.403·(51.3-10)·54) · 5088/1000
         = 16,893 kWh ✓
```

### 3.2.3 Pump energy
```
ΦH,em,out = 228.6 kW (design heat load per STN EN 12831-1)
Vdes = 3600 · 228.6 / (4.18 · 1000 · 20) = 9.85 m³/h
Lmax = 2·(25.03 + 21.23/2 + 12·2.8 + 10) = 158 m
Δpdes = 0.13·158 + 2 + 25 + 1 = 48.6 kPa
Phydr,des = 0.2778 · 48.6 · 9.85 = 133 W

WH,dis,hydr = (133/1000) · 0.42 · 5088 · 1 · 1 · 1 = 284 kWh

fe = (1.25 + (200/133)^0.5) · 1.5 · 2 = 7.43
edis = 7.43 · (0.25 + 0.75 · 0.42^(-1)) = 15.1

WH,dis,aux = 284 · 15.1 = 4,288 kWh ✓
```

### 3.2.4 Recoverable pump heat = 0 (pump in unheated area)

### 3.2.5 Generation loss = 0 (external heat substation)

### 3.2.6 Final result
```
QVYK = QH + Qem,ls + QH,dis,ls + WH,dis,aux
     = 447,539 + 46,023 + 16,893 + 4,288
     = 514,743 kWh

QVYK,m = 514,743 / 4403.4 = 116.9 kWh/(m²·rok)

After recoverable DHW pipe losses (QW,d,i = 2,077 kWh):
QVYK = 514,743 - 2,077 = 512,666 kWh
QVYK,m = 512,666 / 4403.4 = 116.4 kWh/(m²·rok) ✓
```
