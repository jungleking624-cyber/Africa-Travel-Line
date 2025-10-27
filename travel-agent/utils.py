"""
Utility functions for the Travel FAQ Agent
"""

import logging
import re
from pathlib import Path
from datetime import datetime
from typing import Optional

def setup_logging(log_dir: str = "logs", log_level: str = "INFO") -> logging.Logger:
    """Setup logging configuration"""
    log_dir_path = Path(log_dir)
    log_dir_path.mkdir(exist_ok=True)
    
    # Create log filename with timestamp
    log_file = log_dir_path / f"agent_{datetime.now().strftime('%Y%m%d')}.log"
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger("TravelFAQAgent")
    logger.info(f"Logging initialized. Log file: {log_file}")
    
    return logger


def sanitize_input(text: str, max_length: int = 2000) -> str:
    """Sanitize user input"""
    if not text:
        return ""
    
    # Strip whitespace
    text = text.strip()
    
    # Remove potential HTML/script tags
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<[^>]+>', '', text)
    
    # Limit length
    if len(text) > max_length:
        text = text[:max_length]
    
    return text


def extract_destination(query: str) -> Optional[str]:
    """Extract destination/country from user query"""
    # Simple pattern matching for common destination formats
    patterns = [
        r'to\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',  # "to Japan", "to New Zealand"
        r'in\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',  # "in Thailand"
        r'for\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)', # "for Kenya"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, query)
        if match:
            return match.group(1)
    
    return None


def format_error_message(error: Exception, user_friendly: bool = True) -> str:
    """Format error messages"""
    if user_friendly:
        return "I encountered an error while processing your request. Please try again or rephrase your question."
    else:
        return f"Error: {type(error).__name__}: {str(error)}"