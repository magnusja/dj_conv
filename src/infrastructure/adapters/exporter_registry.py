"""
Registry for DJ library exporters
"""
from typing import Dict, List, Optional, Type

from src.infrastructure.adapters.exporters.exporter_interface import ExporterInterface


class ExporterRegistry:
    """
    Registry for DJ library exporters
    """
    
    def __init__(self):
        self.exporters: Dict[str, ExporterInterface] = {}
        
    def register(self, exporter: ExporterInterface):
        """
        Register an exporter
        
        Args:
            exporter: The exporter to register
        """
        self.exporters[exporter.format_name.lower()] = exporter
        
    def get_exporter(self, format_name: str) -> Optional[ExporterInterface]:
        """
        Get an exporter by format name
        
        Args:
            format_name: The name of the DJ software format
            
        Returns:
            The exporter or None if not found
        """
        return self.exporters.get(format_name.lower())
        
    def get_all_exporters(self) -> List[ExporterInterface]:
        """
        Get all registered exporters
        
        Returns:
            A list of all exporters
        """
        return list(self.exporters.values())
        
    def get_format_names(self) -> List[str]:
        """
        Get all registered format names
        
        Returns:
            A list of all format names
        """
        return [exporter.format_name for exporter in self.exporters.values()]
