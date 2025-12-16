"""
Hotel Recommendation Tool - Find the best hotels in a destination city.
ReAct-safe implementation using single string input pattern.
"""

import json
import os
from langchain.tools import tool


@tool
def hotel_recommendation_tool(input: str) -> dict:
    """
    Recommend the best hotel in a city based on budget level and ratings.

    Expected input format (JSON string):
    {"city": "Goa", "budget_level": "medium"}
    
    Args:
        input: JSON string with city (required), budget_level (optional: low/medium/flexible)
    
    Returns:
        Dictionary containing hotel details or error message
    """
    # Debug logging
    print(f"[DEBUG hotel_recommendation_tool] raw input = {input}")
    
    # Parse input - handle both string and dict
    if isinstance(input, str):
        try:
            params = json.loads(input)
        except json.JSONDecodeError:
            return {"error": "Invalid JSON input. Expected format: {\"city\": \"...\"}"}
    elif isinstance(input, dict):
        params = input
    else:
        return {"error": "Invalid input type. Expected JSON string or dict."}
    
    # Extract parameters
    city = params.get("city", "")
    budget_level = params.get("budget_level", "medium")
    
    # Input validation
    if not city or not str(city).strip():
        return {"error": "city is required. Please provide a destination city."}
    
    # Normalize budget level
    budget = budget_level.lower().strip() if budget_level else "medium"
    if budget not in ["low", "medium", "flexible"]:
        budget = "medium"
    
    # Get the data directory path
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
    hotels_file = os.path.join(data_dir, "hotels.json")
    
    try:
        with open(hotels_file, "r", encoding="utf-8") as f:
            all_hotels = json.load(f)
    except FileNotFoundError:
        return {"error": "Hotel database not found."}
    except json.JSONDecodeError:
        return {"error": "Hotel database is corrupted."}
    
    # Filter hotels by city
    city_lower = str(city).strip().lower()
    hotels = [h for h in all_hotels if h.get("city", "").lower() == city_lower]
    
    if not hotels:
        return {"error": f"No hotels found in {city}. Try a different city."}
    
    # Define budget ranges
    budget_ranges = {
        "low": (0, 3000),
        "medium": (3000, 6000),
        "flexible": (0, float('inf'))
    }
    
    min_price, max_price = budget_ranges.get(budget, (3000, 6000))
    
    # Filter by budget
    filtered_hotels = [
        h for h in hotels
        if min_price <= h.get('price_per_night', 0) <= max_price
    ]
    
    if not filtered_hotels:
        filtered_hotels = sorted(hotels, key=lambda x: x.get('price_per_night', 0))[:3]
    
    # Sort by value (stars/price ratio)
    for hotel in filtered_hotels:
        price = hotel.get('price_per_night', 1)
        stars = hotel.get('stars', 1)
        hotel['value_score'] = stars / (price / 1000)
    
    best_hotel = max(filtered_hotels, key=lambda x: x.get('value_score', 0))
    
    return {
        "hotel_name": best_hotel.get("name"),
        "city": best_hotel.get("city"),
        "stars": best_hotel.get("stars"),
        "price_per_night": best_hotel.get("price_per_night"),
        "amenities": best_hotel.get("amenities", []),
        "selection_reason": f"Best value {budget} budget option"
    }
