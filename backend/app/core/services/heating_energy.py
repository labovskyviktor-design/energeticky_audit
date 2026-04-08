"""
Heating Energy Demand calculation — Chapter 3.

Calculates total heating energy demand (QVYK) by summing:
QH + Qem,ls + QH,dis,ls + WH,dis,aux + Qs,ls + Qg,ls - QW,d,i

Per STN EN 15316-1/2/3 and worked example (Bratislava panel block).
"""

import math

from pydantic import BaseModel, Field

from app.core.models.heating_system import (
    EmitterType,
    FuelType,
    HeatingEnergyInput,
    PipeSystem,
    PumpRegulation,
    RoomAutomation,
)
from app.core.services.heating_tables import (
    DELTA_THETA_ROOMAUT,
    FUEL_DATA,
    PUMP_CP,
    get_delta_p_g,
    get_delta_theta_ctr,
    get_delta_theta_emb,
    get_delta_theta_hyd,
    get_delta_theta_im_ctr,
    get_delta_theta_im_emt,
    get_delta_theta_rad,
    get_delta_theta_str,
    get_fuel_efficiency,
)
from app.core.models.calc_constants import (
    resolve_constants,
    ResolvedConstants,
    get_deviations,
)


# ── Result models ──────────────────────────────────────────────


class EmissionLossResult(BaseModel):
    """Výsledok výpočtu tepelnej straty systému odovzdávania."""
    # Context
    system_description: str = Field(description="Popis systému (napr. Radiátory, 70/55)")

    # Detailed components Delta Theta
    delta_theta_str: float = Field(description="∆θstr (K)")
    delta_theta_emb: float = Field(description="∆θemb (K)")
    delta_theta_rad: float = Field(description="∆θrad (K)")
    delta_theta_im_emt: float = Field(description="∆θim,emt (K)")
    delta_theta_ctr: float = Field(description="∆θctr (K)")
    delta_theta_roomaut: float = Field(description="∆θroomaut (K)")
    
    # Aggregated
    delta_theta_hyd: float = Field(description="∆θhyd (K)")
    delta_theta_emt_sys: float = Field(description="∆θemt,sys (K)")
    delta_theta_ctr_sys: float = Field(description="∆θctr,sys (K)")
    delta_theta_int_inc: float = Field(description="∆θint,inc (K)")
    theta_int_inc: float = Field(description="θint,inc (°C)")
    theta_e_comb: float = Field(description="θe,comb — priemerná vonkajšia teplota (°C)")
    q_em_ls: float = Field(description="Qem,ls — tepelná strata odovzdávania (kWh)")


class DistributionLossResult(BaseModel):
    """Výsledok výpočtu tepelnej straty z rozvodov."""
    total_length: float = Field(description="Celková dĺžka rozvodov (m)")
    beta_dis: float = Field(description="βdis — priemerné čiastočné zaťaženie (-)")
    theta_s: float = Field(description="θs — teplota prívodnej vody (°C)")
    theta_r: float = Field(description="θr — teplota vratnej vody (°C)")
    theta_m: float = Field(description="θm — stredná teplota vody (°C)")
    q_dis_ls: float = Field(description="QH,dis,ls — tepelná strata z rozvodov (kWh)")



class PumpEnergyResult(BaseModel):
    """Výsledok výpočtu vlastnej spotreby energie obehového čerpadla."""
    v_des: float = Field(description="Vdes — prietok v pracovnom bode (m³/h)")
    l_max: float = Field(description="Lmax — maximálna dĺžka okruhu (m)")
    delta_p_des: float = Field(description="∆pdes — tlakový spád (kPa)")
    p_hydr_des: float = Field(description="Phydr,des — výkon čerpadla (W)")
    
    # Factors for WH,dis,hydr
    f_net: float = Field(description="fnet — faktor usporiadania siete (-)")
    f_hb: float = Field(description="fhb — faktor hydraulického vyváženia (-)")
    f_g_pm: float = Field(description="fg,pm — faktor generátora (-)")
    
    w_hydr: float = Field(description="WH,dis,hydr — potreba hydraul. energie (kWh)")
    fe: float = Field(description="fe — faktor účinnosti (-)")
    e_dis: float = Field(description="edis — systémový výkonový faktor (-)")
    w_aux: float = Field(description="WH,dis,aux — vlastná spotreba energie (kWh)")
    q_aux_rbl: float = Field(description="QH,dis,aux,rbl — spätne získateľná časť (kWh)")


class GenerationLossResult(BaseModel):
    """Výsledok výpočtu tepelnej straty z výroby tepla."""
    efficiency: float = Field(description="η — účciiaiiainnosť zdroja (-)")
    q_gen_ls: float = Field(description="Qg,ls — tepelná strata výroby (kWh)")
    fuel_type: str = Field(description="Typ paliva / systému")


class HeatingEnergyResult(BaseModel):
    """Kompletný výsledok — potreba energie na vykurovanie."""
    building_name: str
    qh: float = Field(description="QH — potreba tepla na vykurovanie (kWh)")
    emission: EmissionLossResult
    distribution: DistributionLossResult
    pump: PumpEnergyResult
    generation: GenerationLossResult

    q_vyk: float = Field(description="QVYK — potreba energie na vykurovanie (kWh)")
    q_dhw_recoverable: float = Field(description="Spätne získateľná strata z TV (kWh)")
    q_vyk_final: float = Field(description="QVYK po zohľadnení TV (kWh)")
    ab: float = Field(description="Ab — podlahová plocha (m²)")
    q_vyk_m: float = Field(description="QVYK,m — merná potreba energie (kWh/(m²·rok))")
    
    resolved_constants: ResolvedConstants | None = None
    deviations: list[str] = Field(default_factory=list)


# ── Calculation functions ──────────────────────────────────────

def calculate_emission_loss(inp: HeatingEnergyInput) -> EmissionLossResult:
    """
    §3.1.1 — Tepelná strata systému odovzdávania tepla.

    Formula (3.1): Qem,ls = QH · [∆θint,inc / (θint,inc − θe,comb)]
    """
    em = inp.emission
    is_one_pipe_original = (
        em.pipe_system == PipeSystem.ONE_PIPE and not em.is_one_pipe_renovated
    )

    # ∆θhyd — Tab 3.1
    delta_hyd = get_delta_theta_hyd(
        em.pipe_system, em.hydraulic_balancing, em.n_emitters_le_10
    )

    # ∆θemt,sys = ∆θstr + ∆θemb + ∆θrad + ∆θim,emt  (3.4)
    delta_str = get_delta_theta_str(
        em.emitter_type, em.radiator_position, em.radiator_temp_drop,
        is_one_pipe_original, em.regulation,
    )
    delta_emb = get_delta_theta_emb(
        em.emitter_type, em.radiator_position, em.floor_insulation,
    )
    delta_rad = get_delta_theta_rad(em.emitter_type)
    delta_im_emt = get_delta_theta_im_emt(em.emitter_type)
    delta_emt_sys = delta_str + delta_emb + delta_rad + delta_im_emt

    # ∆θctr,sys = ∆θctr + ∆θim,ctr + ∆θroomaut  (3.5)
    delta_ctr = get_delta_theta_ctr(em.emitter_type, em.regulation, em.has_cert)
    delta_im_ctr = get_delta_theta_im_ctr()
    delta_roomaut = DELTA_THETA_ROOMAUT.get(em.room_automation, 0.0)
    delta_ctr_sys = delta_ctr + delta_im_ctr + delta_roomaut

    # Total ∆θint,inc (3.3)
    delta_int_inc = delta_hyd + delta_emt_sys + delta_ctr_sys

    # θint,inc (3.2)
    theta_int_inc = inp.theta_int_ini + delta_int_inc

    # Qem,ls (3.1)
    denominator = theta_int_inc - inp.theta_e_comb
    if denominator <= 0:
        q_em_ls = 0.0
    else:
        q_em_ls = inp.qh * (delta_int_inc / denominator)

    # System description
    desc = f"{em.emitter_type.value}"
    if em.emitter_type == EmitterType.RADIATOR:
        desc += f" ({em.radiator_temp_drop.value})"

    return EmissionLossResult(
        system_description=desc,
        delta_theta_str=round(delta_str, 3),
        delta_theta_emb=round(delta_emb, 3),
        delta_theta_rad=round(delta_rad, 3),
        delta_theta_im_emt=round(delta_im_emt, 3),
        delta_theta_ctr=round(delta_ctr, 3),
        delta_theta_roomaut=round(delta_roomaut, 3),
        
        delta_theta_hyd=round(delta_hyd, 3),
        delta_theta_emt_sys=round(delta_emt_sys, 3),
        delta_theta_ctr_sys=round(delta_ctr_sys, 3),
        delta_theta_int_inc=round(delta_int_inc, 3),
        theta_int_inc=round(theta_int_inc, 2),
        theta_e_comb=round(inp.theta_e_comb, 2),
        q_em_ls=round(q_em_ls, 0),
    )


def calculate_distribution_loss(inp: HeatingEnergyInput, q_em_ls: float) -> DistributionLossResult:
    """
    §3.1.2 — Tepelná strata z rozvodov vykurovacieho systému.

    Formulas (3.8), (3.11), (3.12).
    """
    top_an = inp.heating_days * 24  # annual heating hours

    # QH,dis,out = QH + Qem,ls
    q_dis_out = inp.qh + q_em_ls

    # βdis = QH,dis,out / (Φem · top)  (3.19)
    if inp.phi_em_out > 0 and top_an > 0:
        beta_dis = q_dis_out / (inp.phi_em_out * top_an)
    else:
        beta_dis = 0.5  # default

    # Temperature exponent n
    if inp.emission.emitter_type in (
        EmitterType.FLOOR_WET, EmitterType.FLOOR_DRY,
        EmitterType.FLOOR_DRY_LOW,
    ):
        n = 1.1
    else:
        n = 1.33  # radiators

    # Supply/return temps (3.11, 3.12)
    theta_i = inp.theta_int_ini
    beta_power = beta_dis ** (1 / n) if beta_dis > 0 else 0
    theta_s = (inp.theta_s_des - theta_i) * beta_power + theta_i
    theta_r = (inp.theta_r_des - theta_i) * beta_power + theta_i
    theta_m = (theta_s + theta_r) / 2

    # Pipe losses (3.8)
    q_dis_ls = 0.0
    total_len = 0.0
    for pipe in inp.pipes:
        total_len += pipe.length
        delta_t = theta_m - pipe.ambient_temp
        if delta_t > 0:
            # psi * delta_T * length * hours / 1000 = kWh
            q_dis_ls += (pipe.psi * delta_t * pipe.length * top_an) / 1000.0

    return DistributionLossResult(
        total_length=round(total_len, 1),
        beta_dis=round(beta_dis, 4),
        theta_s=round(theta_s, 1),
        theta_r=round(theta_r, 1),
        theta_m=round(theta_m, 1),
        q_dis_ls=round(q_dis_ls, 0),
    )


def calculate_pump_energy(inp: HeatingEnergyInput, beta_dis: float) -> PumpEnergyResult:
    """
    §3.1.3 — Vlastná spotreba energie systému rozvodu tepla.

    Formulas (3.13)–(3.20).
    """
    top_an = inp.heating_days * 24
    em = inp.emission
    pump = inp.pump

    # Design temperature drop
    delta_temp_des = inp.theta_s_des - inp.theta_r_des
    if delta_temp_des <= 0:
        delta_temp_des = 20.0

    # Flow rate Vdes (3.18)
    c = 4.18  # kJ/(kg·K)
    rho = 1000  # kg/m³
    v_des = 3600 * inp.phi_em_out / (c * rho * delta_temp_des)

    # Lmax (3.17) — max circuit length
    if inp.lmax_override is not None:
        l_max = inp.lmax_override
    elif inp.length_ll > 0 and inp.width_lw > 0:
        if em.pipe_system == PipeSystem.ONE_PIPE:
            lc = inp.length_ll + inp.width_lw
        else:
            lc = 10.0
        l_max = 2 * (inp.length_ll + inp.width_lw / 2 + inp.n_levels * inp.level_height + lc)
    else:
        l_max = 100.0  # default estimate

    # ΔpFH
    delta_p_fh = pump.delta_p_fh if pump.delta_p_fh is not None else 0.0
    if inp.emission.emitter_type in (
        EmitterType.FLOOR_WET, EmitterType.FLOOR_DRY, EmitterType.FLOOR_DRY_LOW,
    ) and pump.delta_p_fh is None:
        delta_p_fh = 25.0

    # ΔpG — Tab 3.7
    delta_p_g = get_delta_p_g(inp.phi_em_out, v_des)

    # Δpdes (3.16)
    delta_p_des = 0.13 * l_max + 2 + delta_p_fh + delta_p_g

    # Phydr,des (3.15)
    p_hydr_des = 0.2778 * delta_p_des * v_des

    # WH,dis,hydr,an (3.14)
    f_net = 1.0
    if em.pipe_system == PipeSystem.ONE_PIPE:
        f_net = 8.6 * pump.kby + 0.7

    f_hb = 1.0 if pump.is_balanced else 1.15

    f_g_pm_map = {
        "standard_otc": 1.0,
        "wall_mounted_otc": 0.75,
        "room_temp": 0.45,
    }
    f_g_pm = f_g_pm_map.get(pump.generator_regulation.value, 1.0)

    w_hydr = (p_hydr_des / 1000) * beta_dis * top_an * f_net * f_hb * f_g_pm

    # fe — efficiency factor
    if pump.p_el_pmp is not None and pump.p_el_pmp > 0:
        fe = pump.p_el_pmp / p_hydr_des if p_hydr_des > 0 else 1.0
    else:
        b = 1 if pump.is_new_building else 2
        if p_hydr_des > 0:
            fe = (1.25 + (200 / p_hydr_des) ** 0.5) * 1.5 * b
        else:
            fe = 1.0

    # edis (3.20)
    cp1, cp2 = PUMP_CP.get(pump.regulation, (0.25, 0.75))
    if beta_dis > 0:
        e_dis = fe * (cp1 + cp2 * beta_dis ** (-1))
    else:
        e_dis = fe * cp1

    # WH,dis,aux,an (3.13)
    w_aux = w_hydr * e_dis

    # Recoverable pump heat (3.21)
    if pump.is_in_heated_zone:
        f_aux_rbl = 0.90 if pump.is_insulated else 0.75
        q_aux_rbl = f_aux_rbl * w_aux
    else:
        q_aux_rbl = 0.0

    return PumpEnergyResult(
        v_des=round(v_des, 2),
        l_max=round(l_max, 1),
        delta_p_des=round(delta_p_des, 1),
        p_hydr_des=round(p_hydr_des, 0),
        f_net=round(f_net, 2),
        f_hb=round(f_hb, 2),
        f_g_pm=round(f_g_pm, 2),
        w_hydr=round(w_hydr, 0),
        fe=round(fe, 2),
        e_dis=round(e_dis, 2),
        w_aux=round(w_aux, 0),
        q_aux_rbl=round(q_aux_rbl, 0),
    )


def calculate_generation_loss(
    inp: HeatingEnergyInput,
    q_em_ls: float,
    q_dis_ls: float,
) -> GenerationLossResult:
    """
    §3.1.5 — Tepelná strata z výroby tepla.

    Formula (3.22): Qg,ls = ((1 − η) / η) · (QH + Qem,ls + QH,dis,ls)
    For external sources, Qg,ls = 0.
    """
    gen = inp.generation

    if gen.is_external:
        return GenerationLossResult(
            efficiency=1.0,
            q_gen_ls=0.0,
            fuel_type=gen.fuel_type.value,
        )

    if gen.efficiency_override is not None:
        eta = gen.efficiency_override
    else:
        eta = get_fuel_efficiency(gen.fuel_type)

    if eta <= 0:
        eta = 0.85

    q_input = inp.qh + q_em_ls + q_dis_ls
    # (1 - eta) / eta * input (3.22)
    q_gen_ls = ((1.0 - eta) / eta) * q_input

    return GenerationLossResult(
        efficiency=round(eta, 3),
        q_gen_ls=round(q_gen_ls, 0),
        fuel_type=gen.fuel_type.value,
    )


def calculate_heating_energy_demand(inp: HeatingEnergyInput) -> HeatingEnergyResult:
    """
    §3.1.6 — Celková potreba energie na vykurovanie.

    Formula (3.23): QVYK = QH + Qem,ls + QH,dis,ls + WH,dis,aux + Qs,ls + Qg,ls
    """
    # Step 1: Emission losses
    emission = calculate_emission_loss(inp)

    # Step 2: Distribution losses
    distribution = calculate_distribution_loss(inp, emission.q_em_ls)

    # Step 3: Pump energy
    pump = calculate_pump_energy(inp, distribution.beta_dis)

    # Step 4: Generation losses
    generation = calculate_generation_loss(
        inp, emission.q_em_ls, distribution.q_dis_ls,
    )

    # Step 5: Total (3.23) — Qs,ls not yet implemented, assumed 0
    q_vyk = (
        inp.qh
        + emission.q_em_ls
        + distribution.q_dis_ls
        + pump.w_aux
        + generation.q_gen_ls  # 0 if external source
    )

    # Step 6: Subtract recoverable DHW losses
    q_vyk_final = q_vyk - inp.q_dhw_recoverable

    # specific demand
    q_vyk_m = q_vyk_final / inp.ab if inp.ab > 0 else 0.0

    resolved = resolve_constants(inp.overrides)

    return HeatingEnergyResult(
        building_name=inp.building_name,
        qh=inp.qh,
        emission=emission,
        distribution=distribution,
        pump=pump,
        generation=generation,
        q_vyk=round(q_vyk, 0),
        q_dhw_recoverable=round(inp.q_dhw_recoverable, 0),
        q_vyk_final=round(q_vyk_final, 0),
        ab=inp.ab,
        q_vyk_m=round(q_vyk_m, 1),
        resolved_constants=resolved,
        deviations=get_deviations(resolved),
    )
