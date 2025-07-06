# AION Makefile for development and deployment

.PHONY: help install install-dev test lint format type-check security clean build upload docker run-dev setup

# Default target
help:
	@echo "🤖 AION - AI Operating Node"
	@echo "Available commands:"
	@echo "  install      - Install production dependencies"
	@echo "  install-dev  - Install development dependencies"
	@echo "  test         - Run tests"
	@echo "  lint         - Run linting"
	@echo "  format       - Format code"
	@echo "  type-check   - Run type checking"
	@echo "  security     - Run security checks"
	@echo "  clean        - Clean build artifacts"
	@echo "  build        - Build package"
	@echo "  upload       - Upload to PyPI"
	@echo "  docker       - Build Docker image"
	@echo "  run-dev      - Run in development mode"
	@echo "  setup        - Setup development environment"

# Installation
install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pre-commit install

# Testing
test:
	pytest -v --tb=short --continue-on-collection-errors

test-basic:
	pytest tests/test_basic.py -v

test-integration:
	pytest tests/test_integration.py -v

test-coverage:
	pytest --cov=. --cov-report=html --cov-report=term-missing

test-verbose:
	pytest -v --cov=. --cov-report=html --cov-report=term-missing

health-check:
	@echo "🔍 Running AION health check..."
	@python -c "import sys; print(f'✅ Python version: {sys.version}')"
	@if [ -f "main.py" ] || [ -f "aion_project/main.py" ]; then echo "✅ Main application found"; else echo "❌ Main application not found"; fi
	@if [ -f "requirements.txt" ]; then echo "✅ Requirements file found"; else echo "❌ Requirements file not found"; fi
	@if [ -d "tests" ]; then echo "✅ Tests directory found"; else echo "❌ Tests directory not found"; fi
	@echo "🎉 Health check completed!"

# Code quality
lint:
	python -m flake8 . --exclude=venv,aion_env,build,dist
	python -m isort --check-only . --skip venv --skip aion_env --skip build --skip dist

format:
	python -m black . --exclude="/(venv|aion_env|build|dist)/"
	python -m isort . --skip venv --skip aion_env --skip build --skip dist

type-check:
	python -m mypy . --ignore-missing-imports --exclude="(venv|aion_env|build|dist)"

# Security
security:
	bandit -r . -f json -o bandit-report.json
	safety check

# Cleanup
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Build and upload
build: clean
	python -m build

upload: build
	twine check dist/*
	twine upload dist/*

upload-test: build
	twine check dist/*
	twine upload --repository testpypi dist/*

# Docker
docker:
	docker build -t aion-ai:latest .

docker-dev:
	docker build -t aion-ai:dev --target development .

docker-run:
	docker run -p 8000:8000 aion-ai:latest

docker-compose-up:
	docker-compose up -d

docker-compose-dev:
	docker-compose --profile dev up -d

# Development
run-dev:
	python main.py cli

run-web:
	python main.py web --host 0.0.0.0 --port 8000

run-tui:
	python main.py tui

# Setup
setup: install-dev
	python run.py setup
	@echo "✅ Development environment setup complete!"
	@echo "📝 Don't forget to configure your AI API keys in ~/.aion/config/ai_config.json"

# Quick start
quick-start:
	@echo "🚀 Quick starting AION..."
	python start_aion_en.py

quick-start-ar:
	@echo "🚀 بدء تشغيل AION..."
	python start_aion.py

# Documentation
docs:
	sphinx-build -b html docs docs/_build/html

docs-serve:
	cd docs/_build/html && python -m http.server 8080

# All checks
check-all: lint type-check security test
	@echo "✅ All checks passed!"

# CI simulation
ci: install-dev check-all build
	@echo "✅ CI simulation complete!"
