# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MeterViewer is a Python library for processing meter-formatted datasets. It provides tools for generating, viewing, and managing meter image datasets with support for data validation and visualization.

## Development Commands

### Environment Setup
```bash
# Install development dependencies
uv sync --group dev

# Install documentation dependencies  
uv sync --group docs
```

### Testing
```bash
# Run all tests
pytest tests/

# Run specific test files
pytest tests/test_dataset.py
pytest tests/test_generator.py
```

### Code Quality
```bash
# Format and lint code
ruff check . --fix
```

### Documentation
```bash
# Build documentation locally
cd docs && make html

# Live documentation server
make docs
```

### Development Tools
```bash
# Start Jupyter notebook server
make notebook

# Launch Streamlit web app
make app
```

## Architecture Overview

### Core Components

**MeterSet** (`src/meterviewer/meterset.py`)
- Core data structure representing a collection of meter images
- Handles image loading, value extraction, and position detection
- Uses XML configuration files for metadata

**MeterDataset** (`src/meterviewer/dataset.py`)
- PyTorch-compatible dataset wrapper around MeterSet
- Supports train/test splits and custom transformations
- Gracefully handles missing PyTorch dependency

**Generator Framework** (`src/meterviewer/generator/`)
- Base generator class for creating synthetic meter datasets
- Supports JSON database and SQLite backends
- Modular architecture for different generation strategies

**Image Processing** (`src/meterviewer/img/`)
- Computer vision utilities using OpenCV
- Image cropping, resizing, validation, and drawing functions
- Color style processing and comparison tools

**FastView UI** (`src/meterviewer/fastview/`)
- Streamlit-based web interface for dataset visualization
- Interactive pages for dataset comparison and single image viewing
- Real-time dataset exploration tools

### Data Flow

1. **Dataset Generation**: Use generator classes to create meter image datasets with metadata
2. **Data Loading**: MeterSet loads images and extracts values from XML configurations  
3. **Visualization**: FastView provides web-based tools for dataset exploration
4. **Analysis**: Jupyter notebooks in `examples/` demonstrate common workflows

## Configuration

The project uses TOML configuration files for dataset generation:
- `config.toml`: Main project configuration
- `dataset-gen.toml`: Dataset generation parameters
- Custom config files in `examples/playground/`

## Package Management

This project uses `uv` for dependency management with pyproject.toml:
- Main dependencies include OpenCV, NumPy, Matplotlib, SQLAlchemy
- Development tools: pytest, ruff, Jupyter, Streamlit
- Optional PyTorch integration for machine learning workflows

## Testing Strategy

Tests are organized by component in `tests/`:
- Unit tests for core functionality 
- Integration tests for dataset operations
- Utility functions for test setup and teardown
- Separate test configurations for different scenarios