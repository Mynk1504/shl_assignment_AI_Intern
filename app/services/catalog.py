import os
import json
from app.core.logger import logger

def load_catalog(filepath: str) -> list:
    """Load the catalog dataset from a JSON file."""
    if not os.path.exists(filepath):
        logger.error(f"Catalog file not found at {filepath}")
        return []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info(f"Successfully loaded {len(data)} items from catalog.")
        return data
    except Exception as e:
        logger.error(f"Failed to load catalog data: {e}")
        return []
