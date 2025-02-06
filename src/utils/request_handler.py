from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import time
import random
import logging
import yaml
import os

class RequestHandler:
    def __init__(self, config_path: str = "config/config.yaml"):
        if not hasattr(self, 'initialized'):
            self.config = self._load_config(config_path)
            self._setup_logging()
            self.playwright = None
            self.browser = None
            self.context = None
            self.page = None
            self.initialized = True
            
    def _setup_browser(self):
        """Initialize Playwright browser"""
        if not self.browser:
            try:
                self.logger.info("Iniciando navegador...")
                
                self.playwright = sync_playwright().start()
                self.browser = self.playwright.chromium.launch(
                    headless=True,
                    args=[
                        '--no-sandbox',
                        '--disable-dev-shm-usage',
                        '--disable-blink-features=AutomationControlled',
                        '--disable-extensions',
                        '--disable-component-extensions-with-background-pages',
                        '--disable-default-apps',
                        '--disable-features=TranslateUI,BlinkGenPropertyTrees',
                        '--disable-popup-blocking',
                        '--disable-background-networking',
                        '--metrics-recording-only',
                        '--no-default-browser-check',
                        '--no-first-run',
                    ]
                )
                
                # Configurar el contexto con evasión de detección
                self.context = self.browser.new_context(
                    viewport={'width': 1920, 'height': 1080},
                    user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    java_script_enabled=True,
                    bypass_csp=True,
                    extra_http_headers={
                        'Accept-Language': 'en-US,en;q=0.9',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"macOS"',
                        'Sec-Fetch-Dest': 'document',
                        'Sec-Fetch-Mode': 'navigate',
                        'Sec-Fetch-Site': 'none',
                        'Sec-Fetch-User': '?1',
                    }
                )
                
                # Configurar la página
                self.page = self.context.new_page()
                self.page.set_default_timeout(30000)
                
                # Evadir detección de webdriver
                self.page.add_init_script("""
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    });
                """)
                
                self.logger.info("Navegador iniciado correctamente")
                
            except Exception as e:
                self.logger.error(f"Error iniciando navegador: {str(e)}")
                self._quit_browser()
                raise
                
    def get(self, url: str, params: dict = None) -> str:
        """Make GET request using Playwright"""
        max_retries = self.config.get('request', {}).get('retry_attempts', 3)
        
        for attempt in range(max_retries):
            try:
                if not self.page:
                    self._setup_browser()
                    
                delay = random.uniform(2, 4)
                self.logger.debug(f"Waiting {delay:.2f} seconds before request")
                time.sleep(delay)
                
                if params:
                    query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
                    url = f"{url}?{query_string}"
                    
                self.logger.debug(f"Requesting URL: {url}")
                
                # Simular comportamiento humano
                self.page.goto('https://www.google.com', wait_until='networkidle')
                time.sleep(random.uniform(1, 2))
                
                response = self.page.goto(url, wait_until='networkidle', timeout=30000)
                
                # Esperar y simular scroll
                self.page.wait_for_selector('body', timeout=10000)
                self._simulate_human_behavior()
                
                content = self.page.content()
                
                return type('Response', (), {
                    'text': content,
                    'status_code': response.status if response else 200,
                    'headers': response.headers if response else {},
                    'url': self.page.url
                })
                
            except PlaywrightTimeout:
                self.logger.warning(f"Timeout en intento {attempt + 1}/{max_retries}")
                continue
                
            except Exception as e:
                self.logger.error(f"Error en request (intento {attempt + 1}/{max_retries}): {str(e)}")
                if attempt == max_retries - 1:
                    return None
                    
                self._quit_browser()
                time.sleep(random.uniform(3, 6))
                
    def _quit_browser(self):
        """Cerrar y limpiar browser"""
        try:
            if self.page:
                self.page.close()
                self.page = None
            if self.context:
                self.context.close()
                self.context = None
            if self.browser:
                self.browser.close()
                self.browser = None
        except Exception as e:
            self.logger.error(f"Error cerrando navegador: {str(e)}")
            
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file"""
        if not os.path.isabs(config_path):
            root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            config_path = os.path.join(root_dir, config_path)
            
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
            
    def _setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/request_handler.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def _simulate_human_behavior(self):
        """Simulate human-like behavior"""
        try:
            # Scroll aleatorio
            for _ in range(random.randint(2, 4)):
                self.page.evaluate('window.scrollBy(0, window.innerHeight * Math.random())')
                time.sleep(random.uniform(0.5, 1.5))
                
            # Mover el mouse aleatoriamente
            self.page.mouse.move(
                random.randint(100, 700),
                random.randint(100, 700)
            )
            
        except Exception as e:
            self.logger.warning(f"Error simulando comportamiento humano: {e}") 