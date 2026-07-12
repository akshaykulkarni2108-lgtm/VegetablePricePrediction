import streamlit as st
from pathlib import Path

from utils.charts import load_dataset, plot_average_price_by_state, plot_top_commodities
from utils.ui_helpers import load_css, render_footer, render_header, render_metric_card

ROOT = Path(__file__).resolve().parents[1]

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
load_css()

df = load_dataset()

render_header(
    "Market Intelligence Dashboard",
    "Track the spread of vegetable prices across states, markets, and commodities.",
    "📊",
)

st.info("The dashboard highlights the most important market signals from the cleaned dataset without changing the trained model.")

cols = st.columns(4)
metrics = [
    ("Total Records", len(df), "Rows available in the dataset", "📦"),
    ("Total States", df["STATE"].nunique(), "Distinct states represented", "🗺️"),
    ("Total Markets", df["Market Name"].nunique(), "Trading locations covered", "🏪"),
    ("Total Vegetables", df["Commodity"].nunique(), "Unique vegetables tracked", "🥬"),
]
for col, (title, value, subtitle, icon) in zip(cols, metrics):
    render_metric_card(col, title, value, subtitle, icon)

chart_left, chart_right = st.columns(2)
with chart_left:
    st.plotly_chart(plot_top_commodities(df), use_container_width=True)
with chart_right:
    st.plotly_chart(plot_average_price_by_state(df), use_container_width=True)

st.markdown("<div class='panel-card'><h4 style='margin-top:0;color:#174d1c;'>Recent Dataset Preview</h4></div>", unsafe_allow_html=True)
st.dataframe(df.head(10), use_container_width=True)

render_footer()