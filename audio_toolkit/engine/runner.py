"""
Main orchestrator for the analysis pipeline.
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
from ..utils.logging import get_logger

logger = get_logger(__name__)


class AnalysisRunner:
    """
    Main pipeline orchestrator.
    
    Loads configuration, prepares context, executes methods, collects results.
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
        
        context = self._load_audio(audio_path)
        
        if self.visualizer is not None:
            self._generate_basic_visualizations(context, output_path)
        
        self._execute_analyses(context)
        
        self._export_results(output_path, audio_path)
        
        logger.info("=" * 80)
        logger.info("Analysis pipeline completed")
        logger.info("=" * 80)
    
    def _load_audio(self, audio_path: Path) -> AnalysisContext:
        """
        Load audio and create analysis context.
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            AnalysisContext ready for analysis
        """
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
        """
        Generate basic visualizations for all channels.
        
        Args:
            context: Analysis context
            output_path: Output directory
        """
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
        """
        Execute all configured analysis methods.
        
        Args:
            context: AnalysisContext
        """
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
    
    def _export_results(self, output_path: Path, audio_path: Path) -> None:
        """
        Export results and configuration.
        
        Args:
            output_path: Output directory
            audio_path: Original audio file path
        """
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