import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import *

def show():
    st.markdown("""
    <div class="page-title">Arrivals Analysis</div>
    <div class="page-subtitle">Monthly Trends, Seasonality Patterns & Year-over-Year Comparisons</div>
    """, unsafe_allow_html=True)

    monthly = load_monthly()
    annual  = load_annual()

    # ── Filters ──────────────────────────────────────────────────────────────
    col_f1, col_f2 = st.columns([2, 3])
    with col_f1:
        available_years = sorted(monthly['year'].unique())
        selected_years  = st.multiselect(
            "Select years to compare",
            available_years,
            default=[2019, 2022, 2023, 2024] if 2024 in available_years else available_years[-3:]
        )

    if not selected_years:
        st.warning("Please select at least one year.")
        return

    filtered = monthly[monthly['year'].isin(selected_years)].copy()

    MONTH_ORDER = ['January','February','March','April','May','June',
                   'July','August','September','October','November','December']
    filtered['month_name'] = pd.Categorical(filtered['month_name'], categories=MONTH_ORDER, ordered=True)
    filtered = filtered.sort_values(['year','month'])

    # ── Chart 1: Line comparison ──────────────────────────────────────────────
    section("Monthly Arrivals — Year Comparison")

    colors_seq = [GOLD, '#3A7BD5', GREEN, ORANGE, RED, '#9B59B6']
    fig = go.Figure()
    for i, yr in enumerate(sorted(selected_years)):
        d = filtered[filtered['year'] == yr]
        fig.add_trace(go.Scatter(
            x=d['month_name'], y=d['arrivals_thousands'],
            mode='lines+markers', name=str(yr),
            line=dict(color=colors_seq[i % len(colors_seq)], width=2.5),
            marker=dict(size=7),
            hovertemplate=f'<b>{yr}</b> — %{{x}}<br>Arrivals: %{{y:,.0f}}K<extra></extra>'
        ))
    apply_theme(fig, height=400)
    fig.update_layout(
        title_text="Monthly Arrivals Profile — Seasonal Shape by Year",
        xaxis_title="Month", yaxis_title="Arrivals (thousands)",
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)
    insight("The seasonal curve is structurally identical every year — July and August consistently "
            "represent 30–35% of annual arrivals, creating extreme pressure on coastal infrastructure "
            "and leaving winter capacity severely underutilized.")

    # ── Chart 2: Heatmap ─────────────────────────────────────────────────────
    section("Arrivals Heatmap — Month × Year Intensity")

    all_monthly = monthly.copy()
    all_monthly['month_name'] = pd.Categorical(all_monthly['month_name'], categories=MONTH_ORDER, ordered=True)
    heatmap_data = all_monthly.pivot_table(index='month_name', columns='year', values='arrivals_thousands')
    heatmap_data = heatmap_data.reindex(MONTH_ORDER)

    fig2 = go.Figure(go.Heatmap(
        z=heatmap_data.values,
        x=[str(c) for c in heatmap_data.columns],
        y=heatmap_data.index.tolist(),
        colorscale=[[0, BLUE_DARK], [0.3, BLUE_LIGHT], [0.65, GOLD], [1, GOLD_LIGHT]],
        hovertemplate='<b>%{y} %{x}</b><br>Arrivals: %{z:,.0f}K<extra></extra>',
        colorbar=dict(
            title=dict(text="Arrivals (K)", font=dict(color=WHITE)),
            tickfont=dict(color=WHITE),
            bgcolor=BLUE_MID,
            bordercolor=BLUE_LIGHT
        )
    ))
    apply_theme(fig2, height=420)
    fig2.update_layout(title_text="Monthly Arrivals Heatmap (All Years)")
    fig2.update_xaxes(title_text="Year", tickangle=-45)
    fig2.update_yaxes(title_text="")
    st.plotly_chart(fig2, use_container_width=True)
    insight("The COVID collapse of 2020 is visible in stark contrast — April through June were "
            "effectively zero. The 2023 heatmap shows the recovery fully mirrors the pre-2015 pattern, "
            "confirming structural demand has returned.")

    # ── Chart 3: Seasonality avg + YoY growth ────────────────────────────────
    section("Seasonality Profile & YoY Growth")
    col_l, col_r = st.columns(2)

    with col_l:
        avg = all_monthly.groupby('month_name', observed=True)['arrivals_thousands'].mean().reset_index()
        avg = avg.set_index('month_name').reindex(MONTH_ORDER).reset_index()
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            x=avg['month_name'], y=avg['arrivals_thousands'],
            marker=dict(
                color=avg['arrivals_thousands'],
                colorscale=[[0, BLUE_LIGHT], [0.5, GOLD], [1, GOLD_LIGHT]],
                showscale=False
            ),
            name='Avg Arrivals',
            hovertemplate='%{x}<br>Avg: %{y:,.0f}K<extra></extra>'
        ))
        apply_theme(fig3, height=340)
        fig3.update_layout(title_text="Average Monthly Profile (All Years)")
        fig3.update_xaxes(tickangle=-45)
        fig3.update_yaxes(title_text="Avg Arrivals (K)")
        st.plotly_chart(fig3, use_container_width=True)

    with col_r:
        yoy = annual[['year','arrivals_thousands','arrivals_yoy_pct']].dropna().copy()
        colors_bar = [GREEN if v >= 0 else RED for v in yoy['arrivals_yoy_pct']]
        fig4 = go.Figure(go.Bar(
            x=yoy['year'], y=yoy['arrivals_yoy_pct'],
            marker_color=colors_bar,
            text=yoy['arrivals_yoy_pct'].apply(lambda x: f'{x:+.1f}%'),
            textposition='outside',
            textfont=dict(size=10, color=WHITE),
            hovertemplate='<b>%{x}</b><br>YoY Growth: %{y:+.1f}%<extra></extra>'
        ))
        fig4.add_hline(y=0, line_color=TEXT_DIM, line_width=1)
        apply_theme(fig4, height=340)
        fig4.update_layout(title_text="Year-over-Year Arrivals Growth (%)")
        fig4.update_xaxes(title_text="Year")
        fig4.update_yaxes(title_text="Growth (%)")
        st.plotly_chart(fig4, use_container_width=True)

    # ── Summary stats ────────────────────────────────────────────────────────
    section("Quick Statistics")
    summer = all_monthly[all_monthly['month'].isin([7, 8])]['arrivals_thousands'].sum()
    total  = all_monthly['arrivals_thousands'].sum()
    best_month_row = all_monthly.loc[all_monthly['arrivals_thousands'].idxmax()]

    c1, c2, c3 = st.columns(3)
    with c1:
        kpi_card("Summer Concentration", f"{summer/total*100:.1f}", suffix="% (Jul+Aug)")
    with c2:
        kpi_card("Peak Month Ever", f"{best_month_row['arrivals_thousands']:,.0f}K",
                 prefix=f"{best_month_row['month_name'][:3]} {int(best_month_row['year'])} — ")
    with c3:
        winter = all_monthly[all_monthly['month'].isin([12,1,2])]['arrivals_thousands'].sum()
        kpi_card("Winter Share", f"{winter/total*100:.1f}", suffix="% (Dec–Feb)")
