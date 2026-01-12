"""
Analysis results structure and aggregation.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from pathlib import Path
import json
from datetime import datetime

from ..utils.logging import get_logger

logger = get_logger(__name__)


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
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)


class ResultsAggregator:
    """
    Aggregates results from all analysis methods.
    """
    
    def __init__(self):
        self.results: Dict[str, List[AnalysisResult]] = {}
        self.metadata: Dict[str, Any] = {}
        self.timestamp = datetime.now().isoformat()
    
    def add_result(self, category: str, result: AnalysisResult) -> None:
        """
        Add a result to the specified category.
        
        Args:
            category: Analysis category (temporal, spectral, etc.)
            result: AnalysisResult instance
        """
        if category not in self.results:
            self.results[category] = []
        
        self.results[category].append(result)
        logger.debug(f"Added result for {category}/{result.method}")
    
    def set_metadata(self, metadata: Dict[str, Any]) -> None:
        """
        Set execution metadata.
        
        Args:
            metadata: Metadata dictionary (audio info, config, etc.)
        """
        self.metadata = metadata
    
    def get_results(self) -> Dict[str, Any]:
        """
        Get all results as dictionary.
        
        Returns:
            Complete results structure
        """
        results_dict = {
            'timestamp': self.timestamp,
            'metadata': self.metadata,
            'results': {}
        }
        
        for category, category_results in self.results.items():
            results_dict['results'][category] = [
                result.to_dict() for result in category_results
            ]
        
        return results_dict
    
    def export_json(self, output_path: Path, include_viz_data: bool = False) -> None:
        """
        Export all results to JSON file.
        
        Args:
            output_path: Output file path
            include_viz_data: Include visualization_data in export
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        results = self.get_results()
        
        if not include_viz_data:
            for category in results.get('results', {}).values():
                for result in category:
                    if 'visualization_data' in result:
                        del result['visualization_data']
        
        logger.info(f"Exporting results to: {output_path}")
        
        try:
            with open(output_path, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            
            logger.info(f"Results exported successfully ({output_path.stat().st_size} bytes)")
            
        except Exception as e:
            logger.error(f"Failed to export results: {e}")
            raise
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get summary statistics of results.
        
        Returns:
            Summary dictionary with counts and categories
        """
        summary = {
            'total_categories': len(self.results),
            'total_methods': sum(len(results) for results in self.results.values()),
            'categories': {}
        }
        
        for category, category_results in self.results.items():
            summary['categories'][category] = {
                'method_count': len(category_results),
                'methods': [result.method for result in category_results]
            }
        
        return summary