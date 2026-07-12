import pandas as pd

import streamlit as st
from pathlib import Path

from utils.charts import load_dataset, plot_average_price_by_state, plot_top_commodities
from utils.ui_helpers import load_css, render_footer, render_header, render_metric_card

ROOT = Path(__file__).resolve().parent

st.set_page_config(
    page_title="AgriPrice AI",
    page_icon="🥕",
    layout="wide",
)

load_css()

df = load_dataset()
variety_df = pd.read_excel(ROOT / "data" / "commodity_variety_grade_dataset.xlsx")

st.sidebar.image(str(ROOT / "images" / "agri_logo.svg"), use_container_width=True)
st.sidebar.markdown(
    """
    <div class="sidebar-brand">
        <h3>AgriPrice AI</h3>
        <p>Smart vegetable market intelligence</p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")
st.sidebar.markdown(
    "<div class='info-banner'>The existing Random Forest workflow remains unchanged while the experience is upgraded for a premium dashboard presentation.</div>",
    unsafe_allow_html=True,
)

render_header(
    "Vegetable Price Prediction Dashboard",
    "A premium AI-powered agriculture forecasting experience for modern project presentations.",
    "🥕",
)

st.markdown(
    "<div class='info-banner'>The platform combines historical market data with a trained Random Forest model to deliver fast and reliable price forecasts.</div>",
    unsafe_allow_html=True,
)

col_a, col_b = st.columns([1.2, 0.8])
with col_a:
    st.markdown(
        """
        <div class="panel-card">
            <h4 style="margin-top:0; color:#f8fafc;">What this dashboard offers</h4>
            <p style="color:#cbd5e1;">Explore historical trends, inspect the dataset, uncover market patterns, and predict vegetable prices through a polished and responsive interface.</p>
            <ul style="color:#cbd5e1; line-height:1.7;">
                <li>Dark premium SaaS-style dashboard</li>
                <li>Interactive Plotly visualizations</li>
                <li>Responsive KPI summaries</li>
                <li>Clean prediction workflow</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col_b:
    st.image(str(ROOT / "images" / "vegetable_banner.svg"), use_container_width=True)

cols = st.columns(4)
metrics = [
    ("Total Records", len(df), "Rows in the cleaned dataset", "📦"),
    ("Total States", df["STATE"].nunique(), "Distinct states covered", "🗺️"),
    ("Total Markets", df["Market Name"].nunique(), "Active trading markets", "🏪"),
    ("Total Vegetables", df["Commodity"].nunique(), "Unique vegetables tracked", "🥬"),
]
for col, (title, value, subtitle, icon) in zip(cols, metrics):
    render_metric_card(col, title, value, subtitle, icon)

chart_col_1, chart_col_2 = st.columns(2)
with chart_col_1:
    st.plotly_chart(plot_top_commodities(df), use_container_width=True)
with chart_col_2:
    st.plotly_chart(plot_average_price_by_state(df), use_container_width=True)

render_footer()