# Kapitola 9: Energetická Certifikácia (Primárna Energia)

## 1. Ciel
Vypočítať **Globálny ukazovateľ - Primárna energia (Q_prim)** a **Emisie CO2** pre celú budovu na základe vypočítaných potrieb energie z predchádzajúcich kapitol (Vykurovanie, Teplá voda) a doplnkových vstupov (Osvetlenie, Chladenie, Vetranie). Určiť energetickú triedu budovy (A0 - G).

## 2. Vstupy
### 2.1 Z predchádzajúcich kapitol
-   **Vykurovanie (QH)**:
    -   Potreba energie (kWh/rok)
    -   Zdroj tepla (Palivo, Účinnosť)
    -   Pomocná energia (Čerpadlá, Regulácia)
-   **Teplá voda (QW)**:
    -   Potreba energie (kWh/rok)
    -   Zdroj tepla (Palivo, Účinnosť)
    -   Pomocná energia (Cirkulácia)

### 2.2 Nové vstupy (Osvetlenie a iné)
-   **Osvetlenie (Q_light)**:
    -   Zjednodušený výpočet alebo priamy vstup (kWh/rok).
    -   Typicky elektrina.
-   **Chladenie (Q_cool)** (voliteľné):
    -   Elektrina (EER).
-   **Vetranie (Q_vent)** (voliteľné):
    -   Elektrina (Rekuperácia).
-   **Fotovoltika (Q_pv)** (voliteľné):
    -   Vyrobená elektrina (kWh/rok) na odpočet.

### 2.3 Faktory primárnej energie (f_prim) a emisií CO2 (f_CO2)
Hodnoty podľa vyhlášky 324/2016 Z.z. (resp. 364/2012 Z.z.):

| Nosič energie | f_prim (kWh/kWh) | f_CO2 (t/MWh) |
| :--- | :--- | :--- |
| Zemný plyn | 1.1 | 0.220 |
| Elektrina | 2.2 | 0.167 |
| Drevené pelety | 0.2 | 0.020 |
| Kusové drevo | 0.1 | 0.020 |
| Uhlie (čierne) | 1.1 | 0.360 |
| CZT (všeobecne) | 1.3 | 0.300 |

*Poznámka: Užívateľ musí mať možnosť editovať tieto faktory.*

## 3. Výpočet

### 3.1 Dodaná energia (Q_del)
Pre každý nosič energie sa spočíta dodaná energia zo všetkých miest spotreby.

$$ Q_{del, i} = \sum Q_{miesto, i} $$

Kde $i$ je nosič (plyn, elektrina...).
Miesta spotreby:
-   Vykurovanie (Zdroj + Čerpadlá)
-   TV (Zdroj + Čerpadlá)
-   Osvetlenie
-   Chladenie/Vetranie

### 3.2 Primárna energia (Q_prim)
$$ Q_{prim} = \sum_i (Q_{del, i} \times f_{prim, i}) - Q_{pv} \times f_{prim, el} $$

### 3.3 Emisie CO2
$$ CO2 = \sum_i (Q_{del, i} \times f_{CO2, i}) $$

### 3.4 Merná primárna energia (q_prim)
$$ q_{prim} = \frac{Q_{prim}}{A_b} \quad [kWh/(m^2 \cdot a)] $$

## 4. Energetická trieda
Porovnanie $q_{prim}$ so škálou pre danú kategóriu budovy.

**Škála pre Rodinné domy (Globalný ukazovateľ):**
-   A0: $\le 54$
-   A1: $55 - 108$
-   B: $109 - 216$
-   C: $217 - 324$
-   D: $325 - 432$
-   E: $433 - 540$
-   F: $541 - 648$
-   G: $> 648$

*(Hodnoty sa líšia pre Bytové domy, Administratívu atď. - treba definovať škály alebo použiť tabuľku).*

## 5. Výstupy
-   Tabuľka energetickej bilancie (Dodaná vs Primárna).
-   Graf energetických tried (farebná škála so šípkou).
-   Celkové emisie CO2.
