"""
Configuration module for SSL certificate handling and user-specific paths.
Provides settings for offline model support and certificate bypass options.
"""

import os
import ssl
import logging
import platform
from pathlib import Path
from typing import Optional, Dict, Any


class Config:
    """Configuration class for handling SSL settings and user-specific paths."""
    
    def __init__(self, username: str = "sanjayfuloria"):
        self.username = username
        self.timestamp = "2025-07-15 08:58:56 UTC"
        
        # Base paths based on problem statement context
        self.base_path = f"/Users/{username}/Documents/Agentic AI Tutorial/Academic_Demos-2"
        
        # User-specific model cache directory
        self.model_cache_dir = self._get_model_cache_dir()
        
        # SSL configuration
        self.ssl_config = self._get_ssl_config()
        
        # Logging configuration
        self.log_config = self._get_log_config()
        
        # Model configuration
        self.model_config = self._get_model_config()
        
    def _get_model_cache_dir(self) -> str:
        """Get user-specific model cache directory."""
        # Create user-specific cache directory
        if platform.system() == "Darwin":  # macOS
            cache_dir = Path.home() / "Library" / "Caches" / "AcademicDemos" / "models"
        else:
            cache_dir = Path.home() / ".cache" / "academic_demos" / "models"
        
        # Ensure directory exists
        cache_dir.mkdir(parents=True, exist_ok=True)
        return str(cache_dir)
    
    def _get_ssl_config(self) -> Dict[str, Any]:
        """Get SSL configuration options."""
        return {
            "verify_ssl": os.getenv("ACADEMIC_DEMOS_VERIFY_SSL", "false").lower() == "true",
            "ssl_cert_file": os.getenv("ACADEMIC_DEMOS_SSL_CERT_FILE"),
            "ssl_ca_bundle": os.getenv("ACADEMIC_DEMOS_SSL_CA_BUNDLE"),
            "disable_ssl_warnings": os.getenv("ACADEMIC_DEMOS_DISABLE_SSL_WARNINGS", "true").lower() == "true",
        }
    
    def _get_log_config(self) -> Dict[str, Any]:
        """Get logging configuration."""
        log_level = os.getenv("ACADEMIC_DEMOS_LOG_LEVEL", "INFO").upper()
        
        # Create logs directory
        log_dir = Path.home() / ".logs" / "academic_demos"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        return {
            "level": getattr(logging, log_level, logging.INFO),
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "log_file": log_dir / "grading_assistant.log",
            "console_output": os.getenv("ACADEMIC_DEMOS_CONSOLE_LOG", "true").lower() == "true",
        }
    
    def _get_model_config(self) -> Dict[str, Any]:
        """Get model configuration options."""
        return {
            "model_name": os.getenv("ACADEMIC_DEMOS_MODEL_NAME", "all-MiniLM-L6-v2"),
            "offline_mode": os.getenv("ACADEMIC_DEMOS_OFFLINE_MODE", "false").lower() == "true",
            "local_files_only": os.getenv("ACADEMIC_DEMOS_LOCAL_FILES_ONLY", "false").lower() == "true",
            "fallback_to_dummy": os.getenv("ACADEMIC_DEMOS_FALLBACK_DUMMY", "true").lower() == "true",
        }
    
    def setup_ssl_context(self) -> Optional[ssl.SSLContext]:
        """Setup SSL context for HTTPS requests."""
        if not self.ssl_config["verify_ssl"]:
            # Create unverified SSL context for bypassing certificate verification
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            return context
        
        # Use custom SSL certificate if provided
        if self.ssl_config["ssl_cert_file"]:
            context = ssl.create_default_context(cafile=self.ssl_config["ssl_cert_file"])
            return context
        
        # Use default SSL context
        return ssl.create_default_context()
    
    def setup_logging(self) -> logging.Logger:
        """Setup logging configuration."""
        # Create logger
        logger = logging.getLogger("academic_demos")
        logger.setLevel(self.log_config["level"])
        
        # Clear existing handlers and close them properly
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)
        
        # Create formatter
        formatter = logging.Formatter(self.log_config["format"])
        
        # File handler
        file_handler = logging.FileHandler(self.log_config["log_file"])
        file_handler.setLevel(self.log_config["level"])
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Console handler
        if self.log_config["console_output"]:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(self.log_config["level"])
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
        
        return logger
    
    def disable_ssl_warnings(self):
        """Disable SSL warnings if configured to do so."""
        if self.ssl_config["disable_ssl_warnings"]:
            try:
                import urllib3
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            except ImportError:
                pass  # urllib3 not available
    
    def get_environment_info(self) -> Dict[str, str]:
        """Get environment information for debugging."""
        return {
            "username": self.username,
            "timestamp": self.timestamp,
            "base_path": self.base_path,
            "model_cache_dir": self.model_cache_dir,
            "platform": platform.system(),
            "python_version": platform.python_version(),
            "ssl_verify": str(self.ssl_config["verify_ssl"]),
            "offline_mode": str(self.model_config["offline_mode"]),
        }


# Global configuration instance
def get_config(username: str = "sanjayfuloria") -> Config:
    """Get global configuration instance."""
    return Config(username=username)