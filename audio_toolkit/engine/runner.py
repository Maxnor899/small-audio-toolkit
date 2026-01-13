"""
Main orchestrator for the analysis pipeline with complete visualization support.
"""

from pathlib import Path
from typing import Dict, Any
import numpy as np

from .context import AnalysisContext
from .results import ResultsAggregator, AnalysisResult
from .registry import get_registry
from ..audio.loader import AudioLoader
from ..audio.channels import ChannelProcessor
from ..audio.preprocessing import Preprocessor
from ..config.loader import ConfigLoader
from ..visualization.plots import Visualizer
from ..visualization import plots_extended as pext
from ..utils.logging import get_logger

logger = get_logger(__name__)


class AnalysisRunner:
    """
    Main pipeline orchestrator with complete visualization support.
    
    Loads configuration, prepares context, executes methods, collects results, generates visualizations.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize runner with configuration.
        
        Args:
            config: Validated configuration dictionary
        """
        self.config = config
        self.registry = get_registry()
        self.results = ResultsAggregator()
        self.context = None
        
        viz_config = config.get('visualization', {})
        if viz_config.get('enabled', False):
            self.visualizer = Visualizer(viz_config)
        else:
            self.visualizer = None
    
    def run(self, audio_path: Path, output_path: Path) -> None:
        """
        Execute the complete analysis pipeline.
        
        Args:
            audio_path: Path to audio file
            output_path: Output directory for results
        """
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
        
        requested_channels = self.config['channels']['analyze']
        logger.info(f"Extracting channels: {requested_channels}")
        
        channel_data = ChannelProcessor.extract_channels(audio_data, requested_channels)
        
        preprocessing_config = self.config.get('preprocessing', {})
        channel_data = self._apply_preprocessing(channel_data, sample_rate, preprocessing_config)
        
        segments = self._compute_segments(channel_data, sample_rate, preprocessing_config)
        
        metadata = {
            'audio_file': str(audio_path),
            'audio_info': audio_info,
            'sample_rate': sample_rate,
            'channels': requested_channels,
            'preprocessing': preprocessing_config,
            'config_version': self.config.get('version', 'unknown')
        }
        
        self.results.set_metadata(metadata)
        
        context = AnalysisContext(
            audio_data=channel_data,
            sample_rate=sample_rate,
            segments=segments,
            metadata=metadata
        )
        
        logger.info(f"Context created: {len(channel_data)} channels, {len(segments)} segments")
        
        return context
    
    def _apply_preprocessing(
        self,
        channel_data: Dict[str, Any],
        sample_rate: int,
        preprocessing_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply preprocessing steps to channels."""
        
        if not preprocessing_config:
            return channel_data
        
        normalize_config = preprocessing_config.get('normalize', {})
        if normalize_config.get('enabled', False):
            method = normalize_config.get('method', 'rms')
            target_level = normalize_config.get('target_level', -20.0)
            
            logger.info(f"Applying {method.upper()} normalization (target: {target_level} dB)")
            
            for channel_name, audio in channel_data.items():
                if method == 'rms':
                    channel_data[channel_name] = Preprocessor.normalize_rms(audio, target_level)
                elif method == 'lufs':
                    channel_data[channel_name] = Preprocessor.normalize_lufs(
                        audio, sample_rate, target_level
                    )
        
        return channel_data
    
    def _compute_segments(
        self,
        channel_data: Dict[str, Any],
        sample_rate: int,
        preprocessing_config: Dict[str, Any]
    ) -> list:
        """Compute temporal segments if configured."""
        
        segmentation_config = preprocessing_config.get('segmentation', {})
        
        if not segmentation_config.get('enabled', False):
            first_channel = list(channel_data.values())[0]
            return [(0, len(first_channel))]
        
        method = segmentation_config.get('method', 'energy')
        duration = segmentation_config.get('segment_duration', 1.0)
        
        logger.info(f"Computing segments: method={method}, duration={duration}s")
        
        first_channel = list(channel_data.values())[0]
        segments = Preprocessor.segment_audio(first_channel, sample_rate, method, duration)
        
        return segments
    
    def _generate_basic_visualizations(
        self,
        context: AnalysisContext,
        output_path: Path
    ) -> None:
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
                f"Waveform - {channel_name}"
            )
            
            spectrum = np.fft.rfft(audio_data)
            freqs = np.fft.rfftfreq(len(audio_data), 1 / context.sample_rate)
            spectrum_path = viz_dir / f"spectrum_{channel_name}"
            self.visualizer.plot_spectrum(
                freqs,
                np.abs(spectrum),
                spectrum_path,
                f"Spectrum - {channel_name}"
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
                "All Channels Overview"
            )
        
        logger.info(f"Basic visualizations saved to: {viz_dir}")
    
    def _execute_analyses(self, context: AnalysisContext) -> None:
        """Execute all configured analysis methods."""
        analyses_config = self.config.get('analyses', {})
        
        for category, category_config in analyses_config.items():
            if not isinstance(category_config, dict):
                continue
            
            if not category_config.get('enabled', False):
                logger.info(f"Category '{category}' is disabled, skipping")
                continue
            
            methods = category_config.get('methods', [])
            logger.info(f"Executing {len(methods)} methods in category '{category}'")
            
            for method_config in methods:
                self._execute_method(category, method_config, context)
    
    def _execute_method(
        self,
        category: str,
        method_config: Dict[str, Any],
        context: AnalysisContext
    ) -> None:
        """Execute a single analysis method."""
        
        method_name = method_config.get('name')
        if not method_name:
            logger.warning(f"Method in '{category}' missing 'name', skipping")
            return
        
        registration = self.registry.get_method(method_name)
        
        if registration is None:
            logger.warning(f"Method '{method_name}' not found in registry, skipping")
            return
        
        params = method_config.get('params', {})
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
                measurements={'error': str(e)},
                metrics={'execution_failed': True}
            )
            self.results.add_result(category, error_result)
    
    def _generate_analysis_visualizations(self, output_path: Path) -> None:
        """Generate visualizations for all analysis results."""
        logger.info("Generating analysis visualizations...")
        
        viz_dir = output_path / 'visualizations'
        viz_dir.mkdir(exist_ok=True, parents=True)
        
        viz_config = self.config.get('visualization', {})
        figsize = tuple(viz_config.get('figsize', [12, 8]))
        dpi = viz_config.get('dpi', 150)
        formats = viz_config.get('formats', ['png'])
        
        results_dict = self.results.to_dict()
        
        for category, methods in results_dict.get('results', {}).items():
            for method_result in methods:
                method = method_result['method']
                viz_data = method_result.get('visualization_data', {})
                
                if not viz_data:
                    continue
                
                try:
                    self._generate_method_visualization(
                        method, viz_data, viz_dir, figsize, dpi, formats
                    )
                except Exception as e:
                    logger.warning(f"Failed to generate visualization for {method}: {e}")
        
        logger.info(f"Analysis visualizations saved to: {viz_dir}")
    
    def _generate_method_visualization(
        self,
        method: str,
        viz_data: Dict,
        viz_dir: Path,
        figsize: tuple,
        dpi: int,
        formats: list
    ) -> None:
        """Generate visualization for a specific method."""
        
        # TEMPORAL
        if method == 'envelope':
            for channel, envelope in viz_data.items():
                self.visualizer.plot_envelope(
                    envelope, self.context.sample_rate,
                    viz_dir / f'envelope_{channel}',
                    f'Amplitude Envelope - {channel}'
                )
        
        elif method == 'autocorrelation':
            for channel, autocorr in viz_data.items():
                self.visualizer.plot_autocorrelation(
                    autocorr, self.context.sample_rate,
                    viz_dir / f'autocorrelation_{channel}',
                    f'Autocorrelation - {channel}'
                )
        
        elif method == 'pulse_detection':
            for channel, data in viz_data.items():
                if 'signal' in data and 'pulse_locations' in data:
                    time = np.arange(len(data['signal'])) / self.context.sample_rate
                    pext.plot_pulses(
                        time, data['signal'], data['pulse_locations'],
                        viz_dir / f'pulses_{channel}',
                        figsize, dpi, formats
                    )
        
        # SPECTRAL
        elif method == 'peak_detection':
            for channel, data in viz_data.items():
                if all(k in data for k in ['frequencies', 'spectrum', 'peaks']):
                    self.visualizer.plot_peaks(
                        data['spectrum'], data['peaks'],
                        viz_dir / f'peaks_{channel}',
                        f'Spectral Peaks - {channel}',
                        'Frequency Bin', 'Magnitude'
                    )
        
        elif method == 'harmonic_analysis':
            for channel, data in viz_data.items():
                if all(k in data for k in ['frequencies', 'spectrum', 'fundamental', 'harmonics']):
                    pext.plot_harmonics(
                        data['frequencies'], data['spectrum'],
                        data['fundamental'], data['harmonics'],
                        viz_dir / f'harmonics_{channel}',
                        figsize, dpi, formats
                    )
        
        elif method == 'cepstrum':
            for channel, data in viz_data.items():
                if all(k in data for k in ['quefrency', 'cepstrum', 'peak_quefrency']):
                    pext.plot_cepstrum(
                        data['quefrency'], data['cepstrum'], data['peak_quefrency'],
                        viz_dir / f'cepstrum_{channel}',
                        figsize, dpi, formats
                    )
        
        # TIME-FREQUENCY
        elif method == 'band_stability':
            for channel, data in viz_data.items():
                if 'times' in data and 'bands' in data:
                    pext.plot_band_stability(
                        data['times'], data['bands'],
                        viz_dir / f'band_stability_{channel}',
                        figsize, dpi, formats
                    )
        
        elif method == 'wavelet':
            for channel, data in viz_data.items():
                if all(k in data for k in ['scalogram', 'scales']):
                    pext.plot_wavelet_scalogram(
                        data['scalogram'], data['scales'], self.context.sample_rate,
                        viz_dir / f'wavelet_{channel}',
                        figsize, dpi, formats
                    )
        
        # MODULATION
        elif method == 'am_detection':
            for channel, data in viz_data.items():
                if all(k in data for k in ['time', 'envelope', 'mod_freqs', 'mod_spectrum']):
                    pext.plot_am_detection(
                        data['time'], data['envelope'],
                        data['mod_freqs'], data['mod_spectrum'],
                        viz_dir / f'am_{channel}',
                        figsize, dpi, formats
                    )
        
        elif method == 'fm_detection':
            for channel, data in viz_data.items():
                if all(k in data for k in ['time', 'inst_freq', 'carrier']):
                    pext.plot_fm_detection(
                        data['time'], data['inst_freq'], data['carrier'],
                        viz_dir / f'fm_{channel}',
                        figsize, dpi, formats
                    )
        
        elif method == 'phase_analysis':
            for channel, data in viz_data.items():
                if all(k in data for k in ['time', 'phase', 'jumps']):
                    pext.plot_phase_analysis(
                        data['time'], data['phase'], data['jumps'],
                        viz_dir / f'phase_{channel}',
                        figsize, dpi, formats
                    )
        
        # INTER-CHANNEL
        elif method == 'cross_correlation':
            for pair_key, data in viz_data.items():
                if 'lags' in data and 'correlation' in data:
                    pext.plot_cross_correlation(
                        data['lags'], data['correlation'], pair_key,
                        viz_dir / f'cross_corr_{pair_key}',
                        figsize, dpi, formats
                    )
        
        elif method == 'lr_difference':
            if 'frequencies' in viz_data and all(k in viz_data for k in ['left', 'right', 'difference']):
                pext.plot_lr_difference(
                    viz_data['frequencies'],
                    viz_data['left'], viz_data['right'], viz_data['difference'],
                    viz_dir / 'lr_difference',
                    figsize, dpi, formats
                )
        
        elif method == 'phase_difference':
            for pair_key, data in viz_data.items():
                if all(k in data for k in ['frequencies', 'phase_diff', 'coherence']):
                    pext.plot_phase_difference(
                        data['frequencies'], data['phase_diff'], data['coherence'], pair_key,
                        viz_dir / f'phase_diff_{pair_key}',
                        figsize, dpi, formats
                    )
        
        # INFORMATION
        elif method == 'local_entropy':
            for channel, data in viz_data.items():
                if 'times' in data and 'entropy' in data:
                    pext.plot_local_entropy(
                        data['times'], data['entropy'],
                        viz_dir / f'local_entropy_{channel}',
                        figsize, dpi, formats
                    )
        
        # STEGANOGRAPHY
        elif method == 'lsb_analysis':
            for channel, data in viz_data.items():
                if 'lsb_bits' in data:
                    pext.plot_lsb_analysis(
                        data['lsb_bits'],
                        viz_dir / f'lsb_{channel}',
                        figsize, dpi, formats
                    )
        
        elif method == 'quantization_noise':
            for channel, data in viz_data.items():
                if 'frequencies' in data and 'noise_spectrum' in data:
                    pext.plot_quantization_noise(
                        data['frequencies'], data['noise_spectrum'],
                        viz_dir / f'quant_noise_{channel}',
                        figsize, dpi, formats
                    )
        
        elif method == 'signal_residual':
            for channel, data in viz_data.items():
                if all(k in data for k in ['time', 'signal', 'residual']):
                    pext.plot_signal_residual(
                        data['time'], data['signal'], data['residual'],
                        viz_dir / f'residual_{channel}',
                        figsize, dpi, formats
                    )
        
        # META-ANALYSIS
        elif method == 'inter_segment_comparison':
            for channel, data in viz_data.items():
                if 'distance_matrix' in data:
                    pext.plot_segment_comparison(
                        data['distance_matrix'],
                        viz_dir / f'segments_{channel}',
                        figsize, dpi, formats
                    )
        
        elif method == 'segment_clustering':
            for channel, data in viz_data.items():
                if 'features_2d' in data and 'labels' in data:
                    pext.plot_clustering(
                        data['features_2d'], data['labels'],
                        viz_dir / f'clustering_{channel}',
                        figsize, dpi, formats
                    )
        
        elif method == 'stability_scores':
            for channel, data in viz_data.items():
                if all(k in data for k in ['times', 'energy', 'spectral']):
                    pext.plot_stability_scores(
                        data['times'], data['energy'], data['spectral'],
                        viz_dir / f'stability_{channel}',
                        figsize, dpi, formats
                    )
    
    def _export_results(self, output_path: Path, audio_path: Path) -> None:
        """Export results and configuration."""
        output_config = self.config.get('output', {})
        
        if output_config.get('save_raw_data', True):
            results_file = output_path / 'results.json'
            self.results.export_json(results_file, include_viz_data=False)
        
        if output_config.get('save_config', True):
            config_file = output_path / 'config_used.json'
            logger.info(f"Saving configuration to: {config_file}")
            import json
            with open(config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        
        summary = self.results.get_summary()
        logger.info(f"Executed {summary['total_methods']} methods across {summary['total_categories']} categories")