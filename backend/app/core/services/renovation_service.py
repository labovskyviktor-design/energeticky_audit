"""
Renovation Service — Chapter 6: Návrh úsporných opatrení.

Takes the 'before' state from Ch2+Ch3, applies selected measures,
recalculates QH (envelope) and Q_VYK (system), and returns a
before/after comparison.
"""

from ..models.climate import (
    ConstructionHTEntry,
    HeatingDemandInput,
    VentilationData,
    WindowSolarEntry,
    ClimateData,
)
from ..models.building import AssessmentLevel
from ..models.heating_system import (
    HeatingEnergyInput,
    EmissionSystemInput,
    DistributionPipeInput,
    PumpInput,
    GenerationSourceInput,
    PipeSystem,
    HydraulicBalancing,
    EmitterType,
    RegulationType,
    RadiatorPosition,
    RadiatorTempDrop,
    PumpRegulation,
    FuelType,
)
from ..models.renovation import (
    MeasureID,
    PSI_INSULATED,
    RenovationInput,
    RenovationComparisonResult,
    SelectedMeasure,
    MEASURES_CATALOG,
)
from .energy_balance import calculate_heating_demand
from .heating_energy import calculate_heating_energy_demand
from .dhw import calculate_dhw_demand
from ..models.dhw import DHWInput, DHWPipeInput, DHWStorageInput, DHWPumpInput, DHWGenerationInput


# ══════════════════════════════════════════════════════════════
# ENVELOPE: Recalculate QH from constructions
# ══════════════════════════════════════════════════════════════

def _recalc_qh(rinp: RenovationInput, constructions: list[dict], delta_u: float) -> float:
    """
    Recalculate QH using the Ch2 engine with given constructions and ΔU.
    Returns QH in kWh.
    """
    # Build ConstructionHTEntry list
    ht_entries = [
        ConstructionHTEntry(
            name=c.get("name", ""),
            u_value=c.get("u_value", 0.5),
            area=c.get("area", 1.0),
            bx=c.get("bx", 1.0),
        )
        for c in constructions
        if c.get("u_value", 0) > 0 and c.get("area", 0) > 0
    ]

    # Build solar entries
    solar_entries = [
        WindowSolarEntry(
            orientation=w.get("orientation", "south"),
            area=w.get("area", 1.0),
            ggl=w.get("ggl", 0.62),
            f_shading=w.get("f_shading", 0.5),
        )
        for w in rinp.windows_solar
        if w.get("area", 0) > 0
    ]

    # Build ventilation
    ventilation = VentilationData(
        v_vb_ratio=rinp.v_vb_ratio,
        n_inf_override=rinp.n_inf_override,
    )

    # Build climate
    climate = ClimateData(
        theta_int=rinp.theta_int_ini,
        theta_e_m=rinp.theta_e_comb,
        heating_days=rinp.heating_days,
    )

    vb = rinp.vb if rinp.vb > 0 else rinp.ab * 2.8  # fallback estimate

    hdi = HeatingDemandInput(
        building_name=rinp.building_name,
        ab=rinp.ab,
        vb=vb,
        constructions=ht_entries,
        delta_u=delta_u,
        ventilation=ventilation,
        qi=rinp.qi,
        windows_solar=solar_entries,
        climate=climate,
        eta_gn=rinp.eta_gn,
    )

    result = calculate_heating_demand(hdi)
    return result.qh


# ══════════════════════════════════════════════════════════════
# SYSTEM: Build HeatingEnergyInput for Ch3
# ══════════════════════════════════════════════════════════════

def _build_heating_input(
    rinp: RenovationInput,
    qh_override: float | None = None,
    after: bool = False,
) -> tuple["HeatingEnergyInput", list[str]]:
    """
    Build a HeatingEnergyInput from RenovationInput.
    If after=True, apply the selected renovation measures.
    If qh_override is provided, use it instead of rinp.qh.
    """
    qh = qh_override if qh_override is not None else rinp.qh

    # Start with current emission system parameters
    regulation_type = rinp.emission_regulation_type
    hydraulic_balancing = rinp.emission_hydraulic_balancing
    theta_s_des = rinp.theta_s_des
    theta_r_des = rinp.theta_r_des

    # Current pipes
    pipes_data = rinp.pipes.copy()

    # Current pump
    pump_p_el = rinp.pump_p_el
    pump_regulation = rinp.pump_regulation
    pump_delta_p = rinp.pump_delta_p_des

    # Current generation
    fuel_type = rinp.fuel_type
    is_external = rinp.is_external
    efficiency_override = rinp.efficiency_override

    # Collect applied measure names
    applied_names = []

    if after:
        enabled = {m.measure_id: m for m in rinp.measures if m.enabled}

        # ─── Hydraulic Balancing ─────────────────────────
        if MeasureID.HYDRAULIC_BALANCING in enabled:
            hydraulic_balancing = "static_with_system"
            applied_names.append("Hydraulické vyregulovanie")

        # ─── Thermostatic Valves ─────────────────────────
        if MeasureID.THERMOSTATIC_VALVES in enabled:
            regulation_type = "p_controller"
            applied_names.append("Výmena termostatických ventilov")

        # ─── Temperature Gradient Reduction ──────────────
        if MeasureID.TEMP_GRADIENT_REDUCTION in enabled:
            m = enabled[MeasureID.TEMP_GRADIENT_REDUCTION]
            theta_s_des = m.new_theta_s_des or 75.0
            theta_r_des = m.new_theta_r_des or 65.0
            applied_names.append(f"Zníženie teplotného spádu ({theta_s_des}/{theta_r_des}°C)")

        # ─── Pipe Insulation ─────────────────────────────
        if MeasureID.PIPE_INSULATION in enabled:
            new_pipes = []
            for p in pipes_data:
                dn = p.get("dn", 50)
                closest_dn = min(PSI_INSULATED.keys(), key=lambda d: abs(d - dn))
                new_psi = PSI_INSULATED[closest_dn]
                new_pipes.append({**p, "psi": new_psi})
            pipes_data = new_pipes
            applied_names.append("Izolácia potrubí (40mm, λ=0.036)")

        # ─── New Pump ────────────────────────────────────
        if MeasureID.NEW_PUMP in enabled:
            m = enabled[MeasureID.NEW_PUMP]
            pump_regulation = m.new_pump_regulation or "dp_variable"
            if m.new_pump_p_el:
                pump_p_el = m.new_pump_p_el
            applied_names.append("Nové čerpadlo s frekvenčným meničom")

        # ─── New Boiler ──────────────────────────────────
        if MeasureID.NEW_BOILER in enabled:
            m = enabled[MeasureID.NEW_BOILER]
            if m.new_fuel_type:
                fuel_type = m.new_fuel_type
            if m.new_efficiency is not None:
                efficiency_override = m.new_efficiency
            is_external = False
            applied_names.append("Nový zdroj tepla")

    # Build pipe inputs
    pipe_inputs = [
        DistributionPipeInput(
            name=p.get("name", ""),
            dn=p.get("dn", 50),
            psi=p.get("psi", 0.5),
            length=p.get("length", 10),
            ambient_temp=p.get("ambient_temp", 10.0),
        )
        for p in pipes_data
    ]

    # Build emission input
    emission_input = EmissionSystemInput(
        pipe_system=PipeSystem(rinp.emission_pipe_system),
        hydraulic_balancing=HydraulicBalancing(hydraulic_balancing),
        emitter_type=EmitterType(rinp.emission_emitter_type),
        regulation=RegulationType(regulation_type),
        radiator_position=RadiatorPosition(rinp.emission_radiator_position),
        radiator_temp_drop=RadiatorTempDrop(rinp.emission_radiator_temp_drop),
    )

    # Build pump input
    pump_input = PumpInput(
        p_el_pmp=pump_p_el,
        regulation=PumpRegulation(pump_regulation),
    )

    # Build generation input
    gen_input = GenerationSourceInput(
        fuel_type=FuelType(fuel_type),
        is_external=is_external,
        efficiency_override=efficiency_override,
    )

    return HeatingEnergyInput(
        building_name=rinp.building_name,
        qh=qh,
        ab=rinp.ab,
        phi_em_out=rinp.phi_em_out,
        theta_s_des=theta_s_des,
        theta_r_des=theta_r_des,
        theta_e_comb=rinp.theta_e_comb,
        theta_int_ini=rinp.theta_int_ini,
        heating_days=rinp.heating_days,
        length_ll=rinp.length_ll,
        width_lw=rinp.width_lw,
        n_levels=rinp.n_levels,
        level_height=rinp.level_height,
        emission=emission_input,
        pipes=pipe_inputs,
        pump=pump_input,
        generation=gen_input,
        q_dhw_recoverable=rinp.q_dhw_recoverable,
    ), applied_names


# ══════════════════════════════════════════════════════════════
# DHW: Build DHWInput for Ch4
# ══════════════════════════════════════════════════════════════

def _build_dhw_input(
    rinp: RenovationInput,
    after: bool = False,
) -> tuple["DHWInput", list[str]]:
    """
    Build a DHWInput from RenovationInput for Chapter 4 calculations.
    """
    applied_names = []

    # Start with base state
    dhw_q_wa = rinp.dhw_q_wa
    fuel_type = rinp.dhw_fuel_type
    is_external = rinp.dhw_is_external
    efficiency_override = rinp.dhw_efficiency_override
    pipes_data = rinp.dhw_pipes.copy()

    if after:
        enabled = {m.measure_id: m for m in rinp.measures if m.enabled}

        # ─── DHW Pipe Insulation ─────────────────────────
        if MeasureID.DHW_PIPE_INSULATION in enabled:
            new_pipes = []
            for p in pipes_data:
                dn = p.get("dn", 25)
                closest_dn = min(PSI_INSULATED.keys(), key=lambda d: abs(d - dn))
                new_psi = PSI_INSULATED[closest_dn]
                new_pipes.append({**p, "psi": new_psi})
            pipes_data = new_pipes
            applied_names.append("Izolácia rozvodov TV (40mm, λ=0.036)")

        # ─── DHW Water Saving ────────────────────────────
        if MeasureID.DHW_WATER_SAVING in enabled:
            m = enabled[MeasureID.DHW_WATER_SAVING]
            if m.new_dhw_q_wa:
                dhw_q_wa = m.new_dhw_q_wa
            else:
                dhw_q_wa = max(10, dhw_q_wa * 0.7)  # default conservative 30% saving
            applied_names.append("Úsporné armatúry na TV")

        # ─── DHW New Source ──────────────────────────────
        if MeasureID.DHW_NEW_SOURCE in enabled:
            m = enabled[MeasureID.DHW_NEW_SOURCE]
            if m.new_dhw_fuel_type:
                fuel_type = m.new_dhw_fuel_type
            if m.new_dhw_efficiency is not None:
                efficiency_override = m.new_dhw_efficiency
            is_external = False
            applied_names.append("Nový zdroj pre prípravu TV")

    # Build Pydantic inputs
    pipe_inputs = [
        DHWPipeInput(
            name=p.get("name", "Rozvod TV"),
            length=p.get("length", 10),
            dn=p.get("dn", 25),
            psi=p.get("psi", 0.3),
            ambient_temp=p.get("ambient_temp", 15.0),
            water_temp=rinp.dhw_water_temp,
            is_circulation=p.get("is_circulation", False)
        )
        for p in pipes_data
    ]

    has_storage = rinp.dhw_tank_volume > 0
    storage_input = DHWStorageInput(
        volume=rinp.dhw_tank_volume,
        standby_loss=rinp.dhw_tank_loss,
        store_temp=rinp.dhw_water_temp,
        has_storage=has_storage
    )

    has_circ = rinp.dhw_pump_hours > 0 and rinp.dhw_pump_p_el > 0
    pump_input = DHWPumpInput(
        power=rinp.dhw_pump_p_el,
        daily_hours=rinp.dhw_pump_hours / 365,
        has_circulation=has_circ
    )

    gen_input = DHWGenerationInput(
        fuel_type=FuelType(fuel_type),
        efficiency_override=efficiency_override,
        is_external=is_external
    )

    result_inp = DHWInput(
        ab=rinp.ab,
        pipes=pipe_inputs,
        storage=storage_input,
        pump=pump_input,
        generation=gen_input,
        heating_days=rinp.heating_days,
        # Default overrides to ensure q_wa is applied
        overrides=CalcConstantsOverride(dhw_q_wa=dhw_q_wa)
    )
    return result_inp, applied_names


# ══════════════════════════════════════════════════════════════
# MAIN: Full renovation comparison
# ══════════════════════════════════════════════════════════════

def calculate_renovation(rinp: RenovationInput) -> RenovationComparisonResult:
    """
    Calculate the before/after comparison for renovation measures.

    Flow:
    1. Determine QH_before (from input or recalculated from constructions_before)
    2. Determine QH_after (from constructions_after with new U-values, or same as before)
    3. Build Ch3 before state → calculate Q_VYK (before)
    4. Apply Ch3 system measures + new QH → calculate Q_VYK (after)
    5. Return full comparison with savings
    """
    # Collect envelope measure names
    envelope_names = []
    enabled_ids = {m.measure_id for m in rinp.measures if m.enabled}

    # ── Step 1: Determine QH_before ──────────────────────
    has_envelope_before = len(rinp.constructions_before) > 0
    if has_envelope_before:
        qh_before = _recalc_qh(rinp, rinp.constructions_before, rinp.delta_u_before)
    else:
        qh_before = rinp.qh

    # ── Step 2: Determine QH_after ───────────────────────
    has_envelope_after = len(rinp.constructions_after) > 0
    if has_envelope_after:
        qh_after = _recalc_qh(rinp, rinp.constructions_after, rinp.delta_u_after)

        # Identify which envelope measures were applied
        if MeasureID.ENVELOPE_INSULATION in enabled_ids:
            envelope_names.append("Zateplenie obvodového plášťa (ETICS)")
        if MeasureID.WINDOW_REPLACEMENT in enabled_ids:
            envelope_names.append("Výmena okien a dverí")
        # If user provided constructions_after but didn't check specific measures,
        # still note generic envelope improvement
        if not envelope_names:
            envelope_names.append("Zlepšenie obalových konštrukcií")
    else:
        qh_after = qh_before  # No envelope change

    # ── Step 3: Before Ch3 ───────────────────────────────
    before_input, _ = _build_heating_input(rinp, qh_override=qh_before, after=False)
    before_result = calculate_heating_energy_demand(before_input)

    # ── Step 4: After Ch3 ────────────────────────────────
    after_input, system_names = _build_heating_input(rinp, qh_override=qh_after, after=True)
    after_result = calculate_heating_energy_demand(after_input)

    # ── Step 5: DHW Evaluation (if requested) ────────────
    dhw_applied = []
    dhw_res_before = None
    dhw_res_after = None
    if rinp.dhw_calculate:
        dhw_inp_before, _ = _build_dhw_input(rinp, after=False)
        dhw_res_before = calculate_dhw_demand(dhw_inp_before)
        
        dhw_inp_after, dhw_applied = _build_dhw_input(rinp, after=True)
        dhw_res_after = calculate_dhw_demand(dhw_inp_after)

    # ── Step 6: Combine results ──────────────────────────
    all_applied = envelope_names + system_names + dhw_applied

    savings_kwh = before_result.q_vyk_final - after_result.q_vyk_final
    savings_pct = (savings_kwh / before_result.q_vyk_final * 100) if before_result.q_vyk_final > 0 else 0
    qh_savings = qh_before - qh_after

    res = RenovationComparisonResult(
        # Heating Before
        q_vyk_before=round(before_result.q_vyk_final, 0),
        q_em_ls_before=round(before_result.emission.q_em_ls, 0),
        q_dis_ls_before=round(before_result.distribution.q_dis_ls, 0),
        w_pump_before=round(before_result.pump.w_aux, 0),
        q_gen_ls_before=round(before_result.generation.q_gen_ls, 0),

        # Heating After
        q_vyk_after=round(after_result.q_vyk_final, 0),
        q_em_ls_after=round(after_result.emission.q_em_ls, 0),
        q_dis_ls_after=round(after_result.distribution.q_dis_ls, 0),
        w_pump_after=round(after_result.pump.w_aux, 0),
        q_gen_ls_after=round(after_result.generation.q_gen_ls, 0),

        # Heating Diffs
        savings_kwh=round(savings_kwh, 0),
        savings_pct=round(savings_pct, 1),

        applied_measures=all_applied,

        # Metadata
        qh_before=round(qh_before, 0),
        qh_after=round(qh_after, 0),
        qh_savings_kwh=round(qh_savings, 0),
        ab=rinp.ab,
        q_vyk_m_before=round(before_result.q_vyk_m, 1),
        q_vyk_m_after=round(after_result.q_vyk_m, 1),
    )

    # Attach DHW Results if available
    if rinp.dhw_calculate and dhw_res_before and dhw_res_after:
        res.dhw_included = True

        res.q_tw_before = round(dhw_res_before.q_tv, 0)
        res.q_tw_dis_ls_before = round(dhw_res_before.q_w_dis_ls, 0)
        res.w_tw_pump_before = round(dhw_res_before.w_w_pump, 0)
        res.q_tw_gen_ls_before = round(dhw_res_before.q_w_gen_ls, 0)

        res.q_tw_after = round(dhw_res_after.q_tv, 0)
        res.q_tw_dis_ls_after = round(dhw_res_after.q_w_dis_ls, 0)
        res.w_tw_pump_after = round(dhw_res_after.w_w_pump, 0)
        res.q_tw_gen_ls_after = round(dhw_res_after.q_w_gen_ls, 0)

        dhw_sav = res.q_tw_before - res.q_tw_after
        dhw_pct = (dhw_sav / res.q_tw_before * 100) if res.q_tw_before > 0 else 0
        res.dhw_savings_kwh = round(dhw_sav, 0)
        res.dhw_savings_pct = round(dhw_pct, 1)

    return res
