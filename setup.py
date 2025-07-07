#!/usr/bin/env python3
"""
Setup script for AION - AI Operating Node
PyPI Package Configuration for pip install aion-ai
"""

from setuptools import setup, find_packages
import os

# Read README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Core requirements for AION
requirements = [
    "typer>=0.9.0",
    "rich>=13.0.0",
    "textual>=0.41.0",
    "fastapi>=0.104.0",
    "uvicorn>=0.24.0",
    "pydantic>=2.0.0",
    "cryptography>=41.0.0",
    "psutil>=5.9.0",
    "aiofiles>=23.0.0",
    "httpx>=0.25.0",
    "python-dotenv>=1.0.0",
    "openai>=1.0.0",
    "google-generativeai>=0.3.0",
    "requests>=2.31.0",
    "pyyaml>=6.0.0",
    "click>=8.0.0",
]

setup(
    name="aion-ai",
    version="2.2.0",
    author="AliPluss",
    author_email="project.django.rst@gmail.com",
    description="🤖 AION - AI Operating Node | Professional Terminal AI Assistant with Multi-Provider Support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AliPluss/AION",
    packages=find_packages(exclude=["tests*", "test_logs*", "*.tests", "*.tests.*"]),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
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
        "Topic :: Office/Business :: Groupware",
        "Topic :: Communications :: Chat",
        "Environment :: Console",
        "Environment :: Console :: Curses",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "isort>=5.12.0",
            "pre-commit>=3.0.0",
        ],
        "full": [
            "jupyter>=1.0.0",
            "notebook>=6.5.0",
            "matplotlib>=3.7.0",
            "pandas>=2.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "aion=aion.main:main",
            "aion-cli=aion.main:main",
            "aion-ai=aion.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "aion": [
            "config/*.json",
            "config/*.yaml",
            "templates/*.html",
            "static/*",
            "locales/*/*.json",
        ],
    },
    keywords=[
        "ai", "artificial-intelligence", "terminal", "assistant", "cli", "tui",
        "openai", "deepseek", "gemini", "automation", "chatbot", "command-line",
        "productivity", "developer-tools", "ai-assistant", "multi-language",
        "cross-platform", "security", "sandbox", "plugin-system"
    ],
    project_urls={
        "Homepage": "https://github.com/AliPluss/AION",
        "Bug Reports": "https://github.com/AliPluss/AION/issues",
        "Source": "https://github.com/AliPluss/AION",
        "Documentation": "https://github.com/AliPluss/AION#readme",
        "Changelog": "https://github.com/AliPluss/AION/releases",
        "Funding": "https://github.com/sponsors/AliPluss",
    },
    zip_safe=False,
    platforms=["any"],
)
