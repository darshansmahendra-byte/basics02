import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    print("Gemini API key found!")
else:
    print("Gemini API key missing!")
    [theme]
base = "dark"
primaryColor = "#7c83ff"
backgroundColor = "#0b1020"
secondaryBackgroundColor = "#141b33"
textColor = "#e8ecf8"
font = "sans serif"
