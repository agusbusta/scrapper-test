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

<<<<<<< HEAD
Logging
-------
- Logs are stored in logs/ directory
- Debug information available in debug_response.html
- Failed searches logged in debug_no_results.html
=======
Limitations and Known Issues
--------------------------
1. Rate Limiting:
   - Google may block requests if too many are made too quickly
   - Use proxy rotation for better results

2. Platform Restrictions:
   - Some social media platforms require API authentication
   - Content behind login walls may not be accessible

3. JavaScript:
   - Some sites require JavaScript rendering
   - Ensure Chrome/Chromium is properly installed

Troubleshooting
--------------
1. If pip/python is not found:
   - Make sure Python is properly installed and added to PATH
   - Try using pip3/python3 instead of pip/python

2. If you get permission errors:
   - On Unix systems, you might need to use sudo
   - Or better, use: pip install --user -r requirements.txt

3. If you get SSL errors:
   - Try updating certificates:
     pip install --upgrade certifi

4. Virtual environment issues:
   - If venv creation fails, try:
     python3 -m pip install --user virtualenv
     python3 -m virtualenv venv

5. If you encounter Google blocks:
   - Increase request_delay in config.yaml
   - Enable proxy rotation
   - Verify your IP isn't blacklisted

6. For memory issues:
   - Reduce max_pages in config
   - Use CSV output for large datasets

Security Considerations
---------------------
1. API Keys:
   - Never commit API keys to version control
   - Use environment variables for sensitive data

2. Proxy Usage:
   - Verify proxy reliability and security
   - Rotate proxies regularly

3. Rate Limiting:
   - Respect website robots.txt
   - Implement appropriate delays
>>>>>>> b6edd6af1ac29fba30970ccdf2b2fe7a1ac025b1
