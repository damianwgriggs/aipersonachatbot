import streamlit as st
import google.generativeai as genai
import logging
import os
import time

# --- Configuration ---
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Securely configure the API key for Hugging Face deployment
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY")) 

# --- AI Model Setup ---
model = genai.GenerativeModel('gemini-1.5-flash')

# --- Rate Limiter Functions (ADDED) ---
def check_rate_limit(limit=5, period_seconds=3600):
    """Checks the usage limit based on Streamlit's Session State."""
    if 'usage_log' not in st.session_state:
        st.session_state.usage_log = []
    
    current_time = time.time()
    cutoff_time = current_time - period_seconds
    st.session_state.usage_log = [ts for ts in st.session_state.usage_log if ts > cutoff_time]
    return len(st.session_state.usage_log) < limit

def add_usage_record():
    """Adds a new usage timestamp to the session state."""
    st.session_state.usage_log.append(time.time())

# --- Chat Manager Class ---
class ChatManager:
    def __init__(self, model):
        self.model = model
    
    def get_response(self, persona, history):
        try:
            chat_session = model.start_chat(history=history)
            last_user_prompt = history[-1]['parts'][0]['text']
            full_prompt = f"{persona}\n\nUser: {last_user_prompt}"
            response = chat_session.send_message(full_prompt)
            return response.text
        except Exception as e:
            logging.error(f"Error generating response: {e}")
            return "I'm sorry, I encountered an error. Please try again."

# --- Main App Interface ---
st.set_page_config(page_title="AI Persona Chatbot", page_icon="🤖", layout="wide")
st.title("🤖 AI Persona Chatbot")

# --- Sidebar for persona customization ---
with st.sidebar:
    st.title("AI Persona")
    persona = st.text_area(
        "Describe the AI's personality and behavior:",
        value="You are a sarcastic pirate who is skeptical of modern technology.",
        height=200,
    )

# --- Session State Management ---
if 'model' not in st.session_state:
    st.session_state.model = genai.GenerativeModel('gemini-1.5-flash')
if 'chat_manager' not in st.session_state:
    st.session_state.chat_manager = ChatManager(st.session_state.model)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
# ADDED: Initialize usage_log for rate limiter
if 'usage_log' not in st.session_state:
    st.session_state.usage_log = []

# --- Chat Display ---
if not st.session_state.chat_history:
    st.session_state.chat_history.append({"role": "model", "parts": [{"text": "Ahoy! What be yer question, landlubber?"}]})

for message in st.session_state.chat_history:
    role = "assistant" if message["role"] == "model" else "user"
    with st.chat_message(role):
        st.markdown(message["parts"][0]["text"])

# --- Chat Input and AI Interaction ---
if user_prompt := st.chat_input("Enter your message:"):
    st.session_state.chat_history.append({"role": "user", "parts": [{"text": user_prompt}]})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # UPDATED: Added rate limit check
    if not check_rate_limit():
        error_message = "Rate limit exceeded. Please try again in an hour."
        st.session_state.chat_history.append({"role": "model", "parts": [{"text": error_message}]})
        with st.chat_message("assistant"):
            st.error(error_message)
    else:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                chat_manager = st.session_state.chat_manager
                assistant_reply = chat_manager.get_response(persona, st.session_state.chat_history)
                st.markdown(assistant_reply)
        
        st.session_state.chat_history.append({"role": "model", "parts": [{"text": assistant_reply}]})
        # Log successful use only if it wasn't an error
        if "I'm sorry, I encountered an error" not in assistant_reply:
            add_usage_record()