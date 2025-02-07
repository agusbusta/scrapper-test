from typing import Dict
from textblob import TextBlob
import logging

class SentimentAnalyzer:
    def __init__(self):
        self._setup_logging()
        
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
        
    def analyze_text(self, text: str) -> Dict:
        """Analyze sentiment of text using TextBlob"""
        if not text or len(text.strip()) < 3:
            return {
                'sentiment': 'Neutral',
                'sentiment_score': 0.0
            }
            
        try:
            # TextBlob analysis
            analysis = TextBlob(text)
            polarity = analysis.sentiment.polarity
            
            # Convertir score a categoría
            if polarity > 0.1:
                sentiment = 'Positive'
            elif polarity < -0.1:
                sentiment = 'Negative'
            else:
                sentiment = 'Neutral'
                
            return {
                'sentiment': sentiment,
                'sentiment_score': round(polarity, 2)
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing sentiment: {e}")
            return {
                'sentiment': 'Neutral',
                'sentiment_score': 0.0
            } 