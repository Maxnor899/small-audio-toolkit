"""
Steganography analysis methods.
"""

from typing import Dict, Any
import numpy as np

from ..engine.context import AnalysisContext
from ..engine.results import AnalysisResult
from ..engine.registry import register_method
from ..utils.logging import get_logger

logger = get_logger(__name__)


def lsb_analysis(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Least Significant Bit analysis.
    """
    measurements = {}
    
    for channel_name, audio_data in context.audio_data.items():
        
        max_samples = 100000
        if len(audio_data) > max_samples:
            audio_subset = audio_data[:max_samples]
            logger.warning(f"LSB analysis: using first {max_samples} samples")
        else:
            audio_subset = audio_data
        
        audio_int16 = (audio_subset * 32767).astype(np.int16)
        
        lsb_bits = audio_int16 & 1
        
        lsb_mean = np.mean(lsb_bits)
        lsb_std = np.std(lsb_bits)
        
        transitions = np.sum(np.abs(np.diff(lsb_bits)))
        transition_rate = transitions / len(lsb_bits)
        
        zero_runs = []
        one_runs = []
        current_run = 1
        for i in range(1, len(lsb_bits)):
            if lsb_bits[i] == lsb_bits[i-1]:
                current_run += 1
            else:
                if lsb_bits[i-1] == 0:
                    zero_runs.append(current_run)
                else:
                    one_runs.append(current_run)
                current_run = 1
        
        measurements[channel_name] = {
            'lsb_mean': float(lsb_mean),
            'lsb_std': float(lsb_std),
            'transition_rate': float(transition_rate),
            'mean_zero_run': float(np.mean(zero_runs)) if zero_runs else 0,
            'mean_one_run': float(np.mean(one_runs)) if one_runs else 0,
            'samples_analyzed': len(audio_subset)
        }
    
    logger.info(f"LSB analysis for {len(context.audio_data)} channels")
    
    return AnalysisResult(
        method='lsb_analysis',
        measurements=measurements
    )


def quantization_noise(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Quantization noise structure analysis.
    """
    measurements = {}
    
    for channel_name, audio_data in context.audio_data.items():
        
        max_samples = 100000
        if len(audio_data) > max_samples:
            audio_subset = audio_data[:max_samples]
            logger.warning(f"Quantization noise: using first {max_samples} samples")
        else:
            audio_subset = audio_data
        
        audio_int16 = (audio_subset * 32767).astype(np.int16)
        audio_reconstructed = audio_int16.astype(np.float32) / 32767.0
        
        noise = audio_subset - audio_reconstructed
        
        noise_power = np.mean(noise ** 2)
        noise_std = np.std(noise)
        
        autocorr = np.correlate(noise, noise, mode='full')
        autocorr = autocorr[len(autocorr)//2:]
        autocorr = autocorr / autocorr[0]
        
        if len(autocorr) > 1:
            first_peak = np.max(autocorr[1:min(100, len(autocorr))])
        else:
            first_peak = 0
        
        noise_spectrum = np.abs(np.fft.rfft(noise))
        flatness = np.exp(np.mean(np.log(noise_spectrum + 1e-10))) / (np.mean(noise_spectrum) + 1e-10)
        
        measurements[channel_name] = {
            'noise_power': float(noise_power),
            'noise_std': float(noise_std),
            'autocorr_peak': float(first_peak),
            'spectral_flatness': float(flatness),
            'samples_analyzed': len(audio_subset)
        }
    
    logger.info(f"Quantization noise for {len(context.audio_data)} channels")
    
    return AnalysisResult(
        method='quantization_noise',
        measurements=measurements
    )


def signal_residual(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Signal vs residual comparison after filtering.
    """
    from scipy import signal
    
    cutoff_freq = params.get('cutoff_freq', 1000)
    
    measurements = {}
    
    for channel_name, audio_data in context.audio_data.items():
        
        max_samples = 100000
        if len(audio_data) > max_samples:
            audio_subset = audio_data[:max_samples]
            logger.warning(f"Signal residual: using first {max_samples} samples")
        else:
            audio_subset = audio_data
        
        nyquist = context.sample_rate / 2
        normalized_cutoff = cutoff_freq / nyquist
        
        b, a = signal.butter(4, normalized_cutoff, btype='low')
        filtered = signal.filtfilt(b, a, audio_subset)
        
        residual = audio_subset - filtered
        
        signal_power = np.mean(filtered ** 2)
        residual_power = np.mean(residual ** 2)
        
        if signal_power > 0:
            snr = 10 * np.log10(signal_power / (residual_power + 1e-10))
        else:
            snr = 0
        
        residual_spectrum = np.abs(np.fft.rfft(residual))
        freqs = np.fft.rfftfreq(len(residual), 1/context.sample_rate)
        
        if len(residual_spectrum) > 0:
            peak_idx = np.argmax(residual_spectrum)
            peak_freq = freqs[peak_idx]
        else:
            peak_freq = 0
        
        measurements[channel_name] = {
            'signal_power': float(signal_power),
            'residual_power': float(residual_power),
            'snr_db': float(snr),
            'residual_peak_freq': float(peak_freq),
            'energy_ratio': float(residual_power / (signal_power + 1e-10)),
            'samples_analyzed': len(audio_subset)
        }
    
    logger.info(f"Signal residual for {len(context.audio_data)} channels")
    
    return AnalysisResult(
        method='signal_residual',
        measurements=measurements,
        metrics={'cutoff_freq': cutoff_freq}
    )


register_method("lsb_analysis", "steganography", lsb_analysis, "LSB analysis")
register_method("quantization_noise", "steganography", quantization_noise, "Quantization noise structure")
register_method("signal_residual", "steganography", signal_residual, "Signal vs residual comparison")