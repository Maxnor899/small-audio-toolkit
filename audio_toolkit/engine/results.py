"""
Analysis results structure and aggregation.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class AnalysisResult:
    """
    Structured result from an analysis method.
    """
    method: str
    measurements: Dict[str, Any]
    metrics: Optional[Dict[str, Any]] = None
    anomaly_score: Optional[float] = None
    visualization_data: Optional[Dict[str, Any]] = None


class ResultsAggregator:
    """
    Aggregates results from all analysis methods.
    """
    
    def __init__(self):
        self.results: Dict[str, List[AnalysisResult]] = {}
    
    def add_result(self, category: str, result: AnalysisResult) -> None:
        """Add a result to the specified category."""
        pass
    
    def export_json(self, path: str) -> None:
        """Export all results to JSON."""
        pass
