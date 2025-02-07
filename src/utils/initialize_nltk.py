import logging

def initialize_nltk():
    """Initialize NLTK (simplified version)"""
    logger = logging.getLogger(__name__)
    logger.info("NLTK initialization skipped - using TextBlob only") 