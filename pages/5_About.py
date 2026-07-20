import streamlit as st
from pathlib import Path

from utils.ui_helpers import load_css, render_footer, render_header, render_status_banner

ROOT = Path(__file__).resolve().parents[1]

st.set_page_config(page_title="About", page_icon="ℹ", layout="wide")
load_css()

render_header(
    "About the Project",
    "A smart agriculture dashboard combining machine learning and an elegant user experience for impressive presentations.",
    "ℹ",
)

render_status_banner(
    "Portfolio-ready product",
    "This project uses a Random Forest Regressor to forecast vegetable prices from historical market data, delivered through a polished and responsive interface.",
    "info",
)

left_col, right_col = st.columns([1.1, 0.9], gap="large")
with left_col:
    st.markdown(
        """
        <div class='glass-card'>
            <h4 style='margin-top:0;'>Project highlights</h4>
            <ul style='margin:0.5rem 0 0;padding-left:1rem;line-height:1.7;'>
                <li>Random Forest Regression for price forecasting</li>
                <li>Cleaned market dataset with categorical encoding</li>
                <li>Responsive and premium Streamlit UI</li>
                <li>Interactive charts and modern storytelling</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
with right_col:
    st.markdown(
        """
        <div class='glass-card'>
            <h4 style='margin-top:0;'>Technical stack</h4>
            <p style='margin:0.35rem 0 0;'>Python • Streamlit • Pandas • Plotly • Scikit-learn • Joblib</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div class='glass-card'><h4 style='margin-top:0;'>Experience focus</h4><p style='margin-bottom:0;'>The redesign centers on a premium AI SaaS feel while leaving the model, preprocessing, and prediction logic intact.</p></div>", unsafe_allow_html=True)

st.image(str(ROOT / "images" / "vegetable_hero.svg"), use_container_width=True)

render_footer()