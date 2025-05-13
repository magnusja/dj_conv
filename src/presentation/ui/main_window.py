"""
Main window for the DJ Library Converter application
"""
import os
import sys
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QComboBox, QFileDialog,
    QProgressBar, QCheckBox, QGroupBox, QMessageBox,
    QApplication
)
from PySide6.QtCore import Qt, Slot, Signal

from src.domain.services.conversion_service import ConversionService
from src.application.services.conversion_orchestrator import ConversionOrchestrator
from src.application.use_cases.import_library import ImportLibraryUseCase
from src.application.use_cases.export_library import ExportLibraryUseCase
from src.infrastructure.adapters.importer_registry import ImporterRegistry
from src.infrastructure.adapters.exporter_registry import ExporterRegistry
from src.infrastructure.adapters.importers.traktor_importer import TraktorImporter
from src.infrastructure.adapters.exporters.rekordbox_exporter import RekordboxExporter


class MainWindow(QMainWindow):
    """
    Main window for the DJ Library Converter application
    """
    
    def __init__(self):
        super().__init__()
        
        # Set up the window
        self.setWindowTitle("DJ Library Converter")
        self.setMinimumSize(600, 400)
        
        # Initialize registries
        self.importer_registry = ImporterRegistry()
        self.exporter_registry = ExporterRegistry()
        
        # Register importers and exporters
        self.importer_registry.register(TraktorImporter())
        self.exporter_registry.register(RekordboxExporter())
        
        # Initialize use cases
        self.import_use_case = ImportLibraryUseCase(self.importer_registry)
        self.export_use_case = ExportLibraryUseCase(self.exporter_registry)
        
        # Initialize services
        self.conversion_service = ConversionService()
        self.conversion_orchestrator = ConversionOrchestrator(
            self.import_use_case,
            self.export_use_case,
            self.conversion_service
        )
        
        # Set up the UI
        self._setup_ui()
        
        # Connect signals
        self._connect_signals()
        
    def _setup_ui(self):
        """Set up the user interface"""
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Input section
        input_group = QGroupBox("Input")
        input_layout = QVBoxLayout(input_group)
        
        # Input format selection
        input_format_layout = QHBoxLayout()
        input_format_layout.addWidget(QLabel("Input Format:"))
        self.input_format_combo = QComboBox()
        for format_name in self.importer_registry.get_format_names():
            self.input_format_combo.addItem(format_name)
        input_format_layout.addWidget(self.input_format_combo)
        input_layout.addLayout(input_format_layout)
        
        # Input file selection
        input_file_layout = QHBoxLayout()
        input_file_layout.addWidget(QLabel("Input File:"))
        self.input_file_edit = QLabel("No file selected")
        input_file_layout.addWidget(self.input_file_edit, 1)
        self.input_file_button = QPushButton("Browse...")
        input_file_layout.addWidget(self.input_file_button)
        input_layout.addLayout(input_file_layout)
        
        main_layout.addWidget(input_group)
        
        # Output section
        output_group = QGroupBox("Output")
        output_layout = QVBoxLayout(output_group)
        
        # Output format selection
        output_format_layout = QHBoxLayout()
        output_format_layout.addWidget(QLabel("Output Format:"))
        self.output_format_combo = QComboBox()
        for format_name in self.exporter_registry.get_format_names():
            self.output_format_combo.addItem(format_name)
        output_format_layout.addWidget(self.output_format_combo)
        output_layout.addLayout(output_format_layout)
        
        # Output file selection
        output_file_layout = QHBoxLayout()
        output_file_layout.addWidget(QLabel("Output File:"))
        self.output_file_edit = QLabel("No file selected")
        output_file_layout.addWidget(self.output_file_edit, 1)
        self.output_file_button = QPushButton("Browse...")
        output_file_layout.addWidget(self.output_file_button)
        output_layout.addLayout(output_file_layout)
        
        main_layout.addWidget(output_group)
        
        # Conversion options
        options_group = QGroupBox("Conversion Options")
        options_layout = QVBoxLayout(options_group)
        
        # Hot cue conversion option
        self.hot_cue_checkbox = QCheckBox("Convert Hot Cues to Memory Cues")
        options_layout.addWidget(self.hot_cue_checkbox)
        
        main_layout.addWidget(options_group)
        
        # Progress bar
        progress_layout = QHBoxLayout()
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        progress_layout.addWidget(self.progress_bar)
        
        self.progress_label = QLabel("Ready")
        progress_layout.addWidget(self.progress_label)
        
        main_layout.addLayout(progress_layout)
        
        # Convert button
        self.convert_button = QPushButton("Convert")
        self.convert_button.setEnabled(False)
        main_layout.addWidget(self.convert_button)
        
    def _connect_signals(self):
        """Connect signals to slots"""
        self.input_file_button.clicked.connect(self._select_input_file)
        self.output_file_button.clicked.connect(self._select_output_file)
        self.convert_button.clicked.connect(self._convert)
        
        # Set up progress callback
        self.conversion_orchestrator.set_progress_callback(self._update_progress)
        
        # Enable/disable convert button based on file selection
        self.input_file_button.clicked.connect(self._update_convert_button)
        self.output_file_button.clicked.connect(self._update_convert_button)
        
    def _select_input_file(self):
        """Select input file"""
        file_filter = "Traktor Library (*.nml);;All Files (*.*)"
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Input File", "", file_filter
        )
        
        if file_path:
            self.input_file_edit.setText(file_path)
            self._update_convert_button()
            
    def _select_output_file(self):
        """Select output file"""
        file_filter = "Rekordbox Library (*.xml);;All Files (*.*)"
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Select Output File", "", file_filter
        )
        
        if file_path:
            self.output_file_edit.setText(file_path)
            self._update_convert_button()
            
    def _update_convert_button(self):
        """Update the state of the convert button"""
        input_file = self.input_file_edit.text()
        output_file = self.output_file_edit.text()
        
        self.convert_button.setEnabled(
            input_file != "No file selected" and 
            output_file != "No file selected"
        )
        
    def _update_progress(self, percentage: int, message: str):
        """Update the progress bar and label"""
        self.progress_bar.setValue(percentage)
        self.progress_label.setText(message)
        QApplication.processEvents()
        
    def _convert(self):
        """Convert the library"""
        input_file = self.input_file_edit.text()
        input_format = self.input_format_combo.currentText()
        output_file = self.output_file_edit.text()
        output_format = self.output_format_combo.currentText()
        
        # Get conversion options
        options = {
            'convert_hot_cues_to_memory_cues': self.hot_cue_checkbox.isChecked()
        }
        
        # Disable UI during conversion
        self._set_ui_enabled(False)
        
        # Perform conversion
        success = self.conversion_orchestrator.convert(
            input_file,
            input_format,
            output_file,
            output_format,
            options
        )
        
        # Re-enable UI
        self._set_ui_enabled(True)
        
        # Show result
        if success:
            QMessageBox.information(
                self,
                "Conversion Complete",
                f"Library successfully converted to {output_format} format."
            )
        else:
            QMessageBox.critical(
                self,
                "Conversion Failed",
                "Failed to convert library. Check the console for details."
            )
            
    def _set_ui_enabled(self, enabled: bool):
        """Enable or disable UI elements during conversion"""
        self.input_format_combo.setEnabled(enabled)
        self.input_file_button.setEnabled(enabled)
        self.output_format_combo.setEnabled(enabled)
        self.output_file_button.setEnabled(enabled)
        self.hot_cue_checkbox.setEnabled(enabled)
        self.convert_button.setEnabled(enabled)
