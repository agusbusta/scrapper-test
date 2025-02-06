import json
import csv
import os
from typing import Dict, List
import logging
from datetime import datetime
import yaml

class DataPipeline:
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config = self._load_config(config_path)
        self._setup_logging()
        self._ensure_directories()
        
    def _load_config(self, config_path: str) -> Dict:
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)
            
    def _setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/pipeline.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def _ensure_directories(self):
        """Create necessary directories if they don't exist"""
        directories = [
            self.config["output"]["directory"],
            "logs",
            "data/raw",
            "data/processed"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            
    def process_results(self, results: List[Dict], keyword: str, date: str) -> str:
        """Process and save search results"""
        # Add metadata
        processed_results = []
        for result in results:
            result.update({
                'keyword': keyword,
                'search_date': date,
                'processed_at': datetime.now().isoformat()
            })
            processed_results.append(result)
            
        # Save results
        output_format = self.config["output"]["format"]
        filename = f"{keyword}_{date.replace('/', '-')}"
        
        if output_format == "json":
            return self._save_json(processed_results, filename)
        elif output_format == "csv":
            return self._save_csv(processed_results, filename)
        else:
            raise ValueError(f"Unsupported output format: {output_format}")
            
    def _save_json(self, data: List[Dict], filename: str) -> str:
        """Save results in JSON format"""
        output_path = os.path.join(
            self.config["output"]["directory"],
            f"{filename}.json"
        )
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Results saved to {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error saving JSON file: {e}")
            raise
            
    def _save_csv(self, data: List[Dict], filename: str) -> str:
        """Save results in CSV format"""
        output_path = os.path.join(
            self.config["output"]["directory"],
            f"{filename}.csv"
        )
        
        try:
            if not data:
                self.logger.warning("No data to save")
                return output_path
                
            fieldnames = data[0].keys()
            
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
                
            self.logger.info(f"Results saved to {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error saving CSV file: {e}")
            raise 