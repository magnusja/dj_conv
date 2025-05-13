"""
Interface for DJ library exporters
"""
from abc import ABC, abstractmethod
from typing import Dict, Any

from src.domain.entities.collection import Collection


class ExporterInterface(ABC):
    """
    Interface for DJ library exporters
    """
    
    @property
    @abstractmethod
    def format_name(self) -> str:
        """Get the name of the DJ software format"""
        pass
    
    @abstractmethod
    def export_library(self, collection: Collection, file_path: str, options: Dict[str, Any] = None) -> bool:
        """
        Export a DJ library to a file
        
        Args:
            collection: The collection to export
            file_path: Path to save the library file
            options: Export options specific to the format
            
        Returns:
            True if export was successful, False otherwise
        """
        pass
