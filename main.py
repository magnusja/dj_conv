#!/usr/bin/env python3
"""
DJ Library Converter - Main Application Entry Point
"""
import sys
from PySide6.QtWidgets import QApplication
from src.presentation.ui.main_window import MainWindow


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
