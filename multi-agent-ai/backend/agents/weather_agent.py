import re
from backend.tools.weather_tool import get_weather
from backend.tools.forecast_tool import get_weather_forecast

# =========================================================
# HELPERS
# =========================================================

def detect_weather_type(query):
    query = query.lower()
    if "next 10 days" in query or "next 5 days" in query:
        return "forecast_long"
    elif "forecast" in query:
        return "forecast"
    elif "weather report" in query:
        return "detailed_report"
    elif "temperature" in query:
        return "temperature"
    return "current_weather"

def extract_city(query):
    patterns = [
        r"weather in ([A-Za-z ]+)",
        r"weather of ([A-Za-z ]+)",
        r"temperature of ([A-Za-z ]+)",
        r"forecast of ([A-Za-z ]+)",
        r"weather report of ([A-Za-z ]+)"
    ]
    for pattern in patterns:
        match = re.search(pattern, query.lower())
        if match:
            city = match.group(1)
            # Remove specific trailing filler phrases
            city = city.replace("and give me weather report", "")
            city = city.replace("for next 10 days", "")
            return city.strip().title()
    return None

# =========================================================
# WEATHER AGENT
# =========================================================

def weather_agent(state):
    query = state["question"]
    results_state = state.get("results", {})
    
    # 1. Intent & City Detection
    weather_type = detect_weather_type(query)
    
    # Priority: Supervisor Extracted City -> Regex Extraction -> Default
    city = results_state.get("extracted_city")
    if not city:
        city = extract_city(query)
    if not city:
        city = "Delhi"
        
    print(f"[DEBUG] Weather Agent | Intent: {weather_type} | City: {city}")

    # 2. Guardrails
    if len(city.split()) > 3:
        return {"result": f"❌ Invalid city name identified: {city}"}

    # 3. Tool Selection
    if weather_type in ["forecast_long", "forecast", "detailed_report"]:
        print(f"[DEBUG] Executing Forecast Tool for {city}")
        result = get_weather_forecast.invoke({"city": city})
    else:
        print(f"[DEBUG] Executing Current Weather Tool for {city}")
        result = get_weather.invoke({"city": city})

    return {
        "result": result
    }
