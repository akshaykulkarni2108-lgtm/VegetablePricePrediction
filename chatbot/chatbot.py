import pandas as pd
import streamlit as st

from chatbot.analyzer import analyze_question
from chatbot.market_api import fetch_live_price
from chatbot.insights import generate_insight
from chatbot.groq_ai import ask_groq
from chatbot.prompts import build_agromate_prompt


class AgroMateChatbot:

    def __init__(self, df, model=None, encoders=None):
        self.df = df.copy() if df is not None else pd.DataFrame()
        self.model = model
        self.encoders = encoders

        if (
            not self.df.empty
            and "Price Date" in self.df.columns
        ):
            self.df["Price Date"] = pd.to_datetime(
                self.df["Price Date"],
                errors="coerce"
            )

    # ----------------------------------------------------
    # Find commodity from question
    # ----------------------------------------------------

    def _find_commodity(self, text):

        if self.df.empty:
            return None

        text = str(text).lower()

        if "Commodity" not in self.df.columns:
            return None

        for item in self.df["Commodity"].dropna().unique():

            if str(item).lower() in text:
                return item

        return None

    # ----------------------------------------------------
    # Find market from question
    # ----------------------------------------------------

    def _find_market(self, text):

        if self.df.empty:
            return None

        text = str(text).lower()

        if "Market Name" not in self.df.columns:
            return None

        for item in self.df["Market Name"].dropna().unique():

            if str(item).lower() in text:
                return item

        return None

    # ----------------------------------------------------
    # Historical summary
    # ----------------------------------------------------

    def _historical_summary(self, commodity):

        subset = self.df[
            self.df["Commodity"].astype(str).str.lower()
            ==
            str(commodity).lower()
        ]

        if subset.empty:
            return None

        return {

            "avg": subset["Modal_Price"].mean(),

            "max": subset["Modal_Price"].max(),

            "min": subset["Modal_Price"].min(),

            "latest": (
                subset["Price Date"].max()
                if "Price Date" in subset.columns
                else "N/A"
            )

        }

    # ----------------------------------------------------
    # Get latest prediction from Streamlit session
    # ----------------------------------------------------

    def _get_prediction(self, historical_avg):

        prediction = historical_avg

        try:

            last_prediction = st.session_state.get(
                "last_prediction"
            )

            if (
                last_prediction
                and
                isinstance(last_prediction, dict)
            ):

                prediction = float(

                    last_prediction.get(
                        "prediction",
                        historical_avg
                    )

                )

        except Exception:

            pass

        return prediction

    # ----------------------------------------------------
    # AI prediction insight
    # ----------------------------------------------------

    def _prediction_insight(self, question, commodity, market):

        history = self._historical_summary(commodity)

        if history is None:
            return "No historical data available for this commodity."

        historical_avg = history["avg"]
        historical_max = history["max"]
        historical_min = history["min"]
        latest_date = history["latest"]

        predicted_price = self._get_prediction(historical_avg)

        # Live price
        live = fetch_live_price(commodity, market)
        live_price = live.get("modal") if live else None

        # Build AI prompt
        prompt = build_agromate_prompt(
            question=question,
            commodity=commodity,
            market=market if market else "Unknown",
            state="Unknown",
            district="Unknown",
            predicted_price=predicted_price,
            historical_avg=historical_avg,
            historical_max=historical_max,
            historical_min=historical_min,
            live_price=live_price,
            latest_date=str(latest_date)
        )

        # AI answer
        ai_answer = ask_groq(prompt)

        # Local insight
        local_insight = generate_insight(
            predicted_price=predicted_price,
            historical_avg=historical_avg,
            historical_max=historical_max,
            historical_min=historical_min,
            live_price=live_price,
            latest_date=latest_date,
            commodity=commodity,
            market=market if market else "Unknown",
            state="Unknown",
            district="Unknown",
            df=self.df
        )

        return ai_answer + "\n\n---\n\n" + local_insight

    # ----------------------------------------------------
    # Live price response
    # ----------------------------------------------------

    def _live_price_response(self, commodity, market):

        live = fetch_live_price(commodity, market)

        if live is None:
            return "⚠ Unable to fetch live market price."

        return f"""
🌐 **Live Market Price**

Commodity : {live.get('commodity','N/A')}

Market : {live.get('market','N/A')}

Date : {live.get('date','N/A')}

Minimum : ₹{live.get('min',0):,.2f}

Maximum : ₹{live.get('max',0):,.2f}

Modal : ₹{live.get('modal',0):,.2f}

Source : {live.get('source','Agmarknet')}
"""

    # ----------------------------------------------------
    # Main chatbot response
    # ----------------------------------------------------

    def get_response(self, question):

        if question is None or str(question).strip() == "":
            return "Please enter a question."

        q = str(question).strip().lower()

        # Greetings
        if any(
            q.startswith(greet)
            for greet in ["hi", "hello", "hey", "namaste"]
        ):
            return (
                "👋 Hello! I am AgroMate AI.\n\n"
                "I can help with:\n"
                "• Historical Prices\n"
                "• Market Trends\n"
                "• Live Prices\n"
                "• Prediction Explanation\n"
                "• Buy / Hold / Sell Recommendation"
            )

        # Live price
        if any(x in q for x in ["live", "today", "current"]):

            commodity = self._find_commodity(question)
            market = self._find_market(question)

            if commodity is None:
                return "Please mention a commodity."

            return self._live_price_response(
                commodity,
                market
            )

        # AI prediction / analysis
        if any(
            x in q
            for x in [
                "prediction",
                "predict",
                "analysis",
                "insight",
                "why",
                "reason",
                "explain",
                "should i sell",
                "should i buy",
                "recommend"
            ]
        ):

            commodity = self._find_commodity(question)
            market = self._find_market(question)

            if commodity is None:
                commodity = "Tomato"

            return self._prediction_insight(
                question,
                commodity,
                market
            )

        # Dataset analysis
        answer = analyze_question(
            self.df,
            question
        )

        if answer:
            return answer

        # Unknown
        return (
            "I couldn't understand your question.\n\n"
            "Try:\n"
            "• Average Tomato Price\n"
            "• Highest Onion Price\n"
            "• Today's Potato Price\n"
            "• Explain Prediction\n"
            "• Should I sell tomatoes today?"
        )