"""
Multi-channel audio file loading.
"""

from pathlib import Path
from typing import Tuple
import numpy as np
import soundfile as sf


class AudioLoader:
    """
    Loads audio files in various formats preserving channel information.
    """
    
    @staticmethod
    def load(audio_path: Path) -> Tuple[np.ndarray, int]:
        """
        Load audio file.
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Tuple of (audio_data, sample_rate)
            audio_data shape: (n_samples,) for mono, (n_samples, n_channels) for multi-channel
            
        Raises:
            FileNotFoundError: If audio file doesn't exist
            RuntimeError: If file format is unsupported
        """
        pass
    
    @staticmethod
    def get_audio_info(audio_path: Path) -> dict:
        """
        Get audio file information without loading data.
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Dictionary with: sample_rate, channels, duration, format
        """
        pass
