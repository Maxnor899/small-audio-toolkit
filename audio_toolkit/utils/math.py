"""
Common mathematical functions.
"""

import numpy as np


def db_to_amplitude(db: float) -> float:
    """
    Convert decibels to linear amplitude.
    
    Args:
        db: Value in decibels
        
    Returns:
        Linear amplitude value
    """
    return 10.0 ** (db / 20.0)


def amplitude_to_db(amplitude: float, reference: float = 1.0) -> float:
    """
    Convert linear amplitude to decibels.
    
    Args:
        amplitude: Linear amplitude value
        reference: Reference amplitude (default: 1.0)
        
    Returns:
        Value in decibels
        
    Raises:
        ValueError: If amplitude is non-positive
    """
    if amplitude <= 0:
        raise ValueError("Amplitude must be positive")
    return 20.0 * np.log10(amplitude / reference)


def normalize_array(arr: np.ndarray, target_range: tuple = (0.0, 1.0)) -> np.ndarray:
    """
    Normalize array to specified range.
    
    Args:
        arr: Input array
        target_range: Target (min, max) tuple (default: (0, 1))
        
    Returns:
        Normalized array
        
    Raises:
        ValueError: If array has zero range
    """
    min_val = arr.min()
    max_val = arr.max()
    
    if min_val == max_val:
        raise ValueError("Array has zero range, cannot normalize")
    
    normalized = (arr - min_val) / (max_val - min_val)
    target_min, target_max = target_range
    return normalized * (target_max - target_min) + target_min


def rms(signal: np.ndarray) -> float:
    """
    Compute Root Mean Square of signal.
    
    Args:
        signal: Input signal
        
    Returns:
        RMS value
    """
    return float(np.sqrt(np.mean(signal ** 2)))


def zero_crossing_rate(signal: np.ndarray) -> float:
    """
    Compute zero crossing rate.
    
    The zero crossing rate is the rate at which the signal changes sign.
    
    Args:
        signal: Input signal
        
    Returns:
        Zero crossing rate (between 0 and 1)
    """
    sign_changes = np.diff(np.sign(signal))
    return float(np.sum(np.abs(sign_changes)) / (2 * len(signal)))