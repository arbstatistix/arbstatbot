# CodingBot - AI Coding Assistant

A Python-based interactive chatbot powered by the Qwen2.5-Coder-32B model, optimized for coding assistance and quantitative finance tasks.

## Features

- **Intelligent Code Assistant**: Specialized in Python and Quantitative Finance
- **Context Awareness**: Maintains conversation history for coherent multi-turn interactions
- **GPU Acceleration**: Optimized for RTX 5070 and Blackwell architecture with Flash Attention support
- **Memory Management**: Reset conversation history on demand with the `clear` command
- **Real-time Streaming**: Responses stream in real-time for immediate feedback

## Requirements

- Python 3.8+
- CUDA-capable GPU (RTX 5070 recommended)
- 32GB+ RAM (for 32B model)

## Installation

1. Clone or download this repository

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure the model file is present in the same directory:
   - `Qwen2.5-Coder-32B-Instruct-Q4_K_M.gguf`

## Usage

Start the bot by running:
```bash
python main.py
```

### Interactive Commands

Once running, interact with the bot using:

| Command | Action |
|---------|--------|
| `q`, `exit`, `quit` | Exit the program |
| `clear` | Reset conversation memory and start fresh |
| Any text | Send a prompt to the AI assistant |

### Example Interaction

```
You: How do I calculate compound interest in Python?
Assistant: To calculate compound interest, you can use the formula...
[Bot streams response]
------------------------------------------------------------
You: What about with monthly compounding?
Assistant: With monthly compounding, you would modify the formula...
```

## Configuration

Edit `main.py` to customize:

- **`n_ctx`**: Context window size (default: 16384 tokens)
- **`n_gpu_layers`**: GPU layer offloading (-1 = full offload)
- **`n_threads`**: CPU threads (optimized for Ryzen 7 9800X3D)
- **`temperature`**: Response randomness (0.2 = deterministic for coding)
- **`max_tokens`**: Maximum response length (2048)

## Model Details

- **Model**: Qwen2.5-Coder-32B-Instruct
- **Quantization**: Q4_K_M (4-bit)
- **Specializations**: Python, Quantitative Finance
- **Optimization**: Flash Attention, GPU acceleration

## File Structure

```
.
├── main.py                                      # Main bot script
├── requirements.txt                             # Python dependencies
├── Qwen2.5-Coder-32B-Instruct-Q4_K_M.gguf     # Model file
├── main.ipynb                                   # Jupyter notebook version
└── README.md                                    # This file
```

## Troubleshooting

### Model file not found
Ensure `Qwen2.5-Coder-32B-Instruct-Q4_K_M.gguf` is in the same directory as `main.py`

### Out of memory errors
- Reduce `n_ctx` value
- Reduce `max_tokens` value
- Ensure no other GPU-intensive applications are running

### Slow responses
- Verify GPU is being used (check `n_gpu_layers=-1`)
- Check CUDA is properly installed
- Monitor GPU memory with `nvidia-smi`

## Dependencies

- `llama-cpp-python`: For running GGUF models
- `torch`: Deep learning framework
- `transformers`: Hugging Face transformers library
- `accelerate`: Multi-GPU support
- `bitsandbytes`: Quantization library

## License

[Specify your license here]

## Author

[Your name]

---

**Note**: This bot is optimized for coding and financial analysis tasks. Keep context window size in mind for very long conversations.
