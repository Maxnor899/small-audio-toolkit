"""
Information-theoretic analysis methods.
"""

from typing import Dict, Any
import numpy as np
import gzip
import io

from ..engine.context import AnalysisContext
from ..engine.results import AnalysisResult
from ..engine.registry import register_method
from ..utils.logging import get_logger

logger = get_logger(__name__)


def shannon_entropy(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Compute Shannon entropy (global).
    """
    num_bins = params.get('num_bins', 256)
    
    measurements = {}
    
    for channel_name, audio_data in context.audio_data.items():
        
        # Normalize to [0, 1]
        normalized = (audio_data - np.min(audio_data)) / (np.max(audio_data) - np.min(audio_data) + 1e-10)
        
        # Histogram
        hist, _ = np.histogram(normalized, bins=num_bins, density=True)
        
        # Remove zeros
        hist = hist[hist > 0]
        
        # Normalize histogram to probabilities
        hist = hist / np.sum(hist)
        
        # Shannon entropy
        entropy = -np.sum(hist * np.log2(hist))
        
        # Max entropy for this number of bins
        max_entropy = np.log2(num_bins)
        
        # Normalized entropy
        normalized_entropy = entropy / max_entropy
        
        measurements[channel_name] = {
            'shannon_entropy': float(entropy),
            'max_entropy': float(max_entropy),
            'normalized_entropy': float(normalized_entropy),
            'num_bins': num_bins
        }
    
    logger.info(f"Shannon entropy for {len(context.audio_data)} channels")
    
    return AnalysisResult(
        method='shannon_entropy',
        measurements=measurements,
        metrics={'num_bins': num_bins}
    )


def local_entropy(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Compute local entropy (windowed).
    """
    window_size = params.get('window_size', 2048)
    hop_length = params.get('hop_length', 512)
    num_bins = params.get('num_bins', 64)
    
    measurements = {}
    
    for channel_name, audio_data in context.audio_data.items():
        
        # Limit for performance
        max_samples = 200000
        if len(audio_data) > max_samples:
            audio_subset = audio_data[:max_samples]
            logger.warning(f"Local entropy: using first {max_samples} samples")
        else:
            audio_subset = audio_data
        
        entropies = []
        
        for i in range(0, len(audio_subset) - window_size, hop_length):
            window = audio_subset[i:i + window_size]
            
            # Normalize window
            normalized = (window - np.min(window)) / (np.max(window) - np.min(window) + 1e-10)
            
            # Histogram
            hist, _ = np.histogram(normalized, bins=num_bins, density=True)
            hist = hist[hist > 0]
            hist = hist / np.sum(hist)
            
            # Entropy
            entropy = -np.sum(hist * np.log2(hist))
            entropies.append(entropy)
        
        entropies = np.array(entropies)
        
        measurements[channel_name] = {
            'mean_entropy': float(np.mean(entropies)),
            'std_entropy': float(np.std(entropies)),
            'min_entropy': float(np.min(entropies)),
            'max_entropy': float(np.max(entropies)),
            'num_windows': len(entropies),
            'entropy_variation': float(np.std(entropies) / (np.mean(entropies) + 1e-10))
        }
    
    logger.info(f"Local entropy for {len(context.audio_data)} channels")
    
    return AnalysisResult(
        method='local_entropy',
        measurements=measurements,
        metrics={'window_size': window_size, 'hop_length': hop_length, 'num_bins': num_bins}
    )


def compression_ratio(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Estimate compression ratio (gzip).
    """
    measurements = {}
    
    for channel_name, audio_data in context.audio_data.items():
        
        # Limit for performance
        max_samples = 100000
        if len(audio_data) > max_samples:
            audio_subset = audio_data[:max_samples]
            logger.warning(f"Compression ratio: using first {max_samples} samples")
        else:
            audio_subset = audio_data
        
        # Convert to bytes (16-bit PCM)
        audio_int16 = (audio_subset * 32767).astype(np.int16)
        audio_bytes = audio_int16.tobytes()
        
        # Original size
        original_size = len(audio_bytes)
        
        # Compress
        compressed = gzip.compress(audio_bytes, compresslevel=9)
        compressed_size = len(compressed)
        
        # Ratio
        ratio = original_size / compressed_size
        
        measurements[channel_name] = {
            'original_size': original_size,
            'compressed_size': compressed_size,
            'compression_ratio': float(ratio),
            'samples_analyzed': len(audio_subset)
        }
    
    logger.info(f"Compression ratio for {len(context.audio_data)} channels")
    
    return AnalysisResult(
        method='compression_ratio',
        measurements=measurements
    )


def approximate_complexity(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Approximate complexity (sample entropy approximation).
    """
    m = params.get('m', 2)  # Pattern length
    r_factor = params.get('r_factor', 0.2)  # Tolerance factor
    
    measurements = {}
    
    for channel_name, audio_data in context.audio_data.items():
        
        # CRITICAL: O(n²) complexity - must use very small sample size
        # 5000 samples = 25M comparisons (~5 seconds)
        # 50000 samples = 2.5B comparisons (~8 minutes)
        max_samples = 5000
        if len(audio_data) > max_samples:
            audio_subset = audio_data[:max_samples]
            logger.warning(f"Approximate complexity: using first {max_samples} samples (O(n²) algorithm)")
        else:
            audio_subset = audio_data
        
        # Tolerance
        r = r_factor * np.std(audio_subset)
        
        N = len(audio_subset)
        
        def phi(m_param):
            patterns = []
            for i in range(N - m_param):
                patterns.append(audio_subset[i:i + m_param])
            
            C = 0
            for i in range(len(patterns)):
                matches = 0
                for j in range(len(patterns)):
                    if np.max(np.abs(patterns[i] - patterns[j])) <= r:
                        matches += 1
                C += matches - 1  # Exclude self-match
            
            return C / (N - m_param)
        
        phi_m = phi(m)
        phi_m1 = phi(m + 1)
        
        # Sample entropy approximation
        if phi_m1 > 0 and phi_m > 0:
            complexity = -np.log(phi_m1 / phi_m)
        else:
            complexity = 0.0
        
        measurements[channel_name] = {
            'approximate_complexity': float(complexity),
            'pattern_length': m,
            'tolerance': float(r),
            'samples_analyzed': len(audio_subset)
        }
    
    logger.info(f"Approximate complexity for {len(context.audio_data)} channels")
    
    return AnalysisResult(
        method='approximate_complexity',
        measurements=measurements,
        metrics={'m': m, 'r_factor': r_factor}
    )


# Register methods
register_method("shannon_entropy", "information", shannon_entropy, "Shannon entropy")
register_method("local_entropy", "information", local_entropy, "Local windowed entropy")
register_method("compression_ratio", "information", compression_ratio, "Compression ratio")
register_method("approximate_complexity", "information", approximate_complexity, "Approximate complexity")