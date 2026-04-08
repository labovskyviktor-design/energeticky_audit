"""
DHW (Domestic Hot Water) service for Chapter 4.
Calculates energy demand for hot water preparation per STN EN 15316-3.
"""

from app.core.models.heating_system import FuelType
from app.core.models.dhw import DHWInput, DHWResult
from app.core.services.heating_tables import get_fuel_efficiency
from app.core.models.calc_constants import resolve_constants, get_deviations


def calculate_dhw_demand(inp: DHWInput) -> DHWResult:
    """
    Calculate seasonal DHW energy demand.
    Q_TV = Q_W + Q_W,d + Q_W,s + Q_W,g
    """
    
    # 1. Net Heat Demand Q_W (Simplified method)
    # Ref: Eq 4.1: Q_W = 20 * Ab
    q_w = 20.0 * inp.ab
    
    # 2. Distribution Losses Q_W,d
    # Ref: Eq 4.2: Q_W,d = Q_W,d,i + Q_W,d,c
    # 2a. Pipe Heat Loss from segments (Circulation + Supply)
    # Ref: Eq 4.3
    q_w_dis_ls = 0.0
    # Assuming operation 24h/365d = 8760h for circulation
    # For supply pipes (non-circ), operation time is smaller?
    # PDF simplified example treats all segments with 8760h if circulation exists?
    # "Tepelná strata úseku potrubia s cirkuláciou TV"
    # Let's assume input pipes are those with circulation or constant heat load.
    
    hours_year = 365 * 24
    
    for pipe in inp.pipes:
        # Ui * L * (theta_m - theta_amb) * t
        # Ui approx Psi? Yes in Ch3 we used Psi as linear loss coeff.
        delta_t = pipe.water_temp - pipe.ambient_temp
        if delta_t > 0:
            q_loss = (pipe.psi * pipe.length * delta_t * hours_year) / 1000.0
            q_w_dis_ls += q_loss

    # 2b. Stagnation Loss (dead legs)
    # Ref: Eq 4.4
    # Simplified estimation if not detailed:
    # In PDF example: 3577 kWh for dead legs.
    # We need volume of dead legs.
    # If user doesn't provide specific dead legs, we can't calc easily.
    # Let's assume 0 if not provided, or add a field for "dead leg volume".
    # For now, 0 unless we add it to input.
    q_w_dis_stag = 0.0 
    
    # 2c. Recoverable Heat from Distribution
    # "Pretože táto tepelná strata prispieva k vykurovaniu bytov..."
    # Only from pipes in heated spaces.
    # Let's assume pipes with ambient_temp >= 15 are in heated spaces?
    # Or just ratio of heating days.
    
    # Calculate recoverable portion from total distribution loss
    # If the pipe is in a heated zone (e.g. ambient > 15?)
    q_dis_rec_potential = 0.0
    for pipe in inp.pipes:
         if pipe.ambient_temp >= 15.0: # Approximation for heated zone
             delta_t = pipe.water_temp - pipe.ambient_temp
             if delta_t > 0:
                 q_dis_rec_potential += (pipe.psi * pipe.length * delta_t * hours_year) / 1000.0

    # Recoverable = Potential * (HeatingDays / 365)
    # PDF example logic: "Spätne získateľná tepelná strata... sa vypočíta takto: ... * 212/365"
    q_rec = q_dis_rec_potential * (inp.heating_days / 365.0)

    # 3. Auxiliary Energy (Pump)
    # Ref: Eq 4.6
    w_w_pump = 0.0
    if inp.pump.has_circulation:
        # 365 * fpump * Ppump / 1000
        w_w_pump = (365.0 * inp.pump.daily_hours * inp.pump.power) / 1000.0
        
    # Pump energy is strictly electrical, but part converts to heat in water?
    # PDF doesn't subtract it from Q_gen. It adds to Total Energy?
    # Eq 4.8: Q_TV = Q_W + Q_W,d + W_W,d,pump + Q_W,s + Q_W,g
    # So it's added as energy demand.
    
    # 4. Storage Losses Q_W,s
    # Ref: Eq 4.7
    q_w_sto_ls = 0.0
    if inp.storage.has_storage:
        # Qs_b * 365 * ...
        # If Qs_b (standby loss) is given in kWh/day for a temp diff.
        # Usually given for 60-20=40K diff?
        # PDF says: Q = Qs,b * (theta_s - theta_amb) / theta_test_diff
        # We assume input standby_loss is the actual loss at operating conditions?
        # Or standard test? "Pohotovostná strata s prispôsobením aktuálneho rozdielu"
        # Let's assume the user inputs the CORRECTED loss or standard. 
        # For simplicity, if user gives kWh/24h, we multiply by 365.
        # Ideally we'd scale it by temp difference if input was standard.
        # Let's stick to simple: Loss/day * 365.
        q_w_sto_ls = inp.storage.standby_loss * 365.0

    # 5. Generation Losses Q_W,g
    # Ref: Eq 4.8 context: "zohľadnením účinnosti zariadenia"
    # Q_W,g = (1 - eta)/eta * Q_output?
    # Q_output_req = Q_W + DistributionLoss + StorageLoss
    # No, usually: Q_gen_input = Q_out / eta
    # Q_gen_ls = Q_gen_input - Q_out = (Q_out / eta) - Q_out = Q_out * (1/eta - 1)
    
    q_out_req = q_w + q_w_dis_ls + q_w_dis_stag + q_w_sto_ls
    
    eta = 1.0
    if not inp.generation.is_external:
        if inp.generation.efficiency_override:
            eta = inp.generation.efficiency_override
        else:
            try:
                eta = get_fuel_efficiency(inp.generation.fuel_type)
            except ValueError:
                eta = 0.90
        
        if eta <= 0: eta = 0.90
            
    # If external, losses are 0 (calculated elsewhere or ignored for building boundary)
    q_w_gen_ls = 0.0
    if not inp.generation.is_external:
         q_w_gen_ls = q_out_req * ((1.0 - eta) / eta)

    # Total Q_TV
    # Eq 4.8: Q_TV = Q_W + Q_W,d,ls + W_pump + Q_W,s + Q_W,g
    q_tv = q_w + q_w_dis_ls + q_w_dis_stag + w_w_pump + q_w_sto_ls + q_w_gen_ls
    
    # Specific
    q_tv_m = q_tv / inp.ab if inp.ab > 0 else 0.0
    
    resolved = resolve_constants(inp.overrides)

    return DHWResult(
        q_w=round(q_w, 0),
        q_w_dis_ls=round(q_w_dis_ls, 0),
        q_w_dis_stag=round(q_w_dis_stag, 0),
        q_w_sto_ls=round(q_w_sto_ls, 0),
        w_w_pump=round(w_w_pump, 0),
        q_w_gen_ls=round(q_w_gen_ls, 0),
        q_tv=round(q_tv, 0),
        q_tv_m=round(q_tv_m, 1),
        q_rec=round(q_rec, 0),
        resolved_constants=resolved,
        deviations=get_deviations(resolved),
    )
