"""
Main orchestrator for the analysis pipeline with complete visualization support.
"""

from pathlib import Path
from typing import Dict, Any
import numpy as np

# ✅ IMPORTANT: importing analyses triggers method registration (side-effect by design)
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
        if normalize_config.get("enabled", False):
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

        if not segmentation_config.get("enabled", False):
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
            waveform_path = viz_dir / f"waveform_{channel_name}"
            max_samples = min(len(audio_data), 100000)

            self.visualizer.plot_waveform(
                audio_data[:max_samples],
                context.sample_rate,
                waveform_path,
                f"Waveform - {channel_name}",
            )

            spectrum = np.fft.rfft(audio_data)
            freqs = np.fft.rfftfreq(len(audio_data), 1 / context.sample_rate)
            spectrum_path = viz_dir / f"spectrum_{channel_name}"

            self.visualizer.plot_spectrum(
                freqs,
                np.abs(spectrum),
                spectrum_path,
                f"Spectrum - {channel_name}",
            )

        if len(context.audio_data) > 1:
            multi_path = viz_dir / "multi_channel_overview"
            sample_data = {
                name: audio[:min(len(audio), 50000)]
                for name, audio in context.audio_data.items()
            }
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

        # ✅ ResultsAggregator provides get_results() (and now also to_dict())
        results_dict = self.results.get_results()

        viz_config = self.config.get("visualization", {})
        formats = viz_config.get("formats", ["png"])
        dpi = viz_config.get("dpi", 150)

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

        # ========================================
        # SPECTRAL
        # ========================================
        
        # 🔧 CORRECTION #1 : Ajout de fft_global
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

        # ========================================
        # TIME-FREQUENCY
        # ========================================
        
        # 🔧 CORRECTION #2 : Ajout de stft
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
        
        # 🔧 CORRECTION #3 : Correction de band_stability (clé 'bands_data' au lieu de 'bands')
        elif method == "band_stability":
            for channel, data in viz_data.items():
                if "times" in data and "bands_data" in data:  # ← CORRECTION ICI
                    from ..visualization.plots import plot_band_stability
                    plot_band_stability(
                        np.asarray(data["times"]),
                        data["bands_data"],  # ← CORRECTION ICI
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
        
        # 🔧 CORRECTION #4 : Correction de am_detection (clés 'modulation_frequencies'/'modulation_spectrum')
        elif method == "am_detection":
            for channel, data in viz_data.items():
                if all(k in data for k in ["time", "envelope", "modulation_frequencies", "modulation_spectrum"]):  # ← CORRECTION ICI
                    self.visualizer.plot_am_detection(
                        np.asarray(data["time"]),
                        np.asarray(data["envelope"]),
                        np.asarray(data["modulation_frequencies"]),  # ← CORRECTION ICI
                        np.asarray(data["modulation_spectrum"]),      # ← CORRECTION ICI
                        viz_dir / f"am_{channel}",
                    )

        # 🔧 CORRECTION #5 : Correction de fm_detection (clés 'instantaneous_frequency'/'carrier_frequency')
        elif method == "fm_detection":
            for channel, data in viz_data.items():
                if all(k in data for k in ["time", "instantaneous_frequency", "carrier_frequency"]):  # ← CORRECTION ICI
                    self.visualizer.plot_fm_detection(
                        np.asarray(data["time"]),
                        np.asarray(data["instantaneous_frequency"]),  # ← CORRECTION ICI
                        float(data["carrier_frequency"]),             # ← CORRECTION ICI
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
        
        # 🔧 CORRECTION #6 : Ajout de lr_difference
        elif method == "lr_difference":
            data = viz_data.get("lr_difference", {})
            if data:
                # Waveform
                if "waveform" in data:
                    max_samples = min(len(data["waveform"]), 100_000)
                    self.visualizer.plot_waveform(
                        np.asarray(data["waveform"][:max_samples]),
                        self.context.sample_rate,
                        viz_dir / "lr_difference_waveform",
                        "L-R Difference Waveform",
                    )
                
                # Spectrum
                if "frequencies" in data and "spectrum" in data:
                    self.visualizer.plot_spectrum(
                        np.asarray(data["frequencies"]),
                        np.asarray(data["spectrum"]),
                        viz_dir / "lr_difference_spectrum",
                        "L-R Difference Spectrum",
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