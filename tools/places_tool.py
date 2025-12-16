"""
Places Discovery Tool - Find attractions and places of interest in a city.
ReAct-safe implementation using single string input pattern.
"""

import json
import os
from langchain.tools import tool


@tool
def places_discovery_tool(input: str) -> dict:
    """
    Discover attractions and places in a city based on interests.

    Expected input format (JSON string):
    {"city": "Goa", "interests": "beach,temple"}
    
    Args:
        input: JSON string with city (required), interests (optional: comma-separated types)
    
    Returns:
        Dictionary containing recommended places or error message
    """
    # Debug logging
    print(f"[DEBUG places_discovery_tool] raw input = {input}")
    
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
    interests = params.get("interests", "")
    
    # Input validation
    if not city or not str(city).strip():
        return {"error": "city is required. Please provide a destination city."}
    
    # Get the data directory path
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
    places_file = os.path.join(data_dir, "places.json")
    
    try:
        with open(places_file, "r", encoding="utf-8") as f:
            all_places = json.load(f)
    except FileNotFoundError:
        return {"error": "Places database not found."}
    except json.JSONDecodeError:
        return {"error": "Places database is corrupted."}
    
    # Filter places by city
    city_lower = str(city).strip().lower()
    places = [p for p in all_places if p.get("city", "").lower() == city_lower]
    
    if not places:
        return {"error": f"No places found in {city}. Try a different city."}
    
    # Parse interests from comma-separated string
    interests_list = []
    if interests and str(interests).strip():
        interests_list = [i.strip().lower() for i in str(interests).split(',') if i.strip()]
    
    # Filter by interests if provided
    if interests_list:
        filtered_places = [
            p for p in places
            if p.get('type', '').lower() in interests_list
        ]
        
        if not filtered_places:
            filtered_places = places
            note = f"No places matched interests '{interests}', showing all places"
        else:
            note = f"Found {len(filtered_places)} places matching interests"
    else:
        filtered_places = places
        note = f"Showing top-rated places in {city}"
    
    # Sort by rating (descending)
    sorted_places = sorted(
        filtered_places,
        key=lambda x: x.get('rating', 0),
        reverse=True
    )
    
    # Return top 5 places
    top_places = []
    for p in sorted_places[:5]:
        top_places.append({
            "name": p.get("name"),
            "type": p.get("type"),
            "rating": p.get("rating"),
            "description": p.get("description", "")
        })
    
    return {
        "places": top_places,
        "count": len(top_places),
        "note": note
    }
