"""Data models for Keren Hishtalmut vs Personal Investment comparison."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class InvestmentInputs:
    """Input parameters for the investment comparison."""

    principal: float  # Initial investment amount in ILS
    monthly_contribution: float  # Monthly contribution amount in ILS (e.g., 1571)
    keren_gross_return: float  # Expected annual return for Keren (e.g., 0.08 for 8%)
    keren_mgmt_fee: float  # Annual management fee (e.g., 0.0035 for 0.35%)
    keren_return_is_net: bool  # True if keren_gross_return is already net of fees
    personal_return: float  # Expected annual return for personal investment (e.g., 0.10 for 10%)
    capital_gains_tax: float  # Capital gains tax rate (e.g., 0.25 for 25%)
    annual_tax_drag: float  # Annual tax drag from dividends/rebalancing (e.g., 0.003 for 0.3%)
    include_tax_drag: bool  # Whether to include tax drag in calculations
    horizon_years: int  # Investment time horizon in years
    keren_lockup_years: int  # Years before Keren can be withdrawn (typically 15)

    def get_keren_net_return(self) -> float:
        """Calculate the net return for Keren Hishtalmut after management fees."""
        if self.keren_return_is_net:
            return self.keren_gross_return
        # Net return = (1 + gross) * (1 - fee) - 1
        return (1 + self.keren_gross_return) * (1 - self.keren_mgmt_fee) - 1

    def get_personal_effective_return(self) -> float:
        """Get the effective personal return accounting for tax drag if enabled."""
        if self.include_tax_drag:
            # Approximate tax drag as a reduction in annual return
            return self.personal_return - self.annual_tax_drag
        return self.personal_return


@dataclass
class YearlyResult:
    """Results for a single year in the comparison."""

    year: int
    keren_fv: float  # Future value in Keren Hishtalmut
    personal_fv_pretax: float  # Future value in personal account before tax
    personal_fv_aftertax: float  # Future value in personal account after capital gains tax
    keren_wins: bool  # True if Keren value is higher

    @property
    def difference(self) -> float:
        """Difference between personal (after tax) and Keren values."""
        return self.personal_fv_aftertax - self.keren_fv

    @property
    def difference_pct(self) -> float:
        """Percentage difference relative to Keren value."""
        if self.keren_fv == 0:
            return 0.0
        return (self.personal_fv_aftertax - self.keren_fv) / self.keren_fv * 100


@dataclass
class ComparisonResult:
    """Complete results of the investment comparison."""

    inputs: InvestmentInputs
    yearly_results: list[YearlyResult]
    breakeven_year: Optional[int]  # First year where personal beats Keren (None if never)
    keren_net_return: float  # Calculated net return for Keren
    personal_effective_return: float  # Effective return for personal (with tax drag if enabled)

    @property
    def final_keren_fv(self) -> float:
        """Final future value in Keren Hishtalmut."""
        if not self.yearly_results:
            return self.inputs.principal
        return self.yearly_results[-1].keren_fv

    @property
    def final_personal_fv(self) -> float:
        """Final future value in personal account (after tax)."""
        if not self.yearly_results:
            return self.inputs.principal
        return self.yearly_results[-1].personal_fv_aftertax

    @property
    def final_difference(self) -> float:
        """Final difference (personal - keren)."""
        return self.final_personal_fv - self.final_keren_fv

    @property
    def winner_at_horizon(self) -> str:
        """Which option wins at the specified horizon."""
        if self.final_difference > 0:
            return "Personal Investment"
        elif self.final_difference < 0:
            return "Keren Hishtalmut"
        else:
            return "Tie"


@dataclass
class SensitivityPoint:
    """A single point in sensitivity analysis."""

    personal_return: float
    tax_rate: float
    breakeven_year: Optional[int]


@dataclass
class RequiredReturnResult:
    """Result of calculating required return to beat Keren."""

    horizon_years: int
    keren_net_return: float
    tax_rate: float
    required_personal_return: float
    alpha_required: float  # required_personal_return - keren_net_return
