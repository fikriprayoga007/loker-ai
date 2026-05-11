# Job Vacancy Collector

A powerful automated system to find and extract job vacancies from across the internet using AI.

## 🚀 Tech Stack
- **Python 3.11**
- **Streamlit**: For the web-based User Interface.
- **Firecrawl**: Web crawler and search engine accessed via **MCP (Model Context Protocol)**.
- **Gemini 3.1 Flash-Lite**: Google's efficient LLM for high-speed data extraction.
- **Pydantic**: For data validation and structured output.

## 🛠️ Features
- **Continuous Search**: The system runs in a loop until manually stopped.
- **Smart Extraction**: Uses Gemini to parse raw website content into clean, structured job data.
- **Rate Limit Handling**: 
    - Automatic 1-minute delay on RPM/TPM limits.
    - Automatic 1-day delay on RPD (Daily) limits.
    - Automatic retries on High Demand (Service Unavailable).
- **Real-time Monitoring**: Full system logs and job listing updates.

## 📋 Prerequisites
1.  **Firecrawl API Key**: Get it from [firecrawl.dev](https://firecrawl.dev).
2.  **Gemini API Key**: Get it from [Google AI Studio](https://aistudio.google.com).

## ⚙️ Installation
1. Clone the repository.
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory and add your keys:
   ```env
   FIRECRAWL_API_KEY=your_firecrawl_key
   GEMINI_API_KEY=your_gemini_key
   ```

## 🚀 Usage
Run the application using Streamlit:
```bash
streamlit run main.py
```

1. Enter your job search keywords (e.g., "Remote Python Developer").
2. Click **Start** to begin the automated search.
3. Watch the logs and job listings update in real-time.
4. Click **Stop** to halt the system.

## 📂 Project Structure
- `main.py`: Entry point and UI implementation.
- `src/`:
    - `crawler.py`: Firecrawl search and scrape logic.
    - `gemini_service.py`: Gemini API interaction and rate limiting.
    - `processor.py`: Orchestration of the search-scrape-extract cycle.
    - `utils.py`: Logging and UI formatting helpers.
- `requirements.txt`: Project dependencies.