"""
Extended plotting utilities for analysis results.
"""

import matplotlib.pyplot as plt
import numpy as np


def _save(fig, output_path, dpi, formats):
    fig.tight_layout()
    for fmt in formats:
        fig.savefig(str(output_path) + f".{fmt}", dpi=dpi)
    plt.close(fig)


def plot_harmonics(freqs, spectrum, fundamental, harmonics,
                   output_path, figsize, dpi, formats):
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(freqs, spectrum)

    ax.axvline(fundamental, color="r", linestyle="--", label="Fundamental")
    for h in harmonics:
        ax.axvline(h, color="g", alpha=0.5)

    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Magnitude")
    ax.set_title("Harmonic Analysis")
    ax.legend()

    _save(fig, output_path, dpi, formats)


def plot_cepstrum(quefrency, cepstrum, peak_quefrency,
                  output_path, figsize, dpi, formats):
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(quefrency, cepstrum)
    ax.axvline(peak_quefrency, color="r", linestyle="--")

    ax.set_xlabel("Quefrency (s)")
    ax.set_ylabel("Amplitude")
    ax.set_title("Cepstrum")

    _save(fig, output_path, dpi, formats)


def plot_wavelet_scalogram(scalogram, scales, sample_rate,
                           output_path, figsize, dpi, formats):
    fig, ax = plt.subplots(figsize=figsize)
    ax.imshow(
        scalogram,
        aspect="auto",
        origin="lower",
        extent=[0, scalogram.shape[1] / sample_rate, scales[0], scales[-1]]
    )

    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Scale")
    ax.set_title("Wavelet Scalogram")

    _save(fig, output_path, dpi, formats)


def plot_cross_correlation(lags, correlation, pair_key,
                           output_path, figsize, dpi, formats):
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(lags, correlation)

    ax.set_xlabel("Lag")
    ax.set_ylabel("Correlation")
    ax.set_title(f"Cross-correlation {pair_key}")

    _save(fig, output_path, dpi, formats)
