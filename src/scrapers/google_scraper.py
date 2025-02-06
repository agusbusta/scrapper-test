from typing import Dict, List, Optional
from datetime import datetime
import urllib.parse
from bs4 import BeautifulSoup
import logging
from utils.request_handler import RequestHandler

class GoogleScraper:
    def __init__(self, config_path: str = "config/config.yaml"):
        self.request_handler = RequestHandler(config_path)
        self.config = self.request_handler.config
        self._setup_logging()
        
    def _setup_logging(self):
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/scraper.log'),
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
        
    def _parse_search_results(self, html_content: str) -> List[Dict]:
        """Parse Google search results page"""
        soup = BeautifulSoup(html_content, 'html.parser')
        results = []
        
        # Selectores para diferentes tipos de resultados
        search_results = (
            soup.select('div.g') or  # Resultados generales
            soup.select('div.rc') or  # Resultados alternativos
            soup.select('div[data-hveid]') or  # Resultados con data-hveid
            soup.select('div.yuRUbf')  # Contenedor de resultados
        )
        
        for result in search_results:
            try:
                # Intentar extraer título y link
                title_elem = (
                    result.select_one('h3') or
                    result.select_one('.LC20lb') or
                    result.select_one('.DKV0Md')
                )
                
                link_elem = (
                    result.select_one('a') or
                    result.select_one('.yuRUbf > a')
                )
                
                snippet_elem = (
                    result.select_one('.VwiC3b') or
                    result.select_one('.st') or
                    result.select_one('.aCOpRe')
                )
                
                if title_elem and link_elem:
                    url = link_elem['href']
                    if url.startswith(('http://', 'https://')):
                        result_data = {
                            'title': title_elem.get_text().strip(),
                            'url': url,
                            'snippet': snippet_elem.get_text().strip() if snippet_elem else '',
                            'platform': self._identify_platform(url)
                        }
                        results.append(result_data)
                        self.logger.debug(f"Parsed result: {result_data['title']}")
                        
            except Exception as e:
                self.logger.error(f"Error parsing result: {e}")
                continue
                
        return results
        
    def search(self, keyword: str, date: str) -> List[Dict]:
        """Perform Google search and return results"""
        search_url = self._build_search_url(keyword, date)
        if not search_url:
            return []
            
        self.logger.info(f"Searching for: {keyword} on date: {date}")
        self.logger.debug(f"Using URL: {search_url}")
        
        response = self.request_handler.get(search_url)
        if not response:
            self.logger.error("Failed to get response from Google")
            return []
            
        self.logger.debug(f"Response status code: {response.status_code}")
        self.logger.debug(f"Response headers: {response.headers}")
        
        results = self._parse_search_results(response.text)
        self.logger.info(f"Found {len(results)} results")
        
        if len(results) == 0:
            self.logger.debug("Response content: " + response.text[:500] + "...")
            
        return results 