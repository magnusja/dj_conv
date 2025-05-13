#!/usr/bin/env python3
"""
Example script to convert a Traktor library to Rekordbox format
"""
import os
import sys
import argparse

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.domain.services.conversion_service import ConversionService
from src.application.services.conversion_orchestrator import ConversionOrchestrator
from src.application.use_cases.import_library import ImportLibraryUseCase
from src.application.use_cases.export_library import ExportLibraryUseCase
from src.infrastructure.adapters.importer_registry import ImporterRegistry
from src.infrastructure.adapters.exporter_registry import ExporterRegistry
from src.infrastructure.adapters.importers.traktor_importer import TraktorImporter
from src.infrastructure.adapters.exporters.rekordbox_exporter import RekordboxExporter


def progress_callback(percentage, message):
    """Callback function to display progress"""
    print(f"{percentage}% - {message}")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Convert Traktor library to Rekordbox format')
    parser.add_argument('input_file', help='Path to the Traktor NML file')
    parser.add_argument('output_file', help='Path to save the Rekordbox XML file')
    parser.add_argument('--convert-hot-cues', action='store_true', 
                        help='Convert hot cues to memory cues')
    
    args = parser.parse_args()
    
    # Initialize registries
    importer_registry = ImporterRegistry()
    exporter_registry = ExporterRegistry()
    
    # Register importers and exporters
    importer_registry.register(TraktorImporter())
    exporter_registry.register(RekordboxExporter())
    
    # Initialize use cases
    import_use_case = ImportLibraryUseCase(importer_registry)
    export_use_case = ExportLibraryUseCase(exporter_registry)
    
    # Initialize services
    conversion_service = ConversionService()
    conversion_orchestrator = ConversionOrchestrator(
        import_use_case,
        export_use_case,
        conversion_service
    )
    
    # Set progress callback
    conversion_orchestrator.set_progress_callback(progress_callback)
    
    # Perform conversion
    options = {
        'convert_hot_cues_to_memory_cues': args.convert_hot_cues
    }
    
    success = conversion_orchestrator.convert(
        args.input_file,
        'Traktor',
        args.output_file,
        'Rekordbox',
        options
    )
    
    if success:
        print(f"Library successfully converted to Rekordbox format: {args.output_file}")
        return 0
    else:
        print("Failed to convert library")
        return 1


if __name__ == "__main__":
    sys.exit(main())
