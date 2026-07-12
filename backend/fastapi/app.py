from fastapi import FastAPI
from pathlib import Path
import pandas as pd
import joblib

app = FastAPI(title="Vegetable Price Prediction API")

ROOT = Path(__file__).resolve().parents[2]

# Load model
model = joblib.load(ROOT / "models" / "random_forest.pkl")
encoders = joblib.load(ROOT / "models" / "encoders.pkl")


def normalize(text):
    return str(text).strip().lower()


def encode_value(column, value):
    """
    Case-insensitive LabelEncoder lookup.
    Accepts:
    Maharashtra
    maharashtra
    MAHARASHTRA
    mAhArAsHtRa
    """

    value = normalize(value)

    encoder = encoders[column]

    mapping = {
        str(cls).strip().lower(): i
        for i, cls in enumerate(encoder.classes_)
    }

    if value not in mapping:
        raise ValueError(
            f"{column} '{value}' not found.\nAvailable values: {list(mapping.keys())[:20]}"
        )

    return mapping[value]


@app.get("/")
def home():
    return {
        "message": "Vegetable Price Prediction API Running 🚀"
    }


@app.post("/predict")
def predict(data: dict):

    try:

        encoded = {
            "STATE": encode_value("STATE", data["STATE"]),
            "District Name": encode_value("District Name", data["District Name"]),
            "Market Name": encode_value("Market Name", data["Market Name"]),
            "Commodity": encode_value("Commodity", data["Commodity"]),
            "Variety": encode_value("Variety", data["Variety"]),
            "Grade": encode_value("Grade", data["Grade"]),
            "Day": int(data["Day"]),
            "Month": int(data["Month"]),
            "Year": int(data["Year"]),
        }

        df = pd.DataFrame([encoded])

        prediction = model.predict(df)[0]

        return {
            "prediction_per_quintal": round(float(prediction), 2),
            "prediction_per_kg": round(float(prediction / 100), 2)
        }

    except Exception as e:
        return {
            "error": str(e)
        }