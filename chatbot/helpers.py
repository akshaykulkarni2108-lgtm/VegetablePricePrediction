import re
import pandas as pd
from rapidfuzz import process, fuzz


def clean_text(text: str) -> str:
    """
    Clean and normalize user input.
    """
    if text is None:
        return ""

    text = str(text).strip().lower()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text)

    return text


def format_price(price):
    """
    Format price with ₹ symbol.
    """
    try:
        return f"₹{float(price):,.2f}"
    except Exception:
        return "N/A"


def format_date(date):
    """
    Format pandas datetime.
    """
    try:
        return pd.to_datetime(date).strftime("%d-%m-%Y")
    except Exception:
        return "N/A"


def fuzzy_match(query: str, choices):
    """
    Return best fuzzy match.
    """
    if not choices:
        return None

    result = process.extractOne(
        query,
        choices,
        scorer=fuzz.token_sort_ratio
    )

    if result is None:
        return None

    value, score, _ = result

    if score >= 75:
        return value

    return None


def extract_commodity(df, question: str):
    """
    Detect commodity from question.
    """
    if "Commodity" not in df.columns:
        return None

    commodities = (
        df["Commodity"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    question = clean_text(question)

    # Exact Match
    for commodity in commodities:
        if commodity.lower() in question:
            return commodity

    # Fuzzy Match
    return fuzzy_match(question, commodities)


def extract_market(df, question: str):
    """
    Detect market name.
    """
    if "Market Name" not in df.columns:
        return None

    markets = (
        df["Market Name"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    question = clean_text(question)

    for market in markets:
        if market.lower() in question:
            return market

    return fuzzy_match(question, markets)


def extract_state(df, question: str):
    """
    Detect state.
    """
    if "STATE" not in df.columns:
        return None

    states = (
        df["STATE"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    question = clean_text(question)

    for state in states:
        if state.lower() in question:
            return state

    return fuzzy_match(question, states)


def extract_district(df, question: str):
    """
    Detect district.
    """
    if "District Name" not in df.columns:
        return None

    districts = (
        df["District Name"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    question = clean_text(question)

    for district in districts:
        if district.lower() in question:
            return district

    return fuzzy_match(question, districts)


def calculate_difference(predicted, live):
    """
    Calculate difference between prediction and live price.
    """
    if predicted is None or live is None:
        return None

    difference = predicted - live
    percent = (difference / live) * 100 if live else 0

    return {
        "difference": round(difference, 2),
        "percentage": round(percent, 2)
    }


def dataset_summary(df):
    """
    Dataset summary.
    """
    return {
        "rows": len(df),
        "states": df["STATE"].nunique() if "STATE" in df.columns else 0,
        "markets": df["Market Name"].nunique() if "Market Name" in df.columns else 0,
        "commodities": df["Commodity"].nunique() if "Commodity" in df.columns else 0,
        "varieties": df["Variety"].nunique() if "Variety" in df.columns else 0,
    }


def latest_date(df):
    """
    Return latest available date.
    """
    if "Price Date" not in df.columns:
        return None

    dates = pd.to_datetime(
        df["Price Date"],
        errors="coerce"
    )

    return dates.max()