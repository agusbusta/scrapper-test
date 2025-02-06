Google Search Scraper
====================

A comprehensive Google Search scraper that extracts data from various platforms based on keywords and dates.

Features
--------
- Google Search scraping with date filtering
- Platform-specific content extraction:
  * News articles
  * Blogs and content sites
  * Social media posts (Twitter/X, Facebook, Instagram, TikTok)
  * Discussion forums (Reddit, Quora)
  * YouTube content
- Date-specific filtering capabilities
- Multi-platform content extraction
- Anti-bot detection mechanisms
- Proxy support and rotation
- Configurable rate limiting
- Detailed error logging and reporting
- Configurable output formats (JSON, CSV)
- Robust error handling and retry mechanisms

Requirements
-----------
- Python 3.8 or higher
- Chrome/Chromium browser (for JavaScript rendering)
- Stable internet connection
- Sufficient disk space for data storage
- Required Python packages (see requirements.txt)

Installation
------------
1. Prerequisites:

   For macOS:
   - Install Homebrew:
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   - Install Python:
     brew install python
   - Install Chrome:
     brew install --cask google-chrome

   For Ubuntu/Debian:
   - Update package list:
     sudo apt update
   - Install Python and pip:
     sudo apt install python3 python3-pip
   - Install Chrome:
     wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
     sudo apt install ./google-chrome-stable_current_amd64.deb

   For Windows:
   - Download and install Python from python.org
     (Make sure to check "Add Python to PATH" during installation)
   - Download and install Chrome from google.com/chrome

2. Clone the repository:
   git clone https://github.com/yourusername/google-search-scraper.git
   cd google-search-scraper

3. Create and activate virtual environment:

   For macOS/Linux:
   - Create virtual environment:
     python3 -m venv venv
   - Activate it:
     source venv/bin/activate

   For Windows:
   - Create virtual environment:
     python -m venv venv
   - Activate it:
     venv\Scripts\activate

4. Install dependencies:
   - For macOS/Linux:
     pip3 install -r requirements.txt
   - For Windows:
     pip install -r requirements.txt

Configuration
------------
1. Copy the example configuration:
   cp config/config.example.yaml config/config.yaml

2. Edit config/config.yaml to customize:
   - Search parameters
   - Request settings
   - Output format (JSON/CSV)
   - Proxy settings (if needed)
   - Rate limiting parameters

Key Configuration Options:
scraping:
  request_delay: 2  # Delay between requests
  max_retries: 3    # Maximum retry attempts
  timeout: 30       # Request timeout in seconds

output:
  format: "json"    # json or csv
  directory: "data/processed"

Usage Examples
-------------
1. Basic search:
   python src/main.py "mamaearth" "12/10/2024"

2. With custom config:
   python src/main.py "mamaearth" "12/10/2024" --config custom_config.yaml

3. Export as CSV:
   python src/main.py "mamaearth" "12/10/2024" --format csv

Output Format
------------
The scraper generates structured data in JSON or CSV format:

Example JSON output:
{
  "title": "Sample Article Title",
  "url": "https://example.com/article",
  "snippet": "Article description...",
  "platform": "News",
  "date": "2024-12-10",
  "content": "Full article content...",
  "author": "John Doe"
}

Project Structure
---------------
project_name/
├── README.txt
├── requirements.txt
├── config/
│   └── config.yaml
├── data/
│   ├── raw/
│   └── processed/
├── logs/
├── src/
│   ├── main.py
│   ├── scrapers/
│   │   ├── google_scraper.py
│   │   ├── news_scraper.py
│   │   ├── social_media_scraper.py
│   │   └── discussions_scraper.py
│   ├── pipelines/
│   │   └── data_pipeline.py
│   └── utils/
│       └── request_handler.py
└── tests/
    └── ...

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
