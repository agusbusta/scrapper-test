import yaml
import logging
import random
import time
from typing import Optional
from playwright.sync_api import sync_playwright

class RequestHandler:
    def __init__(self, config_path: str = "config/config.yaml"):
        self._load_config(config_path)
        self._setup_logging()
        
    def _load_config(self, config_path: str):
        """Load configuration from YAML file"""
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
            
    def _setup_logging(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def _random_sleep(self, min_seconds: float = 1, max_seconds: float = 3):
        time.sleep(random.uniform(min_seconds, max_seconds))
        
    def get(self, url: str, params: dict = None, timeout: int = 30) -> Optional[dict]:
        """Make GET request using Playwright"""
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=True,
                    args=[
                        '--no-sandbox',
                        '--disable-setuid-sandbox',
                        '--disable-blink-features=AutomationControlled',
                        '--disable-extensions',
                        '--disable-component-extensions-with-background-pages',
                        '--disable-default-apps',
                        '--disable-features=TranslateUI',
                        '--disable-background-networking',
                        '--disable-sync',
                        '--metrics-recording-only',
                        '--disable-default-apps',
                        '--no-default-browser-check',
                        '--no-first-run',
                        '--disable-backgrounding-occluded-windows',
                        '--disable-renderer-backgrounding',
                        '--disable-background-timer-throttling',
                    ]
                )
                
                context = browser.new_context(
                    viewport={'width': 1920, 'height': 1080},
                    user_agent=random.choice(self.config["scraping"]["user_agents"]),
                    locale='en-US',
                    timezone_id='America/New_York',
                    permissions=['geolocation'],
                    accept_downloads=True
                )
                
                page = context.new_page()
                
                try:
                    # Visit Google homepage first
                    self.logger.info("Initializing search session...")
                    page.goto('https://www.google.com')
                    page.wait_for_load_state('networkidle')
                    time.sleep(random.uniform(2, 3))
                    
                    # Perform search
                    if params:
                        query_params = '&'.join(f"{k}={v}" for k, v in params.items())
                        full_url = f"{url}?{query_params}"
                    else:
                        full_url = url
                        
                    response = page.goto(full_url)
                    page.wait_for_load_state('networkidle')
                    page.wait_for_selector('div#search', timeout=10000)
                    
                    return type('Response', (), {
                        'text': page.content(),
                        'status_code': response.status if response else 200,
                        'url': page.url
                    })
                    
                finally:
                    browser.close()
                    
        except Exception as e:
            self.logger.error(f"Request error: {str(e)}")
            return None 