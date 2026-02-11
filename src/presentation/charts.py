"""Visualization components using Plotly."""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import Optional

from ..models import ComparisonResult
from ..calculator import (
    find_breakeven_year,
    generate_sensitivity_matrix,
    generate_required_return_dataframe,
)


def create_comparison_chart(result: ComparisonResult) -> go.Figure:
    """
    Create a line chart comparing Keren Hishtalmut vs Personal Investment over time.

    Args:
        result: ComparisonResult from the calculation

    Returns:
        Plotly Figure object
    """
    years = [yr.year for yr in result.yearly_results]
    keren_values = [yr.keren_fv for yr in result.yearly_results]
    personal_values = [yr.personal_fv_aftertax for yr in result.yearly_results]

    fig = go.Figure()

    # Keren Hishtalmut line
    fig.add_trace(
        go.Scatter(
            x=years,
            y=keren_values,
            mode="lines+markers",
            name="Keren Hishtalmut",
            line=dict(color="#38ef7d", width=3),
            marker=dict(size=6),
            hovertemplate="Year %{x}<br>Value: ₪%{y:,.0f}<extra>Keren</extra>",
        )
    )

    # Personal Investment line
    fig.add_trace(
        go.Scatter(
            x=years,
            y=personal_values,
            mode="lines+markers",
            name="Personal (After Tax)",
            line=dict(color="#ff6a00", width=3),
            marker=dict(size=6),
            hovertemplate="Year %{x}<br>Value: ₪%{y:,.0f}<extra>Personal</extra>",
        )
    )

    # Mark breakeven point if it exists within the horizon
    if result.breakeven_year and result.breakeven_year <= result.inputs.horizon_years:
        be_idx = result.breakeven_year - 1
        be_value = result.yearly_results[be_idx].personal_fv_aftertax

        fig.add_trace(
            go.Scatter(
                x=[result.breakeven_year],
                y=[be_value],
                mode="markers+text",
                name="Break-even",
                marker=dict(color="#8E54E9", size=15, symbol="star"),
                text=[f"Year {result.breakeven_year}"],
                textposition="top center",
                hovertemplate="Break-even Point<br>Year %{x}<br>Value: ₪%{y:,.0f}<extra></extra>",
            )
        )

    # Add shaded regions for winner
    for i, yr in enumerate(result.yearly_results):
        if i == 0:
            continue
        color = "rgba(56, 239, 125, 0.1)" if yr.keren_wins else "rgba(255, 106, 0, 0.1)"

    fig.update_layout(
        title="Investment Growth Comparison",
        xaxis_title="Years",
        yaxis_title="Value (₪)",
        hovermode="x unified",
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
        template="plotly_white",
        height=500,
    )

    # Format y-axis as currency
    fig.update_yaxes(tickformat=",")

    return fig


def create_difference_chart(result: ComparisonResult) -> go.Figure:
    """
    Create a bar chart showing the difference between options each year.

    Args:
        result: ComparisonResult from the calculation

    Returns:
        Plotly Figure object
    """
    years = [yr.year for yr in result.yearly_results]
    differences = [yr.difference for yr in result.yearly_results]
    colors = ["#ff6a00" if d > 0 else "#38ef7d" for d in differences]

    fig = go.Figure(
        go.Bar(
            x=years,
            y=differences,
            marker_color=colors,
            hovertemplate="Year %{x}<br>Difference: ₪%{y:,.0f}<extra></extra>",
        )
    )

    # Add zero line
    fig.add_hline(y=0, line_dash="dash", line_color="gray")

    fig.update_layout(
        title="Yearly Difference (Personal - Keren)",
        xaxis_title="Years",
        yaxis_title="Difference (₪)",
        template="plotly_white",
        height=400,
        showlegend=False,
    )

    # Add annotation
    fig.add_annotation(
        x=0.5,
        y=1.05,
        xref="paper",
        yref="paper",
        text="Green = Keren Wins | Orange = Personal Wins",
        showarrow=False,
        font=dict(size=12),
    )

    return fig


def create_sensitivity_heatmap(
    principal: float,
    keren_net_return: float,
    monthly_contribution: float = 0,
    personal_returns: Optional[list[float]] = None,
    tax_rates: Optional[list[float]] = None,
    keren_lockup_years: int = 6,
) -> go.Figure:
    """
    Create a heatmap showing breakeven years for different parameter combinations.

    Args:
        principal: Initial investment amount
        keren_net_return: Net return for Keren
        personal_returns: List of personal return rates to test
        tax_rates: List of tax rates to test

    Returns:
        Plotly Figure object
    """
    if personal_returns is None:
        personal_returns = [0.08, 0.09, 0.10, 0.11, 0.12, 0.13, 0.14, 0.15]

    if tax_rates is None:
        tax_rates = [0.15, 0.20, 0.25, 0.30, 0.35]

    # Build matrix
    matrix = []
    for pr in personal_returns:
        row = []
        for tr in tax_rates:
            be_year = find_breakeven_year(
                principal, keren_net_return, pr, tr, monthly_contribution, 50, keren_lockup_years
            )
            row.append(be_year if be_year else 50)  # Use 50 for "never"
        matrix.append(row)

    # Create heatmap
    fig = go.Figure(
        go.Heatmap(
            z=matrix,
            x=[f"{tr*100:.0f}%" for tr in tax_rates],
            y=[f"{pr*100:.0f}%" for pr in personal_returns],
            colorscale="RdYlGn_r",  # Reversed: green = low (good), red = high
            colorbar=dict(title="Break-even Year"),
            hovertemplate="Personal Return: %{y}<br>Tax Rate: %{x}<br>Break-even: Year %{z}<extra></extra>",
        )
    )

    # Add text annotations
    for i, pr in enumerate(personal_returns):
        for j, tr in enumerate(tax_rates):
            val = matrix[i][j]
            text = str(val) if val < 50 else ">50"
            fig.add_annotation(
                x=j,
                y=i,
                text=text,
                showarrow=False,
                font=dict(color="white" if val > 20 else "black", size=12),
            )

    fig.update_layout(
        title=f"Break-even Year Sensitivity (Keren Net Return: {keren_net_return*100:.1f}%)",
        xaxis_title="Capital Gains Tax Rate",
        yaxis_title="Personal Investment Return",
        template="plotly_white",
        height=500,
    )

    return fig


def create_required_return_chart(
    keren_net_return: float, tax_rate: float, max_horizon: int = 40
) -> go.Figure:
    """
    Create a chart showing required personal return for different horizons.

    Args:
        keren_net_return: Net return for Keren
        tax_rate: Capital gains tax rate
        max_horizon: Maximum horizon to show

    Returns:
        Plotly Figure object
    """
    from ..calculator import calculate_required_return

    horizons = list(range(1, max_horizon + 1))
    required_returns = [
        calculate_required_return(keren_net_return, tax_rate, h) for h in horizons
    ]

    fig = go.Figure()

    # Required return line
    fig.add_trace(
        go.Scatter(
            x=horizons,
            y=[r * 100 for r in required_returns],
            mode="lines",
            name="Required Return",
            line=dict(color="#8E54E9", width=3),
            fill="tozeroy",
            fillcolor="rgba(142, 84, 233, 0.2)",
            hovertemplate="Horizon: %{x} years<br>Required Return: %{y:.2f}%<extra></extra>",
        )
    )

    # Add Keren return reference line
    fig.add_hline(
        y=keren_net_return * 100,
        line_dash="dash",
        line_color="#38ef7d",
        annotation_text=f"Keren Net Return ({keren_net_return*100:.1f}%)",
        annotation_position="right",
    )

    fig.update_layout(
        title="Required Personal Return to Beat Keren Hishtalmut",
        xaxis_title="Investment Horizon (Years)",
        yaxis_title="Required Annual Return (%)",
        template="plotly_white",
        height=400,
        showlegend=False,
    )

    return fig


def create_growth_area_chart(result: ComparisonResult) -> go.Figure:
    """
    Create a stacked area chart showing the composition of returns.

    Args:
        result: ComparisonResult from the calculation

    Returns:
        Plotly Figure object
    """
    years = [yr.year for yr in result.yearly_results]
    principal = result.inputs.principal

    # Keren breakdown
    keren_principal = [principal] * len(years)
    keren_gain = [yr.keren_fv - principal for yr in result.yearly_results]

    # Personal breakdown
    personal_principal = [principal] * len(years)
    personal_gain_pretax = [
        yr.personal_fv_pretax - principal for yr in result.yearly_results
    ]
    personal_tax = [
        yr.personal_fv_pretax - yr.personal_fv_aftertax for yr in result.yearly_results
    ]

    fig = go.Figure()

    # Personal Investment breakdown
    fig.add_trace(
        go.Scatter(
            x=years,
            y=[principal + g - t for g, t in zip(personal_gain_pretax, personal_tax)],
            mode="lines",
            name="Personal: Net Gain",
            line=dict(color="#ff6a00", width=2),
            stackgroup="personal",
            hovertemplate="Year %{x}<br>Net Gain: ₪%{y:,.0f}<extra></extra>",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=years,
            y=personal_tax,
            mode="lines",
            name="Personal: Tax Paid",
            line=dict(color="#ff0000", width=2),
            stackgroup="personal",
            hovertemplate="Year %{x}<br>Tax: ₪%{y:,.0f}<extra></extra>",
        )
    )

    fig.update_layout(
        title="Investment Growth Breakdown",
        xaxis_title="Years",
        yaxis_title="Value (₪)",
        template="plotly_white",
        height=400,
        hovermode="x unified",
    )

    return fig
