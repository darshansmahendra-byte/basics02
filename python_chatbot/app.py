
import streamlit as st
from chatbot import get_reply, reset_chat

st.set_page_config(
    page_title="Darshan AI",
    page_icon="🤖"
)

st.title("🤖 Darshan AI Chatbot")
st.caption("Your personal Python chatbot")

# Initialize conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Clear chat button
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    reset_chat()
    st.rerun()

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Accept a new message
prompt = st.chat_input("Type your message...")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.write(prompt)

    reply = get_reply(prompt)

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })

    with st.chat_message("assistant"):
        st.write(reply)
