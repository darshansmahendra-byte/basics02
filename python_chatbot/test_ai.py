from dotenv import load_dotenv
from openai import OpenAI

# Load API key from .env
load_dotenv()

# Connect to OpenAI
client = OpenAI()

# Send a test message
response = client.responses.create(
    model="gpt-5.5",
    input="Introduce yourself in two sentences."
)

print(response.output_text)