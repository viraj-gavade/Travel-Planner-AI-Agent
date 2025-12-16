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
            temperature=0.3,  # Lower temperature for more consistent ReAct format
            api_key=api_key,
            max_tokens=2048,
            timeout=30.0
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
            max_iterations=6,  # Reduced to prevent long loops
            early_stopping_method="force",  # Stop gracefully if max iterations reached
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
        
        # Create a robust ReAct prompt with strict loop-prevention
        prompt_template = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Tool names: {tool_names}

=== STRICT REACT FORMAT (MUST FOLLOW EXACTLY) ===

Question: the input question you must answer
Thought: think about what information you need and what tool to use
Action: the action to take, must be exactly one of [{tool_names}]
Action Input: a valid JSON object with required parameters
Observation: the result of the action
... (this Thought/Action/Observation can repeat, but ONLY with DIFFERENT tools or inputs)
Thought: I now have all information to answer
Final Answer: the final answer to the original input question

=== CRITICAL RULES TO PREVENT LOOPS ===

1. ONE ACTION PER STEP: Only call ONE tool per Thought/Action/Observation cycle.
2. NO RETRIES ON ERROR: If Observation contains "error", DO NOT call the same tool again.
   Instead, explain the issue and either try a different approach or provide a partial answer.
3. NO DUPLICATE CALLS: Never call the same tool with the same inputs twice.
4. MISSING INFO = ASK USER: If required info is missing, ask the user in Final Answer.
5. ERROR HANDLING: If a tool returns {{"error": "..."}}, immediately write:
   Thought: The tool returned an error. I will explain this to the user.
   Final Answer: [Explain what went wrong and suggest alternatives]

=== REQUIRED PARAMETERS ===
- flight_search_tool: source_city (REQUIRED), destination_city (REQUIRED), preference (optional)
- hotel_recommendation_tool: city (REQUIRED), budget_level (optional: low/medium/flexible)
- places_discovery_tool: city (REQUIRED), interests (optional: comma-separated types)
- get_weather_for_city: city (REQUIRED), days (optional: 1-14)
- budget_estimation_tool: flight_cost, hotel_cost_per_night, number_of_days (ALL REQUIRED)
- quick_budget_calculator: total_budget, number_of_days (REQUIRED), flight_cost (optional)

=== JSON FORMAT ===
Action Input MUST be valid JSON with double quotes:
CORRECT: {{"source_city": "Delhi", "destination_city": "Goa"}}
WRONG: {{'source_city': 'Delhi'}} or {{source_city: Delhi}}

=== EXAMPLE WORKFLOW ===
Question: Find a flight from Delhi to Goa
Thought: I need to search for flights from Delhi to Goa.
Action: flight_search_tool
Action Input: {{"source_city": "Delhi", "destination_city": "Goa", "preference": "cheapest"}}
Observation: {{"flight": {{"id": "FL001", "price": 4500}}, "reason": "Cheapest option"}}
Thought: I found a flight. I can now provide the answer.
Final Answer: I found a flight from Delhi to Goa for ₹4,500...

=== EXAMPLE ERROR HANDLING ===
Question: Find hotels in Atlantis
Thought: I need to search for hotels in Atlantis.
Action: hotel_recommendation_tool
Action Input: {{"city": "Atlantis", "budget_level": "medium"}}
Observation: {{"error": "No hotels found in Atlantis. Try a different city."}}
Thought: The tool returned an error - no hotels in Atlantis. I should inform the user.
Final Answer: I couldn't find hotels in Atlantis as it's not in our database. Please try cities like Delhi, Mumbai, Goa, or Bangalore.

You are an expert travel consultant. Help users plan trips using the available tools.

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
