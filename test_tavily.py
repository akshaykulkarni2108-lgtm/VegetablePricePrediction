from chatbot.tavily_search import search_live_price

result = search_live_price(
    "Today's Tomato modal price Pune market Maharashtra"
)

print(result)