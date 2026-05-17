import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import *

def show():
    st.markdown("""
    <div class="page-title">Markets & Regions</div>
    <div class="page-subtitle">Source Country Analysis, Concentration Risk & Regional Hotel Performance</div>
    """, unsafe_allow_html=True)

    markets  = load_markets()
    regional = load_regional()

    # ── Source markets section ────────────────────────────────────────────────
    section("Source Market Analysis")

    available_years = sorted(markets['year'].unique())
    col_f, _ = st.columns([1, 3])
    with col_f:
        sel_year = st.selectbox("Select year", available_years, index=len(available_years) - 1)

    m_year = markets[markets['year'] == sel_year].copy()

    col_l, col_r = st.columns([3, 2])

    with col_l:
        m_sorted = m_year.sort_values('arrivals_thousands', ascending=True)
        colors = [RED if r == 'Africa' else BLUE_LIGHT if r == 'Europe' else TEXT_DIM
                  for r in m_sorted['region']]
        fig = go.Figure(go.Bar(
            x=m_sorted['arrivals_thousands'], y=m_sorted['country'],
            orientation='h', marker_color=colors,
            text=m_sorted['arrivals_thousands'].apply(lambda x: f'{x:,.0f}K'),
            textposition='outside', textfont=dict(color=WHITE, size=10),
            hovertemplate='<b>%{y}</b><br>Arrivals: %{x:,.0f}K<extra></extra>'
        ))
        apply_theme(fig, height=400)
        fig.update_layout(
            title_text=f"Top Source Markets {sel_year} — 🔴 Africa | 🔵 Europe",
            xaxis_title="Arrivals (thousands)", yaxis_title=""
        )
        fig.update_xaxes(range=[0, m_sorted['arrivals_thousands'].max() * 1.25])
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        region_agg = m_year.groupby('region')['arrivals_thousands'].sum().reset_index()
        fig2 = go.Figure(go.Pie(
            values=region_agg['arrivals_thousands'],
            labels=region_agg['region'],
            hole=0.5,
            marker=dict(colors=[RED, BLUE_LIGHT, TEXT_DIM],
                        line=dict(color=BLUE_DARK, width=2)),
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>%{value:,.0f}K arrivals<br>%{percent}<extra></extra>'
        ))
        fig2.update_layout(**PLOTLY_THEME, height=400,
                           title_text=f"Origin by Region — {sel_year}",
                           margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig2, use_container_width=True)

    # Concentration KPIs
    top2 = m_year.nlargest(2, 'arrivals_thousands')
    top2_total = top2['arrivals_thousands'].sum()
    grand_total = m_year['arrivals_thousands'].sum()
    c1, c2, c3 = st.columns(3)
    with c1:
        kpi_card("Algeria + Libya Share", f"{top2_total/grand_total*100:.1f}", suffix="% of total")
    with c2:
        top_country = m_year.nlargest(1, 'arrivals_thousands').iloc[0]
        kpi_card(f"#{1} Market", f"{top_country['arrivals_thousands']:,.0f}K",
                 prefix=f"{top_country['country']} — ")
    with c3:
        europe = m_year[m_year['region']=='Europe']['arrivals_thousands'].sum()
        kpi_card("European Visitors", f"{europe/grand_total*100:.1f}", suffix="% of total")

    insight(f"In {sel_year}, Algeria and Libya together account for "
            f"{top2_total/grand_total*100:.1f}% of all arrivals — "
            "an extreme concentration risk. Any political instability in either country "
            "can instantly wipe out nearly half of the sector's volume.")

    # ── Market evolution ──────────────────────────────────────────────────────
    section("Top Market Evolution — 2019 vs 2022 vs 2023")

    top_countries = markets.groupby('country')['arrivals_thousands'].sum().nlargest(8).index.tolist()
    evo = markets[markets['country'].isin(top_countries)].copy()

    fig3 = px.bar(
        evo, x='country', y='arrivals_thousands', color='year',
        barmode='group',
        color_discrete_map={2019: TEXT_DIM, 2022: BLUE_LIGHT, 2023: GOLD},
        labels={'arrivals_thousands': 'Arrivals (K)', 'country': '', 'year': 'Year'},
        hover_data={'arrivals_thousands': ':,.0f'}
    )
    apply_theme(fig3, height=380)
    fig3.update_layout(title_text="Market Recovery — Which Countries Came Back?")
    st.plotly_chart(fig3, use_container_width=True)

    # ── Regional section ──────────────────────────────────────────────────────
    section("Regional Hotel Performance — Tunisia Governorates")

    col_map, col_bar = st.columns([3, 2])

    with col_map:
        fig4 = px.scatter_mapbox(
            regional,
            lat='lat', lon='lon',
            size='hotel_beds',
            color='hotel_capacity_pct_2023',
            hover_name='governorate',
            hover_data={
                'hotel_beds': ':,', 'hotel_capacity_pct_2023': ':.0f',
                'tourism_type': True, 'lat': False, 'lon': False
            },
            color_continuous_scale=[[0, RED], [0.5, ORANGE], [1, GREEN]],
            size_max=45, zoom=5.2,
            center={'lat': 33.8, 'lon': 9.7},
            mapbox_style='carto-darkmatter',
        )
        fig4.update_layout(
            **PLOTLY_THEME, height=460,
            title_text="Hotel Capacity & Occupancy Rate 2023",
            margin=dict(l=0, r=0, t=50, b=0),
            coloraxis_colorbar=dict(
                title=dict(text="Occupancy %", font=dict(color=WHITE)),
                tickfont=dict(color=WHITE)
            )
        )
        st.plotly_chart(fig4, use_container_width=True)

    with col_bar:
        reg_sorted = regional.sort_values('hotel_capacity_pct_2023', ascending=True)
        fig5 = go.Figure()
        fig5.add_trace(go.Bar(
            y=reg_sorted['governorate'], x=reg_sorted['hotel_capacity_pct_2019'],
            orientation='h', name='2019', marker_color=TEXT_DIM, opacity=0.6
        ))
        fig5.add_trace(go.Bar(
            y=reg_sorted['governorate'], x=reg_sorted['hotel_capacity_pct_2023'],
            orientation='h', name='2023',
            marker=dict(
                color=reg_sorted['hotel_capacity_pct_2023'],
                colorscale=[[0, RED], [0.5, ORANGE], [1, GREEN]],
                showscale=False
            )
        ))
        apply_theme(fig5, height=460)
        fig5.update_layout(
            title_text="Occupancy Rate: 2019 vs 2023",
            barmode='overlay', xaxis_title="Occupancy (%)",
            legend=dict(x=0.6, y=0.05)
        )
        st.plotly_chart(fig5, use_container_width=True)

    insight("Djerba leads recovery with 88% occupancy in 2023, surpassing its pre-COVID level of 80%. "
            "Northern regions (Tabarka, Bizerte) remain chronically underutilized at under 50% — "
            "representing the largest untapped opportunity for year-round ecotourism development.")
