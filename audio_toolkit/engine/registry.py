"""
Global registry for analysis methods.
"""

from typing import Callable, Dict, Any, Optional, List
from dataclasses import dataclass

from .context import AnalysisContext
from .results import AnalysisResult
from ..utils.logging import get_logger

logger = get_logger(__name__)


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
        """
        Register a new analysis method.
        
        Args:
            identifier: Unique method identifier
            category: Analysis category
            function: Analysis function
            description: Human-readable description
            default_params: Default parameter values
            
        Raises:
            ValueError: If identifier already registered
        """
        if identifier in self._methods:
            raise ValueError(f"Method '{identifier}' is already registered")
        
        registration = MethodRegistration(
            identifier=identifier,
            category=category,
            function=function,
            description=description,
            default_params=default_params or {}
        )
        
        self._methods[identifier] = registration
        logger.debug(f"Registered method: {category}/{identifier}")
    
    def get_method(self, identifier: str) -> Optional[MethodRegistration]:
        """
        Retrieve a registered method.
        
        Args:
            identifier: Method identifier
            
        Returns:
            MethodRegistration if found, None otherwise
        """
        return self._methods.get(identifier)
    
    def get_by_category(self, category: str) -> List[MethodRegistration]:
        """
        Get all methods in a category.
        
        Args:
            category: Category name
            
        Returns:
            List of MethodRegistration instances
        """
        return [
            registration
            for registration in self._methods.values()
            if registration.category == category
        ]
    
    def list_all(self) -> List[str]:
        """
        List all registered method identifiers.
        
        Returns:
            List of method identifiers
        """
        return list(self._methods.keys())
    
    def list_categories(self) -> List[str]:
        """
        List all registered categories.
        
        Returns:
            List of unique category names
        """
        categories = set(
            registration.category
            for registration in self._methods.values()
        )
        return sorted(categories)
    
    def get_info(self, identifier: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a method.
        
        Args:
            identifier: Method identifier
            
        Returns:
            Dictionary with method info, or None if not found
        """
        registration = self.get_method(identifier)
        if registration is None:
            return None
        
        return {
            'identifier': registration.identifier,
            'category': registration.category,
            'description': registration.description,
            'default_params': registration.default_params
        }


_global_registry = MethodRegistry()


def register_method(
    identifier: str,
    category: str,
    function: Callable,
    description: str = "",
    default_params: Optional[Dict[str, Any]] = None
) -> None:
    """
    Register a method in the global registry.
    
    Args:
        identifier: Unique method identifier
        category: Analysis category
        function: Analysis function
        description: Human-readable description
        default_params: Default parameter values
    """
    _global_registry.register(identifier, category, function, description, default_params)


def get_registry() -> MethodRegistry:
    """
    Get the global registry instance.
    
    Returns:
        Global MethodRegistry instance
    """
    return _global_registry