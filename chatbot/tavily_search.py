import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)

def search_live_price(query):
    try:
        response = client.search(
            query=query,
            search_depth="advanced",
            max_results=3
        )
        return response

    except Exception as e:
        print("Tavily Error:", e)
        return None