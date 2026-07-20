from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]


@st.cache_data(show_spinner=False)
def load_dataset():
    return pd.read_csv(ROOT / "data" / "cleaned_data.csv")


def _get_plotly_theme() -> str:
    resolved_theme = st.session_state.get("resolved_theme", "dark")
    return "plotly_white" if resolved_theme == "light" else "plotly_dark"


def _style_chart(fig):
    is_light = _get_plotly_theme() == "plotly_white"
    colors = {
        "text": "#0f172a" if is_light else "#f8fafc",
        "grid": "rgba(148, 163, 184, 0.18)" if is_light else "rgba(148, 163, 184, 0.22)",
    }
    fig.update_layout(
        template=_get_plotly_theme(),
        showlegend=False,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=colors["text"]),
        title=dict(font=dict(color=colors["text"])),
        xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(size=11)),
        yaxis=dict(gridcolor=colors["grid"], zeroline=False),
    )
    fig.update_traces(textposition="outside", marker=dict(line=dict(color="rgba(255,255,255,0.18)", width=1)))
    return fig


def plot_top_commodities(df, top_n: int = 8):
    counts = df["Commodity"].value_counts().head(top_n)
    fig = px.bar(
        counts,
        x=counts.index,
        y=counts.values,
        color=counts.index,
        text=counts.values,
        title="Top Vegetables by Frequency",
    )
    return _style_chart(fig)


def plot_average_price_by_state(df, top_n: int = 8):
    avg_price = df.groupby("STATE")["Modal_Price"].mean().sort_values(ascending=False).head(top_n)
    fig = px.bar(
        avg_price,
        x=avg_price.index,
        y=avg_price.values,
        color=avg_price.index,
        text=avg_price.round(2),
        title="Average Modal Price by State",
    )
    return _style_chart(fig)