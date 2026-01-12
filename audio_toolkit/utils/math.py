"""
Common mathematical functions.
"""

import numpy as np


def db_to_amplitude(db: float) -> float:
    """Convert dB to amplitude."""
    pass


def amplitude_to_db(amplitude: float) -> float:
    """Convert amplitude to dB."""
    pass


def normalize_array(arr: np.ndarray) -> np.ndarray:
    """Normalize array to [0, 1] range."""
    pass


def rms(signal: np.ndarray) -> float:
    """Compute RMS value of signal."""
    pass


def zero_crossing_rate(signal: np.ndarray) -> float:
    """Compute zero crossing rate."""
    pass
