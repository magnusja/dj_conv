"""
Use case for importing a DJ library from a file
"""
from typing import Optional

from src.domain.entities.collection import Collection


class ImportLibraryUseCase:
    """
    Use case for importing a DJ library from a file
    """
    
    def __init__(self, importer_registry):
        self.importer_registry = importer_registry
        
    def execute(self, file_path: str, format_name: str) -> Optional[Collection]:
        """
        Import a DJ library from a file
        
        Args:
            file_path: Path to the library file
            format_name: Name of the DJ software format
            
        Returns:
            The imported collection or None if import failed
        """
        importer = self.importer_registry.get_importer(format_name)
        if not importer:
            raise ValueError(f"No importer found for format: {format_name}")
            
        return importer.import_library(file_path)
