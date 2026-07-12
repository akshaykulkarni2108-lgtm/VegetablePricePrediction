import streamlit as st
from pathlib import Path

from utils.ui_helpers import load_css, render_footer, render_header

ROOT = Path(__file__).resolve().parents[1]

st.set_page_config(page_title="About", page_icon="ℹ", layout="wide")
load_css()

render_header(
    "About the Project",
    "A smart agriculture dashboard combining machine learning and an elegant user experience.",
    "ℹ",
)

st.markdown(
    """
    <div class="panel-card">
        <h4 style="margin-top:0; color:#174d1c;">Vegetable Price Prediction System</h4>
        <p style="color:#4b634b;">This project uses a Random Forest Regressor to forecast vegetable prices from historical market data. The interface is designed to make the project feel polished, accessible, and presentation-ready for academic and portfolio use.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)
with col1:
    st.markdown(
        """
        <div class="panel-card">
            <h5 style="margin-top:0; color:#174d1c;">Project Highlights</h5>
            <ul style="color:#4b634b; line-height:1.7;">
                <li>Random Forest Regression for price forecasting</li>
                <li>Cleaned market dataset with categorical encoding</li>
                <li>Responsive and attractive Streamlit UI</li>
                <li>Interactive charts for better insight</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col2:
    st.image(str(ROOT / "images" / "vegetable_hero.svg"), use_container_width=True)

st.markdown(
    """
    <div class="panel-card">
        <h5 style="margin-top:0; color:#174d1c;">Technical Stack</h5>
        <p style="color:#4b634b; margin-bottom:0;">Python • Streamlit • Pandas • Plotly • Scikit-learn • Joblib</p>
    </div>
    """,
    unsafe_allow_html=True,
)

render_footer()