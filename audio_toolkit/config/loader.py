"""
Configuration file loading and validation.
"""

from pathlib import Path
from typing import Dict, Any
import yaml


class ConfigLoader:
    """
    Loads and validates YAML configuration files.
    """
    
    @staticmethod
    def load(config_path: Path) -> Dict[str, Any]:
        """
        Load configuration from YAML file.
        
        Args:
            config_path: Path to YAML configuration file
            
        Returns:
            Validated configuration dictionary
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            ValueError: If configuration is invalid
        """
        pass
    
    @staticmethod
    def validate(config: Dict[str, Any]) -> None:
        """
        Validate configuration structure and values.
        
        Args:
            config: Configuration dictionary to validate
            
        Raises:
            ValueError: If configuration is invalid
        """
        pass
