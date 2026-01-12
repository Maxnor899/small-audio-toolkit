"""
Frequency domain analysis methods.
"""

from typing import Dict, Any
import numpy as np
from scipy import signal, fft

from ..engine.context import AnalysisContext
from ..engine.results import AnalysisResult
from ..engine.registry import register_method
from ..utils.windowing import get_window
from ..utils.logging import get_logger

logger = get_logger(__name__)


def fft_global(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Compute global FFT spectrum.
    
    Args:
        context: Analysis context
        params: window type
        
    Returns:
        AnalysisResult with frequency spectrum
    """
    window_type = params.get('window', 'hann')
    
    measurements = {}
    
    for channel_name, audio_data in context.audio_data.items():
        
        n_fft = len(audio_data)
        window = get_window(window_type, n_fft)
        
        windowed = audio_data * window
        
        spectrum = np.fft.rfft(windowed)
        magnitude = np.abs(spectrum)
        freqs = np.fft.rfftfreq(n_fft, 1 / context.sample_rate)
        
        measurements[channel_name] = {
            'n_fft': n_fft,
            'frequency_resolution': float(freqs[1] - freqs[0]),
            'peak_frequency': float(freqs[np.argmax(magnitude)]),
            'peak_magnitude': float(np.max(magnitude)),
            'spectral_energy': float(np.sum(magnitude ** 2))
        }
    
    logger.info(f"Computed global FFT for {len(context.audio_data)} channels")
    
    return AnalysisResult(
        method='fft_global',
        measurements=measurements,
        metrics={'window': window_type, 'sample_rate': context.sample_rate}
    )


def peak_detection(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Detect spectral peaks.
    
    Args:
        context: Analysis context
        params: prominence, distance, height
        
    Returns:
        AnalysisResult with peak frequencies and amplitudes
    """
    prominence = params.get('prominence', 10.0)
    distance = params.get('distance', 100)
    height = params.get('height', None)
    
    measurements = {}
    
    for channel_name, audio_data in context.audio_data.items():
        
        n_fft = len(audio_data)
        spectrum = np.fft.rfft(audio_data)
        magnitude = np.abs(spectrum)
        freqs = np.fft.rfftfreq(n_fft, 1 / context.sample_rate)
        
        peaks, properties = signal.find_peaks(
            magnitude,
            prominence=prominence,
            distance=distance,
            height=height
        )
        
        peak_freqs = freqs[peaks].tolist()[:20]
        peak_mags = magnitude[peaks].tolist()[:20]
        
        measurements[channel_name] = {
            'num_peaks': len(peaks),
            'peak_frequencies': peak_freqs,
            'peak_magnitudes': peak_mags,
            'dominant_frequency': float(freqs[peaks[0]]) if len(peaks) > 0 else 0.0,
            'frequency_spread': float(np.std(freqs[peaks])) if len(peaks) > 0 else 0.0
        }
    
    logger.info(f"Detected spectral peaks for {len(context.audio_data)} channels")
    
    return AnalysisResult(
        method='peak_detection',
        measurements=measurements,
        metrics={'prominence': prominence, 'distance': distance}
    )


def harmonic_analysis(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Analyze harmonic relationships.
    
    Args:
        context: Analysis context
        params: fundamental_range, max_harmonics
        
    Returns:
        AnalysisResult with harmonic structure
    """
    fundamental_range = params.get('fundamental_range', [80.0, 400.0])
    max_harmonics = params.get('max_harmonics', 10)
    
    measurements = {}
    
    for channel_name, audio_data in context.audio_data.items():
        
        n_fft = len(audio_data)
        spectrum = np.fft.rfft(audio_data)
        magnitude = np.abs(spectrum)
        freqs = np.fft.rfftfreq(n_fft, 1 / context.sample_rate)
        
        mask = (freqs >= fundamental_range[0]) & (freqs <= fundamental_range[1])
        fundamental_idx = np.argmax(magnitude[mask])
        fundamental_freq = freqs[mask][fundamental_idx]
        
        harmonics_found = []
        harmonic_ratios = []
        
        for n in range(1, max_harmonics + 1):
            target_freq = fundamental_freq * n
            tolerance = fundamental_freq * 0.05
            
            harmonic_mask = (freqs >= target_freq - tolerance) & (freqs <= target_freq + tolerance)
            
            if np.any(harmonic_mask):
                harmonic_magnitude = np.max(magnitude[harmonic_mask])
                harmonics_found.append(n)
                
                if len(harmonics_found) == 1:
                    harmonic_ratios.append(1.0)
                else:
                    harmonic_ratios.append(float(harmonic_magnitude / magnitude[mask][fundamental_idx]))
        
        measurements[channel_name] = {
            'fundamental_frequency': float(fundamental_freq),
            'harmonics_detected': len(harmonics_found),
            'harmonic_numbers': harmonics_found,
            'harmonic_ratios': harmonic_ratios,
            'harmonicity_score': len(harmonics_found) / max_harmonics
        }
    
    logger.info(f"Analyzed harmonics for {len(context.audio_data)} channels")
    
    return AnalysisResult(
        method='harmonic_analysis',
        measurements=measurements,
        metrics={'fundamental_range': fundamental_range, 'max_harmonics': max_harmonics}
    )


def spectral_centroid(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Compute spectral centroid.
    
    Args:
        context: Analysis context
        params: analysis parameters
        
    Returns:
        AnalysisResult with centroid values
    """
    measurements = {}
    
    for channel_name, audio_data in context.audio_data.items():
        
        n_fft = len(audio_data)
        spectrum = np.fft.rfft(audio_data)
        magnitude = np.abs(spectrum)
        freqs = np.fft.rfftfreq(n_fft, 1 / context.sample_rate)
        
        centroid = np.sum(freqs * magnitude) / (np.sum(magnitude) + 1e-10)
        
        measurements[channel_name] = {
            'spectral_centroid': float(centroid),
            'normalized_centroid': float(centroid / (context.sample_rate / 2))
        }
    
    logger.info(f"Computed spectral centroid for {len(context.audio_data)} channels")
    
    return AnalysisResult(
        method='spectral_centroid',
        measurements=measurements
    )


def spectral_flatness(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Compute spectral flatness.
    
    Args:
        context: Analysis context
        params: analysis parameters
        
    Returns:
        AnalysisResult with flatness values
    """
    measurements = {}
    
    for channel_name, audio_data in context.audio_data.items():
        
        n_fft = len(audio_data)
        spectrum = np.fft.rfft(audio_data)
        magnitude = np.abs(spectrum) + 1e-10
        
        geometric_mean = np.exp(np.mean(np.log(magnitude)))
        arithmetic_mean = np.mean(magnitude)
        
        flatness = geometric_mean / arithmetic_mean
        
        measurements[channel_name] = {
            'spectral_flatness': float(flatness),
            'tonality': float(1.0 - flatness)
        }
    
    logger.info(f"Computed spectral flatness for {len(context.audio_data)} channels")
    
    return AnalysisResult(
        method='spectral_flatness',
        measurements=measurements
    )


# Register methods
register_method("fft_global", "spectral", fft_global, "Global FFT spectrum")
register_method("peak_detection", "spectral", peak_detection, "Spectral peak detection")
register_method("harmonic_analysis", "spectral", harmonic_analysis, "Harmonic structure analysis")
register_method("spectral_centroid", "spectral", spectral_centroid, "Spectral centroid")
register_method("spectral_flatness", "spectral", spectral_flatness, "Spectral flatness")