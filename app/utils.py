import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import os

# ── Color palette ─────────────────────────────────────────────────────────────
BLUE_DARK   = "#0A1628"
BLUE_MID    = "#1B2F55"
BLUE_LIGHT  = "#2A4A8A"
GOLD        = "#C9A84C"
GOLD_LIGHT  = "#E8C97E"
WHITE       = "#F5F7FA"
TEXT_DIM    = "#8FA3C4"
GREEN       = "#4CAF90"
RED         = "#E05C5C"
ORANGE      = "#E8913A"

PLOTLY_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color=WHITE, size=12),
    title_font=dict(family="Inter", color=WHITE, size=15, weight=700),
    legend=dict(bgcolor="rgba(27,47,85,0.8)", bordercolor=BLUE_LIGHT, borderwidth=1),
    xaxis=dict(gridcolor="#1E3050", linecolor=BLUE_LIGHT, tickcolor=TEXT_DIM, tickfont=dict(color=TEXT_DIM)),
    yaxis=dict(gridcolor="#1E3050", linecolor=BLUE_LIGHT, tickcolor=TEXT_DIM, tickfont=dict(color=TEXT_DIM)),
)

# ── Data loader (cached) 
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'clean')

@st.cache_data
def load_annual():
    return pd.read_csv(os.path.join(DATA_PATH, 'annual_clean.csv'))

@st.cache_data
def load_monthly():
    return pd.read_csv(os.path.join(DATA_PATH, 'monthly_clean.csv'))

@st.cache_data
def load_markets():
    return pd.read_csv(os.path.join(DATA_PATH, 'markets_clean.csv'))

@st.cache_data
def load_regional():
    return pd.read_csv(os.path.join(DATA_PATH, 'regional_clean.csv'))

@st.cache_data
def load_scorecard():
    return pd.read_csv(os.path.join(DATA_PATH, 'kpi_scorecard.csv'))

# ── KPI card HTML 
def kpi_card(label, value, delta=None, prefix="", suffix=""):
    delta_html = ""
    if delta is not None:
        cls = "pos" if delta >= 0 else "neg"
        arrow = "▲" if delta >= 0 else "▼"
        delta_html = f'<div class="kpi-delta {cls}">{arrow} {abs(delta):.1f}% vs prior year</div>'
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{prefix}{value}{suffix}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

# ── Insight box 
def insight(text):
    st.markdown(f'<div class="insight-box">💡 {text}</div>', unsafe_allow_html=True)

# ── Section header 
def section(title):
    st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)

# ── Apply theme to any plotly figure 
def apply_theme(fig, height=420):
    fig.update_layout(**PLOTLY_THEME, height=height, margin=dict(l=20, r=20, t=50, b=20))
    fig.update_xaxes(showgrid=True, gridwidth=1)
    fig.update_yaxes(showgrid=True, gridwidth=1)
    return fig
