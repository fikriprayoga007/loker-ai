import streamlit as st
import time
import re
from .crawler import JobCrawler
from .gemini_service import GeminiService
from .utils import log_message

class JobProcessor:
    def __init__(self):
        self.crawler = JobCrawler()
        self.gemini = GeminiService()
        
        # Initialize granular states
        if "found_jobs" not in st.session_state: st.session_state.found_jobs = []
        if "processed_urls" not in st.session_state: st.session_state.processed_urls = set()
        if "search_results" not in st.session_state: st.session_state.search_results = []
        if "current_source_index" not in st.session_state: st.session_state.current_source_index = 0
        if "pending_deep_links" not in st.session_state: st.session_state.pending_deep_links = []

    def is_valid_job_url(self, url):
        if not url: return False
        blacklisted_extensions = ('.svg', '.png', '.jpg', '.jpeg', '.gif', '.css', '.js', '.pdf', '.ico')
        if any(url.lower().split('?')[0].endswith(ext) for ext in blacklisted_extensions):
            return False
        return True

    def run_atomic_step(self, keyword):
        """Processes exactly ONE unit of work (Search, Discover Links, or Extract Job)."""
        
        # A. DISCOVERY PHASE: If no results, search first
        if not st.session_state.search_results:
            log_message(f"Initiating search for: {keyword}...", level="INFO")
            st.session_state.search_results = self.crawler.search_jobs(keyword)
            st.session_state.current_source_index = 0
            time.sleep(3) # Anti-spam delay
            return # Let UI refresh

        # B. DEEP LINK EXTRACTION PHASE: If we have pending deep links, process ONE
        if st.session_state.pending_deep_links:
            job_url = st.session_state.pending_deep_links.pop(0)
            job_url = job_url.split('#')[0]
            
            if job_url in st.session_state.processed_urls or not self.is_valid_job_url(job_url):
                return # Next step

            log_message(f"   -> Processing Deep Link: {job_url}", level="DEBUG")
            job_content = self.crawler.scrape_page(job_url)
            time.sleep(2) # Delay
            
            if job_content:
                job_info = self.gemini.extract_job_info(job_content, job_url)
                time.sleep(2) # Delay
                if job_info and job_info.get('title') and job_info.get('title') != "Not specified":
                    st.session_state.found_jobs.append(job_info)
                    st.session_state.processed_urls.add(job_url)
                    log_message(f"      ✅ JOB DISCOVERED: {job_info.get('title')}", level="SUCCESS")
            return # Let UI refresh and show the new job

        # C. ANALYSIS PHASE: Pick the next source to analyze
        idx = st.session_state.current_source_index
        if idx >= len(st.session_state.search_results):
            log_message("All sources processed. Restarting discovery.", level="INFO")
            st.session_state.search_results = [] # Trigger new search
            return

        source = st.session_state.search_results[idx]
        st.session_state.current_source_index += 1

        source_url = source.get('url') or source.get('link') or source.get('item')
        if not source_url and 'content' in source:
            match = re.search(r'https?://[^\s\)]+', source['content'])
            if match: source_url = match.group(0)
        
        if source_url:
            source_url = source_url.split('#')[0]

        if not source_url or not self.is_valid_job_url(source_url):
            return

        log_message(f"Analyzing Source [{idx+1}/{len(st.session_state.search_results)}]: {source_url}", level="INFO")
        
        landing_content = self.crawler.scrape_page(source_url)
        time.sleep(2)
        
        if landing_content:
            new_links = self.gemini.extract_links_from_search(landing_content)
            time.sleep(2)
            if new_links:
                # Add found links to pending queue (limit 3 per source)
                st.session_state.pending_deep_links = new_links[:3]
            else:
                # If no links, treat the source itself as a job link
                st.session_state.pending_deep_links = [source_url]
        
        return # Let UI refresh
