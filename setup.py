"""
Setup script pre Energy Audit Desktop Application
"""

from setuptools import setup, find_packages
from pathlib import Path

# Načítanie obsahu README súboru
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="energy-audit-app",
    version="1.0.0",
    author="Energy Audit Team",
    author_email="team@energyaudit.local",
    description="Desktopová aplikácia na vykonávanie energetického auditu a certifikáciu budov",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/energy-audit-app",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business",
        "Topic :: Scientific/Engineering",
    ],
    python_requires=">=3.8",
    install_requires=[
        "tkinter-modern>=1.4.4",
        "customtkinter>=5.2.2",
        "pandas>=2.1.4",
        "numpy>=1.24.3",
        "openpyxl>=3.1.2",
        "reportlab>=4.0.7",
        "matplotlib>=3.7.2",
        "configparser>=6.0.0",
        "pyyaml>=6.0.1",
        "loguru>=0.7.2",
        "python-dateutil>=2.8.2",
        "pathlib2>=2.3.7",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "energy-audit=src.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.txt", "*.md", "*.yml", "*.yaml", "*.json"],
    },
)