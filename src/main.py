import argparse
from datetime import datetime
import logging
from typing import Dict, List

# Importaciones desde la raíz del proyecto
from scrapers.google_scraper import GoogleScraper
from scrapers.news_scraper import NewsScraper
from scrapers.social_media_scraper import SocialMediaScraper
from scrapers.discussions_scraper import DiscussionsScraper
from pipelines.data_pipeline import DataPipeline
from scrapers.blog_scraper import BlogScraper

def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/main.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Google Search Scraper')
    parser.add_argument('keyword', help='Keyword to search for')
    parser.add_argument('date', help='Date to search (MM/DD/YYYY)')
    parser.add_argument('--config', default='config/config.yaml', help='Path to config file')
    return parser.parse_args()

def extract_detailed_content(results: List[Dict]) -> List[Dict]:
    """Extract detailed content from search results using platform-specific scrapers"""
    news_scraper = NewsScraper()
    social_media_scraper = SocialMediaScraper()
    discussions_scraper = DiscussionsScraper()
    blog_scraper = BlogScraper()
    
    detailed_results = []
    
    for result in results:
        platform = result['platform']
        url = result['url']
        
        detailed_result = result.copy()
        
        if platform == 'news':
            content = news_scraper.extract_article(url)
        elif platform in ['twitter', 'facebook', 'instagram', 'tiktok', 'youtube']:
            content = social_media_scraper.extract_content(url)
        elif platform in ['reddit', 'quora']:
            content = discussions_scraper.extract_discussion(url)
        elif platform == 'blog':
            content = blog_scraper.extract_blog(url)
        else:
            content = None
            
        if content:
            detailed_result.update(content)
            
        detailed_results.append(detailed_result)
        
    return detailed_results

def main():
    # Setup
    args = parse_arguments()
    logger = setup_logging()
    
    try:
        # Initialize scrapers and pipeline
        google_scraper = GoogleScraper(args.config)
        data_pipeline = DataPipeline(args.config)
        
        # Perform Google search
        logger.info(f"Searching for '{args.keyword}' on {args.date}")
        search_results = google_scraper.search(args.keyword, args.date)
        
        if not search_results:
            logger.warning("No search results found")
            return
            
        # Extract detailed content
        logger.info("Extracting detailed content from search results")
        detailed_results = extract_detailed_content(search_results)
        
        # Process and save results
        output_file = data_pipeline.process_results(detailed_results, args.keyword, args.date)
        logger.info(f"Results saved to {output_file}")
        
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise

if __name__ == "__main__":
    main() 