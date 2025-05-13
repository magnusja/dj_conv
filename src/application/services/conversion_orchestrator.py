"""
Service for orchestrating the conversion process
"""
from typing import Dict, Any, Optional, Callable

from src.domain.entities.collection import Collection
from src.domain.services.conversion_service import ConversionService
from src.application.use_cases.import_library import ImportLibraryUseCase
from src.application.use_cases.export_library import ExportLibraryUseCase


class ConversionOrchestrator:
    """
    Service for orchestrating the conversion process between different DJ software formats
    """
    
    def __init__(
        self,
        import_use_case: ImportLibraryUseCase,
        export_use_case: ExportLibraryUseCase,
        conversion_service: ConversionService
    ):
        self.import_use_case = import_use_case
        self.export_use_case = export_use_case
        self.conversion_service = conversion_service
        self.progress_callback = None
        
    def set_progress_callback(self, callback: Callable[[int, str], None]):
        """
        Set a callback function to report progress
        
        Args:
            callback: Function that takes a percentage (0-100) and a message
        """
        self.progress_callback = callback
        
    def _report_progress(self, percentage: int, message: str):
        """Report progress through the callback if set"""
        if self.progress_callback:
            self.progress_callback(percentage, message)
            
    def convert(
        self,
        input_file: str,
        input_format: str,
        output_file: str,
        output_format: str,
        options: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Convert a DJ library from one format to another
        
        Args:
            input_file: Path to the input library file
            input_format: Name of the input DJ software format
            output_file: Path to save the output library file
            output_format: Name of the output DJ software format
            options: Conversion options
            
        Returns:
            True if conversion was successful, False otherwise
        """
        options = options or {}
        
        # Import the library
        self._report_progress(10, f"Importing {input_format} library...")
        try:
            collection = self.import_use_case.execute(input_file, input_format)
            if not collection:
                self._report_progress(100, f"Failed to import {input_format} library")
                return False
        except Exception as e:
            self._report_progress(100, f"Error importing library: {str(e)}")
            return False
            
        # Apply conversions based on options
        self._report_progress(40, "Processing library...")
        try:
            if options.get("convert_hot_cues_to_memory_cues", False):
                collection = self.conversion_service.convert_hot_cues_to_memory_cues(collection)
        except Exception as e:
            self._report_progress(100, f"Error processing library: {str(e)}")
            return False
            
        # Export the library
        self._report_progress(70, f"Exporting to {output_format}...")
        try:
            success = self.export_use_case.execute(
                collection, 
                output_file, 
                output_format,
                options
            )
            if not success:
                self._report_progress(100, f"Failed to export to {output_format}")
                return False
        except Exception as e:
            self._report_progress(100, f"Error exporting library: {str(e)}")
            return False
            
        self._report_progress(100, "Conversion completed successfully")
        return True
