import signal
import sys
import os
from llama_cpp import Llama
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

MODEL_PATH = "Qwen2.5-Coder-32B-Instruct-Q4_K_M.gguf"

class SummaryBot:
    def __init__(self, model_path: str, n_ctx: int = 16384):
        # 1. Path Verification
        if not os.path.exists(model_path):
            st.error(f"[-] ERROR: File not found at {os.path.abspath(model_path)}")
            st.stop()
        st.info(f"[+] Loading Model: {model_path}")
      
        # 2. Conversation History (Context Awareness)
        self.history = [
            {"role": "system", "content": "You are a precise assistant specializing in summarizing email lead status and reasons for no response."}
        ]
        # 3. Model Initialization
        self.llm = Llama(
            model_path=model_path,
            n_gpu_layers=-1, # Offload to RTX 5070
            n_ctx=n_ctx, # Expanded Context Window
            n_threads=12, # Ryzen 7 9800X3D optimization
            flash_attn=True, # Blackwell architecture support
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
                yield content # Yield for streaming in Streamlit
      
        # Add assistant response to history
        self.history.append({"role": "assistant", "content": full_response})

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
            n_gpu_layers=-1, # Offload to RTX 5070
            n_ctx=n_ctx, # Expanded Context Window
            n_threads=12, # Ryzen 7 9800X3D optimization
            flash_attn=True, # Blackwell architecture support
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
                yield content # Yield for streaming in Streamlit
      
        # Add assistant response to history
        self.history.append({"role": "assistant", "content": full_response})

class ReportGenerator:
    def __init__(self, model_path: str):
        self.model_path = model_path
    
    def format_text_with_line_breaks(self, text: str, words_per_line: int = 15) -> str:
        """Insert newlines after every N words in text"""
        words = text.split()
        lines = []
        for i in range(0, len(words), words_per_line):
            lines.append(' '.join(words[i:i + words_per_line]))
        return '\n'.join(lines)
    
    def generate_report(self, excel_id: str):
        # Assuming the Excel file is named based on the ID, e.g., "leads_{excel_id}.xlsx"
        # Adjust this logic if the file pulling mechanism is different (e.g., from a database or API)
        file_path = f"leads_{excel_id}.xlsx"
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Excel file not found: {file_path}")
        
        df = pd.read_excel(file_path)
        
        ist = pytz.timezone('Asia/Kolkata')
        current_time = datetime.now(ist)
        last_24hrs = current_time - timedelta(hours=24)
        
        # Parse sent_at with timezone awareness
        df['sent_at'] = pd.to_datetime(df['sent_at'])
        
        # Filter rows sent in last 24 hours and verified
        filtered = df[df['sent_at'] > last_24hrs]
        filtered = filtered[filtered['verified_at'].notnull()]
        
        report_content = "=====================================================================================================================\n"
        report_content += "OFFICIAL EMAIL LEADS STATUS REPORT\n"
        report_content += "=====================================================================================================================\n"
        report_content += f"REPORT ID: {excel_id}\n"
        report_content += f"GENERATED ON: {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}\n"
        report_content += f"PERIOD: Last 24 Hours (From {last_24hrs.strftime('%Y-%m-%d %H:%M:%S %Z')} to {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')})\n"
        report_content += "=====================================================================================================================\n\n"
        
        if filtered.empty:
            report_content += "No leads sent and verified in the last 24 hours.\n"
        else:
            for _, row in filtered.iterrows():
                # New context window for each lead by creating a new bot instance
                bot = SummaryBot(self.model_path)
                
                query = f"""Summarize in a professional manner why this lead did not respond, based on the following data:
Lead ID: {row['lead_id']}
Email: {row['email']}
First Name: {row['first_name']}
Company: {row['company']}
Status: {row['status']}
Sent At: {row['sent_at']}
Gmail Msg ID: {row.get('gmail_msg_id', 'N/A')}
Bounce Code: {row.get('bounce_code', 'N/A')}
Bounce Reason: {row.get('bounce_reason', 'N/A')}
Verified At: {row['verified_at']}
Provide a short summary focused on the reason for no response."""
                
                full_summary = ""
                for chunk in bot.chat(query):
                    full_summary += chunk
                
                # Format summary with line breaks after every 10 words
                formatted_summary = self.format_text_with_line_breaks(full_summary)
                
                report_content += "---------------------------------------------------------------------------------------------------------------------\n"
                report_content += f"LEAD ID: {row['lead_id']}\n"
                report_content += f"NAME: {row['first_name']}\n"
                report_content += f"COMPANY: {row['company']}\n"
                report_content += f"EMAIL: {row['email']}\n"
                report_content += f"STATUS: {row['status']}\n"
                report_content += "BOUNCE_REASON_SUMMARY:\n"
                report_content += formatted_summary + "\n"
                report_content += "---------------------------------------------------------------------------------------------------------------------\n\n"
        
        report_content += "=====================================================================================================================\n"
        report_content += "END OF REPORT\n"
        report_content += "=====================================================================================================================\n"
        
        report_file = f"report_{excel_id}.txt"
        with open(report_file, 'w') as f:
            f.write(report_content)
        
        print(f"Report generated: {report_file}")

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
                color: #ffffff; /* White text */
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
        abs_path = os.path.abspath(str(MODEL_PATH))
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
    # run_app()
    import os

    # Assuming the model and Excel file are in the current directory or provide full paths
    model_path = os.path.abspath("Qwen2.5-Coder-32B-Instruct-Q4_K_M.gguf")

    # Instantiate the class
    generator = ReportGenerator(model_path)

    # Call the method with the Excel ID (adjust file_path in the class if needed to match "test.xlsx" directly)
    generator.generate_report(excel_id="1")
