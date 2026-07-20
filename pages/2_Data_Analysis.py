import io
import streamlit as st
from pathlib import Path

from utils.charts import load_dataset
from utils.ui_helpers import load_css, render_footer, render_header, render_status_banner

ROOT = Path(__file__).resolve().parents[1]

st.set_page_config(page_title="Data Analysis", page_icon="📋", layout="wide")
load_css()

df = load_dataset()

render_header(
    "Dataset Analysis",
    "Inspect the quality, structure, and completeness of the vegetation price dataset through a refined analytical workspace.",
    "📋",
)

render_status_banner(
    "Clean data, clearer insight",
    "A structured view of the dataset helps validate the prediction pipeline and market patterns without impacting the underlying workflow.",
    "success",
)

tabs = st.tabs(["Dataset Preview", "Missing Values", "Statistics", "Dataset Information"])

with tabs[0]:
    st.markdown("<div class='glass-card'><h4 style='margin-top:0;'>Preview of the cleaned dataset</h4><p style='margin-bottom:0;'>A polished snapshot of the latest market observations.</p></div>", unsafe_allow_html=True)
    st.dataframe(df.head(15), use_container_width=True)

with tabs[1]:
    missing_values = df.isnull().sum().reset_index()
    missing_values.columns = ["Column", "Missing Count"]
    if missing_values["Missing Count"].sum() == 0:
        st.markdown("<div class='status-banner status-banner--success'><div class='status-title'>No missing values</div><div class='status-copy'>The dataset is complete for the monitored fields.</div></div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='status-banner status-banner--warning'><div class='status-title'>Missing values detected</div><div class='status-copy'>A few values are missing in the dataset. Review them before deeper analysis.</div></div>", unsafe_allow_html=True)
    st.dataframe(missing_values, use_container_width=True)

with tabs[2]:
    st.markdown("<div class='glass-card'><h4 style='margin-top:0;'>Descriptive statistics</h4><p style='margin-bottom:0;'>Quick numeric summaries for a fast review of the market dataset.</p></div>", unsafe_allow_html=True)
    st.dataframe(df.describe(include="all").T, use_container_width=True)

with tabs[3]:
    st.markdown("<div class='glass-card'><h4 style='margin-top:0;'>Dataset information</h4><p style='margin-bottom:0;'>A technical snapshot of the dataframe schema and column-level characteristics.</p></div>", unsafe_allow_html=True)
    buffer = io.StringIO()
    df.info(buf=buffer)
    info_text = buffer.getvalue()
    st.text(info_text)

render_footer()