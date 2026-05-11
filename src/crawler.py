import os
import time
from firecrawl import FirecrawlApp
from dotenv import load_dotenv

load_dotenv()

class JobCrawler:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("FIRECRAWL_API_KEY")
        if not self.api_key:
            raise ValueError("FIRECRAWL_API_KEY is missing in .env")
        
        self.app = FirecrawlApp(api_key=self.api_key)

    def search_jobs(self, keyword):
        """Uses Firecrawl Search with retry logic for 408 Timeouts."""
        query = f"job {keyword}" # Slightly shorter query to avoid timeout
        max_retries = 2
        
        for attempt in range(max_retries + 1):
            try:
                print(f"DEBUG: Requesting Firecrawl Search (Attempt {attempt+1})...")
                results = self.app.search(query)
                
                if isinstance(results, dict):
                    return results.get('data', []) or results.get('web', []) or []
                return results
            except Exception as e:
                error_str = str(e)
                print(f"Error Firecrawl search: {error_str}")
                
                if "408" in error_str and attempt < max_retries:
                    print("DEBUG: Timeout 408 detected. Retrying in 5 seconds...")
                    time.sleep(5)
                    continue
                return []
        return []

    def scrape_page(self, url):
        """Scrapes a page using Firecrawl."""
        if not url: return ""
        try:
            print(f"DEBUG: Requesting Firecrawl Scrape for '{url}'...")
            data = self.app.scrape_url(url, params={'onlyMainContent': True})
            
            if isinstance(data, dict):
                return data.get('markdown', '') or data.get('content', '') or str(data)
            return str(data)
        except Exception as e:
            print(f"Error Firecrawl scraping: {e}")
            return ""
