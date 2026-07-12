import io
import streamlit as st
from pathlib import Path

from utils.charts import load_dataset
from utils.ui_helpers import load_css, render_footer, render_header

ROOT = Path(__file__).resolve().parents[1]

st.set_page_config(page_title="Data Analysis", page_icon="📋", layout="wide")
load_css()

df = load_dataset()

render_header(
    "Dataset Analysis",
    "Inspect the quality, structure, and completeness of the vegetation price dataset.",
    "📋",
)

st.success("A clean and structured view of the dataset helps validate the prediction pipeline and market patterns.")

tabs = st.tabs(["Dataset Preview", "Missing Values", "Statistics", "Dataset Information"])

with tabs[0]:
    st.markdown("<div class='panel-card'><h4 style='margin-top:0;color:#174d1c;'>Preview of the cleaned dataset</h4></div>", unsafe_allow_html=True)
    st.dataframe(df.head(15), use_container_width=True)

with tabs[1]:
    missing_values = df.isnull().sum().reset_index()
    missing_values.columns = ["Column", "Missing Count"]
    if missing_values["Missing Count"].sum() == 0:
        st.success("No missing values were found in the dataset.")
    else:
        st.warning("A few values are missing in the dataset. Review them before deeper analysis.")
    st.dataframe(missing_values, use_container_width=True)

with tabs[2]:
    st.markdown("<div class='panel-card'><h4 style='margin-top:0;color:#174d1c;'>Descriptive statistics</h4></div>", unsafe_allow_html=True)
    st.dataframe(df.describe(include="all").T, use_container_width=True)

with tabs[3]:
    buffer = io.StringIO()
    df.info(buf=buffer)
    info_text = buffer.getvalue()
    st.code(info_text)

render_footer()