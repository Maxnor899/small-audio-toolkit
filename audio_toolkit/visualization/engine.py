"""
Visualization orchestration engine.

Responsible for generating all plots (basic + analysis-based)
using functional plotting utilities.
"""

from pathlib import Path
import numpy as np

from .plots import (
    plot_waveform,
    plot_spectrum,
    plot_multi_channel,
    plot_envelope,
    plot_autocorrelation,
    plot_peaks,
    plot_am_detection,
    plot_fm_detection,
    plot_phase_analysis,
    plot_band_stability,
    plot_stft_spectrogram,
)

from .plots_extended import (
    plot_harmonics,
    plot_cepstrum,
    plot_wavelet_scalogram,
    plot_cross_correlation,
)


class VisualizationEngine:
    def __init__(self, config: dict):
        self.enabled = config.get("enabled", False)
        self.figsize = tuple(config.get("figsize", [12, 8]))
        self.dpi = config.get("dpi", 150)
        self.formats = config.get("formats", ["png"])

    # ------------------------------------------------------------
    # BASIC VISUALIZATIONS
    # ------------------------------------------------------------

    def generate_basic(self, context, output_path: Path) -> None:
        if not self.enabled:
            return

        viz_dir = output_path / "visualizations"
        viz_dir.mkdir(parents=True, exist_ok=True)

        for channel, audio in context.audio_data.items():
            max_samples = min(len(audio), 100_000)

            plot_waveform(
                audio[:max_samples],
                context.sample_rate,
                viz_dir / f"waveform_{channel}",
                f"Waveform - {channel}",
            )

            spectrum = np.fft.rfft(audio)
            freqs = np.fft.rfftfreq(len(audio), 1 / context.sample_rate)

            plot_spectrum(
                freqs,
                np.abs(spectrum),
                viz_dir / f"spectrum_{channel}",
                f"Spectrum - {channel}",
            )

        if len(context.audio_data) > 1:
            sample_data = {
                ch: audio[:50_000]
                for ch, audio in context.audio_data.items()
            }

            plot_multi_channel(
                sample_data,
                context.sample_rate,
                viz_dir / "multi_channel_overview",
                "All Channels Overview",
            )

    # ------------------------------------------------------------
    # ANALYSIS VISUALIZATIONS
    # ------------------------------------------------------------

    def generate_from_results(self, results, context, output_path: Path) -> None:
        if not self.enabled:
            return

        viz_dir = output_path / "visualizations"
        viz_dir.mkdir(parents=True, exist_ok=True)

        results_dict = results.to_dict()

        for category, methods in results_dict.get("results", {}).items():
            for method_result in methods:
                method = method_result["method"]
                viz_data = method_result.get("visualization_data", {})

                if not viz_data:
                    continue

                self._dispatch_method(
                    method, viz_data, context, viz_dir
                )

    # ------------------------------------------------------------
    # METHOD DISPATCH
    # ------------------------------------------------------------

    def _dispatch_method(self, method, viz_data, context, viz_dir: Path):

        # TEMPORAL
        if method == "envelope":
            for ch, env in viz_data.items():
                plot_envelope(
                    env,
                    context.sample_rate,
                    viz_dir / f"envelope_{ch}",
                    f"Envelope - {ch}",
                )

        elif method == "autocorrelation":
            for ch, data in viz_data.items():
                plot_autocorrelation(
                    data,
                    context.sample_rate,
                    viz_dir / f"autocorrelation_{ch}",
                    f"Autocorrelation - {ch}",
                )

        # SPECTRAL
        elif method == "fft_global":
            for ch, d in viz_data.items():
                plot_spectrum(
                    d["frequencies"],
                    d["magnitudes"],
                    viz_dir / f"fft_global_{ch}",
                    f"FFT Spectrum - {ch}",
                    figsize=self.figsize,
                    dpi=self.dpi,
                    formats=self.formats,
                )

        elif method == "peak_detection":
            for ch, d in viz_data.items():
                plot_peaks(
                    d["spectrum"],
                    d["peaks"],
                    viz_dir / f"peaks_{ch}",
                    f"Spectral Peaks - {ch}",
                    xlabel="Frequency Bin",
                    ylabel="Magnitude",
                    figsize=self.figsize,
                    dpi=self.dpi,
                    formats=self.formats,
                )

        elif method == "harmonic_analysis":
            for ch, d in viz_data.items():
                plot_harmonics(
                    d["frequencies"],
                    d["spectrum"],
                    d["fundamental"],
                    d["harmonics"],
                    viz_dir / f"harmonics_{ch}",
                    self.figsize,
                    self.dpi,
                    self.formats,
                )

        elif method == "cepstrum":
            for ch, d in viz_data.items():
                plot_cepstrum(
                    d["quefrency"],
                    d["cepstrum"],
                    d["peak_quefrency"],
                    viz_dir / f"cepstrum_{ch}",
                    self.figsize,
                    self.dpi,
                    self.formats,
                )

        # TIME-FREQUENCY
        elif method == "band_stability":
            for ch, d in viz_data.items():
                plot_band_stability(
                    d["times"],
                    d["bands_data"],
                    viz_dir / f"band_stability_{ch}",
                    self.figsize,
                    self.dpi,
                    self.formats,
                )

        elif method == "stft":
            for ch, d in viz_data.items():
                plot_stft_spectrogram(
                    d["frequencies"],
                    d["times"],
                    d["stft_matrix"],
                    context.sample_rate,
                    viz_dir / f"stft_{ch}",
                    f"STFT Spectrogram - {ch}",
                    self.figsize,
                    self.dpi,
                    self.formats,
                )

        elif method == "wavelet":
            for ch, d in viz_data.items():
                plot_wavelet_scalogram(
                    d["scalogram"],
                    d["scales"],
                    context.sample_rate,
                    viz_dir / f"wavelet_{ch}",
                    self.figsize,
                    self.dpi,
                    self.formats,
                )

        # MODULATION
        elif method == "am_detection":
            for ch, d in viz_data.items():
                plot_am_detection(
                    d["time"],
                    d["envelope"],
                    d["modulation_frequencies"],
                    d["modulation_spectrum"],
                    viz_dir / f"am_detection_{ch}",
                    self.figsize,
                    self.dpi,
                    self.formats,
                )

        elif method == "fm_detection":
            for ch, d in viz_data.items():
                plot_fm_detection(
                    d["time"],
                    d["instantaneous_frequency"],
                    d["carrier_frequency"],
                    viz_dir / f"fm_detection_{ch}",
                    self.figsize,
                    self.dpi,
                    self.formats,
                )

        elif method == "phase_analysis":
            for ch, d in viz_data.items():
                plot_phase_analysis(
                    d["time"],
                    d["phase"],
                    d["jumps"],
                    viz_dir / f"phase_analysis_{ch}",
                    self.figsize,
                    self.dpi,
                    self.formats,
                )

        # INTER-CHANNEL
        elif method == "cross_correlation":
            for pair, d in viz_data.items():
                plot_cross_correlation(
                    d["lags"],
                    d["correlation"],
                    pair,
                    viz_dir / f"cross_corr_{pair}",
                    self.figsize,
                    self.dpi,
                    self.formats,
                )

        elif method == "lr_difference":
            # L-R difference gets both waveform and spectrum
            d = viz_data.get("lr_difference", {})
            if d:
                # Waveform
                max_samples = min(len(d["waveform"]), 100_000)
                plot_waveform(
                    d["waveform"][:max_samples],
                    context.sample_rate,
                    viz_dir / "lr_difference_waveform",
                    "L-R Difference Waveform",
                    figsize=self.figsize,
                    dpi=self.dpi,
                    formats=self.formats,
                )
                
                # Spectrum
                plot_spectrum(
                    d["frequencies"],
                    d["spectrum"],
                    viz_dir / "lr_difference_spectrum",
                    "L-R Difference Spectrum",
                    figsize=self.figsize,
                    dpi=self.dpi,
                    formats=self.formats,
                )