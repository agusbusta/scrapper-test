from typing import Dict, Optional
from bs4 import BeautifulSoup
import logging
from utils.request_handler import RequestHandler

class DiscussionsScraper:
    def __init__(self, config_path: str = "config/config.yaml"):
        self.request_handler = RequestHandler(config_path)
        self._setup_logging()
        
    def _setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/discussions_scraper.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def extract_discussion(self, url: str) -> Optional[Dict]:
        """Extract content from discussion platforms"""
        platform = self._identify_platform(url)
        
        if platform == "reddit":
            return self._extract_reddit(url)
        elif platform == "quora":
            return self._extract_quora(url)
        else:
            self.logger.warning(f"Unsupported platform for URL: {url}")
            return None
            
    def _identify_platform(self, url: str) -> str:
        """Identify which discussion platform the URL belongs to"""
        if "reddit.com" in url:
            return "reddit"
        elif "quora.com" in url:
            return "quora"
        return "unknown"
        
    def _extract_reddit(self, url: str) -> Optional[Dict]:
        """Extract content from a Reddit thread"""
        response = self.request_handler.get(url)
        if not response:
            return None
            
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract post title
            title = soup.find('h1')
            title_text = title.get_text().strip() if title else ""
            
            # Extract post content
            content = soup.find('div', attrs={'data-test-id': 'post-content'})
            content_text = content.get_text().strip() if content else ""
            
            # Extract comments (simplified)
            comments = []
            comment_elements = soup.find_all('div', class_='Comment')
            for comment in comment_elements[:10]:  # Limit to top 10 comments
                comment_text = comment.get_text().strip()
                comments.append(comment_text)
                
            return {
                'title': title_text,
                'content': content_text,
                'comments': comments,
                'url': url,
                'platform': 'reddit'
            }
            
        except Exception as e:
            self.logger.error(f"Error extracting Reddit content from {url}: {e}")
            return None
            
    def _extract_quora(self, url: str) -> Optional[Dict]:
        """Extract content from a Quora question/answer"""
        # Implementation would require handling Quora's JavaScript rendering
        self.logger.info("Quora extraction requires JavaScript rendering")
        return None 