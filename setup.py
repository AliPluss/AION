#!/usr/bin/env python3
"""
Setup script for AION - AI Operating Node
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README file
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    requirements = requirements_file.read_text().strip().split('\n')
    requirements = [req.strip() for req in requirements if req.strip() and not req.startswith('#')]

setup(
    name="aion-ai",
    version="1.0.0",
    author="AION Development Team",
    author_email="dev@aion-ai.com",
    description="🤖 AION - AI Operating Node: Multilingual Terminal-based AI Assistant",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/aion-ai",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: System :: Shells",
        "Topic :: Terminals",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "web": [
            "fastapi>=0.104.0",
            "uvicorn>=0.24.0",
            "jinja2>=3.1.0",
            "python-multipart>=0.0.6",
        ],
        "full": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "fastapi>=0.104.0",
            "uvicorn>=0.24.0",
            "jinja2>=3.1.0",
            "python-multipart>=0.0.6",
        ]
    },
    entry_points={
        "console_scripts": [
            "aion=main:app",
            "aion-cli=start_aion_en:main",
            "aion-ar=start_aion:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.json", "*.txt", "*.md", "*.yml", "*.yaml"],
        "locales": ["*.json"],
        "config": ["*.json"],
        "templates": ["*.html", "*.css", "*.js"],
    },
    zip_safe=False,
    keywords="ai, assistant, terminal, multilingual, arabic, cli, tui, web, automation",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/aion-ai/issues",
        "Source": "https://github.com/yourusername/aion-ai",
        "Documentation": "https://github.com/yourusername/aion-ai/wiki",
    },
)
