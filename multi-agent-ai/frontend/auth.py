import requests
import streamlit as st

BASE_URL = "http://127.0.0.1:8000"

def signup(username, email, password):
    # Depending on our UserSignup model, we'll send email and password.
    # Note: Our current FastAPI model backend/routes/auth_routes.py UserSignup only has email and password.
    # I will include username if you decide to add it later, but for now matching the API model.
    response = requests.post(
        f"{BASE_URL}/auth/signup",
        json={
            "email": email,
            "password": password
        }
    )
    return response

def login(email, password):
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "email": email,
            "password": password
        }
    )
    return response
