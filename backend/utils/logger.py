import logging
import sys
from pathlib import Path
from datetime import datetime
from config.settings import settings

# Ensure UTF-8 console output on Windows
try:
    if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

def setup_logger(name: str) -> logging.Logger:
    """Setup logger with file and console handlers with UTF-8 encoding"""
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(detailed_formatter)
    
    # File handler
    log_file = settings.LOGS_DIR / f"app_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_file, encoding='utf-8', errors='replace')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    
    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

class ProjectLogger:
    """Logger for individual projects"""
    
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.log_file = settings.LOGS_DIR / f"project_{project_id}.log"
        self.logger = self._setup_project_logger()
    
    def _setup_project_logger(self) -> logging.Logger:
        logger = logging.getLogger(f"project_{self.project_id}")
        logger.setLevel(logging.INFO)
        
        if logger.handlers:
            return logger
        
        formatter = logging.Formatter(
            '%(asctime)s - [%(name)s] - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # File handler
        file_handler = logging.FileHandler(self.log_file, encoding='utf-8', errors='replace')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Live Terminal Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        return logger
    
    def info(self, message: str):
        self.logger.info(message)
        self._flush()
    
    def error(self, message: str):
        self.logger.error(message)
        self._flush()
    
    def debug(self, message: str):
        self.logger.debug(message)
        self._flush()
    
    def warning(self, message: str):
        self.logger.warning(message)
        self._flush()

    def _flush(self):
        for h in self.logger.handlers:
            h.flush()