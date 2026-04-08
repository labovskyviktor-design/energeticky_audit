"""
Renovation models for Chapter 6 — Návrh úsporných opatrení.

Defines the catalog of renovation measures (Tab. 6.1),
insulated pipe Ψ values (Tab. 6.2), and input/result models
for before/after comparison.
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# ── Tab. 6.1 — Katalóg opatrení ──────────────────────────────

class MeasureCategory(str, Enum):
    """Kategória opatrenia."""
    ENVELOPE = "envelope"
    EMISSION = "emission"
    DISTRIBUTION = "distribution"
    PUMP = "pump"
    GENERATION = "generation"
    REGULATION = "regulation"


class MeasureID(str, Enum):
    """Identifikátor konkrétneho opatrenia z Tab. 6.1."""
    # Envelope (hlavné opatrenia)
    ENVELOPE_INSULATION = "envelope_insulation"
    WINDOW_REPLACEMENT = "window_replacement"
    # System (Ch3 opatrenia)
    HYDRAULIC_BALANCING = "hydraulic_balancing"
    THERMOSTATIC_VALVES = "thermostatic_valves"
    PIPE_INSULATION = "pipe_insulation"
    TEMP_GRADIENT_REDUCTION = "temp_gradient_reduction"
    NEW_PUMP = "new_pump"
    NEW_BOILER = "new_boiler"
    NIGHT_SETBACK = "night_setback"
    AUTO_REGULATION = "auto_regulation"
    # DHW (Ch4 opatrenia)
    DHW_PIPE_INSULATION = "dhw_pipe_insulation"
    DHW_WATER_SAVING = "dhw_water_saving"
    DHW_NEW_SOURCE = "dhw_new_source"


# ── Tab. 6.2 — Ψ po zaizolovaní ──────────────────────────────

# Insulated pipe Ψ values (40mm insulation, λ=0.036 W/(m·K))
PSI_INSULATED = {
    65: 0.296,
    50: 0.243,
    40: 0.208,
    32: 0.189,
    25: 0.170,  # extrapolated
    20: 0.155,  # extrapolated
}


# ── Measure definition catalog ────────────────────────────────

class MeasureDefinition(BaseModel):
    """Definícia jedného opatrenia z katalógu."""
    id: MeasureID
    name: str
    name_sk: str
    category: MeasureCategory
    description: str = ""
    affected_param: str = Field(description="Ovplyvnený parameter")


MEASURES_CATALOG: list[MeasureDefinition] = [
    MeasureDefinition(
        id=MeasureID.ENVELOPE_INSULATION,
        name="Envelope Insulation (ETICS)",
        name_sk="Zateplenie obvodového plášťa (ETICS)",
        category=MeasureCategory.ENVELOPE,
        description="Dodatočné zateplenie stien, strechy, podlahy. Znižuje U-hodnotu konštrukcií.",
        affected_param="U (konštrukcie)",
    ),
    MeasureDefinition(
        id=MeasureID.WINDOW_REPLACEMENT,
        name="Window & Door Replacement",
        name_sk="Výmena okien a dverí",
        category=MeasureCategory.ENVELOPE,
        description="Výmena starých okien/dverí za nové s lepšou U-hodnotou a tesnosťou.",
        affected_param="U (okná, dvere)",
    ),
    MeasureDefinition(
        id=MeasureID.HYDRAULIC_BALANCING,
        name="Hydraulic Balancing",
        name_sk="Hydraulické vyregulovanie",
        category=MeasureCategory.EMISSION,
        description="Zmena prednastavenia termostatických ventilov.",
        affected_param="Δθ_hyd",
    ),
    MeasureDefinition(
        id=MeasureID.THERMOSTATIC_VALVES,
        name="Thermostatic Valves Replacement",
        name_sk="Výmena/kontrola termostatických ventilov",
        category=MeasureCategory.REGULATION,
        description="P-regulátor (termostatická hlavica) — Δθ_ctr klesne z 2.0 na 0.7 K.",
        affected_param="Δθ_ctr",
    ),
    MeasureDefinition(
        id=MeasureID.PIPE_INSULATION,
        name="Pipe Insulation",
        name_sk="Izolácia rozvodných potrubí",
        category=MeasureCategory.DISTRIBUTION,
        description="Nová izolácia 40mm, λ=0.036 W/(m·K). Ψ klesne podľa Tab. 6.2.",
        affected_param="Ψ (pipe)",
    ),
    MeasureDefinition(
        id=MeasureID.TEMP_GRADIENT_REDUCTION,
        name="Temperature Gradient Reduction",
        name_sk="Zníženie teplotného spádu",
        category=MeasureCategory.EMISSION,
        description="Napr. z 90/70 na 75/65 °C cez trojcestný ventil.",
        affected_param="θ_s,des / θ_r,des",
    ),
    MeasureDefinition(
        id=MeasureID.NEW_PUMP,
        name="New Pump with VFD",
        name_sk="Nové čerpadlo s frekvenčným meničom",
        category=MeasureCategory.PUMP,
        description="Výmena starého čerpadla za nové s reguláciou.",
        affected_param="P_el,pmp",
    ),
    MeasureDefinition(
        id=MeasureID.NEW_BOILER,
        name="New Boiler / Heat Pump",
        name_sk="Nový kotol / tepelné čerpadlo",
        category=MeasureCategory.GENERATION,
        description="Výmena zdroja tepla za účinnejší.",
        affected_param="η_gen / fuel_type",
    ),
    MeasureDefinition(
        id=MeasureID.NIGHT_SETBACK,
        name="Night Temperature Setback",
        name_sk="Nočný teplotný útlm",
        category=MeasureCategory.REGULATION,
        description="Zníženie teploty počas noci.",
        affected_param="Δθ_im",
    ),
    MeasureDefinition(
        id=MeasureID.AUTO_REGULATION,
        name="Automatic Regulation System",
        name_sk="Automatický regulačný systém",
        category=MeasureCategory.REGULATION,
        description="Nový alebo opravený ekvitermický regulátor.",
        affected_param="Δθ_ctr",
    ),
    MeasureDefinition(
        id=MeasureID.DHW_PIPE_INSULATION,
        name="DHW Pipe Insulation",
        name_sk="Izolácia rozvodov TV",
        category=MeasureCategory.DISTRIBUTION,
        description="Zaizolovanie rozvodov a cirkulácie TV podľa tabuľky hrúbok.",
        affected_param="Ψ (dhw pipes)",
    ),
    MeasureDefinition(
        id=MeasureID.DHW_WATER_SAVING,
        name="Water Saving Fixtures",
        name_sk="Úsporné armatúry (sprchy/batérie)",
        category=MeasureCategory.EMISSION,
        description="Zníženie spotreby vody (V_W) inštaláciou šetričov.",
        affected_param="Q_W,A",
    ),
    MeasureDefinition(
        id=MeasureID.DHW_NEW_SOURCE,
        name="New DHW Heat Source",
        name_sk="Nový zdroj pre prípravu TV",
        category=MeasureCategory.GENERATION,
        description="Výmena zdroja (napr. za tepelné čerpadlo) pre prípravu TV.",
        affected_param="η_gen_dhw",
    ),
]


# ── Input / Output models ─────────────────────────────────────

class SelectedMeasure(BaseModel):
    """Jedno vybrané opatrenie s prípadnými override hodnotami."""
    measure_id: MeasureID
    enabled: bool = True

    # Override values — ak None, použijú sa defaulty
    new_theta_s_des: Optional[float] = Field(
        default=None, description="Nová projektovaná teplota prívodnej vody (°C)",
    )
    new_theta_r_des: Optional[float] = Field(
        default=None, description="Nová projektovaná teplota vratnej vody (°C)",
    )
    new_pump_p_el: Optional[float] = Field(
        default=None, description="Nový príkon čerpadla (W)",
    )
    new_pump_regulation: Optional[str] = Field(
        default=None, description="Regulácia nového čerpadla",
    )
    new_fuel_type: Optional[str] = Field(
        default=None, description="Nový typ paliva/systému",
    )
    new_efficiency: Optional[float] = Field(
        default=None, description="Nová účinnosť zdroja (-)",
    )
    # DHW Override values
    new_dhw_q_wa: Optional[float] = Field(
        default=None, description="Nová merná potreba tepla na TV (kWh/m2.a)"
    )
    new_dhw_fuel_type: Optional[str] = Field(
        default=None, description="Nový typ zdroja pre TV",
    )
    new_dhw_efficiency: Optional[float] = Field(
        default=None, description="Nová účinnosť zdroja pre TV (-)",
    )


class RenovationInput(BaseModel):
    """Vstup pre výpočet obnovy — before state + vybrané opatrenia."""

    # Before state (from Ch3 calculation)
    building_name: str = Field(default="Budova")
    qh: float = Field(description="QH — potreba tepla na vykurovanie (kWh)")
    ab: float = Field(description="Ab — podlahová plocha budovy (m²)")
    vb: float = Field(default=0, description="Vb — obostavaný objem (m³)")
    phi_em_out: float = Field(description="ΦH,em,out — projektovaný tepelný príkon (kW)")

    theta_s_des: float = Field(default=90, description="Pôvodná θs,des (°C)")
    theta_r_des: float = Field(default=70, description="Pôvodná θr,des (°C)")
    theta_e_comb: float = Field(default=3.86, description="θe,comb (°C)")
    theta_int_ini: float = Field(default=20, description="θint,ini (°C)")
    heating_days: int = Field(default=212, description="Počet vykurovacích dní")

    # Building geometry (for pump estimate)
    length_ll: float = Field(default=0)
    width_lw: float = Field(default=0)
    n_levels: int = Field(default=1)
    level_height: float = Field(default=2.8)

    # ═══ ENVELOPE DATA (for QH recalculation) ═══
    # Constructions before renovation [{name, u_value, area, bx}]
    constructions_before: list[dict] = Field(
        default_factory=list,
        description="Konštrukcie pred obnovou [{name, u_value, area, bx}]",
    )
    # Constructions after renovation (new U-values)
    constructions_after: list[dict] = Field(
        default_factory=list,
        description="Konštrukcie po obnove [{name, u_value, area, bx}]",
    )
    # Windows solar data (for gains recalculation)
    windows_solar: list[dict] = Field(
        default_factory=list,
        description="Solárne dáta okien [{orientation, area, ggl, f_shading}]",
    )
    # Ch2 parameters for QH recalculation
    delta_u_before: float = Field(default=0.10, description="ΔU pred obnovou")
    delta_u_after: float = Field(default=0.05, description="ΔU po obnove")
    v_vb_ratio: float = Field(default=0.85)
    n_inf_override: Optional[float] = Field(default=None)
    qi: float = Field(default=5.0)
    eta_gn: float = Field(default=0.95)

    # Current emission system params
    emission_pipe_system: str = Field(default="two_pipe")
    emission_hydraulic_balancing: str = Field(default="static_per_radiator")
    emission_emitter_type: str = Field(default="radiator")
    emission_regulation_type: str = Field(default="p_controller_old")
    emission_radiator_position: str = Field(default="external_wall_normal")
    emission_radiator_temp_drop: str = Field(default="42.5K")

    # Current pipes
    pipes: list[dict] = Field(
        default_factory=list,
        description="Pôvodné rozvody [{dn, psi, length, ambient_temp}]",
    )

    # Current pump
    pump_p_el: Optional[float] = Field(default=None)
    pump_regulation: str = Field(default="no_regulation")
    pump_delta_p_des: float = Field(default=48.6)

    # Current generation
    fuel_type: str = Field(default="heat_exchanger_hw_hw")
    is_external: bool = Field(default=True)
    efficiency_override: Optional[float] = Field(default=None)

    # Recoverable DHW (Heating context)
    q_dhw_recoverable: float = Field(default=0)

    # ═══ DHW CURRENT STATE (Ch4) ═══
    dhw_calculate: bool = Field(default=False, description="Či sa má vôbec riešiť obnova TV")
    qw_req: float = Field(default=0, description="Potreba tepla na prípravu TV (kWh)")
    dhw_q_wa: float = Field(default=20, description="Merná potreba na TV - default (kWh/m2.a)")
    dhw_water_temp: float = Field(default=57.5, description="Priemerná teplota TV v rozvodoch")
    dhw_pipes: list[dict] = Field(default_factory=list, description="Pôvodné rozvody TV [{typ, dn, psi, length, ambient_temp}]")
    dhw_pump_p_el: float = Field(default=0, description="Príkon cirkulačného čerpadla TV (W)")
    dhw_pump_hours: float = Field(default=8760, description="Prevádzkové hodiny čerpadla TV")
    dhw_tank_volume: float = Field(default=0, description="Objem zásobníka TV (l)")
    dhw_tank_loss: float = Field(default=0, description="Merná strata zásobníka TV (W/K)")
    dhw_fuel_type: str = Field(default="heat_exchanger_hw_hw", description="Zdroj tepla pre TV")
    dhw_is_external: bool = Field(default=True, description="Zdroj TV mimo budovy")
    dhw_efficiency_override: Optional[float] = Field(default=None, description="Účinnosť zdroja pre TV")

    # Selected renovation measures
    measures: list[SelectedMeasure] = Field(default_factory=list)


class RenovationComparisonResult(BaseModel):
    """Výsledok porovnania pred/po obnove."""

    # Before
    q_vyk_before: float = Field(description="QVYK pred obnovou (kWh)")
    q_em_ls_before: float = Field(description="Qem,ls pred (kWh)")
    q_dis_ls_before: float = Field(description="QH,dis,ls pred (kWh)")
    w_pump_before: float = Field(description="WH,dis,aux pred (kWh)")
    q_gen_ls_before: float = Field(description="Qg,ls pred (kWh)")

    # After
    q_vyk_after: float = Field(description="QVYK po obnove (kWh)")
    q_em_ls_after: float = Field(description="Qem,ls po (kWh)")
    q_dis_ls_after: float = Field(description="QH,dis,ls po (kWh)")
    w_pump_after: float = Field(description="WH,dis,aux po (kWh)")
    q_gen_ls_after: float = Field(description="Qg,ls po (kWh)")

    # Differences
    savings_kwh: float = Field(description="Úspora (kWh)")
    savings_pct: float = Field(description="Úspora (%)")

    # Applied measures
    applied_measures: list[str] = Field(description="Zoznam aplikovaných opatrení")

    # Metadata
    qh_before: float = Field(description="QH pred obnovou (kWh)")
    qh_after: float = Field(description="QH po obnove (kWh)")
    qh_savings_kwh: float = Field(default=0, description="Úspora QH (kWh)")
    ab: float = Field(description="Ab — podlahová plocha (m²)")
    q_vyk_m_before: float = Field(description="Merná QVYK pred (kWh/(m²·rok))")
    q_vyk_m_after: float = Field(description="Merná QVYK po (kWh/(m²·rok))")

    # ═══ DHW COMPARISON RESULT ═══
    dhw_included: bool = Field(default=False, description="Či bol spustený výpočet pre TV")
    # Before DHW
    q_tw_before: float = Field(default=0, description="Q_TW pred (kWh)")
    q_tw_dis_ls_before: float = Field(default=0, description="Straty distribúcie TV pred")
    w_tw_pump_before: float = Field(default=0, description="Elektrina čerpadlo TV pred")
    q_tw_gen_ls_before: float = Field(default=0, description="Straty výroba TV pred")
    # After DHW
    q_tw_after: float = Field(default=0, description="Q_TW po (kWh)")
    q_tw_dis_ls_after: float = Field(default=0, description="Straty distribúcie TV po")
    w_tw_pump_after: float = Field(default=0, description="Elektrina čerpadlo TV po")
    q_tw_gen_ls_after: float = Field(default=0, description="Straty výroba TV po")
    # Diffs DHW
    dhw_savings_kwh: float = Field(default=0, description="Úspora TV (kWh)")
    dhw_savings_pct: float = Field(default=0, description="Úspora TV (%)")
