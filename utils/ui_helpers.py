import base64
from pathlib import Path

import streamlit as st


ROOT = Path(__file__).resolve().parents[1]


def load_css():
    css_path = ROOT / "styles" / "main.css"
    with css_path.open("r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def get_local_image_base64(image_path: str) -> str:
    path = ROOT / image_path
    with path.open("rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    return encoded


def render_header(title: str, subtitle: str, emoji: str = "🌿"):
    st.markdown(
        f"""
        <div class="hero-card">
            <div class="hero-badge">{emoji}</div>
            <div>
                <h2 style="margin:0; color:#f8fafc;">{title}</h2>
                <p style="margin:0.25rem 0 0; color:#cbd5e1;">{subtitle}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric_card(column, title: str, value, subtitle: str, icon: str):
    column.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-icon">{icon}</div>
            <div class="metric-subtitle">{title}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer():
    st.markdown(
        """
        <div class="footer-card">
            <div><strong>Project Name:</strong> Vegetable Price Prediction</div>
            <div><strong>ML Algorithm:</strong> Random Forest Regressor</div>
            <div><strong>Developer:</strong> Akshay Kulkarni</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
