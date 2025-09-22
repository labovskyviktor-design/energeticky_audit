# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

Energy Audit Desktop Application is a Slovak-language desktop application built with Python and Tkinter for conducting energy audits and building certifications. The application provides tools for creating energy audits, generating efficiency certificates, and managing audit knowledge and data.

## Development Commands

### Environment Setup
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -e .[dev]
```

### Running the Application
```powershell
# Run directly using the launcher script
python run.py

# Or run the main module
python -m src.main

# Or use the console script (after installation)
energy-audit
```

### Development Tools
```powershell
# Code formatting
black src/ tests/

# Linting
flake8 src/ tests/

# Type checking
mypy src/

# Run tests
pytest

# Run tests with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_specific.py

# Run specific test function
pytest tests/test_specific.py::test_function_name
```

### Project Management
```powershell
# Create directory structure
python src/config.py

# Package for distribution
python setup.py sdist bdist_wheel
```

## Architecture Overview

### Core Structure
- **`src/main.py`**: Main application entry point containing the `EnergyAuditApp` class with Tkinter GUI
- **`src/config.py`**: Centralized configuration including energy constants, material properties, building types, and directory structure
- **`run.py`**: Application launcher script that handles imports and error management

### Key Components

#### GUI Architecture
- Built with Tkinter and ttk for modern styling
- Main window structure: left tool panel + tabbed workspace area
- Menu system with File, Tools, and Help menus
- Notebook widget for multi-tab functionality

#### Configuration System
- Energy constants for thermal calculations (conductivity, capacity, density)
- Building energy efficiency classes (A1-G) with consumption thresholds and colors  
- Predefined building types and heating system categories
- Directory structure management with automatic creation

#### Data Management
- SQLite database for audit storage (`data/energy_audit.db`)
- Automatic directory creation for data, backups, exports, logs
- Template system for report generation
- Export functionality for audit reports

### Technology Stack
- **GUI**: `customtkinter` (5.2.2) and `tkinter-modern` (1.4.4) for modern UI
- **Data Processing**: `pandas` (2.1.4) and `numpy` (1.24.3)
- **Reports**: `reportlab` (4.0.7) for PDF generation, `matplotlib` (3.7.2) for charts
- **Database**: SQLite3 (built-in)
- **Configuration**: `pyyaml` (6.0.1) and `configparser` (6.0.0)
- **Logging**: `loguru` (0.7.2)

### Application Features
The application framework supports:
- Energy audit creation and management
- Building certification generation  
- Energy calculation tools
- Material thermal property database
- Multi-language support (Slovak interface)
- Export to various formats including PDF reports

## Project-Specific Notes

### Language Considerations
- The application interface is in Slovak
- Comments and documentation are in Slovak
- Menu items, labels, and user messages are localized
- When adding new features, maintain Slovak language consistency

### Energy Audit Domain
- Building energy efficiency classification follows European standards (A1-G)
- Thermal calculations use standard material properties defined in `config.py`
- Support for various building types and heating systems common in Slovakia
- Energy consumption thresholds are defined per efficiency class

### File Structure Conventions
- Main source code in `src/` directory
- Configuration constants centralized in `config.py`
- Data files stored in `data/` with automatic subdirectory creation
- Template files for reports in `resources/templates/`
- Backup and export functionality built-in

### Development Considerations
- The application creates necessary directories automatically on first run
- Database schema and initial data should be handled through the configuration system  
- GUI components follow consistent naming (Slovak labels, English code)
- Error handling includes user-friendly Slovak messages