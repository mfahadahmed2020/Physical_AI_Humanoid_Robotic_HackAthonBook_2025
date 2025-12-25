import logging
import sys
from datetime import datetime
from enum import Enum
from typing import Any, Dict
import json
from pathlib import Path


class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Logger:
    def __init__(self, name: str, level: LogLevel = LogLevel.INFO, log_file: str = None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.value))
        
        # Prevent adding multiple handlers if logger already exists
        if not self.logger.handlers:
            # Create console handler
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(getattr(logging, level.value))
            
            # Create formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(formatter)
            
            # Add console handler to logger
            self.logger.addHandler(console_handler)
            
            # Add file handler if specified
            if log_file:
                file_handler = logging.FileHandler(log_file)
                file_handler.setLevel(getattr(logging, level.value))
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)
    
    def _log(self, level: LogLevel, message: str, extra: Dict[str, Any] = None):
        log_method = getattr(self.logger, level.value.lower())
        if extra:
            # Add extra context to the log
            extra_str = json.dumps(extra, default=str)
            log_method(f"{message} | Context: {extra_str}")
        else:
            log_method(message)
    
    def debug(self, message: str, extra: Dict[str, Any] = None):
        self._log(LogLevel.DEBUG, message, extra)
    
    def info(self, message: str, extra: Dict[str, Any] = None):
        self._log(LogLevel.INFO, message, extra)
    
    def warning(self, message: str, extra: Dict[str, Any] = None):
        self._log(LogLevel.WARNING, message, extra)
    
    def error(self, message: str, extra: Dict[str, Any] = None):
        self._log(LogLevel.ERROR, message, extra)
    
    def critical(self, message: str, extra: Dict[str, Any] = None):
        self._log(LogLevel.CRITICAL, message, extra)


# Global logger instance for the application
app_logger = Logger("RoboticsTextbookAPI", log_file="logs/app.log")


# Ensure log directory exists
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)


def get_logger(name: str) -> Logger:
    """Get a logger instance with the specified name"""
    return Logger(name)


def log_api_call(endpoint: str, method: str, user_id: str = None, extra: Dict[str, Any] = None):
    """Log API calls with relevant information"""
    context = {
        "endpoint": endpoint,
        "method": method,
        "user_id": user_id,
        "timestamp": datetime.utcnow().isoformat(),
        **(extra or {})
    }
    app_logger.info(f"API call to {method} {endpoint}", extra=context)


def log_user_action(user_id: str, action: str, resource: str, extra: Dict[str, Any] = None):
    """Log user actions for audit purposes"""
    context = {
        "user_id": user_id,
        "action": action,
        "resource": resource,
        "timestamp": datetime.utcnow().isoformat(),
        **(extra or {})
    }
    app_logger.info(f"User {user_id} performed {action} on {resource}", extra=context)


def log_simulation_event(simulation_id: str, event: str, status: str, extra: Dict[str, Any] = None):
    """Log simulation events"""
    context = {
        "simulation_id": simulation_id,
        "event": event,
        "status": status,
        "timestamp": datetime.utcnow().isoformat(),
        **(extra or {})
    }
    app_logger.info(f"Simulation {simulation_id}: {event} - {status}", extra=context)