import os
import time
import json
import google.generativeai as genai
from google.api_core import exceptions
from dotenv import load_dotenv

load_dotenv()

class GeminiService:
    def __init__(self, api_key=None, model_name="gemini-3.1-flash-lite-preview"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API Key is required")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)

    def extract_job_info(self, raw_content, url):
        """Extracts structured job info from raw page content using Gemini."""
        prompt = f"""
        Extract job vacancy details from the following markdown content. 
        Return ONLY a JSON object with the following keys:
        - title
        - company
        - location
        - type (e.g., Full-time, Remote, Contract)
        - salary
        - description (brief summary)
        - url (use the provided URL)

        Content:
        {raw_content[:8000]} 

        URL: {url}
        """

        max_retries = 5
        retry_delay = 5

        while True:
            try:
                response = self.model.generate_content(
                    prompt,
                    generation_config={"response_mime_type": "application/json"}
                )
                return json.loads(response.text)

            except exceptions.ResourceExhausted as e:
                # Handle Rate Limits
                error_msg = str(e).lower()
                if "quota exceeded for quota metric 'generate content requests per day'" in error_msg:
                    print("RPD Limit reached. Delaying 1 day.")
                    time.sleep(86400) # 1 day
                else:
                    print("RPM/TPM Limit reached. Delaying 1 minute.")
                    time.sleep(60) # 1 minute
                continue

            except exceptions.ServiceUnavailable:
                # Handle High Demand
                print("High demand detected. Retrying...")
                time.sleep(retry_delay)
                continue

            except Exception as e:
                print(f"Error calling Gemini: {e}")
                if max_retries > 0:
                    max_retries -= 1
                    time.sleep(retry_delay)
                    continue
                return None
