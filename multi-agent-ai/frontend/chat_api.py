import requests
import streamlit as st

BASE_URL = "http://127.0.0.1:8000"

def create_chat(user_email, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        f"{BASE_URL}/history/create",
        json={
            "user_email": user_email,
            "title": "New Chat"
        },
        headers=headers
    )
    return response.json()

def save_message(chat_id, role, content, token):
    headers = {"Authorization": f"Bearer {token}"}
    requests.post(
        f"{BASE_URL}/history/message",
        json={
            "chat_id": chat_id,
            "role": role,
            "content": content
        },
        headers=headers
    )

def get_user_chats(user_email, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{BASE_URL}/history/user/{user_email}",
        headers=headers
    )
    return response.json()

def load_chat(chat_id, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{BASE_URL}/history/{chat_id}",
        headers=headers
    )
    return response.json()

