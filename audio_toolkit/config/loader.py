"""
Configuration file loading and validation.
"""

from pathlib import Path
from typing import Dict, Any
import yaml

from .schema import (
    VALID_CATEGORIES,
    VALID_CHANNELS,
    VALID_NORMALIZATION_METHODS,
    VALID_EXPORT_FORMATS,
    VALID_VISUALIZATION_FORMATS,
    REQUIRED_CONFIG_KEYS
)
from ..utils.logging import get_logger

logger = get_logger(__name__)


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
            yaml.YAMLError: If YAML parsing fails
        """
        config_path = Path(config_path)
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        if not config_path.is_file():
            raise ValueError(f"Path is not a file: {config_path}")
        
        logger.info(f"Loading configuration from: {config_path}")
        
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Failed to parse YAML: {e}")
        
        if config is None:
            raise ValueError("Configuration file is empty")
        
        if not isinstance(config, dict):
            raise ValueError("Configuration must be a dictionary")
        
        ConfigLoader.validate(config)
        
        logger.info("Configuration loaded and validated successfully")
        
        return config
    
    @staticmethod
    def validate(config: Dict[str, Any]) -> None:
        """
        Validate configuration structure and values.
        
        Args:
            config: Configuration dictionary to validate
            
        Raises:
            ValueError: If configuration is invalid
        """
        for key in REQUIRED_CONFIG_KEYS:
            if key not in config:
                raise ValueError(f"Missing required configuration key: '{key}'")
        
        ConfigLoader._validate_channels(config.get('channels', {}))
        ConfigLoader._validate_preprocessing(config.get('preprocessing', {}))
        ConfigLoader._validate_analyses(config.get('analyses', {}))
        ConfigLoader._validate_visualization(config.get('visualization', {}))
        ConfigLoader._validate_output(config.get('output', {}))
    
    @staticmethod
    def _validate_channels(channels_config: Dict[str, Any]) -> None:
        """Validate channels configuration."""
        if not isinstance(channels_config, dict):
            raise ValueError("'channels' must be a dictionary")
        
        if 'analyze' not in channels_config:
            raise ValueError("'channels.analyze' is required")
        
        requested_channels = channels_config['analyze']
        
        if not isinstance(requested_channels, list):
            raise ValueError("'channels.analyze' must be a list")
        
        if len(requested_channels) == 0:
            raise ValueError("'channels.analyze' cannot be empty")
        
        for channel in requested_channels:
            if channel not in VALID_CHANNELS:
                raise ValueError(
                    f"Invalid channel '{channel}'. Valid channels: {VALID_CHANNELS}"
                )
    
    @staticmethod
    def _validate_preprocessing(preprocessing_config: Dict[str, Any]) -> None:
        """Validate preprocessing configuration."""
        if not isinstance(preprocessing_config, dict):
            return
        
        if 'normalize' in preprocessing_config:
            normalize = preprocessing_config['normalize']
            if isinstance(normalize, dict) and normalize.get('enabled'):
                method = normalize.get('method')
                if method and method not in VALID_NORMALIZATION_METHODS:
                    raise ValueError(
                        f"Invalid normalization method '{method}'. "
                        f"Valid methods: {VALID_NORMALIZATION_METHODS}"
                    )
    
    @staticmethod
    def _validate_analyses(analyses_config: Dict[str, Any]) -> None:
        """Validate analyses configuration."""
        if not isinstance(analyses_config, dict):
            raise ValueError("'analyses' must be a dictionary")
        
        for category in analyses_config.keys():
            if category not in VALID_CATEGORIES:
                logger.warning(
                    f"Unknown analysis category '{category}'. "
                    f"Valid categories: {VALID_CATEGORIES}"
                )
        
        for category, category_config in analyses_config.items():
            if not isinstance(category_config, dict):
                continue
            
            if not category_config.get('enabled', False):
                continue
            
            methods = category_config.get('methods', [])
            if not isinstance(methods, list):
                raise ValueError(f"'{category}.methods' must be a list")
            
            for method in methods:
                if not isinstance(method, dict):
                    raise ValueError(f"Each method in '{category}' must be a dictionary")
                
                if 'name' not in method:
                    raise ValueError(f"Method in '{category}' missing 'name' field")
    
    @staticmethod
    def _validate_visualization(viz_config: Dict[str, Any]) -> None:
        """Validate visualization configuration."""
        if not isinstance(viz_config, dict):
            return
        
        if 'formats' in viz_config:
            formats = viz_config['formats']
            if not isinstance(formats, list):
                raise ValueError("'visualization.formats' must be a list")
            
            for fmt in formats:
                if fmt not in VALID_VISUALIZATION_FORMATS:
                    raise ValueError(
                        f"Invalid visualization format '{fmt}'. "
                        f"Valid formats: {VALID_VISUALIZATION_FORMATS}"
                    )
    
    @staticmethod
    def _validate_output(output_config: Dict[str, Any]) -> None:
        """Validate output configuration."""
        if not isinstance(output_config, dict):
            return
        
        if 'export_formats' in output_config:
            formats = output_config['export_formats']
            if not isinstance(formats, list):
                raise ValueError("'output.export_formats' must be a list")
            
            for fmt in formats:
                if fmt not in VALID_EXPORT_FORMATS:
                    raise ValueError(
                        f"Invalid export format '{fmt}'. "
                        f"Valid formats: {VALID_EXPORT_FORMATS}"
                    )