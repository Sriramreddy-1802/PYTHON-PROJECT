import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as gg
import plotly.graph_objects as go
from generate_data import generate_health_camp_data

# ---------------------------------------------------------
# 1. Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Health Camp Coverage Analyzer",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------
# 2. Theme State Management
# ---------------------------------------------------------
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

def toggle_theme():
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"

IS_DARK = st.session_state.theme == "dark"

# Color constants based on theme
BG_COLOR = "#09090b" if IS_DARK else "#ffffff"
BG_SUBTLE = "#121215" if IS_DARK else "#f8fafc"
CARD_BG = "#16161a" if IS_DARK else "#ffffff"
CARD_HOVER = "#1d1d24" if IS_DARK else "#f1f5f9"
BORDER_COLOR = "#27272a" if IS_DARK else "#e2e8f0"
BORDER_SUBTLE = "#1e1e24" if IS_DARK else "#f1f5f9"
TEXT_COLOR = "#f4f4f5" if IS_DARK else "#0f172a"
TEXT_MUTED = "#94a3b8" if IS_DARK else "#64748b"
TEXT_DIM = "#64748b" if IS_DARK else "#94a3b8"
ACCENT_BLUE = "#3b82f6"
GREEN_COLOR = "#22c55e" if IS_DARK else "#16a34a"
GREEN_BG = "rgba(34,197,94,0.12)" if IS_DARK else "rgba(22,163,74,0.08)"
RED_COLOR = "#ef4444" if IS_DARK else "#dc2626"
RED_BG = "rgba(239,68,68,0.12)" if IS_DARK else "rgba(220,38,38,0.08)"
AMBER_COLOR = "#f59e0b" if IS_DARK else "#d97706"
AMBER_BG = "rgba(245,158,11,0.12)" if IS_DARK else "rgba(217,119,6,0.08)"

# ---------------------------------------------------------
# 3. Inject CSS Styles
# ---------------------------------------------------------
css = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Hide Streamlit Header & Chrome */
    header[data-testid="stHeader"], #MainMenu, footer, [data-testid="stToolbar"],
    [data-testid="stDecoration"], [data-testid="stStatusWidget"], .stDeployButton,
    div[data-testid="stSidebarCollapsedControl"] {{
        display: none !important;
    }}
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"], .main, .block-container, section[data-testid="stMain"] {{
        background-color: {BG_COLOR} !important;
        color: {TEXT_COLOR} !important;
        font-family: 'DM Sans', -apple-system, sans-serif !important;
    }}
    
    .block-container {{
        padding: 1.5rem 2rem 3rem !important;
        max-width: 1400px !important;
    }}
    
    /* Top Header Bar */
    .brand-bar {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding-bottom: 1.25rem;
        margin-bottom: 1rem;
        border-bottom: 1px solid {BORDER_COLOR};
    }}
    .brand-title {{
        font-size: 1.5rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        color: {TEXT_COLOR};
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }}
    .brand-badge {{
        font-size: 0.72rem;
        padding: 3px 10px;
        border-radius: 20px;
        background: {ACCENT_BLUE}22;
        color: {ACCENT_BLUE};
        border: 1px solid {ACCENT_BLUE}44;
        font-weight: 600;
        letter-spacing: 0.03em;
    }}
    .brand-subtitle {{
        font-size: 0.85rem;
        color: {TEXT_MUTED};
        margin-top: 2px;
    }}
    
    /* KPI Card Component */
    .metric-card {{
        background: {CARD_BG};
        border: 1px solid {BORDER_COLOR};
        border-radius: 12px;
        padding: 1.1rem 1.25rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        transition: transform 0.15s ease, border-color 0.15s ease;
    }}
    .metric-card:hover {{
        border-color: {ACCENT_BLUE}66;
    }}
    .metric-label {{
        font-size: 0.78rem;
        color: {TEXT_MUTED};
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }}
    .metric-value {{
        font-size: 1.75rem;
        font-weight: 700;
        color: {TEXT_COLOR};
        letter-spacing: -0.03em;
        margin: 0.2rem 0;
        font-family: 'JetBrains Mono', monospace;
    }}
    .metric-delta {{
        font-size: 0.75rem;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 6px;
        display: inline-flex;
        align-items: center;
        gap: 4px;
    }}
    .delta-up {{ color: {GREEN_COLOR}; background: {GREEN_BG}; }}
    .delta-down {{ color: {RED_COLOR}; background: {RED_BG}; }}
    .delta-warn {{ color: {AMBER_COLOR}; background: {AMBER_BG}; }}

    /* Filter Bar Box */
    .filter-box {{
        background: {CARD_BG};
        border: 1px solid {BORDER_COLOR};
        border-radius: 12px;
        padding: 1rem 1.25rem 0.5rem;
        margin-bottom: 1.5rem;
    }}
    
    /* Container Wrappers for Charts */
    .chart-wrap {{
        background: {CARD_BG};
        border: 1px solid {BORDER_COLOR};
        border-radius: 12px;
        padding: 1.1rem 1.25rem 0.8rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        height: 100%;
    }}
    .chart-header {{
        margin-bottom: 0.75rem;
    }}
    .chart-title {{
        font-size: 0.92rem;
        font-weight: 700;
        color: {TEXT_COLOR};
        letter-spacing: -0.01em;
    }}
    .chart-subtitle {{
        font-size: 0.75rem;
        color: {TEXT_MUTED};
        margin-top: 1px;
    }}

    /* Table Component */
    .table-container {{
        background: {CARD_BG};
        border: 1px solid {BORDER_COLOR};
        border-radius: 12px;
        overflow: hidden;
        margin-top: 1rem;
    }}
    .data-table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 0.82rem;
    }}
    .data-table th {{
        text-align: left;
        padding: 0.75rem 1rem;
        color: {TEXT_MUTED};
        font-weight: 600;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        background: {BG_SUBTLE};
        border-bottom: 1px solid {BORDER_COLOR};
    }}
    .data-table td {{
        padding: 0.7rem 1rem;
        color: {TEXT_COLOR};
        border-bottom: 1px solid {BORDER_SUBTLE};
    }}
    .data-table tr:last-child td {{
        border-bottom: none;
    }}
    .data-table tr:hover td {{
        background-color: {CARD_HOVER};
    }}
    
    /* Badges */
    .badge {{
        display: inline-block;
        padding: 3px 9px;
        border-radius: 6px;
        font-size: 0.72rem;
        font-weight: 600;
    }}
    .badge-green {{ color: {GREEN_COLOR}; background: {GREEN_BG}; border: 1px solid {GREEN_COLOR}33; }}
    .badge-amber {{ color: {AMBER_COLOR}; background: {AMBER_BG}; border: 1px solid {AMBER_COLOR}33; }}
    .badge-red {{ color: {RED_COLOR}; background: {RED_BG}; border: 1px solid {RED_COLOR}33; }}
    .badge-blue {{ color: {ACCENT_BLUE}; background: {ACCENT_BLUE}18; border: 1px solid {ACCENT_BLUE}33; }}

    /* Streamlit Tabs Customization */
    button[data-baseweb="tab"] {{
        background: transparent !important;
        color: {TEXT_MUTED} !important;
        font-size: 0.86rem !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.25rem !important;
        border: 1px solid transparent !important;
        border-radius: 8px !important;
    }}
    button[data-baseweb="tab"][aria-selected="true"] {{
        color: {TEXT_COLOR} !important;
        background: {CARD_BG} !important;
        border-color: {BORDER_COLOR} !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
    }}
    [data-baseweb="tab-highlight"], [data-baseweb="tab-border"] {{
        display: none !important;
    }}
    [data-baseweb="tab-list"] {{
        gap: 6px !important;
        background: {BG_SUBTLE} !important;
        border: 1px solid {BORDER_COLOR} !important;
        border-radius: 10px !important;
        padding: 4px !important;
        margin-bottom: 1.5rem !important;
    }}
    
    [data-testid="stHorizontalBlock"] {{
        gap: 1.2rem !important;
    }}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. Data Loading & Caching
# ---------------------------------------------------------
@st.cache_data
def load_data():
    data_file = os.path.join(os.path.dirname(__file__), "data", "health_camps.csv")
    if not os.path.exists(data_file):
        df = generate_health_camp_data()
        os.makedirs(os.path.dirname(data_file), exist_ok=True)
        df.to_csv(data_file, index=False)
    else:
        df = pd.read_csv(data_file)
    df["date"] = pd.to_datetime(df["date"])
    return df

raw_df = load_data()

# ---------------------------------------------------------
# 5. Header Bar & Theme Switcher
# ---------------------------------------------------------
head_col1, head_col2 = st.columns([8, 2])
with head_col1:
    st.markdown(f"""
    <div class="brand-bar" style="border-bottom:none; padding-bottom:0; margin-bottom:0;">
        <div>
            <div class="brand-title">
                🏥 Health Camp Coverage Analyzer
                <span class="brand-badge">PUBLIC HEALTH ANALYTICS</span>
            </div>
            <div class="brand-subtitle">
                Monitoring population coverage, clinical screening metrics, logistics, & healthcare equity across district health camps.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with head_col2:
    theme_btn_label = "☀️ Light Theme" if IS_DARK else "🌙 Dark Theme"
    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
    if st.button(theme_btn_label, use_container_width=True):
        toggle_theme()
        st.rerun()

st.markdown(f"<div style='border-bottom:1px solid {BORDER_COLOR}; margin: 0.75rem 0 1.25rem 0;'></div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 6. Global Interactive Filters Bar
# ---------------------------------------------------------
st.markdown(f"""
<div class="filter-box">
    <div style="font-size:0.75rem; font-weight:700; color:{TEXT_MUTED}; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:0.5rem;">
        🔍 Filter Analytics Cohort
    </div>
</div>
""", unsafe_allow_html=True)

f_col1, f_col2, f_col3, f_col4 = st.columns(4)

with f_col1:
    districts = ["All Districts"] + list(raw_df["district"].unique())
    selected_district = st.selectbox("District / Territory", districts)

with f_col2:
    camp_types = ["All Camp Types"] + list(raw_df["camp_type"].unique())
    selected_camp_type = st.selectbox("Health Camp Category", camp_types)

with f_col3:
    status_options = ["All Statuses"] + list(raw_df["coverage_status"].unique())
    selected_status = st.selectbox("Coverage Status Filter", status_options)

with f_col4:
    min_date = raw_df["date"].min().date()
    max_date = raw_df["date"].max().date()
    date_range = st.date_input("Date Range", value=[min_date, max_date], min_value=min_date, max_value=max_date)

# Apply Filter Logic
df_filtered = raw_df.copy()

if selected_district != "All Districts":
    df_filtered = df_filtered[df_filtered["district"] == selected_district]

if selected_camp_type != "All Camp Types":
    df_filtered = df_filtered[df_filtered["camp_type"] == selected_camp_type]

if selected_status != "All Statuses":
    df_filtered = df_filtered[df_filtered["coverage_status"] == selected_status]

if isinstance(date_range, list) or isinstance(date_range, tuple):
    if len(date_range) == 2:
        df_filtered = df_filtered[
            (df_filtered["date"].dt.date >= date_range[0]) & 
            (df_filtered["date"].dt.date <= date_range[1])
        ]

# ---------------------------------------------------------
# 7. Helper Component Functions
# ---------------------------------------------------------
def render_metric(label, value, delta=None, delta_type="up"):
    arrow = "↑" if delta_type == "up" else ("↓" if delta_type == "down" else "→")
    cls = f"delta-{delta_type}"
    delta_html = f'<div class="metric-delta {cls}">{arrow} {delta}</div>' if delta else ""
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans, sans-serif", color=TEXT_MUTED, size=11),
    margin=dict(l=10, r=10, t=25, b=10),
    xaxis=dict(
        gridcolor="rgba(255,255,255,0.05)" if IS_DARK else "rgba(0,0,0,0.06)",
        zerolinecolor="rgba(255,255,255,0.05)" if IS_DARK else "rgba(0,0,0,0.06)",
        tickfont=dict(size=10, color=TEXT_MUTED),
    ),
    yaxis=dict(
        gridcolor="rgba(255,255,255,0.05)" if IS_DARK else "rgba(0,0,0,0.06)",
        zerolinecolor="rgba(255,255,255,0.05)" if IS_DARK else "rgba(0,0,0,0.06)",
        tickfont=dict(size=10, color=TEXT_MUTED),
    ),
    legend=dict(
        font=dict(color=TEXT_MUTED, size=10),
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)

# ---------------------------------------------------------
# 8. Dashboard Navigation Tabs
# ---------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Executive Overview",
    "🩺 Clinical & Demographics",
    "🚑 Logistics & Cost Efficiency",
    "📋 Camp Directory & Data",
    "🔮 Coverage Scenario Simulator"
])

# =========================================================
# TAB 1: EXECUTIVE OVERVIEW
# =========================================================
with tab1:
    # Key Summary Metrics
    total_camps = len(df_filtered)
    total_target = df_filtered["target_population"].sum()
    total_screened = df_filtered["screened_patients"].sum()
    overall_cov = round((total_screened / max(1, total_target)) * 100, 1)
    critical_cases = df_filtered["critical_referrals"].sum()
    crit_rate = round((critical_cases / max(1, total_screened)) * 100, 1)
    avg_cost = round(df_filtered["cost_per_patient"].mean(), 2) if len(df_filtered) > 0 else 0
    
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        render_metric("Total Camps Conducted", f"{total_camps:,}", delta="+12% vs last cycle", delta_type="up")
    with k2:
        render_metric("Target Population", f"{total_target:,}", delta="Identified cohort", delta_type="warn")
    with k3:
        render_metric("Patients Screened", f"{total_screened:,}", delta=f"{overall_cov}% overall coverage", delta_type="up" if overall_cov >= 75 else "down")
    with k4:
        render_metric("Critical Referrals", f"{critical_cases:,}", delta=f"{crit_rate}% referral rate", delta_type="warn")
    with k5:
        render_metric("Avg Cost / Patient", f"${avg_cost:.2f}", delta="Optimal range", delta_type="up")
        
    st.markdown("<div style='height:15px;'></div>", unsafe_allow_html=True)
    
    # Map & Coverage Distribution Row
    col_map, col_dist = st.columns([6, 4])
    
    with col_map:
        st.markdown(f"""
        <div class="chart-wrap">
            <div class="chart-header">
                <div class="chart-title">Geospatial Health Camp Coverage Map</div>
                <div class="chart-subtitle">Circle size indicates patient volume screened; color represents target coverage achievement %</div>
            </div>
        """, unsafe_allow_html=True)
        
        if len(df_filtered) > 0:
            scatter_fn = getattr(px, "scatter_map", getattr(px, "scatter_mapbox", None))
            if scatter_fn:
                fig_map = scatter_fn(
                    df_filtered,
                    lat="latitude",
                    lon="longitude",
                    size="screened_patients",
                    color="coverage_pct",
                    color_continuous_scale=px.colors.diverging.RdYlGn,
                    range_color=[40, 100],
                    hover_name="camp_name",
                    hover_data={
                        "district": True,
                        "target_population": ":,",
                        "screened_patients": ":,",
                        "coverage_pct": ":.1f%",
                        "critical_referrals": ":,",
                        "latitude": False,
                        "longitude": False
                    },
                    zoom=8.8,
                    center={"lat": df_filtered["latitude"].mean(), "lon": df_filtered["longitude"].mean()},
                    height=420
                )
                map_style_key = "map_style" if hasattr(px, "scatter_map") else "mapbox_style"
                layout_kwargs = {
                    map_style_key: "carto-darkmatter" if IS_DARK else "carto-positron",
                    "paper_bgcolor": "rgba(0,0,0,0)",
                    "plot_bgcolor": "rgba(0,0,0,0)",
                    "margin": dict(l=0, r=0, t=0, b=0),
                    "coloraxis_colorbar": dict(
                        title=dict(text="Coverage %", font=dict(size=10, color=TEXT_MUTED)),
                        ticksuffix="%",
                        len=0.7,
                        thickness=12,
                        tickfont=dict(size=9, color=TEXT_MUTED)
                    )
                }
                fig_map.update_layout(**layout_kwargs)
                st.plotly_chart(fig_map, use_container_width=True, config={"displayModeBar": False})
            else:
                st.info("Map renderer unavailable.")
        else:
            st.info("No camp data available for selected filters.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_dist:
        st.markdown(f"""
        <div class="chart-wrap">
            <div class="chart-header">
                <div class="chart-title">District Population Coverage vs Target</div>
                <div class="chart-subtitle">Comparing screened population against target by district</div>
            </div>
        """, unsafe_allow_html=True)
        
        if len(df_filtered) > 0:
            dist_summary = df_filtered.groupby("district")[["target_population", "screened_patients"]].sum().reset_index()
            dist_summary["coverage_pct"] = (dist_summary["screened_patients"] / dist_summary["target_population"]) * 100
            dist_summary = dist_summary.sort_values("coverage_pct", ascending=True)
            
            fig_dist = go.Figure()
            fig_dist.add_trace(go.Bar(
                y=dist_summary["district"],
                x=dist_summary["screened_patients"],
                name="Screened",
                orientation='h',
                marker=dict(color=ACCENT_BLUE, cornerradius=4)
            ))
            fig_dist.add_trace(go.Bar(
                y=dist_summary["district"],
                x=dist_summary["target_population"] - dist_summary["screened_patients"],
                name="Unscreened Gap",
                orientation='h',
                marker=dict(color=RED_COLOR if IS_DARK else "#fca5a5", cornerradius=4)
            ))
            fig_dist.update_layout(
                barmode='stack',
                height=420,
                **PLOT_LAYOUT
            )
            st.plotly_chart(fig_dist, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No data to show.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.markdown("<div style='height:15px;'></div>", unsafe_allow_html=True)
    
    # Monthly Timeline Trend
    st.markdown(f"""
    <div class="chart-wrap">
        <div class="chart-header">
            <div class="chart-title">Monthly Screening Volume & Critical Referral Trends</div>
            <div class="chart-subtitle">Tracking outreach velocity and medical intervention triggers over time</div>
        </div>
    """, unsafe_allow_html=True)
    
    if len(df_filtered) > 0:
        df_filtered["year_month"] = df_filtered["date"].dt.to_period("M").astype(str)
        monthly_df = df_filtered.groupby("year_month")[["screened_patients", "critical_referrals", "target_population"]].sum().reset_index()
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Bar(
            x=monthly_df["year_month"],
            y=monthly_df["screened_patients"],
            name="Screened Patients",
            marker=dict(color=ACCENT_BLUE, cornerradius=5)
        ))
        fig_trend.add_trace(go.Scatter(
            x=monthly_df["year_month"],
            y=monthly_df["critical_referrals"],
            name="Critical Referrals",
            yaxis="y2",
            mode="lines+markers",
            line=dict(color=RED_COLOR, width=3),
            marker=dict(size=7, color=RED_COLOR)
        ))
        
        layout_trend = PLOT_LAYOUT.copy()
        layout_trend["yaxis2"] = dict(
            title=dict(text="Critical Cases", font=dict(color=RED_COLOR, size=10)),
            overlaying="y",
            side="right",
            gridcolor="rgba(0,0,0,0)",
            tickfont=dict(size=10, color=RED_COLOR)
        )
        layout_trend["height"] = 300
        
        fig_trend.update_layout(**layout_trend)
        st.plotly_chart(fig_trend, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# TAB 2: CLINICAL & DEMOGRAPHICS
# =========================================================
with tab2:
    if len(df_filtered) > 0:
        c_demo1, c_demo2, c_demo3 = st.columns([3, 4, 3])
        
        with c_demo1:
            st.markdown(f"""
            <div class="chart-wrap">
                <div class="chart-header">
                    <div class="chart-title">Gender Distribution</div>
                    <div class="chart-subtitle">Breakdown of beneficiaries screened</div>
                </div>
            """, unsafe_allow_html=True)
            
            male_total = df_filtered["male_screened"].sum()
            female_total = df_filtered["female_screened"].sum()
            
            fig_gender = px.pie(
                values=[male_total, female_total],
                names=["Male", "Female"],
                color_discrete_sequence=[ACCENT_BLUE, "#ec4899"],
                hole=0.55,
                height=300
            )
            fig_gender.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=10, t=10, b=10),
                legend=dict(font=dict(color=TEXT_MUTED), orientation="h", y=-0.1)
            )
            st.plotly_chart(fig_gender, use_container_width=True, config={"displayModeBar": False})
            st.markdown("</div>", unsafe_allow_html=True)
            
        with c_demo2:
            st.markdown(f"""
            <div class="chart-wrap">
                <div class="chart-header">
                    <div class="chart-title">Age Group Cohort Analysis</div>
                    <div class="chart-subtitle">Demographic age brackets across screened population</div>
                </div>
            """, unsafe_allow_html=True)
            
            u18 = df_filtered["under_18"].sum()
            a18_60 = df_filtered["age_18_60"].sum()
            a60 = df_filtered["above_60"].sum()
            
            age_df = pd.DataFrame({
                "Age Group": ["Under 18 yrs", "18 - 60 yrs", "Above 60 yrs"],
                "Count": [u18, a18_60, a60]
            })
            
            fig_age = px.bar(
                age_df,
                x="Age Group",
                y="Count",
                color="Age Group",
                color_discrete_sequence=["#38bdf8", "#818cf8", "#c084fc"],
                text_auto=',',
                height=300
            )
            fig_age.update_traces(marker=dict(cornerradius=6))
            fig_age.update_layout(showlegend=False, **PLOT_LAYOUT)
            st.plotly_chart(fig_age, use_container_width=True, config={"displayModeBar": False})
            st.markdown("</div>", unsafe_allow_html=True)
            
        with c_demo3:
            st.markdown(f"""
            <div class="chart-wrap">
                <div class="chart-header">
                    <div class="chart-title">Risk Stratification</div>
                    <div class="chart-subtitle">Patient risk categorization post-screening</div>
                </div>
            """, unsafe_allow_html=True)
            
            crit = df_filtered["critical_referrals"].sum()
            mod_risk = int(df_filtered["hypertension_cases"].sum() * 0.7 + df_filtered["diabetes_cases"].sum() * 0.6)
            normal = max(0, total_screened - crit - mod_risk)
            
            risk_df = pd.DataFrame({
                "Category": ["Low Risk / Normal", "Moderate Risk", "High Risk Referral"],
                "Patients": [normal, mod_risk, crit]
            })
            
            fig_risk = px.pie(
                risk_df,
                values="Patients",
                names="Category",
                color="Category",
                color_discrete_map={
                    "Low Risk / Normal": GREEN_COLOR,
                    "Moderate Risk": AMBER_COLOR,
                    "High Risk Referral": RED_COLOR
                },
                hole=0.55,
                height=300
            )
            fig_risk.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=10, t=10, b=10),
                legend=dict(font=dict(color=TEXT_MUTED), orientation="h", y=-0.1)
            )
            st.plotly_chart(fig_risk, use_container_width=True, config={"displayModeBar": False})
            st.markdown("</div>", unsafe_allow_html=True)
            
        st.markdown("<div style='height:15px;'></div>", unsafe_allow_html=True)
        
        # Clinical Screened Disease Prevalence
        st.markdown(f"""
        <div class="chart-wrap">
            <div class="chart-header">
                <div class="chart-title">Disease Prevalence & Screening Findings by Camp Type</div>
                <div class="chart-subtitle">Total cases detected per medical category</div>
            </div>
        """, unsafe_allow_html=True)
        
        disease_df = df_filtered.groupby("camp_type")[
            ["hypertension_cases", "diabetes_cases", "anemia_cases", "vision_defect_cases", "dental_issues"]
        ].sum().reset_index()
        
        fig_dis = go.Figure()
        fig_dis.add_trace(go.Bar(name="Hypertension", x=disease_df["camp_type"], y=disease_df["hypertension_cases"], marker_color="#ef4444"))
        fig_dis.add_trace(go.Bar(name="Diabetes", x=disease_df["camp_type"], y=disease_df["diabetes_cases"], marker_color="#f59e0b"))
        fig_dis.add_trace(go.Bar(name="Anemia", x=disease_df["camp_type"], y=disease_df["anemia_cases"], marker_color="#ec4899"))
        fig_dis.add_trace(go.Bar(name="Vision Defects", x=disease_df["camp_type"], y=disease_df["vision_defect_cases"], marker_color="#3b82f6"))
        fig_dis.add_trace(go.Bar(name="Dental Issues", x=disease_df["camp_type"], y=disease_df["dental_issues"], marker_color="#10b981"))
        
        fig_dis.update_layout(barmode="group", height=320, **PLOT_LAYOUT)
        st.plotly_chart(fig_dis, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# TAB 3: LOGISTICS & COST EFFICIENCY
# =========================================================
with tab3:
    if len(df_filtered) > 0:
        l_col1, l_col2 = st.columns(2)
        
        with l_col1:
            st.markdown(f"""
            <div class="chart-wrap">
                <div class="chart-header">
                    <div class="chart-title">Medical Personnel Deployment Ratio</div>
                    <div class="chart-subtitle">Average staff deployed per camp by organizer</div>
                </div>
            """, unsafe_allow_html=True)
            
            staff_df = df_filtered.groupby("organizer")[["doctors_deployed", "nurses_deployed", "chw_deployed"]].mean().reset_index()
            
            fig_staff = go.Figure()
            fig_staff.add_trace(go.Bar(x=staff_df["organizer"], y=staff_df["doctors_deployed"], name="Doctors", marker_color="#3b82f6"))
            fig_staff.add_trace(go.Bar(x=staff_df["organizer"], y=staff_df["nurses_deployed"], name="Nurses", marker_color="#8b5cf6"))
            fig_staff.add_trace(go.Bar(x=staff_df["organizer"], y=staff_df["chw_deployed"], name="CHWs", marker_color="#06b6d4"))
            
            fig_staff.update_layout(barmode="stack", height=330, **PLOT_LAYOUT)
            st.plotly_chart(fig_staff, use_container_width=True, config={"displayModeBar": False})
            st.markdown("</div>", unsafe_allow_html=True)
            
        with l_col2:
            st.markdown(f"""
            <div class="chart-wrap">
                <div class="chart-header">
                    <div class="chart-title">Cost per Patient Screened ($) by District</div>
                    <div class="chart-subtitle">Evaluating budget utilization efficiency across regions</div>
                </div>
            """, unsafe_allow_html=True)
            
            cost_df = df_filtered.groupby("district")["cost_per_patient"].mean().reset_index()
            cost_df = cost_df.sort_values("cost_per_patient", ascending=False)
            
            fig_cost = px.bar(
                cost_df,
                x="district",
                y="cost_per_patient",
                color="cost_per_patient",
                color_continuous_scale="Blues",
                text_auto='.2f',
                height=330
            )
            fig_cost.update_layout(coloraxis_showscale=False, **PLOT_LAYOUT)
            fig_cost.update_traces(marker=dict(cornerradius=6))
            st.plotly_chart(fig_cost, use_container_width=True, config={"displayModeBar": False})
            st.markdown("</div>", unsafe_allow_html=True)
            
        st.markdown("<div style='height:15px;'></div>", unsafe_allow_html=True)
        
        # Budget vs Coverage Efficiency Scatter Plot
        st.markdown(f"""
        <div class="chart-wrap">
            <div class="chart-header">
                <div class="chart-title">Budget Allocation vs Patient Coverage Efficiency</div>
                <div class="chart-subtitle">Quadrant analysis: Top-right represents high budget, high coverage performance</div>
            </div>
        """, unsafe_allow_html=True)
        
        fig_scatter = px.scatter(
            df_filtered,
            x="budget_usd",
            y="coverage_pct",
            size="screened_patients",
            color="camp_type",
            hover_name="camp_name",
            hover_data=["district", "cost_per_patient", "doctors_deployed"],
            height=340
        )
        fig_scatter.update_layout(**PLOT_LAYOUT)
        st.plotly_chart(fig_scatter, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# TAB 4: CAMP DIRECTORY & DATA EXPLORER
# =========================================================
with tab4:
    st.markdown(f"""
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem;">
        <div>
            <span style="font-weight:700; font-size:1rem; color:{TEXT_COLOR};">Health Camp Performance Ledger</span>
            <span style="font-size:0.8rem; color:{TEXT_MUTED}; margin-left:0.5rem;">({len(df_filtered)} records matching criteria)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Search input
    search_query = st.text_input("🔎 Search Camp Name or ID", placeholder="Type camp name or ID (e.g. CMP-1005)...")
    
    table_df = df_filtered.copy()
    if search_query:
        table_df = table_df[
            table_df["camp_name"].str.contains(search_query, case=False, na=False) |
            table_df["camp_id"].str.contains(search_query, case=False, na=False)
        ]
    
    # Render styled HTML Table
    rows_html = ""
    for idx, row in table_df.head(25).iterrows():
        status_cls = "badge-green" if row["coverage_pct"] >= 90 else ("badge-blue" if row["coverage_pct"] >= 75 else ("badge-amber" if row["coverage_pct"] >= 55 else "badge-red"))
        date_str = row["date"].strftime("%b %d, %Y")
        
        rows_html += f"""
        <tr>
            <td><strong style="font-family:'JetBrains Mono';">{row['camp_id']}</strong></td>
            <td><strong>{row['camp_name']}</strong><br><span style="font-size:0.72rem; color:{TEXT_MUTED};">{row['organizer']}</span></td>
            <td>{row['district']}</td>
            <td>{row['camp_type']}</td>
            <td>{date_str}</td>
            <td style="font-family:'JetBrains Mono';">{row['target_population']:,}</td>
            <td style="font-family:'JetBrains Mono';">{row['screened_patients']:,}</td>
            <td><span class="badge {status_cls}">{row['coverage_pct']:.1f}% ({row['coverage_status']})</span></td>
            <td style="color:{RED_COLOR}; font-weight:600; font-family:'JetBrains Mono';">{row['critical_referrals']}</td>
            <td style="font-family:'JetBrains Mono';">${row['cost_per_patient']:.2f}</td>
        </tr>
        """
        
    st.markdown(f"""
    <div class="table-container">
        <table class="data-table">
            <thead>
                <tr>
                    <th>Camp ID</th>
                    <th>Camp Name & Organizer</th>
                    <th>District</th>
                    <th>Category</th>
                    <th>Date</th>
                    <th>Target Pop</th>
                    <th>Screened</th>
                    <th>Coverage Status</th>
                    <th>Critical Referrals</th>
                    <th>Cost/Patient</th>
                </tr>
            </thead>
            <tbody>
                {rows_html if rows_html else f"<tr><td colspan='10' style='text-align:center;'>No matching camps found.</td></tr>"}
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='height:15px;'></div>", unsafe_allow_html=True)
    
    # Download CSV button
    csv_data = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Export Filtered Health Camp Dataset (CSV)",
        data=csv_data,
        file_name="health_camp_coverage_data.csv",
        mime="text/csv"
    )


# =========================================================
# TAB 5: COVERAGE SCENARIO SIMULATOR
# =========================================================
with tab5:
    st.markdown(f"""
    <div class="chart-wrap" style="margin-bottom:1.5rem;">
        <div class="chart-header">
            <div class="chart-title">🔮 What-If Health Camp Resource & Coverage Simulator</div>
            <div class="chart-subtitle">Simulate how scaling doctors, community health workers, and budget allocation impacts projected screening coverage</div>
        </div>
    """, unsafe_allow_html=True)
    
    sim_col1, sim_col2 = st.columns([4, 6])
    
    with sim_col1:
        st.subheader("Simulation Inputs")
        
        target_dist = st.selectbox("Select Target District for Simulation", list(raw_df["district"].unique()))
        
        dist_base = raw_df[raw_df["district"] == target_dist]
        current_avg_doctors = int(dist_base["doctors_deployed"].mean())
        current_avg_chw = int(dist_base["chw_deployed"].mean())
        current_avg_budget = int(dist_base["budget_usd"].mean())
        current_coverage = dist_base["coverage_pct"].mean()
        
        add_doctors = st.slider("Additional Doctors per Camp", 0, 10, 2)
        add_chw = st.slider("Additional Community Health Workers (CHWs)", 0, 25, 5)
        budget_increase_pct = st.slider("Budget Increase %", 0, 100, 20)
        
        # Simulation Logic
        sim_doctor_boost = add_doctors * 3.5
        sim_chw_boost = add_chw * 1.8
        sim_budget_boost = budget_increase_pct * 0.25
        
        projected_coverage = min(98.5, current_coverage + sim_doctor_boost + sim_chw_boost + sim_budget_boost)
        projected_screened = int(dist_base["target_population"].sum() * (projected_coverage / 100))
        current_screened = dist_base["screened_patients"].sum()
        additional_patients = projected_screened - current_screened
        
    with sim_col2:
        st.subheader("Simulation Results & Impact Projection")
        
        r1, r2, r3 = st.columns(3)
        with r1:
            render_metric("Current Coverage %", f"{current_coverage:.1f}%")
        with r2:
            render_metric("Projected Coverage %", f"{projected_coverage:.1f}%", delta=f"+{projected_coverage - current_coverage:.1f}% gain", delta_type="up")
        with r3:
            render_metric("Additional Screenings", f"+{additional_patients:,}", delta="Patients reached", delta_type="up")
            
        st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
        
        # Comparison Bar Chart
        sim_comp_df = pd.DataFrame({
            "Scenario": ["Current Baseline", "Projected Simulation"],
            "Coverage %": [current_coverage, projected_coverage],
            "Total Patients Screened": [current_screened, projected_screened]
        })
        
        fig_sim = px.bar(
            sim_comp_df,
            x="Scenario",
            y="Coverage %",
            color="Scenario",
            color_discrete_sequence=[TEXT_MUTED, GREEN_COLOR],
            text_auto='.1f%',
            height=280
        )
        fig_sim.update_layout(showlegend=False, **PLOT_LAYOUT)
        fig_sim.update_traces(marker=dict(cornerradius=6))
        st.plotly_chart(fig_sim, use_container_width=True, config={"displayModeBar": False})
        
    st.markdown("</div>", unsafe_allow_html=True)
