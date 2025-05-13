"""
Use case for exporting a DJ library to a file
"""
from typing import Dict, Any, Optional

from src.domain.entities.collection import Collection


class ExportLibraryUseCase:
    """
    Use case for exporting a DJ library to a file
    """
    
    def __init__(self, exporter_registry):
        self.exporter_registry = exporter_registry
        
    def execute(
        self, 
        collection: Collection, 
        file_path: str, 
        format_name: str,
        options: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Export a DJ library to a file
        
        Args:
            collection: The collection to export
            file_path: Path to save the library file
            format_name: Name of the DJ software format
            options: Export options specific to the format
            
        Returns:
            True if export was successful, False otherwise
        """
        exporter = self.exporter_registry.get_exporter(format_name)
        if not exporter:
            raise ValueError(f"No exporter found for format: {format_name}")
            
        return exporter.export_library(collection, file_path, options or {})
