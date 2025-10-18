import streamlit as st
from dotenv import load_dotenv
import os
import sys
from openai import OpenAI


def load_keys():
    load_dotenv(override=True)
    openrouter_key = os.getenv('OPENROUTER_API_KEY')

    if openrouter_key:
        return True, openrouter_key
    else:
        return False


try:
    key_test, api_key = load_keys()
    if key_test:
        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
except:
    st.error("API Key not found. Please set the API_KEY environment variable.")
    st.stop()


MODEL = "openai/gpt-3.5-turbo"
SYSTEM_PROMPT = "You are a helpful and friendly assistant. Keep your responses concise."
# ---

st.title("Streamlit OpenAI Chatbot 🤖💬")

# 2. Initialize Chat History in Streamlit Session State
# The conversation history is stored in this list of dictionaries.
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# 3. Display Chat Messages from History on App Rerun
for message in st.session_state.messages:
    # Skip the 'system' message for display, but keep it for API context
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 4. Accept User Input
if query := st.chat_input("Ask me anything"):
    # Add user message to history and display it
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # 5. Call the OpenAI Chat API with the FULL Conversation History
    with st.chat_message("assistant"):
        # Create a Streamlit element to hold the streaming response
        response_placeholder = st.empty()
        full_response = ""
        
        try:
            # Use the streaming API for better UX
            stream = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            
            # Stream the response chunk by chunk
            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    response_placeholder.markdown(full_response + "▌") # Cursor effect
            
            response_placeholder.markdown(full_response) # Final content

        except Exception as e:
            st.error(f"An error occurred: {e}")
            full_response = f"Sorry, an error occurred while calling the OpenAI API: {e}"
            response_placeholder.markdown(full_response)

        # 6. Add the Assistant's Response to Chat History
        st.session_state.messages.append({"role": "assistant", "content": full_response})