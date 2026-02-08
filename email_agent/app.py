#!/usr/bin/env python3
"""
Streamlit frontend for email campaign and lead management dashboard.
"""
import json
import os
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import pytz
import streamlit as st

from main import load_config, download_google_sheet_to_xlsx, ReportGenerator, get_creds
from send_emails import send_emails_to_leads, verify_email_status, get_email_content, format_email_content


def load_email_config(config_file: str = "config.json") -> dict:
    """Load configuration from JSON file."""
    with open(config_file, "r", encoding="utf-8") as f:
        config = json.load(f)
    return config


def get_leads_dataframe(date_str: str = None) -> pd.DataFrame:
    """Download and load leads from sheet."""
    if date_str is None:
        date_str = datetime.now().strftime("%d%m%Y")
    
    config = load_config()
    output_dir = Path(config.get("OUTPUT_DIR", "leads_agent_excel_files"))
    output_prefix = config.get("OUTPUT_PREFIX", "leads_")
    xlsx_path = output_dir / f"{output_prefix}{date_str}.xlsx"
    
    download_google_sheet_to_xlsx(config["SPREADSHEET_ID"], xlsx_path)
    df = pd.read_excel(xlsx_path)
    return df, xlsx_path


def display_leads_table():
    """Display leads in a formatted table."""
    st.header("📋 Leads Dashboard")
    
    date_str = datetime.now().strftime("%d%m%Y")
    
    try:
        df, _ = get_leads_dataframe(date_str)
        config = load_config()
        
        # Get column names
        col_bounce_reason = config.get("COL_BOUNCE_REASON", "bounce_reason")
        col_sent_at = config.get("COL_SENT_AT", "sent_at")
        col_verified_at = config.get("COL_VERIFIED_AT", "verified_at")
        
        # Format display - make bounce_reason column wider
        display_df = df.copy()
        
        # Filter columns for display
        display_cols = ["lead_id", "first_name", "email", "company", "status", col_sent_at]
        if col_bounce_reason in display_df.columns:
            display_cols.append(col_bounce_reason)
        if col_verified_at in display_df.columns:
            display_cols.append(col_verified_at)
        
        # Only show existing columns
        display_cols = [c for c in display_cols if c in display_df.columns]
        display_df = display_df[display_cols]
        
        # Custom CSS for wider bounce reason column
        st.markdown("""
        <style>
        .dataframe { width: 100%; }
        .dataframe th, .dataframe td { 
            padding: 12px;
            text-align: left;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.dataframe(display_df, width='stretch', height=400)
        
        st.success(f"✓ Loaded {len(df)} leads from {date_str}")
        
    except Exception as e:
        st.error(f"Error loading leads: {e}")


def send_email_now():
    """Send emails immediately."""
    st.header("✉️ Send Emails Now")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Send Emails Today", key="send_btn"):
            date_str = datetime.now().strftime("%d%m%Y")
            
            with st.spinner("Sending emails..."):
                try:
                    result = send_emails_to_leads(date_str)
                    st.success(f"✓ Sent: {result['success']} | Failed: {result['failed']}")
                    st.write(result)
                except Exception as e:
                    st.error(f"Error sending emails: {e}")
    
    with col2:
        st.info("Make sure SMTP credentials are configured in config.json")


def verify_status():
    """Verify email status and get back information."""
    st.header("🔍 Verify Email Status")
    
    if st.button("Verify Status Now", key="verify_btn"):
        date_str = datetime.now().strftime("%d%m%Y")
        
        with st.spinner("Verifying email status..."):
            try:
                result = verify_email_status(date_str)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Leads", result['total_leads'])
                with col2:
                    st.metric("Delivered", result['delivered'])
                with col3:
                    st.metric("Bounced", result['bounced'])
                
                if result['bounce_details']:
                    st.subheader("Bounce Details")
                    bounce_df = pd.DataFrame(result['bounce_details'])
                    st.dataframe(bounce_df, width='stretch')
                
            except Exception as e:
                st.error(f"Error verifying status: {e}")


def generate_report():
    """Generate report using the model."""
    st.header("📊 Generate Report")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        report_type = st.radio(
            "Report Type",
            ["Quick Report", "Custom Schedule"],
            horizontal=True
        )
    
    if report_type == "Quick Report":
        if st.button("Generate Report Now", key="report_btn"):
            date_str = datetime.now().strftime("%d%m%Y")
            
            with st.spinner("Generating report..."):
                try:
                    config = load_config()
                    model_path = os.path.abspath(config["MODEL_PATH"])
                    
                    _, xlsx_path = get_leads_dataframe(date_str)
                    
                    gen = ReportGenerator(model_path)
                    report_path = gen.generate_report_from_xlsx(xlsx_path, date_str)
                    
                    st.success(f"✓ Report generated: {report_path}")
                    
                    # Display report content
                    with open(report_path, "r") as f:
                        report_content = f.read()
                    st.text_area("Report Content", report_content, height=400)
                    
                except Exception as e:
                    st.error(f"Error generating report: {e}")
    
    else:  # Custom Schedule
        st.subheader("⏰ Schedule Custom Report")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            report_time = st.time_input("Report Time", value=datetime.strptime("09:00", "%H:%M").time())
        
        with col2:
            report_frequency = st.selectbox("Frequency", ["Daily", "Every 2 Days", "Weekly"])
        
        with col3:
            verification_hours = st.number_input("Verification Hours", min_value=1, max_value=72, value=12)
        
        # Use defaults or custom
        use_config_defaults = st.checkbox("Use config.json defaults", value=True)
        
        if st.button("Save Schedule", key="schedule_btn"):
            config = load_email_config()
            
            if not use_config_defaults:
                # Update config with custom values
                config["EMAIL_CONFIG"]["SCHEDULE_TIME"] = report_time.strftime("%H:%M")
                
                freq_map = {"Daily": 1, "Every 2 Days": 2, "Weekly": 7}
                config["EMAIL_CONFIG"]["SCHEDULE_FREQUENCY_DAYS"] = freq_map.get(report_frequency, 1)
                config["EMAIL_CONFIG"]["VERIFICATION_HOURS"] = verification_hours
                
                with open("config.json", "w") as f:
                    json.dump(config, f, indent=2)
                
                st.success("✓ Custom schedule saved to config.json")
            else:
                st.info("✓ Using defaults from config.json")


def download_data():
    """Download the leads data."""
    st.header("⬇️ Download Data")
    
    date_str = datetime.now().strftime("%d%m%Y")
    
    try:
        df, xlsx_path = get_leads_dataframe(date_str)
        
        # Convert to CSV
        csv = df.to_csv(index=False)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.download_button(
                label="Download as CSV",
                data=csv,
                file_name=f"leads_{date_str}.csv",
                mime="text/csv"
            )
        
        with col2:
            # Excel download
            excel_bytes = pd.ExcelFile(xlsx_path).book
            st.download_button(
                label="Download as Excel",
                data=open(xlsx_path, "rb").read(),
                file_name=f"leads_{date_str}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
    except Exception as e:
        st.error(f"Error downloading data: {e}")


def main():
    """Main Streamlit app."""
    st.set_page_config(
        page_title="Email Campaign Manager",
        page_icon="📧",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Sidebar
    with st.sidebar:
        st.title("📧 Email Campaign Manager")
        
        page = st.radio(
            "Navigation",
            ["Dashboard", "Send Emails", "Verify Status", "Generate Report", "Download Data"]
        )
        
        st.markdown("---")
        
        with st.expander("⚙️ Configuration"):
            st.write("Current configuration values:")
            config = load_config()
            email_cfg = config.get("EMAIL_CONFIG", {})
            
            st.metric("Spreadsheet ID", config["SPREADSHEET_ID"][:20] + "...")
            st.metric("Sender Email", email_cfg.get("SENDER_EMAIL", "Not configured"))
            st.metric("Verification Hours", email_cfg.get("VERIFICATION_HOURS", 12))
            st.metric("Schedule Enabled", email_cfg.get("SCHEDULE_ENABLED", False))
    
    # Main content
    if page == "Dashboard":
        display_leads_table()
    elif page == "Send Emails":
        send_email_now()
    elif page == "Verify Status":
        verify_status()
    elif page == "Generate Report":
        generate_report()
    elif page == "Download Data":
        download_data()
    
    # Footer
    st.markdown("---")
    st.markdown("Built for Email Campaign Management")


if __name__ == "__main__":
    main()
