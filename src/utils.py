import streamlit as st
from datetime import datetime
import sys

def log_message(message, level="INFO"):
    """Logs a message to the terminal for full tracking."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    emojis = {
        "INFO": "ℹ️",
        "DEBUG": "🔍",
        "WARNING": "⚠️",
        "ERROR": "❌",
        "SUCCESS": "✅"
    }
    
    emoji = emojis.get(level, "📝")
    log_entry = f"[{timestamp}] {emoji} [{level}] {message}"
    
    # PRINT TO TERMINAL (Standard Output)
    print(log_entry, flush=True)
    
    # We still keep it in session state just in case, but it's not shown in UI anymore
    if "logs" not in st.session_state:
        st.session_state.logs = []
    st.session_state.logs.append(log_entry)

def format_job_card(job):
    """Formats a job dictionary into a nice markdown card."""
    return f"""
<div style="border: 1px solid #ddd; padding: 15px; border-radius: 10px; margin-bottom: 15px; background-color: #f9f9f9; color: #333">
    <h3 style="margin-top:0; color: #007bff;">{job.get('title', 'Unknown Title')}</h3>
    <p><b>Company:</b> {job.get('company', 'Unknown')} | <b>Location:</b> {job.get('location', 'Unknown')}</p>
    <p><b>Type:</b> {job.get('type', 'N/A')} | <b>Salary:</b> {job.get('salary', 'Not specified')}</p>
    <hr>
    <p>{job.get('description', '')[:500]}...</p>
    <a href="{job.get('url', '#')}" target="_blank" style="display: inline-block; padding: 5px 10px; background-color: #28a745; color: white; text-decoration: none; border-radius: 5px;">View Job Source</a>
</div>
"""
