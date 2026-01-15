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
    magnitude_db = 20 * np.log10(magnitude + 1e-12)

    im = ax.pcolormesh(
        times,
        frequencies,
        magnitude_db,
        shading="auto",
        cmap="viridis",
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
# Visualizer wrapper (compat runner historique)
# ----------------------------

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
        plot_stft_spectrogram(frequencies, times, stft_matrix, sample_rate, output_path, title, self.figsize, self.dpi, self.formats)

    def plot_cqt_spectrogram(self, frequencies, times, cqt_db, output_path, title="CQT Spectrogram"):
        plot_cqt_spectrogram(frequencies, times, cqt_db, output_path, title, self.figsize, self.dpi, self.formats)
