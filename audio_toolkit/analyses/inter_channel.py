"""
Inter-channel analysis methods.
"""

from typing import Dict, Any
import numpy as np
from scipy import signal

from ..engine.context import AnalysisContext
from ..engine.results import AnalysisResult
from ..engine.registry import register_method
from ..utils.logging import get_logger

logger = get_logger(__name__)


def cross_correlation(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Cross-correlation between channels.
    
    Args:
        context: Analysis context
        params: max_lag, max_samples
        
    Returns:
        AnalysisResult with cross-correlation data and visualization_data
    """
    max_lag = params.get('max_lag', 1000)
    max_samples = params.get('max_samples', 50000)  # CRITICAL: limit samples for performance
    
    measurements = {}
    visualization_data = {}
    
    # Need at least 2 channels
    channels = list(context.audio_data.keys())
    if len(channels) < 2:
        logger.warning("Cross-correlation needs at least 2 channels")
        return AnalysisResult(
            method='cross_correlation',
            measurements={'error': 'Need at least 2 channels'},
            metrics={'max_lag': max_lag}
        )
    
    # Compare all pairs
    for i in range(len(channels)):
        for j in range(i + 1, len(channels)):
            channel_a = channels[i]
            channel_b = channels[j]
            
            audio_a = context.audio_data[channel_a]
            audio_b = context.audio_data[channel_b]
            
            # CRITICAL OPTIMIZATION: limit samples to avoid long computation
            if len(audio_a) > max_samples:
                audio_a = audio_a[:max_samples]
                logger.warning(f"Cross-correlation: using first {max_samples} samples for {channel_a}")
            if len(audio_b) > max_samples:
                audio_b = audio_b[:max_samples]
            
            # Compute cross-correlation
            correlation = np.correlate(audio_a, audio_b, mode='full')
            correlation = correlation[len(correlation) // 2:]
            correlation = correlation[:max_lag]
            
            # Normalize
            correlation = correlation / correlation[0] if correlation[0] != 0 else correlation
            
            # Find peak
            peak_idx = np.argmax(np.abs(correlation))
            peak_value = correlation[peak_idx]
            
            pair_key = f'{channel_a}_vs_{channel_b}'
            measurements[pair_key] = {
                'max_correlation': float(np.max(np.abs(correlation))),
                'peak_lag': int(peak_idx),
                'peak_value': float(peak_value),
                'mean_correlation': float(np.mean(correlation)),
                'correlation_at_zero': float(correlation[0])
            }
            
            # Add visualization data
            lags = np.arange(len(correlation))
            visualization_data[pair_key] = {
                'lags': lags,
                'correlation': correlation
            }
    
    logger.info(f"Cross-correlation for {len(measurements)} channel pairs")
    
    return AnalysisResult(
        method='cross_correlation',
        measurements=measurements,
        metrics={'max_lag': max_lag, 'max_samples': max_samples},
        visualization_data=visualization_data
    )


def lr_difference(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Analyze L-R difference signal.
    
    Args:
        context: Analysis context
        params: analysis parameters
        
    Returns:
        AnalysisResult with L-R analysis and visualization_data
    """
    measurements = {}
    visualization_data = {}
    
    # Check if we have left and right
    if 'left' not in context.audio_data or 'right' not in context.audio_data:
        logger.warning("L-R analysis needs left and right channels")
        return AnalysisResult(
            method='lr_difference',
            measurements={'error': 'Need left and right channels'}
        )
    
    left = context.audio_data['left']
    right = context.audio_data['right']
    difference = left - right
    
    # Energy comparison
    left_energy = np.sum(left ** 2)
    right_energy = np.sum(right ** 2)
    diff_energy = np.sum(difference ** 2)
    
    # Spectrum of difference
    diff_spectrum = np.fft.rfft(difference)
    diff_magnitude = np.abs(diff_spectrum)
    freqs = np.fft.rfftfreq(len(difference), 1 / context.sample_rate)
    
    peak_idx = np.argmax(diff_magnitude)
    
    measurements['lr_difference'] = {
        'left_energy': float(left_energy),
        'right_energy': float(right_energy),
        'difference_energy': float(diff_energy),
        'energy_ratio': float(diff_energy / (left_energy + right_energy + 1e-10)),
        'difference_rms': float(np.sqrt(np.mean(difference ** 2))),
        'difference_peak_freq': float(freqs[peak_idx]),
        'difference_peak_magnitude': float(diff_magnitude[peak_idx]),
        'contains_unique_info': diff_energy > (left_energy + right_energy) * 0.01
    }
    
    # Add visualization data
    visualization_data['lr_difference'] = {
        'waveform': difference,
        'frequencies': freqs,
        'spectrum': diff_magnitude
    }
    
    logger.info("L-R difference analysis complete")
    
    return AnalysisResult(
        method='lr_difference',
        measurements=measurements,
        visualization_data=visualization_data
    )


def phase_difference(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Phase difference between channels.
    
    Args:
        context: Analysis context
        params: frequency bands
        
    Returns:
        AnalysisResult with phase difference data
    """
    measurements = {}
    
    channels = list(context.audio_data.keys())
    if len(channels) < 2:
        logger.warning("Phase difference needs at least 2 channels")
        return AnalysisResult(
            method='phase_difference',
            measurements={'error': 'Need at least 2 channels'}
        )
    
    # Analyze pairs
    for i in range(len(channels)):
        for j in range(i + 1, len(channels)):
            channel_a = channels[i]
            channel_b = channels[j]
            
            audio_a = context.audio_data[channel_a]
            audio_b = context.audio_data[channel_b]
            
            # Compute analytic signals
            analytic_a = signal.hilbert(audio_a)
            analytic_b = signal.hilbert(audio_b)
            
            # Instantaneous phase
            phase_a = np.angle(analytic_a)
            phase_b = np.angle(analytic_b)
            
            # Phase difference
            phase_diff = phase_a - phase_b
            
            # Wrap to [-pi, pi]
            phase_diff = np.arctan2(np.sin(phase_diff), np.cos(phase_diff))
            
            # Statistics
            phase_diff_mean = np.mean(phase_diff)
            phase_diff_std = np.std(phase_diff)
            
            # Phase coherence
            phase_coherence = np.abs(np.mean(np.exp(1j * phase_diff)))
            
            pair_key = f'{channel_a}_vs_{channel_b}'
            measurements[pair_key] = {
                'phase_diff_mean': float(phase_diff_mean),
                'phase_diff_std': float(phase_diff_std),
                'phase_diff_range': float(np.max(phase_diff) - np.min(phase_diff)),
                'phase_coherence': float(phase_coherence),
                'in_phase': abs(phase_diff_mean) < np.pi / 4,
                'out_of_phase': abs(abs(phase_diff_mean) - np.pi) < np.pi / 4
            }
    
    logger.info(f"Phase difference for {len(measurements)} channel pairs")
    
    return AnalysisResult(
        method='phase_difference',
        measurements=measurements
    )


def time_delay(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Inter-channel time delay (ITD).
    
    Args:
        context: Analysis context
        params: max_delay_samples, max_samples
        
    Returns:
        AnalysisResult with time delay data
    """
    max_delay = params.get('max_delay_samples', 100)
    max_samples = params.get('max_samples', 50000)  # CRITICAL: limit samples for performance
    
    measurements = {}
    
    channels = list(context.audio_data.keys())
    if len(channels) < 2:
        logger.warning("Time delay needs at least 2 channels")
        return AnalysisResult(
            method='time_delay',
            measurements={'error': 'Need at least 2 channels'},
            metrics={'max_delay': max_delay}
        )
    
    # Analyze pairs
    for i in range(len(channels)):
        for j in range(i + 1, len(channels)):
            channel_a = channels[i]
            channel_b = channels[j]
            
            audio_a = context.audio_data[channel_a]
            audio_b = context.audio_data[channel_b]
            
            # CRITICAL OPTIMIZATION: limit samples
            if len(audio_a) > max_samples:
                audio_a = audio_a[:max_samples]
                logger.warning(f"Time delay: using first {max_samples} samples")
            if len(audio_b) > max_samples:
                audio_b = audio_b[:max_samples]
            
            # Cross-correlation to find delay
            correlation = np.correlate(audio_a, audio_b, mode='full')
            
            # Find peak near center
            center = len(correlation) // 2
            search_range = slice(center - max_delay, center + max_delay)
            local_corr = correlation[search_range]
            
            peak_idx = np.argmax(np.abs(local_corr))
            delay_samples = peak_idx - max_delay
            delay_ms = delay_samples / context.sample_rate * 1000
            
            pair_key = f'{channel_a}_vs_{channel_b}'
            measurements[pair_key] = {
                'delay_samples': int(delay_samples),
                'delay_ms': float(delay_ms),
                'correlation_at_delay': float(local_corr[peak_idx]),
                'is_synchronized': abs(delay_samples) < 5
            }
    
    logger.info(f"Time delay for {len(measurements)} channel pairs")
    
    return AnalysisResult(
        method='time_delay',
        measurements=measurements,
        metrics={'max_delay': max_delay, 'max_samples': max_samples}
    )


# Register methods
register_method("cross_correlation", "inter_channel", cross_correlation, "Cross-correlation")
register_method("lr_difference", "inter_channel", lr_difference, "L-R difference")
register_method("phase_difference", "inter_channel", phase_difference, "Phase difference")
register_method("time_delay", "inter_channel", time_delay, "Time delay (ITD)")