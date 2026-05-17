import streamlit as st

# ── Page config — must be first Streamlit call ────────────────────────────────
st.set_page_config(
    page_title="Tunisia Tourism Intelligence",
    page_icon="🇹🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Global CSS — Deep Blue & Gold theme ───────────────────────────────────────
st.markdown("""
<style>
/* ── Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Root variables ── */
:root {
    --blue-dark:   #0A1628;
    --blue-mid:    #1B2F55;
    --blue-light:  #2A4A8A;
    --gold:        #C9A84C;
    --gold-light:  #E8C97E;
    --white:       #F5F7FA;
    --text-dim:    #8FA3C4;
}

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0D1B2A;
    color: #F5F7FA;
}

/* ── Main container ── */
.main .block-container {
    padding: 1.5rem 2.5rem 2rem 2.5rem;
    max-width: 1400px;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0A1628 0%, #1B2F55 100%);
    border-right: 1px solid #2A4A8A;
}
[data-testid="stSidebar"] * {
    color: #F5F7FA !important;
}
[data-testid="stSidebar"] .stRadio label {
    font-size: 14px;
    padding: 6px 0;
    cursor: pointer;
}

/* ── KPI cards ── */
.kpi-card {
    background: linear-gradient(135deg, #1B2F55 0%, #0A1628 100%);
    border: 1px solid #2A4A8A;
    border-top: 3px solid #C9A84C;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    height: 100%;
}
.kpi-label {
    font-size: 11px;
    font-weight: 600;
    color: #8FA3C4;
    text-transform: uppercase;
    letter-spacing: .08em;
    margin-bottom: 6px;
}
.kpi-value {
    font-size: 28px;
    font-weight: 700;
    color: #C9A84C;
    line-height: 1.1;
}
.kpi-delta {
    font-size: 12px;
    margin-top: 6px;
}
.kpi-delta.pos { color: #4CAF90; }
.kpi-delta.neg { color: #E05C5C; }

/* ── Section headers ── */
.section-header {
    font-size: 13px;
    font-weight: 600;
    color: #C9A84C;
    text-transform: uppercase;
    letter-spacing: .1em;
    border-bottom: 1px solid #2A4A8A;
    padding-bottom: 8px;
    margin: 1.5rem 0 1rem;
}

/* ── Page title ── */
.page-title {
    font-size: 28px;
    font-weight: 700;
    color: #F5F7FA;
    margin-bottom: 4px;
}
.page-subtitle {
    font-size: 14px;
    color: #8FA3C4;
    margin-bottom: 1.5rem;
}

/* ── Insight box ── */
.insight-box {
    background: linear-gradient(135deg, #1B2F55 0%, #162240 100%);
    border-left: 4px solid #C9A84C;
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    margin: 12px 0;
    font-size: 13px;
    color: #D0DCEE;
    line-height: 1.6;
}

/* ── Plotly charts — transparent background ── */
.js-plotly-plot .plotly .bg { fill: transparent !important; }

/* ── Selectbox, slider ── */
[data-testid="stSelectbox"] > div,
[data-testid="stMultiSelect"] > div {
    background: #1B2F55;
    border: 1px solid #2A4A8A;
    border-radius: 8px;
    color: #F5F7FA;
}

/* ── Divider ── */
hr { border-color: #2A4A8A; }

/* ── Hide Streamlit auto-page nav ── */
[data-testid="stSidebarNavItems"] { display: none !important; }
[data-testid="stSidebarNav"]      { display: none !important; }
section[data-testid="stSidebarNav"] { display: none !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0A1628; }
::-webkit-scrollbar-thumb { background: #2A4A8A; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0 1.5rem;'>
        <div style='font-size:40px'>🇹🇳</div>
        <div style='font-size:16px; font-weight:700; color:#C9A84C; margin-top:8px;'>Tunisia Tourism</div>
        <div style='font-size:11px; color:#8FA3C4; margin-top:4px; letter-spacing:.08em;'>INTELLIGENCE DASHBOARD</div>
    </div>
    <hr style='border-color:#2A4A8A; margin-bottom:1.2rem;'>
    """, unsafe_allow_html=True)

    st.markdown("<div style='font-size:11px;color:#8FA3C4;letter-spacing:.08em;font-weight:600;margin-bottom:8px;'>NAVIGATION</div>", unsafe_allow_html=True)

    page = st.radio(
        label="",
        options=[
            "🏠  Executive Overview",
            "✈️  Arrivals Analysis",
            "💰  Financial Performance",
            "🌍  Markets & Regions"
        ],
        label_visibility="collapsed"
    )

    st.markdown("""
    <hr style='border-color:#2A4A8A; margin: 1.5rem 0 1rem;'>
    <div style='font-size:11px;color:#8FA3C4;letter-spacing:.08em;font-weight:600;margin-bottom:10px;'>DATA SOURCES</div>
    <div style='font-size:11px;color:#8FA3C4;line-height:2;'>
        📊 World Bank (2000–2020)<br>
        📋 INS / ONTT (2021–2024)<br>
        🏨 ONTT Regional Stats<br>
        💹 ONTT Investments Report
    </div>
    <hr style='border-color:#2A4A8A; margin: 1rem 0;'>
    <div style='font-size:10px;color:#4A6080;text-align:center;'>
        Period: 2000 – 2024<br>DS2 Project · 2025
    </div>
    """, unsafe_allow_html=True)

# ── Route to pages ────────────────────────────────────────────────────────────
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if "Executive" in page:
    from views import overview
    overview.show()
elif "Arrivals" in page:
    from views import arrivals
    arrivals.show()
elif "Financial" in page:
    from views import financial
    financial.show()
elif "Markets" in page:
    from views import markets
    markets.show()
