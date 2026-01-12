"""
Channel management: L, R, mono, sum, difference.
"""

from typing import Dict, List
import numpy as np

from ..utils.logging import get_logger

logger = get_logger(__name__)


class ChannelProcessor:
    """
    Processes multi-channel audio into individual and derived channels.
    """
    
    @staticmethod
    def extract_channels(
        audio_data: np.ndarray,
        requested_channels: List[str]
    ) -> Dict[str, np.ndarray]:
        """
        Extract requested channels from audio data.
        
        Args:
            audio_data: Raw audio data from loader
                Shape: (n_samples,) for mono or (n_samples, n_channels) for multi-channel
            requested_channels: List of channel names to extract
                Valid: 'left', 'right', 'mono', 'sum', 'difference'
            
        Returns:
            Dictionary mapping channel names to audio data
            
        Raises:
            ValueError: If requested channel is invalid or unavailable
        """
        valid_channels = {'left', 'right', 'mono', 'sum', 'difference'}
        
        for channel in requested_channels:
            if channel not in valid_channels:
                raise ValueError(f"Invalid channel '{channel}'. Valid: {valid_channels}")
        
        channels = {}
        
        is_mono = audio_data.ndim == 1
        is_stereo = audio_data.ndim == 2 and audio_data.shape[1] >= 2
        
        logger.info(f"Processing {len(requested_channels)} channels from {'mono' if is_mono else 'stereo'} audio")
        
        for channel_name in requested_channels:
            
            if channel_name == 'left':
                if is_mono:
                    channels['left'] = audio_data
                elif is_stereo:
                    channels['left'] = audio_data[:, 0]
                else:
                    raise ValueError("Cannot extract 'left' channel from audio data")
            
            elif channel_name == 'right':
                if is_mono:
                    channels['right'] = audio_data
                elif is_stereo:
                    channels['right'] = audio_data[:, 1]
                else:
                    raise ValueError("Cannot extract 'right' channel: not stereo")
            
            elif channel_name == 'mono':
                channels['mono'] = ChannelProcessor.to_mono(audio_data)
            
            elif channel_name == 'sum':
                if not is_stereo:
                    raise ValueError("Cannot compute 'sum': need stereo audio")
                left = audio_data[:, 0]
                right = audio_data[:, 1]
                channels['sum'] = ChannelProcessor.compute_sum(left, right)
            
            elif channel_name == 'difference':
                if not is_stereo:
                    raise ValueError("Cannot compute 'difference': need stereo audio")
                left = audio_data[:, 0]
                right = audio_data[:, 1]
                channels['difference'] = ChannelProcessor.compute_difference(left, right)
        
        return channels
    
    @staticmethod
    def compute_sum(left: np.ndarray, right: np.ndarray) -> np.ndarray:
        """
        Compute L + R.
        
        Args:
            left: Left channel
            right: Right channel
            
        Returns:
            Sum of channels
        """
        return left + right
    
    @staticmethod
    def compute_difference(left: np.ndarray, right: np.ndarray) -> np.ndarray:
        """
        Compute L - R.
        
        Args:
            left: Left channel
            right: Right channel
            
        Returns:
            Difference of channels
        """
        return left - right
    
    @staticmethod
    def to_mono(audio_data: np.ndarray) -> np.ndarray:
        """
        Convert multi-channel to mono by averaging.
        
        Args:
            audio_data: Input audio (mono or multi-channel)
            
        Returns:
            Mono audio
        """
        if audio_data.ndim == 1:
            return audio_data
        
        return np.mean(audio_data, axis=1)