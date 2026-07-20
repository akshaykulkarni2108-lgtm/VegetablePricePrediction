import base64
from pathlib import Path
from typing import Literal, TypedDict, cast

import streamlit as st


ROOT = Path(__file__).resolve().parents[1]

ThemeMode = Literal["dark", "light", "auto"]


class ThemePalette(TypedDict):
    bg: str
    bg_secondary: str
    sidebar: str
    glass: str
    border: str
    text: str
    muted: str
    primary: str
    accent: str
    shadow: str
    shadow_strong: str
    input: str
    gradient: str
    ambient: str
    ambient_soft: str


THEME_OPTIONS: tuple[ThemeMode, ...] = ("dark", "light", "auto")


def _theme_label(mode: ThemeMode) -> str:
    labels = {
        "dark": "🌙 Dark Mode",
        "light": "☀️ Light Mode",
        "auto": "🖥️ Auto",
    }
    return labels[mode]


def _initialize_theme_mode() -> ThemeMode:
    if "theme_mode" not in st.session_state:
        st.session_state.theme_mode = "auto"

    theme_mode = st.session_state.theme_mode
    if theme_mode not in THEME_OPTIONS:
        st.session_state.theme_mode = "auto"
        return "auto"

    return cast(ThemeMode, theme_mode)


def _resolve_theme_mode(theme_mode: ThemeMode) -> ThemeMode:
    if theme_mode != "auto":
        return theme_mode

    try:
        configured = st.get_option("theme.base")
    except Exception:
        configured = None

    if configured in {"dark", "night"}:
        return "dark"
    if configured in {"light", "default"}:
        return "light"

    return "dark"


def _get_palette(theme_mode: ThemeMode) -> ThemePalette:
    resolved_theme = _resolve_theme_mode(theme_mode)
    if resolved_theme == "light":
        return {
            "bg": "#f5f7fb",
            "bg_secondary": "#edf2f8",
            "sidebar": "rgba(255,255,255,0.82)",
            "glass": "rgba(255,255,255,0.76)",
            "border": "rgba(15, 23, 42, 0.1)",
            "text": "#0f172a",
            "muted": "#475569",
            "primary": "#16a34a",
            "accent": "#f59e0b",
            "shadow": "0 18px 55px rgba(15, 23, 42, 0.12)",
            "shadow_strong": "0 24px 70px rgba(15, 23, 42, 0.18)",
            "input": "rgba(255,255,255,0.96)",
            "gradient": "linear-gradient(135deg, #16a34a 0%, #f59e0b 100%)",
            "ambient": "rgba(22, 163, 74, 0.16)",
            "ambient_soft": "rgba(245, 158, 11, 0.16)",
        }

    return {
        "bg": "#040816",
        "bg_secondary": "#071120",
        "sidebar": "rgba(4, 8, 22, 0.82)",
        "glass": "rgba(255,255,255,0.08)",
        "border": "rgba(255,255,255,0.14)",
        "text": "#f8fafc",
        "muted": "#dbe4f0",
        "primary": "#34d399",
        "accent": "#fbbf24",
        "shadow": "0 18px 55px rgba(2, 8, 23, 0.42)",
        "shadow_strong": "0 24px 70px rgba(2, 8, 23, 0.56)",
        "input": "rgba(8, 15, 33, 0.8)",
        "gradient": "linear-gradient(135deg, #34d399 0%, #f59e0b 100%)",
        "ambient": "rgba(52, 211, 153, 0.18)",
        "ambient_soft": "rgba(251, 191, 36, 0.18)",
    }


def render_theme_controls() -> None:
    st.sidebar.markdown(
        """
        <div class="sidebar-card">
            <div class="section-label">Appearance</div>
            <div class="sidebar-title">Theme</div>
            <div class="sidebar-copy">Switch instantly and keep your preference for this session.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    current_theme = _initialize_theme_mode()
    theme_mode = st.sidebar.radio(
        "Theme",
        options=list(THEME_OPTIONS),
        index=list(THEME_OPTIONS).index(current_theme),
        key="theme_mode",
        horizontal=False,
        label_visibility="collapsed",
        format_func=_theme_label,
    )

    resolved_theme = _resolve_theme_mode(cast(ThemeMode, theme_mode))
    st.session_state.resolved_theme = resolved_theme
    st.sidebar.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)
    st.sidebar.caption("Auto follows the active system preference whenever available.")


def load_css() -> None:
    render_theme_controls()

    current_theme = _initialize_theme_mode()
    resolved_theme = _resolve_theme_mode(current_theme)
    palette = _get_palette(current_theme)
    st.session_state.resolved_theme = resolved_theme

    css_path = ROOT / "styles" / "main.css"
    with css_path.open("r", encoding="utf-8") as f:
        css = f.read()

    st.markdown(
        f"""
        <style>
        :root {{
            --app-background: {palette['bg']};
            --app-background-secondary: {palette['bg_secondary']};
            --sidebar-background: {palette['sidebar']};
            --glass-background: {palette['glass']};
            --border: {palette['border']};
            --text: {palette['text']};
            --muted: {palette['muted']};
            --primary: {palette['primary']};
            --accent: {palette['accent']};
            --shadow: {palette['shadow']};
            --shadow-strong: {palette['shadow_strong']};
            --input-background: {palette['input']};
            --gradient: {palette['gradient']};
            --ambient-glow: {palette['ambient']};
            --ambient-soft: {palette['ambient_soft']};
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
