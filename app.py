# HOW TO RUN:
# 1. pip install -r requirements.txt
# 2. Add your Groq API key to .env file
# 3. streamlit run app.py

import streamlit as st
import os
import uuid
from groq import Groq
from dotenv import load_dotenv

# =========================================================
# SESSION STATE INITIALIZATION
# =========================================================

load_dotenv()

@st.cache_resource
def get_groq_client():
    return Groq(api_key=os.getenv("GROQ_API_KEY"))

client = get_groq_client()

st.set_page_config(layout="wide", page_title="Shark.AI", page_icon="🦈")

# Initialize State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversations" not in st.session_state:
    st.session_state.conversations = []
if "model" not in st.session_state:
    st.session_state.model = "llama3-70b-8192"

# =========================================================
# ADVANCED CSS — REAL CHATGPT CLONE
# =========================================================

st.markdown("""
<style>
    /* Global Background Fixes */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #212121 !important;
        color: #ececec !important;
    }

    /* THE INFAMOUS WHITE BAR FIX */
    /* This targets the bottom container and forces it to be dark */
    [data-testid="stBottom"], [data-testid="stChatInputContainer"] {
        background-color: #212121 !important;
        background: #212121 !important;
        border-top: none !important;
    }

    /* Sidebar Background */
    [data-testid="stSidebar"] {
        background-color: #171717 !important;
        border-right: 1px solid #303030 !important;
    }

    /* CHAT INPUT — PILL SHAPE */
    /* This turns the square box into a floating rounded pill */
    [data-testid="stChatInput"] {
        background-color: #2f2f2f !important;
        border-radius: 32px !important;
        border: 1px solid #424242 !important;
        padding-left: 10px !important;
        padding-right: 10px !important;
        max-width: 800px !important;
        margin: 0 auto !important;
    }
    
    [data-testid="stChatInput"] textarea {
        background-color: transparent !important;
        color: #ececec !important;
        border: none !important;
    }

    /* Message Bubbles */
    .stChatMessage {
        background-color: transparent !important;
        max-width: 800px !important;
        margin: 0 auto !important;
    }

    [data-testid="stChatMessageUser"] {
        background-color: #2f2f2f !important;
        border-radius: 18px !important;
        padding: 10px 18px !important;
        margin-bottom: 20px !important;
        width: fit-content !important;
        margin-left: auto !important;
    }

    [data-testid="stChatMessageAssistant"] {
        padding: 10px 0px !important;
        margin-bottom: 25px !important;
    }

    /* Buttons & Sidebar styling */
    .stButton > button {
        background-color: transparent !important;
        color: #ececec !important;
        border: 1px solid #303030 !important;
        border-radius: 8px !important;
        width: 100% !important;
        text-align: left !important;
        font-size: 14px !important;
    }
    
    .stButton > button:hover {
        background-color: #2a2a2a !important;
        border-color: #424242 !important;
    }

    /* Hide Streamlit Elements */
    #MainMenu, footer, header { visibility: hidden; }
    
    /* Typography */
    .welcome-text {
        text-align: center;
        font-size: 28px;
        font-weight: 600;
        margin-top: 100px;
        margin-bottom: 40px;
        color: #fff !important;
    }

    /* Grid Suggestions (ChatGPT 4 Style) */
    .suggestion-card {
        background-color: transparent !important;
        border: 1px solid #424242 !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        cursor: pointer;
        transition: 0.2s;
        height: 100% !important;
        text-align: left !important;
    }

    /* Dark Mode Icon logic */
    .shark-logo {
        display: block;
        margin: 0 auto;
        width: 40px;
        opacity: 0.9;
    }

</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.markdown("<h2 style='font-size: 20px;'>🦈 Shark.AI</h2>", unsafe_allow_html=True)
    
    if st.button("＋ New Chat"):
        if st.session_state.messages:
            title = st.session_state.messages[0]["content"][:25]
            st.session_state.conversations.append({
                "id": str(uuid.uuid4()),
                "title": title,
                "messages": list(st.session_state.messages)
            })
        st.session_state.messages = []
        st.rerun()

    st.divider()

    if st.session_state.conversations:
        st.markdown("<p style='font-size: 11px; color: #8e8ea0; text-transform: uppercase;'>Recent</p>", unsafe_allow_html=True)
        for convo in reversed(st.session_state.conversations):
            if st.button(f"💬 {convo['title']}", key=f"convo_{convo['id']}"):
                st.session_state.messages = list(convo["messages"])
                st.rerun()

    st.divider()
    st.session_state.model = st.selectbox("Model", ["llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768"])
    st.markdown("<p style='font-size: 11px; color: #8e8ea0; text-align: center;'>Shark.AI · Powered by Groq</p>", unsafe_allow_html=True)

# =========================================================
# MAIN AREA
# =========================================================

if not st.session_state.messages:
    # Shark Logo
    st.markdown("<h1 style='text-align: center; font-size: 60px; margin-top: 50px;'>🦈</h1>", unsafe_allow_html=True)
    st.markdown("<div class='welcome-text'>How can I help you today?</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💡 Explain quantum computing simply", key="q1"):
            st.session_state.prefill = "Explain quantum computing simply"
            st.rerun()
        if st.button("✍️ Write a LinkedIn post about AI", key="q2"):
            st.session_state.prefill = "Write a LinkedIn post about AI"
            st.rerun()
            
    with col2:
        if st.button("🐍 Write a Python web scraper", key="q3"):
            st.session_state.prefill = "Write a Python web scraper"
            st.rerun()
        if st.button("🐛 Debug my Python code", key="q4"):
            st.session_state.prefill = "Debug my Python code"
            st.rerun()

# Display Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =========================================================
# INPUT & STREAMING
# =========================================================

prompt = st.chat_input("Message Shark.AI...")

# Prefill from buttons
if "prefill" in st.session_state:
    prompt = st.session_state.prefill
    del st.session_state.prefill

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                model=st.session_state.model,
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                stream=True,
            )
            response = st.write_stream((chunk.choices[0].delta.content or "" for chunk in stream))
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"❌ Groq API Error: {str(e)}")
            st.info("Check if your API key in .env is correct and has not expired.")
            response = str(e)
    st.rerun()