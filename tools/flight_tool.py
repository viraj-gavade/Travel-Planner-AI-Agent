"""
Flight Search Tool - Find and recommend the best flights between cities.
ReAct-safe implementation using single string input pattern.
"""

import json
import os
from langchain.tools import tool


@tool
def flight_search_tool(input: str) -> dict:
    """
    Search and return the best flight between two cities.

    Expected input format (JSON string):
    {"source_city": "Delhi", "destination_city": "Goa", "preference": "cheapest"}
    
    Args:
        input: JSON string with source_city (required), destination_city (required), preference (optional)
    
    Returns:
        Dictionary containing flight information or error message
    """
    # Debug logging
    print(f"[DEBUG flight_search_tool] raw input = {input}")
    
    # Parse input - handle both string and dict
    if isinstance(input, str):
        try:
            params = json.loads(input)
        except json.JSONDecodeError:
            return {"error": "Invalid JSON input. Expected format: {\"source_city\": \"...\", \"destination_city\": \"...\"}"}
    elif isinstance(input, dict):
        params = input
    else:
        return {"error": "Invalid input type. Expected JSON string or dict."}
    
    # Extract parameters
    source_city = params.get("source_city", "")
    destination_city = params.get("destination_city", "")
    preference = params.get("preference", "cheapest")
    
    # Validate inputs
    if not source_city or not destination_city:
        return {"error": "Both source_city and destination_city are required."}
    
    # Get the data directory path
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
    flights_file = os.path.join(data_dir, "flights.json")
    
    # Load dataset
    try:
        with open(flights_file, "r", encoding="utf-8") as f:
            flights = json.load(f)
    except FileNotFoundError:
        return {"error": "Flight database not found."}
    except json.JSONDecodeError:
        return {"error": "Flight database is corrupted."}
    
    # Normalize inputs
    src = source_city.strip().lower()
    dst = destination_city.strip().lower()
    pref = preference.strip().lower() if preference else "cheapest"
    
    # Filter flights
    matches = [
        f for f in flights
        if f.get("from", "").lower() == src
        and f.get("to", "").lower() == dst
    ]
    
    if not matches:
        return {"error": f"No flights found from {source_city} to {destination_city}."}
    
    # Select best flight based on preference
    if pref == "fastest" and "arrival_time" in matches[0]:
        selected = sorted(matches, key=lambda x: x.get("arrival_time", ""))[0]
        reason = "Fastest available flight"
    else:
        selected = sorted(matches, key=lambda x: x.get("price", float("inf")))[0]
        reason = "Lowest cost among available flights"
    
    return {
        "flight_id": selected.get("flight_id"),
        "airline": selected.get("airline"),
        "from": selected.get("from"),
        "to": selected.get("to"),
        "departure_time": selected.get("departure_time"),
        "arrival_time": selected.get("arrival_time"),
        "price": selected.get("price"),
        "selection_reason": reason
    }
