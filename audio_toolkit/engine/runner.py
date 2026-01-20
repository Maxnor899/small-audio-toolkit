# audio_toolkit/engine/runner.py
"""
Main orchestrator for the analysis pipeline with complete visualization support.
"""

from pathlib import Path
from typing import Dict, Any
import numpy as np

# IMPORTANT: importing analyses triggers method registration (side-effect by design)
from .. import analyses  # noqa: F401

from .context import AnalysisContext
from .results import ResultsAggregator, AnalysisResult
from .registry import get_registry
from ..audio.loader import AudioLoader
from ..audio.channels import ChannelProcessor
from ..audio.preprocessing import Preprocessor
from ..config.loader import ConfigLoader
from ..visualization.plots import Visualizer
from ..utils.logging import get_logger

logger = get_logger(__name__)


class AnalysisRunner:
    """
    Main pipeline orchestrator with complete visualization support.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.registry = get_registry()
        self.results = ResultsAggregator()
        self.context = None

        viz_config = config.get("visualization", {})
        if viz_config.get("enabled", False):
            self.visualizer = Visualizer(viz_config)
        else:
            self.visualizer = None

    def run(self, audio_path: Path, output_path: Path) -> None:
        logger.info("=" * 80)
        logger.info("Starting analysis pipeline")
        logger.info("=" * 80)

        output_path = Path(output_path)
        output_path.mkdir(parents=True, exist_ok=True)

        self.context = self._load_audio(audio_path)

        if self.visualizer is not None:
            self._generate_basic_visualizations(self.context, output_path)

        self._execute_analyses(self.context)

        if self.visualizer is not None:
            self._generate_analysis_visualizations(output_path)

        self._export_results(output_path, audio_path)

        logger.info("=" * 80)
        logger.info("Analysis pipeline completed")
        logger.info("=" * 80)

    def _load_audio(self, audio_path: Path) -> AnalysisContext:
        """Load audio and create analysis context."""
        logger.info(f"Loading audio: {audio_path}")

        audio_data, sample_rate = AudioLoader.load(audio_path)
        audio_info = AudioLoader.get_audio_info(audio_path)

        requested_channels = self.config["channels"]["analyze"]
        logger.info(f"Extracting channels: {requested_channels}")

        channel_data = ChannelProcessor.extract_channels(audio_data, requested_channels)

        preprocessing_config = self.config.get("preprocessing", {})
        channel_data = self._apply_preprocessing(channel_data, sample_rate, preprocessing_config)

        segments = self._compute_segments(channel_data, sample_rate, preprocessing_config)

        metadata = {
            "audio_file": str(audio_path),
            "audio_info": audio_info,
            "sample_rate": sample_rate,
            "channels": requested_channels,
            "preprocessing": preprocessing_config,
            "config_version": self.config.get("version", "unknown"),
        }

        self.results.set_metadata(metadata)

        context = AnalysisContext(
            audio_data=channel_data,
            sample_rate=sample_rate,
            segments=segments,
            metadata=metadata,
        )

        logger.info(f"Context created: {len(channel_data)} channels, {len(segments)} segments")
        return context

    def _apply_preprocessing(
        self,
        channel_data: Dict[str, Any],
        sample_rate: int,
        preprocessing_config: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Apply preprocessing steps to channels."""
        if not preprocessing_config:
            return channel_data

        normalize_config = preprocessing_config.get("normalize", {})
        if isinstance(normalize_config, dict) and normalize_config.get("enabled", False):
            method = normalize_config.get("method", "rms")
            target_level = normalize_config.get("target_level", -20.0)

            logger.info(f"Applying {method.upper()} normalization (target: {target_level} dB)")

            for channel_name, audio in channel_data.items():
                if method == "rms":
                    channel_data[channel_name] = Preprocessor.normalize_rms(audio, target_level)
                elif method == "lufs":
                    channel_data[channel_name] = Preprocessor.normalize_lufs(audio, sample_rate, target_level)

        return channel_data

    def _compute_segments(
        self,
        channel_data: Dict[str, Any],
        sample_rate: int,
        preprocessing_config: Dict[str, Any],
    ) -> list:
        """Compute temporal segments if configured."""
        segmentation_config = preprocessing_config.get("segmentation", {})

        if not isinstance(segmentation_config, dict) or not segmentation_config.get("enabled", False):
            first_channel = list(channel_data.values())[0]
            return [(0, len(first_channel))]

        method = segmentation_config.get("method", "energy")
        duration = segmentation_config.get("segment_duration", 1.0)

        logger.info(f"Computing segments: method={method}, duration={duration}s")

        first_channel = list(channel_data.values())[0]
        segments = Preprocessor.segment_audio(first_channel, sample_rate, method, duration)
        return segments

    def _generate_basic_visualizations(self, context: AnalysisContext, output_path: Path) -> None:
        """Generate basic visualizations for all channels."""
        viz_dir = output_path / "visualizations"
        viz_dir.mkdir(exist_ok=True)

        logger.info("Generating basic visualizations...")

        for channel_name, audio_data in context.audio_data.items():
            # AMELIORATION : Waveform avec limite
            waveform_path = viz_dir / f"waveform_{channel_name}"
            max_samples = min(len(audio_data), 100000)

            self.visualizer.plot_waveform(
                audio_data[:max_samples],
                context.sample_rate,
                waveform_path,
                f"Waveform - {channel_name}",
            )

            # FIX: Spectrum avec limite aussi
            max_samples_spectrum = min(len(audio_data), 100000)
            spectrum = np.fft.rfft(audio_data[:max_samples_spectrum])
            freqs = np.fft.rfftfreq(max_samples_spectrum, 1 / context.sample_rate)
            spectrum_path = viz_dir / f"spectrum_{channel_name}"

            self.visualizer.plot_spectrum(
                freqs,
                np.abs(spectrum),
                spectrum_path,
                f"Spectrum - {channel_name}",
            )

        if len(context.audio_data) > 1:
            multi_path = viz_dir / "multi_channel_overview"
            sample_data = {name: audio[:min(len(audio), 50000)] for name, audio in context.audio_data.items()}
            self.visualizer.plot_multi_channel(
                sample_data,
                context.sample_rate,
                multi_path,
                "All Channels Overview",
            )

        logger.info(f"Basic visualizations saved to: {viz_dir}")

    def _execute_analyses(self, context: AnalysisContext) -> None:
        """Execute all configured analysis methods."""
        analyses_config = self.config.get("analyses", {})

        for category, category_config in analyses_config.items():
            if not isinstance(category_config, dict):
                continue

            if not category_config.get("enabled", False):
                continue

            methods = category_config.get("methods", [])
            if not methods:
                continue

            for method_config in methods:
                self._execute_method(context, category, method_config)

    def _execute_method(self, context: AnalysisContext, category: str, method_config: Dict) -> None:
        method_name = method_config.get("name")
        if not method_name:
            logger.warning(f"Method in '{category}' missing 'name', skipping")
            return

        registration = self.registry.get_method(method_name)
        if registration is None:
            logger.warning(f"Method '{method_name}' not found in registry, skipping")
            return

        params = method_config.get("params", {})
        merged_params = {**registration.default_params, **params}

        logger.info(f"Executing: {category}/{method_name}")

        try:
            result = registration.function(context, merged_params)
            self.results.add_result(category, result)
            
            # FIX: Vérifier si l'analyse a retourné une erreur
            if 'error' in result.measurements:
                logger.error(
                    f"  {category}/{method_name} failed: {result.measurements['error']}"
                )
            else:
                logger.info(f"Completed: {category}/{method_name}")

        except Exception as e:
            logger.error(f"Failed to execute {category}/{method_name}: {e}")

            error_result = AnalysisResult(
                method=method_name,
                measurements={"error": str(e)},
                metrics={"execution_failed": True},
            )
            self.results.add_result(category, error_result)

    def _generate_analysis_visualizations(self, output_path: Path) -> None:
        """Generate visualizations for all analysis results."""
        logger.info("Generating analysis visualizations...")

        viz_dir = output_path / "visualizations"
        viz_dir.mkdir(exist_ok=True, parents=True)

        results_dict = self.results.get_results()

        for category, methods in results_dict.get("results", {}).items():
            for method_result in methods:
                method = method_result["method"]
                viz_data = method_result.get("visualization_data", {})

                if not viz_data:
                    continue

                try:
                    self._generate_method_visualization(method, viz_data, viz_dir)
                except Exception as e:
                    logger.warning(f"Failed to generate visualization for {method}: {e}")

        logger.info(f"Analysis visualizations saved to: {viz_dir}")

    def _generate_method_visualization(self, method: str, viz_data: Dict, viz_dir: Path) -> None:
        """Generate visualization for a specific method."""
        
        # FIX: Vérifier explicitement si viz_data est vide/None
        if not viz_data:
            logger.debug(f"No visualization data for method '{method}', skipping")
            return

        # ========================================
        # TEMPORAL
        # ========================================
        if method == "envelope":
            for channel, envelope in viz_data.items():
                self.visualizer.plot_envelope(
                    envelope,
                    self.context.sample_rate,
                    viz_dir / f"envelope_{channel}",
                    f"Amplitude Envelope - {channel}",
                )

        elif method == "autocorrelation":
            for channel, autocorr in viz_data.items():
                self.visualizer.plot_autocorrelation(
                    autocorr,
                    self.context.sample_rate,
                    viz_dir / f"autocorrelation_{channel}",
                    f"Autocorrelation - {channel}",
                )

        elif method == "pulse_detection":
            for channel, data in viz_data.items():
                if all(k in data for k in ["waveform", "envelope", "pulse_positions", "threshold_level"]):
                    self.visualizer.plot_pulse_detection(
                        np.asarray(data["waveform"]),
                        np.asarray(data["envelope"]),
                        np.asarray(data["pulse_positions"]),
                        float(data["threshold_level"]),
                        self.context.sample_rate,
                        viz_dir / f"pulse_detection_{channel}",
                        f"Pulse Detection - {channel}",
                    )

        # ========================================
        # SPECTRAL
        # ========================================
        elif method == "fft_global":
            for channel, data in viz_data.items():
                if "frequencies" in data and "magnitudes" in data:
                    self.visualizer.plot_spectrum(
                        np.asarray(data["frequencies"]),
                        np.asarray(data["magnitudes"]),
                        viz_dir / f"fft_global_{channel}",
                        f"FFT Spectrum - {channel}",
                    )

        elif method == "peak_detection":
            for channel, data in viz_data.items():
                if "spectrum" in data and "peaks" in data:
                    self.visualizer.plot_peaks(
                        np.asarray(data["spectrum"]),
                        np.asarray(data["peaks"]),
                        viz_dir / f"peaks_{channel}",
                        f"Spectral Peaks - {channel}",
                        "Frequency Bin",
                        "Magnitude",
                    )

        elif method == "harmonic_analysis":
            for channel, data in viz_data.items():
                if all(k in data for k in ["frequencies", "spectrum", "fundamental", "harmonics"]):
                    self.visualizer.plot_harmonics(
                        np.asarray(data["frequencies"]),
                        np.asarray(data["spectrum"]),
                        float(data["fundamental"]),
                        list(data["harmonics"]),
                        viz_dir / f"harmonics_{channel}",
                    )

        elif method == "cepstrum":
            for channel, data in viz_data.items():
                if all(k in data for k in ["quefrency", "cepstrum", "peak_quefrency"]):
                    self.visualizer.plot_cepstrum(
                        np.asarray(data["quefrency"]),
                        np.asarray(data["cepstrum"]),
                        float(data["peak_quefrency"]),
                        viz_dir / f"cepstrum_{channel}",
                    )

        elif method == "spectral_centroid":
            for channel, data in viz_data.items():
                if all(k in data for k in ["frequencies", "spectrum", "centroid"]):
                    self.visualizer.plot_spectral_centroid(
                        np.asarray(data["frequencies"]),
                        np.asarray(data["spectrum"]),
                        float(data["centroid"]),
                        viz_dir / f"spectral_centroid_{channel}",
                        f"Spectral Centroid - {channel}",
                    )

        elif method == "spectral_bandwidth":
            for channel, data in viz_data.items():
                if all(k in data for k in ["frequencies", "spectrum", "centroid", "bandwidth", "lower_bound", "upper_bound"]):
                    self.visualizer.plot_spectral_bandwidth(
                        np.asarray(data["frequencies"]),
                        np.asarray(data["spectrum"]),
                        float(data["centroid"]),
                        float(data["bandwidth"]),
                        float(data["lower_bound"]),
                        float(data["upper_bound"]),
                        viz_dir / f"spectral_bandwidth_{channel}",
                        f"Spectral Bandwidth - {channel}",
                    )

        # ========================================
        # TIME-FREQUENCY
        # ========================================
        elif method == "stft":
            for channel, data in viz_data.items():
                if all(k in data for k in ["frequencies", "times", "stft_matrix"]):
                    from ..visualization.plots import plot_stft_spectrogram
                    plot_stft_spectrogram(
                        np.asarray(data["frequencies"]),
                        np.asarray(data["times"]),
                        np.asarray(data["stft_matrix"]),
                        self.context.sample_rate,
                        viz_dir / f"stft_{channel}",
                        f"STFT Spectrogram - {channel}",
                        figsize=self.visualizer.figsize,
                        dpi=self.visualizer.dpi,
                        formats=self.visualizer.formats,
                    )

        elif method == "cqt":
            for channel, data in viz_data.items():
                if all(k in data for k in ["frequencies", "times", "cqt_db"]):
                    from ..visualization.plots import plot_cqt_spectrogram
                    plot_cqt_spectrogram(
                        np.asarray(data["frequencies"]),
                        np.asarray(data["times"]),
                        np.asarray(data["cqt_db"]),
                        viz_dir / f"cqt_{channel}",
                        f"CQT Spectrogram - {channel}",
                        figsize=self.visualizer.figsize,
                        dpi=self.visualizer.dpi,
                        formats=self.visualizer.formats,
                    )

        elif method == "band_stability":
            for channel, data in viz_data.items():
                if "times" in data and "bands_data" in data:
                    from ..visualization.plots import plot_band_stability
                    plot_band_stability(
                        np.asarray(data["times"]),
                        data["bands_data"],
                        viz_dir / f"band_stability_{channel}",
                        figsize=self.visualizer.figsize,
                        dpi=self.visualizer.dpi,
                        formats=self.visualizer.formats,
                    )

        elif method == "wavelet":
            for channel, data in viz_data.items():
                if all(k in data for k in ["scalogram", "scales"]):
                    self.visualizer.plot_wavelet_scalogram(
                        np.asarray(data["scalogram"]),
                        np.asarray(data["scales"]),
                        self.context.sample_rate,
                        viz_dir / f"wavelet_{channel}",
                    )

        # ========================================
        # MODULATION
        # ========================================
        elif method == "am_detection":
            for channel, data in viz_data.items():
                if all(k in data for k in ["time", "envelope", "modulation_frequencies", "modulation_spectrum"]):
                    self.visualizer.plot_am_detection(
                        np.asarray(data["time"]),
                        np.asarray(data["envelope"]),
                        np.asarray(data["modulation_frequencies"]),
                        np.asarray(data["modulation_spectrum"]),
                        viz_dir / f"am_{channel}",
                    )

        elif method == "fm_detection":
            for channel, data in viz_data.items():
                if all(k in data for k in ["time", "instantaneous_frequency", "carrier_frequency"]):
                    self.visualizer.plot_fm_detection(
                        np.asarray(data["time"]),
                        np.asarray(data["instantaneous_frequency"]),
                        float(data["carrier_frequency"]),
                        viz_dir / f"fm_{channel}",
                    )

        elif method == "phase_analysis":
            for channel, data in viz_data.items():
                if all(k in data for k in ["time", "phase", "jumps"]):
                    self.visualizer.plot_phase_analysis(
                        np.asarray(data["time"]),
                        np.asarray(data["phase"]),
                        np.asarray(data["jumps"]),
                        viz_dir / f"phase_{channel}",
                    )

        # ========================================
        # INTER-CHANNEL
        # ========================================
        elif method == "cross_correlation":
            for pair_key, data in viz_data.items():
                if "lags" in data and "correlation" in data:
                    self.visualizer.plot_cross_correlation(
                        np.asarray(data["lags"]),
                        np.asarray(data["correlation"]),
                        pair_key,
                        viz_dir / f"cross_corr_{pair_key}",
                    )

        elif method == "lr_difference":
            data = viz_data.get("lr_difference", {})
            if data:
                if "waveform" in data:
                    max_samples = min(len(data["waveform"]), 100_000)
                    self.visualizer.plot_waveform(
                        np.asarray(data["waveform"][:max_samples]),
                        self.context.sample_rate,
                        viz_dir / "lr_difference_waveform",
                        "L-R Difference Waveform",
                    )

                if "frequencies" in data and "spectrum" in data:
                    self.visualizer.plot_spectrum(
                        np.asarray(data["frequencies"]),
                        np.asarray(data["spectrum"]),
                        viz_dir / "lr_difference_spectrum",
                        "L-R Difference Spectrum",
                    )

        # ========================================
        # INFORMATION
        # ========================================
        elif method == "local_entropy":
            for channel, data in viz_data.items():
                if all(k in data for k in ["times", "entropies", "mean_level"]):
                    self.visualizer.plot_temporal_curve(
                        np.asarray(data["times"]),
                        np.asarray(data["entropies"]),
                        float(data["mean_level"]),
                        viz_dir / f"local_entropy_{channel}",
                        f"Local Entropy Evolution - {channel}",
                        "Entropy (bits)",
                    )

        # ========================================
        # META_ANALYSIS
        # ========================================
        elif method == "stability_scores":
            for channel, data in viz_data.items():
                if all(k in data for k in ["times", "energy", "spectral_centroid", "energy_mean", "centroid_mean"]):
                    self.visualizer.plot_stability_dual(
                        np.asarray(data["times"]),
                        np.asarray(data["energy"]),
                        np.asarray(data["spectral_centroid"]),
                        float(data["energy_mean"]),
                        float(data["centroid_mean"]),
                        viz_dir / f"stability_scores_{channel}",
                        f"Stability Analysis - {channel}",
                    )


        # ========================================
        # SPECTRAL NEW
        # ========================================
        elif method == "spectral_rolloff":
            for channel, data in viz_data.items():
                if all(k in data for k in ["frequencies", "spectrum", "rolloff_frequency", "rolloff_percent"]):
                    self.visualizer.plot_spectral_rolloff(
                        np.asarray(data["frequencies"]),
                        np.asarray(data["spectrum"]),
                        float(data["rolloff_frequency"]),
                        float(data["rolloff_percent"]),
                        viz_dir / f"spectral_rolloff_{channel}",
                        f"Spectral Rolloff - {channel}",
                    )

        elif method == "spectral_flux":
            for channel, data in viz_data.items():
                if all(k in data for k in ["times", "flux", "mean_flux"]):
                    self.visualizer.plot_spectral_flux(
                        np.asarray(data["times"]),
                        np.asarray(data["flux"]),
                        float(data["mean_flux"]),
                        viz_dir / f"spectral_flux_{channel}",
                        f"Spectral Flux - {channel}",
                    )

        # ========================================
        # MODULATION (PHASE 3B)
        # ========================================
        elif method == "chirp_detection":
            for channel, data in viz_data.items():
                if all(k in data for k in ["times", "frequencies", "spectrogram", "chirps"]):
                    self.visualizer.plot_chirp_detection(
                        np.asarray(data["times"]),
                        np.asarray(data["frequencies"]),
                        np.asarray(data["spectrogram"]),
                        list(data["chirps"]),
                        viz_dir / f"chirp_detection_{channel}",
                        f"Chirp Detection - {channel}",
                    )

        # ========================================
        # INFORMATION (PHASE 3B)
        # ========================================
        elif method == "mutual_information":
            # mutual_information has global data, not per-channel
            if "channel_names" in viz_data and "mi_matrix" in viz_data and "mi_pairs" in viz_data:
                self.visualizer.plot_mutual_information(
                    list(viz_data["channel_names"]),
                    np.asarray(viz_data["mi_matrix"]),
                    dict(viz_data["mi_pairs"]),
                    viz_dir / "mutual_information",
                    "Mutual Information Between Channels",
                )

        # ========================================
        # STEGANOGRAPHY (PHASES 3A+3B)
        # ========================================
        elif method == "lsb_analysis":
            for channel, data in viz_data.items():
                if all(k in data for k in ["lsb_bits", "zero_runs", "one_runs", "transition_rate"]):
                    self.visualizer.plot_lsb_analysis(
                        np.asarray(data["lsb_bits"]),
                        np.asarray(data["zero_runs"]),
                        np.asarray(data["one_runs"]),
                        float(data["transition_rate"]),
                        viz_dir / f"lsb_analysis_{channel}",
                        f"LSB Analysis - {channel}",
                    )

        elif method == "parity_analysis":
            for channel, data in viz_data.items():
                if all(k in data for k in ["parity_bits", "run_lengths", "transition_rate", "expected_transition_rate"]):
                    self.visualizer.plot_parity_analysis(
                        np.asarray(data["parity_bits"]),
                        np.asarray(data["run_lengths"]),
                        float(data["transition_rate"]),
                        float(data["expected_transition_rate"]),
                        viz_dir / f"parity_analysis_{channel}",
                        f"Parity Analysis - {channel}",
                    )

        elif method == "statistical_anomalies":
            for channel, data in viz_data.items():
                if all(k in data for k in ["histogram", "bin_centers", "normal_distribution", "outlier_indices", "outlier_values", "z_scores", "z_threshold"]):
                    self.visualizer.plot_statistical_anomalies(
                        np.asarray(data["histogram"]),
                        np.asarray(data["bin_centers"]),
                        np.asarray(data["normal_distribution"]),
                        np.asarray(data["outlier_indices"]),
                        np.asarray(data["outlier_values"]),
                        np.asarray(data["z_scores"]),
                        float(data["z_threshold"]),
                        viz_dir / f"statistical_anomalies_{channel}",
                        f"Statistical Anomalies - {channel}",
                    )

        # ========================================
        # META_ANALYSIS (PHASE 3A)
        # ========================================
        elif method == "high_order_statistics":
            for channel, data in viz_data.items():
                if all(k in data for k in ["histogram", "bin_centers", "normal_distribution", "mean", "std", "skewness", "kurtosis"]):
                    self.visualizer.plot_high_order_statistics(
                        np.asarray(data["histogram"]),
                        np.asarray(data["bin_centers"]),
                        np.asarray(data["normal_distribution"]),
                        float(data["mean"]),
                        float(data["std"]),
                        float(data["skewness"]),
                        float(data["kurtosis"]),
                        viz_dir / f"high_order_statistics_{channel}",
                        f"High-Order Statistics - {channel}",
                    )

    def _export_results(self, output_path: Path, audio_path: Path) -> None:
        """Export results and configuration."""
        output_config = self.config.get("output", {})

        if output_config.get("save_raw_data", True):
            results_file = output_path / "results.json"
            self.results.export_json(results_file, include_viz_data=False)

        if output_config.get("save_config", True):
            config_file = output_path / "config_used.json"
            logger.info(f"Saving configuration to: {config_file}")
            import json
            with open(config_file, "w") as f:
                json.dump(self.config, f, indent=2)

        summary = self.results.get_summary()
        logger.info(
            f"Executed {summary['total_methods']} methods across {summary['total_categories']} categories"
        )
