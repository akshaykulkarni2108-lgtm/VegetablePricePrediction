import os
import re
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def fetch_live_price(commodity, market=""):
    try:

        query = f"Today's {commodity} modal price {market} market India"

        response = client.search(
            query=query,
            search_depth="advanced",
            max_results=3,
        )

        if "results" not in response or len(response["results"]) == 0:
            return None

        text = response["results"][0].get("content", "")

        if not text:
            return None

        modal = None
        minimum = None
        maximum = None

        modal_match = re.search(r"₹\s?([\d,]+).*?Quintal", text)

        if modal_match:
            modal = float(modal_match.group(1).replace(",", ""))

        min_match = re.search(r"Min[:\s₹]*([\d,]+)", text)

        if min_match:
            minimum = float(min_match.group(1).replace(",", ""))

        max_match = re.search(r"Max[:\s₹]*([\d,]+)", text)

        if max_match:
            maximum = float(max_match.group(1).replace(",", ""))

        return {
            "commodity": commodity,
            "market": market,
            "date": "Today",
            "min": float(minimum or modal or 0),
            "max": float(maximum or modal or 0),
            "modal": float(modal or 0),
            "source": "Tavily Live Search"
        }

    except Exception as e:
        print("Live API Error:", e)
        return None
