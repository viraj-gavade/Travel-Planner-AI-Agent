"""
Weather Lookup Tool - Fetch weather forecasts for a location.
"""

import json
from typing import List
from langchain.tools import tool
import requests
from datetime import datetime, timedelta


def _fetch_weather(latitude: float, longitude: float, days: int = 7) -> dict:
    """
    Internal helper to fetch weather forecast for a location using Open-Meteo API.
    
    Args:
        latitude: Latitude of the location (between -90 and 90)
        longitude: Longitude of the location (between -180 and 180)
        days: Number of days to forecast (default: 7)
    
    Returns:
        Dictionary containing weather forecast data or error message
    """
    try:
        # Validate coordinates
        if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
            return {"error": "Invalid coordinates. Latitude: -90 to 90, Longitude: -180 to 180."}
        
        # Limit days to API maximum (16 days for forecast)
        days = min(days, 16)
        
        # Use the FORECAST API (not archive) for future dates
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": "temperature_2m_max,temperature_2m_min,weather_code",
            "timezone": "auto",
            "forecast_days": days
        }
        
        # Make API request
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Process weather data
        forecast_list = []
        daily_data = data.get('daily', {})
        
        dates_list = daily_data.get('time', [])
        temps_max = daily_data.get('temperature_2m_max', [])
        temps_min = daily_data.get('temperature_2m_min', [])
        weather_codes = daily_data.get('weather_code', [])
        
        # Weather code to condition mapping (simplified)
        weather_conditions = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Foggy",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Slight snow",
            73: "Moderate snow",
            75: "Heavy snow",
            80: "Slight showers",
            81: "Moderate showers",
            82: "Violent showers",
            85: "Slight snow showers",
            86: "Heavy snow showers",
            95: "Thunderstorm",
            96: "Thunderstorm with hail",
            99: "Thunderstorm with hail"
        }
        
        for i, date in enumerate(dates_list):
            code = weather_codes[i] if i < len(weather_codes) else 0
            condition = weather_conditions.get(code, "Unknown")
            
            forecast_list.append({
                "date": date,
                "temperature_2m_max": temps_max[i] if i < len(temps_max) else None,
                "temperature_2m_min": temps_min[i] if i < len(temps_min) else None,
                "weather_condition": condition,
                "weather_code": code
            })
        
        # Return clean domain data (no success flag)
        return {
            "forecast": forecast_list,
            "location": {
                "latitude": latitude,
                "longitude": longitude,
                "timezone": data.get('timezone', 'UTC')
            },
            "days_requested": days
        }
    
    except requests.RequestException as e:
        return {"error": f"Weather API request failed: {str(e)}"}
    except Exception as e:
        return {"error": f"Weather data processing failed: {str(e)}"}


# Location coordinates for major Indian cities
CITY_COORDINATES = {
    "Delhi": (28.7041, 77.1025),
    "Mumbai": (19.0760, 72.8777),
    "Bangalore": (12.9716, 77.5946),
    "Goa": (15.4909, 73.8278),
    "Hyderabad": (17.3850, 78.4867),
    "Chennai": (13.0827, 80.2707),
    "Kolkata": (22.5726, 88.3639),
    "Jaipur": (26.9124, 75.7873),
    "Pune": (18.5204, 73.8567),
    "Ahmedabad": (23.0225, 72.5714),
}


@tool
def get_weather_for_city(input: str) -> dict:
    """
    Get weather forecast for a major Indian city.

    Expected input format (JSON string):
    {"city": "Goa", "days": 7}
    
    Args:
        input: JSON string with city (required), days (optional: 1-14)
    
    Returns:
        Dictionary containing weather forecast for the city or error message
    """
    # Debug logging
    print(f"[DEBUG get_weather_for_city] raw input = {input}")
    
    # Parse input - handle both string and dict
    if isinstance(input, str):
        try:
            params = json.loads(input)
        except json.JSONDecodeError:
            return {"error": f"Invalid JSON input. Available cities: {list(CITY_COORDINATES.keys())}"}
    elif isinstance(input, dict):
        params = input
    else:
        return {"error": "Invalid input type. Expected JSON string or dict."}
    
    # Extract parameters
    city = params.get("city", "")
    days = params.get("days", 7)
    
    # Input validation
    if not city or not str(city).strip():
        return {"error": f"city is required. Available cities: {list(CITY_COORDINATES.keys())}"}
    
    city = str(city).strip()
    if city not in CITY_COORDINATES:
        return {"error": f"City '{city}' not available. Choose from: {list(CITY_COORDINATES.keys())}"}
    
    lat, lon = CITY_COORDINATES[city]
    return _fetch_weather(lat, lon, days=days)
