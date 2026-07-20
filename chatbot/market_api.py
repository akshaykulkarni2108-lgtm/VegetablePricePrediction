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

        text = response["results"][0]["content"]

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
            "min": minimum if minimum else modal,
            "max": maximum if maximum else modal,
            "modal": modal,
            "source": "Tavily Live Search"
        }

    except Exception as e:
        print("Live API Error:", e)
        return None