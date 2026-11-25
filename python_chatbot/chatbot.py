
previous_messages = []


def get_reply(message):
    message = message.lower().strip()

    if "hello" in message or "hi" in message:
        return "Hello! Welcome to Darshan AI. How can I help you?"

    elif "your name" in message:
        return "My name is Darshan AI, your Python chatbot!"

    elif "python" in message:
        return "Python is a popular programming language used in AI, automation and web development."

    elif "how are you" in message:
        return "I am doing great! Thanks for asking."

    elif "help" in message:
        return "I can answer simple questions about Python and chat with you."

    elif "time" in message:
        return "I am running locally on your computer."
    elif "jena milk price" in message:
        return "20rs per liter."

    elif "bye" in message:
        return "Goodbye! Have a wonderful day."

    else:
        return "Interesting question! I am still learning. Try asking me about Python."


def reset_chat():
    global previous_messages
    previous_messages = []
