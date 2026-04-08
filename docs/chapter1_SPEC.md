# Chapter 1 — SPEC: Tepelno-technické vlastnosti stavebných konštrukcií

> **Source of truth:** Krajčík, M. a kol. — Energetické hodnotenie budov, str. 10–22

## 1. Formulas

### (1.1) Požiadavka na U
```
U ≤ U_r1   [W/(m²·K)]
```
Konštrukcia musí mať U ≤ požadovanej (odporúčanej) hodnote Ur1.

### (1.2) Výpočet U z tepelného odporu
```
U = 1 / (Rsi + ΣR + Rse)   [W/(m²·K)]
```
- **Rsi** — tepelný odpor na vnútornom povrchu ((m²·K)/W)
- **R** — súčet odporov vrstiev ((m²·K)/W)
- **Rse** — tepelný odpor na vonkajšom povrchu ((m²·K)/W)

### (1.3) Požiadavka na R
```
R ≥ R_r1   [(m²·K)/W]
```

### (1.4) Výpočet R z vrstiev
```
ΣR = Σ(di / λi)   [(m²·K)/W]
```
- **di** — hrúbka vrstvy (m)
- **λi** — súčiniteľ tepelnej vodivosti (W/(m·K))

### (1.5) Požiadavka na okná
```
UW ≤ UW,r1   [W/(m²·K)]
```
Pre budovy s čiastočnou obnovou: `UW ≤ UW,max`

---

## 2. Reference Tables (STN 73 0540-2/Z1)

### Tab 1.1 — Požiadavky na U nepriesvitných konštrukcií

| Konštrukcia | U_max | U_N | U_r1 | U_r2 |
|---|---|---|---|---|
| Vonkajšia stena (sklon > 45°) | 0.46 | 0.32 | 0.22 | 0.15 |
| Plochá strecha (≤ 45°) | 0.30 | 0.20 | 0.15 | 0.10 |
| Strop nad vonkajším prostredím | 0.30 | 0.20 | 0.15 | 0.10 |
| Strop pod nevyk. priestorom | 0.35 | 0.25 | 0.20 | 0.15 |

### Tab 1.3 — Požiadavky na U_W otvorových konštrukcií

| Konštrukcia | U_W,max | U_W,N | U_W,r1 | U_W,r2 |
|---|---|---|---|---|
| Okná, dvere v obvodovej stene | 1.7 | 1.4 | 1.0 | 0.6 |
| Okná v šikmej streche | 1.7 | 1.5 | 1.4 | 1.0 |

### Surface Resistance Constants

| Parameter | Value | Condition |
|---|---|---|
| Rse | 0.04 | Vonkajší povrch |
| Rsi | 0.13 | Vnútorný (vodorovný tok) |
| Rsi | 0.10 | Vnútorný (tok zdola nahor) |
| Rsi | 0.17 | Vnútorný (tok zhora nadol) |

---

## 3. Example Building (Test Data)

**Bytový dom, Bratislava, P 1.14 BA**
- 13 podlaží, nepodpivničený, 48 bytov
- θ_int = 20 °C, θ_ext = -11 °C

### 3.1 Obvodový plášť (Tab 1.4)
| # | Materiál | d (m) | λ (W/(m·K)) | R (m²·K/W) |
|---|---|---|---|---|
| 1 | Omietka vnútorná | 0.010 | 0.880 | 0.011 |
| 2 | Železobetón | 0.150 | 1.580 | 0.095 |
| 3 | Penový polystyrén | 0.080 | 0.070 | 1.143 |
| 4 | Železobetón | 0.070 | 1.580 | 0.044 |
| 5 | Omietka vonkajšia | 0.020 | 1.160 | 0.017 |

- **ΣR = 1.31** → Rsi=0.13 + 1.31 + Rse=0.04 = 1.48 → **U = 0.68** → Ur1=0.22 → ❌ **NEVYHOVUJE**

### 3.2 Strešný plášť (Tab 1.5)
| # | Materiál | d (m) | λ (W/(m·K)) | R (m²·K/W) |
|---|---|---|---|---|
| 1 | Omietka vnútorná | 0.010 | 0.880 | 0.011 |
| 2 | ŽB stropný panel | 0.150 | 1.580 | 0.095 |
| 3 | Penový polystyrén | 0.050 | 0.044 | 1.136 |
| 4 | Pórobetónový panel | 0.100 | 0.190 | 0.526 |
| 5 | Hydroizolácia | 0.015 | 0.210 | 0.071 |

- **ΣR = 1.84** → Rsi=0.10 + 1.84 + Rse=0.04 = 1.98 → **U = 0.50** → Ur1=0.15 → ❌ **NEVYHOVUJE**

### 3.3 Strop nad nevyk. podlažím (Tab 1.6)
| # | Materiál | d (m) | λ (W/(m·K)) | R (m²·K/W) |
|---|---|---|---|---|
| 1 | PVC podlahovina | 0.005 | 0.160 | 0.031 |
| 2 | Cementový poter | 0.020 | 1.020 | 0.020 |
| 3 | ŽB stropný panel | 0.150 | 1.340 | 0.112 |
| 4 | Dosky z čadičovej plsti | 0.060 | 0.048 | 1.250 |
| 5 | Lignátové dosky | 0.006 | 0.220 | 0.027 |
| 6 | Omietka vnútorná | 0.010 | 0.700 | 0.014 |

- **ΣR = 1.45** → Rsi=0.17 + 1.45 + Rsi=0.17 = 1.79 → **U = 0.56** → Ur1=0.85 → ✅ **VYHOVUJE**

### 3.4 Otvorové konštrukcie (Tab 1.7)
| Konštrukcia | U_W | U_W,max | Posúdenie |
|---|---|---|---|
| Pôvodné drevené zdvojené okná | 2.7 | 1.7 | ❌ NEVYHOVUJE |
| Oceľové okná (schodisko/výťah) | 5.2 | 1.7 | ❌ NEVYHOVUJE |
| Oceľová vstupná zasklená stena | 5.2 | 1.7 | ❌ NEVYHOVUJE |
| Vymenené plastové okná | 1.3 | 1.7 | ✅ VYHOVUJE |

---

## 4. Scope Note

> **Zjednodušenie projektu:** Užívateľ zadáva priamo hodnotu U a plochy konštrukcií.
> Výpočet R z vrstiev (vzorce 1.2, 1.4) implementujeme ako **bonus funkciu**
> (voliteľný "detail mode"), ale core flow pracuje s hotovými U-hodnotami.
