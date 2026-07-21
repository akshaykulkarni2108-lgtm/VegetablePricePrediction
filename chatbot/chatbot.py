import re
import pandas as pd
import streamlit as st

from typing import Dict, Any, Sequence

try:
    from chatbot.analyzer import analyze_question  # noqa: F401
except Exception:
    analyze_question = None

try:
    from chatbot.market_api import fetch_live_price
except Exception:
    def fetch_live_price(commodity: str, market: str = "") -> Dict[str, Any]:
        return {
            "commodity": commodity,
            "market": market,
            "date": "Today",
            "min": 0.0,
            "max": 0.0,
            "modal": 0.0,
            "source": "Fallback",
        }

try:
    from chatbot.insights import generate_insight
except Exception:
    def generate_insight(
        predicted_price,
        historical_avg,
        historical_max,
        historical_min,
        live_price,
        latest_date,
        commodity,
        market,
        state,
        district,
        df,
    ):
        return "Insight unavailable at the moment."

try:
    from chatbot.groq_ai import ask_groq
except Exception:
    def ask_groq(prompt: str) -> str:
        return "Groq analysis unavailable at the moment."

try:
    from chatbot.prompts import build_agromate_prompt
except Exception:
    def build_agromate_prompt(
        question,
        commodity,
        market,
        state,
        district,
        predicted_price,
        historical_avg,
        historical_max,
        historical_min,
        live_price,
        latest_date,
    ):
        return str(question)


class AgroMateChatbot:
    """
    AgroMateChatbot: A production-ready chatbot for agricultural market insights.
    Supports greetings, historical analysis, dataset queries, live prices,
    prediction explanation, AI analysis, recommendations, and forecasts.
    """

    # ----------------------------------------------------
    # Commodity Aliases
    # ----------------------------------------------------
    COMMODITY_ALIASES = {
        "tomato": ["tomato", "tomatoes"],
        "onion": ["onion", "onions"],
        "potato": ["potato", "potatoes"],
        "brinjal": ["brinjal", "eggplant"],
        "capsicum": ["capsicum", "bell pepper"],
        "chilli": ["chilli", "chilies", "chili", "green chilli", "green chili"],
    }

    # ----------------------------------------------------
    # Intent Keywords
    # ----------------------------------------------------
    INTENT_KEYWORDS = {
        "GREETING": ["hi", "hello", "hey", "namaste"],
        "LIVE_PRICE": [
            "live",
            "live price",
            "today live",
            "today market",
            "market price",
            "current price",
            "today price",
            "today's price",
        ],
        "PREDICTION": ["prediction", "predict", "forecast"],
        "ANALYSIS": ["analysis", "insight", "explain", "reason", "why"],
        "RECOMMENDATION": ["should i sell", "should i buy", "recommend"],
        "DATASET_QUERY": ["average", "highest", "lowest", "trend"],
    }

    def __init__(self, df: pd.DataFrame, model=None, encoders=None):
        self.df = df.copy() if df is not None else pd.DataFrame()
        self.model = model
        self.encoders = encoders
        self._cache_commodities = None
        self._cache_markets = None

        if not self.df.empty and "Price Date" in self.df.columns:
            self.df["Price Date"] = pd.to_datetime(
                self.df["Price Date"], errors="coerce"
            )

    # ----------------------------------------------------
    # Intent Detection
    # ----------------------------------------------------
    def _detect_intent(self, text: str) -> str:
        q = text.strip().lower()
        for intent, keywords in self.INTENT_KEYWORDS.items():
            if any(k in q for k in keywords):
                return intent
        return "UNKNOWN"

    # ----------------------------------------------------
    # Commodity Detection
    # ----------------------------------------------------
    def _find_commodity(self, text: str):
        if not text:
            return None
        text_lower = str(text).lower()
        for canonical, aliases in self.COMMODITY_ALIASES.items():
            for alias in aliases:
                if alias in text_lower:
                    return canonical.title()
        if not self.df.empty and "Commodity" in self.df.columns:
            if self._cache_commodities is None:
                self._cache_commodities = [
                    str(item).lower()
                    for item in self.df["Commodity"].dropna().unique()
                ]
            for item in self._cache_commodities:
                if item in text_lower:
                    return item.title()
        return None

    # ----------------------------------------------------
    # Market Detection
    # ----------------------------------------------------
    def _find_market(self, text: str):
        if not text:
            return None
        text_lower = str(text).lower()
        if not self.df.empty and "Market Name" in self.df.columns:
            if self._cache_markets is None:
                self._cache_markets = [
                    str(item).lower()
                    for item in self.df["Market Name"].dropna().unique()
                ]
            for item in self._cache_markets:
                if item in text_lower:
                    return item.title()
        patterns = [r"\bin\s+([a-zA-Z ]+)", r"\bat\s+([a-zA-Z ]+)", r"\bnear\s+([a-zA-Z ]+)"]
        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                return match.group(1).strip().title()
        return None

    # ----------------------------------------------------
    # Historical Summary
    # ----------------------------------------------------
    def _historical_summary(self, commodity: str):
        if self.df.empty or "Commodity" not in self.df.columns:
            return None
        subset = self.df[
            self.df["Commodity"].astype(str).str.lower() == str(commodity).lower()
        ]
        if subset.empty or "Modal_Price" not in subset.columns:
            return None
        avg_price = subset["Modal_Price"].mean()
        max_price = subset["Modal_Price"].max()
        min_price = subset["Modal_Price"].min()
        latest_date = subset["Price Date"].max() if "Price Date" in subset.columns else None
        total_records = len(subset)
        trend = "Increasing" if avg_price < max_price else "Stable/Decreasing"
        return {
            "avg": float(avg_price or 0),
            "max": float(max_price or 0),
            "min": float(min_price or 0),
            "latest": latest_date,
            "total_records": total_records,
            "trend": trend,
        }

    # ----------------------------------------------------
    # Prediction
    # ----------------------------------------------------
    def _get_prediction(self, historical_avg: float) -> float:
        prediction = historical_avg
        try:
            last_prediction = st.session_state.get("last_prediction")
            if last_prediction and isinstance(last_prediction, dict):
                prediction = float(last_prediction.get("prediction", historical_avg))
        except Exception:
            prediction = historical_avg
        return prediction

    # ----------------------------------------------------
    # Live Price Response
    # ----------------------------------------------------
    def _live_price_response(self, commodity: str, market: str):
        live = fetch_live_price(commodity, market)
        if not live:
            return "⚠ Unable to fetch live market price."
        min_price = float(live.get("min", 0) or 0)
        max_price = float(live.get("max", 0) or 0)
        modal_price = float(live.get("modal", 0) or 0)
        return f"""
### 🌐 Live Market Price

- **Commodity:** {live.get("commodity", "N/A")}
- **Market:** {live.get("market", "N/A")}
- **Date:** {live.get("date", "Today")}
- **Minimum Price:** ₹{min_price:,.2f}
- **Maximum Price:** ₹{max_price:,.2f}
- **Modal Price:** ₹{modal_price:,.2f}
- **Source:** {live.get("source", "Tavily")}
"""

    # ----------------------------------------------------
    # Recommendation
    # ----------------------------------------------------
    def _generate_recommendation(self, predicted: float, live: float) -> str:
        if predicted > live * 1.05:
            return "📈 **Recommendation: BUY** — Predicted price is significantly higher than live price."
        elif predicted >= live * 0.95:
            return "🤝 **Recommendation: HOLD** — Predicted price is slightly higher or equal to live price."
        else:
            return "📉 **Recommendation: SELL** — Predicted price is lower than live price."

    # ----------------------------------------------------
    # Prediction Insight
    # ----------------------------------------------------
    def _prediction_insight(self, question: str, commodity: str, market: str):
        history = self._historical_summary(commodity)
        if history is None:
            return "No historical data available for this commodity."

        historical_avg = history["avg"]
        predicted_price = self._get_prediction(historical_avg)
        live = fetch_live_price(commodity, market)
        live_price = float(live.get("modal", 0) or 0) if live else 0

        prompt = build_agromate_prompt(
            question=question,
            commodity=commodity,
            market=market if market else "Unknown",
            state="Unknown",
            district="Unknown",
            predicted_price=predicted_price,
            historical_avg=historical_avg,
            historical_max=history["max"],
            historical_min=history["min"],
            live_price=live_price,
            latest_date=str(history["latest"]),
        )
        try:
            ai_answer = ask_groq(prompt)
        except Exception:
            ai_answer = "AI analysis unavailable at the moment."

        local_insight = generate_insight(
            predicted_price=predicted_price,
            historical_avg=historical_avg,
            historical_max=history["max"],
            historical_min=history["min"],
            live_price=live_price,
            latest_date=history["latest"],
            commodity=commodity,
            market=market if market else "Unknown",
            state="Unknown",
            district="Unknown",
            df=self.df,
        )
        recommendation = self._generate_recommendation(predicted_price, live_price)

        return f"""
### 🤖 Prediction Insight

{ai_answer}

{local_insight}

**Recommendation:** {recommendation}
"""

    def get_response(self, question: str):
        if not question:
            return "Please ask a question about a commodity."

        question = str(question).strip()
        intent = self._detect_intent(question)
        commodity = self._find_commodity(question)
        market = self._find_market(question)

        if intent == "GREETING":
            return "👋 Hello! I'm AgroMate AI. Ask me about live prices, predictions, trends, or historical data."

        if commodity is None:
            return "🌾 Please mention a commodity name like Tomato, Onion, Potato, Garlic, etc."

        live_price_data = fetch_live_price(commodity, market)

        if intent == "LIVE_PRICE":
            return self._live_price_response(commodity, market)

        if intent in ["PREDICTION", "ANALYSIS", "RECOMMENDATION"]:
            return self._prediction_insight(question, commodity, market)

        history = self._historical_summary(commodity)
        if history:
            return f"""
### 📊 Historical Summary

**Commodity:** {commodity}

- Average Price: ₹{history['avg']:.2f}
- Highest Price: ₹{history['max']:.2f}
- Lowest Price: ₹{history['min']:.2f}
- Trend: {history['trend']}
"""

        return "Sorry, I couldn't understand your question."
