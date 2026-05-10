import streamlit as st
from datetime import datetime

def log_message(message, level="INFO"):
    """Adds a message to the session state logs."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}"
    
    if "logs" not in st.session_state:
        st.session_state.logs = []
    
    st.session_state.logs.append(log_entry)
    # Keep only last 100 logs
    if len(st.session_state.logs) > 100:
        st.session_state.logs.pop(0)

def format_job_card(job):
    """Formats a job dictionary into a nice markdown card."""
    return f"""
### {job.get('title', 'Unknown Title')}
**Company:** {job.get('company', 'Unknown')} | **Location:** {job.get('location', 'Unknown')}
**Type:** {job.get('type', 'N/A')} | **Salary:** {job.get('salary', 'Not specified')}

{job.get('description', '')[:300]}...

[View Job Source]({job.get('url', '#')})
---
"""
