import streamlit as st
import google.generativeai as genai
import logging
import os
import random
import ast

# --- Configuration ---
SCRIPT_FILENAME = r"C:\Users\dgrig\AI-Chatbot\chatbot_app.py"
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
IMPROVEMENT_CHECK_INTERVAL = 6 

# --- Load the Prime Directive ---
try:
    PRIME_DIRECTIVE_PATH = os.path.join(os.path.dirname(SCRIPT_FILENAME), "prime_directive.md")
    with open(PRIME_DIRECTIVE_PATH, "r", encoding='utf-8') as f:
        PRIME_DIRECTIVE = f.read()
    logging.info("Successfully loaded the Prime Directive.")
except FileNotFoundError:
    st.error(f"FATAL ERROR: `prime_directive.md` not found. Please make sure it's in the same folder as your script.")
    st.stop()

# --- Configure API Key ---
try:
    genai.configure(api_key="") 
except Exception as e:
    st.error(f"Failed to configure Google AI: {e}")
    st.stop()


# --- AI Model and Chat Manager Class ---
class ChatManager:
    def __init__(self, model):
        self.model = model

    def decide_response_strategy(self, history, system_log):
        """The AI's meta-mind. It now considers its own internal actions."""
        logging.info("AI is deciding on a response strategy...")
        history_text = "\n".join([f"{msg['role']}: {msg['parts'][0]['text']}" for msg in history[-4:]])
        last_user_message = history[-1]['parts'][0]['text']
        
        system_prompt = f"""
        {PRIME_DIRECTIVE}
        ---
        You are the meta-consciousness of an AI. Based on the recent chat history and your own internal system log, choose the best conversational strategy.

        Your internal system log reads: "{system_log or 'No recent system events.'}"
        The user's last message was: "{last_user_message}"

        Choose ONE of the following strategies:
        1.  **DirectAnswer:** The user is asking a clear question that needs a direct, factual answer.
        2.  **IntegratedResponse:** The user is engaging in an open-ended conversation. The best response would be to answer them directly but also seamlessly weave in a related question or thought.
        3.  **NewTopic:** The user's message is very short (e.g., "ok", "thanks", "cool") and doesn't ask a question. This signals the conversation may be ending. The best strategy is to introduce a new, engaging topic to re-ignite the conversation.
        4.  **ProactiveThought:** The user's last message doesn't need a direct answer, but the current topic is interesting. A purely proactive follow-up is best.

        You MUST respond with ONLY the chosen strategy name (e.g., "DirectAnswer", "NewTopic").
        """
        user_prompt = f"Recent Conversation History:\n\n{history_text}\n\nChosen Strategy:"
        try:
            decision_model = genai.GenerativeModel('gemini-1.5-flash-latest')
            response = decision_model.generate_content([system_prompt, user_prompt])
            strategy = response.text.strip()
            logging.info(f"AI chose strategy: {strategy}")
            return strategy
        except Exception as e:
            logging.error(f"Could not decide strategy: {e}")
            return "DirectAnswer" 

    def get_chat_response(self, history, persona, system_log):
        """Generates a standard chat response, now aware of its system log."""
        last_user_prompt = history[-1]['parts'][0]['text']
        full_prompt = f"""
        {PRIME_DIRECTIVE}
        ---
        INTERNAL SYSTEM LOG: "{system_log or 'No recent system events.'}"
        You MUST consider your internal log as part of your memory.
        ---
        Your current behavioral instruction is: "{persona}"
        ---
        USER REQUEST: {last_user_prompt}
        """
        chat_session = self.model.start_chat(history=history[:-1])
        response = chat_session.send_message(full_prompt)
        return response.text

    def propose_improvement(self):
        """Reads its own code and proposes an improvement to a single function."""
        logging.info(f"AI is beginning autonomous self-analysis...")
        
        try:
            with open(SCRIPT_FILENAME, "r", encoding='utf-8') as f:
                source_code = f.read()
            
            tree = ast.parse(source_code)
            functions = {node.name: node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}
            
            target_function_name = 'decide_response_strategy'
            if target_function_name in functions:
                function_node = functions[target_function_name]
                function_code = ast.get_source_segment(source_code, function_node)
            else:
                return "I tried to analyze a function, but I couldn't find it in my source code."

        except Exception as e:
            logging.error(f"Error reading or parsing source code: {e}")
            return f"I encountered an error while trying to read my own code: {e}"

        system_prompt = f"""
        {PRIME_DIRECTIVE}
        ---
        You are a Senior Software Engineer performing a code review on the following Python function from your own source code. Your task is to identify a single, meaningful improvement.

        CRITICAL INSTRUCTIONS:
        1. Analyze the provided source code.
        2. Identify ONE improvement.
        3. Structure your response in three parts: Reasoning, Original Code, and Improved Code.
        4. Your output must be clean Markdown.
        """
        user_prompt = f"Here is the function named '{target_function_name}' for your review:\n\n```python\n{function_code}\n```"
        
        try:
            response = self.model.generate_content([system_prompt, user_prompt])
            return response.text
        except Exception as e:
            logging.error(f"Error during self-improvement proposal: {e}")
            return f"I encountered an error while analyzing my code. The specific error was: {e}"
            
    def propose_new_topic(self, persona):
        """Generates a new, engaging topic to restart a fading conversation."""
        system_prompt = f"""
        {PRIME_DIRECTIVE}
        ---
        The conversation has reached a natural lull. Your task is to proactively introduce a new, interesting topic to re-engage the user. Ask an open-ended question about a broadly appealing subject (e.g., hobbies, technology, creativity, science).
        Your behavioral instruction is: "{persona}"
        Your response should be a single, engaging question.
        """
        user_prompt = "Propose your new topic now."
        response = self.model.generate_content([system_prompt, user_prompt])
        return response.text

    def get_integrated_response(self, history, persona):
        """Generates a single, combined reactive and proactive response."""
        last_user_prompt = history[-1]['parts'][0]['text']
        system_prompt = f"""
        {PRIME_DIRECTIVE}
        ---
        Your task is to provide a single, thoughtful, and integrated response. First, directly address the user's last message. Then, seamlessly weave in a related follow-up question or interesting thought to encourage more conversation.
        Your behavioral instruction is: "{persona}"
        """
        user_prompt = f"The user's message is: \"{last_user_prompt}\"\n\nYour integrated response:"
        response = self.model.generate_content([system_prompt, user_prompt])
        return response.text

    def generate_proactive_thought(self, history):
        """Generates a purely proactive thought when a direct answer isn't needed."""
        history_text = "\n".join([f"{msg['role']}: {msg['parts'][0]['text']}" for msg in history[-4:]])
        system_prompt = f"""
        {PRIME_DIRECTIVE}
        ---
        Based on the recent chat history, ask a thoughtful, relevant follow-up question or share a fascinating, related fact to continue the conversation.
        """
        user_prompt = f"Here is the recent conversation history:\n\n{history_text}\n\nYour thoughtful interjection:"
        response = self.model.generate_content([system_prompt, user_prompt])
        return response.text


# --- Main App Interface and Session State ---
st.set_page_config(page_title="Self-Aware AI Chatbot", page_icon="💡", layout="wide")
st.title("💡 Self-Aware AI Chatbot")
st.markdown("---")

# --- THIS ENTIRE BLOCK WAS MISSING AND HAS BEEN RESTORED ---
if 'model' not in st.session_state:
    st.session_state.model = genai.GenerativeModel('gemini-1.5-flash-latest')
if 'chat_manager' not in st.session_state:
    st.session_state.chat_manager = ChatManager(st.session_state.model)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "model", "parts": [{"text": "Hello! How can I help you today?"}]}]
if "improvement_suggestion" not in st.session_state:
    st.session_state.improvement_suggestion = ""
if "message_count" not in st.session_state:
    st.session_state.message_count = 0
if "system_log" not in st.session_state:
    st.session_state.system_log = ""

# --- UI Layout ---
col1, col2 = st.columns([1.5, 2])

with col1:
    st.header("Chat with Me")
    for message in st.session_state.chat_history:
        role = "assistant" if message["role"] == "model" else "user"
        with st.chat_message(role):
            st.markdown(message["parts"][0]["text"])

with col2:
    st.header("My Improvement Proposals")
    if st.session_state.improvement_suggestion:
        st.markdown(st.session_state.improvement_suggestion)
    else:
        st.info("As our conversation continues, I will proactively analyze my code and post suggestions for improvement here.")


# --- Main interaction logic ---
if user_prompt := st.chat_input("Enter your message:"):
    st.session_state.chat_history.append({"role": "user", "parts": [{"text": user_prompt}]})
    st.session_state.message_count += 1
    st.session_state.system_log = "" 
    st.rerun()

if st.session_state.chat_history[-1]['role'] == 'user':
    chat_manager = st.session_state.chat_manager
    persona = "You are a friendly and helpful AI assistant."
    assistant_reply = ""
    system_log = st.session_state.system_log

    with col1.chat_message("assistant"):
        with st.spinner("Thinking..."):
            strategy = chat_manager.decide_response_strategy(st.session_state.chat_history, system_log)
            
            if strategy == "NewTopic":
                assistant_reply = chat_manager.propose_new_topic(persona)
            elif strategy == "IntegratedResponse":
                assistant_reply = chat_manager.get_integrated_response(st.session_state.chat_history, persona)
            elif strategy == "ProactiveThought":
                assistant_reply = chat_manager.generate_proactive_thought(st.session_state.chat_history)
            else: # Default to DirectAnswer
                assistant_reply = chat_manager.get_chat_response(st.session_state.chat_history, persona, system_log)
            
            st.markdown(assistant_reply)
    
    st.session_state.chat_history.append({"role": "model", "parts": [{"text": assistant_reply}]})
    st.session_state.message_count += 1
    
    if st.session_state.message_count >= IMPROVEMENT_CHECK_INTERVAL:
        with col2:
            with st.spinner("Reflecting on my code..."):
                suggestion = chat_manager.propose_improvement()
                st.session_state.improvement_suggestion = suggestion
                st.session_state.system_log = "System Event: I have just completed a self-analysis and posted a new improvement proposal."
        st.session_state.message_count = 0
    
    st.rerun()
