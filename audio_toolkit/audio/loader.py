"""
Multi-channel audio file loading.
"""

from pathlib import Path
from typing import Tuple, Dict, Any
import numpy as np
import soundfile as sf

from ..utils.logging import get_logger

logger = get_logger(__name__)


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
        audio_path = Path(audio_path)
        
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        if not audio_path.is_file():
            raise ValueError(f"Path is not a file: {audio_path}")
        
        try:
            logger.info(f"Loading audio file: {audio_path}")
            audio_data, sample_rate = sf.read(str(audio_path), dtype='float32')
            
            logger.info(f"Loaded: {audio_data.shape}, {sample_rate} Hz")
            
            return audio_data, sample_rate
            
        except RuntimeError as e:
            raise RuntimeError(f"Failed to load audio file {audio_path}: {e}")
    
    @staticmethod
    def get_audio_info(audio_path: Path) -> Dict[str, Any]:
        """
        Get audio file information without loading data.
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Dictionary with: sample_rate, channels, duration, format, subtype
            
        Raises:
            FileNotFoundError: If audio file doesn't exist
        """
        audio_path = Path(audio_path)
        
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        try:
            info = sf.info(str(audio_path))
            
            return {
                'sample_rate': info.samplerate,
                'channels': info.channels,
                'duration': info.duration,
                'frames': info.frames,
                'format': info.format,
                'subtype': info.subtype
            }
            
        except RuntimeError as e:
            raise RuntimeError(f"Failed to read audio info from {audio_path}: {e}")