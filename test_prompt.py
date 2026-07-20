from chatbot.prompts import build_agromate_prompt

print(
    build_agromate_prompt(
        question="Should I sell tomatoes today?",
        commodity="Tomato",
        market="Pune",
        state="Maharashtra",
        district="Pune",
        predicted_price=2800,
        historical_avg=2500,
        historical_max=3400,
        historical_min=1800,
        live_price=2700,
        latest_date="12-07-2026",
    )
)