import streamlit as st
import time
from src.processor import JobProcessor
from src.utils import log_message, format_job_card
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.set_page_config(page_title="AI Job Vacancy Collector", layout="wide")

# Initialize session state
if "is_running" not in st.session_state:
    st.session_state.is_running = False
if "logs" not in st.session_state:
    st.session_state.logs = []
if "found_jobs" not in st.session_state:
    st.session_state.found_jobs = []

# Header
st.title("🚀 AI Job Vacancy Collector")
st.markdown("Search the internet for job vacancies using Firecrawl and Gemini 3.1 Flash-Lite.")

# Sidebar - Configuration
with st.sidebar:
    st.header("Search Parameters")
    keywords = st.text_input("Job Keywords", placeholder="e.g. Senior Python Developer Remote")
    
    col1, col2 = st.columns(2)
    
    if not st.session_state.is_running:
        if st.button("▶️ Start", use_container_width=True, type="primary"):
            if not keywords:
                st.error("Please enter keywords first!")
            else:
                st.session_state.is_running = True
                st.rerun()
    else:
        if st.button("⏹️ Stop", use_container_width=True, type="secondary"):
            st.session_state.is_running = False
            log_message("System stopped by user.", level="WARNING")
            st.rerun()

    st.divider()
    st.info("The system will continue searching until stopped. It automatically handles Gemini API rate limits.")

# Main Layout - Two Columns
col_jobs, col_logs = st.columns([2, 1])

with col_logs:
    st.subheader("📋 System Logs")
    log_container = st.empty()
    # Display logs from session state
    log_text = "\n".join(st.session_state.logs[::-1]) # Show latest first
    log_container.code(log_text if log_text else "Waiting for logs...", language="text")

with col_jobs:
    st.subheader("💼 Job Listings")
    job_container = st.container()
    
    if not st.session_state.found_jobs:
        job_container.info("No jobs found yet. Start the system to begin searching.")
    else:
        for job in st.session_state.found_jobs[::-1]: # Show latest first
            job_container.markdown(format_job_card(job))

# Execution Loop
if st.session_state.is_running:
    try:
        processor = JobProcessor()
        while st.session_state.is_running:
            processor.run_cycle(keywords)
            
            # Update UI by rerunning or just updating containers
            # Since we are in a loop, we can use st.rerun() or rely on the next cycle
            # To keep it alive and responsive, we can sleep a bit
            time.sleep(5)
            st.rerun() # Rerun to refresh the UI with new logs and jobs
            
    except Exception as e:
        log_message(f"Critical Error: {e}", level="ERROR")
        st.session_state.is_running = False
        st.rerun()
