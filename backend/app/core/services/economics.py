"""
Chapter 8: Economics and Return on Investment (Návratnosť a Ziskovosť).
"""

from app.core.models.economics import EconomicsInput, EconomicsResult, CashflowYear


def calculate_economics(data: EconomicsInput) -> EconomicsResult:
    """
    Calculate PB, NPV, NPVQ, and cumulative Cashflow for the given inputs.
    """
    # ─── 1. Basic savings & rates ───────────────────────
    # Financial savings in Year 1
    savings_v1 = data.energy_savings_kwh * data.energy_price
    
    # Real interest rate: r = (nr - b) / (1 + b)
    r = (data.nominal_interest_rate - data.inflation_rate) / (1 + data.inflation_rate)
    
    # Simple Payback: PB = I / B
    # Rounding to 1 decimal place, cap at 999 if savings are 0 to avoid Infinity
    if savings_v1 > 0:
        pb = data.investment_cost / savings_v1
    else:
        pb = 999.0
        
    # ─── 2. Net Present Value (NPV) & NPVQ ──────────────
    # NPV formula: Sum of B*(1+b)^t / (1+nr)^t over lifetime n, minus Investment I
    # Since r = (nr - b)/(1+b), mathematically: Future Value Discounted back.
    # The script specifies: NPV = sum(B_t / (1+r)^t) - I ... if B is constant.
    # We will use the direct year-by-year summation to explicitly handle inflation over time.
    npv_sum = 0.0
    for t in range(1, data.economic_lifetime + 1):
        # The document simplifies: NPV = B * [ ((1+r)^n - 1) / (r * (1+r)^n) ] - I
        # Let's use the explicit generic discount calculation to be robust.
        # Cashflow for year t (only energy savings, not loan)
        # Note: If we use real interest rate 'r', we discount the constant Year 1 savings base.
        # Savings base B = savings_v1
        discount_factor = (1 + r) ** t
        npv_sum += savings_v1 / discount_factor
        
    npv = npv_sum - data.investment_cost
    npvq = npv / data.investment_cost if data.investment_cost > 0 else 0.0

    # ─── 3. Cashflow (Hotovostný tok) ───────────────────
    # Financing
    loan_amount = data.investment_cost * data.loan_share
    own_capital = data.investment_cost - loan_amount
    
    # Annuity Factor for loan (Faktor anuity)
    # PMT = P * [ i(1+i)^n ] / [ (1+i)^n - 1 ]
    # where i = nominal_interest_rate, n = loan_duration
    if data.nominal_interest_rate > 0 and data.loan_duration > 0:
        i = data.nominal_interest_rate
        n = data.loan_duration
        annuity_factor = (i * (1 + i)**n) / ((1 + i)**n - 1)
        annual_debt_service = loan_amount * annuity_factor
    elif data.loan_duration > 0:
        annual_debt_service = loan_amount / data.loan_duration
    else:
        annual_debt_service = 0.0

    # Generate Yearly Array
    cashflow_array = []
    payback_year = None
    
    # Year 0
    cumulative_cf = -own_capital
    cashflow_array.append(CashflowYear(
        year=0,
        savings_indexed=0.0,
        debt_service=0.0,
        additional_investment=data.investment_cost, # Showing total investment in yr 0 config
        net_cashflow=-own_capital,
        cumulative_cashflow=cumulative_cf
    ))

    # Years 1 to economic_lifetime
    current_savings = savings_v1
    for t in range(1, data.economic_lifetime + 1):
        if t > 1:
            current_savings = current_savings * (1 + data.inflation_rate)
            
        debt_service = annual_debt_service if t <= data.loan_duration else 0.0
        
        # Check additional investments
        # In the text, dodatočná investícia in Year 11 is evaluated at future value.
        # User input is usually provided in today's EUR, so we need to inflate it.
        add_inv_base = data.additional_investments_schedule.get(str(t), 0.0)
        add_inv = add_inv_base * ((1 + data.inflation_rate) ** t) if add_inv_base > 0 else 0.0
        
        net_cf = current_savings - debt_service - add_inv
        cumulative_cf += net_cf
        
        # Determine payback year logic
        if cumulative_cf > 0 and payback_year is None:
            payback_year = t
            
        cashflow_array.append(CashflowYear(
            year=t,
            savings_indexed=round(current_savings, 0),
            debt_service=round(debt_service, 0),
            additional_investment=round(add_inv, 0),
            net_cashflow=round(net_cf, 0),
            cumulative_cashflow=round(cumulative_cf, 0)
        ))

    return EconomicsResult(
        financial_savings=round(savings_v1, 0),
        real_interest_rate=round(r * 100, 2),
        simple_payback=round(pb, 1),
        net_present_value=round(npv, 0),
        npv_quotient=round(npvq, 2),
        cashflow_series=cashflow_array,
        payback_year_cashflow=payback_year
    )
