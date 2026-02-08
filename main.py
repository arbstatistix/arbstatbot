import signal
import sys
import os
from llama_cpp import Llama

class CodingBot:
    def __init__(self, model_path: str, n_ctx: int = 16384):
        # 1. Path Verification
        if not os.path.exists(model_path):
            print(f"[-] ERROR: File not found at {os.path.abspath(model_path)}")
            sys.exit(1)

        print(f"[+] Loading Model: {model_path}")
        self._setup_signal_handlers()
        
        # 2. Conversation History (Context Awareness)
        self.history = [
            {"role": "system", "content": "You are a precise coding assistant specializing in Python and Quantitative Finance."}
        ]

        # 3. Model Initialization
        self.llm = Llama(
            model_path=model_path,
            n_gpu_layers=-1,      # Offload to RTX 5070
            n_ctx=n_ctx,          # Expanded Context Window
            n_threads=12,         # Ryzen 7 9800X3D optimization
            flash_attn=True,      # Blackwell architecture support
            verbose=False
        )
        print("[+] Bot initialized with memory. Ready to chat!")

    def _setup_signal_handlers(self):
        def signal_handler(sig, frame):
            print("\nShutting down...")
            sys.exit(0)
        signal.signal(signal.SIGINT, signal_handler)

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
        print("Assistant: ", end="", flush=True)
        for chunk in response_stream:
            if 'content' in chunk['choices'][0]['delta']:
                content = chunk['choices'][0]['delta']['content']
                print(content, end="", flush=True)
                full_response += content
        
        # Add assistant response to history
        self.history.append({"role": "assistant", "content": full_response})
        print("\n" + "-" * 60)

    def run(self):
        print("CodingBot active. (Type 'q' to quit, 'clear' to reset memory)\n")
        while True:
            try:
                user_query = input("You: ").strip()
                if user_query.lower() in ["exit", "quit", "q"]: break
                if user_query.lower() == "clear":
                    self.history = [self.history[0]]
                    print("Memory cleared!")
                    continue
                if not user_query: continue
                
                self.chat(user_query)
            except Exception as e:
                print(f"\nError: {e}")

if __name__ == "__main__":
    # Use the full absolute path to be safe
    import os
    abs_path = os.path.abspath("Qwen2.5-Coder-32B-Instruct-Q4_K_M.gguf")
    bot = CodingBot(model_path=abs_path)
    bot.run()