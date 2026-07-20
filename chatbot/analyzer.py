import pandas as pd

from chatbot.helpers import (
    clean_text,
    extract_commodity,
    extract_market,
    extract_state,
    extract_district,
    format_price,
    format_date,
)


def analyze_question(df: pd.DataFrame, question: str) -> str:
    """
    Main analysis function.
    """

    if df.empty:
        return "Dataset is empty."

    question = clean_text(question)

    commodity = extract_commodity(df, question)
    market = extract_market(df, question)
    state = extract_state(df, question)
    district = extract_district(df, question)

    data = df.copy()

    if commodity:
        data = data[data["Commodity"] == commodity]

    if market:
        data = data[data["Market Name"] == market]

    if state:
        data = data[data["STATE"] == state]

    if district:
        data = data[data["District Name"] == district]

    if data.empty:
        return "No matching data found."

    # -----------------------------
    # Average Price
    # -----------------------------
    if "average" in question or "avg" in question:

        avg = data["Modal_Price"].mean()

        return (
            f"📊 Average Price\n\n"
            f"Commodity : {commodity or 'All'}\n"
            f"Market : {market or 'All'}\n"
            f"Average Modal Price : {format_price(avg)}"
        )

    # -----------------------------
    # Highest Price
    # -----------------------------
    if "highest" in question or "maximum" in question:

        row = data.loc[data["Modal_Price"].idxmax()]

        return (
            f"📈 Highest Price\n\n"
            f"Commodity : {row['Commodity']}\n"
            f"Market : {row['Market Name']}\n"
            f"State : {row['STATE']}\n"
            f"Price : {format_price(row['Modal_Price'])}\n"
            f"Date : {format_date(row['Price Date'])}"
        )

    # -----------------------------
    # Lowest Price
    # -----------------------------
    if "lowest" in question or "minimum" in question:

        row = data.loc[data["Modal_Price"].idxmin()]

        return (
            f"📉 Lowest Price\n\n"
            f"Commodity : {row['Commodity']}\n"
            f"Market : {row['Market Name']}\n"
            f"State : {row['STATE']}\n"
            f"Price : {format_price(row['Modal_Price'])}\n"
            f"Date : {format_date(row['Price Date'])}"
        )

    # -----------------------------
    # Latest Price
    # -----------------------------
    if "latest" in question or "recent" in question:

        data["Price Date"] = pd.to_datetime(data["Price Date"])

        latest = data.sort_values(
            "Price Date",
            ascending=False
        ).iloc[0]

        return (
            f"🕒 Latest Price\n\n"
            f"Commodity : {latest['Commodity']}\n"
            f"Market : {latest['Market Name']}\n"
            f"Modal Price : {format_price(latest['Modal_Price'])}\n"
            f"Date : {format_date(latest['Price Date'])}"
        )

    # -----------------------------
    # Count Records
    # -----------------------------
    if "records" in question or "count" in question:

        return f"Dataset contains {len(data):,} matching records."

    # -----------------------------
    # Trend
    # -----------------------------
    if "trend" in question:

        avg = data["Modal_Price"].mean()

        latest = data.sort_values(
            "Price Date",
            ascending=False
        ).iloc[0]["Modal_Price"]

        if latest > avg:
            trend = "📈 Upward Trend"

        elif latest < avg:
            trend = "📉 Downward Trend"

        else:
            trend = "➡ Stable Trend"

        return (
            f"{trend}\n\n"
            f"Latest Price : {format_price(latest)}\n"
            f"Historical Average : {format_price(avg)}"
        )

    # -----------------------------
    # Market Summary
    # -----------------------------
    if "summary" in question:

        return (
            f"📋 Summary\n\n"
            f"Records : {len(data):,}\n"
            f"Average : {format_price(data['Modal_Price'].mean())}\n"
            f"Maximum : {format_price(data['Modal_Price'].max())}\n"
            f"Minimum : {format_price(data['Modal_Price'].min())}"
        )

    # -----------------------------
    # Default
    # -----------------------------
    return (
        "🤖 I can answer:\n\n"
        "• Average Price\n"
        "• Highest Price\n"
        "• Lowest Price\n"
        "• Latest Price\n"
        "• Trend Analysis\n"
        "• Summary\n"
        "• Record Count"
    )