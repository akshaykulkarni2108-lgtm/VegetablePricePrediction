from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]


@st.cache_data
def load_dataset():
    return pd.read_csv(ROOT / "data" / "cleaned_data.csv")


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
    fig.update_layout(
        template="plotly_dark",
        showlegend=False,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor="#0f172a",
        plot_bgcolor="#0f172a",
        font=dict(color="#f8fafc"),
        title=dict(font=dict(color="#f8fafc")),
    )
    fig.update_traces(textposition="outside", marker=dict(line=dict(color="#111827", width=1)))
    return fig


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
    fig.update_layout(
        template="plotly_dark",
        showlegend=False,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor="#0f172a",
        plot_bgcolor="#0f172a",
        font=dict(color="#f8fafc"),
        title=dict(font=dict(color="#f8fafc")),
    )
    fig.update_traces(textposition="outside", marker=dict(line=dict(color="#111827", width=1)))
    return fig