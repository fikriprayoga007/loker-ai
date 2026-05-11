import os
import json
import time
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class GeminiService:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is missing in .env")
        
        genai.configure(api_key=self.api_key)
        # Using a more standard model name to avoid 404
        self.model_name = 'gemini-3.1-flash-lite-preview'
        try:
            self.model = genai.GenerativeModel(self.model_name)
        except:
            # Fallback to gemini-pro if flash is not found
            self.model = genai.GenerativeModel('gemini-pro')

    def extract_job_info(self, html_content, url):
        """Extracts structured job info from raw content."""
        prompt = f"""
        Extract job vacancy information from the following content. 
        Return ONLY a JSON object with these keys: 
        title, company, location, type, salary, description.
        If info missing, use "Not specified".
        
        URL: {url}
        Content:
        {html_content[:15000]}
        """
        
        try:
            print(f"DEBUG: Requesting Gemini Extraction...")
            response = self.model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            return json.loads(response.text)
        except Exception as e:
            print(f"DEBUG: Gemini Extraction Error: {e}")
            return None

    def extract_links_from_search(self, search_markdown):
        """Extracts job vacancy URLs from search results."""
        prompt = f"""
        Extract all external URLs that likely point to actual job vacancy detail pages.
        Return ONLY a JSON array of strings (URLs).
        
        Content:
        {search_markdown[:10000]}
        """
        try:
            print(f"DEBUG: Requesting Gemini Link Discovery...")
            response = self.model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            # Handle potential markdown code blocks in response
            text = response.text.strip()
            if text.startswith("```"):
                text = text.split("```")[1].replace("json", "").strip()
            
            urls = json.loads(text)
            return urls if isinstance(urls, list) else []
        except Exception as e:
            print(f"DEBUG: Gemini Discovery Error: {e}")
            return []
