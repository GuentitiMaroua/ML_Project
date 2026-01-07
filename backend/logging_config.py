"""
Centralized logging configuration for SmartCoach Pro
"""
import logging
from pathlib import Path


def setup_logging():
    """Configure logging for the entire application"""
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / "smartcoach.log", encoding='utf-8'),
            logging.StreamHandler()
        ]
    )


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a module
    
    Args:
        name: Module name (usually __name__)
    
    Returns:
        Logger instance
    """
    return logging.getLogger(name)


# Setup logging when module is imported
setup_logging()
