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
        AnalysisResult with frequency spectrum and visualization_data
    """
    window_type = params.get('window', 'hann')
    
    measurements = {}
    visualization_data = {}
    
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
        
        # Add visualization data
        visualization_data[channel_name] = {
            'frequencies': freqs,
            'magnitudes': magnitude
        }
    
    logger.info(f"Computed global FFT for {len(context.audio_data)} channels")
    
    return AnalysisResult(
        method='fft_global',
        measurements=measurements,
        metrics={'window': window_type, 'sample_rate': context.sample_rate},
        visualization_data=visualization_data
    )


def peak_detection(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Detect spectral peaks.
    
    Args:
        context: Analysis context
        params: prominence, distance, height
        
    Returns:
        AnalysisResult with peak frequencies and amplitudes and visualization_data
    """
    prominence = params.get('prominence', 10.0)
    distance = params.get('distance', 100)
    height = params.get('height', None)
    
    measurements = {}
    visualization_data = {}
    
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
        
        # Add visualization data
        visualization_data[channel_name] = {
            'spectrum': magnitude,
            'peaks': peaks
        }
    
    logger.info(f"Detected spectral peaks for {len(context.audio_data)} channels")
    
    return AnalysisResult(
        method='peak_detection',
        measurements=measurements,
        metrics={'prominence': prominence, 'distance': distance},
        visualization_data=visualization_data
    )


def harmonic_analysis(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Analyze harmonic relationships.
    
    Args:
        context: Analysis context
        params: fundamental_range, max_harmonics
        
    Returns:
        AnalysisResult with harmonic structure and visualization_data
    """
    fundamental_range = params.get('fundamental_range', [80.0, 400.0])
    max_harmonics = params.get('max_harmonics', 10)
    
    measurements = {}
    visualization_data = {}
    
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
        harmonic_frequencies = []
        
        for n in range(1, max_harmonics + 1):
            target_freq = fundamental_freq * n
            tolerance = fundamental_freq * 0.05
            
            harmonic_mask = (freqs >= target_freq - tolerance) & (freqs <= target_freq + tolerance)
            
            if np.any(harmonic_mask):
                harmonic_magnitude = np.max(magnitude[harmonic_mask])
                harmonics_found.append(n)
                harmonic_frequencies.append(target_freq)
                
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
        
        # Add visualization data
        visualization_data[channel_name] = {
            'frequencies': freqs,
            'spectrum': magnitude,
            'fundamental': fundamental_freq,
            'harmonics': harmonic_frequencies
        }
    
    logger.info(f"Analyzed harmonics for {len(context.audio_data)} channels")
    
    return AnalysisResult(
        method='harmonic_analysis',
        measurements=measurements,
        metrics={'fundamental_range': fundamental_range, 'max_harmonics': max_harmonics},
        visualization_data=visualization_data
    )


def spectral_centroid(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Compute spectral centroid.
    
    Args:
        context: Analysis context
        params: analysis parameters
        
    Returns:
        AnalysisResult with centroid values and visualization_data
    """
    measurements = {}
    visualization_data = {}
    
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
        
        # AJOUT: visualization_data pour afficher spectrum + centroid line
        visualization_data[channel_name] = {
            'frequencies': freqs,
            'spectrum': magnitude,
            'centroid': centroid
        }
    
    logger.info(f"Computed spectral centroid for {len(context.audio_data)} channels")
    
    return AnalysisResult(
        method='spectral_centroid',
        measurements=measurements,
        visualization_data=visualization_data
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
    visualization_data = {}
    
    for channel_name, audio_data in context.audio_data.items():
        
        n_fft = len(audio_data)
        spectrum = np.fft.rfft(audio_data)
        magnitude = np.abs(spectrum) + 1e-10
        
        geometric_mean = np.exp(np.mean(np.log(magnitude)))
        arithmetic_mean = np.mean(magnitude)
        
        flatness = geometric_mean / (arithmetic_mean + 1e-10)
        
        measurements[channel_name] = {
            'spectral_flatness': float(flatness),
            'tonality': float(1.0 - flatness)
        }
        visualization_data[channel_name] = {
            'spectral_flatness': float(flatness),
            'tonality': float(1.0 - flatness)
        }
    
    logger.info(f"Computed spectral flatness for {len(context.audio_data)} channels")
    
    return AnalysisResult(
        method='spectral_flatness',
        measurements=measurements,
        visualization_data=visualization_data
    )


def cepstrum_analysis(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Cepstrum analysis with visualization_data.
    """
    measurements = {}
    visualization_data = {}
    
    for channel_name, audio_data in context.audio_data.items():
        
        max_samples = 100000
        if len(audio_data) > max_samples:
            audio_subset = audio_data[:max_samples]
            logger.warning(f"Cepstrum: using first {max_samples} samples")
        else:
            audio_subset = audio_data
        
        spectrum = np.fft.fft(audio_subset)
        log_spectrum = np.log(np.abs(spectrum) + 1e-10)
        cepstrum = np.fft.ifft(log_spectrum).real
        
        quefrency = np.arange(len(cepstrum)) / context.sample_rate
        
        cepstrum_magnitude = np.abs(cepstrum[:len(cepstrum)//2])
        quefrency_axis = quefrency[:len(cepstrum)//2]
        
        peak_idx = np.argmax(cepstrum_magnitude[1:]) + 1
        peak_quefrency = quefrency_axis[peak_idx]
        peak_magnitude = cepstrum_magnitude[peak_idx]
        
        measurements[channel_name] = {
            'peak_quefrency': float(peak_quefrency),
            'peak_magnitude': float(peak_magnitude),
            'cepstrum_mean': float(np.mean(cepstrum_magnitude)),
            'cepstrum_std': float(np.std(cepstrum_magnitude)),
            'samples_analyzed': len(audio_subset)
        }
        
        # Add visualization data
        visualization_data[channel_name] = {
            'quefrency': quefrency_axis,
            'cepstrum': cepstrum_magnitude,
            'peak_quefrency': peak_quefrency
        }
    
    logger.info(f"Cepstrum for {len(context.audio_data)} channels")
    
    return AnalysisResult(
        method='cepstrum',
        measurements=measurements,
        visualization_data=visualization_data
    )


def spectral_bandwidth(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Spectral bandwidth with visualization_data.
    
    Args:
        context: Analysis context
        params: analysis parameters
        
    Returns:
        AnalysisResult with bandwidth values and visualization_data
    """
    measurements = {}
    visualization_data = {}
    
    for channel_name, audio_data in context.audio_data.items():
        
        spectrum = np.fft.rfft(audio_data)
        magnitude = np.abs(spectrum)
        freqs = np.fft.rfftfreq(len(audio_data), 1/context.sample_rate)
        
        power = magnitude ** 2
        total_power = np.sum(power)
        
        if total_power > 0:
            centroid = np.sum(freqs * power) / total_power
            bandwidth = np.sqrt(np.sum(((freqs - centroid) ** 2) * power) / total_power)
        else:
            centroid = 0
            bandwidth = 0
        
        measurements[channel_name] = {
            'spectral_bandwidth': float(bandwidth),
            'spectral_centroid_Hz': float(centroid)
        }
        
        # AJOUT: visualization_data pour afficher spectrum + bandwidth zone
        visualization_data[channel_name] = {
            'frequencies': freqs,
            'spectrum': magnitude,
            'centroid': centroid,
            'bandwidth': bandwidth,
            'lower_bound': centroid - bandwidth,
            'upper_bound': centroid + bandwidth
        }
    
    logger.info(f"Spectral bandwidth for {len(context.audio_data)} channels")
    
    return AnalysisResult(
        method='spectral_bandwidth',
        measurements=measurements,
        visualization_data=visualization_data
    )


def spectral_rolloff(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Compute spectral rolloff frequency.
    
    Spectral rolloff is the frequency below which a specified percentage
    (default 85%) of the total spectral energy is contained.
    
    Args:
        context: Analysis context
        params: rolloff_percent (default 0.85)
        
    Returns:
        AnalysisResult with rolloff frequency and visualization_data
    """
    rolloff_percent = params.get('rolloff_percent', 0.85)
    
    measurements = {}
    visualization_data = {}
    
    for channel_name, audio_data in context.audio_data.items():
        
        spectrum = np.fft.rfft(audio_data)
        magnitude = np.abs(spectrum)
        freqs = np.fft.rfftfreq(len(audio_data), 1/context.sample_rate)
        
        # Compute cumulative energy
        power = magnitude ** 2
        cumulative_power = np.cumsum(power)
        total_power = cumulative_power[-1]
        
        # Find rolloff frequency
        rolloff_threshold = rolloff_percent * total_power
        rolloff_idx = np.where(cumulative_power >= rolloff_threshold)[0]
        
        if len(rolloff_idx) > 0:
            rolloff_freq = float(freqs[rolloff_idx[0]])
        else:
            rolloff_freq = float(freqs[-1])
        
        measurements[channel_name] = {
            'rolloff_frequency': rolloff_freq,
            'rolloff_percent': rolloff_percent,
            'normalized_rolloff': rolloff_freq / (context.sample_rate / 2),
            'energy_concentration': float(rolloff_freq / (freqs[-1] + 1e-10))
        }
        
        # Visualization data
        visualization_data[channel_name] = {
            'frequencies': freqs,
            'spectrum': magnitude,
            'rolloff_frequency': rolloff_freq,
            'rolloff_percent': rolloff_percent
        }
    
    logger.info(f"Spectral rolloff for {len(context.audio_data)} channels")
    
    return AnalysisResult(
        method='spectral_rolloff',
        measurements=measurements,
        metrics={'rolloff_percent': rolloff_percent},
        visualization_data=visualization_data
    )


def spectral_flux(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Compute spectral flux (rate of spectral change).
    
    Spectral flux measures how quickly the power spectrum changes,
    useful for detecting onsets and temporal variations.
    
    Args:
        context: Analysis context
        params: window_size, hop_length
        
    Returns:
        AnalysisResult with spectral flux over time and visualization_data
    """
    window_size = params.get('window_size', 2048)
    hop_length = params.get('hop_length', 512)
    
    measurements = {}
    visualization_data = {}
    
    for channel_name, audio_data in context.audio_data.items():
        
        # Limit for performance
        max_samples = 200000
        if len(audio_data) > max_samples:
            audio_subset = audio_data[:max_samples]
            logger.warning(f"Spectral flux: using first {max_samples} samples")
        else:
            audio_subset = audio_data
        
        # Compute STFT
        window = get_window('hann', window_size)
        frequencies, times, stft_matrix = signal.stft(
            audio_subset,
            fs=context.sample_rate,
            window=window,
            nperseg=window_size,
            noverlap=window_size - hop_length
        )
        
        magnitude = np.abs(stft_matrix)
        
        # Compute spectral flux (difference between consecutive frames)
        flux = np.sqrt(np.sum(np.diff(magnitude, axis=1) ** 2, axis=0))
        
        measurements[channel_name] = {
            'mean_flux': float(np.mean(flux)),
            'std_flux': float(np.std(flux)),
            'max_flux': float(np.max(flux)),
            'min_flux': float(np.min(flux)),
            'num_frames': len(flux),
            'flux_variation': float(np.std(flux) / (np.mean(flux) + 1e-10))
        }
        
        # Visualization data
        visualization_data[channel_name] = {
            'times': times[1:],  # flux has one less frame than times
            'flux': flux,
            'mean_flux': np.mean(flux)
        }
    
    logger.info(f"Spectral flux for {len(context.audio_data)} channels")
    
    return AnalysisResult(
        method='spectral_flux',
        measurements=measurements,
        metrics={'window_size': window_size, 'hop_length': hop_length},
        visualization_data=visualization_data
    )


# Register methods
register_method("fft_global", "spectral", fft_global, "Global FFT spectrum")
register_method("peak_detection", "spectral", peak_detection, "Spectral peak detection")
register_method("harmonic_analysis", "spectral", harmonic_analysis, "Harmonic structure analysis")
register_method("spectral_centroid", "spectral", spectral_centroid, "Spectral centroid")
register_method("spectral_flatness", "spectral", spectral_flatness, "Spectral flatness")
register_method("cepstrum", "spectral", cepstrum_analysis, "Cepstrum analysis")
register_method("spectral_bandwidth", "spectral", spectral_bandwidth, "Spectral bandwidth")
register_method("spectral_rolloff", "spectral", spectral_rolloff, "Spectral rolloff frequency")
register_method("spectral_flux", "spectral", spectral_flux, "Spectral flux (rate of change)")
