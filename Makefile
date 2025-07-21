# Variables
VENV_NAME = venv
PYTHON = $(VENV_NAME)/bin/python
PIP = $(VENV_NAME)/bin/pip
PYTEST = $(VENV_NAME)/bin/pytest

.PHONY: all setup install run test test-cov test-file test-pattern docker docker-down clean migrate logs help

# Default target
all: docker migrate logs

# Create virtual environment and install dependencies locally
setup:
	@echo "Creating virtual environment and installing dependencies..."
	python3 -m venv $(VENV_NAME)
	$(PIP) install -r requirements.txt

# Install dependencies into venv
install: $(VENV_NAME)
	@echo "Installing dependencies..."
	$(PIP) install -r requirements.txt

# Run FastAPI app locally (not recommended if using Docker)
run:
	@echo "Running FastAPI locally..."
	uvicorn app.main:app --reload

# Run tests
test: install
	@echo "Running tests..."
	$(PYTEST)

# Run tests with coverage
test-cov: install
	@echo "Running tests with coverage..."
	$(PYTEST) --cov=app --cov-report=html --cov-report=term

# Run specific test file
test-file: install
	@echo "Running specific test file..."
	@read -p "Enter test file path (e.g., tests/test_main.py): " file; \
	$(PYTEST) $$file -v

# Run tests matching a pattern
test-pattern: install
	@echo "Running tests matching pattern..."
	@read -p "Enter test pattern (e.g., test_create): " pattern; \
	$(PYTEST) -k $$pattern -v

# Start Docker containers
docker:
	@echo "Running Docker Compose..."
	docker compose up --build -d

# Stop and remove Docker containers
docker-down:
	docker compose down

# Apply Alembic migrations inside Docker
migrate:
	@echo "Applying DB migrations..."
	docker compose exec api alembic upgrade head

# View container logs
logs:
	docker compose logs -f

# Clean up
clean:
	@echo "Cleaning up..."
	rm -rf $(VENV_NAME)
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -exec rm -rf {} +

# Help menu
help:
	@echo "Usage: make [TARGET]"
	@echo ""
	@echo "Targets:"
	@echo "  setup        - Create venv and install dependencies"
	@echo "  install      - Install dependencies into venv"
	@echo "  run          - Run FastAPI locally (not via Docker)"
	@echo "  test         - Run tests"
	@echo "  test-cov     - Run tests with coverage report"
	@echo "  test-file    - Run specific test file"
	@echo "  test-pattern - Run tests matching a pattern"
	@echo "  docker       - Build and start Docker containers"
	@echo "  docker-down  - Stop Docker containers"
	@echo "  migrate      - Run Alembic migrations inside container"
	@echo "  logs         - View container logs"
	@echo "  clean        - Remove venv, pyc, and __pycache__"
	@echo "  help         - Show this message"
