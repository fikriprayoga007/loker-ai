import os
from firecrawl import FirecrawlApp
from dotenv import load_dotenv

load_dotenv()

class JobCrawler:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("FIRECRAWL_API_KEY")
        if not self.api_key:
            raise ValueError("Firecrawl API Key is required")
        self.app = FirecrawlApp(api_key=self.api_key)

    def search_jobs(self, query, limit=5):
        """Searches for job listings using Firecrawl."""
        try:
            # Adding 'job vacancy' to query to improve results
            full_query = f"{query} job vacancy"
            results = self.app.search(full_query, limit=limit)
            return results.get('web', [])
        except Exception as e:
            print(f"Error searching jobs: {e}")
            return []

    def scrape_job_page(self, url):
        """Scrapes a specific job page."""
        try:
            # We want the main content to avoid bloat for the LLM
            data = self.app.scrape_url(url, params={'onlyMainContent': True})
            return data.get('markdown', '') or data.get('content', '')
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return ""
