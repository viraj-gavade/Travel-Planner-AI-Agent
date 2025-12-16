#!/usr/bin/env python
"""
Main entry point for the Travel Planner AI Agent (powered by Groq).

This script can be used to:
1. Test individual tools
2. Run the agent from the command line
3. Start the Streamlit UI

Usage:
    python main.py [command] [args]
    
Commands:
    test-tools      Test all available tools
    test-agent      Test the travel agent with a sample query
    streamlit       Start the Streamlit UI (recommended)
    
Example:
    python main.py test-tools
    python main.py test-agent
    python main.py streamlit

Note: Set GROQ_API_KEY in .env file before running!
      Get free key from: https://console.groq.com
"""

import sys
import os
import json
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent.travel_agent import create_travel_agent
from tools.flight_tool import flight_search_tool
from tools.hotel_tool import hotel_recommendation_tool
from tools.places_tool import places_discovery_tool
from tools.weather_tool import get_weather_for_city
from tools.budget_tool import budget_estimation_tool, quick_budget_calculator


def test_tools():
    """Test all individual tools."""
    print("\n" + "="*70)
    print("🧪 TESTING INDIVIDUAL TOOLS")
    print("="*70 + "\n")
    
    # Test Flight Tool
    print("1️⃣ Testing Flight Search Tool...")
    print("-" * 50)
    try:
        flight_result = flight_search_tool(
            source_city="Delhi",
            destination_city="Goa",
            preference="cheapest"
        )
        print(f"✅ Flight Search Result:")
        print(json.dumps(flight_result, indent=2, default=str))
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "="*70 + "\n")
    
    # Test Hotel Tool
    print("2️⃣ Testing Hotel Recommendation Tool...")
    print("-" * 50)
    try:
        hotel_result = hotel_recommendation_tool(
            city="Goa",
            budget_level="medium"
        )
        print(f"✅ Hotel Recommendation Result:")
        print(json.dumps(hotel_result, indent=2, default=str))
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "="*70 + "\n")
    
    # Test Places Tool
    print("3️⃣ Testing Places Discovery Tool...")
    print("-" * 50)
    try:
        places_result = places_discovery_tool(
            city="Goa",
            interests=["beach", "temple", "museum"]
        )
        print(f"✅ Places Discovery Result:")
        print(json.dumps(places_result, indent=2, default=str))
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "="*70 + "\n")
    
    # Test Weather Tool
    print("4️⃣ Testing Weather Lookup Tool...")
    print("-" * 50)
    try:
        weather_result = get_weather_for_city(
            city="Goa",
            days=5
        )
        print(f"✅ Weather Forecast Result:")
        print(json.dumps(weather_result, indent=2, default=str))
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "="*70 + "\n")
    
    # Test Budget Tool
    print("5️⃣ Testing Budget Estimation Tool...")
    print("-" * 50)
    try:
        budget_result = budget_estimation_tool(
            flight_cost=5000,
            hotel_cost_per_night=3000,
            number_of_days=4,
            daily_expenses=1500
        )
        print(f"✅ Budget Estimation Result:")
        print(json.dumps(budget_result, indent=2, default=str))
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "="*70 + "\n")
    
    # Test Quick Budget Calculator
    print("6️⃣ Testing Quick Budget Calculator...")
    print("-" * 50)
    try:
        quick_budget_result = quick_budget_calculator(
            total_budget=50000,
            number_of_days=4,
            flight_cost=5000
        )
        print(f"✅ Quick Budget Calculator Result:")
        print(json.dumps(quick_budget_result, indent=2, default=str))
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "="*70 + "\n")


def test_agent():
    """Test the travel agent with a sample query."""
    print("\n" + "="*70)
    print("🤖 TESTING TRAVEL AGENT (Powered by Groq)")
    print("="*70 + "\n")
    
    try:
        # Create agent
        print("Creating travel agent with Groq LLM...")
        agent = create_travel_agent()
        print("✅ Agent created successfully!\n")
        
        # Sample query
        query = """
        I want to plan a 4-day trip from Delhi to Goa with a budget of ₹50,000.
        I prefer affordable flights. Please recommend a hotel, check the weather,
        and create a day-wise itinerary with attractions like beaches and temples.
        Also provide a detailed budget breakdown.
        """
        
        print("📋 Query:")
        print(query)
        print("\n" + "-"*70)
        print("🔄 Agent Processing...")
        print("-"*70 + "\n")
        
        # Plan trip
        result = agent.plan_trip(query)
        
        if result.get('success'):
            print("✅ Trip Planning Successful!\n")
            print("📝 Response:")
            print(result.get('response', 'No response'))
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
    
    except Exception as e:
        print(f"❌ Error creating/running agent: {e}")
        import traceback
        traceback.print_exc()


def show_help():
    """Show help information."""
    print(__doc__)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("\n🌍 Travel Planner AI Agent - Main Entry Point\n")
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "test-tools":
        test_tools()
    elif command == "test-agent":
        test_agent()
    elif command == "streamlit":
        print("\n🌐 Starting Streamlit UI...")
        print("Opening: http://localhost:8501")
        print("\nTo stop, press Ctrl+C\n")
        os.system("streamlit run app.py")
    elif command == "help" or command == "-h" or command == "--help":
        show_help()
    else:
        print(f"\n❌ Unknown command: {command}\n")
        show_help()


if __name__ == "__main__":
    main()
