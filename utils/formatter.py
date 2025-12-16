"""
Output formatting utilities for travel itineraries and recommendations.
"""

from typing import Dict, List, Any
from datetime import datetime


def format_flight_info(flight: Dict[str, Any]) -> str:
    """
    Format flight information for display.
    
    Args:
        flight: Flight dictionary
    
    Returns:
        Formatted flight string
    """
    if not flight:
        return "No flight information available"
    
    departure = flight.get('departure_time', 'N/A')
    arrival = flight.get('arrival_time', 'N/A')
    price = flight.get('price', 'N/A')
    airline = flight.get('airline', 'N/A')
    from_city = flight.get('from', 'N/A')
    to_city = flight.get('to', 'N/A')
    
    return (f"✈️ {airline}\n"
            f"   Route: {from_city} → {to_city}\n"
            f"   Departure: {departure}\n"
            f"   Arrival: {arrival}\n"
            f"   Price: ₹{price:,}")


def format_hotel_info(hotel: Dict[str, Any]) -> str:
    """
    Format hotel information for display.
    
    Args:
        hotel: Hotel dictionary
    
    Returns:
        Formatted hotel string
    """
    if not hotel:
        return "No hotel information available"
    
    name = hotel.get('name', 'N/A')
    city = hotel.get('city', 'N/A')
    stars = hotel.get('stars', 'N/A')
    price = hotel.get('price_per_night', 'N/A')
    amenities = ", ".join(hotel.get('amenities', []))
    
    return (f"🏨 {name}\n"
            f"   City: {city}\n"
            f"   Rating: {'⭐' * stars}\n"
            f"   Price per Night: ₹{price:,}\n"
            f"   Amenities: {amenities}")


def format_place_info(place: Dict[str, Any]) -> str:
    """
    Format place/attraction information for display.
    
    Args:
        place: Place dictionary
    
    Returns:
        Formatted place string
    """
    if not place:
        return "No place information available"
    
    name = place.get('name', 'N/A')
    place_type = place.get('type', 'N/A')
    rating = place.get('rating', 'N/A')
    city = place.get('city', 'N/A')
    
    return f"📍 {name} ({place_type.title()})\n   Rating: {rating}/5.0 | City: {city}"


def format_weather_info(weather: Dict[str, Any]) -> str:
    """
    Format weather information for display.
    
    Args:
        weather: Weather dictionary
    
    Returns:
        Formatted weather string
    """
    if not weather:
        return "No weather information available"
    
    date = weather.get('date', 'N/A')
    temp_min = weather.get('temperature_2m_min', 'N/A')
    temp_max = weather.get('temperature_2m_max', 'N/A')
    condition = weather.get('weather_condition', 'N/A')
    
    return f"🌤️  {date}: {condition} | Min: {temp_min}°C | Max: {temp_max}°C"


def format_budget_breakdown(budget: Dict[str, Any]) -> str:
    """
    Format budget breakdown for display.
    
    Args:
        budget: Budget dictionary with costs
    
    Returns:
        Formatted budget string
    """
    if not budget:
        return "No budget information available"
    
    flight = budget.get('flight_cost', 0)
    hotel = budget.get('hotel_total', 0)
    daily = budget.get('daily_expenses_total', 0)
    total = budget.get('total_estimate', 0)
    
    return (f"💰 Budget Breakdown:\n"
            f"   Flight: ₹{flight:,}\n"
            f"   Hotel (Total): ₹{hotel:,}\n"
            f"   Daily Expenses: ₹{daily:,}\n"
            f"   ─────────────────\n"
            f"   Total Estimate: ₹{total:,}")


def format_itinerary(itinerary: List[Dict[str, Any]]) -> str:
    """
    Format day-wise itinerary for display.
    
    Args:
        itinerary: List of daily plans
    
    Returns:
        Formatted itinerary string
    """
    if not itinerary:
        return "No itinerary available"
    
    formatted = "📅 Day-wise Itinerary:\n"
    for i, day in enumerate(itinerary, 1):
        formatted += f"\nDay {i}:\n"
        formatted += f"  Activities: {day.get('activities', 'Rest day')}\n"
        formatted += f"  Meals: {day.get('meals', 'N/A')}\n"
        formatted += f"  Notes: {day.get('notes', 'N/A')}\n"
    
    return formatted
