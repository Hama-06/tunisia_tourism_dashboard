import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import *

def show():
    # ── Header ──────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="page-title">Executive Overview</div>
    <div class="page-subtitle">Tunisia Tourism Sector — Strategic Performance Dashboard · 2000–2024</div>
    """, unsafe_allow_html=True)

    annual = load_annual()
    scorecard = load_scorecard()

    # ── Year filter ──────────────────────────────────────────────────────────
    col_f1, col_f2, _ = st.columns([1, 1, 3])
    with col_f1:
        year_min = int(annual['year'].min())
        year_max = int(annual['year'].max())
        start_year = st.selectbox("From", list(range(year_min, year_max)), index=0)
    with col_f2:
        end_year = st.selectbox("To", list(range(start_year + 1, year_max + 1)), index=len(list(range(start_year + 1, year_max + 1))) - 1)

    df = annual[(annual['year'] >= start_year) & (annual['year'] <= end_year)].copy()
    latest = df[df['year'] == df['year'].max()].iloc[0]
    prev   = df[df['year'] == df['year'].max() - 1].iloc[0] if len(df) > 1 else latest

    # ── KPI Cards ────────────────────────────────────────────────────────────
    section("Key Performance Indicators")
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        delta = (latest['arrivals_thousands'] - prev['arrivals_thousands']) / prev['arrivals_thousands'] * 100
        kpi_card("Tourist Arrivals", f"{latest['arrivals_thousands']:,.0f}K", delta=delta)
    with c2:
        delta = (latest['receipts_musd'] - prev['receipts_musd']) / prev['receipts_musd'] * 100
        kpi_card("Tourism Revenue", f"{latest['receipts_musd']:,.0f}", prefix="$", suffix="M", delta=delta)
    with c3:
        delta = (latest['revenue_per_visitor_usd'] - prev['revenue_per_visitor_usd']) / prev['revenue_per_visitor_usd'] * 100
        kpi_card("Revenue / Visitor", f"{latest['revenue_per_visitor_usd']:,.0f}", prefix="$", suffix=" USD", delta=delta)
    with c4:
        delta = (latest['recovery_index'] - prev['recovery_index']) / prev['recovery_index'] * 100
        kpi_card("Recovery Index", f"{latest['recovery_index']:.1f}", suffix="% of 2019", delta=delta)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Arrivals Timeline ────────────────────────────────────────────────────
    section("Arrivals Timeline — A Story of Resilience")

    events = {2011: ("Revolution", ORANGE), 2015: ("Terror Attacks", RED),
              2019: ("All-time Peak", GREEN), 2020: ("COVID-19", RED), 2023: ("Record Recovery", GREEN)}

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['year'], y=df['arrivals_thousands'],
        mode='lines+markers',
        line=dict(color=GOLD, width=3),
        marker=dict(size=7, color=GOLD, line=dict(color=BLUE_MID, width=2)),
        fill='tozeroy', fillcolor='rgba(201,168,76,0.08)',
        name='Arrivals (K)',
        hovertemplate='<b>%{x}</b><br>Arrivals: %{y:,.0f}K<extra></extra>'
    ))
    for yr, (label, color) in events.items():
        row = df[df['year'] == yr]
        if not row.empty:
            fig.add_annotation(
                x=yr, y=row['arrivals_thousands'].values[0],
                text=label, showarrow=True, arrowhead=2,
                arrowcolor=color, font=dict(size=10, color=color),
                bgcolor=BLUE_MID, bordercolor=color, borderwidth=1,
                borderpad=4, ax=0, ay=-55
            )
    apply_theme(fig, height=400)
    fig.update_xaxes(title_text="Year")
    fig.update_yaxes(title_text="Arrivals (thousands)")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": "hover"})

    insight("Tunisia reached 9.8M arrivals in 2024, surpassing the pre-COVID record of 9.4M set in 2019. "
            "The sector absorbed three major shocks (2011, 2015, 2020) and emerged stronger each time — "
            "a testament to structural demand resilience.")

    # ── Bottom row: Revenue bar + Recovery gauge ─────────────────────────────
    section("Revenue Performance & Recovery Status")
    col_l, col_r = st.columns([3, 2])

    with col_l:
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=df['year'], y=df['receipts_musd'],
            marker=dict(
                color=df['receipts_musd'],
                colorscale=[[0, BLUE_LIGHT], [0.5, GOLD], [1, GOLD_LIGHT]],
                showscale=False
            ),
            name='Revenue (M USD)',
            hovertemplate='<b>%{x}</b><br>Revenue: $%{y:,.0f}M<extra></extra>'
        ))
        apply_theme(fig2, height=320)
        fig2.update_xaxes(title_text="Year")
        fig2.update_yaxes(title_text="Revenue (M USD)")
        fig2.update_layout(title_text="Annual Tourism Revenue (M USD)")
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": "hover"})

    with col_r:
        ri = float(latest['recovery_index'])
        fig3 = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=ri,
            delta={'reference': 100, 'valueformat': '.1f',
                   'increasing': {'color': GREEN}, 'decreasing': {'color': RED}},
            number={'suffix': '%', 'font': {'size': 42, 'color': GOLD}},
            title={'text': f"Recovery vs 2019<br><span style='font-size:12px;color:{TEXT_DIM}'>2019 baseline = 100</span>",
                   'font': {'color': WHITE, 'size': 14}},
            gauge={
                'axis': {'range': [0, 140], 'tickcolor': TEXT_DIM,
                         'tickfont': {'color': TEXT_DIM}, 'nticks': 8},
                'bar': {'color': GOLD, 'thickness': 0.25},
                'bgcolor': BLUE_MID,
                'bordercolor': BLUE_LIGHT,
                'steps': [
                    {'range': [0, 50],   'color': 'rgba(224,92,92,0.2)'},
                    {'range': [50, 100], 'color': 'rgba(232,145,58,0.15)'},
                    {'range': [100, 140],'color': 'rgba(76,175,144,0.15)'},
                ],
                'threshold': {'line': {'color': GREEN, 'width': 3},
                              'thickness': 0.8, 'value': 100}
            }
        ))
        apply_theme(fig3, height=320)
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": "hover"})

    # ── Investment trend ─────────────────────────────────────────────────────
    section("Tourism Investment (M TND) — 2016 to 2024")
    inv_df = df[df['investment_mtnd'].notna()].copy()
    if not inv_df.empty:
        fig4 = go.Figure()
        fig4.add_trace(go.Scatter(
            x=inv_df['year'], y=inv_df['investment_mtnd'],
            mode='lines+markers+text',
            line=dict(color=GOLD, width=2, dash='dot'),
            marker=dict(size=10, color=GOLD, symbol='diamond'),
            text=inv_df['investment_mtnd'].apply(lambda x: f'{x:.0f}M'),
            textposition='top center',
            textfont=dict(color=GOLD_LIGHT, size=11),
            hovertemplate='<b>%{x}</b><br>Investment: %{y:.0f}M TND<extra></extra>'
        ))
        apply_theme(fig4, height=280)
        fig4.update_xaxes(title_text="Year")
        fig4.update_yaxes(title_text="Investment (M TND)")
        st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": "hover"})
        insight("Tourism investments peaked at 447M TND in 2017 but collapsed post-2018 and post-COVID. "
                "The 2024 figure of 205M TND remains 54% below the 2017 peak — "
                "a critical infrastructure gap that risks constraining future capacity.")
