import streamlit as st
from pathlib import Path

from utils.charts import load_dataset, plot_average_price_by_state, plot_top_commodities
from utils.ui_helpers import load_css, render_footer, render_header, render_metric_card, render_status_banner

ROOT = Path(__file__).resolve().parents[1]

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
load_css()

df = load_dataset()

render_header(
    "Market Intelligence Dashboard",
    "Track the spread of vegetable prices across states, markets, and commodities with a premium analytics view.",
    "📊",
)

render_status_banner(
    "Signal overview",
    "The dashboard highlights the most important market signals from the cleaned dataset without changing the trained model.",
    "info",
)

metrics = [
    ("Total Records", f"{len(df):,}", "Rows available in the dataset", "📦"),
    ("Total States", df["STATE"].nunique(), "Distinct states represented", "🗺️"),
    ("Total Markets", df["Market Name"].nunique(), "Trading locations covered", "🏪"),
    ("Total Vegetables", df["Commodity"].nunique(), "Unique vegetables tracked", "🥬"),
]

metric_cols = st.columns(4)
for index, (title, value, subtitle, icon) in enumerate(metrics):
    render_metric_card(metric_cols[index % 4], title, value, subtitle, icon)

st.markdown("<div class='section-label'>Performance Overview</div>", unsafe_allow_html=True)
chart_left, chart_right = st.columns(2)
with chart_left:
    st.markdown("<div class='glass-card'><h4>Commodity frequency</h4><p>Understand which vegetables appear most often in the historical records.</p></div>", unsafe_allow_html=True)
    st.plotly_chart(plot_top_commodities(df), use_container_width=True)
with chart_right:
    st.markdown("<div class='glass-card'><h4>Regional pricing</h4><p>Compare average modal prices across states with a refined visual layout.</p></div>", unsafe_allow_html=True)
    st.plotly_chart(plot_average_price_by_state(df), use_container_width=True)

st.markdown("<div class='section-label'>Recent Records</div>", unsafe_allow_html=True)
st.markdown("<div class='table-card'><div class='glass-card' style='margin-bottom:0;padding:0;border:none;box-shadow:none;background:transparent;'><h4 style='margin-top:0;'>Dataset preview</h4><p style='margin-bottom:0;'>A compact view of the latest market records for presentation and review.</p></div></div>", unsafe_allow_html=True)
st.dataframe(df.head(10), use_container_width=True)

render_footer()