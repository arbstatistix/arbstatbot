# JSON Configuration Files Format Guide

This document explains the structure and format of the three main JSON configuration files used in the Email Campaign Manager.

---

## 1. config.json

**Location:** `/home/mate/Desktop/github/llm/email_agent/config.json`

**Purpose:** Main configuration file for the application. Controls all settings for model paths, Google Sheets, and email campaigns.

### Complete Format with Dummy Values

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
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send"
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

### Field Descriptions

| Field | Type | Example | Description |
|-------|------|---------|-------------|
| `MODEL_PATH` | string | `"../Qwen2.5-Coder-32B-Instruct-Q4_K_M.gguf"` | Path to Qwen model GGUF file (relative to email_agent directory) |
| `SCOPES` | array | `["https://www.googleapis.com/auth/spreadsheets.readonly"]` | Google API scopes for Sheets read access |
| `CREDENTIALS_JSON` | string | `"credentials.json"` | Filename of Google OAuth credentials |
| `TOKEN_JSON` | string | `"token.json"` | Filename of Google API token (auto-generated) |
| `SPREADSHEET_ID` | string | `"1V7_ck61GD0ltJ6pKDfQC-cYjtqYJzrwkbtGAJZ1hL80"` | Your Google Sheet ID |
| `OUTPUT_DIR` | string | `"leads_agent_excel_files"` | Directory to save downloaded Excel files |
| `OUTPUT_PREFIX` | string | `"leads_"` | Prefix for downloaded files (e.g., leads_08022026.xlsx) |
| `COL_SENT_AT` | string | `"sent_at"` | Column name in sheet for email sent timestamp |
| `COL_VERIFIED_AT` | string | `"verified_at"` | Column name in sheet for verification timestamp |
| `COL_BOUNCE_REASON` | string | `"bounce_reason"` | Column name in sheet for bounce reason |
| `ENABLE_GMAIL_PULL` | boolean | `false` | Enable fetching email snippets from Gmail |
| `GMAIL_SCOPES` | array | `["https://www.googleapis.com/auth/gmail.readonly", "https://www.googleapis.com/auth/gmail.send"]` | Gmail API scopes |
| `COL_GMAIL_MSG_ID` | string | `"gmail_msg_id"` | Column name for Gmail message IDs |
| `MAX_GMAIL_BODY_CHARS` | number | `2500` | Max characters to fetch from Gmail messages |

### EMAIL_CONFIG Sub-Section

| Field | Type | Example | Description |
|-------|------|---------|-------------|
| `EMAIL_FOLDER` | string | `"email_to_send"` | Folder containing email templates |
| `EMAIL_SUBJECT` | string | `"Special Opportunity for You"` | Default email subject line |
| `SCHEDULE_ENABLED` | boolean | `false` | Enable scheduled email sending |
| `SCHEDULE_TIME` | string | `"09:00"` | Time to send (24-hour format HH:MM) |
| `SCHEDULE_FREQUENCY_DAYS` | number | `1` | Days between sends (1=daily, 7=weekly) |
| `VERIFICATION_HOURS` | number | `12` | Hours to wait before verifying status |
| `EMAIL_COLUMN` | string | `"email"` | Column name in sheet with email addresses |
| `EMAIL_TRACKING_SHEET` | string | `"email_sends"` | Sheet name for tracking sent emails |

### Usage Notes

- **Relative paths**: `MODEL_PATH` is relative to the `email_agent` directory (use `../` to go up one level)
- **Absolute paths**: `OUTPUT_DIR` is relative to current directory
- **Column names**: Must exactly match your Google Sheet column headers
- **Time format**: Use 24-hour format for `SCHEDULE_TIME` (e.g., "14:30" for 2:30 PM)
- **Scopes**: Don't modify unless you understand Google API permissions

---

## 2. credentials.json

**Location:** `/home/mate/Desktop/github/llm/email_agent/credentials.json`

**Purpose:** Contains OAuth 2.0 credentials from Google Cloud Console. Needed for authentication.

**⚠️ CRITICAL:** This file contains sensitive information. Never commit to version control!

### Format with Dummy Values

```json
{
  "type": "oauth2",
  "client_id": "123456789012-abcdefghijklmnopqrstuvwxyz1234.apps.googleusercontent.com",
  "project_id": "email-campaign-manager-123456",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_secret": "GOCSPX-abcdefghijklmnopqrst1234567890",
  "redirect_uris": [
    "http://localhost:8080/",
    "urn:ietf:wg:oauth:2.0:oob"
  ]
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Always `"oauth2"` for desktop applications |
| `client_id` | string | Unique identifier from Google Cloud Console (format: `[number]-[random].apps.googleusercontent.com`) |
| `project_id` | string | Your Google Cloud project ID |
| `auth_uri` | string | Google authentication endpoint (always this value) |
| `token_uri` | string | Token generation endpoint (always this value) |
| `auth_provider_x509_cert_url` | string | Certificate validation URL (always this value) |
| `client_secret` | string | Secret key from Google (starts with `GOCSPX-`) |
| `redirect_uris` | array | Authorized redirect URLs (includes localhost for local testing) |

### Where to Get This File

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project
3. Go to **APIs & Services** → **Credentials**
4. Click **Create Credentials** → **OAuth 2.0 Client ID**
5. Select **Desktop application**
6. Download the JSON file
7. Save as `credentials.json` in `email_agent/` directory

### Security Best Practices

- ✅ Never commit to Git
- ✅ Use with `.gitignore`: `credentials.json`
- ✅ Treat like a password
- ✅ If compromised, regenerate in Google Cloud Console

---

## 3. token.json

**Location:** `/home/mate/Desktop/github/llm/email_agent/token.json`

**Purpose:** Stores OAuth 2.0 access tokens after user authorization. **Auto-generated** on first run.

**⚠️ CRITICAL:** This file contains access tokens. Never commit to version control!

### Format with Dummy Values

```json
{
  "type": "authorized_user",
  "client_id": "123456789012-abcdefghijklmnopqrstuvwxyz1234.apps.googleusercontent.com",
  "client_secret": "GOCSPX-abcdefghijklmnopqrst1234567890",
  "refresh_token": "1//0gK1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z7a8b9c0d1e2f",
  "access_token": "ya29.a0AfH6SMAbCdEfGhIjKlMnOpQrStUvWxYz1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r",
  "token_expiry": "2026-02-08T19:15:42Z",
  "token_uri": "https://oauth2.googleapis.com/token",
  "user_agent": null,
  "scopes": [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/spreadsheets.readonly"
  ],
  "token_info_uri": "https://www.googleapis.com/oauth2/v1/tokeninfo",
  "invalid": false,
  "_class": "OAuth2Credentials",
  "_module": "oauth2client.client"
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Always `"authorized_user"` for user credentials |
| `client_id` | string | Matches `credentials.json` client_id |
| `client_secret` | string | Matches `credentials.json` client_secret |
| `refresh_token` | string | Used to get new access tokens (long-lived) |
| `access_token` | string | Current access token (short-lived, expires) |
| `token_expiry` | string | ISO 8601 timestamp of when access_token expires |
| `token_uri` | string | Endpoint to refresh tokens |
| `user_agent` | null/string | User agent string (usually null) |
| `scopes` | array | List of authorized Google API scopes |
| `token_info_uri` | string | Endpoint to validate token info |
| `invalid` | boolean | True if token is invalid/revoked |
| `_class` | string | Python class name (internal use) |
| `_module` | string | Python module name (internal use) |

### How This File is Created

1. On first run: `python send_emails.py send`
2. You'll see authorization URL
3. User clicks link and authorizes
4. Google redirects with authorization code
5. System exchanges code for tokens
6. `token.json` is automatically created and saved

### Token Lifecycle

- **Access Token**: Expires in ~1 hour
- **Refresh Token**: Long-lived, used to get new access tokens
- **Automatic Refresh**: System refreshes automatically when needed

### If Token Expires

The system will automatically refresh using the `refresh_token`. If refresh fails:
1. Delete `token.json`
2. Re-run the script
3. Authorize again

---

## File Hierarchy & Relationships

```
email_agent/
│
├── config.json                          ← User edits this
│   ├── References: MODEL_PATH
│   ├── References: SPREADSHEET_ID
│   └── References: CREDENTIALS_JSON, TOKEN_JSON filenames
│
├── credentials.json                     ← Downloaded from Google Cloud (secret!)
│   ├── Contains: client_id, client_secret
│   └── Used by: get_creds() function
│
└── token.json                          ← Auto-generated on first run (secret!)
    ├── Contains: access_token, refresh_token
    ├── Generated from: credentials.json
    └── Automatically managed by: Google API client
```

---

## How These Files Work Together

### First Run Flow

```
1. User runs: python send_emails.py send
2. Script reads: config.json
3. Script finds: credentials.json (should already exist)
4. Script checks: token.json (doesn't exist yet)
5. User is prompted: "Please visit this URL to authorize..."
6. User authorizes in browser
7. Script receives: Authorization code
8. Script exchanges: Code → Access token + Refresh token
9. Script saves: token.json (auto-generated)
10. Script sends: Emails using token.json
```

### Subsequent Runs

```
1. User runs: python send_emails.py send
2. Script reads: config.json
3. Script reads: token.json (exists from before)
4. If token valid: Use it directly
5. If token expired: Use refresh_token to get new access_token
6. Script sends: Emails
```

---

## Dummy vs Real Values

### How to Tell If Values Are Dummy

| Value | Dummy Format | Real Format |
|-------|--------------|------------|
| `client_id` | `123456789012-abc...` | `[10-12 digits]-[26 chars].apps.googleusercontent.com` |
| `client_secret` | `GOCSPX-abc...` | `GOCSPX-[20+ random chars]` |
| `refresh_token` | `1//0gK...` | `1//0gK[60+ random chars]` |
| `access_token` | `ya29.a0...` | `ya29.a0[80+ random chars]` |
| `SPREADSHEET_ID` | `1V7_ck61GD0ltJ6pKDfQC-cYjtqYJzrwkbtGAJZ1hL80` | Similar format, different value |

---

## Common Issues & Solutions

### Issue: "credentials.json not found"

**Solution:**
- Ensure file is in `email_agent/` directory
- Check filename spelling (case-sensitive)
- Verify path in config.json: `"CREDENTIALS_JSON": "credentials.json"`

### Issue: "Invalid credentials" error

**Solutions:**
- Delete `token.json`
- Re-download `credentials.json` from Google Cloud Console
- Re-authorize by running script

### Issue: "Token expired"

**Solution:**
- Automatic refresh should handle this
- If not working, delete `token.json` and re-authorize

### Issue: "Access scopes insufficient"

**Solution:**
1. Delete `token.json`
2. Check config.json scopes match what you need
3. Re-authorize with new scopes

---

## File Validation Checklist

Before running the application:

- ✅ `config.json` exists in `email_agent/`
- ✅ `SPREADSHEET_ID` in config.json is valid
- ✅ `MODEL_PATH` points to correct GGUF file
- ✅ `credentials.json` exists in `email_agent/`
- ✅ `credentials.json` has `client_id` and `client_secret` fields
- ✅ Email template file exists: `email_to_send/email_DDMMYYYY.txt`
- ✅ Both files are in `.gitignore`

---

## Summary Table

| File | Location | Created By | Contains | Secret? | Editable? |
|------|----------|-----------|----------|---------|-----------|
| `config.json` | `email_agent/` | User | Settings | No | Yes |
| `credentials.json` | `email_agent/` | Google Cloud Console | OAuth credentials | YES | No |
| `token.json` | `email_agent/` | Script (auto) | Access tokens | YES | No |

---

**Remember:** Always keep `credentials.json` and `token.json` out of version control!
