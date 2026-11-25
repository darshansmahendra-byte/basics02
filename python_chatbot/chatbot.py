
from google import genai
from google.genai import types
from config import GEMINI_API_KEY

# Connect to Gemini
client = genai.Client(api_key=GEMINI_API_KEY)

MODEL = "gemini-3.6-flash"

# Give your chatbot a personality
def create_chat():
    return client.chats.create(
        model=MODEL,
        config=types.GenerateContentConfig(
            system_instruction=(
                "You are Nova AI,created by Darshan, a friendly and intelligent "
                "assistant. Answer clearly in simple English."
            )
        )
    )


chat = create_chat()


def get_reply(message):
    global chat

    try:
        response = chat.send_message(message)
        return response.text or "I couldn't generate a text response."

    except Exception as error:
        return f"Gemini error: {error}"


def reset_chat():
    global chat
    chat = create_chat()
