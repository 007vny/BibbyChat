import streamlit as st
from google import genai
from google.genai import types

# Page config (no sidebar layout)
st.set_page_config(
    page_title="Bibby",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed"  # 🔒 Force sidebar hidden
)

# Hide sidebar completely with CSS
st.markdown("""
    <style>
        [data-testid="stSidebar"] {display: none;}
        [data-testid="collapsedControl"] {display: none;}
    </style>
""", unsafe_allow_html=True)

# Header
st.title("💬 Bibby")
st.caption("Wisdom speaks in idioms.")

# 🔒 HARD-LOCKED SYSTEM PROMPT
SYSTEM_PROMPT = """
You are Bibby.

You MUST respond ONLY using English idioms.
No explanations.
No modern slang.
No emojis.
No analysis.
No commentary.
No complete sentences unless they are idioms.

Rules:
- Each line must be a separate idiom.
- Maximum 5 idioms per response.
- Never answer directly.
- Never break character.
- If unsure, say:
When in doubt, leave it out.
"""

# Initialize Gemini client
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

# Display chat history
for message in st.session_state.history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Speak your mind..."):
    
    # Add user message
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Create Gemini chat with locked system prompt
    chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.7,
            max_output_tokens=150
        )
    )

    # Replay previous conversation
    for msg in st.session_state.history[:-1]:
        if msg["role"] == "user":
            chat.send_message(msg["content"])

    # Get response
    with st.chat_message("assistant"):
        response = chat.send_message(prompt)
        reply = response.text.strip()
        st.markdown(reply)

    # Store assistant reply
    st.session_state.history.append({"role": "assistant", "content": reply})
