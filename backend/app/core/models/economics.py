"""
Chapter 8: Economic Calculations and Return on Investment (Economics)
Contains models for Simple Payback, NPV, NPVQ, and Cashflow.
"""

from pydantic import BaseModel, Field

class CashflowYear(BaseModel):
    year: int = Field(description="Rok (0 = investícia)")
    savings_indexed: float = Field(default=0.0, description="Finančná úspora s úročením o infláciu (€)")
    debt_service: float = Field(default=0.0, description="Dlhová služba (splátka úveru, €)")
    additional_investment: float = Field(default=0.0, description="Dodatočná investícia (€)")
    net_cashflow: float = Field(description="Čistý cashflow v danom roku (€)")
    cumulative_cashflow: float = Field(description="Kumulovaný cashflow do daného roku (€)")


class EconomicsInput(BaseModel):
    """Vstupné dáta pre ekonomické zhodnotenie úsporných opatrení (Kapitola 8)."""
    investment_cost: float = Field(..., description="Celkové investičné náklady (I v €)")
    energy_savings_kwh: float = Field(..., description="Ročná úspora energie (S v kWh/rok)")
    energy_price: float = Field(..., description="Súčasná cena energie (E v €/kWh)")
    
    economic_lifetime: int = Field(default=30, description="Ekonomická životnosť (n v rokoch)")
    nominal_interest_rate: float = Field(default=0.05, description="Nominálna úroková miera (nr, napr. 0.05 pre 5%)")
    inflation_rate: float = Field(default=0.02, description="Miera inflácie (b, napr. 0.02 pre 2%)")
    
    # Financing parameters
    loan_share: float = Field(default=0.8, description="Podiel úveru z investície (napr. 0.8 pre 80%)")
    loan_duration: int = Field(default=20, description="Dĺžka splácania úveru (v rokoch)")
    
    # Optional additional investments (e.g., pump replacement after 10 years)
    additional_investments_schedule: dict[str, float] = Field(
        default_factory=dict, 
        description="Dodatočné investície v špecifických rokoch. Formát: {'11': 2000.0}"
    )


class EconomicsResult(BaseModel):
    """Výsledky hospodárnosti (PB, NPV, NPVQ, Cashflow)."""
    financial_savings: float = Field(description="Ročná finančná úspora v 1. roku (B v €/rok)")
    real_interest_rate: float = Field(description="Reálna úroková miera (r v %)")
    
    # Key Metrics
    simple_payback: float = Field(description="Hrubá návratnosť (PB v rokoch)")
    net_present_value: float = Field(description="Čistá súčasná hodnota (NPV v €)")
    npv_quotient: float = Field(description="Koeficient čistej súčasnej hodnoty (NPVQ)")
    
    # Cashflow Chart Data
    cashflow_series: list[CashflowYear] = Field(description="Ročný vývoj hotovostného toku")
    payback_year_cashflow: int | None = Field(description="Rok, v ktorom sa kumulovaný cashflow stane kladným (None ak sa nevráti do konca životnosti)")
