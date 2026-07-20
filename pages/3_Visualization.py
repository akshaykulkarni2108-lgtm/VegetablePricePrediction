import streamlit as st
from utils.charts import load_dataset, plot_average_price_by_state, plot_top_commodities
from utils.ui_helpers import load_css, render_footer, render_header, render_status_banner

st.set_page_config(page_title="Visualization", page_icon="📈", layout="wide")
load_css()

df = load_dataset()

render_header(
    "Interactive Market Visualizations",
    "View vegetable demand and average price behavior through modern Plotly charts with a polished presentation layer.",
    "📈",
)

render_status_banner(
    "Visual storytelling",
    "These visuals are designed to make the agricultural data easier to interpret and present without changing any underlying plotting logic.",
    "info",
)

left, right = st.columns(2)
with left:
    st.markdown("<div class='glass-card'><h4>Commodity frequency</h4><p>Track the volume of each vegetable across the cleaned dataset.</p></div>", unsafe_allow_html=True)
    st.plotly_chart(plot_top_commodities(df), use_container_width=True)
with right:
    st.markdown("<div class='glass-card'><h4>State-wise pricing</h4><p>Compare regional modal prices through a refined visual summary.</p></div>", unsafe_allow_html=True)
    st.plotly_chart(plot_average_price_by_state(df), use_container_width=True)

render_footer()