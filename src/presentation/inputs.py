"""Streamlit input components for the sidebar."""

import streamlit as st
from ..models import InvestmentInputs


def render_sidebar_inputs() -> InvestmentInputs:
    """
    Render all input controls in the sidebar and return the collected inputs.

    Returns:
        InvestmentInputs dataclass with all user inputs
    """
    st.sidebar.header("Investment Parameters")

    # Principal amount
    st.sidebar.subheader("Investment Amounts")
    principal = st.sidebar.number_input(
        "Initial Principal (₪)",
        min_value=0,
        max_value=10_000_000,
        value=0,
        step=10_000,
        help="Initial lump sum amount (default 0 for starting from scratch)",
    )
    
    monthly_contribution = st.sidebar.number_input(
        "Monthly Contribution (₪)",
        min_value=0,
        max_value=50_000,
        value=1571,
        step=100,
        help="Monthly contribution amount (typical employer + employee contribution)",
    )

    # Keren Hishtalmut parameters
    st.sidebar.subheader("Keren Hishtalmut")

    keren_gross_return = st.sidebar.slider(
        "Expected Return (%)",
        min_value=0.0,
        max_value=15.0,
        value=8.0,
        step=0.1,
        help="Expected annual return in Keren Hishtalmut",
    ) / 100

    keren_mgmt_fee = st.sidebar.slider(
        "Management Fee (%)",
        min_value=0.0,
        max_value=2.0,
        value=0.35,
        step=0.05,
        help="Annual management fee charged by the fund",
    ) / 100

    keren_return_is_net = st.sidebar.checkbox(
        "Return is already net of fees",
        value=False,
        help="Check if the return above is already after deducting management fees",
    )

    # Show calculated net return
    if not keren_return_is_net:
        net_return = (1 + keren_gross_return) * (1 - keren_mgmt_fee) - 1
        st.sidebar.info(f"Net return after fees: **{net_return*100:.2f}%**")

    # Personal investment parameters
    st.sidebar.subheader("Personal Investment")

    personal_return = st.sidebar.slider(
        "Expected Return (%)",
        min_value=0.0,
        max_value=20.0,
        value=10.0,
        step=0.1,
        help="Expected annual return from personal investment",
    ) / 100

    capital_gains_tax = st.sidebar.slider(
        "Capital Gains Tax (%)",
        min_value=0.0,
        max_value=50.0,
        value=25.0,
        step=1.0,
        help="Tax rate on capital gains when you sell",
    ) / 100

    # Tax drag toggle
    st.sidebar.subheader("Tax Drag (Advanced)")

    include_tax_drag = st.sidebar.checkbox(
        "Include annual tax drag",
        value=False,
        help="Account for taxes on dividends and rebalancing during holding period",
    )

    annual_tax_drag = 0.0
    if include_tax_drag:
        annual_tax_drag = st.sidebar.slider(
            "Annual Tax Drag (%)",
            min_value=0.0,
            max_value=2.0,
            value=0.3,
            step=0.1,
            help="Estimated annual tax leakage from dividends/rebalancing",
        ) / 100

        effective_return = personal_return - annual_tax_drag
        st.sidebar.info(f"Effective return after tax drag: **{effective_return*100:.2f}%**")

    # Time horizon
    st.sidebar.subheader("Time Horizon")

    horizon_years = st.sidebar.slider(
        "Investment Horizon (Years)",
        min_value=1,
        max_value=40,
        value=20,
        help="How long you plan to hold the investment",
    )
    
    keren_lockup_years = st.sidebar.number_input(
        "Keren Lockup Period (Years)",
        min_value=1,
        max_value=10,
        value=10,
        help="Years before Keren funds can be withdrawn (typically 10 years in Israel)",
    )

    return InvestmentInputs(
        principal=float(principal),
        monthly_contribution=float(monthly_contribution),
        keren_gross_return=keren_gross_return,
        keren_mgmt_fee=keren_mgmt_fee,
        keren_return_is_net=keren_return_is_net,
        personal_return=personal_return,
        capital_gains_tax=capital_gains_tax,
        annual_tax_drag=annual_tax_drag,
        include_tax_drag=include_tax_drag,
        horizon_years=horizon_years,
        keren_lockup_years=keren_lockup_years,
    )


def render_scenario_presets() -> None:
    """Render preset scenario buttons in the sidebar."""
    st.sidebar.subheader("Quick Scenarios")

    col1, col2 = st.sidebar.columns(2)

    with col1:
        if st.button("Conservative", use_container_width=True):
            st.session_state["preset"] = "conservative"

    with col2:
        if st.button("Aggressive", use_container_width=True):
            st.session_state["preset"] = "aggressive"


def get_preset_values(preset: str) -> dict:
    """Get preset parameter values."""
    presets = {
        "conservative": {
            "keren_gross_return": 0.07,
            "personal_return": 0.08,
            "horizon_years": 10,
        },
        "aggressive": {
            "keren_gross_return": 0.08,
            "personal_return": 0.12,
            "horizon_years": 25,
        },
    }
    return presets.get(preset, {})
