from typing import Dict
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import logging
import re
from utils.request_handler import RequestHandler
from bs4 import BeautifulSoup
import nltk

class SentimentAnalyzer:
    def __init__(self):
        self._setup_logging()
        self.using_vader = False
        
        try:
            # Intentar diferentes rutas para encontrar VADER
            try:
                nltk.data.find('sentiment/vader_lexicon.zip')
            except LookupError:
                nltk.data.find('sentiment/vader_lexicon/vader_lexicon.txt')
            
            from nltk.sentiment.vader import SentimentIntensityAnalyzer
            self.vader = SentimentIntensityAnalyzer()
            self.using_vader = True
            self.logger.info("VADER initialized successfully")
        except (LookupError, ImportError) as e:
            self.logger.warning(f"Could not initialize VADER: {e}")
            self.logger.info("Using TextBlob only")
            
        self.request_handler = RequestHandler()
        # Palabras clave negativas específicas
        self.negative_keywords = {
            'scam', 'fraud', 'fake', 'cheat', 'scamming', 'scammed',
            'fraudulent', 'misleading', 'deceptive', 'false', 'lying',
            'rip-off', 'ripoff', 'rip off', 'scammer', 'scammers',
            'cheating', 'deceiving', 'defrauding', 'fraudsters',
            'worst', 'terrible', 'horrible', 'bad', 'poor', 'awful', 'unknown'
        }
        # Palabras clave positivas específicas
        self.positive_keywords = {
            'great', 'excellent', 'good', 'best', 'amazing', 'wonderful',
            'fantastic', 'outstanding', 'superb', 'perfect', 'legitimate',
            'authentic', 'genuine', 'reliable', 'trustworthy', 'honest'
        }
        
    def _setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/sentiment.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def _contains_negative_keywords(self, text: str) -> bool:
        """Check if text contains negative keywords"""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.negative_keywords)
        
    def _contains_positive_keywords(self, text: str) -> bool:
        """Check if text contains positive keywords"""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.positive_keywords)
        
    def _extract_article_content(self, url: str) -> str:
        """Extract main content from article URL"""
        try:
            response = self.request_handler.get(url)
            if not response:
                return ""
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove unwanted elements
            for element in soup.select('script, style, nav, header, footer, iframe, .ads, .comments'):
                element.decompose()
                
            # Try to find main content
            article = soup.find(['article', 'main', '.post-content', '.entry-content'])
            if article:
                return article.get_text(strip=True, separator=' ')
                
            # Fallback to paragraphs if no article found
            paragraphs = soup.find_all('p')
            content = ' '.join(p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 50)
            return content
            
        except Exception as e:
            self.logger.error(f"Error extracting article content: {e}")
            return ""
            
    def analyze_text(self, text: str, url: str = None) -> Dict:
        """Analyze sentiment using VADER and TextBlob with fallback to full article"""
        if not text or len(text.strip()) < 50 and url:
            self.logger.info("Text too short, attempting to extract full article")
            article_content = self._extract_article_content(url)
            if article_content:
                text = f"{text} {article_content}"
                
        if not text or len(text.strip()) < 3:
            return {
                'sentiment': 'Neutral',
                'sentiment_score': 0.0
            }
            
        try:
            text = text.lower()
            
            if self.using_vader:
                # VADER analysis
                vader_scores = self.vader.polarity_scores(text)
                compound_score = vader_scores['compound']
                
                # TextBlob as backup
                blob_score = TextBlob(text).sentiment.polarity
                
                # Combine scores
                final_score = (compound_score * 0.7) + (blob_score * 0.3)
            else:
                # TextBlob only
                final_score = TextBlob(text).sentiment.polarity
            
            # Check for negative keywords
            has_negative = any(keyword in text for keyword in self.negative_keywords)
            if has_negative:
                final_score = min(final_score - 0.3, -0.1)
                
            # Determine sentiment category
            if final_score <= -0.1:
                sentiment = 'Negative'
            elif final_score >= 0.1:
                sentiment = 'Positive'
            else:
                sentiment = 'Neutral'
                
            return {
                'sentiment': sentiment,
                'sentiment_score': round(final_score, 2)
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing sentiment: {e}")
            return {
                'sentiment': 'Neutral',
                'sentiment_score': 0.0
            } 