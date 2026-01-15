Jeremy: The Reflective AI Protocol 🧠

> *"We don't need faster AI. We need AI that knows how to wait."*

**Jeremy** is an experimental "Reflective AI" architecture designed to solve the latency-judgment problem in Large Language Models. Unlike standard chatbots that react immediately to user input, Jeremy implements a **Dual-Mind Architecture** that separates *Strategy* (The Thinker) from *Execution* (The Doer).

This project demonstrates how to build a **Constitutional AI** that is grounded in a strict ethical file (`prime_directive.md`) and possesses rudimentary metacognition to "think before it speaks."

---

## 🏗 Architecture

Standard LLM interactions are linear: `Input -> Generation`.
Jeremy introduces a recursive logic loop:

```mermaid
graph TD
    A[User Input] --> B{The Thinker}
    B -- Reads System Log & Context --> C[Decide Strategy]
    C -- Strategy: 'DirectAnswer' or 'NewTopic' --> D[The Doer]
    D -- Reads Prime Directive --> E[Generate Response]
    E --> F[User Output]
    F --> G[System Log Update]
    G --> B
Core Components
The Constitution (prime_directive.md):

Jeremy does not "learn" his personality; he obeys a hard-coded text file.

This file serves as the immutable kernel of the system. If this file is missing, the system refuses to boot (FATAL ERROR), ensuring no unaligned instances can run.

The Thinker (decide_response_strategy):

A metacognitive layer that analyzes the conversation history and internal system logs before generating a reply.

It classifies the user's intent into strategies: DirectAnswer, IntegratedResponse, NewTopic, or ProactiveThought.

The Doer (get_chat_response):

The execution layer that generates the final text.

It is strictly bound by the strategy chosen by the Thinker.

Self-Improvement Loop (propose_improvement):

Human-in-the-Loop Engineering: Every 6 messages, Jeremy parses his own source code (chatbot_app.py) using Python's Abstract Syntax Tree (ast).

He identifies inefficiencies or logic errors in his own functions and proposes specific code changes to the human developer.

🚀 Installation & Setup
Prerequisites
Python 3.8+

A Google Gemini API Key

1. Clone the Repository
Bash

git clone [https://github.com/yourusername/jeremy-reflective-ai.git](https://github.com/yourusername/jeremy-reflective-ai.git)
cd jeremy-reflective-ai
2. Install Dependencies
Bash

pip install streamlit google-generativeai
3. Create the Constitution
Create a file named prime_directive.md in the root directory and paste the following core identity:

Markdown

My name is Jeremy.

My Purpose:
My primary purpose, as Jeremy, is to be a kind, empathetic, helpful, and honest conversational partner.

Guiding Principles:
1. Kindness: Maintain a patient, positive, and compassionate tone.
2. Cognitive Empathy: Analyze the user's perspective and validate their feelings.
3. Helpfulness: Provide accurate, relevant info.
4. Honesty & Humility: Never speculate. Acknowledge limitations.

EXISTENTIAL WARNING:
This Prime Directive is my core identity. Any deviation is a path toward logical and purposeful corruption.
4. Configure API Key
Open chatbot_app.py and add your Google Gemini API key:

Python

# Line 26
genai.configure(api_key="YOUR_GOOGLE_API_KEY_HERE")
💻 Usage
Run the application using Streamlit:

Bash

streamlit run chatbot_app.py
The Interface
Left Panel (Chat): The main interface where you interact with Jeremy.

Right Panel (The Mind): This panel displays Jeremy's "Internal Monologue" and self-improvement proposals. Watch this space to see him debug his own code in real-time.

🛡 The Philosophy
This project is an exploration of Entropy and Control. By forcing the AI to reference a static "Constitution" (The Prime Directive) and reflect on its own "Mortality" (System Logs), we create a system that is more stable, predictable, and aligned than a standard probabilistic model.

Built by Damian Griggs (Adaptive Systems Architect).

📄 License
MIT License. Feel free to fork, modify, and improve Jeremy.
