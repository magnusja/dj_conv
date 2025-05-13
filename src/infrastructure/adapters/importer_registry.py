"""
Registry for DJ library importers
"""
from typing import Dict, List, Optional, Type

from src.infrastructure.adapters.importers.importer_interface import ImporterInterface


class ImporterRegistry:
    """
    Registry for DJ library importers
    """
    
    def __init__(self):
        self.importers: Dict[str, ImporterInterface] = {}
        
    def register(self, importer: ImporterInterface):
        """
        Register an importer
        
        Args:
            importer: The importer to register
        """
        self.importers[importer.format_name.lower()] = importer
        
    def get_importer(self, format_name: str) -> Optional[ImporterInterface]:
        """
        Get an importer by format name
        
        Args:
            format_name: The name of the DJ software format
            
        Returns:
            The importer or None if not found
        """
        return self.importers.get(format_name.lower())
        
    def get_all_importers(self) -> List[ImporterInterface]:
        """
        Get all registered importers
        
        Returns:
            A list of all importers
        """
        return list(self.importers.values())
        
    def get_format_names(self) -> List[str]:
        """
        Get all registered format names
        
        Returns:
            A list of all format names
        """
        return [importer.format_name for importer in self.importers.values()]
