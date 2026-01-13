"""
Extended visualization functions for all analysis methods.
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

from ..utils.logging import get_logger

logger = get_logger(__name__)


def plot_harmonics(
    frequencies: np.ndarray,
    magnitudes: np.ndarray,
    fundamental: float,
    harmonics: List[float],
    output_path: Path,
    figsize: tuple = (12, 8),
    dpi: int = 150,
    formats: list = ['png']
) -> None:
    """Plot spectrum with harmonic markers."""
    fig, ax = plt.subplots(figsize=figsize)
    
    magnitudes_db = 20 * np.log10(magnitudes + 1e-10)
    ax.plot(frequencies, magnitudes_db, linewidth=1, color='blue', alpha=0.7, label='Spectrum')
    
    # Mark fundamental
    ax.axvline(x=fundamental, color='red', linestyle='--', linewidth=2, label=f'Fundamental: {fundamental:.1f} Hz')
    
    # Mark harmonics
    for i, harmonic in enumerate(harmonics, start=2):
        ax.axvline(x=harmonic, color='orange', linestyle='--', linewidth=1, alpha=0.5, label=f'H{i}: {harmonic:.1f} Hz' if i <= 5 else '')
    
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Magnitude (dB)')
    ax.set_title('Harmonic Analysis')
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)
    
    save_figure(fig, output_path, formats, dpi)
    plt.close(fig)


def plot_cepstrum(
    quefrency: np.ndarray,
    cepstrum: np.ndarray,
    peak_quefrency: float,
    output_path: Path,
    figsize: tuple = (12, 8),
    dpi: int = 150,
    formats: list = ['png']
) -> None:
    """Plot cepstrum."""
    fig, ax = plt.subplots(figsize=figsize)
    
    ax.plot(quefrency * 1000, cepstrum, linewidth=1, color='green')
    ax.axvline(x=peak_quefrency * 1000, color='red', linestyle='--', label=f'Peak: {peak_quefrency*1000:.2f} ms')
    
    ax.set_xlabel('Quefrency (ms)')
    ax.set_ylabel('Amplitude')
    ax.set_title('Cepstrum')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    save_figure(fig, output_path, formats, dpi)
    plt.close(fig)


def plot_band_stability(
    times: np.ndarray,
    bands_data: Dict[str, np.ndarray],
    output_path: Path,
    figsize: tuple = (12, 8),
    dpi: int = 150,
    formats: list = ['png']
) -> None:
    """Plot band energy stability over time."""
    fig, ax = plt.subplots(figsize=figsize)
    
    for band_name, energy in bands_data.items():
        ax.plot(times, energy, linewidth=1, label=band_name)
    
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Energy')
    ax.set_title('Frequency Band Stability')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    save_figure(fig, output_path, formats, dpi)
    plt.close(fig)


def plot_wavelet_scalogram(
    scalogram: np.ndarray,
    scales: np.ndarray,
    sample_rate: int,
    output_path: Path,
    figsize: tuple = (12, 8),
    dpi: int = 150,
    formats: list = ['png']
) -> None:
    """Plot wavelet scalogram."""
    fig, ax = plt.subplots(figsize=figsize)
    
    extent = [0, scalogram.shape[1] / sample_rate, scales[-1], scales[0]]
    
    im = ax.imshow(
        np.abs(scalogram),
        aspect='auto',
        cmap='viridis',
        extent=extent,
        interpolation='bilinear'
    )
    
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Scale')
    ax.set_title('Wavelet Scalogram')
    
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Magnitude')
    
    save_figure(fig, output_path, formats, dpi)
    plt.close(fig)


def plot_am_detection(
    time: np.ndarray,
    envelope: np.ndarray,
    modulation_frequencies: np.ndarray,
    modulation_spectrum: np.ndarray,
    output_path: Path,
    figsize: tuple = (12, 8),
    dpi: int = 150,
    formats: list = ['png']
) -> None:
    """Plot AM detection results."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize)
    
    # Envelope
    ax1.plot(time, envelope, linewidth=1, color='red')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Amplitude')
    ax1.set_title('Amplitude Envelope')
    ax1.grid(True, alpha=0.3)
    
    # Modulation spectrum
    ax2.plot(modulation_frequencies, modulation_spectrum, linewidth=1, color='blue')
    ax2.set_xlabel('Modulation Frequency (Hz)')
    ax2.set_ylabel('Magnitude')
    ax2.set_title('Modulation Spectrum')
    ax2.grid(True, alpha=0.3)
    
    fig.tight_layout()
    save_figure(fig, output_path, formats, dpi)
    plt.close(fig)


def plot_fm_detection(
    time: np.ndarray,
    instantaneous_frequency: np.ndarray,
    carrier_frequency: float,
    output_path: Path,
    figsize: tuple = (12, 8),
    dpi: int = 150,
    formats: list = ['png']
) -> None:
    """Plot FM detection results."""
    fig, ax = plt.subplots(figsize=figsize)
    
    ax.plot(time, instantaneous_frequency, linewidth=1, color='blue')
    ax.axhline(y=carrier_frequency, color='red', linestyle='--', label=f'Carrier: {carrier_frequency:.1f} Hz')
    
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Frequency (Hz)')
    ax.set_title('Instantaneous Frequency (FM Detection)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    save_figure(fig, output_path, formats, dpi)
    plt.close(fig)


def plot_phase_analysis(
    time: np.ndarray,
    phase: np.ndarray,
    jumps: np.ndarray,
    output_path: Path,
    figsize: tuple = (12, 8),
    dpi: int = 150,
    formats: list = ['png']
) -> None:
    """Plot phase analysis with jump markers."""
    fig, ax = plt.subplots(figsize=figsize)
    
    ax.plot(time, phase, linewidth=1, color='blue', label='Phase')
    if len(jumps) > 0:
        ax.plot(time[jumps], phase[jumps], 'rx', markersize=10, label=f'Jumps ({len(jumps)})')
    
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Phase (radians)')
    ax.set_title('Instantaneous Phase Analysis')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    save_figure(fig, output_path, formats, dpi)
    plt.close(fig)


def plot_cross_correlation(
    lags: np.ndarray,
    correlation: np.ndarray,
    channel_pair: str,
    output_path: Path,
    figsize: tuple = (12, 8),
    dpi: int = 150,
    formats: list = ['png']
) -> None:
    """Plot cross-correlation between channels."""
    fig, ax = plt.subplots(figsize=figsize)
    
    ax.plot(lags, correlation, linewidth=1, color='purple')
    peak_idx = np.argmax(np.abs(correlation))
    ax.axvline(x=lags[peak_idx], color='red', linestyle='--', label=f'Peak lag: {lags[peak_idx]:.0f} samples')
    
    ax.set_xlabel('Lag (samples)')
    ax.set_ylabel('Correlation')
    ax.set_title(f'Cross-Correlation: {channel_pair}')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    save_figure(fig, output_path, formats, dpi)
    plt.close(fig)


def plot_lr_difference(
    frequencies: np.ndarray,
    left_spectrum: np.ndarray,
    right_spectrum: np.ndarray,
    difference_spectrum: np.ndarray,
    output_path: Path,
    figsize: tuple = (12, 8),
    dpi: int = 150,
    formats: list = ['png']
) -> None:
    """Plot L, R, and L-R spectra."""
    fig, ax = plt.subplots(figsize=figsize)
    
    ax.plot(frequencies, 20*np.log10(left_spectrum+1e-10), linewidth=1, label='Left', alpha=0.7)
    ax.plot(frequencies, 20*np.log10(right_spectrum+1e-10), linewidth=1, label='Right', alpha=0.7)
    ax.plot(frequencies, 20*np.log10(difference_spectrum+1e-10), linewidth=2, label='L-R Difference', color='red')
    
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Magnitude (dB)')
    ax.set_title('L-R Stereo Field Analysis')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    save_figure(fig, output_path, formats, dpi)
    plt.close(fig)


def plot_phase_difference(
    frequencies: np.ndarray,
    phase_diff: np.ndarray,
    coherence: np.ndarray,
    channel_pair: str,
    output_path: Path,
    figsize: tuple = (12, 8),
    dpi: int = 150,
    formats: list = ['png']
) -> None:
    """Plot phase difference and coherence."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize)
    
    ax1.plot(frequencies, phase_diff, linewidth=1, color='blue')
    ax1.axhline(y=0, color='red', linestyle='--', alpha=0.5)
    ax1.axhline(y=np.pi, color='red', linestyle='--', alpha=0.5)
    ax1.axhline(y=-np.pi, color='red', linestyle='--', alpha=0.5)
    ax1.set_ylabel('Phase Difference (rad)')
    ax1.set_title(f'Phase Difference: {channel_pair}')
    ax1.grid(True, alpha=0.3)
    
    ax2.plot(frequencies, coherence, linewidth=1, color='green')
    ax2.set_xlabel('Frequency (Hz)')
    ax2.set_ylabel('Coherence')
    ax2.set_title('Phase Coherence')
    ax2.grid(True, alpha=0.3)
    
    fig.tight_layout()
    save_figure(fig, output_path, formats, dpi)
    plt.close(fig)


def plot_local_entropy(
    times: np.ndarray,
    entropy: np.ndarray,
    output_path: Path,
    figsize: tuple = (12, 8),
    dpi: int = 150,
    formats: list = ['png']
) -> None:
    """Plot local entropy over time."""
    fig, ax = plt.subplots(figsize=figsize)
    
    ax.plot(times, entropy, linewidth=1, color='purple')
    ax.axhline(y=np.mean(entropy), color='red', linestyle='--', label=f'Mean: {np.mean(entropy):.2f}')
    
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Entropy')
    ax.set_title('Local Entropy (Windowed)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    save_figure(fig, output_path, formats, dpi)
    plt.close(fig)


def plot_lsb_analysis(
    lsb_bits: np.ndarray,
    output_path: Path,
    figsize: tuple = (12, 8),
    dpi: int = 150,
    formats: list = ['png']
) -> None:
    """Plot LSB bit distribution."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    
    # Time series
    ax1.plot(lsb_bits[:1000], linewidth=1, color='blue')
    ax1.set_xlabel('Sample')
    ax1.set_ylabel('LSB Value')
    ax1.set_title('LSB Sequence (first 1000)')
    ax1.grid(True, alpha=0.3)
    
    # Histogram
    ax2.hist(lsb_bits, bins=2, color='green', edgecolor='black')
    ax2.set_xlabel('LSB Value')
    ax2.set_ylabel('Count')
    ax2.set_title('LSB Distribution')
    ax2.grid(True, alpha=0.3)
    
    fig.tight_layout()
    save_figure(fig, output_path, formats, dpi)
    plt.close(fig)


def plot_quantization_noise(
    frequencies: np.ndarray,
    noise_spectrum: np.ndarray,
    output_path: Path,
    figsize: tuple = (12, 8),
    dpi: int = 150,
    formats: list = ['png']
) -> None:
    """Plot quantization noise spectrum."""
    fig, ax = plt.subplots(figsize=figsize)
    
    ax.plot(frequencies, 20*np.log10(noise_spectrum+1e-10), linewidth=1, color='red')
    
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Magnitude (dB)')
    ax.set_title('Quantization Noise Spectrum')
    ax.grid(True, alpha=0.3)
    
    save_figure(fig, output_path, formats, dpi)
    plt.close(fig)


def plot_signal_residual(
    time: np.ndarray,
    signal: np.ndarray,
    residual: np.ndarray,
    output_path: Path,
    figsize: tuple = (12, 8),
    dpi: int = 150,
    formats: list = ['png']
) -> None:
    """Plot signal vs residual."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize)
    
    ax1.plot(time, signal, linewidth=0.5, color='blue', label='Filtered Signal')
    ax1.set_ylabel('Amplitude')
    ax1.set_title('Filtered Signal')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    ax2.plot(time, residual, linewidth=0.5, color='red', label='Residual')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Amplitude')
    ax2.set_title('Residual (High-pass)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    fig.tight_layout()
    save_figure(fig, output_path, formats, dpi)
    plt.close(fig)


def plot_segment_comparison(
    distance_matrix: np.ndarray,
    output_path: Path,
    figsize: tuple = (12, 8),
    dpi: int = 150,
    formats: list = ['png']
) -> None:
    """Plot segment distance matrix."""
    fig, ax = plt.subplots(figsize=figsize)
    
    im = ax.imshow(distance_matrix, cmap='viridis', aspect='auto')
    ax.set_xlabel('Segment')
    ax.set_ylabel('Segment')
    ax.set_title('Inter-Segment Distance Matrix')
    
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Distance')
    
    save_figure(fig, output_path, formats, dpi)
    plt.close(fig)


def plot_clustering(
    features_2d: np.ndarray,
    labels: np.ndarray,
    output_path: Path,
    figsize: tuple = (12, 8),
    dpi: int = 150,
    formats: list = ['png']
) -> None:
    """Plot segment clustering."""
    fig, ax = plt.subplots(figsize=figsize)
    
    scatter = ax.scatter(features_2d[:, 0], features_2d[:, 1], c=labels, cmap='tab10', s=100)
    ax.set_xlabel('Feature 1')
    ax.set_ylabel('Feature 2')
    ax.set_title('Segment Clustering')
    plt.colorbar(scatter, ax=ax, label='Cluster')
    
    save_figure(fig, output_path, formats, dpi)
    plt.close(fig)


def plot_stability_scores(
    times: np.ndarray,
    energy_stability: np.ndarray,
    spectral_stability: np.ndarray,
    output_path: Path,
    figsize: tuple = (12, 8),
    dpi: int = 150,
    formats: list = ['png']
) -> None:
    """Plot temporal and spectral stability."""
    fig, ax = plt.subplots(figsize=figsize)
    
    ax.plot(times, energy_stability, linewidth=1, label='Energy Stability')
    ax.plot(times, spectral_stability, linewidth=1, label='Spectral Stability')
    
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Stability Score')
    ax.set_title('Temporal and Spectral Stability')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    save_figure(fig, output_path, formats, dpi)
    plt.close(fig)


def plot_pulses(
    time: np.ndarray,
    signal: np.ndarray,
    pulse_locations: np.ndarray,
    output_path: Path,
    figsize: tuple = (12, 8),
    dpi: int = 150,
    formats: list = ['png']
) -> None:
    """Plot detected pulses on signal."""
    fig, ax = plt.subplots(figsize=figsize)
    
    ax.plot(time, signal, linewidth=0.5, color='blue', alpha=0.7)
    ax.plot(time[pulse_locations], signal[pulse_locations], 'rx', markersize=8, label=f'{len(pulse_locations)} pulses')
    
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Amplitude')
    ax.set_title('Pulse Detection')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    save_figure(fig, output_path, formats, dpi)
    plt.close(fig)


def save_figure(fig: plt.Figure, output_path: Path, formats: list, dpi: int) -> None:
    """Save figure in specified formats."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    for fmt in formats:
        file_path = output_path.with_suffix(f'.{fmt}')
        fig.savefig(file_path, dpi=dpi, bbox_inches='tight')
    