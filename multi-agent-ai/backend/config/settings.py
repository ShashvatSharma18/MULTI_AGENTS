import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# =========================================================
# TRACING & LANGSMITH
# =========================================================

os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGCHAIN_TRACING_V2", "true")
os.environ["LANGSMITH_TRACING"] = os.getenv("LANGSMITH_TRACING", "true")

# =========================================================
# API KEYS
# =========================================================

MAIN_GROQ_API_KEY = os.getenv("MAIN_GROQ_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

