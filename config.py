import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# YouTube API Configuration
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "YOUR_YOUTUBE_API_KEY_HERE")

# Ollama Configuration (for CrewAI)
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:1b")

# Analysis Configuration
SEARCH_QUERY = os.getenv("SEARCH_QUERY", "smart fan")
TOP_N_RESULTS = int(os.getenv("TOP_N_RESULTS", "50"))
TARGET_BRAND = os.getenv("TARGET_BRAND", "atomberg")
COMPETITOR_BRANDS = os.getenv("COMPETITOR_BRANDS", "crompton,havells,orient,usha,bajaj").split(",")
