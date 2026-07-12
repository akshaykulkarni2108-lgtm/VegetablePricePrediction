import joblib
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.charts import load_dataset
from utils.ui_helpers import load_css, render_footer, render_header

ROOT = Path(__file__).resolve().parents[1]

st.set_page_config(
    page_title="Price Prediction",
    page_icon="🥕",
    layout="wide"
)

load_css()

# -----------------------------
# Load Data
# -----------------------------

df = load_dataset()

model = joblib.load(ROOT / "models" / "random_forest.pkl")
encoders = joblib.load(ROOT / "models" / "encoders.pkl")

# -----------------------------
# Header
# -----------------------------

render_header(
    "Price Forecasting Panel",
    "Predict Vegetable Prices using Machine Learning",
    "🥕"
)

st.markdown("---")

# =====================================================
# STATE
# =====================================================

state = st.selectbox(
    "State",
    sorted(df["STATE"].dropna().unique()),
    index=None,
    placeholder="Select State"
)

district = None
market = None
commodity = None
variety = None
grade = None

# =====================================================
# DISTRICT
# =====================================================

if state:

    district_list = sorted(
        df[df["STATE"] == state]["District Name"].dropna().unique()
    )

    district = st.selectbox(
        "District",
        district_list,
        index=None,
        placeholder="Select District"
    )

# =====================================================
# MARKET
# =====================================================

if district:

    market_list = sorted(
        df[
            (df["STATE"] == state)
            &
            (df["District Name"] == district)
        ]["Market Name"].dropna().unique()
    )

    market = st.selectbox(
        "Market",
        market_list,
        index=None,
        placeholder="Select Market"
    )

# =====================================================
# COMMODITY
# =====================================================

commodity = st.selectbox(
    "Commodity",
    sorted(df["Commodity"].dropna().unique()),
    index=None,
    placeholder="Select Commodity"
)

# =====================================================
# VARIETY
# =====================================================

if commodity:

    variety_list = sorted(
        df[
            df["Commodity"] == commodity
        ]["Variety"].dropna().unique()
    )

    variety = st.selectbox(
        "Variety",
        variety_list,
        index=None,
        placeholder="Select Variety"
    )

# =====================================================
# GRADE
# =====================================================

if variety:

    grade_list = sorted(
        df[
            (df["Commodity"] == commodity)
            &
            (df["Variety"] == variety)
        ]["Grade"].dropna().unique()
    )

    grade = st.selectbox(
        "Grade",
        grade_list,
        index=None,
        placeholder="Select Grade"
    )

# =====================================================
# DATE
# =====================================================

c1, c2, c3 = st.columns(3)

with c1:
    day = st.number_input("Day", 1, 31, 1)

with c2:
    month = st.number_input("Month", 1, 12, 1)

with c3:
    year = st.number_input("Year", 2024, 2035, 2026)

st.markdown("")

predict = st.button(
    "🔍 Predict Price",
    use_container_width=True
)

# =====================================================
# PREDICTION
# =====================================================

if predict:

    if None in [state, district, market, commodity, variety, grade]:

        st.warning("Please select all fields.")
        st.stop()

    with st.spinner("Generating Prediction..."):

        input_df = pd.DataFrame({

            "STATE":[encoders["STATE"].transform([state])[0]],

            "District Name":[encoders["District Name"].transform([district])[0]],

            "Market Name":[encoders["Market Name"].transform([market])[0]],

            "Commodity":[encoders["Commodity"].transform([commodity])[0]],

            "Variety":[encoders["Variety"].transform([variety])[0]],

            "Grade":[encoders["Grade"].transform([grade])[0]],

            "Day":[day],
            "Month":[month],
            "Year":[year]

        })

        prediction = model.predict(input_df)[0]

    st.success("Prediction Generated Successfully")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Price / Quintal",
            f"₹ {prediction:,.2f}"
        )

    with col2:

        st.metric(
            "Price / Kg",
            f"₹ {prediction/100:,.2f}"
        )

    # =====================================================
    # HISTORICAL DATA
    # =====================================================

    history = df[

        (df["STATE"] == state)

        &

        (df["District Name"] == district)

        &

        (df["Market Name"] == market)

        &

        (df["Commodity"] == commodity)

        &

        (df["Variety"] == variety)

        &

        (df["Grade"] == grade)

    ].copy()

    if not history.empty:

        history["Price Date"] = pd.to_datetime(history["Price Date"])

        history = history.sort_values("Price Date")

        fig = px.line(

            history,

            x="Price Date",

            y="Modal_Price",

            markers=True,

            title="Historical Price Trend"

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info("No Historical Data Found.")

render_footer()