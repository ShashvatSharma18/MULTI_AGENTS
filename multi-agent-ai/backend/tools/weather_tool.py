import os
import requests
from langchain_core.tools import tool

# =========================================================
# WEATHER TOOL
# =========================================================

@tool
def get_weather(city: str) -> str:
    """Get current weather of city"""

    api_key = os.getenv("WEATHER_API_KEY")

    if not api_key:
        return "❌ Weather API key not configured"

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:

        response = requests.get(url)

        data = response.json()

        if response.status_code != 200:
            return "❌ City not found"

        temp = data["main"]["temp"]
        weather = data["weather"][0]["description"]

        return f"🌤️ Weather in {city}: {temp}°C, {weather}"

    except Exception as e:
        return f"❌ Weather Error: {str(e)}"
