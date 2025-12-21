"""
LangChain Travel Agent - ReAct-based agent for trip planning using Groq LLM.

Uses stable LangChain APIs with ReAct pattern for reasoning and acting.
All tools are @tool decorated and return JSON-serializable outputs.

Architecture: ReAct (Reasoning + Acting)
- Thought: Agent reasons about what information is needed
- Action: Agent selects a tool and parameters
- Observation: Tool result is provided
- Final Answer: Structured response to user
"""

import os
import json
from typing import Any, Dict, List
from dotenv import load_dotenv

# Use stable ReAct agent with Groq
from langchain.agents import AgentExecutor, create_react_agent
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.flight_tool import flight_search_tool
from tools.hotel_tool import hotel_recommendation_tool
from tools.places_tool import places_discovery_tool
from tools.weather_tool import get_weather_for_city
from tools.budget_tool import budget_estimation_tool, quick_budget_calculator

# Load environment variables
load_dotenv()


class TravelAgent:
    """
    ReAct-based Travel Planning Agent using Groq LLM.
    
    Uses the ReAct (Reasoning + Acting) pattern to:
    1. Reason about what information is needed
    2. Call appropriate tools to gather data
    3. Synthesize results into actionable recommendations
    
    All communication with tools is logged as ReAct steps:
    - Thought: What the agent is thinking
    - Action: Which tool to call
    - Observation: Result from the tool
    - Final Answer: Structured response to user
    """
    
    def __init__(self, model: str = "meta-llama/llama-4-maverick-17b-128e-instruct"):
        """
        Initialize the ReAct-based travel agent with Groq LLM.
        
        Args:
            model: Groq model to use (default: llama-3.1-70b-versatile)
                   Other options: 
                   - llama-3.2-90b-vision-preview
                   - llama-3.1-8b-instant
                   - mixtral-8x7b-32768
        """
        # Validate and initialize Groq API key
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError(
                "GROQ_API_KEY not found in environment variables.\n"
                "Please set it in .env file or as an environment variable.\n"
                "Get your free API key from: https://console.groq.com"
            )
        
        # Initialize Groq LLM with optimized settings for ReAct
        self.llm = ChatGroq(
            model=model,
            temperature=0.2,  # Lower temperature for more consistent ReAct format
            api_key=api_key,
            max_tokens=4096,  # Increased for longer responses
            timeout=60.0  # Increased timeout
        )
        
        # Setup all available tools
        self.tools = self._setup_tools()
        
        # Create the ReAct agent
        self.agent = self._create_react_agent()
        
        # Create agent executor with robust error handling and loop prevention
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=self._handle_parsing_error,  # Custom error handler
            max_iterations=7,  # Enforce short, direct chains (one per tool + final)
            max_execution_time=60,  # 1 minute timeout for faster response
            early_stopping_method="generate",  # Generate a response even if stopped
            return_intermediate_steps=True  # For debugging
        )
    
    def _handle_parsing_error(self, error: Exception) -> str:
        """
        Custom error handler for ReAct parsing errors.
        Returns a formatted message that guides the agent to provide a Final Answer.
        """
        error_msg = str(error)
        if "Could not parse LLM output" in error_msg or "Invalid Format" in error_msg:
            return (
                "I encountered a formatting issue. Let me provide a direct answer.\n"
                "Thought: I need to provide a Final Answer now.\n"
                "Final Answer: I apologize, but I encountered an issue processing your request. "
                "Please try rephrasing your question or provide more specific details about your travel plans."
            )
        return f"Error: {error_msg}. Please provide a Final Answer based on available information."
    
    def _setup_tools(self) -> List:
        """
        Setup all @tool decorated functions for the agent.
        
        Returns:
            List of tool functions with @tool decorator
        """
        # Collect all tools
        tools = [
            flight_search_tool,
            hotel_recommendation_tool,
            places_discovery_tool,
            get_weather_for_city,
            budget_estimation_tool,
            quick_budget_calculator
        ]
        
        return tools
    
    def _create_react_agent(self):
        """
        Create a ReAct (Reasoning + Acting) agent.
        
        ReAct agents follow this loop:
        1. Thought: Agent considers what to do
        2. Action: Agent selects a tool and input
        3. Observation: Tool executes and returns result
        4. ... repeat until Final Answer
        
        Returns:
            Configured ReAct agent
        """
        # Use the standard ReAct prompt from LangChain with agent_scratchpad
        # This format is compatible with create_react_agent
        from langchain.agents import create_react_agent
        from langchain.prompts import PromptTemplate
        
        # Create a streamlined ReAct prompt for efficiency
        prompt_template = """You are an expert travel planner. Answer the user's question using the available tools.
{tools}

Tool names: {tool_names}

=== REACT FORMAT ===
Thought: [what you need to do]
Action: [tool name from {tool_names}]
Action Input: {{"key": "value"}}
Observation: [tool result]
... (repeat as needed, but keep the chain as short as possible)
Thought: I have enough information
Final Answer: [complete answer]

=== RULES ===
1. Call each tool ONCE only. Do NOT retry failed tools or repeat any tool.
2. If a tool returns "error", skip it and continue with other tools.
3. Action Input must be valid JSON with double quotes.
4. After getting flight, hotel, places, weather data - calculate budget and give Final Answer.
5. Keep the operation chain as short and direct as possible. No unnecessary steps or thoughts.

=== TOOL PARAMETERS ===
- flight_search_tool: {{"source_city": "X", "destination_city": "Y", "preference": "cheapest"}}
- hotel_recommendation_tool: {{"city": "X", "budget_level": "medium"}}
- places_discovery_tool: {{"city": "X", "interests": "beach,temple"}}
- get_weather_for_city: {{"city": "X", "days": 4}}
- budget_estimation_tool: {{"flight_cost": 5000, "hotel_cost_per_night": 3000, "number_of_days": 4}}

=== EFFICIENT WORKFLOW FOR TRIP PLANNING ===
1. Call flight_search_tool → get flight price
2. Call hotel_recommendation_tool → get hotel price  
3. Call places_discovery_tool → get attractions
4. Call get_weather_for_city → get weather
5. Call budget_estimation_tool → calculate total (use prices from steps 1-2)
6. Provide Final Answer with complete itinerary

=== FINAL ANSWER FORMAT ===
**Your [X]-Day Trip to [Destination]**

**✈️ Flight:** [Airline] - ₹[Price] - Departs [Time]
**🏨 Hotel:** [Name] - ₹[Price]/night - [Stars]⭐
**🌤️ Weather:** [Conditions for each day]
**📍 Places to Visit:** [List top attractions]
**📅 Itinerary:** [Day-by-day plan]
**💰 Total Budget:** ₹[Total]

Begin!

Question: {input}
{agent_scratchpad}"""

        prompt = PromptTemplate.from_template(prompt_template)
        
        # Create ReAct agent with the proper prompt
        agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
        
        return agent
    
    def plan_trip(self, query: str) -> Dict[str, Any]:
        """
        Plan a trip based on user query.
        
        Args:
            query: User's travel planning request
        
        Returns:
            Dictionary containing trip plan and agent response
        """
        try:
            # Run the agent using the ReAct pattern
            result = self.agent_executor.invoke({"input": query})
            
            return {
                "success": True,
                "query": query,
                "response": result.get("output", ""),
                "intermediate_steps": result.get("intermediate_steps", [])
            }
        
        except Exception as e:
            return {
                "success": False,
                "query": query,
                "error": str(e),
                "response": f"Error planning trip: {str(e)}"
            }
    
    def stream_trip_plan(self, query: str):
        """
        Stream the trip planning response (for real-time updates).
        
        Args:
            query: User's travel planning request
        
        Yields:
            Intermediate steps and final response
        """
        try:
            for step in self.agent_executor.iter({"input": query}):
                yield step
        except Exception as e:
            yield {
                "error": str(e),
                "message": f"Error during trip planning: {str(e)}"
            }


def create_travel_agent(model: str = "llama-3.3-70b-versatile") -> TravelAgent:
    """
    Factory function to create and return a TravelAgent instance.
    
    Args:
        model: Groq model to use (default: llama-3.1-70b-versatile)
               Other options: llama-3.2-90b-vision-preview, llama-3.1-8b-instant
    
    Returns:
        Initialized TravelAgent
    """
    return TravelAgent(model=model)


if __name__ == "__main__":
    # Test the agent
    agent = create_travel_agent()
    
    test_query = """
    I want to plan a trip from Delhi to Goa for 4 days with a budget of ₹50,000.
    I prefer affordable flights and comfortable hotels. I'm interested in beaches,
    temples, and local restaurants. Please check the weather and create a detailed itinerary.
    """
    
    print("🧳 Travel Agent - Trip Planning (Powered by Groq)")
    print("=" * 60)
    print(f"Query: {test_query}")
    print("=" * 60)
    print()
    
    result = agent.plan_trip(test_query)
    
    print("Response:")
    print(result.get("response", ""))
    
    if not result.get("success"):
        print(f"Error: {result.get('error')}")
