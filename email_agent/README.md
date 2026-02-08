# Email Campaign Manager - Complete Setup Guide

⚠️ **IMPORTANT: Before you start, read this section first!**

### Critical Files That Must Be Created/Configured:

1. **`config.json`** - Main configuration file (located in `email_agent/`)
   - Format: JSON
   - Location: `email_agent/config.json`
   - Purpose: Stores all settings (Spreadsheet ID, model path, email configuration)
   - **DANGER:** Add to `.gitignore` to prevent committing sensitive data

2. **`credentials.json`** - Google OAuth credentials (located in `email_agent/`)
   - Format: JSON (downloaded from Google Cloud Console)
   - Location: `email_agent/credentials.json`
   - Purpose: OAuth 2.0 authentication for Google Sheets & Gmail APIs
   - **DANGER:** Contains client_secret - NEVER commit to version control!
   - How to get: See [Google Credentials Setup](#google-credentials-setup) section

3. **`token.json`** - Google API access token (AUTO-GENERATED)
   - Format: JSON (auto-created on first run)
   - Location: `email_agent/token.json`
   - Purpose: Stores access tokens after user authorization
   - **DANGER:** Contains access tokens - NEVER commit to version control!
   - When created: Automatically generated after first authorization

### For Complete JSON Format Details:
📖 **See [JSON_CONFIG_FORMAT.md](./JSON_CONFIG_FORMAT.md)** - Explains format of all 3 files with dummy values shown

### Quick Checklist:
- ✅ Have `config.json` ready (see Configuration section below)
- ✅ Download `credentials.json` from Google Cloud Console (see Google Credentials Setup)
- ✅ Both files go in `email_agent/` directory
- ✅ `token.json` is auto-generated (don't create manually)
- ✅ Add both to `.gitignore`

---

A comprehensive end-to-end email campaign management system with lead tracking, automated sending, status verification, and AI-powered reporting using the Qwen model.

## 📋 Table of Contents

1. [Features](#features)
2. [System Requirements](#system-requirements)
3. [Installation](#installation)
4. [Qwen Model Setup](#qwen-model-setup)
5. [Google Credentials Setup](#google-credentials-setup)
6. [Configuration](#configuration)
7. [Email Templates](#email-templates)
8. [Running the Application](#running-the-application)
9. [Usage Guide](#usage-guide)
10. [Troubleshooting](#troubleshooting)

---

## 🎯 Features

- **📋 Leads Dashboard** - View all leads in a formatted table with bounce reasons displayed prominently
- **✉️ Email Sending** - Send personalized emails to leads from templates using Gmail API
- **🔍 Status Verification** - Check email delivery status and bounce information
- **📊 AI Reports** - Generate detailed analysis reports using the Qwen model
- **⏰ Scheduling** - Configure automated sending and verification schedules
- **⬇️ Data Export** - Download leads data in CSV or Excel format

---

## 🖥️ System Requirements

- Python 3.11+
- 32GB+ RAM (for running Qwen 32B model)
- NVIDIA GPU (recommended for faster inference)
- Linux/Mac or Windows with WSL2
- Internet connection (for Google API access)

---

## 📦 Installation

### Step 1: Clone and Navigate to Project

```bash
cd email_agent
```

### Step 2: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt contents:**
```
accelerate
bitsandbytes
torch
transformers
llama-cpp-python
pandas
openpyxl
pytz
google-auth-oauthlib
google-auth-httplib2
google-api-python-client
streamlit
APScheduler
```

---

## 🤖 Qwen Model Setup

### What is Qwen?

Qwen is an advanced LLM (Large Language Model) from Alibaba that powers the AI report generation. The system uses **Qwen2.5-Coder-32B** quantized to GGUF format for efficient local execution.

### Step 1: Download the Qwen Model

The Qwen model file should be placed in the parent directory of `email_agent`:

```bash
cd ..
```

**Option A: Download from Hugging Face (Recommended)**

```bash
# Using huggingface-cli
huggingface-cli download Qwen/Qwen2.5-Coder-32B-Instruct-GGUF Qwen2.5-Coder-32B-Instruct-Q4_K_M.gguf --local-dir . --local-dir-use-symlinks False
```

Or manually download from: https://huggingface.co/Qwen/Qwen2.5-Coder-32B-Instruct-GGUF

**Option B: Using wget**

```bash
wget https://huggingface.co/Qwen/Qwen2.5-Coder-32B-Instruct-GGUF/resolve/main/Qwen2.5-Coder-32B-Instruct-Q4_K_M.gguf
```

### Step 2: Verify Model Location

The file should be at:
```
./Qwen2.5-Coder-32B-Instruct-Q4_K_M.gguf
```

The config.json references it as:
```json
"MODEL_PATH": "../Qwen2.5-Coder-32B-Instruct-Q4_K_M.gguf"
```

---

## 🔐 Google Credentials Setup

### Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project: **Email Campaign Manager**
3. Enable these APIs:
   - **Google Sheets API**
   - **Gmail API**

### Step 2: Create OAuth 2.0 Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **OAuth Client ID**
3. Select **Desktop application**
4. Download the credentials as JSON
5. Save as `credentials.json` in the `email_agent` folder:

```
email_agent/credentials.json
```

### Step 3: First Time Authorization

When you first run the email sending or Streamlit app, you'll be prompted:

```
Please visit this URL to authorize this application:
https://accounts.google.com/o/oauth2/auth?...
```

1. Click the link
2. Sign in with your Google account
3. Grant permissions for:
   - Google Sheets (read-only)
   - Gmail (read & send)
4. Return to terminal - a `token.json` will be automatically created

**Token location:**
```
email_agent/token.json
```

### Credentials Checklist

- ✅ `credentials.json` - In `email_agent` folder
- ✅ `token.json` - Auto-generated after first authorization
- ✅ Both files are in `.gitignore` (don't commit to version control)

---

## ⚙️ Configuration

### config.json Overview

Located at: `email_agent/config.json`

**Complete configuration file:**

```json
{
  "MODEL_PATH": "../Qwen2.5-Coder-32B-Instruct-Q4_K_M.gguf",
  "SCOPES": [
    "https://www.googleapis.com/auth/spreadsheets.readonly"
  ],
  "CREDENTIALS_JSON": "credentials.json",
  "TOKEN_JSON": "token.json",
  "SPREADSHEET_ID": "1V7_ck61GD0ltJ6pKDfQC-cYjtqYJzrwkbtGAJZ1hL80",
  "OUTPUT_DIR": "leads_agent_excel_files",
  "OUTPUT_PREFIX": "leads_",
  "COL_SENT_AT": "sent_at",
  "COL_VERIFIED_AT": "verified_at",
  "COL_BOUNCE_REASON": "bounce_reason",
  "ENABLE_GMAIL_PULL": false,
  "GMAIL_SCOPES": [
    "https://www.googleapis.com/auth/gmail.readonly"
  ],
  "COL_GMAIL_MSG_ID": "gmail_msg_id",
  "MAX_GMAIL_BODY_CHARS": 2500,
  "EMAIL_CONFIG": {
    "EMAIL_FOLDER": "email_to_send",
    "EMAIL_SUBJECT": "Special Opportunity for You",
    "SCHEDULE_ENABLED": false,
    "SCHEDULE_TIME": "09:00",
    "SCHEDULE_FREQUENCY_DAYS": 1,
    "VERIFICATION_HOURS": 12,
    "EMAIL_COLUMN": "email",
    "EMAIL_TRACKING_SHEET": "email_sends"
  }
}
```

### Configuration Parameters Explained

#### Core Settings
- **MODEL_PATH**: Path to Qwen GGUF model file
- **SPREADSHEET_ID**: Your Google Sheet ID containing leads
- **CREDENTIALS_JSON**: Google OAuth credentials file
- **TOKEN_JSON**: Auto-generated Google API token

#### Folder & File Settings
- **OUTPUT_DIR**: Where downloaded Excel files are saved (`leads_agent_excel_files/`)
- **OUTPUT_PREFIX**: Prefix for downloaded files (default: `leads_`)

#### Column Names (from your Google Sheet)
- **COL_SENT_AT**: Column with email sent timestamp (default: `sent_at`)
- **COL_VERIFIED_AT**: Column with verification timestamp (default: `verified_at`)
- **COL_BOUNCE_REASON**: Column with bounce reason (default: `bounce_reason`)
- **COL_GMAIL_MSG_ID**: Column with Gmail message ID (optional)

#### Email Configuration
- **EMAIL_FOLDER**: Folder containing email templates (`email_to_send/`)
- **EMAIL_SUBJECT**: Default subject line for emails
- **EMAIL_COLUMN**: Sheet column with email addresses (default: `email`)
- **SCHEDULE_ENABLED**: Enable scheduled sending (true/false)
- **SCHEDULE_TIME**: Time to send emails in HH:MM format (e.g., "09:00")
- **SCHEDULE_FREQUENCY_DAYS**: Send frequency (1 = daily, 7 = weekly, etc.)
- **VERIFICATION_HOURS**: Hours to wait before verifying status (default: 12)

#### Gmail Options
- **ENABLE_GMAIL_PULL**: Fetch email snippets from Gmail (requires additional setup)
- **MAX_GMAIL_BODY_CHARS**: Max characters to fetch from Gmail (default: 2500)

### How to Update Configuration

**To change any setting:**

1. Open `config.json` in your editor
2. Modify the value
3. Save the file
4. Restart the Streamlit app or script

**Example: Change verification hours to 24**

```json
"VERIFICATION_HOURS": 24
```

---

## 📧 Email Templates

### What Are Email Templates?

Email templates are text files containing your outreach email. They support personalization using placeholders that are replaced with actual lead data.

### Template Location

```
email_agent/email_to_send/
```

### File Naming Convention

Name templates by date in `DDMMYYYY` format:

```
email_08022026.txt    # For February 8, 2026
email_09022026.txt    # For February 9, 2026
```

The system automatically looks for the template matching today's date.

### Template Format

**Basic structure:**

```
Subject: Your Subject Line Here

Dear {first_name},

Your email body here...

Best regards,
Your Name
```

### Available Placeholders

- `{first_name}` - Lead's first name
- `{last_name}` - Lead's last name
- `{email}` - Lead's email address
- `{company}` - Lead's company name

### Example Template

```
Subject: Special Opportunity for {company}

Dear {first_name},

I hope this email finds you well!

I've been impressed by the work you and your team at {company} are doing. 
I believe there's a unique opportunity that could significantly benefit your organization.

Would you be available for a brief 15-minute call this week? 
I'm flexible with timing and happy to work around your schedule.

Looking forward to connecting!

Best regards,
John Doe
Product Manager
Your Company
john@yourcompany.com
```

### How to Create a New Template

1. Create a file: `email_DDMMYYYY.txt` in `email_to_send/` folder
2. Write your email with Subject: on first line
3. Add placeholders for personalization
4. Save and run the campaign

---

## 🚀 Running the Application

### Option 1: Streamlit Dashboard (Recommended for UI)

The Streamlit app provides a beautiful web interface for managing campaigns.

```bash
cd email_agent
source venv/bin/activate
streamlit run app.py
```

**Access the app:**
- Open browser to: `http://localhost:8502`
- Or: `http://192.168.1.8:8502` (from another machine on network)

### Option 2: Command Line Scripts

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

**Generate report from main script:**

```bash
python main.py
```

---

## 📖 Usage Guide

### Dashboard View

1. **Open Streamlit**: `streamlit run app.py`
2. **Select "Dashboard"** from sidebar
3. View all leads in table format
4. Bounce reasons displayed prominently

### Sending Emails

**Via Streamlit:**

1. Navigate to **"Send Emails"** tab
2. Click **"Send Emails Today"** button
3. Monitor progress in real-time

**Via Command Line:**

```bash
python send_emails.py send
```

### Verifying Status

**Via Streamlit:**

1. Navigate to **"Verify Status"** tab
2. Click **"Verify Status Now"**
3. View metrics:
   - Total Leads
   - Delivered
   - Bounced
   - Bounce details table

**Via Command Line:**

```bash
python send_emails.py verify
```

### Generating Reports

**Option 1: Quick Report (Streamlit)**

1. Navigate to **"Generate Report"** tab
2. Select **"Quick Report"**
3. Click **"Generate Report Now"**
4. View report content in text area

**Option 2: Custom Schedule (Streamlit)**

1. Navigate to **"Generate Report"** tab
2. Select **"Custom Schedule"**
3. Set:
   - **Report Time**: HH:MM format
   - **Frequency**: Daily / Every 2 Days / Weekly
   - **Verification Hours**: 1-72 hours
4. Choose **"Use config.json defaults"** or set custom
5. Click **"Save Schedule"**

### Downloading Data

1. Navigate to **"Download Data"** tab
2. Choose format:
   - **CSV** - For spreadsheet analysis
   - **Excel** - For detailed reports
3. File downloads automatically

### Scheduling Automated Tasks

To enable automatic email sending:

1. Edit `config.json`
2. Set:
   ```json
   "EMAIL_CONFIG": {
     "SCHEDULE_ENABLED": true,
     "SCHEDULE_TIME": "09:00",
     "SCHEDULE_FREQUENCY_DAYS": 1
   }
   ```
3. Run: `python send_emails.py` (as background service)

---

## 🐛 Troubleshooting

### Qwen Model Issues

**Problem**: "Model not found" error

```
FileNotFoundError: Model not found: /path/to/Qwen2.5-Coder-32B-Instruct-Q4_K_M.gguf
```

**Solution**:
1. Verify model is downloaded to parent directory of email_agent
2. Check MODEL_PATH in config.json: `"../Qwen2.5-Coder-32B-Instruct-Q4_K_M.gguf"`
3. Run: `ls -lh ../Qwen2.5-Coder-32B-Instruct-Q4_K_M.gguf`

**Problem**: "CUDA out of memory"

**Solution**:
- Reduce model context: Change `n_ctx=16384` in main.py to lower value
- Or: Use lower quantization (Q5, Q6 instead of Q4)

---

### Google API Issues

**Problem**: "Request had insufficient authentication scopes"

**Solution**:
1. Delete `token.json` in email_agent folder
2. Re-run the script - it will prompt for authorization
3. Grant all requested permissions

**Problem**: "403 Forbidden - Access Denied"

**Solution**:
1. Verify `credentials.json` is in email_agent folder
2. Check Google Cloud Console permissions
3. Ensure APIs are enabled:
   - Google Sheets API ✅
   - Gmail API ✅

---

### Email Sending Issues

**Problem**: "No emails found" / "Email file not found"

**Solution**:
1. Create email template: `email_DDMMYYYY.txt` in `email_to_send/` folder
2. Check date format is correct (DDMMYYYY)
3. For Feb 8, 2026: `email_08022026.txt`

**Problem**: "SMTP Authentication Error" (old SMTP setup)

**Solution**:
- System now uses Gmail API, not SMTP
- No passwords needed
- Just authorize via Google OAuth

---

### Streamlit Issues

**Problem**: "ModuleNotFoundError" when running app

**Solution**:
```bash
# Activate virtual environment
source venv/bin/activate
# Install missing packages
pip install -r requirements.txt
```

**Problem**: "Address already in use" on port 8502

**Solution**:
```bash
# Kill existing Streamlit process
lsof -ti:8502 | xargs kill -9

# Or run on different port
streamlit run app.py --server.port 8503
```

---

### Sheet/Data Issues

**Problem**: "Spreadsheet has no tabs"

**Solution**:
1. Verify `SPREADSHEET_ID` in config.json is correct
2. Ensure sheet has at least one tab
3. Check you have read access to the sheet

**Problem**: Column names not matching

**Solution**:
1. Check actual column names in your Google Sheet
2. Update config.json:
   ```json
   "COL_SENT_AT": "your_sent_column_name",
   "COL_VERIFIED_AT": "your_verified_column_name",
   "COL_BOUNCE_REASON": "your_bounce_column_name",
   "EMAIL_COLUMN": "your_email_column_name"
   ```

---

## 📁 Project Structure

```
email_agent/
├── main.py                          # Core pipeline (download, report generation)
├── send_emails.py                   # Email sending via Gmail API
├── app.py                           # Streamlit dashboard
├── config.json                      # Configuration file (DON'T COMMIT)
├── requirements.txt                 # Python dependencies
├── credentials.json                 # Google OAuth (DON'T COMMIT)
├── token.json                       # Google API token (DON'T COMMIT)
├── email_to_send/                   # Email templates
│   └── email_DDMMYYYY.txt           # Template for specific date
├── leads_agent_excel_files/         # Downloaded Excel files
│   └── leads_DDMMYYYY.xlsx          # Downloaded leads data
└── excel_leads_daily_list/          # Generated reports
    └── report_DDMMYYYY.txt          # AI-generated reports
```

---

## 🔒 Security Notes

### Files to Keep Secret

**Add to .gitignore:**
```
credentials.json
token.json
config.json
*.xlsx
*.csv
report_*.txt
```

**Why?**
- `credentials.json`: Contains OAuth credentials
- `token.json`: Contains access tokens
- `config.json`: May contain sensitive settings
- Data files: Contain personal information

### Best Practices

1. ✅ Use environment variables for secrets
2. ✅ Rotate credentials regularly
3. ✅ Use OAuth 2.0 (not passwords)
4. ✅ Enable 2FA on Google account
5. ✅ Review API permissions in Google Cloud Console

---

## 📞 Support & Debugging

### Enable Verbose Logging

Edit `send_emails.py` to see detailed output:

```python
# Add to imports
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test Components Individually

**Test Google Sheets access:**
```python
from main import download_google_sheet_to_xlsx
download_google_sheet_to_xlsx(SPREADSHEET_ID, "test.xlsx")
```

**Test Email Sending:**
```python
from send_emails import send_emails_to_leads
result = send_emails_to_leads("08022026")
print(result)
```

**Test Report Generation:**
```python
from main import ReportGenerator
gen = ReportGenerator("path/to/model.gguf")
gen.generate_report_from_xlsx("leads.xlsx", "08022026")
```

---

## 🎓 Next Steps

1. ✅ Install dependencies
2. ✅ Download Qwen model
3. ✅ Set up Google credentials
4. ✅ Configure config.json with your Spreadsheet ID
5. ✅ Create email template in email_to_send/
6. ✅ Run `streamlit run app.py`
7. ✅ Send your first campaign!

---

## 📝 License & Notes

- Qwen model is open-source (Apache 2.0)
- Streamlit is open-source (Apache 2.0)
- This project is for educational/business use
- Respect email marketing regulations (CAN-SPAM, GDPR)

---

**Happy Campaigning! 🚀**
