from chatbot.groq_ai import ask_groq

answer = ask_groq(
    """
Explain why tomato prices increase during rainy season.
"""
)

print(answer)