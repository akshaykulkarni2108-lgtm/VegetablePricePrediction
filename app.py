import pandas as pd
import streamlit as st
from pathlib import Path

from utils.charts import load_dataset, plot_average_price_by_state, plot_top_commodities
from utils.ui_helpers import load_css, render_footer, render_header, render_metric_card, render_status_banner

ROOT = Path(__file__).resolve().parent

st.set_page_config(
    page_title="AgriPrice AI",
    page_icon="🥕",
    layout="wide",
)

load_css()

df = load_dataset()

st.sidebar.markdown(
    f"""
    <div class="sidebar-brand">
        <div class="sidebar-logo">🥕</div>
        <div>
            <div class="sidebar-title">AgriPrice AI</div>
            <div class="sidebar-copy">Premium market intelligence</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

render_header(
    "Vegetable Price Prediction",
    "AI-powered agricultural market intelligence for modern forecasting and portfolio-ready presentations.",
    "🥕",
)

st.markdown(
    """
    <div class="hero-shell">
        <div class="hero-copy">
            <div class="section-label">AI SaaS Dashboard</div>
            <h2>From raw market signals to polished forecasts in seconds.</h2>
            <p>Explore historical trends, inspect market context, and generate predictions with the same trained Random Forest workflow preserved beneath the new experience.</p>
            <div class="hero-actions">
                <span class="hero-pill">Glassmorphism UI</span>
                <span class="hero-pill">Theme aware charts</span>
                <span class="hero-pill">Responsive by design</span>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

render_status_banner(
    "Live intelligence",
    "The interface now feels like a premium AI product while the existing machine learning workflow stays unchanged.",
    "info",
)

metrics = [
    ("Dataset Size", f"{len(df):,}", "Rows across the cleaned dataset", "📦"),
    ("States", df["STATE"].nunique(), "Coverage across regions", "🗺️"),
    ("Markets", df["Market Name"].nunique(), "Trading hubs tracked", "🏪"),
    ("Commodities", df["Commodity"].nunique(), "Vegetables monitored", "🥬"),
    ("Prediction Count", f"{len(df):,}", "Ready for live forecasting", "⚡"),
    ("Highest Price", f"₹ {df['Modal_Price'].max():,.2f}", "Peak market signal", "📈"),
    ("Lowest Price", f"₹ {df['Modal_Price'].min():,.2f}", "Minimum observed price", "📉"),
    ("Average Price", f"₹ {df['Modal_Price'].mean():,.2f}", "Typical modal price", "🧠"),
]

metric_cols = st.columns(4)
for index, (title, value, subtitle, icon) in enumerate(metrics):
    col = metric_cols[index % 4]
    render_metric_card(col, title, value, subtitle, icon)

st.markdown("<div class='section-label'>Performance Overview</div>", unsafe_allow_html=True)
chart_col_1, chart_col_2 = st.columns(2)
with chart_col_1:
    st.markdown("<div class='glass-card'><h4>Market volume</h4><p>See which commodities appear most commonly across the dataset.</p></div>", unsafe_allow_html=True)
    st.plotly_chart(plot_top_commodities(df), use_container_width=True)
with chart_col_2:
    st.markdown("<div class='glass-card'><h4>Regional pricing</h4><p>Compare average modal prices across states with a polished visual summary.</p></div>", unsafe_allow_html=True)
    st.plotly_chart(plot_average_price_by_state(df), use_container_width=True)

render_footer()