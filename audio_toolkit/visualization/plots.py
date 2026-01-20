# audio_toolkit/visualization/plots.py
"""
Extended visualization functions for all analysis methods + Visualizer wrapper.

Per architecture: visualization is optional and must not affect analysis execution.
"""

from pathlib import Path
from typing import Dict, Any, List
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from ..utils.logging import get_logger

logger = get_logger(__name__)


# ----------------------------
# Small helpers
# ----------------------------

def save_figure(fig: plt.Figure, output_path: Path, formats: list, dpi: int) -> None:
    """Save figure in specified formats."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    for fmt in formats:
        file_path = output_path.with_suffix(f".{fmt}")
        fig.savefig(file_path, dpi=dpi, bbox_inches="tight")


# ----------------------------
# Basic plots
# ----------------------------

def plot_waveform(
    signal: np.ndarray,
    sample_rate: int,
    output_path: Path,
    title: str,
    figsize: tuple = (12, 4),
    dpi: int = 150,
    formats: list = ["png"],
) -> None:
    """Plot a waveform."""
    fig, ax = plt.subplots(figsize=figsize)
    t = np.arange(len(signal)) / float(sample_rate)
    ax.plot(t, signal, linewidth=0.8, color="blue", alpha=0.8)
    ax.set_title(title)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    save_figure(fig, output_path, formats, dpi)
    plt.close(fig)


def plot_spectrum(
    frequencies: np.ndarray,
    magnitudes: np.ndarray,
    output_path: Path,
    title: str,
    figsize: tuple = (12, 4),
    dpi: int = 150,
    formats: list = ["png"],
    db: bool = True,
) -> None:
    """Plot a magnitude spectrum."""
    fig, ax = plt.subplots(figsize=figsize)
    y = magnitudes
    if db:
        y = 20 * np.log10(np.maximum(magnitudes, 1e-12))
        ax.set_ylabel("Magnitude (dB)")
    else:
        ax.set_ylabel("Magnitude")

    ax.plot(frequencies, y, linewidth=0.8, color="blue", alpha=0.8)
    ax.set_title(title)
    ax.set_xlabel("Frequency (Hz)")
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    save_figure(fig, output_path, formats, dpi)
    plt.close(fig)


def plot_multi_channel(
    channels: Dict[str, np.ndarray],
    sample_rate: int,
    output_path: Path,
    title: str,
    figsize: tuple = (12, 6),
    dpi: int = 150,
    formats: list = ["png"],
) -> None:
    """Overlay multiple channels waveforms."""
    fig, ax = plt.subplots(figsize=figsize)

    for name, sig in channels.items():
        t = np.arange(len(sig)) / float(sample_rate)
        ax.plot(t, sig, linewidth=0.7, alpha=0.8, label=name)

    ax.set_title(title)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")
    ax.legend()
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    save_figure(fig, output_path, formats, dpi)
    plt.close(fig)


def plot_envelope(
    envelope: np.ndarray,
    sample_rate: int,
    output_path: Path,
    title: str,
    figsize: tuple = (12, 4),
    dpi: int = 150,
    formats: list = ["png"],
) -> None:
    """Plot amplitude envelope."""
    fig, ax = plt.subplots(figsize=figsize)
    t = np.arange(len(envelope)) / float(sample_rate)
    ax.plot(t, envelope, linewidth=1.0, color="red", alpha=0.8)
    ax.set_title(title)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    save_figure(fig, output_path, formats, dpi)
    plt.close(fig)


def plot_autocorrelation(
    autocorr: np.ndarray,
    sample_rate: int,
    output_path: Path,
    title: str,
    figsize: tuple = (12, 4),
    dpi: int = 150,
    formats: list = ["png"],
) -> None:
    """Plot autocorrelation (lag in seconds)."""
    fig, ax = plt.subplots(figsize=figsize)
    lags = np.arange(len(autocorr)) / float(sample_rate)
    ax.plot(lags, autocorr, linewidth=1.0, color="green", alpha=0.8)
    ax.set_title(title)
    ax.set_xlabel("Lag (s)")
    ax.set_ylabel("Correlation")
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    save_figure(fig, output_path, formats, dpi)
    plt.close(fig)


def plot_peaks(
    spectrum: np.ndarray,
    peaks: np.ndarray,
    output_path: Path,
    title: str,
    xlabel: str = "Bin",
    ylabel: str = "Magnitude",
    figsize: tuple = (12, 4),
    dpi: int = 150,
    formats: list = ["png"],
) -> None:
    """Plot spectrum bins with detected peaks highlighted."""
    fig, ax = plt.subplots(figsize=figsize)
    x = np.arange(len(spectrum))
    ax.plot(x, spectrum, linewidth=0.8, color="blue", alpha=0.7)

    if peaks is not None and len(peaks) > 0:
        ax.plot(peaks, spectrum[peaks], "rx", markersize=6, label=f"Peaks ({len(peaks)})")
        ax.legend()

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    save_figure(fig, output_path, formats, dpi)
    plt.close(fig)


# ----------------------------
# Extended plots
# ----------------------------

def plot_harmonics(
    frequencies: np.ndarray,
    magnitudes: np.ndarray,
    fundamental: float,
    harmonics: List[float],
    output_path: Path,
    figsize: tuple = (12, 8),
    dpi: int = 150,
    formats: list = ["png"],
) -> None:
    """Plot spectrum with harmonic markers."""
    fig, ax = plt.subplots(figsize=figsize)

    magnitudes_db = 20 * np.log10(magnitudes + 1e-10)
    ax.plot(
        frequencies, magnitudes_db, linewidth=1, color="blue", alpha=0.7, label="Spectrum"
    )

    ax.axvline(
        x=fundamental,
        color="red",
        linestyle="--",
        linewidth=2,
        label=f"Fundamental: {fundamental:.1f} Hz",
    )

    for i, harmonic in enumerate(harmonics, start=2):
        ax.axvline(
            x=harmonic,
            color="orange",
            linestyle="--",
            linewidth=1,
            alpha=0.5,
            label=f"H{i}: {harmonic:.1f} Hz" if i <= 5 else "",
        )

    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Magnitude (dB)")
    ax.set_title("Harmonic Analysis")
    ax.legend(loc="upper right")
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
    formats: list = ["png"],
) -> None:
    """Plot cepstrum."""
    fig, ax = plt.subplots(figsize=figsize)

    ax.plot(quefrency * 1000, cepstrum, linewidth=1, color="green")
    ax.axvline(
        x=peak_quefrency * 1000,
        color="red",
        linestyle="--",
        label=f"Peak: {peak_quefrency*1000:.2f} ms",
    )

    ax.set_xlabel("Quefrency (ms)")
    ax.set_ylabel("Amplitude")
    ax.set_title("Cepstrum")
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
    formats: list = ["png"],
) -> None:
    """Plot band energy stability over time."""
    fig, ax = plt.subplots(figsize=figsize)

    for band_name, energy in bands_data.items():
        ax.plot(times, energy, linewidth=1, label=band_name)

    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Energy")
    ax.set_title("Frequency Band Stability")
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
    formats: list = ["png"],
) -> None:
    """Plot wavelet scalogram."""
    fig, ax = plt.subplots(figsize=figsize)

    extent = [0, scalogram.shape[1] / sample_rate, scales[-1], scales[0]]

    im = ax.imshow(
        np.abs(scalogram),
        aspect="auto",
        cmap="viridis",
        extent=extent,
        interpolation="bilinear",
    )

    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Scale")
    ax.set_title("Wavelet Scalogram")

    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label("Magnitude")

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
    formats: list = ["png"],
) -> None:
    """Plot AM detection results."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize)

    ax1.plot(time, envelope, linewidth=1, color="red")
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Amplitude")
    ax1.set_title("Amplitude Envelope")
    ax1.grid(True, alpha=0.3)

    ax2.plot(modulation_frequencies, modulation_spectrum, linewidth=1, color="blue")
    ax2.set_xlabel("Modulation Frequency (Hz)")
    ax2.set_ylabel("Magnitude")
    ax2.set_title("Modulation Spectrum")
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
    formats: list = ["png"],
) -> None:
    """Plot FM detection results."""
    fig, ax = plt.subplots(figsize=figsize)

    ax.plot(time, instantaneous_frequency, linewidth=1, color="blue")
    ax.axhline(
        y=carrier_frequency,
        color="red",
        linestyle="--",
        label=f"Carrier: {carrier_frequency:.1f} Hz",
    )

    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Frequency (Hz)")
    ax.set_title("Instantaneous Frequency (FM Detection)")
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
    formats: list = ["png"],
) -> None:
    """Plot phase analysis with jump markers."""
    fig, ax = plt.subplots(figsize=figsize)

    ax.plot(time, phase, linewidth=1, color="blue", label="Phase")
    if len(jumps) > 0:
        ax.plot(time[jumps], phase[jumps], "rx", markersize=10, label=f"Jumps ({len(jumps)})")

    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Phase (radians)")
    ax.set_title("Instantaneous Phase Analysis")
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
    formats: list = ["png"],
) -> None:
    """Plot cross-correlation between channels."""
    fig, ax = plt.subplots(figsize=figsize)

    ax.plot(lags, correlation, linewidth=1, color="purple")
    peak_idx = np.argmax(np.abs(correlation))
    ax.axvline(
        x=lags[peak_idx],
        color="red",
        linestyle="--",
        label=f"Peak lag: {lags[peak_idx]:.0f} samples",
    )

    ax.set_xlabel("Lag (samples)")
    ax.set_ylabel("Correlation")
    ax.set_title(f"Cross-Correlation: {channel_pair}")
    ax.legend()
    ax.grid(True, alpha=0.3)

    save_figure(fig, output_path, formats, dpi)
    plt.close(fig)


def plot_stft_spectrogram(
    frequencies: np.ndarray,
    times: np.ndarray,
    stft_matrix: np.ndarray,
    sample_rate: int,
    output_path: Path,
    title: str = "STFT Spectrogram",
    figsize: tuple = (14, 8),
    dpi: int = 150,
    formats: list = ["png"],
    vmin: float = -80,
    vmax: float = 0,
    cmap: str = "viridis",
    gain_db: float = 0.0,
) -> None:
    """
    Plot STFT spectrogram (time-frequency representation).

    Args:
        frequencies: Frequency bins (Hz)
        times: Time frames (seconds)
        stft_matrix: Complex STFT matrix (freq x time)
        sample_rate: Audio sample rate
        output_path: Output file path (without extension)
        title: Plot title
    """
    fig, ax = plt.subplots(figsize=figsize)

    magnitude = np.abs(stft_matrix)
    magnitude_db = 20 * np.log10(magnitude + 1e-12) + float(gain_db)

    im = ax.pcolormesh(
        times,
        frequencies,
        magnitude_db,
        shading="auto",
        cmap=cmap,
        vmin=vmin,
        vmax=vmax,
    )

    ax.set_xlabel("Time")
    ax.set_ylabel("Hz")
    ax.set_title(title)

    # Format time axis for long durations
    if len(times) > 0 and times[-1] > 120:
        from matplotlib.ticker import FuncFormatter

        def format_time(x, _p):
            minutes = int(x // 60)
            seconds = int(x % 60)
            return f"{minutes}:{seconds:02d}"

        ax.xaxis.set_major_formatter(FuncFormatter(format_time))

    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label("Magnitude (dB)")

    fig.tight_layout()
    save_figure(fig, output_path, formats, dpi)
    plt.close(fig)


def plot_cqt_spectrogram(
    frequencies: np.ndarray,
    times: np.ndarray,
    cqt_db: np.ndarray,
    output_path: Path,
    title: str = "CQT Spectrogram",
    figsize: tuple = (14, 8),
    dpi: int = 150,
    formats: list = ["png"],
    vmin: float = None,
    vmax: float = None,
) -> None:
    """
    Plot CQT spectrogram (log-frequency time-frequency representation).

    Args:
        frequencies: CQT center frequencies (Hz), length = freq_bins
        times: Time frames (s), length = time_bins
        cqt_db: Magnitude in dB (freq_bins x time_bins)
        output_path: Output file path (without extension)
        title: Plot title
    """
    fig, ax = plt.subplots(figsize=figsize)

    freqs = np.asarray(frequencies)
    t = np.asarray(times)
    M = np.asarray(cqt_db)

    # Robust display range defaults
    if vmin is None:
        vmin = float(np.percentile(M, 5))
    if vmax is None:
        vmax = float(np.percentile(M, 95))

    im = ax.pcolormesh(
        t,
        freqs,
        M,
        shading="auto",
        cmap="viridis",
        vmin=vmin,
        vmax=vmax,
    )

    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Frequency (Hz)")
    ax.set_title(title)

    if np.all(freqs > 0):
        ax.set_yscale("log")

    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label("Magnitude (dB)")

    fig.tight_layout()
    save_figure(fig, output_path, formats, dpi)
    plt.close(fig)



# ----------------------------
# NEW visualizations
# ----------------------------

def plot_pulse_detection(
    waveform: np.ndarray,
    envelope: np.ndarray,
    pulse_positions: np.ndarray,
    threshold_level: float,
    sample_rate: int,
    output_path: Path,
    title: str = "Pulse Detection",
    figsize: tuple = (14, 6),
    dpi: int = 150,
    formats: list = ["png"],
) -> None:
    """
    Plot waveform with detected pulse markers.
    
    Args:
        waveform: Audio waveform
        envelope: Hilbert envelope
        pulse_positions: Sample indices of detected pulses
        threshold_level: Detection threshold level
        sample_rate: Sample rate in Hz
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize, sharex=True)
    
    time = np.arange(len(waveform)) / float(sample_rate)
    
    # Top: waveform with pulse markers
    ax1.plot(time, waveform, linewidth=0.5, color="blue", alpha=0.6, label="Waveform")
    
    if len(pulse_positions) > 0:
        pulse_times = pulse_positions / float(sample_rate)
        ax1.scatter(
            pulse_times,
            waveform[pulse_positions],
            color="red",
            s=50,
            marker="x",
            linewidths=2,
            label=f"Pulses ({len(pulse_positions)})",
            zorder=5
        )
    
    ax1.set_ylabel("Amplitude")
    ax1.set_title(title)
    ax1.legend(loc="upper right")
    ax1.grid(True, alpha=0.25)
    
    # Bottom: envelope with threshold
    ax2.plot(time, envelope, linewidth=1, color="orange", alpha=0.8, label="Envelope")
    ax2.axhline(
        y=threshold_level,
        color="red",
        linestyle="--",
        linewidth=1.5,
        label=f"Threshold: {threshold_level:.3f}",
        alpha=0.7
    )
    
    if len(pulse_positions) > 0:
        pulse_times = pulse_positions / float(sample_rate)
        ax2.scatter(
            pulse_times,
            envelope[pulse_positions],
            color="red",
            s=30,
            marker="o",
            alpha=0.6,
            zorder=5
        )
    
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Envelope")
    ax2.legend(loc="upper right")
    ax2.grid(True, alpha=0.25)
    
    fig.tight_layout()
    save_figure(fig, output_path, formats, dpi)
    plt.close(fig)


def plot_spectral_centroid(
    frequencies: np.ndarray,
    spectrum: np.ndarray,
    centroid: float,
    output_path: Path,
    title: str = "Spectral Centroid",
    figsize: tuple = (12, 6),
    dpi: int = 150,
    formats: list = ["png"],
) -> None:
    """Plot spectrum with centroid marker."""
    fig, ax = plt.subplots(figsize=figsize)
    
    spectrum_db = 20 * np.log10(spectrum + 1e-12)
    ax.plot(frequencies, spectrum_db, linewidth=1, color="blue", alpha=0.7, label="Spectrum")
    
    ax.axvline(
        x=centroid,
        color="red",
        linestyle="--",
        linewidth=2,
        label=f"Centroid: {centroid:.1f} Hz",
        alpha=0.8
    )
    
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Magnitude (dB)")
    ax.set_title(title)
    ax.legend(loc="upper right")
    ax.grid(True, alpha=0.25)
    
    fig.tight_layout()
    save_figure(fig, output_path, formats, dpi)
    plt.close(fig)


def plot_spectral_bandwidth(
    frequencies: np.ndarray,
    spectrum: np.ndarray,
    centroid: float,
    bandwidth: float,
    lower_bound: float,
    upper_bound: float,
    output_path: Path,
    title: str = "Spectral Bandwidth",
    figsize: tuple = (12, 6),
    dpi: int = 150,
    formats: list = ["png"],
) -> None:
    """Plot spectrum with bandwidth zone."""
    fig, ax = plt.subplots(figsize=figsize)
    
    spectrum_db = 20 * np.log10(spectrum + 1e-12)
    ax.plot(frequencies, spectrum_db, linewidth=1, color="blue", alpha=0.7, label="Spectrum")
    
    ax.axvline(
        x=centroid,
        color="red",
        linestyle="--",
        linewidth=2,
        label=f"Centroid: {centroid:.1f} Hz",
        alpha=0.8
    )
    
    ax.axvspan(
        lower_bound,
        upper_bound,
        color="red",
        alpha=0.2,
        label=f"Bandwidth: {bandwidth:.1f} Hz"
    )
    
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Magnitude (dB)")
    ax.set_title(title)
    ax.legend(loc="upper right")
    ax.grid(True, alpha=0.25)
    
    fig.tight_layout()
    save_figure(fig, output_path, formats, dpi)
    plt.close(fig)


def plot_temporal_curve(
    times: np.ndarray,
    values: np.ndarray,
    mean_level: float,
    output_path: Path,
    title: str,
    ylabel: str,
    figsize: tuple = (14, 5),
    dpi: int = 150,
    formats: list = ["png"],
) -> None:
    """Plot a temporal curve (generic for entropy, stability, etc.)."""
    fig, ax = plt.subplots(figsize=figsize)
    
    ax.plot(times, values, linewidth=1, color="blue", alpha=0.7, label=ylabel)
    
    ax.axhline(
        y=mean_level,
        color="red",
        linestyle="--",
        linewidth=1,
        label=f"Mean: {mean_level:.3f}",
        alpha=0.6
    )
    
    ax.set_xlabel("Time (s)")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend(loc="upper right")
    ax.grid(True, alpha=0.25)
    
    fig.tight_layout()
    save_figure(fig, output_path, formats, dpi)
    plt.close(fig)


def plot_stability_dual(
    times: np.ndarray,
    energy: np.ndarray,
    spectral_centroid: np.ndarray,
    energy_mean: float,
    centroid_mean: float,
    output_path: Path,
    title: str = "Stability Analysis",
    figsize: tuple = (14, 8),
    dpi: int = 150,
    formats: list = ["png"],
) -> None:
    """Plot dual temporal curves for stability scores (energy + spectral)."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize, sharex=True)
    
    # Top: Energy stability
    ax1.plot(times, energy, linewidth=1, color="blue", alpha=0.7, label="Energy")
    ax1.axhline(
        y=energy_mean,
        color="red",
        linestyle="--",
        linewidth=1,
        label=f"Mean: {energy_mean:.2e}",
        alpha=0.6
    )
    ax1.set_ylabel("Energy")
    ax1.set_title(f"{title} - Energy Stability")
    ax1.legend(loc="upper right")
    ax1.grid(True, alpha=0.25)
    
    # Bottom: Spectral stability
    ax2.plot(times, spectral_centroid, linewidth=1, color="green", alpha=0.7, label="Spectral Centroid")
    ax2.axhline(
        y=centroid_mean,
        color="red",
        linestyle="--",
        linewidth=1,
        label=f"Mean: {centroid_mean:.2f}",
        alpha=0.6
    )
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Spectral Centroid (bin)")
    ax2.set_title(f"{title} - Spectral Stability")
    ax2.legend(loc="upper right")
    ax2.grid(True, alpha=0.25)
    
    fig.tight_layout()
    save_figure(fig, output_path, formats, dpi)
    plt.close(fig)



# ----------------------------
# Visualizer wrapper (compat runner historique)
# ----------------------------


# ================================================================================
 NEW VISUALIZATION FUNCTIONS
# ================================================================================


def plot_spectral_rolloff(
    frequencies: np.ndarray,
    spectrum: np.ndarray,
    rolloff_frequency: float,
    rolloff_percent: float,
    output_path: Path,
    title: str = "Spectral Rolloff",
    figsize: tuple = (12, 6),
    dpi: int = 150,
    formats: list = ["png"]
) -> None:
    """
    Plot spectrum with rolloff frequency marker.
    
    Args:
        frequencies: Frequency bins
        spectrum: Magnitude spectrum
        rolloff_frequency: Rolloff frequency value
        rolloff_percent: Rolloff percentage (e.g., 0.85)
        output_path: Output file path
        title: Plot title
        figsize: Figure size
        dpi: Dots per inch
        formats: Output formats
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot spectrum
    ax.plot(frequencies, spectrum, linewidth=0.8, color="blue", alpha=0.7, label="Spectrum")
    
    # Mark rolloff frequency
    ax.axvline(rolloff_frequency, color="red", linestyle="--", linewidth=2, 
               label=f"{int(rolloff_percent*100)}% Rolloff = {rolloff_frequency:.1f} Hz")
    
    ax.set_title(title)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Magnitude")
    ax.legend(loc="upper right")
    ax.grid(True, alpha=0.25)
    
    fig.tight_layout()
    save_figure(fig, output_path, formats, dpi)
    plt.close(fig)


def plot_spectral_flux(
    times: np.ndarray,
    flux: np.ndarray,
    mean_flux: float,
    output_path: Path,
    title: str = "Spectral Flux",
    figsize: tuple = (12, 6),
    dpi: int = 150,
    formats: list = ["png"]
) -> None:
    """
    Plot spectral flux over time.
    
    Args:
        times: Time points
        flux: Spectral flux values
        mean_flux: Mean flux level
        output_path: Output file path
        title: Plot title
        figsize: Figure size
        dpi: Dots per inch
        formats: Output formats
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot flux
    ax.plot(times, flux, linewidth=0.8, color="purple", alpha=0.8, label="Spectral Flux")
    
    # Mark mean level
    ax.axhline(mean_flux, color="red", linestyle="--", linewidth=1.5, 
               label=f"Mean = {mean_flux:.4f}")
    
    ax.set_title(title)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Flux (arbitrary units)")
    ax.legend(loc="upper right")
    ax.grid(True, alpha=0.25)
    
    fig.tight_layout()
    save_figure(fig, output_path, formats, dpi)
    plt.close(fig)


def plot_high_order_statistics(
    histogram: np.ndarray,
    bin_centers: np.ndarray,
    normal_distribution: np.ndarray,
    mean: float,
    std: float,
    skewness: float,
    kurtosis: float,
    output_path: Path,
    title: str = "High-Order Statistics",
    figsize: tuple = (12, 6),
    dpi: int = 150,
    formats: list = ["png"]
) -> None:
    """
    Plot histogram with normal distribution overlay and statistics.
    
    Args:
        histogram: Histogram values
        bin_centers: Bin center positions
        normal_distribution: Fitted normal distribution
        mean: Mean value
        std: Standard deviation
        skewness: Skewness value
        kurtosis: Kurtosis value
        output_path: Output file path
        title: Plot title
        figsize: Figure size
        dpi: Dots per inch
        formats: Output formats
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot histogram
    ax.bar(bin_centers, histogram, width=(bin_centers[1]-bin_centers[0])*0.8, 
           alpha=0.6, color="blue", edgecolor="black", label="Data Distribution")
    
    # Overlay normal distribution
    ax.plot(bin_centers, normal_distribution, color="red", linewidth=2, 
            linestyle="--", label="Normal Distribution")
    
    # Add statistics text box
    stats_text = f"Mean: {mean:.6f}\nStd: {std:.6f}\nSkewness: {skewness:.4f}\nKurtosis: {kurtosis:.4f}"
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, 
            fontsize=10, verticalalignment="top",
            bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))
    
    ax.set_title(title)
    ax.set_xlabel("Amplitude")
    ax.set_ylabel("Probability Density")
    ax.legend(loc="upper right")
    ax.grid(True, alpha=0.25)
    
    fig.tight_layout()
    save_figure(fig, output_path, formats, dpi)
    plt.close(fig)


def plot_statistical_anomalies(
    histogram: np.ndarray,
    bin_centers: np.ndarray,
    normal_distribution: np.ndarray,
    outlier_indices: np.ndarray,
    outlier_values: np.ndarray,
    z_scores: np.ndarray,
    z_threshold: float,
    output_path: Path,
    title: str = "Statistical Anomalies",
    figsize: tuple = (12, 10),
    dpi: int = 150,
    formats: list = ["png"]
) -> None:
    """
    Plot dual subplot: histogram with outliers + Z-scores time series.
    
    Args:
        histogram: Histogram values
        bin_centers: Bin center positions
        normal_distribution: Fitted normal distribution
        outlier_indices: Indices of outlier samples
        outlier_values: Values of outliers
        z_scores: Z-score for each sample
        z_threshold: Threshold for outlier detection
        output_path: Output file path
        title: Plot title
        figsize: Figure size
        dpi: Dots per inch
        formats: Output formats
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize)
    
    # Top: Histogram with outliers marked
    ax1.bar(bin_centers, histogram, width=(bin_centers[1]-bin_centers[0])*0.8, 
            alpha=0.6, color="blue", edgecolor="black", label="Distribution")
    ax1.plot(bin_centers, normal_distribution, color="green", linewidth=2, 
             linestyle="--", label="Normal Fit")
    
    # Mark outliers
    if len(outlier_values) > 0:
        ax1.scatter(outlier_values, np.zeros_like(outlier_values), 
                   color="red", s=50, marker="x", label=f"Outliers (n={len(outlier_values)})", zorder=5)
    
    ax1.set_title(f"{title} - Distribution")
    ax1.set_xlabel("Amplitude")
    ax1.set_ylabel("Probability Density")
    ax1.legend()
    ax1.grid(True, alpha=0.25)
    
    # Bottom: Z-scores time series
    sample_indices = np.arange(len(z_scores))
    ax2.plot(sample_indices, z_scores, linewidth=0.5, color="blue", alpha=0.7, label="Z-Scores")
    ax2.axhline(z_threshold, color="red", linestyle="--", linewidth=1.5, label=f"Threshold = {z_threshold}")
    ax2.axhline(-z_threshold, color="red", linestyle="--", linewidth=1.5)
    
    # Mark outliers
    if len(outlier_indices) > 0:
        ax2.scatter(outlier_indices, z_scores[outlier_indices], 
                   color="red", s=20, marker="o", alpha=0.6, label="Outliers")
    
    ax2.set_title(f"{title} - Z-Scores")
    ax2.set_xlabel("Sample Index")
    ax2.set_ylabel("Z-Score")
    ax2.legend()
    ax2.grid(True, alpha=0.25)
    
    fig.tight_layout()
    save_figure(fig, output_path, formats, dpi)
    plt.close(fig)


def plot_chirp_detection(
    times: np.ndarray,
    frequencies: np.ndarray,
    spectrogram: np.ndarray,
    chirps: list,
    output_path: Path,
    title: str = "Chirp Detection",
    figsize: tuple = (12, 8),
    dpi: int = 150,
    formats: list = ["png"]
) -> None:
    """
    Plot spectrogram with detected chirps overlaid.
    
    Args:
        times: Time bins
        frequencies: Frequency bins
        spectrogram: STFT magnitude matrix
        chirps: List of detected chirps (dict with start_time, end_time, start_freq, end_freq)
        output_path: Output file path
        title: Plot title
        figsize: Figure size
        dpi: Dots per inch
        formats: Output formats
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot spectrogram
    magnitude_db = 20 * np.log10(np.maximum(spectrogram, 1e-10))
    im = ax.pcolormesh(times, frequencies, magnitude_db, cmap="viridis", shading="auto")
    
    # Overlay chirps
    for chirp in chirps:
        # Draw rectangle around chirp
        t_start = chirp['start_time']
        t_end = chirp['end_time']
        f_start = chirp['start_freq']
        f_end = chirp['end_freq']
        
        # Draw diagonal line showing chirp trend
        ax.plot([t_start, t_end], [f_start, f_end], 
               color="red", linewidth=2, linestyle="--", alpha=0.8)
        
        # Draw bounding box
        from matplotlib.patches import Rectangle
        rect_width = t_end - t_start
        rect_height = abs(f_end - f_start)
        rect_y = min(f_start, f_end)
        rect = Rectangle((t_start, rect_y), rect_width, rect_height,
                        linewidth=2, edgecolor="red", facecolor="none", alpha=0.6)
        ax.add_patch(rect)
    
    ax.set_title(f"{title} ({len(chirps)} chirps detected)")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Frequency (Hz)")
    
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label("Magnitude (dB)")
    
    fig.tight_layout()
    save_figure(fig, output_path, formats, dpi)
    plt.close(fig)


def plot_lsb_analysis(
    lsb_bits: np.ndarray,
    zero_runs: np.ndarray,
    one_runs: np.ndarray,
    transition_rate: float,
    output_path: Path,
    title: str = "LSB Analysis",
    figsize: tuple = (12, 10),
    dpi: int = 150,
    formats: list = ["png"]
) -> None:
    """
    Plot dual subplot: LSB bit sequence + run length histogram.
    
    Args:
        lsb_bits: LSB bit sequence
        zero_runs: Run lengths for zeros
        one_runs: Run lengths for ones
        transition_rate: Transition rate value
        output_path: Output file path
        title: Plot title
        figsize: Figure size
        dpi: Dots per inch
        formats: Output formats
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize)
    
    # Top: LSB bit sequence
    sample_indices = np.arange(len(lsb_bits))
    ax1.plot(sample_indices, lsb_bits, linewidth=0.5, color="blue", alpha=0.7)
    ax1.set_title(f"{title} - LSB Bit Sequence (Transition Rate: {transition_rate:.4f})")
    ax1.set_xlabel("Sample Index")
    ax1.set_ylabel("LSB Bit")
    ax1.set_ylim([-0.2, 1.2])
    ax1.grid(True, alpha=0.25)
    
    # Bottom: Run length histogram
    all_runs = np.concatenate([zero_runs, one_runs]) if len(zero_runs) > 0 and len(one_runs) > 0 else np.array([])
    
    if len(all_runs) > 0:
        bins = np.arange(0, min(50, np.max(all_runs) + 2))
        ax2.hist(zero_runs, bins=bins, alpha=0.6, color="blue", edgecolor="black", label="Zero Runs")
        ax2.hist(one_runs, bins=bins, alpha=0.6, color="red", edgecolor="black", label="One Runs")
        ax2.set_title(f"{title} - Run Length Distribution")
        ax2.set_xlabel("Run Length")
        ax2.set_ylabel("Count")
        ax2.legend()
        ax2.grid(True, alpha=0.25)
    else:
        ax2.text(0.5, 0.5, "No runs detected", ha="center", va="center", transform=ax2.transAxes)
    
    fig.tight_layout()
    save_figure(fig, output_path, formats, dpi)
    plt.close(fig)


def plot_parity_analysis(
    parity_bits: np.ndarray,
    run_lengths: np.ndarray,
    transition_rate: float,
    expected_transition_rate: float,
    output_path: Path,
    title: str = "Parity Analysis",
    figsize: tuple = (12, 10),
    dpi: int = 150,
    formats: list = ["png"]
) -> None:
    """
    Plot dual subplot: parity bits evolution + transition rate comparison.
    
    Args:
        parity_bits: Parity bit sequence
        run_lengths: Run length distribution
        transition_rate: Observed transition rate
        expected_transition_rate: Expected transition rate for random data
        output_path: Output file path
        title: Plot title
        figsize: Figure size
        dpi: Dots per inch
        formats: Output formats
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize)
    
    # Top: Parity bit evolution
    sample_indices = np.arange(len(parity_bits))
    ax1.plot(sample_indices, parity_bits, linewidth=0.5, color="purple", alpha=0.7)
    ax1.set_title(f"{title} - Parity Bits Evolution")
    ax1.set_xlabel("Sample Index")
    ax1.set_ylabel("Parity Bit")
    ax1.set_ylim([-0.2, 1.2])
    ax1.grid(True, alpha=0.25)
    
    # Bottom: Run length histogram + transition rate bar
    if len(run_lengths) > 0:
        bins = np.arange(0, min(50, np.max(run_lengths) + 2))
        ax2.hist(run_lengths, bins=bins, alpha=0.6, color="green", edgecolor="black")
        ax2.set_title(f"{title} - Run Length Distribution")
        ax2.set_xlabel("Run Length")
        ax2.set_ylabel("Count")
        ax2.grid(True, alpha=0.25)
        
        # Add transition rate comparison text
        anomaly = abs(transition_rate - expected_transition_rate)
        stats_text = f"Transition Rate: {transition_rate:.4f}\nExpected: {expected_transition_rate:.4f}\nAnomaly: {anomaly:.4f}"
        ax2.text(0.98, 0.98, stats_text, transform=ax2.transAxes, 
                fontsize=10, verticalalignment="top", horizontalalignment="right",
                bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))
    else:
        ax2.text(0.5, 0.5, "No runs detected", ha="center", va="center", transform=ax2.transAxes)
    
    fig.tight_layout()
    save_figure(fig, output_path, formats, dpi)
    plt.close(fig)


def plot_mutual_information(
    channel_names: list,
    mi_matrix: np.ndarray,
    mi_pairs: dict,
    output_path: Path,
    title: str = "Mutual Information",
    figsize: tuple = (10, 8),
    dpi: int = 150,
    formats: list = ["png"]
) -> None:
    """
    Plot mutual information as heatmap or bar chart.
    
    Args:
        channel_names: Names of channels
        mi_matrix: Mutual information matrix (NxN)
        mi_pairs: Dict of pairwise MI values
        output_path: Output file path
        title: Plot title
        figsize: Figure size
        dpi: Dots per inch
        formats: Output formats
    """
    n_channels = len(channel_names)
    
    if n_channels >= 3:
        # Use heatmap for 3+ channels
        fig, ax = plt.subplots(figsize=figsize)
        
        im = ax.imshow(mi_matrix, cmap="hot", aspect="auto")
        
        # Set ticks
        ax.set_xticks(np.arange(n_channels))
        ax.set_yticks(np.arange(n_channels))
        ax.set_xticklabels(channel_names, rotation=45, ha="right")
        ax.set_yticklabels(channel_names)
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label("Mutual Information (bits)")
        
        # Add text annotations
        for i in range(n_channels):
            for j in range(n_channels):
                if i != j:
                    text = ax.text(j, i, f"{mi_matrix[i, j]:.3f}",
                                 ha="center", va="center", color="white", fontsize=9)
        
        ax.set_title(title)
        
    else:
        # Use bar chart for 2 channels
        fig, ax = plt.subplots(figsize=figsize)
        
        pair_names = list(mi_pairs.keys())
        mi_values = list(mi_pairs.values())
        
        ax.bar(pair_names, mi_values, color="skyblue", edgecolor="black", alpha=0.8)
        ax.set_title(title)
        ax.set_ylabel("Mutual Information (bits)")
        ax.set_xlabel("Channel Pairs")
        ax.grid(True, alpha=0.25, axis="y")
        
        # Rotate labels if needed
        if len(pair_names) > 2:
            plt.xticks(rotation=45, ha="right")
    
    fig.tight_layout()
    save_figure(fig, output_path, formats, dpi)
    plt.close(fig)

class Visualizer:
    """
    Lightweight wrapper around functional plotters.

    Keeps the "engine uses a class, plotters are functions" design:
    - config stored here (figsize, dpi, formats)
    - zero analysis logic here
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config or {}
        self.figsize = tuple(self.config.get("figsize", [12, 8]))
        self.dpi = int(self.config.get("dpi", 150))
        self.formats = list(self.config.get("formats", ["png"]))
        # Per-method visualization options (pure rendering parameters)
        self.stft_cfg = dict(self.config.get("stft", {}) or {})

    # Basics
    def plot_waveform(self, signal, sample_rate, output_path, title):
        plot_waveform(signal, sample_rate, output_path, title, dpi=self.dpi, formats=self.formats)

    def plot_spectrum(self, freqs, magnitudes, output_path, title):
        plot_spectrum(freqs, magnitudes, output_path, title, dpi=self.dpi, formats=self.formats)

    def plot_multi_channel(self, channels, sample_rate, output_path, title):
        plot_multi_channel(channels, sample_rate, output_path, title, dpi=self.dpi, formats=self.formats)

    def plot_envelope(self, envelope, sample_rate, output_path, title):
        plot_envelope(envelope, sample_rate, output_path, title, dpi=self.dpi, formats=self.formats)

    def plot_autocorrelation(self, autocorr, sample_rate, output_path, title):
        plot_autocorrelation(autocorr, sample_rate, output_path, title, dpi=self.dpi, formats=self.formats)

    def plot_peaks(self, spectrum, peaks, output_path, title, xlabel="Bin", ylabel="Magnitude"):
        plot_peaks(spectrum, peaks, output_path, title, xlabel, ylabel, dpi=self.dpi, formats=self.formats)

    # Extended (delegate to module functions, keep config centralized)
    def plot_harmonics(self, frequencies, magnitudes, fundamental, harmonics, output_path):
        plot_harmonics(frequencies, magnitudes, fundamental, harmonics, output_path, self.figsize, self.dpi, self.formats)

    def plot_cepstrum(self, quefrency, cepstrum, peak_quefrency, output_path):
        plot_cepstrum(quefrency, cepstrum, peak_quefrency, output_path, self.figsize, self.dpi, self.formats)

    def plot_band_stability(self, times, bands_data, output_path):
        plot_band_stability(times, bands_data, output_path, self.figsize, self.dpi, self.formats)

    def plot_wavelet_scalogram(self, scalogram, scales, sample_rate, output_path):
        plot_wavelet_scalogram(scalogram, scales, sample_rate, output_path, self.figsize, self.dpi, self.formats)

    def plot_am_detection(self, time, envelope, mod_freqs, mod_spectrum, output_path):
        plot_am_detection(time, envelope, mod_freqs, mod_spectrum, output_path, self.figsize, self.dpi, self.formats)

    def plot_fm_detection(self, time, inst_freq, carrier, output_path):
        plot_fm_detection(time, inst_freq, carrier, output_path, self.figsize, self.dpi, self.formats)

    def plot_phase_analysis(self, time, phase, jumps, output_path):
        plot_phase_analysis(time, phase, jumps, output_path, self.figsize, self.dpi, self.formats)

    def plot_cross_correlation(self, lags, corr, pair_key, output_path):
        plot_cross_correlation(lags, corr, pair_key, output_path, self.figsize, self.dpi, self.formats)

    def plot_stft_spectrogram(self, frequencies, times, stft_matrix, sample_rate, output_path, title="STFT Spectrogram"):
        cmap = str(self.stft_cfg.get("colormap", "viridis"))
        vmin_db = float(self.stft_cfg.get("vmin_db", -80))
        vmax_db = float(self.stft_cfg.get("vmax_db", 0))
        gain_db = float(self.stft_cfg.get("gain_db", 0.0))
        plot_stft_spectrogram(
            frequencies,
            times,
            stft_matrix,
            sample_rate,
            output_path,
            title,
            self.figsize,
            self.dpi,
            self.formats,
            vmin=vmin_db,
            vmax=vmax_db,
            cmap=cmap,
            gain_db=gain_db,
        )

    def plot_cqt_spectrogram(self, frequencies, times, cqt_db, output_path, title="CQT Spectrogram"):
        plot_cqt_spectrogram(frequencies, times, cqt_db, output_path, title, self.figsize, self.dpi, self.formats)

    def plot_pulse_detection(self, waveform, envelope, pulse_positions, threshold_level, sample_rate, output_path, title="Pulse Detection"):
        plot_pulse_detection(waveform, envelope, pulse_positions, threshold_level, sample_rate, output_path, title, self.figsize, self.dpi, self.formats)

    def plot_spectral_centroid(self, frequencies, spectrum, centroid, output_path, title="Spectral Centroid"):
        plot_spectral_centroid(frequencies, spectrum, centroid, output_path, title, self.figsize, self.dpi, self.formats)

    def plot_spectral_bandwidth(self, frequencies, spectrum, centroid, bandwidth, lower_bound, upper_bound, output_path, title="Spectral Bandwidth"):
        plot_spectral_bandwidth(frequencies, spectrum, centroid, bandwidth, lower_bound, upper_bound, output_path, title, self.figsize, self.dpi, self.formats)

    def plot_temporal_curve(self, times, values, mean_level, output_path, title, ylabel):
        plot_temporal_curve(times, values, mean_level, output_path, title, ylabel, self.figsize, self.dpi, self.formats)

    def plot_stability_dual(self, times, energy, spectral_centroid, energy_mean, centroid_mean, output_path, title="Stability Analysis"):
        plot_stability_dual(times, energy, spectral_centroid, energy_mean, centroid_mean, output_path, title, self.figsize, self.dpi, self.formats)
    def plot_spectral_rolloff(self, frequencies, spectrum, rolloff_frequency, rolloff_percent, output_path, title="Spectral Rolloff"):
        plot_spectral_rolloff(frequencies, spectrum, rolloff_frequency, rolloff_percent, output_path, title, self.figsize, self.dpi, self.formats)

    def plot_spectral_flux(self, times, flux, mean_flux, output_path, title="Spectral Flux"):
        plot_spectral_flux(times, flux, mean_flux, output_path, title, self.figsize, self.dpi, self.formats)

    def plot_high_order_statistics(self, histogram, bin_centers, normal_distribution, mean, std, skewness, kurtosis, output_path, title="High-Order Statistics"):
        plot_high_order_statistics(histogram, bin_centers, normal_distribution, mean, std, skewness, kurtosis, output_path, title, self.figsize, self.dpi, self.formats)

    def plot_statistical_anomalies(self, histogram, bin_centers, normal_distribution, outlier_indices, outlier_values, z_scores, z_threshold, output_path, title="Statistical Anomalies"):
        plot_statistical_anomalies(histogram, bin_centers, normal_distribution, outlier_indices, outlier_values, z_scores, z_threshold, output_path, title, self.figsize, self.dpi, self.formats)

    def plot_chirp_detection(self, times, frequencies, spectrogram, chirps, output_path, title="Chirp Detection"):
        plot_chirp_detection(times, frequencies, spectrogram, chirps, output_path, title, self.figsize, self.dpi, self.formats)

    def plot_lsb_analysis(self, lsb_bits, zero_runs, one_runs, transition_rate, output_path, title="LSB Analysis"):
        plot_lsb_analysis(lsb_bits, zero_runs, one_runs, transition_rate, output_path, title, self.figsize, self.dpi, self.formats)

    def plot_parity_analysis(self, parity_bits, run_lengths, transition_rate, expected_transition_rate, output_path, title="Parity Analysis"):
        plot_parity_analysis(parity_bits, run_lengths, transition_rate, expected_transition_rate, output_path, title, self.figsize, self.dpi, self.formats)

    def plot_mutual_information(self, channel_names, mi_matrix, mi_pairs, output_path, title="Mutual Information"):
        plot_mutual_information(channel_names, mi_matrix, mi_pairs, output_path, title, self.figsize, self.dpi, self.formats)