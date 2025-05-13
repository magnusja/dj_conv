"""
Interface for DJ library importers
"""
from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.collection import Collection


class ImporterInterface(ABC):
    """
    Interface for DJ library importers
    """
    
    @property
    @abstractmethod
    def format_name(self) -> str:
        """Get the name of the DJ software format"""
        pass
    
    @abstractmethod
    def import_library(self, file_path: str) -> Optional[Collection]:
        """
        Import a DJ library from a file
        
        Args:
            file_path: Path to the library file
            
        Returns:
            The imported collection or None if import failed
        """
        pass
    
    @abstractmethod
    def can_import(self, file_path: str) -> bool:
        """
        Check if this importer can import the given file
        
        Args:
            file_path: Path to the library file
            
        Returns:
            True if this importer can import the file, False otherwise
        """
        pass
