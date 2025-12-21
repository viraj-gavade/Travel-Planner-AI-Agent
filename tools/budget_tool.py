"""
Budget Estimation Tool - Calculate total trip cost breakdown.
ReAct-safe implementation using single dict input pattern.
"""

import json
from langchain.tools import tool


def _parse_int(value, default=0):
    """Safely parse an integer value."""
    if value is None:
        return default
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


@tool
def budget_estimation_tool(input) -> dict:
    """
    Estimate the total cost of a trip with breakdown.

    Accepts either a dict or a JSON string as input.
    Expected input format:
    {
      "flight_cost": 3800,
      "hotel_cost_per_night": 4000,
      "number_of_days": 4,
      "daily_expenses": 1000
    }
    
    Args:
        input: Dictionary or JSON string with flight_cost, hotel_cost_per_night, number_of_days (all required), daily_expenses (optional)
    
    Returns:
        Dictionary containing cost breakdown or error message
    """
    # Debug logging
    print(f"[DEBUG budget_estimation_tool] raw input = {input}")

    # Accept both dict and JSON string
    if isinstance(input, str):
        try:
            params = json.loads(input)
        except json.JSONDecodeError:
            return {"error": "Invalid JSON input. Expected format: {\"flight_cost\": ..., ...}"}
    elif isinstance(input, dict):
        params = input
    else:
        return {"error": "Invalid input type. Expected JSON string or dict."}

    # Extract parameters from params dict
    flight_cost = _parse_int(params.get("flight_cost", 0))
    hotel_cost_per_night = _parse_int(params.get("hotel_cost_per_night", 0))
    number_of_days = _parse_int(params.get("number_of_days", 0))
    daily_expenses = _parse_int(params.get("daily_expenses", 1000), 1000)

    # Input validation
    if flight_cost == 0 and hotel_cost_per_night == 0 and number_of_days == 0:
        return {"error": "flight_cost, hotel_cost_per_night, and number_of_days are required."}

    if number_of_days == 0:
        return {"error": "number_of_days must be greater than 0."}

    if any(x < 0 for x in [flight_cost, hotel_cost_per_night, number_of_days, daily_expenses]):
        return {"error": "All costs must be non-negative values."}

    # Calculate costs
    hotel_total = hotel_cost_per_night * number_of_days
    daily_expenses_total = daily_expenses * number_of_days
    total_estimate = flight_cost + hotel_total + daily_expenses_total
    per_day_average = total_estimate / number_of_days

    return {
        "total_estimate": total_estimate,
        "flight_cost": flight_cost,
        "hotel_total": hotel_total,
        "hotel_per_night": hotel_cost_per_night,
        "daily_expenses_total": daily_expenses_total,
        "number_of_days": number_of_days,
        "per_day_average": round(per_day_average, 2),
        "currency": "INR",
        "summary": f"Total trip cost: Rs {total_estimate:,} for {number_of_days} days"
    }


@tool
def quick_budget_calculator(input: str) -> dict:
    """
    Quick budget calculator to suggest hotel and daily expenses allocation.

    Expected input format (JSON string):
    {"total_budget": 50000, "number_of_days": 4, "flight_cost": 3800}
    
    Args:
        input: JSON string with total_budget, number_of_days (required), flight_cost (optional)
    
    Returns:
        Dictionary containing budget allocation suggestions or error message
    """
    # Debug logging
    print(f"[DEBUG quick_budget_calculator] raw input = {input}")
    
    # Parse input - handle both string and dict
    if isinstance(input, str):
        try:
            params = json.loads(input)
        except json.JSONDecodeError:
            return {"error": "Invalid JSON input. Expected format: {\"total_budget\": ..., \"number_of_days\": ...}"}
    elif isinstance(input, dict):
        params = input
    else:
        return {"error": "Invalid input type. Expected JSON string or dict."}
    
    # Extract parameters from params dict
    total_budget = _parse_int(params.get("total_budget", 0))
    number_of_days = _parse_int(params.get("number_of_days", 0))
    flight_cost = _parse_int(params.get("flight_cost", 0))
    
    # Input validation
    if total_budget == 0 or number_of_days == 0:
        return {"error": "total_budget and number_of_days are required and must be greater than 0."}
    
    if total_budget <= 0 or number_of_days <= 0:
        return {"error": "Budget and days must be positive values."}
    
    remaining_budget = total_budget - flight_cost
    
    if remaining_budget < 0:
        return {"error": "Flight cost exceeds total budget. Increase budget or find cheaper flights."}
    
    # Suggest 60% for hotels, 40% for daily expenses
    hotel_budget = int(remaining_budget * 0.6)
    daily_budget = int(remaining_budget * 0.4)
    hotel_per_night = hotel_budget / number_of_days
    daily_per_day = daily_budget / number_of_days
    
    return {
        "total_budget": total_budget,
        "flight_cost": flight_cost,
        "remaining_budget": remaining_budget,
        "hotel_per_night": round(hotel_per_night, 2),
        "daily_expenses_per_day": round(daily_per_day, 2),
        "number_of_days": number_of_days,
        "recommendation": f"For Rs {total_budget:,} budget, allocate Rs {round(hotel_per_night, 0):.0f}/night for hotel"
    }

