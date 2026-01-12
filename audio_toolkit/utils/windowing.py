"""
Window functions for signal processing.
"""

import numpy as np
from scipy import signal
from typing import Optional


def get_window(window_type: str, length: int) -> np.ndarray:
    """
    Get window function.
    
    Args:
        window_type: Window type ('hann', 'hamming', 'blackman', 'rectangular')
        length: Window length in samples
        
    Returns:
        Window array
        
    Raises:
        ValueError: If window type is invalid or length is non-positive
    """
    if length <= 0:
        raise ValueError("Window length must be positive")
    
    valid_windows = {'hann', 'hamming', 'blackman', 'rectangular'}
    if window_type not in valid_windows:
        raise ValueError(f"Invalid window type '{window_type}'. Valid types: {valid_windows}")
    
    if window_type == 'rectangular':
        return np.ones(length)
    
    return signal.get_window(window_type, length)


def apply_window(signal_data: np.ndarray, window: np.ndarray) -> np.ndarray:
    """
    Apply window to signal.
    
    Args:
        signal_data: Input signal
        window: Window array
        
    Returns:
        Windowed signal
        
    Raises:
        ValueError: If signal and window lengths don't match
    """
    if len(signal_data) != len(window):
        raise ValueError(f"Signal length {len(signal_data)} != window length {len(window)}")
    
    return signal_data * window


def overlap_add(frames: np.ndarray, hop_length: int) -> np.ndarray:
    """
    Reconstruct signal from overlapping frames using overlap-add method.
    
    Args:
        frames: 2D array of shape (n_frames, frame_length)
        hop_length: Hop length between frames in samples
        
    Returns:
        Reconstructed signal
        
    Raises:
        ValueError: If frames is not 2D or hop_length is non-positive
    """
    if frames.ndim != 2:
        raise ValueError(f"Frames must be 2D array, got {frames.ndim}D")
    
    if hop_length <= 0:
        raise ValueError("Hop length must be positive")
    
    n_frames, frame_length = frames.shape
    signal_length = (n_frames - 1) * hop_length + frame_length
    
    reconstructed = np.zeros(signal_length)
    
    for i, frame in enumerate(frames):
        start = i * hop_length
        reconstructed[start:start + frame_length] += frame
    
    return reconstructed