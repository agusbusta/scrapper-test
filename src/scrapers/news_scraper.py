from typing import Dict, Optional
from bs4 import BeautifulSoup
import logging
from utils.request_handler import RequestHandler

class NewsScraper:
    def __init__(self, config_path: str = "config/config.yaml"):
        self.request_handler = RequestHandler(config_path)
        self._setup_logging()
        
    def _setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/news_scraper.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def extract_article(self, url: str) -> Optional[Dict]:
        """Extract content from a news article"""
        response = self.request_handler.get(url)
        if not response:
            return None
            
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract article title
            title = soup.find('h1')
            title_text = title.get_text().strip() if title else ""
            
            # Extract article content
            article_content = ""
            article_body = soup.find(['article', 'div'], class_=['article-body', 'content', 'story-body'])
            if article_body:
                paragraphs = article_body.find_all('p')
                article_content = ' '.join([p.get_text().strip() for p in paragraphs])
                
            # Extract author
            author = soup.find(['a', 'span'], class_=['author', 'byline'])
            author_name = author.get_text().strip() if author else "Unknown"
            
            # Extract date
            date = soup.find(['time', 'span'], class_=['date', 'published'])
            publish_date = date.get_text().strip() if date else ""
            
            return {
                'title': title_text,
                'content': article_content,
                'author': author_name,
                'publish_date': publish_date,
                'url': url,
                'platform': 'news'
            }
            
        except Exception as e:
            self.logger.error(f"Error extracting article from {url}: {e}")
            return None 