"""Core calculation logic for Keren Hishtalmut vs Personal Investment comparison."""

from typing import Optional
import pandas as pd
import numpy as np

from .models import (
    InvestmentInputs,
    YearlyResult,
    ComparisonResult,
    SensitivityPoint,
    RequiredReturnResult,
)


def calculate_keren_fv(
    principal: float, net_return: float, years: int, monthly_contribution: float = 0
) -> float:
    """
    Calculate future value in Keren Hishtalmut (tax-exempt) with monthly contributions.

    Formula for lump sum: FV = P * (1 + r)^T
    Formula for annuity: FV = PMT * [((1 + r_monthly)^months - 1) / r_monthly]

    Args:
        principal: Initial investment amount
        net_return: Net annual return after management fees (e.g., 0.0762 for 7.62%)
        years: Number of years
        monthly_contribution: Monthly contribution amount (default 0)

    Returns:
        Future value at the end of the period
    """
    # Lump sum growth
    fv_lump = principal * (1 + net_return) ** years
    
    # Monthly contributions growth
    if monthly_contribution > 0 and years > 0:
        monthly_rate = (1 + net_return) ** (1/12) - 1
        months = years * 12
        # Future value of annuity formula
        fv_annuity = monthly_contribution * (((1 + monthly_rate) ** months - 1) / monthly_rate)
    else:
        fv_annuity = 0
    
    return fv_lump + fv_annuity


def calculate_personal_fv_pretax(
    principal: float, return_rate: float, years: int, monthly_contribution: float = 0
) -> float:
    """
    Calculate future value in personal account before tax with monthly contributions.

    Formula for lump sum: FV_pre = P * (1 + r)^T
    Formula for annuity: FV = PMT * [((1 + r_monthly)^months - 1) / r_monthly]

    Args:
        principal: Initial investment amount
        return_rate: Annual return rate (e.g., 0.10 for 10%)
        years: Number of years
        monthly_contribution: Monthly contribution amount (default 0)

    Returns:
        Future value before capital gains tax
    """
    # Lump sum growth
    fv_lump = principal * (1 + return_rate) ** years
    
    # Monthly contributions growth
    if monthly_contribution > 0 and years > 0:
        monthly_rate = (1 + return_rate) ** (1/12) - 1
        months = years * 12
        # Future value of annuity formula
        fv_annuity = monthly_contribution * (((1 + monthly_rate) ** months - 1) / monthly_rate)
    else:
        fv_annuity = 0
    
    return fv_lump + fv_annuity


def calculate_personal_fv_aftertax(
    principal: float,
    return_rate: float,
    years: int,
    tax_rate: float,
    monthly_contribution: float = 0,
) -> float:
    """
    Calculate future value in personal account after capital gains tax at sale.

    For lump sum: FV_after = P * [τ + (1 - τ) * (1 + r)^T]
    For contributions: Tax applies to each contribution's gain separately

    Args:
        principal: Initial investment amount
        return_rate: Annual return rate (e.g., 0.10 for 10%)
        years: Number of years
        tax_rate: Capital gains tax rate (e.g., 0.25 for 25%)
        monthly_contribution: Monthly contribution amount (default 0)

    Returns:
        Future value after capital gains tax
    """
    # Lump sum after tax
    if principal > 0:
        fv_lump_pretax = principal * (1 + return_rate) ** years
        gain_lump = fv_lump_pretax - principal
        fv_lump = principal + gain_lump * (1 - tax_rate)
    else:
        fv_lump = 0
    
    # Monthly contributions after tax
    # Each contribution grows for a different period and has its own gain
    if monthly_contribution > 0 and years > 0:
        monthly_rate = (1 + return_rate) ** (1/12) - 1
        fv_contributions = 0
        
        for month in range(1, years * 12 + 1):
            # Months remaining for this contribution to grow
            months_growth = years * 12 - month + 1
            contribution_fv = monthly_contribution * (1 + monthly_rate) ** months_growth
            contribution_gain = contribution_fv - monthly_contribution
            contribution_after_tax = monthly_contribution + contribution_gain * (1 - tax_rate)
            fv_contributions += contribution_after_tax
    else:
        fv_contributions = 0
    
    return fv_lump + fv_contributions


def find_breakeven_year(
    principal: float,
    keren_net_return: float,
    personal_return: float,
    tax_rate: float,
    monthly_contribution: float = 0,
    max_years: int = 100,
    keren_lockup_years: int = 15,
) -> Optional[int]:
    """
    Find the first year where personal investment beats Keren Hishtalmut.
    
    Personal investment scenario: Keep money in Keren until lockup, then withdraw
    and invest personally from that point forward.

    Args:
        principal: Initial investment amount
        keren_net_return: Net annual return for Keren after fees
        personal_return: Annual return for personal investment
        tax_rate: Capital gains tax rate
        monthly_contribution: Monthly contribution amount
        max_years: Maximum years to search
        keren_lockup_years: Years before Keren can be withdrawn (default 15)

    Returns:
        First year where personal FV (after tax) >= Keren FV, or None if never
    """
    # Get Keren value at lockup (what you'd withdraw)
    keren_at_lockup = calculate_keren_fv(
        principal, keren_net_return, keren_lockup_years, monthly_contribution
    )
    
    # Start checking from year after lockup
    for year in range(keren_lockup_years + 1, max_years + 1):
        # Option A: Stay in Keren
        keren_fv = calculate_keren_fv(principal, keren_net_return, year, monthly_contribution)
        
        # Option B: Withdrew at lockup, invested personally since then
        years_since_lockup = year - keren_lockup_years
        
        # Withdrawn lump sum growth
        lump_sum_pretax = calculate_personal_fv_pretax(
            keren_at_lockup, personal_return, years_since_lockup, 0
        )
        lump_sum_gain = lump_sum_pretax - keren_at_lockup
        lump_sum_aftertax = keren_at_lockup + lump_sum_gain * (1 - tax_rate)
        
        # New contributions since lockup
        contributions_aftertax = calculate_personal_fv_aftertax(
            0, personal_return, years_since_lockup, tax_rate, monthly_contribution
        )
        
        personal_fv = lump_sum_aftertax + contributions_aftertax
        
        if personal_fv >= keren_fv:
            return year
    
    return None


def calculate_required_return(
    keren_net_return: float, tax_rate: float, years: int
) -> float:
    """
    Calculate the personal return required to match Keren Hishtalmut for a given horizon.

    From: (1 + r_KH)^T = τ + (1 - τ) * (1 + r_B)^T
    Solving: 1 + r_B = ((1 + r_KH)^T - τ) / (1 - τ))^(1/T)

    Args:
        keren_net_return: Net annual return for Keren after fees
        tax_rate: Capital gains tax rate
        years: Investment horizon in years

    Returns:
        Required annual return for personal investment to break even
    """
    keren_fv_factor = (1 + keren_net_return) ** years
    numerator = keren_fv_factor - tax_rate
    denominator = 1 - tax_rate

    if denominator <= 0 or numerator <= 0:
        return float("inf")

    return (numerator / denominator) ** (1 / years) - 1


def run_comparison(inputs: InvestmentInputs) -> ComparisonResult:
    """
    Run a complete comparison between Keren Hishtalmut and personal investment.
    
    Critical: During lockup period, money MUST stay in Keren. Personal investment
    option means withdrawing at lockup end and then investing personally.

    Args:
        inputs: All input parameters for the comparison

    Returns:
        ComparisonResult with yearly data and summary metrics
    """
    keren_net_return = inputs.get_keren_net_return()
    personal_effective_return = inputs.get_personal_effective_return()
    lockup = inputs.keren_lockup_years

    yearly_results: list[YearlyResult] = []
    breakeven_year: Optional[int] = None
    
    # Calculate Keren value at lockup (for personal investment withdrawal scenario)
    keren_at_lockup = calculate_keren_fv(
        inputs.principal, keren_net_return, lockup, inputs.monthly_contribution
    )

    for year in range(1, inputs.horizon_years + 1):
        # Option A: Keep in Keren for all years
        keren_fv = calculate_keren_fv(
            inputs.principal, keren_net_return, year, inputs.monthly_contribution
        )
        
        # Option B: Personal investment scenario
        if year <= lockup:
            # Before/at lockup: Money is in Keren (no choice)
            # So personal option = same as Keren during lockup
            personal_fv_pretax = keren_fv
            personal_fv_aftertax = keren_fv  # No tax yet, still in Keren
        else:
            # After lockup: Withdrew Keren balance at lockup, now investing personally
            years_since_lockup = year - lockup
            
            # The withdrawn lump sum grows at personal rate
            lump_sum_pretax = calculate_personal_fv_pretax(
                keren_at_lockup, personal_effective_return, years_since_lockup, 0
            )
            
            # New monthly contributions since lockup grow at personal rate
            contributions_pretax = calculate_personal_fv_pretax(
                0, personal_effective_return, years_since_lockup, inputs.monthly_contribution
            )
            
            personal_fv_pretax = lump_sum_pretax + contributions_pretax
            
            # Calculate tax on gains
            # Lump sum: gain is (current_value - withdrawn_amount)
            lump_sum_gain = lump_sum_pretax - keren_at_lockup
            lump_sum_aftertax = keren_at_lockup + lump_sum_gain * (1 - inputs.capital_gains_tax)
            
            # Contributions: calculate tax on each contribution's gain
            contributions_aftertax = calculate_personal_fv_aftertax(
                0, personal_effective_return, years_since_lockup, 
                inputs.capital_gains_tax, inputs.monthly_contribution
            )
            
            personal_fv_aftertax = lump_sum_aftertax + contributions_aftertax

        # Keren wins if value is higher
        keren_wins = keren_fv > personal_fv_aftertax

        yearly_results.append(
            YearlyResult(
                year=year,
                keren_fv=keren_fv,
                personal_fv_pretax=personal_fv_pretax,
                personal_fv_aftertax=personal_fv_aftertax,
                keren_wins=keren_wins,
            )
        )

        # Track first breakeven year (after lockup period)
        if (
            breakeven_year is None
            and not keren_wins
            and year > lockup
        ):
            breakeven_year = year

    return ComparisonResult(
        inputs=inputs,
        yearly_results=yearly_results,
        breakeven_year=breakeven_year,
        keren_net_return=keren_net_return,
        personal_effective_return=personal_effective_return,
    )


def generate_comparison_dataframe(result: ComparisonResult) -> pd.DataFrame:
    """
    Generate a pandas DataFrame from comparison results.

    Args:
        result: ComparisonResult from run_comparison

    Returns:
        DataFrame with yearly comparison data
    """
    data = []
    for yr in result.yearly_results:
        data.append(
            {
                "Year": yr.year,
                "Keren Hishtalmut": yr.keren_fv,
                "Personal (Before Tax)": yr.personal_fv_pretax,
                "Personal (After Tax)": yr.personal_fv_aftertax,
                "Difference": yr.difference,
                "Difference %": yr.difference_pct,
                "Winner": "Keren" if yr.keren_wins else "Personal",
            }
        )
    return pd.DataFrame(data)


def generate_sensitivity_matrix(
    principal: float,
    keren_net_return: float,
    personal_returns: list[float],
    tax_rates: list[float],
    monthly_contribution: float = 0,
    max_years: int = 50,
    keren_lockup_years: int = 15,
) -> pd.DataFrame:
    """
    Generate a sensitivity matrix showing breakeven years for different
    combinations of personal return and tax rate.

    Args:
        principal: Initial investment amount
        keren_net_return: Net annual return for Keren
        personal_returns: List of personal return rates to test
        tax_rates: List of tax rates to test
        max_years: Maximum years to search for breakeven

    Returns:
        DataFrame with personal returns as rows and tax rates as columns
    """
    data = []
    for pr in personal_returns:
        row = {"Personal Return": f"{pr*100:.1f}%"}
        for tr in tax_rates:
            be_year = find_breakeven_year(
                principal, keren_net_return, pr, tr, monthly_contribution, max_years, keren_lockup_years
            )
            row[f"Tax {tr*100:.0f}%"] = be_year if be_year else ">50"
        data.append(row)

    df = pd.DataFrame(data)
    df.set_index("Personal Return", inplace=True)
    return df


def generate_required_return_table(
    keren_net_return: float,
    tax_rate: float,
    horizons: list[int],
) -> list[RequiredReturnResult]:
    """
    Generate a table showing required personal return for different horizons.

    Args:
        keren_net_return: Net annual return for Keren
        tax_rate: Capital gains tax rate
        horizons: List of investment horizons in years

    Returns:
        List of RequiredReturnResult for each horizon
    """
    results = []
    for years in horizons:
        required = calculate_required_return(keren_net_return, tax_rate, years)
        results.append(
            RequiredReturnResult(
                horizon_years=years,
                keren_net_return=keren_net_return,
                tax_rate=tax_rate,
                required_personal_return=required,
                alpha_required=required - keren_net_return,
            )
        )
    return results


def generate_required_return_dataframe(
    keren_net_return: float,
    tax_rate: float,
    horizons: list[int],
) -> pd.DataFrame:
    """
    Generate a DataFrame showing required personal return for different horizons.

    Args:
        keren_net_return: Net annual return for Keren
        tax_rate: Capital gains tax rate
        horizons: List of investment horizons in years

    Returns:
        DataFrame with horizon and required returns
    """
    results = generate_required_return_table(keren_net_return, tax_rate, horizons)
    data = []
    for r in results:
        data.append(
            {
                "Horizon (Years)": r.horizon_years,
                "Keren Net Return": f"{r.keren_net_return*100:.2f}%",
                "Required Personal Return": f"{r.required_personal_return*100:.2f}%",
                "Alpha Required": f"{r.alpha_required*100:.2f}%",
            }
        )
    return pd.DataFrame(data)
