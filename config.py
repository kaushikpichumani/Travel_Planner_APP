import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
AMADEUS_API_KEY = os.getenv('AMADEUS_CLIENT_ID')
AMADEUS_API_SECRET = os.getenv('AMADEUS_CLIENT_SECRET')
OPENAI_API_KEY = os.getenv('OPENAI_API')
TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')