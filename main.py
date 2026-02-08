import signal
import sys
import os
from llama_cpp import Llama
import streamlit as st

class CodingBot:
    def __init__(self, model_path: str, n_ctx: int = 16384):
        # 1. Path Verification
        if not os.path.exists(model_path):
            st.error(f"[-] ERROR: File not found at {os.path.abspath(model_path)}")
            st.stop()
        st.info(f"[+] Loading Model: {model_path}")
       
        # 2. Conversation History (Context Awareness)
        self.history = [
            {"role": "system", "content": "You are a precise coding assistant specializing in Python and Quantitative Finance."}
        ]
        # 3. Model Initialization
        self.llm = Llama(
            model_path=model_path,
            n_gpu_layers=-1,  # Offload to RTX 5070
            n_ctx=n_ctx,  # Expanded Context Window
            n_threads=12,  # Ryzen 7 9800X3D optimization
            flash_attn=True,  # Blackwell architecture support
            verbose=False
        )
        st.success("[+] Bot initialized with memory. Ready to chat!")

    def chat(self, user_query: str):
        # Add user input to history
        self.history.append({"role": "user", "content": user_query})
        # Generate response using FULL context
        response_stream = self.llm.create_chat_completion(
            messages=self.history,
            stream=True,
            temperature=0.2,
            max_tokens=2048
        )
        full_response = ""
        for chunk in response_stream:
            if 'content' in chunk['choices'][0]['delta']:
                content = chunk['choices'][0]['delta']['content']
                full_response += content
                yield content  # Yield for streaming in Streamlit
       
        # Add assistant response to history
        self.history.append({"role": "assistant", "content": full_response})

def run_app():
    # Custom CSS for dark-themed futuristic CLI look with updated background and glowing white outlines
    st.markdown("""
        <style>
            /* Overall dark black-grey theme */
            .stApp {
                background-color: #121212;
                color: #ffffff;
            }
            /* Chat messages styling to mimic CLI */
            .stMarkdown {
                font-family: 'Courier New', monospace;
                color: #ffffff;  /* White text */
                background-color: #000000;
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #ffffff;
                box-shadow: 0 0 10px #ffffff;
            }
            /* User input area */
            .stTextInput > div > div > input {
                background-color: #1c1f26;
                color: #ffffff;
                border: 1px solid #ffffff;
            }
            /* Buttons */
            .stButton > button {
                background-color: #ffffff;
                color: #000000;
                border: none;
            }
            /* Sidebar for controls */
            .css-1lcbmhc {
                background-color: #121212;
            }
        </style>
    """, unsafe_allow_html=True)

    # Initialize session state
    if 'bot' not in st.session_state:
        abs_path = os.path.abspath("Qwen2.5-Coder-32B-Instruct-Q4_K_M.gguf")
        st.session_state.bot = CodingBot(model_path=abs_path)
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Sidebar for controls
    with st.sidebar:
        st.title("CodingBot Controls")
        if st.button("Clear Memory"):
            st.session_state.bot.history = [st.session_state.bot.history[0]]
            st.session_state.messages = []
            st.success("Memory cleared!")

    # Display chat history with Markdown support
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    if prompt := st.chat_input("Type your query here (or 'q' to quit)..."):
        if prompt.lower() in ["exit", "quit", "q"]:
            st.info("Shutting down...")
            st.stop()

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Generate and stream assistant response
        with st.chat_message("assistant"):
            response_container = st.empty()
            streamed_response = ""
            for chunk in st.session_state.bot.chat(prompt):
                streamed_response += chunk
                response_container.markdown(streamed_response)
            st.session_state.messages.append({"role": "assistant", "content": streamed_response})

if __name__ == "__main__":
    run_app()