import streamlit as st
import time
from .crawler import JobCrawler
from .gemini_service import GeminiService
from .utils import log_message

class JobProcessor:
    def __init__(self):
        self.crawler = JobCrawler()
        self.gemini = GeminiService()
        if "found_jobs" not in st.session_state:
            st.session_state.found_jobs = []
        if "processed_urls" not in st.session_state:
            st.session_state.processed_urls = set()

    def run_cycle(self, keyword):
        """Runs one cycle of searching and processing jobs."""
        log_message(f"Starting search cycle for: {keyword}")
        
        # 1. Search for jobs
        search_results = self.crawler.search_jobs(keyword)
        if not search_results:
            log_message("No results found in this cycle.", level="WARNING")
            return

        for result in search_results:
            # Check if user pressed stop
            if not st.session_state.get("is_running", False):
                break

            url = result.get('url')
            if url in st.session_state.processed_urls:
                continue
            
            log_message(f"Processing: {url}")
            
            # 2. Scrape the page
            content = self.crawler.scrape_job_page(url)
            if not content:
                continue

            # 3. Extract info with Gemini
            job_info = self.gemini.extract_job_info(content, url)
            
            if job_info:
                st.session_state.found_jobs.append(job_info)
                st.session_state.processed_urls.add(url)
                log_message(f"New job found: {job_info.get('title')} at {job_info.get('company')}", level="SUCCESS")
            
            # Small delay to be polite
            time.sleep(2)

        log_message("Cycle completed. Waiting for next run...")
