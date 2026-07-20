import time
from pathlib import Path

import joblib
import streamlit as st

from chatbot.chatbot import AgroMateChatbot
from utils.charts import load_dataset
from utils.ui_helpers import load_css, render_footer, render_header

ROOT = Path(__file__).resolve().parents[1]

st.set_page_config(page_title="AgroMate AI", page_icon="🤖", layout="wide")

load_css()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_user_input" not in st.session_state:
    st.session_state.last_user_input = ""


@st.cache_data(show_spinner=False)
def get_dataset():
    return load_dataset()


@st.cache_resource(show_spinner=False)
def get_model_and_encoders():
    try:
        model = joblib.load(ROOT / "models" / "random_forest.pkl")
        encoders = joblib.load(ROOT / "models" / "encoders.pkl")
        return model, encoders
    except Exception:
        return None, None


def ensure_chatbot() -> AgroMateChatbot:
    if "chatbot" not in st.session_state:
        df = get_dataset()
        model, encoders = get_model_and_encoders()
        st.session_state.chatbot = AgroMateChatbot(df, model, encoders)
    return st.session_state.chatbot


if st.sidebar.button("🗑️ Clear Chat", use_container_width=True):
    st.session_state.messages = []
    st.session_state.last_user_input = ""
    st.session_state.pop("chatbot", None)

bot = ensure_chatbot()
render_header("🤖 AgroMate AI", "Your Smart Agriculture Assistant", "🤖")

if len(st.session_state.messages) == 0:
    st.markdown(
        """
        <div class="glass-card" style="padding:2rem; text-align:center;">
            <h2 style="margin-top:0;">🤖 AgroMate AI</h2>
            <h4>Your Smart Agriculture Assistant</h4>
            <p style="margin-bottom:1rem;">
                Ask questions about vegetable prices, market trends, historical data, live market prices, and prediction insights.
            </p>
            <div style="text-align:left; max-width:400px; margin:auto;">
                <p><b>Example Questions:</b></p>
                • Today's tomato price<br>
                • Live onion price<br>
                • Current potato price<br>
                • Historical average of garlic<br>
                • Show tomato trend<br>
                • Explain prediction
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar="🤖" if msg["role"] == "assistant" else "👤"):
            st.markdown(msg["content"])

user_input = st.chat_input("Ask AgroMate AI...")
if user_input is not None:
    user_input = user_input.strip()
    if not user_input:
        st.warning("Please enter a question before sending it.")
    elif st.session_state.last_user_input and st.session_state.last_user_input.lower() == user_input.lower():
        st.warning("That question was just asked. Try a new one to continue the conversation.")
    else:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.last_user_input = user_input

        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)

        with st.spinner("AgroMate AI is thinking..."):
            response = bot.get_response(user_input)

        if not response or not str(response).strip():
            response = "I couldn't generate a response right now. Please try again."

        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant", avatar="🤖"):
            placeholder = st.empty()
            rendered = str(response).strip()
            for index in range(1, min(len(rendered), 220) + 1):
                placeholder.markdown(rendered[:index])
                time.sleep(0.003)
            placeholder.markdown(rendered)

render_footer()
