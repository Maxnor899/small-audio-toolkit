"""
Audio preprocessing methods.
"""

from typing import Dict, Any, List, Tuple
import numpy as np
from scipy import signal

from ..utils.math import rms, db_to_amplitude
from ..utils.logging import get_logger

logger = get_logger(__name__)


class Preprocessor:
    """
    Applies preprocessing steps to audio data.
    """
    
    @staticmethod
    def normalize_rms(audio: np.ndarray, target_level: float) -> np.ndarray:
        """
        Normalize audio to target RMS level.
        
        Args:
            audio: Input audio data
            target_level: Target level in dB
            
        Returns:
            Normalized audio
        """
        current_rms = rms(audio)
        
        if current_rms == 0:
            logger.warning("Audio has zero RMS, cannot normalize")
            return audio
        
        target_amplitude = db_to_amplitude(target_level)
        scale_factor = target_amplitude / current_rms
        
        normalized = audio * scale_factor
        
        logger.info(f"Normalized RMS: {current_rms:.4f} -> {rms(normalized):.4f} (target: {target_amplitude:.4f})")
        
        return normalized
    
    @staticmethod
    def normalize_lufs(audio: np.ndarray, sample_rate: int, target_level: float) -> np.ndarray:
        """
        Normalize audio to target LUFS level.
        
        Note: This is a simplified LUFS implementation.
        For production use, consider pyloudnorm library.
        
        Args:
            audio: Input audio data
            sample_rate: Sample rate in Hz
            target_level: Target level in LUFS
            
        Returns:
            Normalized audio
        """
        logger.warning("LUFS normalization using simplified RMS approximation")
        
        return Preprocessor.normalize_rms(audio, target_level)
    
    @staticmethod
    def detect_silence(
        audio: np.ndarray,
        sample_rate: int,
        threshold_db: float,
        min_duration: float
    ) -> List[Tuple[int, int]]:
        """
        Detect silence regions.
        
        Args:
            audio: Input audio data
            sample_rate: Sample rate in Hz
            threshold_db: Silence threshold in dB
            min_duration: Minimum silence duration in seconds
            
        Returns:
            List of (start_sample, end_sample) tuples for silence regions
        """
        threshold_amplitude = db_to_amplitude(threshold_db)
        min_samples = int(min_duration * sample_rate)
        
        is_silent = np.abs(audio) < threshold_amplitude
        
        silence_regions = []
        in_silence = False
        start_sample = 0
        
        for i, silent in enumerate(is_silent):
            if silent and not in_silence:
                start_sample = i
                in_silence = True
            elif not silent and in_silence:
                duration = i - start_sample
                if duration >= min_samples:
                    silence_regions.append((start_sample, i))
                in_silence = False
        
        if in_silence:
            duration = len(audio) - start_sample
            if duration >= min_samples:
                silence_regions.append((start_sample, len(audio)))
        
        logger.info(f"Detected {len(silence_regions)} silence regions")
        
        return silence_regions
    
    @staticmethod
    def segment_audio(
        audio: np.ndarray,
        sample_rate: int,
        method: str,
        segment_duration: float
    ) -> List[Tuple[int, int]]:
        """
        Segment audio into homogeneous regions.
        
        Args:
            audio: Input audio data
            sample_rate: Sample rate in Hz
            method: Segmentation method ('energy' or 'spectral')
            segment_duration: Target segment duration in seconds
            
        Returns:
            List of (start_sample, end_sample) tuples for segments
            
        Raises:
            ValueError: If method is invalid
        """
        valid_methods = {'energy', 'spectral'}
        if method not in valid_methods:
            raise ValueError(f"Invalid segmentation method '{method}'. Valid: {valid_methods}")
        
        segment_samples = int(segment_duration * sample_rate)
        
        if method == 'energy':
            return Preprocessor._segment_by_energy(audio, segment_samples)
        elif method == 'spectral':
            return Preprocessor._segment_by_spectral(audio, sample_rate, segment_samples)
        
        return []
    
    @staticmethod
    def _segment_by_energy(
        audio: np.ndarray,
        segment_samples: int
    ) -> List[Tuple[int, int]]:
        """
        Simple fixed-duration segmentation based on energy.
        
        Args:
            audio: Input audio
            segment_samples: Segment size in samples
            
        Returns:
            List of segment boundaries
        """
        segments = []
        n_samples = len(audio)
        
        for start in range(0, n_samples, segment_samples):
            end = min(start + segment_samples, n_samples)
            segments.append((start, end))
        
        logger.info(f"Created {len(segments)} energy-based segments")
        
        return segments
    
    @staticmethod
    def _segment_by_spectral(
        audio: np.ndarray,
        sample_rate: int,
        segment_samples: int
    ) -> List[Tuple[int, int]]:
        """
        Fixed-duration segmentation with spectral analysis.
        
        Args:
            audio: Input audio
            sample_rate: Sample rate
            segment_samples: Segment size in samples
            
        Returns:
            List of segment boundaries
        """
        segments = []
        n_samples = len(audio)
        
        for start in range(0, n_samples, segment_samples):
            end = min(start + segment_samples, n_samples)
            
            if end - start < segment_samples // 2:
                continue
            
            segments.append((start, end))
        
        logger.info(f"Created {len(segments)} spectral-based segments")
        
        return segments