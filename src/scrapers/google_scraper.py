from typing import Dict, List, Optional
from datetime import datetime
import urllib.parse
from bs4 import BeautifulSoup
import logging
from utils.request_handler import RequestHandler
from utils.sentiment_analyzer import SentimentAnalyzer
import time
import random

class GoogleScraper:
    def __init__(self, config_path: str = "config/config.yaml"):
        self.request_handler = RequestHandler(config_path)
        self.config = self.request_handler.config
        self.sentiment_analyzer = SentimentAnalyzer()
        self._setup_logging()
        
    def _setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/google_scraper.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def _build_search_url(self, keyword: str, date: str) -> str:
        """Build Google search URL with date filter"""
        try:
            # Determinar el tipo de búsqueda basado en las palabras clave
            search_type = None
            if any(word in keyword.lower() for word in ['reddit', 'forum', 'discussion']):
                search_type = None  # Búsqueda general para discusiones
            elif any(word in keyword.lower() for word in ['news', 'article']):
                search_type = 'nws'  # Búsqueda de noticias
            elif any(word in keyword.lower() for word in ['blog', 'tutorial']):
                search_type = None  # Búsqueda general para blogs
            
            # Construir parámetros de búsqueda
            params = {
                'q': keyword,
                'num': self.config["google_search"]["results_per_page"],
                'hl': 'en',  # Idioma
                'gl': 'us',  # País
                'as_qdr': 'all',  # Cualquier fecha
                'source': 'lnt',  # Búsqueda avanzada
                'tbs': f'cdr:1,cd_min:{date},cd_max:{date}',  # Filtro de fecha
                'safe': 'off',  # SafeSearch desactivado
                'filter': '0'  # Sin filtrado de resultados similares
            }
            
            # Agregar tipo de búsqueda si es específico
            if search_type:
                params['tbm'] = search_type
                
            base_url = self.config["google_search"]["base_url"]
            url = f"{base_url}?{urllib.parse.urlencode(params)}"
            
            self.logger.debug(f"Built search URL: {url}")
            return url
            
        except Exception as e:
            self.logger.error(f"Error building URL: {e}")
            return None
            
    def _identify_platform(self, url: str) -> str:
        """Identify the platform type based on the URL"""
        for platform_type, domains in self.config["platforms"].items():
            if any(domain in url.lower() for domain in domains):
                return platform_type
        return "other"
        
    def search(self, keyword: str, date: str) -> List[Dict]:
        """Perform Google search with date filtering"""
        self.logger.info(f"Searching for: {keyword} (date: {date})")
        all_results = []
        seen_urls = set()
        page = 0
        max_pages = self.config["google_search"]["max_pages"]
        
        try:
            while page < max_pages:
                params = {
                    'q': keyword,
                    'num': 100,  # Maximum results per page
                    'start': page * 100,  # Skip previous results
                    'hl': 'en',
                    'gl': 'us'
                }
                
                response = self.request_handler.get(
                    'https://www.google.com/search',
                    params=params,
                    timeout=30
                )
                
                if not response:
                    self.logger.error("Failed to get response from Google")
                    break
                    
                page_results = self._parse_search_results(response.text, seen_urls)
                
                if not page_results:
                    self.logger.info("No more results found")
                    break
                    
                all_results.extend(page_results)
                self.logger.info(f"Found {len(page_results)} results on page {page + 1}")
                
                # Check if there's a "Next" button
                soup = BeautifulSoup(response.text, 'html.parser')
                next_button = soup.select_one('#pnnext')
                if not next_button:
                    self.logger.info("No more pages available")
                    break
                    
                page += 1
                time.sleep(random.uniform(2, 4))  # Delay between pages
                
            self.logger.info(f"Total results found: {len(all_results)}")
            return all_results
            
        except Exception as e:
            self.logger.error(f"Search error: {str(e)}")
            return all_results
        
    def _parse_search_results(self, html_content: str, seen_urls: set) -> List[Dict]:
        """Parse Google search results page with sentiment analysis"""
        soup = BeautifulSoup(html_content, 'html.parser')
        results = []

        main_content = soup.select_one('#main, #search, #rso')
        if main_content:
            search_results = main_content.select(
                'div.g, div[data-sokoban-container], div.hlcw0c, div[data-header-feature="0"]'
            )
            
            self.logger.debug(f"Found {len(search_results)} results in main container")
            
            for result in search_results:
                try:
                    # Extract and process result
                    link_container = result.select_one('div.yuRUbf, div.egMi0')
                    if not link_container:
                        continue
                        
                    link_elem = link_container.select_one('a[href^="http"]')
                    if not link_elem:
                        continue
                        
                    url = link_elem['href']
                    
                    # Skip if URL already seen
                    if url in seen_urls:
                        continue
                    seen_urls.add(url)
                    
                    title_elem = link_elem.select_one('h3')
                    if not title_elem:
                        continue
                        
                    snippet_container = result.select_one('div.VwiC3b, div.IsZvec')
                    
                    result_data = {
                        'title': title_elem.get_text().strip(),
                        'url': url,
                        'snippet': snippet_container.get_text().strip() if snippet_container else '',
                        'platform': self._identify_platform(url),
                        **self.sentiment_analyzer.analyze_text(
                            f"{title_elem.get_text().strip()} {snippet_container.get_text().strip() if snippet_container else ''}",
                            url=url
                        )
                    }
                    results.append(result_data)
                    
                except Exception as e:
                    self.logger.error(f"Error processing result: {str(e)}")
                    continue

        return results
        
    def _determine_platform(self, url: str) -> str:
        """Determine the platform type based on URL"""
        # ... resto del código existente ... 