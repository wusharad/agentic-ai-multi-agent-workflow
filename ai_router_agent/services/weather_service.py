# Calls ai_weather_agent API
import requests

WEATHER_AGENT_URL = "http://localhost:8003/weather/query"

def call_weather_agent(payload: dict, trace_id: str):
    print(f"[{trace_id}] Agent called: WEATHER_AGENT")
    # return requests.post(WEATHER_AGENT_URL, json=payload).json()
    # Temporary mock response until weather service is available
    response = {
        "location": "Mumbai",
        "date": "2026-01-14",
        "forecast": {
            "condition": "Partly Cloudy",
            "temperature_celsius": 29,
            "humidity_percent": 68,
            "chance_of_rain_percent": 20
        },
        "status": "SUCCESS"
    }

    return response
