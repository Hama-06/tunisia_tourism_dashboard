import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import *

def show():
    st.markdown("""
    <div class="page-title">Financial Performance</div>
    <div class="page-subtitle">Revenue Trends, Quality of Tourism & Investment Analysis</div>
    """, unsafe_allow_html=True)

    annual = load_annual()

    # ── Filter ───────────────────────────────────────────────────────────────
    years = st.slider("Year range", int(annual['year'].min()), int(annual['year'].max()),
                      (2000, int(annual['year'].max())))
    df = annual[(annual['year'] >= years[0]) & (annual['year'] <= years[1])].copy()

    # ── KPI row ──────────────────────────────────────────────────────────────
    section("Financial KPIs — Latest Year")
    latest = df[df['year'] == df['year'].max()].iloc[0]
    prev   = df[df['year'] == df['year'].max() - 1].iloc[0] if len(df) > 1 else latest

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        d = (latest['receipts_musd'] - prev['receipts_musd']) / prev['receipts_musd'] * 100
        kpi_card("Revenue USD", f"{latest['receipts_musd']:,.0f}", prefix="$", suffix="M", delta=d)
    with c2:
        d = (latest['receipts_mtnd'] - prev['receipts_mtnd']) / prev['receipts_mtnd'] * 100
        kpi_card("Revenue TND", f"{latest['receipts_mtnd']:,.0f}", suffix="M TND", delta=d)
    with c3:
        d = (latest['revenue_per_visitor_usd'] - prev['revenue_per_visitor_usd']) / prev['revenue_per_visitor_usd'] * 100
        kpi_card("Revenue / Visitor", f"{latest['revenue_per_visitor_usd']:.0f}", prefix="$", suffix=" USD", delta=d)
    with c4:
        d = (latest['tourism_pct_exports'] - prev['tourism_pct_exports']) / prev['tourism_pct_exports'] * 100
        kpi_card("% of Exports", f"{latest['tourism_pct_exports']:.1f}", suffix="%", delta=d)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Chart 1: Dual-axis revenue vs arrivals ────────────────────────────────
    section("Revenue vs Arrivals — Volume vs Value Dynamics")
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(
        x=df['year'], y=df['arrivals_thousands'],
        name='Arrivals (K)', marker_color=BLUE_LIGHT, opacity=0.75,
        hovertemplate='<b>%{x}</b><br>Arrivals: %{y:,.0f}K<extra></extra>'
    ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=df['year'], y=df['receipts_musd'],
        name='Revenue ($M)', line=dict(color=GOLD, width=3),
        marker=dict(size=8, color=GOLD),
        hovertemplate='<b>%{x}</b><br>Revenue: $%{y:,.0f}M<extra></extra>'
    ), secondary_y=True)
    fig.update_layout(**PLOTLY_THEME, height=400,
                      title_text="Arrivals (bars) vs Revenue (line) — Growing Gap",
                      margin=dict(l=20, r=20, t=50, b=20))
    fig.update_yaxes(title_text="Arrivals (thousands)", secondary_y=False,
                     gridcolor="#1E3050", tickfont=dict(color=TEXT_DIM))
    fig.update_yaxes(title_text="Revenue (M USD)", secondary_y=True,
                     tickfont=dict(color=GOLD))
    fig.update_xaxes(gridcolor="#1E3050", tickfont=dict(color=TEXT_DIM))
    st.plotly_chart(fig, use_container_width=True)
    insight("Revenue did not grow proportionally to arrivals after 2017. The post-attack period saw "
            "Tunisia compete on price to attract volume — a strategy that compressed revenue per visitor. "
            "The 2008 peak of $554/visitor has never been recovered.")

    # ── Chart 2: Revenue per visitor trend ───────────────────────────────────
    section("Revenue per Visitor — The Quality of Tourism Indicator")
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=df['year'], y=df['revenue_per_visitor_usd'],
        mode='lines+markers',
        line=dict(color=GOLD, width=3),
        marker=dict(size=9, color=df['revenue_per_visitor_usd'],
                    colorscale=[[0, RED], [0.5, ORANGE], [1, GREEN]],
                    showscale=False, line=dict(color=BLUE_MID, width=2)),
        fill='tozeroy', fillcolor='rgba(201,168,76,0.06)',
        hovertemplate='<b>%{x}</b><br>Revenue/Visitor: $%{y:,.0f}<extra></extra>'
    ))
    # Reference line at 2008 peak
    fig2.add_hline(y=554, line_dash='dash', line_color=TEXT_DIM,
                   annotation_text="2008 Peak: $554",
                   annotation_font=dict(color=TEXT_DIM, size=11))
    apply_theme(fig2, height=360)
    fig2.update_layout(title_text="Revenue per Visitor (USD) — Are Tourists Spending More?")
    fig2.update_xaxes(title_text="Year")
    fig2.update_yaxes(title_text="USD / Visitor")
    st.plotly_chart(fig2, use_container_width=True)

    # ── Chart 3: Tourism % of exports + investments ───────────────────────────
    section("Strategic Importance & Investment Commitment")
    col_l, col_r = st.columns(2)

    with col_l:
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=df['year'], y=df['tourism_pct_exports'],
            mode='lines+markers',
            line=dict(color='#3A7BD5', width=2.5),
            fill='tozeroy', fillcolor='rgba(58,123,213,0.08)',
            marker=dict(size=7, color='#3A7BD5'),
            hovertemplate='<b>%{x}</b><br>Tourism % Exports: %{y:.1f}%<extra></extra>'
        ))
        apply_theme(fig3, height=340)
        fig3.update_layout(title_text="Tourism as % of Total Exports")
        fig3.update_xaxes(title_text="Year")
        fig3.update_yaxes(title_text="% of Exports")
        st.plotly_chart(fig3, use_container_width=True)

    with col_r:
        inv_df = df[df['investment_mtnd'].notna()].copy()
        if not inv_df.empty:
            colors = [GREEN if v >= 300 else ORANGE if v >= 200 else RED
                      for v in inv_df['investment_mtnd']]
            fig4 = go.Figure(go.Bar(
                x=inv_df['year'], y=inv_df['investment_mtnd'],
                marker_color=colors,
                text=inv_df['investment_mtnd'].apply(lambda x: f'{x:.0f}M'),
                textposition='outside', textfont=dict(color=WHITE, size=10),
                hovertemplate='<b>%{x}</b><br>Investment: %{y:.0f}M TND<extra></extra>'
            ))
            apply_theme(fig4, height=340)
            fig4.update_layout(title_text="Tourism Investments (M TND)")
            fig4.update_xaxes(title_text="Year")
            fig4.update_yaxes(title_text="M TND")
            st.plotly_chart(fig4, use_container_width=True)
        else:
            st.info("Investment data available from 2016 onwards.")

    insight("Tourism's share of exports fluctuates between 8% and 23% — highly sensitive to security "
            "perceptions. The 2015–2016 crash (23% → 10%) illustrates how terrorism risk reprices "
            "destination competitiveness faster than any other factor.")
