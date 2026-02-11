"""Custom CSS styles for the Streamlit app."""

CUSTOM_CSS = """
<style>
    /* Main metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        padding: 20px;
        color: white;
        text-align: center;
        margin-bottom: 10px;
    }

    .metric-card.keren {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    }

    .metric-card.personal {
        background: linear-gradient(135deg, #ee0979 0%, #ff6a00 100%);
    }

    .metric-card.breakeven {
        background: linear-gradient(135deg, #4776E6 0%, #8E54E9 100%);
    }

    .metric-card.winner {
        background: linear-gradient(135deg, #F2994A 0%, #F2C94C 100%);
    }

    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 10px 0;
    }

    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }

    /* Winner highlighting */
    .winner-keren {
        border: 3px solid #38ef7d;
        box-shadow: 0 0 15px rgba(56, 239, 125, 0.3);
    }

    .winner-personal {
        border: 3px solid #ff6a00;
        box-shadow: 0 0 15px rgba(255, 106, 0, 0.3);
    }

    /* Table styling */
    .dataframe {
        font-size: 0.9rem;
    }

    /* Section headers */
    .section-header {
        border-bottom: 2px solid #667eea;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }

    /* Info boxes */
    .info-box {
        background-color: #f0f2f6;
        border-left: 4px solid #667eea;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 5px 5px 0;
    }

    /* Breakeven highlight in table */
    .breakeven-row {
        background-color: #fff3cd !important;
        font-weight: bold;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Sidebar styling */
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }

    /* Tooltip styling */
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: help;
    }

    .tooltip .tooltiptext {
        visibility: hidden;
        background-color: #333;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 8px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -100px;
        width: 200px;
        font-size: 0.8rem;
    }

    .tooltip:hover .tooltiptext {
        visibility: visible;
    }
</style>
"""


def get_metric_html(label: str, value: str, card_class: str = "") -> str:
    """Generate HTML for a metric card."""
    return f"""
    <div class="metric-card {card_class}">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """


def format_currency(value: float, symbol: str = "₪") -> str:
    """Format a number as currency."""
    return f"{symbol}{value:,.0f}"


def format_percentage(value: float, decimals: int = 2) -> str:
    """Format a decimal as percentage."""
    return f"{value * 100:.{decimals}f}%"
