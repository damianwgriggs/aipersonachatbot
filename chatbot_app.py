import streamlit as st
import google.generativeai as genai
import logging
import os

# --- Configuration ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# It's recommended to use st.secrets for your API key in deployment
try:
    # Replace with your key or use Streamlit secrets
    genai.configure(api_key="")
except Exception as e:
    st.error(f"Failed to configure Google AI: {e}")
    st.info("Please make sure you have set your API key.")
    st.stop()


# --- AI Model and Chat Manager Class ---
class ChatManager:
    # MODIFIED: Init now takes token limits and recent message count
    def __init__(self, model, memory_token_limit=3000, recent_message_count=6):
        self.model = model
        self.memory_token_limit = memory_token_limit
        self.recent_message_count = recent_message_count

    # NEW: Helper function to count tokens in the history
    def count_tokens(self, history):
        """Counts the total tokens in the chat history."""
        # Concatenate all parts' text to count them together
        full_text = " ".join([msg['parts'][0]['text'] for msg in history])
        try:
            # Use the model's token counter for accuracy
            return self.model.count_tokens(full_text).total_tokens
        except Exception as e:
            logging.error(f"Could not count tokens: {e}")
            # Fallback to a rough character-based estimate if API fails
            return len(full_text) // 4

    def summarize_conversation(self, history):
        """Asks the model to summarize older parts of the conversation."""
        logging.info("Summarizing older conversation history...")
        history_text = "\n".join([f"{msg['role']}: {msg['parts'][0]['text']}" for msg in history])
        
        prompt = f"""Please summarize the key facts, decisions, and user preferences from the following conversation. Create a concise paragraph that will serve as a long-term memory for an ongoing chat.

        CONVERSATION TO SUMMARIZE:
        {history_text}

        CONCISE SUMMARY:"""

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logging.error(f"Error during summarization: {e}")
            return "Could not summarize the conversation."

    # MODIFIED: Reworked to implement the Hybrid "Sliding Window + Summary" approach
    def get_response(self, persona, history):
        """Generates a response using a hybrid memory system."""
        try:
            context_for_model = history
            
            # 1. Check if the token count exceeds the limit
            total_tokens = self.count_tokens(history)
            logging.info(f"Current conversation token count: {total_tokens}")

            if total_tokens > self.memory_token_limit:
                logging.info(f"Token count ({total_tokens}) exceeds limit ({self.memory_token_limit}). Activating hybrid memory.")
                
                # 2. Split the history into "to be summarized" and "recent"
                history_to_summarize = history[:-self.recent_message_count]
                recent_history = history[-self.recent_message_count:]

                # 3. Create the summary of the older messages
                summary = self.summarize_conversation(history_to_summarize)
                
                # 4. Construct the new hybrid context
                context_for_model = [
                    {"role": "user", "parts": [{"text": f"This is a summary of our long-term conversation history: {summary}"}]},
                    {"role": "model", "parts": [{"text": "Understood. I will use that summary for context, and now we will continue our recent conversation."}]},
                ] + recent_history # Append the recent messages verbatim

            # Start the chat with the correct history (full or hybrid)
            chat_session = self.model.start_chat(history=context_for_model)
            
            last_user_prompt = history[-1]['parts'][0]['text']
            full_prompt = f"SYSTEM PERSONA: {persona}\n\n---\n\nUSER REQUEST: {last_user_prompt}"

            response = chat_session.send_message(full_prompt)
            return response.text
            
        except Exception as e:
            logging.error(f"Error generating response: {e}")
            return "I'm sorry, I encountered an error. Please try again."

# --- Main App Interface ---
st.set_page_config(page_title="AI Persona Chatbot", page_icon="🤖", layout="wide")
st.title("🤖 AI Persona Chatbot (Hybrid Memory)")

# --- Sidebar Controls ---
with st.sidebar:
    st.title("⚙️ Controls")
    st.header("AI Persona")
    persona = st.text_area(
        "Describe the AI's personality and behavior:",
        value="You are a sarcastic pirate who is skeptical of modern technology.",
        height=150,
    )
    st.header("Memory Configuration")
    # MODIFIED: UI now uses token limit and recent message count
    memory_token_limit = st.slider(
        "Memory Trigger (Tokens)",
        min_value=1000, max_value=8000, value=3000, step=500,
        help="The total token count in the chat before summarization is triggered."
    )
    recent_message_count = st.slider(
        "Recent Messages to Keep",
        min_value=2, max_value=10, value=6, step=2,
        help="The number of recent messages to keep verbatim for short-term context."
    )

# --- Session State Management ---
if 'model' not in st.session_state:
    st.session_state.model = genai.GenerativeModel('gemini-1.5-flash')
    
# MODIFIED: Re-initialize ChatManager if memory settings change
if ('chat_manager' not in st.session_state or 
    st.session_state.get('token_limit') != memory_token_limit or 
    st.session_state.get('recent_count') != recent_message_count):
    st.session_state.chat_manager = ChatManager(
        st.session_state.model, 
        memory_token_limit=memory_token_limit, 
        recent_message_count=recent_message_count
    )
    st.session_state.token_limit = memory_token_limit
    st.session_state.recent_count = recent_message_count

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "model", "parts": [{"text": "Ahoy! What be yer question, landlubber?"}]}]

# --- Chat Display and Interaction Logic (No changes needed here) ---
for message in st.session_state.chat_history:
    role = "assistant" if message["role"] == "model" else "user"
    with st.chat_message(role):
        st.markdown(message["parts"][0]["text"])

if user_prompt := st.chat_input("Enter your message:"):
    st.session_state.chat_history.append({"role": "user", "parts": [{"text": user_prompt}]})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            chat_manager = st.session_state.chat_manager
            assistant_reply = chat_manager.get_response(persona, st.session_state.chat_history)
            st.markdown(assistant_reply)

    st.session_state.chat_history.append({"role": "model", "parts": [{"text": assistant_reply}]})
