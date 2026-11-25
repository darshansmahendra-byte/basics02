import os
from dotenv import load_dotenv

# Load settings from the .env file
load_dotenv()

# Read the API key securely
API_KEY = os.getenv("OPENAI_API_KEY")

if API_KEY:
    print("AI API key found!")
else:
    print("No API key found. Running in local mode.")