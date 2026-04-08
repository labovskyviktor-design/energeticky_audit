
import asyncio
from app.core.models.climate import (
    ClimateData,
    ConstructionHTEntry,
    HeatingDemandInput,
    VentilationData,
    WindowSolarEntry,
    Orientation,
)
from app.core.models.heating_system import (
    HeatingEnergyInput,
    EmissionSystemInput,
    DistributionPipeInput,
    PumpInput,
    GenerationSourceInput,
    EmitterType,
    PipeSystem,
    FuelType,
)
from app.core.models.building import AssessmentLevel
from app.core.services.energy_balance import calculate_heating_demand
from app.core.services.heating_energy import calculate_heating_energy_demand

def test_chapter_2():
    print("\n--- Verifying Chapter 2 (Heating Demand) ---")
    
    # Scenario 1: Basic test case
    input_data = HeatingDemandInput(
        building_name="Test Building",
        ab=100.0,
        vb=300.0,
        constructions=[
            ConstructionHTEntry(name="Wall", u_value=0.25, area=100.0, bx=1.0),
            ConstructionHTEntry(name="Window", u_value=1.0, area=20.0, bx=1.0),
        ],
        delta_u=0.05,
        ventilation=VentilationData(v_vb_ratio=0.85, n_inf_override=0.5),
        qi=5.0,
        windows_solar=[
            WindowSolarEntry(orientation=Orientation.SOUTH, area=10.0, ggl=0.5),
            WindowSolarEntry(orientation=Orientation.NORTH, area=10.0, ggl=0.5),
        ],
        climate=ClimateData(theta_int=20.0, theta_e_m=4.0, heating_days=200, theta_e_des=-11.0),
        eta_gn=0.95,
    )
    
    result = calculate_heating_demand(input_data, AssessmentLevel.U_R1)
    
    print(f"QH: {result.qh} kWh/a")
    print(f"Phi_HL: {result.phi_hl} kW")
    
    # Assertions for sanity check
    assert result.qh > 0, "QH must be positive"
    assert result.phi_hl > 0, "Phi_HL must be positive"
    print("✅ Chapter 2 Basic Test Passed")
    
    return result

def test_chapter_3(ch2_result):
    print("\n--- Verifying Chapter 3 (Heating Energy Demand) ---")
    
    # Scenario 1: Basic test case linked to Ch2
    input_data = HeatingEnergyInput(
        building_name="Test Building",
        qh=ch2_result.qh,
        phi_em_out=ch2_result.phi_hl,  # Linking Phi_HL from Ch2
        ab=100.0,
        theta_e_comb=4.0,
        # Default values for missing fields to avoid validation errors
        theta_int_ini=20.0,
        theta_s_des=90.0,
        theta_r_des=70.0,
        heating_days=200,

        emission=EmissionSystemInput(
            emitter_type=EmitterType.RADIATOR,
            radiator_temp_drop="60K", 
            radiator_position="external_wall_normal",
            regulation="p_controller",
            pipe_system=PipeSystem.TWO_PIPE,
            hydraulic_balancing="static_with_system",
            n_emitters_le_10=False,
            room_automation="none",
            has_cert=True,
            is_one_pipe_renovated=False,
            floor_insulation="minimum",
        ),
        pipes=[
            DistributionPipeInput(name="Pipe 1", dn=20, length=20.0, psi=0.2, ambient_temp=20.0)
        ],
        pump=PumpInput(
            p_el_pmp=50.0,
            regulation="dp_variable",
            is_balanced=True,
            is_new_building=True,
            is_in_heated_zone=True,
            is_insulated=True,
            generator_regulation="standard_otc",
        ),
        generation=GenerationSourceInput(
            fuel_type=FuelType.NATURAL_GAS_CONDENSING,
            is_external=False,
            efficiency_override=None,
        ),
        q_dhw_recoverable=0.0,
    )

    result = calculate_heating_energy_demand(input_data)
    
    print(f"QVYK: {result.q_vyk} kWh/a")
    print(f"Emission System: {result.emission.system_description}")
    print(f"Emission Loss: {result.emission.q_em_ls} kWh/a")
    print(f"Pipe Length: {result.distribution.total_length} m")
    print(f"Distribution Loss: {result.distribution.q_dis_ls} kWh/a")
    print(f"Generation Loss: {result.generation.q_gen_ls} kWh/a")
    
    assert result.q_vyk > result.qh, "QVYK must be greater than QH (losses added)"
    assert result.generation.q_gen_ls > 0, "Generation loss should be > 0 for internal boiler"
    print("✅ Chapter 3 Basic Test Passed")

    # Scenario 2: External Source (OST) -> Generation loss should be 0
    input_data.generation.is_external = True
    result_ext = calculate_heating_energy_demand(input_data)
    print(f"QVYK (External): {result_ext.q_vyk} kWh/a")
    print(f"Generation Loss (External): {result_ext.generation.q_gen_ls} kWh/a")
    assert result_ext.generation.q_gen_ls == 0, "Generation loss must be 0 for external source"
    print("✅ Chapter 3 External Source Test Passed")

    # Scenario 3: Efficiency Override
    input_data.generation.is_external = False
    input_data.generation.efficiency_override = 0.50 # 50% efficiency
    result_eff = calculate_heating_energy_demand(input_data)
    print(f"QVYK (50% Eff): {result_eff.q_vyk} kWh/a")
    print(f"Generation Loss (50% Eff): {result_eff.generation.q_gen_ls} kWh/a")
    # Note: Logic in service: if efficiency_override is set, it uses it.
    assert result_eff.generation.q_gen_ls > result.generation.q_gen_ls, "Lower efficiency should mean higher loss"
    print("✅ Chapter 3 Efficiency Override Test Passed")

if __name__ == "__main__":
    try:
        ch2_res = test_chapter_2()
        test_chapter_3(ch2_res)
        print("\n🎉 All verifications passed!")
    except Exception as e:
        print(f"\n❌ Verification failed: {e}")
        import traceback
        traceback.print_exc()
