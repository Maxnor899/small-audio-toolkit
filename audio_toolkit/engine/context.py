"""
Analysis context shared across all analysis methods.
"""

from typing import Dict, List, Tuple, Any
import numpy as np


class AnalysisContext:
    """
    Immutable context passed to each analysis method.
    
    Contains audio data, metadata, and execution parameters.
    """
    
    def __init__(
        self,
        audio_data: Dict[str, np.ndarray],
        sample_rate: int,
        segments: List[Tuple[int, int]],
        metadata: Dict[str, Any]
    ):
        self.audio_data = audio_data
        self.sample_rate = sample_rate
        self.segments = segments
        self.metadata = metadata
