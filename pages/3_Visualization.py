import streamlit as st
from utils.charts import load_dataset, plot_average_price_by_state, plot_top_commodities
from utils.ui_helpers import load_css, render_footer, render_header

st.set_page_config(page_title="Visualization", page_icon="📈", layout="wide")
load_css()

df = load_dataset()

render_header(
    "Interactive Market Visualizations",
    "View vegetable demand and average price behavior through modern Plotly charts.",
    "📈",
)

st.info("These visuals are designed to make the agricultural data easier to interpret and present.")

left, right = st.columns(2)
with left:
    st.plotly_chart(plot_top_commodities(df), use_container_width=True)
with right:
    st.plotly_chart(plot_average_price_by_state(df), use_container_width=True)

render_footer()