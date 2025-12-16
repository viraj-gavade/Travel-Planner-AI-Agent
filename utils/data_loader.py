"""
Data loader utilities for loading and caching JSON datasets.
"""

import json
import os
from pathlib import Path
from typing import Any, List, Dict

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent


def load_json_data(filename: str) -> List[Dict[str, Any]]:
    """
    Load JSON data from the data directory.
    
    Args:
        filename: Name of the JSON file (e.g., 'flights.json')
    
    Returns:
        List of dictionaries containing the data
    
    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file is not valid JSON
    """
    file_path = PROJECT_ROOT / "data" / filename
    
    if not file_path.exists():
        raise FileNotFoundError(f"Data file not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return data


def get_flights() -> List[Dict[str, Any]]:
    """Load flights data."""
    return load_json_data('flights.json')


def get_hotels() -> List[Dict[str, Any]]:
    """Load hotels data."""
    return load_json_data('hotels.json')


def get_places() -> List[Dict[str, Any]]:
    """Load places data."""
    return load_json_data('places.json')


def filter_flights(source_city: str, destination_city: str) -> List[Dict[str, Any]]:
    """
    Filter flights by source and destination cities.
    
    Args:
        source_city: Source city name
        destination_city: Destination city name
    
    Returns:
        List of matching flights
    """
    flights = get_flights()
    filtered = [
        f for f in flights
        if f.get('from', '').lower() == source_city.lower()
        and f.get('to', '').lower() == destination_city.lower()
    ]
    return filtered


def filter_hotels(city: str) -> List[Dict[str, Any]]:
    """
    Filter hotels by city.
    
    Args:
        city: City name
    
    Returns:
        List of matching hotels
    """
    hotels = get_hotels()
    filtered = [h for h in hotels if h.get('city', '').lower() == city.lower()]
    return filtered


def filter_places(city: str) -> List[Dict[str, Any]]:
    """
    Filter places by city.
    
    Args:
        city: City name
    
    Returns:
        List of matching places
    """
    places = get_places()
    filtered = [p for p in places if p.get('city', '').lower() == city.lower()]
    return filtered
