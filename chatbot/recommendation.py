import pandas as pd


class RecommendationEngine:

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    # -------------------------------------------------
    # BUY / HOLD / SELL
    # -------------------------------------------------
    def buy_hold_sell(self, predicted_price: float, live_price: float):

        if live_price <= 0:
            return {
                "recommendation": "UNKNOWN",
                "reason": "Live price unavailable."
            }

        change = ((predicted_price - live_price) / live_price) * 100

        if change >= 10:
            rec = "BUY"

        elif change >= -5:
            rec = "HOLD"

        else:
            rec = "SELL"

        return {
            "recommendation": rec,
            "change_percent": round(change, 2),
            "predicted_price": predicted_price,
            "live_price": live_price,
            "reason": f"Predicted price is {change:.2f}% compared to live price."
        }

    # -------------------------------------------------
    # PROFIT ESTIMATOR
    # -------------------------------------------------
    def estimate_profit(self,
                        quantity_quintal: float,
                        predicted_price: float,
                        live_price: float):

        profit = (predicted_price - live_price) * quantity_quintal

        return {
            "quantity": quantity_quintal,
            "profit": round(profit, 2)
        }

    # -------------------------------------------------
    # BEST MARKET
    # -------------------------------------------------
    def best_market(self, commodity: str):

        if self.df.empty:
            return None

        df = self.df[
            self.df["Commodity"].str.lower()
            == commodity.lower()
        ]

        if df.empty:
            return None

        market = (
            df.groupby("Market Name")["Modal_Price"]
            .mean()
            .sort_values(ascending=False)
            .head(5)
            .reset_index()
        )

        return market

    # -------------------------------------------------
    # BEST DAY
    # -------------------------------------------------
    def best_day(self, commodity: str):

        if "Price Date" not in self.df.columns:
            return None

        df = self.df[
            self.df["Commodity"].str.lower()
            == commodity.lower()
        ].copy()

        if df.empty:
            return None

        df["Day"] = pd.to_datetime(
            df["Price Date"]
        ).dt.day_name()

        result = (
            df.groupby("Day")["Modal_Price"]
            .mean()
            .sort_values(ascending=False)
            .reset_index()
        )

        return result

    # -------------------------------------------------
    # ALTERNATIVE CROPS
    # -------------------------------------------------
    def alternative_crop(self, top_n=5):

        result = (
            self.df.groupby("Commodity")["Modal_Price"]
            .mean()
            .sort_values(ascending=False)
            .head(top_n)
            .reset_index()
        )

        return result