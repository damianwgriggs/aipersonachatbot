AI Persona Chatbot
This is a fully functional, customizable chatbot application built with Python and Streamlit, powered by the Google Gemini API. The application allows a user to define the personality and behavior of an AI assistant and then engage in a conversation with it.

This project is a definitive portfolio piece from my "AI Execution Sprint," showcasing an advanced, architecturally sound application built using the "Architect & AI Co-Pilot" development framework. The final code is the result of an iterative process of AI-generation and human-led refinement, resulting in a secure, efficient, and well-designed product.

Features
Customizable AI Persona: Users can define the AI's personality, tone, and background knowledge using a simple text input in the sidebar.

Persistent Conversation History: The chatbot remembers the entire conversation for the duration of a user's session, providing context for follow-up questions.

Modern Chat Interface: The application uses Streamlit's native st.chat_message and st.chat_input for a clean and intuitive user experience.

Robust Architecture: The code is structured using a dedicated ChatManager class to encapsulate all AI interaction and state logic, separating it from the UI code.

Efficient State Management: Utilizes Streamlit's official st.session_state to store the chat history and the ChatManager instance, ensuring the application is efficient and stable.

Key Technologies
Python: The core programming language.

Streamlit: For building the interactive web interface.

Google Gemini API: For powering the conversational AI.

Hugging Face Spaces: For hosting the live, deployed application.

Setup and Configuration
To run this project, you will need a secret API key from Google.

1. Clone and Install
First, clone the repository from GitHub and install the necessary libraries.

# Clone the repository
git clone [URL_OF_YOUR_GITHUB_REPO]

# Navigate into the project directory
cd AI-Persona-Chatbot

# Install all required libraries
pip install -r requirements.txt

2. API Key Configuration
This project is configured to use a secure method for handling API keys on the server but requires a manual change for local testing.

For Local Testing:
To run the app on your own computer, you must temporarily add your API key to the code.

Get your free API key from Google AI Studio.

Open the chatbot_app.py file in a code editor.

Find the configuration line (around line 10):

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

Replace that entire line with the following, pasting your key inside the quotation marks:

genai.configure(api_key="YOUR_API_KEY_GOES_HERE")

For Deployment:
IMPORTANT: Before uploading your code to a public repository, you MUST revert the API key line back to the secure version:

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

You will then need to add your key to the Repository secrets in your Hugging Face Space's Settings, using GOOGLE_API_KEY as the name.

How to Run the App
To Run Locally: After adding your API key to the chatbot_app.py file, run this command in your terminal:

streamlit run chatbot_app.py

To Deploy: Upload the secure version of the code and the requirements.txt to a Hugging Face Space. The application will build and run automatically.
