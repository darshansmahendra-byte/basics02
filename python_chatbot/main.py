
from chatbot import get_reply, reset_chat

print("================================")
print("       DARSHAN AI CHATBOT")
print("================================")
print("Type 'exit' to quit.")
print("Type 'clear' to reset conversation.")

while True:

    message = input("\nYou: ").strip()

    if message.lower() == "exit":
        print("Bot: Goodbye!")
        break

    elif message.lower() == "clear":
        reset_chat()
        print("Bot: Conversation cleared!")
        continue

    elif not message:
        print("Bot: Please enter a message.")
        continue

    reply = get_reply(message)

    print("Bot:", reply)
