# 🚀 Groq Setup Guide

This guide walks you through setting up your Travel Planner AI Agent with Groq LLM (free tier).

## Why Groq?

| Feature | Groq | OpenAI |
|---------|------|--------|
| **Cost** | Free tier available | Paid subscription |
| **Speed** | 40+ tokens/sec | 10-20 tokens/sec |
| **Setup** | 2 minutes | 5 minutes + billing |
| **API Key** | Instant | Requires payment method |
| **Models** | Llama 3 8B/70B | GPT-3.5, GPT-4 |
| **Perfect for** | Demos & Prototyping | Production apps |

## Step 1: Get Your Groq API Key

### Option A: Web Browser (Easiest)

1. **Visit Groq Console**
   - Open: https://console.groq.com

2. **Sign Up (Free)**
   - Click "Sign Up"
   - Email or Google/GitHub login
   - **No credit card required** for free tier
   - Verify email

3. **Create API Key**
   - Go to "API Keys" section
   - Click "Create New Key"
   - Name it: `travel-planner`
   - Copy the key (starts with `gsk_`)
   - **Keep it safe** - don't share it!

4. **Save in .env**
   ```bash
   GROQ_API_KEY=gsk_your_key_here
   ```

### Option B: Command Line

```bash
# Set API key in current terminal (Windows)
set GROQ_API_KEY=gsk_your_key_here

# Set API key in current terminal (macOS/Linux)
export GROQ_API_KEY=gsk_your_key_here
```

## Step 2: Configure Your Project

### 1. Create .env File
```bash
cd "w:\Travel Planner AI Agent"
cp .env.example .env
```

### 2. Add Your API Key
Edit `.env`:
```
GROQ_API_KEY=gsk_your_actual_key_from_console
```

### 3. Verify Setup
```bash
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('✅ API Key loaded' if os.getenv('GROQ_API_KEY') else '❌ API Key not found')"
```

## Step 3: Install Dependencies

```bash
# Activate virtual environment (if using one)
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Install requirements with Groq support
pip install -r requirements.txt
```

### Required Packages
```
langchain==0.1.11
langchain-groq==0.0.1      # Groq integration
streamlit==1.28.1
python-dotenv==1.0.0
requests==2.31.0
pandas==2.3.3
pyarrow==19.0.0
```

## Step 4: Test Your Setup

### Test 1: Verify API Key
```bash
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
key = os.getenv('GROQ_API_KEY')
if key and key.startswith('gsk_'):
    print('✅ API Key is valid')
else:
    print('❌ API Key not found or invalid')
    print('Please check your .env file')
"
```

### Test 2: Test Individual Tools
```bash
python main.py test-tools
```

Expected output:
```
🧪 TESTING INDIVIDUAL TOOLS
✅ Flight Search Result: { "success": true, ... }
✅ Hotel Recommendation Result: { "success": true, ... }
... etc
```

### Test 3: Test Travel Agent
```bash
python main.py test-agent
```

Expected output:
```
🤖 TESTING TRAVEL AGENT (Powered by Groq)
Creating travel agent with Groq LLM...
✅ Agent created successfully!

[Agent will process your test query and generate trip plan]
```

### Test 4: Launch UI
```bash
python main.py streamlit
# or directly:
streamlit run app.py
```

Open browser: http://localhost:8501

## Troubleshooting

### Issue: "GROQ_API_KEY not found"

**Solution 1: Check .env file**
```bash
# Windows
type .env

# macOS/Linux
cat .env
```

Make sure the file contains:
```
GROQ_API_KEY=gsk_...
```

**Solution 2: Restart terminal**
After editing .env, close and reopen your terminal.

**Solution 3: Set environment variable directly**
```bash
# Windows PowerShell
$env:GROQ_API_KEY = "gsk_..."

# Windows CMD
set GROQ_API_KEY=gsk_...

# macOS/Linux
export GROQ_API_KEY=gsk_...
```

### Issue: "Error 401: Invalid API Key"

**Solutions:**
1. Copy the key directly from console (no extra spaces)
2. Make sure key starts with `gsk_`
3. Generate a new key in console if needed
4. Verify .env file is in project root directory

### Issue: "Connection timeout"

**Solutions:**
1. Check internet connection
2. Groq might be down - check [status page](https://status.groq.com)
3. Try again in a minute
4. Use a different API key

### Issue: "Rate limit exceeded"

**Groq Free Tier Limits:**
- Requests/minute: 30
- Tokens/minute: 6,000
- Requests/day: 14,400

**Solution:** Wait a few minutes before retrying, or upgrade to paid tier.

## Groq Models Available

### Llama 3 8B (Default - Recommended)
```python
create_travel_agent(model="llama3-8b-8192")
```
- ✅ Fast (40+ tokens/sec)
- ✅ Perfect for demos
- ✅ Good reasoning
- ✅ Lower latency

### Llama 3 70B (More Capable)
```python
create_travel_agent(model="llama3-70b-8192")
```
- ✅ Better understanding
- ✅ Longer context (8192 tokens)
- ❌ Slower
- ❌ Higher latency
- ⚠️ May hit rate limits faster

## Performance Tips

### 1. Use 8B Model for Quick Demos
```python
# Fast and responsive
agent = create_travel_agent(model="llama3-8b-8192")
```

### 2. Cache API Responses
Tools already return cached JSON to avoid repeated API calls.

### 3. Batch Requests
The agent batches tool calls automatically.

### 4. Monitor Token Usage
Check [Groq Console](https://console.groq.com) for usage stats.

## Free Tier Benefits

✅ **Always Free:**
- 30 requests/minute
- 6,000 tokens/minute
- Excellent for development
- Excellent for demos
- Excellent for small projects

✅ **When to Upgrade:**
- High-traffic production apps
- Need guaranteed uptime SLA
- Need more tokens/minute

## Advanced: Run Locally with Ollama

If you prefer fully local, free LLM (offline), use Ollama instead:

### Install Ollama
```bash
# Download from https://ollama.ai
# Follow installation instructions
```

### Configure for Ollama
```python
# In agent/travel_agent.py
from langchain_community.chat_models import ChatOllama

llm = ChatOllama(
    model="llama2",
    temperature=0.7
)
```

## Next Steps

1. ✅ Get Groq API key
2. ✅ Add to .env file
3. ✅ Install requirements
4. ✅ Run tests
5. ✅ Launch Streamlit UI
6. 🎉 Start planning trips!

## Support & Resources

- **Groq Docs**: https://groq.readthedocs.io/
- **Groq Console**: https://console.groq.com
- **Status Page**: https://status.groq.com
- **LangChain Groq**: https://github.com/langchain-ai/langchain
- **Community**: Groq Discord community

## FAQ

**Q: Is Groq really free?**
A: Yes! Free tier includes 30 requests/minute. Perfect for demos and personal use.

**Q: How long is the free tier available?**
A: Groq hasn't announced an end date. Free tier is designed for developers.

**Q: Can I use this in production?**
A: Yes, with a paid Groq subscription for higher limits.

**Q: Why switch from OpenAI to Groq?**
A: Cost savings, speed, and ease of setup. Perfect for prototyping!

**Q: What if I still want to use OpenAI?**
A: You can! Just use `langchain-openai` instead of `langchain-groq`.

---

**Happy Planning with Groq! 🚀🌍✈️**
