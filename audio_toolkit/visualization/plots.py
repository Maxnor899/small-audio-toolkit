"""
Visualization functions for analysis results.
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

from ..utils.logging import get_logger

logger = get_logger(__name__)


class Visualizer:
    """
    Generates visualizations from analysis results.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize visualizer with configuration.
        
        Args:
            config: Visualization configuration
        """
        self.config = config
        self.dpi = config.get("dpi", 300)
        self.figsize = config.get("figsize", [12, 8])
        self.formats = config.get("formats", ["png"])
    
    def plot_waveform(
        self,
        audio: np.ndarray,
        sample_rate: int,
        output_path: Path,
        title: str = "Waveform"
    ) -> None:
        """
        Plot time-domain waveform.
        
        Args:
            audio: Audio data
            sample_rate: Sample rate in Hz
            output_path: Output file path (without extension)
            title: Plot title
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        time = np.arange(len(audio)) / sample_rate
        
        ax.plot(time, audio, linewidth=0.5, color='blue')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Amplitude')
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
        
        self.save_figure(fig, output_path)
        plt.close(fig)
        
        logger.info(f"Saved waveform plot: {output_path}")
    
    def plot_spectrum(
        self,
        frequencies: np.ndarray,
        magnitudes: np.ndarray,
        output_path: Path,
        title: str = "Spectrum",
        log_scale: bool = True
    ) -> None:
        """
        Plot frequency spectrum.
        
        Args:
            frequencies: Frequency array (Hz)
            magnitudes: Magnitude array
            output_path: Output file path (without extension)
            title: Plot title
            log_scale: Use logarithmic scale for magnitude
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        if log_scale:
            magnitudes_db = 20 * np.log10(magnitudes + 1e-10)
            ax.plot(frequencies, magnitudes_db, linewidth=1, color='green')
            ax.set_ylabel('Magnitude (dB)')
        else:
            ax.plot(frequencies, magnitudes, linewidth=1, color='green')
            ax.set_ylabel('Magnitude')
        
        ax.set_xlabel('Frequency (Hz)')
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
        
        self.save_figure(fig, output_path)
        plt.close(fig)
        
        logger.info(f"Saved spectrum plot: {output_path}")
    
    def plot_spectrogram(
        self,
        spectrogram: np.ndarray,
        sample_rate: int,
        hop_length: int,
        output_path: Path,
        title: str = "Spectrogram"
    ) -> None:
        """
        Plot time-frequency spectrogram.
        
        Args:
            spectrogram: Spectrogram array (frequency x time)
            sample_rate: Sample rate in Hz
            hop_length: Hop length in samples
            output_path: Output file path (without extension)
            title: Plot title
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        magnitude_db = 20 * np.log10(np.abs(spectrogram) + 1e-10)
        
        extent = [
            0,
            spectrogram.shape[1] * hop_length / sample_rate,
            0,
            sample_rate / 2
        ]
        
        im = ax.imshow(
            magnitude_db,
            aspect='auto',
            origin='lower',
            cmap='viridis',
            extent=extent
        )
        
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Frequency (Hz)')
        ax.set_title(title)
        
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Magnitude (dB)')
        
        self.save_figure(fig, output_path)
        plt.close(fig)
        
        logger.info(f"Saved spectrogram plot: {output_path}")
    
    def plot_envelope(
        self,
        envelope: np.ndarray,
        sample_rate: int,
        output_path: Path,
        title: str = "Amplitude Envelope"
    ) -> None:
        """
        Plot amplitude envelope.
        
        Args:
            envelope: Envelope data
            sample_rate: Sample rate in Hz
            output_path: Output file path (without extension)
            title: Plot title
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        time = np.arange(len(envelope)) / sample_rate
        
        ax.plot(time, envelope, linewidth=1, color='red')
        ax.fill_between(time, 0, envelope, alpha=0.3, color='red')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Amplitude')
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
        
        self.save_figure(fig, output_path)
        plt.close(fig)
        
        logger.info(f"Saved envelope plot: {output_path}")
    
    def plot_autocorrelation(
        self,
        autocorr: np.ndarray,
        sample_rate: int,
        output_path: Path,
        title: str = "Autocorrelation"
    ) -> None:
        """
        Plot autocorrelation function.
        
        Args:
            autocorr: Autocorrelation data
            sample_rate: Sample rate in Hz
            output_path: Output file path (without extension)
            title: Plot title
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        lags = np.arange(len(autocorr)) / sample_rate
        
        ax.plot(lags, autocorr, linewidth=1, color='purple')
        ax.set_xlabel('Lag (s)')
        ax.set_ylabel('Correlation')
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='k', linestyle='--', alpha=0.3)
        
        self.save_figure(fig, output_path)
        plt.close(fig)
        
        logger.info(f"Saved autocorrelation plot: {output_path}")
    
    def plot_multi_channel(
        self,
        channels: Dict[str, np.ndarray],
        sample_rate: int,
        output_path: Path,
        title: str = "Multi-Channel Waveforms"
    ) -> None:
        """
        Plot multiple channels in subplots.
        
        Args:
            channels: Dictionary of channel_name -> audio_data
            sample_rate: Sample rate in Hz
            output_path: Output file path (without extension)
            title: Plot title
        """
        n_channels = len(channels)
        fig, axes = plt.subplots(n_channels, 1, figsize=(self.figsize[0], self.figsize[1] * n_channels / 2))
        
        if n_channels == 1:
            axes = [axes]
        
        for ax, (channel_name, audio_data) in zip(axes, channels.items()):
            time = np.arange(len(audio_data)) / sample_rate
            ax.plot(time, audio_data, linewidth=0.5)
            ax.set_ylabel(f'{channel_name}')
            ax.grid(True, alpha=0.3)
        
        axes[-1].set_xlabel('Time (s)')
        fig.suptitle(title)
        fig.tight_layout()
        
        self.save_figure(fig, output_path)
        plt.close(fig)
        
        logger.info(f"Saved multi-channel plot: {output_path}")
    
    def plot_peaks(
        self,
        data: np.ndarray,
        peaks: np.ndarray,
        output_path: Path,
        title: str = "Peak Detection",
        x_label: str = "Sample",
        y_label: str = "Amplitude"
    ) -> None:
        """
        Plot data with detected peaks marked.
        
        Args:
            data: Signal data
            peaks: Peak indices
            output_path: Output file path (without extension)
            title: Plot title
            x_label: X-axis label
            y_label: Y-axis label
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        ax.plot(data, linewidth=1, color='blue', label='Signal')
        ax.plot(peaks, data[peaks], 'rx', markersize=10, label='Peaks')
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title(title)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        self.save_figure(fig, output_path)
        plt.close(fig)
        
        logger.info(f"Saved peaks plot: {output_path}")
    
    def save_figure(self, fig: plt.Figure, output_path: Path) -> None:
        """
        Save figure in configured formats.
        
        Args:
            fig: Matplotlib figure
            output_path: Output path without extension
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        for fmt in self.formats:
            file_path = output_path.with_suffix(f'.{fmt}')
            fig.savefig(file_path, dpi=self.dpi, bbox_inches='tight')
            logger.debug(f"Saved {fmt}: {file_path}")