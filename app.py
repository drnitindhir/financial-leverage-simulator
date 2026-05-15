import math
from typing import Dict, Any, List

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# ------------------------------------------------------------
# Page Configuration
# ------------------------------------------------------------
st.set_page_config(
    page_title="Financial Leverage & Risk Simulator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ------------------------------------------------------------
# Global Constants
# ------------------------------------------------------------
CAPITAL_EMPLOYED_CRORE = 100.0
CAPITAL_EMPLOYED_LAKH = CAPITAL_EMPLOYED_CRORE * 100.0  # 1 crore = 100 lakh
INTEREST_RATE = 0.10
TAX_RATE = 0.30
MAX_DEBT_PERCENT = 90


# ------------------------------------------------------------
# Custom CSS
# ------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(26, 188, 156, 0.13), transparent 32%),
            radial-gradient(circle at top right, rgba(231, 76, 60, 0.11), transparent 28%),
            linear-gradient(135deg, #07111f 0%, #0b1728 42%, #101b2f 100%);
        color: #f7fbff;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #07111f 0%, #0b1728 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }

    section[data-testid="stSidebar"] label {
        color: #dce8f7 !important;
        font-weight: 600;
    }

    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2rem;
    }

    .main-title {
        font-size: 2.25rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        margin-bottom: 0.1rem;
        color: #ffffff;
    }

    .subtitle {
        color: #9fb1c7;
        font-size: 0.98rem;
        margin-bottom: 1.2rem;
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.065);
        border: 1px solid rgba(255, 255, 255, 0.10);
        box-shadow: 0 16px 45px rgba(0, 0, 0, 0.24);
        border-radius: 22px;
        padding: 1.1rem 1.15rem;
        min-height: 250px;
        backdrop-filter: blur(12px);
    }

    .scenario-title {
        font-size: 1.12rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 0.8rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .risk-pill {
        padding: 0.32rem 0.65rem;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 800;
        letter-spacing: 0.02em;
    }

    .risk-safe {
        color: #02140f;
        background: #2ee59d;
    }

    .risk-moderate {
        color: #1d1100;
        background: #ffb84d;
    }

    .risk-high {
        color: #ffffff;
        background: #ff4f5e;
    }

    .metric-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0.68rem;
    }

    .metric-box {
        background: rgba(8, 17, 32, 0.70);
        border: 1px solid rgba(255, 255, 255, 0.09);
        border-radius: 16px;
        padding: 0.72rem 0.8rem;
    }

    .metric-label {
        color: #94a6bd;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 0.25rem;
    }

    .metric-value {
        color: #ffffff;
        font-size: 1rem;
        font-weight: 800;
        line-height: 1.2;
    }

    .metric-value-green {
        color: #2ee59d;
    }

    .metric-value-orange {
        color: #ffb84d;
    }

    .metric-value-red {
        color: #ff4f5e;
    }

    .section-heading {
        color: #ffffff;
        font-size: 1.35rem;
        font-weight: 800;
        margin: 1.45rem 0 0.75rem 0;
        letter-spacing: -0.02em;
    }

    .assumption-card {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.10);
        border-radius: 18px;
        padding: 0.9rem;
        margin-bottom: 1rem;
    }

    .assumption-title {
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 0.5rem;
    }

    .assumption-line {
        color: #b4c2d4;
        font-size: 0.88rem;
        margin: 0.18rem 0;
    }

    div[data-testid="stDataFrame"] {
        border-radius: 18px;
        overflow: hidden;
    }

    .footer {
        color: #8798ad;
        text-align: center;
        font-size: 0.86rem;
        padding-top: 1.5rem;
    }

    hr {
        border: none;
        height: 1px;
        background: rgba(255, 255, 255, 0.10);
        margin: 1.1rem 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------
def format_lakh(value: float) -> str:
    return f"₹{value:,.2f} lakh"


def format_crore_from_lakh(value_lakh: float) -> str:
    return f"₹{value_lakh / 100:,.2f} crore"


def format_percent(value: float) -> str:
    if value is None or (isinstance(value, float) and not math.isfinite(value)):
        return "N/A"
    return f"{value:,.2f}%"


def format_ratio(value: float) -> str:
    if value is None or (isinstance(value, float) and not math.isfinite(value)):
        return "N/A"
    return f"{value:,.2f}x"


def safe_divide(numerator: float, denominator: float) -> float:
    if denominator == 0:
        return math.inf if numerator > 0 else 0.0
    return numerator / denominator


def classify_risk(icr: float) -> Dict[str, Any]:
    if icr is None or not math.isfinite(icr):
        return {
            "level": "Safe",
            "score": 10,
            "class": "risk-safe",
            "color": "#2ee59d",
        }

    if icr > 3:
        return {
            "level": "Safe",
            "score": 20,
            "class": "risk-safe",
            "color": "#2ee59d",
        }
    if icr >= 1.5:
        return {
            "level": "Moderate",
            "score": 55,
            "class": "risk-moderate",
            "color": "#ffb84d",
        }
    return {
        "level": "High Risk",
        "score": 85,
        "class": "risk-high",
        "color": "#ff4f5e",
    }


def calculate_scenario(name: str, debt_percent: float, ebit_lakh: float) -> Dict[str, Any]:
    debt_lakh = CAPITAL_EMPLOYED_LAKH * (debt_percent / 100)
    equity_lakh = CAPITAL_EMPLOYED_LAKH - debt_lakh
    interest_lakh = debt_lakh * INTEREST_RATE
    pbt_lakh = ebit_lakh - interest_lakh
    tax_lakh = pbt_lakh * TAX_RATE if pbt_lakh > 0 else 0.0
    pat_lakh = pbt_lakh - tax_lakh
    roe_percent = (pat_lakh / equity_lakh) * 100 if equity_lakh > 0 else math.nan
    icr = safe_divide(ebit_lakh, interest_lakh) if interest_lakh > 0 else math.inf
    dfl = safe_divide(ebit_lakh, pbt_lakh)
    risk = classify_risk(icr)

    return {
        "Scenario": name,
        "Capital Employed": CAPITAL_EMPLOYED_LAKH,
        "Debt %": debt_percent,
        "Debt": debt_lakh,
        "Equity": equity_lakh,
        "EBIT": ebit_lakh,
        "Interest": interest_lakh,
        "PBT": pbt_lakh,
        "Tax": tax_lakh,
        "PAT": pat_lakh,
        "ROE": roe_percent,
        "ICR": icr,
        "DFL": dfl,
        "Risk Level": risk["level"],
        "Risk Score": risk["score"],
        "Risk Class": risk["class"],
        "Risk Color": risk["color"],
    }


def scenario_card(scenario: Dict[str, Any]) -> None:
    roe_class = "metric-value-green" if scenario["ROE"] >= 0 else "metric-value-red"
    pat_class = "metric-value-green" if scenario["PAT"] >= 0 else "metric-value-red"
    pbt_class = "metric-value-green" if scenario["PBT"] >= 0 else "metric-value-red"
    icr_class = (
        "metric-value-green"
        if scenario["Risk Level"] == "Safe"
        else "metric-value-orange"
        if scenario["Risk Level"] == "Moderate"
        else "metric-value-red"
    )

    st.markdown(
        f"""
        <div class="glass-card">
            <div class="scenario-title">
                <span>{scenario["Scenario"]}</span>
                <span class="risk-pill {scenario["Risk Class"]}">{scenario["Risk Level"]}</span>
            </div>
            <div class="metric-grid">
                <div class="metric-box">
                    <div class="metric-label">Debt</div>
                    <div class="metric-value">{format_crore_from_lakh(scenario["Debt"])}</div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">Equity</div>
                    <div class="metric-value">{format_crore_from_lakh(scenario["Equity"])}</div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">Interest</div>
                    <div class="metric-value">{format_crore_from_lakh(scenario["Interest"])}</div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">PBT</div>
                    <div class="metric-value {pbt_class}">{format_crore_from_lakh(scenario["PBT"])}</div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">PAT</div>
                    <div class="metric-value {pat_class}">{format_crore_from_lakh(scenario["PAT"])}</div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">ROE</div>
                    <div class="metric-value {roe_class}">{format_percent(scenario["ROE"])}</div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">ICR</div>
                    <div class="metric-value {icr_class}">{format_ratio(scenario["ICR"])}</div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">DFL</div>
                    <div class="metric-value">{format_ratio(scenario["DFL"])}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def risk_gauge(scenario: Dict[str, Any]) -> go.Figure:
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=scenario["Risk Score"],
            number={
                "suffix": "/100",
                "font": {"size": 28, "color": "#ffffff"},
            },
            title={
                "text": f"{scenario['Scenario']} Risk Score",
                "font": {"size": 16, "color": "#dce8f7"},
            },
            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickcolor": "#8fa6bf",
                    "tickfont": {"color": "#9fb1c7"},
                },
                "bar": {"color": scenario["Risk Color"], "thickness": 0.28},
                "bgcolor": "rgba(255,255,255,0.08)",
                "borderwidth": 1,
                "bordercolor": "rgba(255,255,255,0.18)",
                "steps": [
                    {"range": [0, 35], "color": "rgba(46, 229, 157, 0.25)"},
                    {"range": [35, 70], "color": "rgba(255, 184, 77, 0.28)"},
                    {"range": [70, 100], "color": "rgba(255, 79, 94, 0.30)"},
                ],
                "threshold": {
                    "line": {"color": "#ffffff", "width": 3},
                    "thickness": 0.75,
                    "value": scenario["Risk Score"],
                },
            },
        )
    )
    fig.update_layout(
        height=285,
        margin=dict(l=20, r=20, t=55, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#ffffff"),
    )
    return fig


def donut_chart(scenario: Dict[str, Any]) -> go.Figure:
    fig = go.Figure(
        data=[
            go.Pie(
                labels=["Debt", "Equity"],
                values=[scenario["Debt"], scenario["Equity"]],
                customdata=[scenario["Debt"] / 100, scenario["Equity"] / 100],
                hole=0.62,
                marker=dict(colors=["#ff4f5e", "#2ee59d"]),
                textinfo="label+percent",
                textfont=dict(color="#ffffff", size=13),
                hovertemplate="%{label}<br>₹%{customdata:,.2f} crore<br>%{percent}<extra></extra>",
            )
        ]
    )
    fig.update_layout(
        title=dict(
            text=f"{scenario['Scenario']} Debt vs Equity",
            x=0.5,
            font=dict(color="#ffffff", size=16),
        ),
        height=320,
        margin=dict(l=10, r=10, t=55, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=True,
        legend=dict(
            orientation="h",
            y=-0.05,
            x=0.5,
            xanchor="center",
            font=dict(color="#dce8f7"),
        ),
    )
    return fig


def table_dataframe(scenarios: List[Dict[str, Any]]) -> pd.DataFrame:
    rows = []
    for s in scenarios:
        rows.append(
            {
                "Scenario": s["Scenario"],
                "Capital Employed": f"₹{CAPITAL_EMPLOYED_CRORE:,.0f} crore",
                "Debt %": f"{s['Debt %']:.0f}%",
                "Debt": format_crore_from_lakh(s["Debt"]),
                "Equity": format_crore_from_lakh(s["Equity"]),
                "EBIT": format_crore_from_lakh(s["EBIT"]),
                "Interest": format_crore_from_lakh(s["Interest"]),
                "PBT": format_crore_from_lakh(s["PBT"]),
                "PAT": format_crore_from_lakh(s["PAT"]),
                "ROE": format_percent(s["ROE"]),
                "ICR": format_ratio(s["ICR"]),
                "DFL": format_ratio(s["DFL"]),
                "Risk Level": s["Risk Level"],
            }
        )
    return pd.DataFrame(rows)


# ------------------------------------------------------------
# Sidebar Inputs
# ------------------------------------------------------------
st.sidebar.markdown(
    """
    <div class="assumption-card">
        <div class="assumption-title">Fixed Assumptions</div>
        <div class="assumption-line">Capital Employed: ₹100 crore</div>
        <div class="assumption-line">Interest Rate: 10%</div>
        <div class="assumption-line">Tax Rate: 30%</div>
        <div class="assumption-line">Maximum Debt: 90%</div>
        <div class="assumption-line">EBIT Unit: ₹ crore</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown("### Scenario Inputs")

defaults = {
    "Scenario 1": {"debt_percent": 20, "ebit": 6},
    "Scenario 2": {"debt_percent": 50, "ebit": 10},
    "Scenario 3": {"debt_percent": 80, "ebit": 14},
}

scenario_inputs = {}

for scenario_name, default in defaults.items():
    st.sidebar.markdown(f"#### {scenario_name}")

    debt_percent = st.sidebar.number_input(
        f"{scenario_name} Debt Percentage",
        min_value=0,
        max_value=MAX_DEBT_PERCENT,
        value=default["debt_percent"],
        step=10,
        help="Debt percentage can be entered from 0% to 90% in steps of 10%.",
        key=f"{scenario_name}_debt_percent",
    )

    ebit_crore = st.sidebar.slider(
        f"{scenario_name} EBIT (₹ crore)",
        min_value=0,
        max_value=20,
        value=default["ebit"],
        step=1,
        help="EBIT is displayed in crores. Example: 6 means ₹6 crore.",
        key=f"{scenario_name}_ebit",
    )

    scenario_inputs[scenario_name] = {
        "debt_percent": debt_percent,
        # Backend still uses lakh internally because capital employed is already converted to lakh.
        # 1 crore = 100 lakh.
        "ebit_lakh": ebit_crore * 100.0,
    }

    st.sidebar.markdown("---")


# ------------------------------------------------------------
# Main App
# ------------------------------------------------------------
st.markdown(
    """
    <div class="main-title">Financial Leverage & Risk Simulator</div>
    <div class="subtitle">Developed by Dr. Nitin Dhir · Scenario-based capital structure and risk dashboard</div>
    """,
    unsafe_allow_html=True,
)

scenarios = [
    calculate_scenario(
        name,
        values["debt_percent"],
        values["ebit_lakh"],
    )
    for name, values in scenario_inputs.items()
]

# Row 1: Three Scenario Summary Cards
st.markdown('<div class="section-heading">Scenario Summary Cards</div>', unsafe_allow_html=True)
cols = st.columns(3)
for col, scenario in zip(cols, scenarios):
    with col:
        scenario_card(scenario)

# Detailed comparison table above charts as requested
st.markdown('<div class="section-heading">Detailed Scenario Comparison Table</div>', unsafe_allow_html=True)
comparison_df = table_dataframe(scenarios)
st.dataframe(comparison_df, use_container_width=True, hide_index=True)

# Row 2: Three Risk Gauges
st.markdown('<div class="section-heading">Risk Gauges</div>', unsafe_allow_html=True)
gauge_cols = st.columns(3)
for col, scenario in zip(gauge_cols, scenarios):
    with col:
        st.plotly_chart(risk_gauge(scenario), use_container_width=True)

# Row 3: Three Debt-Equity Donut Charts
st.markdown('<div class="section-heading">Debt vs Equity Donut Charts</div>', unsafe_allow_html=True)
donut_cols = st.columns(3)
for col, scenario in zip(donut_cols, scenarios):
    with col:
        st.plotly_chart(donut_chart(scenario), use_container_width=True)

st.markdown(
    """
    <div class="footer">
        Financial Leverage & Risk Simulator · Developed by Dr. Nitin Dhir
    </div>
    """,
    unsafe_allow_html=True,
)
