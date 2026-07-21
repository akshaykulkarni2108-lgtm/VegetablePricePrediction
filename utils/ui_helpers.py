import base64
from pathlib import Path

import streamlit as st


ROOT = Path(__file__).resolve().parents[1]


def load_css() -> None:
    
    

    css_path = ROOT / "styles" / "main.css"
    with css_path.open("r", encoding="utf-8") as f:
        css = f.read()

    st.markdown(
        f"""
        <style>
        :root {{
            --app-background: #0B1220;
            --app-background-secondary: #161F33;
            --sidebar-background: rgba(6, 12, 26, 0.92);
            --glass-background: #161F33;
            --border: rgba(255,255,255,0.12);
            --text: #F8FAFC;
            --muted: #94A3B8;
            --primary: #22C55E;
            --accent: #F59E0B;
            --shadow: 0 18px 55px rgba(2, 8, 23, 0.42);
            --shadow-strong: 0 24px 70px rgba(2, 8, 23, 0.56);
            --input-background: rgba(8, 15, 33, 0.88);
            --gradient: linear-gradient(135deg, #22C55E 0%, #F59E0B 100%);
            --ambient-glow: rgba(34, 197, 94, 0.16);
            --ambient-soft: rgba(245, 158, 11, 0.16);
            --glass-blur: 22px;
        }}
        {css}
        </style>
        """,
        unsafe_allow_html=True,
    )


def get_local_image_base64(image_path: str) -> str:
    path = ROOT / image_path
    with path.open("rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    return encoded


def render_header(title: str, subtitle: str, emoji: str = "🌿"):
    st.markdown(
        f"""
        <div class="hero-shell">
            <div class="hero-badge">{emoji}</div>
            <div class="hero-copy">
                <div class="section-label">Premium Intelligence</div>
                <h2>{title}</h2>
                <p>{subtitle}</p>
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
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_status_banner(title: str, message: str, tone: str = "info"):
    st.markdown(
        f"""
        <div class="status-banner status-banner--{tone}">
            <div class="status-title">{title}</div>
            <div class="status-copy">{message}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer():
    st.markdown(
        """
        <div class="footer-card">
            <div><strong>Project:</strong> Vegetable Price Prediction</div>
            <div><strong>ML Model:</strong> Random Forest Regressor</div>
            <div><strong>Developer:</strong> Akshay Kulkarni</div>
            <div><strong>Version:</strong> Phase 1 • Premium UI</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
