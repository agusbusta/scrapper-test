import argparse
from datetime import datetime
import logging
from typing import Dict, List
import os
import json
import csv

# Importaciones desde la raíz del proyecto
from scrapers.google_scraper import GoogleScraper
from scrapers.news_scraper import NewsScraper
from scrapers.social_media_scraper import SocialMediaScraper
from scrapers.discussions_scraper import DiscussionsScraper
from pipelines.data_pipeline import DataPipeline
from scrapers.blog_scraper import BlogScraper
from utils.initialize_nltk import initialize_nltk

def setup_logging():
    """Configure logging"""
    logging.basicConfig(
        level=logging.DEBUG,  # Cambiado a DEBUG para más detalle
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/main.log'),
            logging.StreamHandler()  # Esto mostrará logs en consola
        ]
    )
    return logging.getLogger(__name__)

def parse_args():
    parser = argparse.ArgumentParser(description='Google Search Scraper')
    parser.add_argument('--keyword', default='tech blogging tips', help='Search keyword')
    parser.add_argument('--date', default=datetime.now().strftime('%m/%d/%Y'), help='Search date (MM/DD/YYYY)')
    parser.add_argument('--config', type=str, help='Path to config file', default='config/config.yaml')
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
    logger = setup_logging()
    logger.info("Starting Google Search Scraper...")
    
    try:
        # Initialize NLTK
        initialize_nltk()
        
        # Get arguments
        args = parse_args()
        logger.info(f"Search parameters: keyword='{args.keyword}', date='{args.date}'")
        
        # Initialize and perform search
        scraper = GoogleScraper(config_path=args.config)
        results = scraper.search(args.keyword, args.date)
        
        if not results:
            logger.warning("No results found")
            return
            
        # Save results
        output_dir = "data/processed"
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{args.keyword.replace(' ', '_')}_{args.date.replace('/', '-')}"
        
        # Save as JSON and CSV
        json_path = os.path.join(output_dir, f"{filename}.json")
        csv_path = os.path.join(output_dir, f"{filename}.csv")
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['title', 'url', 'snippet', 'platform', 'sentiment', 'sentiment_score'])
            writer.writeheader()
            for result in results:
                writer.writerow(result)
                
        logger.info(f"Saved {len(results)} results to {output_dir}")
        
    except Exception as e:
        logger.error(f"Error during execution: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    main() 