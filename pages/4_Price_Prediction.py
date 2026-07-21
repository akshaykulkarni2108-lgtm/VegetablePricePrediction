import joblib
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.charts import load_dataset
from utils.ui_helpers import load_css, render_footer, render_header

ROOT = Path(__file__).resolve().parents[1]

st.set_page_config(page_title="Price Prediction", page_icon="🥕", layout="wide")

load_css()


@st.cache_data(show_spinner=False)
def get_dataset():
    return load_dataset()


@st.cache_resource(show_spinner=False)
def get_model_and_encoders():
    try:
        model = joblib.load(ROOT / "models" / "random_forest.pkl")
        encoders = joblib.load(ROOT / "models" / "encoders.pkl")
        return model, encoders
    except Exception:
        return None, None


@st.cache_data(show_spinner=False)
def build_lookup_dicts(df: pd.DataFrame):
    state_to_district = (
        df.groupby("STATE")["District Name"].apply(lambda x: sorted(x.dropna().unique())).to_dict()
    )
    district_to_market = (
        df.groupby(["STATE", "District Name"])["Market Name"]
        .apply(lambda x: sorted(x.dropna().unique()))
        .to_dict()
    )
    commodity_to_variety = (
        df.groupby("Commodity")["Variety"].apply(lambda x: sorted(x.dropna().unique())).to_dict()
    )
    variety_to_grade = (
        df.groupby(["Commodity", "Variety"])["Grade"]
        .apply(lambda x: sorted(x.dropna().unique()))
        .to_dict()
    )
    return state_to_district, district_to_market, commodity_to_variety, variety_to_grade


def safe_encode(encoder, value: str, field: str):
    if encoder is None or value is None:
        return None
    if value not in encoder.classes_:
        st.error(f"⚠️ Selected {field} '{value}' was not available in market. Please choose another option.")
        return None
    return encoder.transform([value])[0]


df = get_dataset()
model, encoders = get_model_and_encoders()
state_to_district, district_to_market, commodity_to_variety, variety_to_grade = build_lookup_dicts(df)

if model is None or encoders is None:
    st.error("The prediction model is currently unavailable. Please try again later.")
    st.stop()

render_header(
    "Price Forecasting Panel",
    "Predict vegetable prices using the existing machine learning pipeline through a premium forecasting interface.",
    "🥕",
)

# ✅ Full-page centered form
st.markdown(
    """
    <style>
        .center-container {
            display: flex;
            justify-content: center;
            align-items: flex-start;
            width: 100%;
        }
        .form-card {
            flex: 1;
            max-width: 800px; /* keeps it readable on desktop */
            background: rgba(255,255,255,0.08);
            padding: 2rem;
            border-radius: 12px;
            backdrop-filter: blur(12px);
        }
        @media (max-width: 768px) {
            .form-card {
                max-width: 100%; /* mobile full width */
                padding: 1rem;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='center-container'><div class='form-card'>", unsafe_allow_html=True)

# --- FORM ---
state = st.selectbox("State", sorted(state_to_district.keys()), index=None, placeholder="Select State")
district = None
market = None
commodity = None
variety = None
grade = None

if state:
    district_list = state_to_district.get(state, [])
    district = st.selectbox("District", district_list, index=None, placeholder="Select District")

if district:
    market_list = district_to_market.get((state, district), [])
    market = st.selectbox("Market", market_list, index=None, placeholder="Select Market")

commodity = st.selectbox("Commodity", sorted(commodity_to_variety.keys()), index=None, placeholder="Select Commodity")

if commodity:
    variety_list = commodity_to_variety.get(commodity, [])
    variety = st.selectbox("Variety", variety_list, index=None, placeholder="Select Variety")

if variety:
    grade_list = variety_to_grade.get((commodity, variety), [])
    grade = st.selectbox("Grade", grade_list, index=None, placeholder="Select Grade")

c1, c2, c3 = st.columns(3)
with c1:
    day = st.number_input("Day", 1, 31, 1)
with c2:
    month = st.number_input("Month", 1, 12, 1)
with c3:
    year = st.number_input("Year", 2024, 2050, 2026)

predict = st.button("Predict Price", use_container_width=True)

st.markdown("</div></div>", unsafe_allow_html=True)
# --- END FORM ---

if predict:
    if None in [state, district, market, commodity, variety, grade]:
        st.markdown("<div class='status-banner status-banner--warning'><div class='status-title'>Incomplete selection</div><div class='status-copy'>Please select all required market fields before generating a forecast.</div></div>", unsafe_allow_html=True)
        st.stop()

    encoded_values = {}
    encoder_map = {
        "State": encoders["STATE"],
        "District": encoders["District Name"],
        "Market": encoders["Market Name"],
        "Commodity": encoders["Commodity"],
        "Variety": encoders["Variety"],
        "Grade": encoders["Grade"],
    }
    for field_name, value in {
        "State": state,
        "District": district,
        "Market": market,
        "Commodity": commodity,
        "Variety": variety,
        "Grade": grade,
    }.items():
        encoded_value = safe_encode(encoder_map[field_name], value, field_name)
        if encoded_value is None:
            st.stop()
        encoded_values[field_name] = encoded_value

    with st.spinner("Generating forecast..."):
        input_df = pd.DataFrame({
            "STATE": [encoded_values["State"]],
            "District Name": [encoded_values["District"]],
            "Market Name": [encoded_values["Market"]],
            "Commodity": [encoded_values["Commodity"]],
            "Variety": [encoded_values["Variety"]],
            "Grade": [encoded_values["Grade"]],
            "Day": [day],
            "Month": [month],
            "Year": [year],
        })
        prediction = model.predict(input_df)[0]

    st.markdown(
        f"""
        <div class="result-card">
            <div class="section-label">Prediction ready</div>
            <h4 style="margin:0.2rem 0 0.4rem;">Forecast completed successfully</h4>
            <div class="prediction-value">₹ {prediction:,.2f}</div>
            <p style="margin:0.35rem 0 0;">Price per quintal • Equivalent to ₹ {prediction / 100:,.2f} per kg</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    history = df[
        (df["STATE"] == state)
        & (df["District Name"] == district)
        & (df["Market Name"] == market)
        & (df["Commodity"] == commodity)
        & (df["Variety"] == variety)
        & (df["Grade"] == grade)
    ].copy()

    if not history.empty:
        history["Price Date"] = pd.to_datetime(history["Price Date"])
        history = history.sort_values("Price Date")

        fig = px.line(history, x="Price Date", y="Modal_Price", markers=True, title="Historical Price Trend")
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=50, b=20),
            font=dict(color="#F8FAFC"),
            title=dict(font=dict(color="#F8FAFC")),
            xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(size=11)),
            yaxis=dict(gridcolor="rgba(148, 163, 184, 0.22)", zeroline=False),
        )

        st.markdown("<div class='glass-card'><h4 style='margin-top:0;'>Historical trend</h4><p style='margin-bottom:0;'>A compact view of the selected market's historical price movements.</p></div>", unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.markdown("<div class='status-banner status-banner--warning'><div class='status-title'>No historical data</div><div class='status-copy'>No matching records were found for the selected market context.</div></div>", unsafe_allow_html=True)

render_footer()
