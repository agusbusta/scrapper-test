from typing import Dict, Optional
from bs4 import BeautifulSoup
import logging
from utils.request_handler import RequestHandler

class BlogScraper:
    def __init__(self, config_path: str = "config/config.yaml"):
        self.request_handler = RequestHandler(config_path)
        self._setup_logging()
        
    def _setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/blog_scraper.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def extract_blog(self, url: str) -> Optional[Dict]:
        """Extract content from blog posts"""
        try:
            response = self.request_handler.get(url)
            if not response:
                return None
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Intentar extraer el contenido del blog
            title = soup.find(['h1', 'header'])
            content = soup.find(['article', 'div.post-content', 'div.entry-content'])
            author = soup.find(['a.author', 'span.author', 'div.author'])
            date = soup.find(['time', 'span.date', 'div.date'])
            
            return {
                'title': title.get_text().strip() if title else "",
                'content': content.get_text().strip() if content else "",
                'author': author.get_text().strip() if author else "",
                'publish_date': date.get_text().strip() if date else "",
                'url': url,
                'platform': 'blog'
            }
            
        except Exception as e:
            self.logger.error(f"Error extracting blog content from {url}: {e}")
            return None 