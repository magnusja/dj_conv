# DJ Library Converter

A utility for converting DJ libraries between different formats, with a focus on Traktor to Rekordbox conversion.

## Features

- Convert Native Instruments Traktor libraries to Pioneer Rekordbox format
- Preserve playlists, hot cues, loops, and other metadata
- Configurable conversion options (hot cue to memory cue, etc.)
- Extensible architecture for adding support for other DJ software formats

## Requirements

- Python 3.8+
- PySide6
- lxml

## Installation

This project uses Poetry for dependency management.

```bash
# Install Poetry if you don't have it
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install
```

Alternatively, you can use pip:

```bash
pip install -r requirements.txt
```

## Usage

Using Poetry:

```bash
poetry run python main.py
```

Or directly:

```bash
python main.py
```

Command-line conversion:

```bash
# Using Poetry script
poetry run traktor2rekordbox input.nml output.xml --convert-hot-cues

# Or directly
poetry run python examples/convert_traktor_to_rekordbox.py input.nml output.xml --convert-hot-cues
```

## Architecture

This project follows Domain-Driven Design principles with a clean architecture approach:

- **Domain Layer**: Core business entities and logic
- **Application Layer**: Use cases and orchestration
- **Infrastructure Layer**: External systems integration (file formats, storage)
- **Presentation Layer**: User interface

## Extending

To add support for additional DJ software formats:

1. Create a new importer in `src/infrastructure/adapters/importers/`
2. Create a new exporter in `src/infrastructure/adapters/exporters/`
3. Implement the respective interfaces
4. Register the new format in the UI

## License

MIT
