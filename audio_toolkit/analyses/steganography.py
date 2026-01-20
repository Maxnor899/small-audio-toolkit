"""
Steganography analysis methods.
"""

from typing import Dict, Any
import numpy as np
from scipy import stats

from ..engine.context import AnalysisContext
from ..engine.results import AnalysisResult
from ..engine.registry import register_method
from ..utils.logging import get_logger

logger = get_logger(__name__)


def lsb_analysis(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Least Significant Bit analysis with visualization_data.
    
    Args:
        context: Analysis context
        params: analysis parameters
        
    Returns:
        AnalysisResult with LSB analysis and visualization_data
    """
    measurements = {}
    visualization_data = {}
    
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
        
        # Visualization data
        visualization_data[channel_name] = {
            'lsb_bits': lsb_bits[:min(10000, len(lsb_bits))],  # Limit for visualization
            'zero_runs': np.array(zero_runs),
            'one_runs': np.array(one_runs),
            'transition_rate': transition_rate
        }
    
    logger.info(f"LSB analysis for {len(context.audio_data)} channels")
    
    return AnalysisResult(
        method='lsb_analysis',
        measurements=measurements,
        visualization_data=visualization_data
    )


def quantization_noise(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Quantization noise structure analysis.
    """
    measurements = {}
    
    for channel_name, audio_data in context.audio_data.items():
        
        max_samples = 50000  # Reduced for faster autocorrelation
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


def statistical_anomalies(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Detect statistical anomalies using Z-scores and outliers.
    
    Identifies samples that deviate significantly from the mean,
    which could indicate embedded data or tampering.
    
    Args:
        context: Analysis context
        params: z_threshold (default 3.0), num_bins (for histogram)
        
    Returns:
        AnalysisResult with anomaly detection and visualization_data
    """
    z_threshold = params.get('z_threshold', 3.0)
    num_bins = params.get('num_bins', 100)
    
    measurements = {}
    visualization_data = {}
    
    for channel_name, audio_data in context.audio_data.items():
        
        max_samples = 100000
        if len(audio_data) > max_samples:
            audio_subset = audio_data[:max_samples]
            logger.warning(f"Statistical anomalies: using first {max_samples} samples")
        else:
            audio_subset = audio_data
        
        # Compute Z-scores
        mean = np.mean(audio_subset)
        std = np.std(audio_subset)
        z_scores = np.abs((audio_subset - mean) / (std + 1e-10))
        
        # Find outliers
        outliers = np.where(z_scores > z_threshold)[0]
        outlier_values = audio_subset[outliers]
        
        # Histogram
        hist, bin_edges = np.histogram(audio_subset, bins=num_bins, density=True)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        
        # Fit normal distribution
        normal_dist = stats.norm.pdf(bin_centers, mean, std)
        
        # Chi-square goodness of fit test
        observed_freq, _ = np.histogram(audio_subset, bins=num_bins)
        expected_freq = len(audio_subset) * normal_dist * (bin_edges[1] - bin_edges[0])
        
        # Avoid division by zero
        valid_bins = expected_freq > 5
        if np.sum(valid_bins) > 0:
            chi2_stat = np.sum((observed_freq[valid_bins] - expected_freq[valid_bins])**2 / 
                              (expected_freq[valid_bins] + 1e-10))
            chi2_pvalue = 1.0 - stats.chi2.cdf(chi2_stat, np.sum(valid_bins) - 1)
        else:
            chi2_stat = 0
            chi2_pvalue = 1.0
        
        measurements[channel_name] = {
            'num_outliers': len(outliers),
            'outlier_rate': float(len(outliers) / len(audio_subset)),
            'max_z_score': float(np.max(z_scores)),
            'mean_z_score': float(np.mean(z_scores)),
            'chi2_statistic': float(chi2_stat),
            'chi2_pvalue': float(chi2_pvalue),
            'normality_test': chi2_pvalue > 0.05,  # True if data looks normal
            'samples_analyzed': len(audio_subset)
        }
        
        # Visualization data
        visualization_data[channel_name] = {
            'histogram': hist,
            'bin_centers': bin_centers,
            'normal_distribution': normal_dist,
            'outlier_indices': outliers[:1000],  # Limit for viz
            'outlier_values': outlier_values[:1000],
            'z_threshold': z_threshold,
            'z_scores': z_scores[:min(10000, len(z_scores))]
        }
    
    logger.info(f"Statistical anomalies for {len(context.audio_data)} channels")
    
    return AnalysisResult(
        method='statistical_anomalies',
        measurements=measurements,
        metrics={'z_threshold': z_threshold, 'num_bins': num_bins},
        visualization_data=visualization_data
    )


def parity_analysis(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Analyze parity bits for statistical anomalies.
    
    Examines the parity (even/odd) of sample values to detect
    patterns that might indicate steganography.
    
    Args:
        context: Analysis context
        params: analysis parameters
        
    Returns:
        AnalysisResult with parity analysis and visualization_data
    """
    measurements = {}
    visualization_data = {}
    
    for channel_name, audio_data in context.audio_data.items():
        
        max_samples = 100000
        if len(audio_data) > max_samples:
            audio_subset = audio_data[:max_samples]
            logger.warning(f"Parity analysis: using first {max_samples} samples")
        else:
            audio_subset = audio_data
        
        # Convert to 16-bit integers
        audio_int16 = (audio_subset * 32767).astype(np.int16)
        
        # Extract parity bits (LSB of each sample determines parity)
        parity_bits = audio_int16 & 1
        
        # Parity statistics
        parity_mean = np.mean(parity_bits)
        parity_std = np.std(parity_bits)
        
        # Count transitions
        transitions = np.sum(np.abs(np.diff(parity_bits)))
        transition_rate = transitions / (len(parity_bits) - 1)
        
        # Expected transition rate for random parity: ~0.5
        expected_transition_rate = 0.5
        transition_anomaly = abs(transition_rate - expected_transition_rate)
        
        # Run length analysis
        runs = []
        current_run = 1
        for i in range(1, len(parity_bits)):
            if parity_bits[i] == parity_bits[i-1]:
                current_run += 1
            else:
                runs.append(current_run)
                current_run = 1
        runs.append(current_run)
        
        mean_run_length = np.mean(runs)
        std_run_length = np.std(runs)
        
        # Chi-square test for uniform distribution
        observed = np.bincount(parity_bits)
        expected = np.array([len(parity_bits) / 2, len(parity_bits) / 2])
        chi2_stat = np.sum((observed - expected)**2 / expected)
        chi2_pvalue = 1.0 - stats.chi2.cdf(chi2_stat, 1)
        
        measurements[channel_name] = {
            'parity_mean': float(parity_mean),
            'parity_std': float(parity_std),
            'transition_rate': float(transition_rate),
            'transition_anomaly': float(transition_anomaly),
            'mean_run_length': float(mean_run_length),
            'std_run_length': float(std_run_length),
            'chi2_statistic': float(chi2_stat),
            'chi2_pvalue': float(chi2_pvalue),
            'appears_random': chi2_pvalue > 0.05,
            'samples_analyzed': len(audio_subset)
        }
        
        # Visualization data
        visualization_data[channel_name] = {
            'parity_bits': parity_bits[:min(5000, len(parity_bits))],
            'run_lengths': np.array(runs),
            'transition_rate': transition_rate,
            'expected_transition_rate': expected_transition_rate
        }
    
    logger.info(f"Parity analysis for {len(context.audio_data)} channels")
    
    return AnalysisResult(
        method='parity_analysis',
        measurements=measurements,
        visualization_data=visualization_data
    )


register_method("lsb_analysis", "steganography", lsb_analysis, "LSB analysis")
register_method("quantization_noise", "steganography", quantization_noise, "Quantization noise structure")
register_method("signal_residual", "steganography", signal_residual, "Signal vs residual comparison")
register_method("statistical_anomalies", "steganography", statistical_anomalies, "Statistical anomaly detection")
register_method("parity_analysis", "steganography", parity_analysis, "Parity bit analysis")