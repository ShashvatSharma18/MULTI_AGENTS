import streamlit as st
import os
import sys
import uuid
import time
import requests
import json
from datetime import datetime, timezone
from auth import signup, login
from chat_api import (
    create_chat,
    save_message,
    get_user_chats,
    load_chat
)

# =========================================================
# PATH SETUP
# =========================================================
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(page_title="Shark Engine", page_icon="🦈", layout="wide")

# =========================================================
# AGENTIC THEME (AI ENGINE EDITION)
# =========================================================
st.markdown("""
<style>
    /* Global Background: Deep Charcoal AI Space */
    .stApp {
        background: radial-gradient(circle at 50% 50%, #1A1D23 0%, #0E1117 100%);
        color: #E6EAF1;
    }
    
    /* Sidebar: Industrial Agent Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #11141B !important;
        border-right: 1px solid #232936;
        width: 320px !important;
    }
    
    /* Center the Main Content */
    .main .block-container {
        max-width: 900px;
        padding-top: 2rem;
    }

    /* Agent Identity Badge */
    .agent-identity {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 12px;
        color: #00D1FF;
    }
    .agent-avatar {
        width: 32px;
        height: 32px;
        background: linear-gradient(135deg, #00D1FF, #0070F3);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        color: white;
        box-shadow: 0 0 10px rgba(0, 209, 255, 0.4);
    }
    .agent-name {
        font-size: 14px;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }

    /* AI Chat Bubbles (Wide & Modern) */
    .stChatMessage {
        border-radius: 16px !important;
        margin-bottom: 24px;
        padding: 24px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.05);
    }
    
    .stChatMessage[data-testid="stChatMessageAssistant"] {
        background-color: #1A1F26 !important;
        border-right: 4px solid #00D1FF;
    }
    
    .stChatMessage[data-testid="stChatMessageUser"] {
        background-color: #232936 !important;
        border-status: none;
    }

    /* Action Buttons (Industrial & Flat) */
    .stButton>button {
        width: 100%;
        background: #232936;
        color: #FFFFFF;
        border: 1px solid #30363D;
        border-radius: 12px;
        height: 48px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background: #30363D;
        border-color: #00D1FF;
        color: #00D1FF;
    }

    /* Chat Input: Docked Bottom Bar */
    .stChatInputContainer {
        border: 1px solid #30363D !important;
        background: #11141B !important;
        border-radius: 16px !important;
        box-shadow: 0 -10px 40px rgba(0,0,0,0.3);
    }

    /* Status Box Style */
    .status-msg {
        color: #8B949E;
        font-size: 13px;
        font-style: italic;
        margin-bottom: 4px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    @keyframes pulse {
        0% { opacity: 0.5; }
        50% { opacity: 1; }
        100% { opacity: 0.5; }
    }
    .status-pulse {
        width: 8px; height: 8px;
        background: #00D1FF;
        border-radius: 50%;
        animation: pulse 1.5s infinite;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# SESSION STATE
# =========================================================
if "token" not in st.session_state:
    st.session_state.token = None
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = None
if "chat_id" not in st.session_state:
    st.session_state.chat_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

# =========================================================
# AUTH GATE
# =========================================================
if not st.session_state.logged_in:
    st.markdown("""
        <div style='text-align: center; margin-top: 8rem;'>
            <h1 style='font-size: 4rem; font-weight: 900; background: linear-gradient(90deg, #00D1FF, #0070F3); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>SHARK ENGINE</h1>
            <p style='color: #8B949E; margin-top: 10px; font-size: 1.2rem;'>Advanced Multi-Agent Orchestration Protocol</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        st.markdown("<div style='background: #161B22; padding: 3rem; border-radius: 20px; border: 1px solid #30363D; box-shadow: 0 20px 60px rgba(0,0,0,0.4);'>", unsafe_allow_html=True)
        login_tab, signup_tab = st.tabs(["IDENTIFY", "NEW REGISTRY"])
        
        with login_tab:
            with st.form("l_form"):
                u = st.text_input("Registry ID (Email)")
                p = st.text_input("Access Key", type="password")
                if st.form_submit_button("AUTHORIZE MISSION"):
                    res = login(u, p)
                    if res.status_code == 200:
                        d = res.json()
                        st.session_state.token = d.get("token")
                        st.session_state.user_email = d.get("email")
                        st.session_state.logged_in = True
                        st.rerun()
                    else: st.error("Access Denied.")
                    
        with signup_tab:
            with st.form("s_form"):
                u = st.text_input("Registry ID (Email)")
                p = st.text_input("New Access Key", type="password")
                if st.form_submit_button("DEPLOY PROTOCOL"):
                    res = signup("", u, p)
                    if res.status_code == 200: st.success("Registry Created.")
                    else: st.error("Storage Fault.")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# =========================================================
# MAIN APP (LOGGED IN)
# =========================================================
from backend.rag.ingestion import ingest_pdf, ingest_text

# SIDEBAR
with st.sidebar:
    st.markdown("### 💠 AGENT STATUS")
    st.markdown(f"**ONLINE:** `{st.session_state.user_email.split('@')[0].upper()}`")
    
    if st.button("TERMINATE CONNECTION"):
        st.session_state.token = None
        st.session_state.logged_in = False
        st.rerun()

    st.divider()
    st.subheader("📁 SESSION ARCHIVE")
    if st.button("＋ NEW MISSION"):
        new_chat = create_chat(st.session_state.user_email, st.session_state.token)
        st.session_state.chat_id = new_chat["chat_id"]
        st.session_state.messages = []
        st.session_state.resume_text = ""
        st.rerun()

    try:
        chats = get_user_chats(st.session_state.user_email, st.session_state.token)
        for chat in (chats if isinstance(chats, list) else []):
            chat_id = chat["_id"]
            col1, col2 = st.sidebar.columns([0.8, 0.2])
            
            with col1:
                label = f"🆔 {chat.get('title', 'Unknown')[:20]}"
                if st.button(label, key=f"c_{chat_id}", use_container_width=True):
                    ld = load_chat(chat_id, st.session_state.token)
                    st.session_state.chat_id = chat_id
                    st.session_state.messages = ld.get("messages", [])
                    st.rerun()
            
            with col2:
                if st.button("🗑️", key=f"del_{chat_id}"):
                    # Execute delete via API
                    requests.delete(
                        f"http://localhost:8000/history/delete/{chat_id}",
                        headers={"Authorization": f"Bearer {st.session_state.token}"}
                    )
                    # If the deleted chat was currently open, reset it
                    if st.session_state.chat_id == chat_id:
                        st.session_state.chat_id = None
                        st.session_state.messages = []
                    st.rerun()
    except: pass

# CHAT
if not st.session_state.messages:
    name = st.session_state.user_email.split("@")[0].title()
    st.markdown(f"""
        <div style='margin-top: 120px; text-align: center;'>
            <h1 style='font-size: 3.5rem; font-weight: 800; color: #FFFFFF;'>Ready for input, {name}.</h1>
            <p style='color: #8B949E; font-size: 1.2rem;'>Agent core synchronized. Orchestration engine is idling.</p>
        </div>
    """, unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant":
            st.markdown("""
                <div class='agent-identity'>
                    <div class='agent-avatar'>S</div>
                    <div class='agent-name'>Shark Engine Core</div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown(msg["content"])

prompt = st.chat_input("Message Shark Engine...")

if prompt:
    if not st.session_state.chat_id:
        new_chat = create_chat(st.session_state.user_email, st.session_state.token)
        st.session_state.chat_id = new_chat["chat_id"]

    st.session_state.messages.append({"role": "user", "content": prompt})
    save_message(st.session_state.chat_id, "user", prompt, st.session_state.token)

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        st.markdown("""
            <div class='agent-identity'>
                <div class='agent-avatar'>S</div>
                <div class='agent-name'>Shark Engine Core</div>
            </div>
        """, unsafe_allow_html=True)
        
        status_box = st.empty()
        response_box = st.empty()
        
        full_text = ""
        
        try:
            payload = {
                "message": prompt,
                "resume_text": st.session_state.resume_text,
                "history": st.session_state.messages
            }
            
            # SSE streaming call
            response = requests.post(
                "http://localhost:8000/chat/run",
                json=payload,
                headers={"Authorization": f"Bearer {st.session_state.token}"},
                stream=True
            )
            
            for line in response.iter_lines():
                if line:
                    decoded = line.decode("utf-8")
                    if decoded.startswith("data: "):
                        data = json.loads(decoded[6:])
                        
                        if data["type"] == "status":
                            status_box.markdown(f"<div class='status-msg'><div class='status-pulse'></div>{data['content']}</div>", unsafe_allow_html=True)
                        
                        elif data["type"] == "token":
                            status_box.empty() # Clear status when text starts streaming
                            full_text += data["content"]
                            response_box.markdown(full_text)
                            
            if full_text:
                save_message(st.session_state.chat_id, "assistant", full_text, st.session_state.token)
                st.session_state.messages.append({"role": "assistant", "content": full_text})
            
        except Exception as e:
            st.error(f"Signal Failure: {str(e)}")