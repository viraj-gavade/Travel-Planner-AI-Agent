import sys
import os

# Add parent directory to path so we can import tools
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.flight_tool import FlightSearchTool

tool = FlightSearchTool()

result = tool.search_flight(
    source_city="Delhi",
    destination_city="Goa",
    preference="cheapest"
)

print(result)
