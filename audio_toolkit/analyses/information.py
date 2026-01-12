"""
Information theory analysis methods.
"""

from typing import Dict, Any
import numpy as np

from ..engine.context import AnalysisContext
from ..engine.results import AnalysisResult
from ..engine.registry import register_method


def shannon_entropy(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Compute Shannon entropy.
    
    Args:
        context: Analysis context
        params: window_size, normalize
        
    Returns:
        AnalysisResult with entropy values
    """
    pass


def local_entropy(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Compute local entropy over sliding window.
    
    Args:
        context: Analysis context
        params: window_size, hop_length
        
    Returns:
        AnalysisResult with local entropy values
    """
    pass


def compression_ratio(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Compute compression ratio.
    
    Args:
        context: Analysis context
        params: algorithm ('gzip' or 'lz77')
        
    Returns:
        AnalysisResult with compression ratios
    """
    pass


def approximate_complexity(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Measure approximate algorithmic complexity.
    
    Args:
        context: Analysis context
        params: analysis parameters
        
    Returns:
        AnalysisResult with complexity measures
    """
    pass


# Register methods
register_method("shannon_entropy", "information", shannon_entropy)
register_method("local_entropy", "information", local_entropy)
register_method("compression_ratio", "information", compression_ratio)
register_method("approximate_complexity", "information", approximate_complexity)
