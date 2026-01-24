"""
Temporal domain analysis methods.
"""

from typing import Dict, Any
import numpy as np
from scipy import signal

from ..engine.context import AnalysisContext
from ..engine.results import AnalysisResult
from ..engine.registry import register_method
from ..utils.logging import get_logger

logger = get_logger(__name__)


def envelope_analysis(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Compute amplitude envelope using Hilbert transform or RMS.
    
    Args:
        context: Analysis context
        params: method ('hilbert' or 'rms'), window_size (for rms)
        
    Returns:
        AnalysisResult with envelope data and visualization_data
    """
    method = params.get('method', 'hilbert')
    
    measurements = {}
    metrics = {}
    visualization_data = {}
    
    for channel_name, audio_data in context.audio_data.items():
        
        if method == 'hilbert':
            analytic_signal = signal.hilbert(audio_data)
            envelope = np.abs(analytic_signal)
        
        elif method == 'rms':
            window_size = params.get('window_size', 1024)
            hop_length = window_size // 2
            
            envelope = []
            for i in range(0, len(audio_data) - window_size, hop_length):
                window = audio_data[i:i + window_size]
                rms_value = np.sqrt(np.mean(window ** 2))
                envelope.append(rms_value)
            
            envelope = np.array(envelope)
        
        else:
            raise ValueError(f"Unknown envelope method: {method}")
        
        measurements[channel_name] = {
            'envelope_mean': float(np.mean(envelope)),
            'envelope_max': float(np.max(envelope)),
            'envelope_std': float(np.std(envelope)),
            'envelope_length': len(envelope)
        }
        
        # Add visualization data
        visualization_data[channel_name] = envelope
    
    metrics['method'] = method
    
    logger.info(f"Computed {method} envelope for {len(context.audio_data)} channels")
    
    return AnalysisResult(
        method='envelope',
        measurements=measurements,
        metrics=metrics,
        visualization_data=visualization_data
    )


def autocorrelation_analysis(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Compute temporal autocorrelation.
    
    Args:
        context: Analysis context
        params: max_lag, normalize, max_samples
        
    Returns:
        AnalysisResult with autocorrelation data and visualization_data
    """
    max_lag = params.get('max_lag', 1000)
    normalize = params.get('normalize', True)
    max_samples = params.get('max_samples', 50000)  # CRITICAL: limit samples for performance
    
    measurements = {}
    visualization_data = {}
    
    for channel_name, audio_data in context.audio_data.items():
        
        # CRITICAL OPTIMIZATION: limit samples to avoid 4+ hour computation
        if len(audio_data) > max_samples:
            audio_subset = audio_data[:max_samples]
            logger.warning(f"Autocorrelation: using first {max_samples} samples (out of {len(audio_data)}) for {channel_name}")
        else:
            audio_subset = audio_data
        
        autocorr = np.correlate(audio_subset, audio_subset, mode='full')
        autocorr = autocorr[len(autocorr) // 2:]
        
        autocorr = autocorr[:max_lag]
        
        if normalize:
            autocorr = autocorr / autocorr[0]
        
        peaks, properties = signal.find_peaks(autocorr, height=0.1)
        
        measurements[channel_name] = {
            'autocorr_max': float(np.max(autocorr[1:])),
            'autocorr_mean': float(np.mean(autocorr)),
            'first_peak_lag': int(peaks[0]) if len(peaks) > 0 else None,
            'num_peaks': len(peaks),
            'periodicity_score': float(np.max(autocorr[1:])) if len(autocorr) > 1 else 0.0
        }
        
        # Add visualization data
        visualization_data[channel_name] = autocorr
    
    logger.info(f"Computed autocorrelation (max_lag={max_lag}) for {len(context.audio_data)} channels")
    
    return AnalysisResult(
        method='autocorrelation',
        measurements=measurements,
        metrics={'max_lag': max_lag, 'normalized': normalize, 'max_samples': max_samples},
        visualization_data=visualization_data
    )


def pulse_detection(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Detect discrete pulses or impulses.
    
    Args:
        context: Analysis context
        params: threshold, min_distance
        
    Returns:
        AnalysisResult with detected pulse positions and visualization_data
    """
    threshold = params.get('threshold', 0.5)
    min_distance = params.get('min_distance', 100)
    
    measurements = {}
    visualization_data = {}
    
    for channel_name, audio_data in context.audio_data.items():
        
        envelope = np.abs(signal.hilbert(audio_data))
        
        peaks, properties = signal.find_peaks(
            envelope,
            height=threshold * np.max(envelope),
            distance=min_distance
        )
        
        if len(peaks) > 1:
            intervals = np.diff(peaks)
            interval_std = float(np.std(intervals))
            interval_mean = float(np.mean(intervals))
        else:
            interval_std = 0.0
            interval_mean = 0.0
        
        measurements[channel_name] = {
            'num_pulses': len(peaks),
            'pulse_positions': peaks.tolist()[:100],
            'interval_mean': interval_mean,
            'interval_std': interval_std,
            'regularity_score': 1.0 - min(interval_std / (interval_mean + 1e-10), 1.0)
        }
        
        # AJOUT: visualization_data pour afficher waveform + pulse markers
        # Limiter à 100k samples pour la visualisation
        max_viz_samples = min(len(audio_data), 100000)
        visualization_data[channel_name] = {
            'waveform': audio_data[:max_viz_samples],
            'envelope': envelope[:max_viz_samples],
            'pulse_positions': peaks[peaks < max_viz_samples],  # Garder seulement les pulses visibles
            'threshold_level': threshold * np.max(envelope)
        }
    
    logger.info(f"Detected pulses for {len(context.audio_data)} channels")
    
    return AnalysisResult(
        method='pulse_detection',
        measurements=measurements,
        metrics={'threshold': threshold, 'min_distance': min_distance},
        visualization_data=visualization_data
    )


def duration_ratios(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Compute ratios between event intervals.
    
    Args:
        context: Analysis context
        params: event detection parameters
        
    Returns:
        AnalysisResult with interval ratios
    """
    threshold = params.get('threshold', 0.3)
    min_distance = params.get('min_distance', 100)
    
    measurements = {}
    visualization_data = {}
    
    for channel_name, audio_data in context.audio_data.items():
        
        envelope = np.abs(signal.hilbert(audio_data))
        
        peaks, _ = signal.find_peaks(
            envelope,
            height=threshold * np.max(envelope),
            distance=min_distance
        )
        
        if len(peaks) < 2:
            measurements[channel_name] = {
                'num_events': len(peaks),
                'ratios': [],
                'ratio_mean': 0.0,
                'ratio_std': 0.0
            }
            visualization_data[channel_name] = {
                'ratios': []
            }
            continue
        
        intervals = np.diff(peaks)
        
        ratios = []
        for i in range(len(intervals) - 1):
            if intervals[i + 1] > 0:
                ratio = intervals[i] / intervals[i + 1]
                ratios.append(float(ratio))
        
        measurements[channel_name] = {
            'num_events': len(peaks),
            'num_intervals': len(intervals),
            'ratios': ratios[:50],
            'ratio_mean': float(np.mean(ratios)) if ratios else 0.0,
            'ratio_std': float(np.std(ratios)) if ratios else 0.0
        }
        visualization_data[channel_name] = {
            'ratios': ratios
        }
    
    logger.info(f"Computed duration ratios for {len(context.audio_data)} channels")
    
    return AnalysisResult(
        method='duration_ratios',
        measurements=measurements,
        metrics={'threshold': threshold},
        visualization_data=visualization_data
    )


# Register methods
register_method("envelope", "temporal", envelope_analysis, "Amplitude envelope analysis")
register_method("autocorrelation", "temporal", autocorrelation_analysis, "Temporal autocorrelation")
register_method("pulse_detection", "temporal", pulse_detection, "Pulse/impulse detection")
register_method("duration_ratios", "temporal", duration_ratios, "Event interval ratios")
