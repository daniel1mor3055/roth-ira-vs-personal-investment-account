"""
Keren Hishtalmut vs Personal Investment Comparison Tool

A Streamlit application to compare the financial outcomes of keeping money
in Keren Hishtalmut (Israel's tax-advantaged savings fund) versus withdrawing
and investing personally.
"""

import streamlit as st
import pandas as pd

from src.models import InvestmentInputs
from src.calculator import (
    run_comparison,
    generate_comparison_dataframe,
    generate_required_return_dataframe,
)
from src.presentation.inputs import render_sidebar_inputs
from src.presentation.charts import (
    create_comparison_chart,
    create_difference_chart,
    create_sensitivity_heatmap,
    create_required_return_chart,
)
from src.presentation.styles import CUSTOM_CSS, format_currency, format_percentage

# Page configuration
st.set_page_config(
    page_title="Keren Hishtalmut vs Personal Investment",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Title and introduction
st.title("Keren Hishtalmut vs Personal Investment")
st.markdown(
    """
Compare the long-term financial outcomes of two strategies:

**Option A:** Keep contributing to Keren Hishtalmut for the entire period

**Option B:** Contribute to Keren during the lockup period (typically 6 years), 
then withdraw and invest personally going forward

⚠️ **Important:** During the lockup period, money must stay in Keren Hishtalmut. 
The comparison shows what happens if you withdraw after lockup vs. keeping it in Keren.
"""
)

# Render sidebar inputs
inputs = render_sidebar_inputs()

# Run comparison
result = run_comparison(inputs)

# Summary Metrics Row
st.header("Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if result.breakeven_year:
        be_text = f"Year {result.breakeven_year}"
        be_help = f"First year (after {inputs.keren_lockup_years}-year lockup) where personal investment beats Keren Hishtalmut"
    else:
        be_text = "Never"
        be_help = f"Personal investment never beats Keren within {inputs.horizon_years} years"
    
    st.metric(
        label="Break-even Year",
        value=be_text,
        help=be_help,
    )

with col2:
    st.metric(
        label="Keren Value at Horizon",
        value=format_currency(result.final_keren_fv),
        delta=format_percentage(result.keren_net_return) + " net return",
    )

with col3:
    st.metric(
        label="Personal Value at Horizon",
        value=format_currency(result.final_personal_fv),
        delta=format_percentage(result.personal_effective_return) + " return (after lockup)",
        help=f"Withdrew at year {inputs.keren_lockup_years} and invested personally since then",
    )

with col4:
    diff_sign = "+" if result.final_difference > 0 else ""
    st.metric(
        label=f"Winner at Year {inputs.horizon_years}",
        value=result.winner_at_horizon,
        delta=f"{diff_sign}{format_currency(result.final_difference)}",
        delta_color="normal" if result.final_difference >= 0 else "inverse",
    )

st.divider()

# Main comparison chart
st.header("Growth Comparison")
comparison_chart = create_comparison_chart(result)
st.plotly_chart(comparison_chart, use_container_width=True)

# Two columns: Difference chart and data table
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("Yearly Difference")
    diff_chart = create_difference_chart(result)
    st.plotly_chart(diff_chart, use_container_width=True)

with col_right:
    st.subheader("Comparison Table")

    # Generate and display dataframe
    df = generate_comparison_dataframe(result)

    # Format currency columns
    df["Keren Hishtalmut"] = df["Keren Hishtalmut"].apply(lambda x: f"₪{x:,.0f}")
    df["Personal (Before Tax)"] = df["Personal (Before Tax)"].apply(
        lambda x: f"₪{x:,.0f}"
    )
    df["Personal (After Tax)"] = df["Personal (After Tax)"].apply(
        lambda x: f"₪{x:,.0f}"
    )
    df["Difference"] = df["Difference"].apply(
        lambda x: f"+₪{x:,.0f}" if x > 0 else f"₪{x:,.0f}"
    )
    df["Difference %"] = df["Difference %"].apply(lambda x: f"{x:+.1f}%")

    # Highlight breakeven row
    def highlight_breakeven(row):
        if result.breakeven_year and row["Year"] == result.breakeven_year:
            return ["background-color: #d97706; color: white; font-weight: bold"] * len(row)
        return [""] * len(row)

    styled_df = df.style.apply(highlight_breakeven, axis=1)
    st.dataframe(styled_df, use_container_width=True, height=400)

st.divider()

# Sensitivity Analysis Section
st.header("Sensitivity Analysis")

tab1, tab2 = st.tabs(["Break-even Heatmap", "Required Return"])

with tab1:
    st.markdown(
        """
    This heatmap shows the break-even year for different combinations of
    **personal investment return** and **capital gains tax rate**.
    Lower numbers (green) mean personal investment wins sooner.
    """
    )

    heatmap = create_sensitivity_heatmap(
        principal=inputs.principal,
        keren_net_return=result.keren_net_return,
        monthly_contribution=inputs.monthly_contribution,
        keren_lockup_years=inputs.keren_lockup_years,
    )
    st.plotly_chart(heatmap, use_container_width=True)

with tab2:
    st.markdown(
        """
    This chart shows the **minimum annual return** you need from personal investment
    to match Keren Hishtalmut for different investment horizons.
    The longer your horizon, the lower the required return.
    """
    )

    required_chart = create_required_return_chart(
        keren_net_return=result.keren_net_return,
        tax_rate=inputs.capital_gains_tax,
    )
    st.plotly_chart(required_chart, use_container_width=True)

    # Table of required returns
    horizons = [5, 10, 15, 20, 25, 30]
    req_df = generate_required_return_dataframe(
        result.keren_net_return, inputs.capital_gains_tax, horizons
    )
    st.dataframe(req_df, use_container_width=True, hide_index=True)

st.divider()

# Key Assumptions Box
st.header("Key Assumptions")

with st.expander("Click to view the assumptions used in this analysis", expanded=False):
    st.markdown(
        f"""
    ### Your Inputs
    - **Initial Principal:** {format_currency(inputs.principal)}
    - **Monthly Contribution:** {format_currency(inputs.monthly_contribution)}
    - **Keren Lockup Period:** {inputs.keren_lockup_years} years (cannot withdraw before this)
    - **Keren Hishtalmut Return:** {format_percentage(inputs.keren_gross_return)}
      {'(already net of fees)' if inputs.keren_return_is_net else f'gross, {format_percentage(inputs.keren_mgmt_fee)} management fee'}
    - **Keren Net Return:** {format_percentage(result.keren_net_return)}
    - **Personal Investment Return:** {format_percentage(inputs.personal_return)}
      {f'(effective: {format_percentage(result.personal_effective_return)} after tax drag)' if inputs.include_tax_drag else ''}
    - **Capital Gains Tax:** {format_percentage(inputs.capital_gains_tax)}
    - **Investment Horizon:** {inputs.horizon_years} years

    ### Model Assumptions
    1. **Keren Hishtalmut is tax-exempt** on capital gains when withdrawn after the vesting period
    2. **Personal investment tax is deferred** until sale (no annual capital gains realization)
    3. **Returns are compounded annually** with no withdrawals
    4. **Tax rates remain constant** throughout the investment period
    5. **No inflation adjustment** - all values are nominal

    ### Important Notes
    - The "tax drag" option accounts for annual tax leakage from dividends and rebalancing
    - Break-even calculations assume you hold until the specified horizon
    - Real-world results may vary based on actual market performance and tax law changes
    """
    )

# Documentation link
st.sidebar.divider()
st.sidebar.markdown(
    """
### Learn More
See the [full mathematical analysis](docs/keren_hishtalmut_analysis.md)
for detailed formulas and explanations.
"""
)
