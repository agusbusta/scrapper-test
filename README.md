Google Search Scraper
====================

A Python-based Google Search scraper that extracts and analyzes search results with sentiment analysis.

Features
--------
- Google Search scraping with customizable parameters
- Sentiment analysis of search results using TextBlob
- Platform identification (blogs, news, social media, discussions)
- Results export in JSON and CSV formats
- Configurable logging system
- Anti-detection measures using Playwright

Requirements
-----------
- Python 3.8+
- Google Chrome browser
- Required Python packages (see requirements.txt)

Installation
-----------
1. Clone the repository
2. Create and activate virtual environment:
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows

3. Install dependencies:
   pip install -r requirements.txt

4. Install Playwright browsers:
   playwright install chromium

Usage
-----
Basic search:
python src/main.py --keyword "your search term" --date "MM/DD/YYYY"

Example:
python src/main.py --keyword "python tutorial" --date "02/10/2024"

Output Files
-----------
Results are saved in data/processed/ directory:
1. JSON file (python_tutorial_02-10-2024.json):
   - Full details including sentiment analysis
   - Complete search result information

2. CSV file (python_tutorial_02-10-2024.csv):
   - title
   - url
   - snippet
   - platform
   - sentiment
   - sentiment_score

Configuration
------------
Edit config/config.yaml to customize:
- User agents for browser simulation
- Request delays and timeouts
- Search parameters
- Output formats
- Platform identifiers

Project Structure
---------------
src/
├── main.py                 # Main script
├── scrapers/
│   └── google_scraper.py   # Google search scraping
└── utils/
    ├── request_handler.py  # Playwright request handling
    ├── sentiment_analyzer.py # TextBlob sentiment analysis
    └── initialize_nltk.py  # NLTK initialization

Logging
-------
- Logs are stored in logs/ directory
- Debug information available in debug_response.html
- Failed searches logged in debug_no_results.html
