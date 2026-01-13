"""
Time-frequency domain analysis methods.
"""

from typing import Dict, Any
import numpy as np
from scipy import signal

from ..engine.context import AnalysisContext
from ..engine.results import AnalysisResult
from ..engine.registry import register_method
from ..utils.windowing import get_window
from ..utils.logging import get_logger

logger = get_logger(__name__)


def stft_analysis(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Compute Short-Time Fourier Transform (spectrogram).
    
    Args:
        context: Analysis context
        params: window_size, hop_length, window_type
        
    Returns:
        AnalysisResult with STFT data and statistics
    """
    window_size = params.get('window_size', 2048)
    hop_length = params.get('hop_length', 512)
    window_type = params.get('window_type', 'hann')
    
    measurements = {}
    visualization_data = {}
    
    for channel_name, audio_data in context.audio_data.items():
        
        # Compute STFT
        window = get_window(window_type, window_size)
        
        frequencies, times, stft_matrix = signal.stft(
            audio_data,
            fs=context.sample_rate,
            window=window,
            nperseg=window_size,
            noverlap=window_size - hop_length
        )
        
        magnitude = np.abs(stft_matrix)
        
        # Compute statistics
        temporal_mean = np.mean(magnitude, axis=1)
        spectral_mean = np.mean(magnitude, axis=0)
        
        # Find dominant frequency over time
        dominant_freq_indices = np.argmax(magnitude, axis=0)
        dominant_frequencies = frequencies[dominant_freq_indices]
        
        # Spectral flux (measure of change)
        spectral_flux = np.sqrt(np.sum(np.diff(magnitude, axis=1) ** 2, axis=0))
        
        measurements[channel_name] = {
            'num_time_frames': len(times),
            'num_freq_bins': len(frequencies),
            'frequency_resolution': float(frequencies[1] - frequencies[0]),
            'time_resolution': float(times[1] - times[0]) if len(times) > 1 else 0.0,
            'mean_magnitude': float(np.mean(magnitude)),
            'max_magnitude': float(np.max(magnitude)),
            'dominant_freq_mean': float(np.mean(dominant_frequencies)),
            'dominant_freq_std': float(np.std(dominant_frequencies)),
            'spectral_flux_mean': float(np.mean(spectral_flux)),
            'spectral_flux_max': float(np.max(spectral_flux)),
            'temporal_stability': float(1.0 - np.std(spectral_mean) / (np.mean(spectral_mean) + 1e-10))
        }
        
        # Store for visualization (downsample if too large)
        max_time_frames = 500
        if stft_matrix.shape[1] > max_time_frames:
            downsample_factor = stft_matrix.shape[1] // max_time_frames
            stft_vis = stft_matrix[:, ::downsample_factor]
            times_vis = times[::downsample_factor]
        else:
            stft_vis = stft_matrix
            times_vis = times
        
        visualization_data[channel_name] = {
            'stft_matrix': stft_vis.tolist(),
            'frequencies': frequencies.tolist()[:100],
            'times': times_vis.tolist()
        }
    
    logger.info(f"Computed STFT for {len(context.audio_data)} channels")
    
    return AnalysisResult(
        method='stft',
        measurements=measurements,
        metrics={'window_size': window_size, 'hop_length': hop_length, 'window_type': window_type},
        visualization_data=visualization_data
    )


def cqt_analysis(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Compute Constant-Q Transform.
    
    Note: Requires librosa for full implementation.
    """
    measurements = {}
    
    for channel_name in context.audio_data.keys():
        measurements[channel_name] = {
            'note': 'CQT requires librosa - not implemented'
        }
    
    logger.warning("CQT not fully implemented (requires librosa)")
    
    return AnalysisResult(
        method='cqt',
        measurements=measurements,
        metrics={'implemented': False}
    )


def wavelet_analysis(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Wavelet transform analysis with visualization_data.
    """
    wavelet_type = params.get('wavelet', 'morlet')
    num_scales = params.get('num_scales', 64)
    
    measurements = {}
    visualization_data = {}
    
    for channel_name, audio_data in context.audio_data.items():
        
        # Limit for performance
        max_samples = 100000
        if len(audio_data) > max_samples:
            audio_subset = audio_data[:max_samples]
            logger.warning(f"Wavelet: using first {max_samples} samples")
        else:
            audio_subset = audio_data
        
        scales = np.geomspace(1, 128, num_scales)
        
        if wavelet_type == 'morlet':
            coefficients, frequencies = signal.cwt(
                audio_subset,
                signal.morlet2,
                scales,
                w=6.0
            )
        else:
            coefficients, frequencies = signal.cwt(
                audio_subset,
                signal.ricker,
                scales
            )
        
        magnitude = np.abs(coefficients)
        
        measurements[channel_name] = {
            'num_scales': num_scales,
            'samples_analyzed': len(audio_subset),
            'mean_magnitude': float(np.mean(magnitude)),
            'max_magnitude': float(np.max(magnitude)),
            'scale_of_max': int(np.unravel_index(np.argmax(magnitude), magnitude.shape)[0]),
            'energy_concentration': float(np.max(magnitude) / (np.mean(magnitude) + 1e-10))
        }
        
        # Add visualization data
        visualization_data[channel_name] = {
            'scalogram': magnitude,
            'scales': scales
        }
    
    logger.info(f"Computed wavelet for {len(context.audio_data)} channels")
    
    return AnalysisResult(
        method='wavelet',
        measurements=measurements,
        metrics={'wavelet': wavelet_type, 'num_scales': num_scales},
        visualization_data=visualization_data
    )


def band_stability(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Measure stability of frequency bands over time.
    """
    window_size = params.get('window_size', 2048)
    hop_length = params.get('hop_length', 512)
    
    bands = params.get('bands', [
        (0, 100),
        (100, 500),
        (500, 2000),
        (2000, 8000),
        (8000, 20000)
    ])
    
    measurements = {}
    
    for channel_name, audio_data in context.audio_data.items():
        
        window = get_window('hann', window_size)
        frequencies, times, stft_matrix = signal.stft(
            audio_data,
            fs=context.sample_rate,
            window=window,
            nperseg=window_size,
            noverlap=window_size - hop_length
        )
        
        magnitude = np.abs(stft_matrix)
        
        band_stability_data = {}
        
        for i, (low, high) in enumerate(bands):
            band_mask = (frequencies >= low) & (frequencies < high)
            
            if not np.any(band_mask):
                continue
            
            band_energy = np.sum(magnitude[band_mask, :], axis=0)
            
            stability = 1.0 - (np.std(band_energy) / (np.mean(band_energy) + 1e-10))
            
            band_stability_data[f'{low}-{high}Hz'] = {
                'mean_energy': float(np.mean(band_energy)),
                'stability_score': float(np.clip(stability, 0, 1)),
                'variation_coefficient': float(np.std(band_energy) / (np.mean(band_energy) + 1e-10))
            }
        
        measurements[channel_name] = band_stability_data
    
    logger.info(f"Computed band stability for {len(context.audio_data)} channels")
    
    return AnalysisResult(
        method='band_stability',
        measurements=measurements,
        metrics={'num_bands': len(bands), 'bands': bands}
    )


# Register methods
register_method("stft", "time_frequency", stft_analysis, "Short-Time Fourier Transform")
register_method("cqt", "time_frequency", cqt_analysis, "Constant-Q Transform")
register_method("wavelet", "time_frequency", wavelet_analysis, "Wavelet transform")
register_method("band_stability", "time_frequency", band_stability, "Frequency band stability")