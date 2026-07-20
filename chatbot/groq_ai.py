import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def ask_groq(prompt: str) -> str:
    """
    Send prompt to Groq Llama model and return response.
    """

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=1024,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are AgroMate AI, an intelligent agriculture assistant. "
                        "Answer only agriculture, vegetable prices, markets, farming, "
                        "predictions and related questions. "
                        "Always provide clear and professional answers."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"Groq Error: {e}"