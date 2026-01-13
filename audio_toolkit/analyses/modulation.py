"""
Modulation analysis methods (AM/FM/Phase).
"""

from typing import Dict, Any
import numpy as np
from scipy import signal

from ..engine.context import AnalysisContext
from ..engine.results import AnalysisResult
from ..engine.registry import register_method
from ..utils.logging import get_logger

logger = get_logger(__name__)


def am_detection(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Detect Amplitude Modulation.
    
    Args:
        context: Analysis context
        params: analysis parameters
        
    Returns:
        AnalysisResult with AM detection data and visualization_data
    """
    measurements = {}
    visualization_data = {}
    
    for channel_name, audio_data in context.audio_data.items():
        
        # Compute envelope using Hilbert transform
        analytic_signal = signal.hilbert(audio_data)
        envelope = np.abs(analytic_signal)
        
        # Analyze envelope spectrum (modulation spectrum)
        envelope_fft = np.fft.rfft(envelope)
        envelope_magnitude = np.abs(envelope_fft)
        envelope_freqs = np.fft.rfftfreq(len(envelope), 1 / context.sample_rate)
        
        # Find peaks in modulation spectrum (exclude DC)
        peaks, properties = signal.find_peaks(
            envelope_magnitude[1:],
            prominence=np.max(envelope_magnitude) * 0.1
        )
        peaks = peaks + 1  # Adjust for skipped DC
        
        modulation_frequencies = envelope_freqs[peaks].tolist()[:10]
        modulation_magnitudes = envelope_magnitude[peaks].tolist()[:10]
        
        # Modulation depth (normalized variation)
        modulation_depth = (np.max(envelope) - np.min(envelope)) / (np.mean(envelope) + 1e-10)
        
        # Modulation index (ratio of AC to DC)
        ac_component = np.std(envelope)
        dc_component = np.mean(envelope)
        modulation_index = ac_component / (dc_component + 1e-10)
        
        measurements[channel_name] = {
            'modulation_detected': len(peaks) > 0,
            'num_modulation_frequencies': len(peaks),
            'modulation_frequencies': modulation_frequencies,
            'modulation_magnitudes': modulation_magnitudes,
            'dominant_modulation_freq': float(envelope_freqs[peaks[0]]) if len(peaks) > 0 else 0.0,
            'modulation_depth': float(modulation_depth),
            'modulation_index': float(modulation_index),
            'envelope_mean': float(np.mean(envelope)),
            'envelope_std': float(np.std(envelope))
        }
        
        # Add visualization data
        time = np.arange(len(envelope)) / context.sample_rate
        visualization_data[channel_name] = {
            'time': time,
            'envelope': envelope,
            'modulation_frequencies': envelope_freqs,
            'modulation_spectrum': envelope_magnitude
        }
    
    logger.info(f"AM detection for {len(context.audio_data)} channels")
    
    return AnalysisResult(
        method='am_detection',
        measurements=measurements,
        visualization_data=visualization_data
    )


def fm_detection(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Detect Frequency Modulation.
    
    Args:
        context: Analysis context
        params: analysis parameters
        
    Returns:
        AnalysisResult with FM detection data and visualization_data
    """
    measurements = {}
    visualization_data = {}
    
    for channel_name, audio_data in context.audio_data.items():
        
        # Compute analytic signal
        analytic_signal = signal.hilbert(audio_data)
        
        # Instantaneous phase
        instantaneous_phase = np.unwrap(np.angle(analytic_signal))
        
        # Instantaneous frequency (derivative of phase)
        instantaneous_frequency = np.diff(instantaneous_phase) / (2.0 * np.pi) * context.sample_rate
        
        # FM metrics
        freq_mean = np.mean(instantaneous_frequency)
        freq_std = np.std(instantaneous_frequency)
        freq_range = np.max(instantaneous_frequency) - np.min(instantaneous_frequency)
        
        # Frequency deviation (measure of FM)
        frequency_deviation = freq_std
        
        # Analyze frequency modulation spectrum
        fm_fft = np.fft.rfft(instantaneous_frequency)
        fm_magnitude = np.abs(fm_fft)
        fm_freqs = np.fft.rfftfreq(len(instantaneous_frequency), 1 / context.sample_rate)
        
        # Find peaks in FM spectrum
        peaks, _ = signal.find_peaks(
            fm_magnitude[1:],
            prominence=np.max(fm_magnitude) * 0.1
        )
        peaks = peaks + 1
        
        fm_mod_frequencies = fm_freqs[peaks].tolist()[:10]
        
        measurements[channel_name] = {
            'fm_detected': freq_std > freq_mean * 0.01,  # Heuristic threshold
            'carrier_frequency_mean': float(freq_mean),
            'frequency_deviation': float(frequency_deviation),
            'frequency_range': float(freq_range),
            'frequency_std': float(freq_std),
            'num_fm_components': len(peaks),
            'fm_modulation_frequencies': fm_mod_frequencies,
            'modulation_index_fm': float(frequency_deviation / (freq_mean + 1e-10))
        }
        
        # Add visualization data
        time = np.arange(len(instantaneous_frequency)) / context.sample_rate
        visualization_data[channel_name] = {
            'time': time,
            'instantaneous_frequency': instantaneous_frequency,
            'carrier_frequency': freq_mean
        }
    
    logger.info(f"FM detection for {len(context.audio_data)} channels")
    
    return AnalysisResult(
        method='fm_detection',
        measurements=measurements,
        visualization_data=visualization_data
    )


def phase_analysis(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Analyze instantaneous phase.
    
    Args:
        context: Analysis context
        params: analysis parameters
        
    Returns:
        AnalysisResult with phase data and visualization_data
    """
    measurements = {}
    visualization_data = {}
    
    for channel_name, audio_data in context.audio_data.items():
        
        # Compute analytic signal
        analytic_signal = signal.hilbert(audio_data)
        
        # Instantaneous phase
        instantaneous_phase = np.angle(analytic_signal)
        unwrapped_phase = np.unwrap(instantaneous_phase)
        
        # Phase statistics
        phase_mean = np.mean(instantaneous_phase)
        phase_std = np.std(instantaneous_phase)
        
        # Phase coherence (consistency of phase)
        phase_diff = np.diff(unwrapped_phase)
        phase_coherence = 1.0 - (np.std(phase_diff) / (np.mean(np.abs(phase_diff)) + 1e-10))
        
        # Detect phase jumps
        phase_jump_threshold = np.pi / 2
        phase_jump_indices = np.where(np.abs(np.diff(instantaneous_phase)) > phase_jump_threshold)[0]
        phase_jumps = len(phase_jump_indices)
        
        measurements[channel_name] = {
            'phase_mean': float(phase_mean),
            'phase_std': float(phase_std),
            'phase_range': float(np.max(instantaneous_phase) - np.min(instantaneous_phase)),
            'unwrapped_phase_total': float(unwrapped_phase[-1] - unwrapped_phase[0]),
            'phase_coherence': float(np.clip(phase_coherence, 0, 1)),
            'num_phase_jumps': int(phase_jumps),
            'phase_jump_rate': float(phase_jumps / len(audio_data) * context.sample_rate)
        }
        
        # Add visualization data
        time = np.arange(len(unwrapped_phase)) / context.sample_rate
        visualization_data[channel_name] = {
            'time': time,
            'phase': unwrapped_phase,
            'jumps': phase_jump_indices
        }
    
    logger.info(f"Phase analysis for {len(context.audio_data)} channels")
    
    return AnalysisResult(
        method='phase_analysis',
        measurements=measurements,
        visualization_data=visualization_data
    )


def modulation_index(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Compute overall modulation index.
    
    Args:
        context: Analysis context
        params: analysis parameters
        
    Returns:
        AnalysisResult with modulation index
    """
    measurements = {}
    
    for channel_name, audio_data in context.audio_data.items():
        
        # Compute envelope
        analytic_signal = signal.hilbert(audio_data)
        envelope = np.abs(analytic_signal)
        
        # Overall modulation index
        ac = np.std(envelope)
        dc = np.mean(envelope)
        mod_index = ac / (dc + 1e-10)
        
        # Modulation depth
        mod_depth = (np.max(envelope) - np.min(envelope)) / (np.mean(envelope) + 1e-10)
        
        measurements[channel_name] = {
            'modulation_index': float(mod_index),
            'modulation_depth': float(mod_depth),
            'ac_component': float(ac),
            'dc_component': float(dc),
            'peak_to_average_ratio': float(np.max(envelope) / (np.mean(envelope) + 1e-10))
        }
    
    logger.info(f"Modulation index for {len(context.audio_data)} channels")
    
    return AnalysisResult(
        method='modulation_index',
        measurements=measurements
    )


# Register methods
register_method("am_detection", "modulation", am_detection, "AM detection")
register_method("fm_detection", "modulation", fm_detection, "FM detection")
register_method("phase_analysis", "modulation", phase_analysis, "Phase analysis")
register_method("modulation_index", "modulation", modulation_index, "Modulation index")