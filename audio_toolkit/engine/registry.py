"""
Global registry for analysis methods.
"""

from typing import Callable, Dict, Any, Optional
from dataclasses import dataclass

from .context import AnalysisContext
from .results import AnalysisResult


@dataclass
class MethodRegistration:
    """
    Registration entry for an analysis method.
    """
    identifier: str
    category: str
    function: Callable[[AnalysisContext, Dict[str, Any]], AnalysisResult]
    description: str
    default_params: Dict[str, Any]


class MethodRegistry:
    """
    Global registry for all analysis methods.
    """
    
    def __init__(self):
        self._methods: Dict[str, MethodRegistration] = {}
    
    def register(
        self,
        identifier: str,
        category: str,
        function: Callable,
        description: str = "",
        default_params: Optional[Dict[str, Any]] = None
    ) -> None:
        """Register a new analysis method."""
        pass
    
    def get_method(self, identifier: str) -> Optional[MethodRegistration]:
        """Retrieve a registered method."""
        pass
    
    def get_by_category(self, category: str) -> list:
        """Get all methods in a category."""
        pass


_global_registry = MethodRegistry()


def register_method(
    identifier: str,
    category: str,
    function: Callable,
    description: str = "",
    default_params: Optional[Dict[str, Any]] = None
) -> None:
    """Register a method in the global registry."""
    _global_registry.register(identifier, category, function, description, default_params)


def get_registry() -> MethodRegistry:
    """Get the global registry instance."""
    return _global_registry
