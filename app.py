"""
Streamlit UI for Travel Planner Agent powered by Groq LLM.

This application uses Groq (free tier available) instead of OpenAI for LLM inference.
Groq provides fast, reliable cloud-based LLM access without OpenAI costs.
"""

import streamlit as st
import json
from datetime import datetime, timedelta
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent.travel_agent import create_travel_agent
from utils.formatter import (
    format_flight_info, format_hotel_info, format_place_info,
    format_weather_info, format_budget_breakdown
)

# Configure page
st.set_page_config(
    page_title="🌍 Travel Planner AI Agent",
    page_icon="🧳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 0rem;
    }
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 1.2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid #28a745;
    }
    .error-box {
        background-color: #f8d7da;
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid #dc3545;
    }
    </style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables."""
    if 'agent' not in st.session_state:
        st.session_state.agent = create_travel_agent()
    if 'trip_result' not in st.session_state:
        st.session_state.trip_result = None
    if 'planning_in_progress' not in st.session_state:
        st.session_state.planning_in_progress = False


def render_header():
    """Render the application header."""
    col1, col2 = st.columns([1, 4])
    with col1:
        st.markdown("# 🌍")
    with col2:
        st.title("Travel Planner AI Agent")
    st.markdown("*Your intelligent travel planning companion powered by Groq LLM (Free & Fast)*")
    st.divider()


def render_sidebar_inputs():
    """Render input controls in sidebar."""
    st.sidebar.header("✈️ Trip Details")
    
    # Verbose toggle at top
    st.sidebar.subheader("🔧 Settings")
    show_verbose = st.sidebar.checkbox(
        "Show Agent Reasoning (Verbose)",
        value=True,
        help="Display the agent's thought process, actions, and observations"
    )
    
    st.sidebar.divider()
    
    # Trip type
    trip_type = st.sidebar.radio(
        "Trip Type",
        ["Domestic", "International"]
    )
    
    # Cities
    st.sidebar.subheader("📍 Cities")
    source_city = st.sidebar.text_input(
        "Source City",
        value="Delhi",
        help="Your starting city"
    )
    
    destination_city = st.sidebar.text_input(
        "Destination City",
        value="Goa",
        help="Your target destination"
    )
    
    # Travel dates
    st.sidebar.subheader("📅 Travel Dates")
    start_date = st.sidebar.date_input(
        "Start Date",
        value=datetime.now() + timedelta(days=7),
        min_value=datetime.now()
    )
    
    number_of_days = st.sidebar.slider(
        "Duration (Days)",
        min_value=1,
        max_value=30,
        value=4,
        step=1
    )
    
    # Budget
    st.sidebar.subheader("💰 Budget")
    total_budget = st.sidebar.number_input(
        "Total Budget (₹)",
        min_value=5000,
        value=50000,
        step=5000,
        help="Your total trip budget in rupees"
    )
    
    budget_level = st.sidebar.selectbox(
        "Budget Level",
        ["low", "medium", "flexible"],
        help="Hotel budget preference"
    )
    
    # Preferences
    st.sidebar.subheader("🎯 Preferences")
    flight_preference = st.sidebar.radio(
        "Flight Preference",
        ["Cheapest", "Fastest"],
        help="Choose your flight priority"
    )
    
    # Interests
    interests = st.sidebar.multiselect(
        "Interests",
        [
            "temple", "museum", "fort", "lake", "beach",
            "park", "restaurant", "market", "monument"
        ],
        default=["temple", "beach"],
        help="Select attractions you're interested in"
    )
    
    return {
        "trip_type": trip_type,
        "source_city": source_city,
        "destination_city": destination_city,
        "start_date": start_date,
        "number_of_days": number_of_days,
        "total_budget": total_budget,
        "budget_level": budget_level,
        "flight_preference": flight_preference.lower(),
        "interests": interests,
        "show_verbose": show_verbose
    }


def build_query(inputs: dict) -> str:
    """
    Build the agent query from user inputs.
    
    Args:
        inputs: Dictionary of user inputs
    
    Returns:
        Formatted query string
    """
    interests_str = ", ".join(inputs["interests"]) if inputs["interests"] else "general attractions"
    
    query = f"""
    I want to plan a {inputs['number_of_days']}-day trip from {inputs['source_city']} 
    to {inputs['destination_city']} starting on {inputs['start_date'].strftime('%Y-%m-%d')}.
    
    Trip Details:
    - Total Budget: ₹{inputs['total_budget']:,}
    - Budget Level: {inputs['budget_level']}
    - Flight Preference: {inputs['flight_preference']}
    - Travel Duration: {inputs['number_of_days']} days
    - Interests: {interests_str}
    
    Please provide:
    1. Flight recommendation (with {inputs['flight_preference']} option)
    2. Hotel suggestion based on {inputs['budget_level']} budget
    3. Top attractions matching my interests
    4. Weather forecast for the dates
    5. Detailed day-wise itinerary
    6. Budget breakdown and recommendations
    
    Make sure all recommendations fit within my ₹{inputs['total_budget']:,} budget.
    """
    
    return query


def display_results(result: dict, show_verbose: bool = True):
    """
    Display the trip planning results.
    
    Args:
        result: Agent response dictionary
        show_verbose: Whether to show agent reasoning steps
    """
    if not result.get('success'):
        st.error(f"❌ Error: {result.get('error', 'Unknown error occurred')}")
        return
    
    response = result.get('response', '')
    intermediate_steps = result.get('intermediate_steps', [])
    
    # Display verbose agent reasoning FIRST (if enabled)
    if show_verbose and intermediate_steps:
        st.subheader("🧠 Agent Reasoning (Verbose)")
        
        for i, step in enumerate(intermediate_steps, 1):
            # Each step is a tuple: (AgentAction, observation)
            if isinstance(step, tuple) and len(step) == 2:
                action, observation = step
                
                # Create an expander for each step
                with st.expander(f"Step {i}: {getattr(action, 'tool', 'Unknown Tool')}", expanded=True):
                    # Tool called
                    tool_name = getattr(action, 'tool', 'Unknown')
                    tool_input = getattr(action, 'tool_input', {})
                    log = getattr(action, 'log', '')
                    
                    # Show Thought (from log)
                    if log:
                        st.markdown("**💭 Thought:**")
                        # Extract thought from log
                        thought_lines = []
                        for line in log.split('\n'):
                            if line.strip() and not line.strip().startswith('Action'):
                                thought_lines.append(line.strip())
                        if thought_lines:
                            st.info('\n'.join(thought_lines))
                    
                    # Show Action
                    st.markdown(f"**🔧 Action:** `{tool_name}`")
                    
                    # Show Action Input
                    st.markdown("**📥 Action Input:**")
                    if isinstance(tool_input, str):
                        try:
                            parsed_input = json.loads(tool_input)
                            st.json(parsed_input)
                        except:
                            st.code(tool_input)
                    else:
                        st.json(tool_input)
                    
                    # Show Observation
                    st.markdown("**👁️ Observation:**")
                    if isinstance(observation, dict):
                        # Check for errors
                        if 'error' in observation:
                            st.error(observation['error'])
                        else:
                            st.json(observation)
                    else:
                        st.code(str(observation))
            else:
                # Fallback for unexpected format
                with st.expander(f"Step {i}", expanded=False):
                    st.json(step if isinstance(step, (dict, list)) else str(step))
        
        st.divider()
    
    # Display main response
    st.subheader("✈️ Your Trip Plan")
    st.markdown(response)
    
    # Display raw intermediate steps (collapsed)
    if intermediate_steps:
        with st.expander("📊 Raw Tool Data (JSON)"):
            for i, step in enumerate(intermediate_steps, 1):
                st.markdown(f"**Step {i}:**")
                if isinstance(step, tuple) and len(step) == 2:
                    action, observation = step
                    st.json({
                        "tool": getattr(action, 'tool', 'Unknown'),
                        "tool_input": getattr(action, 'tool_input', {}),
                        "observation": observation if isinstance(observation, (dict, list, str)) else str(observation)
                    })
                else:
                    st.json(step if isinstance(step, (dict, list)) else str(step))


def render_main_content(inputs: dict):
    """
    Render the main content area.
    
    Args:
        inputs: Dictionary of user inputs
    """
    # Plan button
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("🚀 Generate Itinerary", use_container_width=True, type="primary"):
            st.session_state.planning_in_progress = True
    
    with col2:
        if st.button("🔄 Clear Results", use_container_width=True):
            st.session_state.trip_result = None
    
    # Display results
    if st.session_state.planning_in_progress:
        st.info("⏳ Planning your trip... This may take a moment.")
        
        # Build query and plan trip
        query = build_query(inputs)
        result = st.session_state.agent.plan_trip(query)
        st.session_state.trip_result = result
        st.session_state.planning_in_progress = False
        st.rerun()
    
    if st.session_state.trip_result:
        st.divider()
        display_results(st.session_state.trip_result, show_verbose=inputs.get('show_verbose', True))
        
        # Export option
        st.divider()
        st.subheader("💾 Export Trip Plan")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Download as JSON
            json_data = json.dumps(st.session_state.trip_result, indent=2, default=str)
            st.download_button(
                label="📥 Download as JSON",
                data=json_data,
                file_name=f"trip_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        with col2:
            # Download as Text
            text_data = f"""
TRIP PLAN
=========
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Query:
{st.session_state.trip_result.get('query', 'N/A')}

Response:
{st.session_state.trip_result.get('response', 'N/A')}
"""
            st.download_button(
                label="📄 Download as Text",
                data=text_data,
                file_name=f"trip_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )


def render_info_section():
    """Render information about the application."""
    with st.expander("ℹ️ About This Application"):
        st.markdown("""
        ### 🌍 Travel Planner AI Agent (Powered by Groq)
        
        This intelligent travel planning assistant helps you plan your perfect trip using AI and real data.
        **Now using Groq for fast, free LLM inference!**
        
        **Features:**
        - ✈️ Smart flight recommendations based on your preferences
        - 🏨 Hotel suggestions tailored to your budget
        - 📍 Attraction discovery based on your interests
        - 🌤️ Live weather forecasts
        - 📅 Detailed day-wise itineraries
        - 💰 Accurate budget calculations and breakdowns
        
        **How it works:**
        1. Enter your travel details in the sidebar
        2. Click "Generate Itinerary" to start planning
        3. The AI (powered by Groq) will use available tools to find the best options
        4. Review your personalized trip plan
        5. Export your itinerary as JSON or text
        
        **Tools Used:**
        - LangChain for AI agent orchestration
        - Groq for fast, free LLM inference (llama3-8b model)
        - Open-Meteo API for weather forecasts
        - Local datasets for flights, hotels, and attractions
        
        **Why Groq instead of OpenAI?**
        - ✅ Free tier available (no credit card required initially)
        - ✅ Fast inference (40+ tokens/second)
        - ✅ Reliable API uptime
        - ✅ No monthly subscription required
        - ✅ Great for demos and prototyping
        
        **Data Sources:**
        - Flights: Local JSON database
        - Hotels: Local JSON database
        - Attractions: Local JSON database
        - Weather: Open-Meteo API (free, no API key required)
        """)



def main():
    """Main application function."""
    # Initialize session state
    initialize_session_state()
    
    # Render header
    render_header()
    
    # Get sidebar inputs
    inputs = render_sidebar_inputs()
    
    # Render main content
    render_main_content(inputs)
    
    # Render info section
    st.divider()
    render_info_section()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center'>"
        "<p>🧳 Travel Planner AI Agent | Powered by LangChain & Groq</p>"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
