# CodingBot - AI Coding Assistant

A Python-based interactive chatbot powered by the Qwen2.5-Coder-32B model, optimized for coding assistance and quantitative finance tasks.

---

## 🎯 Email Campaign Manager Users - Start Here!

If you're setting up the **Email Campaign Manager**, read this first:

### Critical Files That Must Be Created/Configured:

1. **`config.json`** - Configuration file
   - **Location:** `/home/mate/Desktop/github/llm/email_agent/config.json`
   - **Format:** JSON
   - **Danger:** Add to `.gitignore` before committing

2. **`credentials.json`** - Google OAuth credentials
   - **Location:** `/home/mate/Desktop/github/llm/email_agent/credentials.json`
   - **Format:** JSON (download from Google Cloud Console)
   - **Danger:** NEVER commit - contains client_secret!

3. **`token.json`** - API access token (AUTO-GENERATED)
   - **Location:** `/home/mate/Desktop/github/llm/email_agent/token.json`
   - **Auto-created:** On first run
   - **Danger:** NEVER commit - contains access tokens!

**📖 For detailed JSON format explanation:** See [email_agent/JSON_CONFIG_FORMAT.md](./email_agent/JSON_CONFIG_FORMAT.md)

**👉 Then follow:** [email_agent/README.md](./email_agent/README.md) for complete Email Campaign Manager setup

---

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

---

# 📧 Email Campaign Manager

A comprehensive email campaign management system with lead tracking, automated sending, status verification, and AI-powered reporting using the Qwen model.

## Features

- **📋 Leads Dashboard** - View all leads in a formatted table with bounce reasons displayed prominently
- **✉️ Email Sending** - Send personalized emails to leads from templates using Gmail API
- **🔍 Status Verification** - Check email delivery status and bounce information
- **📊 AI Reports** - Generate detailed analysis reports using the Qwen model
- **⏰ Scheduling** - Configure automated sending and verification schedules
- **⬇️ Data Export** - Download leads data in CSV or Excel format

## Quick Start

### 1. Navigate to Email Agent

```bash
cd /home/mate/Desktop/github/llm/email_agent
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Google Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable **Google Sheets API** and **Gmail API**
4. Create **OAuth 2.0 Desktop credentials**
5. Download and save as `credentials.json` in the `email_agent` folder

### 4. Configure Your Spreadsheet

Edit `config.json`:
```json
{
  "SPREADSHEET_ID": "your-spreadsheet-id-here"
}
```

### 5. Create Email Template

Create file: `email_to_send/email_08022026.txt`

```
Subject: Special Opportunity for {company}

Dear {first_name},

I hope this email finds you well!

Would you be available for a brief 15-minute call this week?

Best regards,
Your Name
```

### 6. Run the Application

**Streamlit Dashboard (Recommended):**
```bash
streamlit run app.py
```

Open: `http://localhost:8502`

**Or via Command Line:**
```bash
python send_emails.py send      # Send emails
python send_emails.py verify    # Check status
python main.py                  # Generate report
```

## Configuration Details

### config.json Parameters

**Core Settings**
- `MODEL_PATH`: Path to Qwen GGUF model
- `SPREADSHEET_ID`: Your Google Sheet ID
- `CREDENTIALS_JSON`: Google OAuth file location
- `TOKEN_JSON`: Auto-generated token file

**Email Configuration**
- `EMAIL_FOLDER`: Folder containing templates (`email_to_send/`)
- `EMAIL_SUBJECT`: Default email subject
- `EMAIL_COLUMN`: Sheet column name for emails
- `SCHEDULE_TIME`: Send time in HH:MM format
- `SCHEDULE_FREQUENCY_DAYS`: Send frequency (1=daily, 7=weekly)
- `VERIFICATION_HOURS`: Hours to wait before checking status

**Column Names**
- `COL_SENT_AT`: Sheet column for sent timestamp
- `COL_VERIFIED_AT`: Sheet column for verification timestamp
- `COL_BOUNCE_REASON`: Sheet column for bounce reason

### Email Template Placeholders

Supported placeholders in email templates:
- `{first_name}` - Lead's first name
- `{last_name}` - Lead's last name
- `{email}` - Lead's email
- `{company}` - Lead's company name

## Project Structure

```
email_agent/
├── main.py                      # Core pipeline
├── send_emails.py               # Email sending via Gmail API
├── app.py                       # Streamlit dashboard
├── config.json                  # Configuration
├── requirements.txt             # Dependencies
├── credentials.json             # Google OAuth (secret)
├── token.json                   # API token (secret)
├── email_to_send/               # Email templates
│   └── email_DDMMYYYY.txt
├── leads_agent_excel_files/     # Downloaded leads
└── excel_leads_daily_list/      # Generated reports
```

## Usage Guide

### Streamlit Dashboard Tabs

1. **Dashboard** - View all leads with bounce reasons
2. **Send Emails** - Send emails to leads immediately
3. **Verify Status** - Check delivery and bounce statistics
4. **Generate Report** - Create AI-powered analysis or schedule custom reports
5. **Download Data** - Export leads as CSV or Excel

### Command Line Usage

**Send emails for today:**
```bash
python send_emails.py send
```

**Send emails for a specific date:**
```bash
python send_emails.py send 08022026
```

**Verify email status:**
```bash
python send_emails.py verify
```

**Generate report:**
```bash
python main.py
```

## Google Credentials Setup

### Step 1: Create Credentials

1. Visit [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project
3. Enable APIs:
   - Google Sheets API
   - Gmail API
4. Create OAuth 2.0 Desktop credentials
5. Download and save as `credentials.json`

### Step 2: First Authorization

On first run, you'll be prompted:
```
Please visit this URL to authorize this application:
https://accounts.google.com/o/oauth2/auth?...
```

Click the link, authorize, and `token.json` will be auto-created.

### Files Location

```
email_agent/
├── credentials.json     # Your OAuth credentials
└── token.json          # Auto-generated, includes access tokens
```

## Troubleshooting

### Model Issues
- **Model not found**: Ensure model file is at `../Qwen2.5-Coder-32B-Instruct-Q4_K_M.gguf`
- **Out of memory**: Reduce `n_ctx` in main.py or use lower quantization

### Google API Issues
- **Authentication error**: Delete `token.json` and re-authorize
- **Permission denied**: Verify credentials.json and API permissions

### Email Issues
- **No emails found**: Create template at `email_to_send/email_DDMMYYYY.txt`
- **Template not loaded**: Check date format (DDMMYYYY)

### Streamlit Issues
- **Module not found**: Run `pip install -r requirements.txt`
- **Port in use**: Use `streamlit run app.py --server.port 8503`

## Security Notes

⚠️ **Keep These Files Secret:**
- `credentials.json` - OAuth credentials
- `token.json` - API tokens
- `config.json` - May contain sensitive data

Add to `.gitignore`:
```
credentials.json
token.json
*.xlsx
*.csv
report_*.txt
```

## For Complete Setup Details

See [email_agent/README.md](./email_agent/README.md) for:
- Detailed Qwen model installation
- Step-by-step Google credentials setup
- Complete configuration guide
- Email template creation
- Advanced scheduling
- Full troubleshooting guide
