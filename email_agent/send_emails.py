#!/usr/bin/env python3
"""
Email sending script with scheduler using Gmail API.
Reads emails from email_to_send folder and sends them to leads from the Google Sheet.
"""
import os
import json
import base64
from pathlib import Path
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from main import load_config, download_google_sheet_to_xlsx, get_creds
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


def load_email_config(config_file: str = "config.json") -> dict:
    """Load configuration from JSON file."""
    with open(config_file, "r", encoding="utf-8") as f:
        config = json.load(f)
    return config


def get_email_content(date_str: str) -> str:
    """
    Load email content from email_to_send folder.
    Expected format: email_to_send/email_(DDMMYYYY).txt
    """
    email_folder = Path("email_to_send")
    email_file = email_folder / f"email_{date_str}.txt"
    
    if not email_file.exists():
        raise FileNotFoundError(f"Email file not found: {email_file}")
    
    with open(email_file, "r", encoding="utf-8") as f:
        return f.read()


def format_email_content(content: str, lead_data: dict) -> tuple:
    """
    Format email content with lead data.
    Returns (subject, body)
    """
    # Extract subject and body
    lines = content.split("\n")
    subject = ""
    body = ""
    
    if lines and lines[0].startswith("Subject:"):
        subject = lines[0].replace("Subject:", "").strip()
        body = "\n".join(lines[2:]).strip()  # Skip empty line after subject
    else:
        subject = "Special Opportunity for You"
        body = content
    
    # Format with lead data
    placeholders = {
        "{first_name}": lead_data.get("first_name", ""),
        "{company}": lead_data.get("company", ""),
        "{email}": lead_data.get("email", ""),
        "{last_name}": lead_data.get("last_name", ""),
    }
    
    for placeholder, value in placeholders.items():
        subject = subject.replace(placeholder, str(value))
        body = body.replace(placeholder, str(value))
    
    return subject, body


def send_email_via_gmail_api(recipient_email: str, subject: str, body: str, 
                             sender_email: str, gmail_service) -> bool:
    """
    Send email using Gmail API.
    """
    try:
        msg = MIMEText(body, "plain")
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = recipient_email
        
        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        send_message = {"raw": raw}
        
        gmail_service.users().messages().send(userId="me", body=send_message).execute()
        print(f"[OK] Email sent to {recipient_email}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to send email to {recipient_email}: {e}")
        return False


def send_emails_to_leads(date_str: str = None) -> dict:
    """
    Main function to send emails to all leads from the sheet using Gmail API.
    """
    if date_str is None:
        date_str = datetime.now().strftime("%d%m%Y")
    
    config = load_email_config()
    email_cfg = config.get("EMAIL_CONFIG", {})
    
    # Get Gmail credentials (expanded scopes to include sending + sheets access)
    combined_scopes = [
        "https://www.googleapis.com/auth/gmail.send", 
        "https://www.googleapis.com/auth/gmail.readonly",
        "https://www.googleapis.com/auth/spreadsheets.readonly"
    ]
    
    try:
        creds = get_creds(combined_scopes)
        gmail_service = build("gmail", "v1", credentials=creds)
        
        # Get authenticated user's email
        profile = gmail_service.users().getProfile(userId="me").execute()
        sender_email = profile.get("emailAddress", "")
        
        if not sender_email:
            raise ValueError("Could not retrieve sender email from Gmail profile")
        
    except Exception as e:
        raise ValueError(f"Gmail API authentication failed: {e}")
    
    email_subject = email_cfg.get("EMAIL_SUBJECT", "Special Opportunity for You")
    email_column = email_cfg.get("EMAIL_COLUMN", "email")
    
    # Download sheet to dated XLSX
    output_dir = Path(config.get("OUTPUT_DIR", "leads_agent_excel_files"))
    output_prefix = config.get("OUTPUT_PREFIX", "leads_")
    xlsx_path = output_dir / f"{output_prefix}{date_str}.xlsx"
    
    download_google_sheet_to_xlsx(config["SPREADSHEET_ID"], xlsx_path)
    print(f"[OK] Downloaded sheet to {xlsx_path}")
    
    # Load leads from Excel
    df = pd.read_excel(xlsx_path)
    
    # Get email content
    try:
        email_content = get_email_content(date_str)
    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
        return {"success": 0, "failed": 0, "error": str(e)}
    
    # Send emails
    success_count = 0
    failed_count = 0
    sent_recipients = []
    
    for idx, row in df.iterrows():
        email = row.get(email_column, "")
        if not email or pd.isna(email):
            continue
        
        try:
            subject, body = format_email_content(email_content, row.to_dict())
            if send_email_via_gmail_api(email, subject, body, sender_email, gmail_service):
                success_count += 1
                sent_recipients.append(email)
            else:
                failed_count += 1
        except Exception as e:
            print(f"[ERROR] Error processing {email}: {e}")
            failed_count += 1
    
    result = {
        "success": success_count,
        "failed": failed_count,
        "timestamp": datetime.now().isoformat(),
        "recipients": sent_recipients,
        "sender": sender_email
    }
    
    print(f"\n[SUMMARY] Sent: {success_count}, Failed: {failed_count}")
    return result


def verify_email_status(date_str: str = None) -> dict:
    """
    Verify email status by checking bounce information and update sent_at timestamp.
    """
    if date_str is None:
        date_str = datetime.now().strftime("%d%m%Y")
    
    config = load_email_config()
    output_dir = Path(config.get("OUTPUT_DIR", "leads_agent_excel_files"))
    output_prefix = config.get("OUTPUT_PREFIX", "leads_")
    xlsx_path = output_dir / f"{output_prefix}{date_str}.xlsx"
    
    # Download latest sheet
    download_google_sheet_to_xlsx(config["SPREADSHEET_ID"], xlsx_path)
    
    df = pd.read_excel(xlsx_path)
    col_sent_at = config.get("COL_SENT_AT", "sent_at")
    col_bounce_reason = config.get("COL_BOUNCE_REASON", "bounce_reason")
    
    # Count bounced vs delivered
    bounced = df[col_bounce_reason].notna().sum()
    delivered = df[col_bounce_reason].isna().sum()
    
    return {
        "timestamp": datetime.now().isoformat(),
        "total_leads": len(df),
        "delivered": delivered,
        "bounced": bounced,
        "bounce_details": df[df[col_bounce_reason].notna()][[
            "email", col_bounce_reason
        ]].to_dict(orient="records") if col_bounce_reason in df.columns else []
    }


def setup_scheduler():
    """
    Setup background scheduler for periodic email sending.
    """
    config = load_email_config()
    email_cfg = config.get("EMAIL_CONFIG", {})
    
    if not email_cfg.get("SCHEDULE_ENABLED", False):
        print("[INFO] Scheduler is disabled in config")
        return None
    
    schedule_time = email_cfg.get("SCHEDULE_TIME", "09:00")
    frequency_days = email_cfg.get("SCHEDULE_FREQUENCY_DAYS", 1)
    
    scheduler = BackgroundScheduler()
    
    # Schedule based on frequency
    if frequency_days == 1:
        scheduler.add_job(
            send_emails_to_leads,
            'cron',
            hour=int(schedule_time.split(":")[0]),
            minute=int(schedule_time.split(":")[1]),
            id='daily_email_send'
        )
    else:
        scheduler.add_job(
            send_emails_to_leads,
            'interval',
            days=frequency_days,
            hour=int(schedule_time.split(":")[0]),
            minute=int(schedule_time.split(":")[1]),
            id='periodic_email_send'
        )
    
    scheduler.start()
    print(f"[OK] Scheduler started. Next send at {schedule_time}")
    return scheduler


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "send":
        date_arg = sys.argv[2] if len(sys.argv) > 2 else None
        result = send_emails_to_leads(date_arg)
        print(f"Result: {result}")
    elif len(sys.argv) > 1 and sys.argv[1] == "verify":
        date_arg = sys.argv[2] if len(sys.argv) > 2 else None
        result = verify_email_status(date_arg)
        print(f"Result: {result}")
    else:
        print("Usage:")
        print("  python send_emails.py send [DDMMYYYY]  - Send emails for a specific date")
        print("  python send_emails.py verify [DDMMYYYY] - Verify email status")

