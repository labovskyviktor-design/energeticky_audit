# Chapter 4: Potreba energie na prípravu teplej vody (DHW)

**Goal:** Calculate the total energy demand for domestic hot water preparation ($Q_{TV}$ or $Q_{W}$).
**Reference:** STN EN 15316-3, STN EN 15316-5.

## 1. Celková potreba energie ($Q_{TV}$)
The total energy required corresponds to the sum of the net heat demand and all system losses.
$$Q_{TV} = Q_W + Q_{W,d} + Q_{W,s} + Q_{W,g}$$

Where:
*   $Q_W$: Net heat demand for DHW (Potreba tepla na prípravu TV).
*   $Q_{W,d}$: Distribution heat losses (Tepelná strata z distribúcie TV).
*   $Q_{W,s}$: Storage heat losses (Tepelná strata z akumulácie TV).
*   $Q_{W,g}$: Generation heat losses (Tepelná strata z výroby TV).

## 2. Net Heat Demand ($Q_W$)
Calculated using a simplified method based on floor area.
$$Q_W = 20 \cdot A_b \quad [kWh/rok]$$
*   $A_b$: Total floor area (from Chapter 1).
*   $20$: Default specific demand factor ($kWh/(m^2 \cdot a)$) for residential buildings.

## 3. Distribution Losses ($Q_{W,d}$)
Losses from pipes (circulation and supply) and auxiliary energy.

### A. Pipe Heat Loss ($Q_{W,d,ls}$)
Sum of losses from all pipe segments.
$$Q_{W,d,ls} = \sum \left( \frac{1}{1000} \cdot U_i \cdot L_i \cdot (\theta_{W,d,i} - \theta_{amb}) \cdot t_{op} \right)$$
*   $U_i$: Linear thermal transmittance ($W/mK$).
    *   $\Psi$ input? Or calculated from insulation? (Use $\Psi$ as input similar to Ch3).
*   $L_i$: Length of pipe segment ($m$).
*   $\theta_{W,d,i}$: Average water temperature in pipe ($^\circ C$). Typically $55-60^\circ C$.
    *   Example uses $\theta_m = 57.5^\circ C$.
*   $\theta_{amb}$: Ambient temperature ($^\circ C$).
*   $t_{op}$: Operation hours. $365 \cdot 24 = 8760$ h for circulation.

### B. Stagnation Loss ($Q_{W,d,stag}$)
Losses in dead legs (pipes without circulation, e.g., to taps).
$$Q_{W,d,stag} = \frac{365 \cdot N_{tap}}{3600 \cdot 1000} \cdot V_W \cdot c_W \cdot (\theta_{W,d} - \theta_{amb})$$
*   $N_{tap}$: Number of draw-offs per day (e.g., 5).
*   $V_W$: Volume of water in dead-leg pipes ($m^3$).
*   $c_W$: Specific heat capacity of water = $4181 \, J/(kgK)$.
*   **Recoverable Heat**: Part of this loss heats the building during heating season.
    $$Q_{DHW,recoverable} = Q_{W,d,stag} \cdot \frac{days_{heating}}{365}$$

### C. Auxiliary Energy ($W_{W,d,pump}$)
$$W_{W,d,pump} = \frac{365}{1000} \cdot t_{pump} \cdot P_{pump}$$
*   $t_{pump}$: Pump operation hours/day (usually 24).
*   $P_{pump}$: Pump power ($W$).

## 4. Storage Losses ($Q_{W,s}$)
Losses from the storage tank.
$$Q_{W,s} = Q_{st,loss,day} \cdot 365 \cdot \frac{\theta_{W,s} - \theta_{amb}}{\theta_{test,diff}}$$
*   $Q_{st,loss,day}$: Standby loss ($kWh/day$). If unknown, use max allowed from Tab 4.1.
*   $\theta_{W,s}$: Storage temp ($^\circ C$).
*   $\theta_{amb}$: Ambient temp around tank ($^\circ C$).

## 5. Generation Losses ($Q_{W,g}$)
Depends on the heat source efficiency.
$$Q_{W,g} = Q_{input} \cdot \frac{1 - \eta}{\eta}$$
*   Uses same efficiency factors as Chapter 3 (Tab 3.10).
*   If external source (OST), usually 0 loss *in building*.

## Inputs Required
*   **Global**: $A_b$, Heating days (for recoverable).
*   **Pipes**: List of segments (Length, DN/Volume, $\Psi$, Ambient temp).
*   **Circulation**: Pump power, Operation hours.
*   **Storage**: Volume, Standby loss, Ambient temp.
*   **Generation**: Source type (Reuse Ch3 source?), Efficiency.

## Outputs
*   $Q_W$
*   $Q_{W,d}$
*   $Q_{W,s}$
*   $Q_{W,g}$
*   $Q_{TV}$ (Total)
*   $Q_{DHW,recoverable}$ (to feed back into Ch2/Ch3).
