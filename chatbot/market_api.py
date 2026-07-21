import os
import re
from typing import Dict, Any, Optional , Sequence
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

DEBUG = True


def fetch_live_price(commodity: str, market: str = "") -> Dict[str, Any]:
    """
    Fetch live market price for a given commodity and market using Tavily Search.

    Args:
        commodity (str): The commodity name (e.g., "Tomato").
        market (str, optional): The market name (e.g., "Nashik"). Defaults to "".

    Returns:
        Dict[str, Any]: A dictionary containing commodity, market, date, min, max,
                        modal, and source. Prices are always floats.
    """
    try:
        query = f"Today's {commodity} modal price {market} market India".strip()
        if DEBUG:
            print("Query:", query)

        response = client.search(
            query=query,
            search_depth="advanced",
            max_results=3,
        )
        print("Response:", response)

        if not response or "results" not in response or len(response["results"]) == 0:
            return _default_response(commodity, market)

        for result in response["results"]:
            text = result.get("content", "")
            if not text:
                continue

            if DEBUG:
                print("Content:", text)

            modal = _extract_price(
                text,
                [
                    r"Modal Price[:\s₹]*([\d,]+)",
                    r"Modal[:\s₹]*([\d,]+)",
                    r"Average Price[:\s₹]*([\d,]+)",
                    r"Average[:\s₹]*([\d,]+)",
                    r"₹\s?([\d,]+).*?(?:Quintal|kg)",
                    r"(?:Rs\.?|INR)\s*([\d,]+)",
                    r"([\d,]+)/quintal",
                    r"Modal\s*Rate[:\s₹Rs\.]*([\d,]+)"
                    r"Wholesale\s*Price[:\s₹Rs\.]*([\d,]+)"
                ],
            )

            minimum = _extract_price(
                text,
                [
                    r"Min[:\s₹]*([\d,]+)",
                    r"Minimum Price[:\s₹]*([\d,]+)",
                    r"Minimum[:\s₹]*([\d,]+)",
                ],
            )

            maximum = _extract_price(
                text,
                [
                    r"Max[:\s₹]*([\d,]+)",
                    r"Maximum Price[:\s₹]*([\d,]+)",
                    r"Maximum[:\s₹]*([\d,]+)",
                ],
            )

            # Fallbacks
            if modal == 0 and minimum > 0 and maximum > 0:
                modal = (minimum + maximum) / 2
            if minimum == 0 and modal > 0:
                minimum = modal
            if maximum == 0 and modal > 0:
                maximum = modal

            # If all are zero, try to extract any reasonable number
            if modal == 0 and minimum == 0 and maximum == 0:
                numbers = re.findall(r"[\d,]{3,}", text)
                prices = []
                for num in numbers:
                    try:
                        val = float(num.replace(",", ""))
                        if 100 <= val <= 100000:
                            prices.append(val)
                    except ValueError:
                        continue
                if prices:
                    modal = prices[0]
                    minimum = modal
                    maximum = modal

            if DEBUG:
                print("Parsed Prices:", {"modal": modal, "min": minimum, "max": maximum})

            if modal > 0 or minimum > 0 or maximum > 0:
                return {
                    "commodity": commodity,
                    "market": market,
                    "date": "Today",
                    "min": float(minimum or modal or 0),
                    "max": float(maximum or modal or 0),
                    "modal": float(modal or 0),
                    "source": "Tavily Live Search",
                }

        return _default_response(commodity, market)

    except Exception as e:
        print("Live API Error:", e)
        return _default_response(commodity, market)


def _extract_price(text: str, patterns: Sequence[str]) -> float:
    """
    Extract price from text using multiple regex patterns.

    Args:
        text (str): The text to search.
        patterns (list): List of regex patterns.

    Returns:
        float: Extracted price or 0 if not found.
    """
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                return float(match.group(1).replace(",", ""))
            except ValueError:
                continue
    return 0.0


def _default_response(commodity: str, market: str) -> Dict[str, Any]:
    """
    Return a default response when live price data is unavailable.

    Args:
        commodity (str): The commodity name.
        market (str): The market name.

    Returns:
        Dict[str, Any]: Default dictionary with zero prices.
    """
    return {
        "commodity": commodity,
        "market": market,
        "date": "Today",
        "min": 0.0,
        "max": 0.0,
        "modal": 0.0,
        "source": "Tavily Live Search",
    }
