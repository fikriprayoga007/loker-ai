import streamlit as st
import time
from src.processor import JobProcessor
from src.utils import format_job_card

st.set_page_config(page_title="AI Job Vacancy Collector", page_icon="💼", layout="wide")

st.title("💼 AI Job Vacancy Collector")

# Initialize session state
if "is_running" not in st.session_state:
    st.session_state.is_running = False
if "found_jobs" not in st.session_state:
    st.session_state.found_jobs = []
if "last_job_count" not in st.session_state:
    st.session_state.last_job_count = 0

# Sidebar
with st.sidebar:
    st.header("Search Jobs")
    with st.form("search_form", clear_on_submit=False):
        keyword = st.text_input("Job Keyword", placeholder="e.g. AI Engineer", value=st.session_state.get("last_keyword", ""))
        button_label = "Stop Search" if st.session_state.is_running else "Start Search"
        submit_button = st.form_submit_button(button_label, use_container_width=True)

    if submit_button:
        if st.session_state.is_running:
            st.session_state.is_running = False
            st.rerun()
        else:
            if not keyword:
                st.error("Please enter a keyword!")
            else:
                st.session_state.last_keyword = keyword
                st.session_state.is_running = True
                st.session_state.found_jobs = [] # Reset on new search
                st.rerun()

    st.divider()
    st.metric("Jobs Found", len(st.session_state.found_jobs))

# Main Display
st.subheader("Job Listings")

# Placeholder for real-time updates
job_container = st.container()

with job_container:
    if not st.session_state.found_jobs:
        if st.session_state.is_running:
            st.info("Searching... Please wait for a few moments for the first results to appear in the terminal and then here.")
        else:
            st.info("Enter a keyword and click 'Start Search' to begin.")
    else:
        for job in reversed(st.session_state.found_jobs):
            st.markdown(format_job_card(job), unsafe_allow_html=True)

# Execution Loop
if st.session_state.is_running:
    # We use a trick to make it feel more responsive
    processor = JobProcessor()
    
    # Check if we have new jobs every few seconds by running the cycle
    # The cycle itself now has internal checks to see if is_running is still true
    # Execute one atomic step (one small unit of work)
    processor.run_atomic_step(st.session_state.get("last_keyword", ""))
    
    # After cycle, rerun to show all found jobs
    st.rerun()
