"""
Main orchestrator for the analysis pipeline.
"""

from pathlib import Path
from typing import Dict, Any

from .context import AnalysisContext
from .results import ResultsAggregator
from .registry import get_registry


class AnalysisRunner:
    """
    Main pipeline orchestrator.
    
    Loads configuration, prepares context, executes methods, collects results.
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.registry = get_registry()
        self.results = ResultsAggregator()
    
    def run(self, audio_path: Path, output_path: Path) -> None:
        """
        Execute the complete analysis pipeline.
        
        Args:
            audio_path: Path to audio file
            output_path: Output directory for results
        """
        pass
    
    def _load_audio(self, audio_path: Path) -> AnalysisContext:
        """Load audio and create analysis context."""
        pass
    
    def _execute_analyses(self, context: AnalysisContext) -> None:
        """Execute all configured analysis methods."""
        pass
    
    def _export_results(self, output_path: Path) -> None:
        """Export results and configuration."""
        pass
