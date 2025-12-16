# 🌍 Travel Planner AI Agent

An intelligent, end-to-end travel planning system that autonomously creates personalized trip itineraries using LangChain, **Groq LLM**, and real-time data.

**🎉 Now powered by Groq (Free & Fast LLM)** - No OpenAI costs needed!

## 🎯 Features

✨ **AI-Powered Trip Planning** (Powered by Groq LLM)
- Intelligent flight recommendations (cheapest or fastest)
- Smart hotel selection based on budget and ratings
- Personalized attraction discovery matching your interests
- Live weather forecasts for your destination
- Detailed day-wise itineraries with activities
- Accurate budget estimation and breakdown

🛠️ **LangChain Agent Architecture**
- Tool-calling agent for autonomous planning
- 5 specialized tools for different planning aspects
- Streaming support for real-time responses
- Error handling and fallback strategies

🚀 **Groq LLM Integration**
- **Free tier** available (no credit card required initially)
- **Fast inference** (40+ tokens per second)
- **Reliable API** with good uptime
- **Perfect for demos** and prototyping
- Uses Llama 3 8B model for fast reasoning

🎨 **User Interfaces**
- Beautiful Streamlit web UI for easy interaction
- Command-line testing interface
- JSON export for integration with other systems

📊 **Real Data Sources**
- Local JSON datasets for flights, hotels, and attractions
- Open-Meteo API for free weather forecasts
- Realistic data covering Indian cities

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Groq API Key (**free tier available** - [get one here](https://console.groq.com))

### Why Groq?
✅ **Free** - No credit card required initially  
✅ **Fast** - 40+ tokens/second inference speed  
✅ **Reliable** - Cloud-based with good uptime  
✅ **Easy Setup** - Single API key in .env  
✅ **Perfect for Demos** - Great for prototyping and evaluation

### Installation

1. **Clone/Download the project**
```bash
cd Travel\ Planner\ AI\ Agent
```

2. **Create a virtual environment** (recommended)
```bash
# Using conda
conda create -n travel-planner python=3.10
conda activate travel-planner

# Or using venv
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
# Copy the example .env file
cp .env.example .env

# Edit .env and add your Groq API key
# Windows: notepad .env
# macOS/Linux: nano .env
```

Your `.env` file should look like:
```
GROQ_API_KEY=gsk_your-actual-groq-key-here
```

**Get your free Groq API key:**
1. Visit [Groq Console](https://console.groq.com)
2. Sign up (free, no credit card needed)
3. Create an API key
4. Copy it to your .env file

### Usage

#### Option 1: Launch the Streamlit Web UI (Recommended)
```bash
# Start the web application
python main.py streamlit

# Or directly
streamlit run app.py
```
Then open http://localhost:8501 in your browser.

#### Option 2: Test Individual Tools
```bash
python main.py test-tools
```
This tests all 5 tools independently to verify they're working correctly.

#### Option 3: Test the Agent
```bash
python main.py test-agent
```
This runs the full agent with a sample travel planning query.

## 📁 Project Structure

```
Travel Planner AI Agent/
├── data/
│   ├── flights.json          # Flight data
│   ├── hotels.json           # Hotel data
│   └── places.json           # Attractions data
│
├── tools/                    # LangChain Tools
│   ├── __init__.py
│   ├── flight_tool.py        # ✈️ Flight search
│   ├── hotel_tool.py         # 🏨 Hotel recommendations
│   ├── places_tool.py        # 📍 Attraction discovery
│   ├── weather_tool.py       # 🌤️ Weather forecasts
│   └── budget_tool.py        # 💰 Budget calculations
│
├── agent/                    # Travel Agent
│   ├── __init__.py
│   ├── travel_agent.py       # Main agent logic
│   └── prompts.py            # System prompts
│
├── utils/                    # Utilities
│   ├── __init__.py
│   ├── data_loader.py        # Data loading functions
│   └── formatter.py          # Output formatting
│
├── app.py                    # 🎨 Streamlit UI
├── main.py                   # 🚀 Main entry point
├── requirements.txt          # Dependencies
├── .env.example              # Environment template
└── README.md                 # This file
```

## 🔧 How It Works

### The Agent Flow

1. **User Input** → Provide trip details (cities, dates, budget, interests)
2. **Query Building** → Convert inputs to an agent query
3. **Agent Processing** → LLM reads the query and decides which tools to use
4. **Tool Execution**:
   - 🛫 Flight Tool: Searches and selects best flights
   - 🏨 Hotel Tool: Recommends hotels based on budget
   - 📍 Places Tool: Discovers attractions matching interests
   - 🌤️ Weather Tool: Fetches weather forecasts
   - 💰 Budget Tool: Calculates total costs
5. **Itinerary Generation** → LLM creates day-wise plan using tool results
6. **Output** → Display structured trip plan

### Tools Overview

#### 1. Flight Search Tool (`flight_tool.py`)
```python
flight_search_tool(
    source_city: str,           # e.g., "Delhi"
    destination_city: str,      # e.g., "Goa"
    preference: str = "cheapest" # or "fastest"
)
```
Returns the best flight with reasoning and alternatives.

#### 2. Hotel Recommendation Tool (`hotel_tool.py`)
```python
hotel_recommendation_tool(
    city: str,                  # Destination city
    budget_level: str = "medium" # "low", "medium", or "flexible"
)
```
Returns best-value hotel matching budget criteria.

#### 3. Places Discovery Tool (`places_tool.py`)
```python
places_discovery_tool(
    city: str,                  # Destination city
    interests: List[str] = None # e.g., ["temple", "beach"]
)
```
Returns top-rated attractions matching interests.

#### 4. Weather Tool (`weather_tool.py`)
```python
get_weather_for_city(
    city: str,                  # Destination city
    days: int = 7              # Number of days
)
```
Returns daily weather forecast using Open-Meteo API.

#### 5. Budget Tool (`budget_tool.py`)
```python
budget_estimation_tool(
    flight_cost: int,           # Flight price
    hotel_cost_per_night: int,  # Daily hotel rate
    number_of_days: int,        # Trip duration
    daily_expenses: int = 1000  # Food, activities, transport
)
```
Returns detailed cost breakdown and per-day averages.

## 🎨 Streamlit UI Guide

### Input Panel (Left Sidebar)
- **Trip Type**: Domestic or International
- **Cities**: Source and destination
- **Travel Dates**: Start date and duration
- **Budget**: Total budget and level (low/medium/flexible)
- **Flight Preference**: Cheapest or fastest
- **Interests**: Multi-select attractions

### Main Panel
- **Trip Summary**: Overview of the planned trip
- **Flight Details**: Recommended flight with timing and cost
- **Hotel Recommendation**: Suggested accommodation
- **Day-wise Itinerary**: Activities for each day
- **Weather Forecast**: Expected conditions
- **Budget Breakdown**: Cost analysis and recommendations

### Export Options
- Download trip plan as **JSON** (for integration)
- Download trip plan as **Text** (for sharing)

## 📊 Sample Output

The agent generates comprehensive trip plans like:

```
✈️ Flight Recommendation:
   Airline: IndiGo
   Route: Delhi → Goa
   Departure: 2025-01-04 11:32
   Arrival: 2025-01-04 15:32
   Price: ₹2,907
   Reason: Cheapest option at ₹2,907

🏨 Hotel Recommendation:
   Name: Grand Palace Hotel
   City: Goa
   Rating: ⭐⭐⭐⭐
   Price: ₹3,897/night
   Amenities: WiFi, Pool, Gym

📍 Top Attractions:
   - Beautiful Temple (Rating: 4.2/5)
   - Famous Fort (Rating: 4.6/5)
   - Historic Lake (Rating: 4.5/5)

💰 Budget Breakdown:
   Flight: ₹2,907
   Hotel (4 nights): ₹15,588
   Daily Expenses: ₹6,000
   Total: ₹24,495
   Per Day: ₹6,124
```

## 🔑 API Key Setup

### Getting Your OpenAI API Key

1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key (you won't see it again!)
5. Paste it in your `.env` file:
   ```
   OPENAI_API_KEY=sk-your-key-here
   ```

## 📦 Dependencies

- **langchain** (0.1.11): AI agent framework
- **langchain-groq** (0.0.1): Groq LLM integration
- **streamlit** (1.28.1): Web UI framework
- **requests**: HTTP library for API calls
- **pandas** (2.3.3): Data processing
- **python-dotenv**: Environment variable management

See `requirements.txt` for exact versions.

## 🧪 Testing

### Test Individual Tools
```bash
python main.py test-tools
```
Output shows successful tool execution with sample data.

### Test the Full Agent
```bash
python main.py test-agent
```
Runs a complete trip planning flow with detailed output.

### Test Specific Tool from Python
```python
from tools.flight_tool import flight_search_tool

result = flight_search_tool("Delhi", "Goa", "cheapest")
print(result)
```

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'tools'"
**Solution**: Make sure you're running from the project root directory:
```bash
# ❌ Wrong
cd test
python test_file_tool.py

# ✅ Correct
python test/test_file_tool.py
```

### "Error: 'GROQ_API_KEY' not found"
**Solution**: Ensure `.env` file exists with your Groq API key:
```bash
cp .env.example .env
# Edit .env and add your Groq API key from https://console.groq.com
```

Alternatively, set the environment variable directly:
```bash
# Windows PowerShell
$env:GROQ_API_KEY = "your_groq_key_here"

# Windows CMD
set GROQ_API_KEY=your_groq_key_here

# macOS/Linux
export GROQ_API_KEY=your_groq_key_here
```

### "Connection error to Open-Meteo"
**Solution**: Check your internet connection. Weather data requires external API access.

### "No flights found from X to Y"
**Solution**: Check the data files. Not all city pairs may have flight data. Sample data includes:
- Delhi ↔ Goa
- Delhi ↔ Kolkata
- Chennai ↔ Hyderabad
- And many more...

## 🚀 Advanced Usage

### Customize Prompts
Edit `agent/prompts.py` to change agent behavior and output format.

### Add Custom Tools
Create a new file in `tools/` with a `@tool` decorated function and add it to the agent.

### Modify Data
Edit JSON files in `data/` folder to add or update flights, hotels, and attractions.

### Change Model
In `agent/travel_agent.py`, you can use different Groq models:
```python
# Use the fast 8B model (default, recommended)
agent = create_travel_agent(model="llama3-8b-8192")

# Or use the more capable 70B model
agent = create_travel_agent(model="llama3-70b-8192")
```

## 📝 Example Queries

### Budget Trip
"Plan a 3-day trip from Delhi to Jaipur with ₹25,000 budget. I like temples and historic sites."

### Comfort Trip
"I want a 5-day luxury trip from Mumbai to Goa. Budget is flexible. Find expensive, high-rated hotels and high-end attractions."

### Adventure Trip
"Plan a 4-day adventure trip from Bangalore to Goa. I'm interested in beaches, water sports, and restaurants. Budget: ₹40,000."

## 🎓 Learning Resources

- [LangChain Documentation](https://python.langchain.com/)
- [Groq Console & Documentation](https://console.groq.com)
- [Groq API Docs](https://groq.readthedocs.io/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [Open-Meteo Weather API](https://open-meteo.com/)

## 📄 License

This project is open source and available for educational and commercial use.

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Add more cities and data
- Integrate more travel APIs (Skyscanner, TripAdvisor)
- Multi-language support
- Mobile app version
- User accounts and saved itineraries

## 📧 Support

For issues or questions:
1. Check the troubleshooting section
2. Review example queries
3. Check data files for available cities/routes

## 🙏 Acknowledgments

- OpenAI for GPT models
- LangChain for agent framework
- Streamlit for UI framework
- Open-Meteo for weather data
- Community contributors

---

**Happy Traveling! 🌍✈️🧳**

Built with ❤️ using Python, LangChain, and **Groq LLM**

**Key Advantages:**
- ✅ **Zero OpenAI costs** - Use free Groq tier
- ✅ **Fast inference** - 40+ tokens/second
- ✅ **Easy deployment** - Single API key setup
- ✅ **Production ready** - Reliable API with monitoring
- ✅ **Excellent for demos** - Impress clients without big bills
