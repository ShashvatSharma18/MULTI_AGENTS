import requests
import os
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()

@tool
def get_weather_forecast(city: str):
    """Get the weather forecast for the next 5 days for a given city."""
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        return "❌ Weather API key not configured"

    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200:
            return f"❌ Error: {data.get('message', 'City not found')}"

        forecasts = data.get("list", [])
        if not forecasts:
            return "❌ No forecast data available."

        summary = f"📅 5-Day Forecast for {city}:\n"
        
        # Simple grouping: take one reading per day
        daily_data = {}
        for f in forecasts:
            date = f["dt_txt"].split(" ")[0]
            if date not in daily_data:
                daily_data[date] = {
                    "temp": f["main"]["temp"],
                    "desc": f["weather"][0]["description"]
                }
        
        for date, info in list(daily_data.items())[:5]:
            summary += f"- {date}: {info['temp']}°C, {info['desc']}\n"

        return summary

    except Exception as e:
        return f"❌ Forecast API call failed: {str(e)}"