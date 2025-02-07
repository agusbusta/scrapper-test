import nltk
import logging
import time
import os
import shutil
from pathlib import Path
import zipfile
import io

def initialize_nltk():
    """Initialize NLTK and download required resources"""
    logger = logging.getLogger(__name__)
    logger.info("Starting NLTK initialization...")
    
    try:
        nltk_data_dir = os.path.expanduser('~/nltk_data')
        vader_dir = os.path.join(nltk_data_dir, 'sentiment', 'vader_lexicon')
        logger.info(f"Checking VADER directory: {vader_dir}")
        
        # Verificar si VADER ya está instalado correctamente
        try:
            nltk.data.find('sentiment/vader_lexicon.zip')
            logger.info("VADER lexicon already installed and accessible")
            return True
        except LookupError:
            logger.info("VADER not found in NLTK data, attempting installation...")
        
        os.makedirs(vader_dir, exist_ok=True)
        
        # Crear el archivo zip con el lexicon
        zip_path = os.path.join(nltk_data_dir, 'sentiment', 'vader_lexicon.zip')
        
        # Primero intentar con el archivo local
        local_vader = Path('./vader_lexicon/vader_lexicon.txt')
        if local_vader.exists():
            logger.info(f"Found local VADER lexicon at {local_vader}")
            with zipfile.ZipFile(zip_path, 'w') as zf:
                zf.write(local_vader, 'vader_lexicon/vader_lexicon.txt')
            logger.info(f"Created VADER zip at {zip_path}")
            return True
            
        # Si no, intentar con el archivo en venv
        venv_vader = Path('./venv/lib/python3.13/site-packages/vaderSentiment/vader_lexicon.txt')
        if venv_vader.exists():
            logger.info(f"Found VADER lexicon in venv at {venv_vader}")
            with zipfile.ZipFile(zip_path, 'w') as zf:
                zf.write(venv_vader, 'vader_lexicon/vader_lexicon.txt')
            logger.info(f"Created VADER zip at {zip_path}")
            return True
            
        logger.warning("Could not find VADER lexicon locally")
        return False
            
    except Exception as e:
        logger.error(f"Unexpected error initializing NLTK: {str(e)}")
        logger.error("Falling back to TextBlob only")
        return False 