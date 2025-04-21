# Variables
VENV_NAME = venv
PYTHON = $(VENV_NAME)/bin/python
PIP = $(VENV_NAME)/bin/pip
PYTEST = $(VENV_NAME)/bin/pytest

.PHONY: all setup install run test docker docker-down clean migrate logs help

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
	PYTHONPATH=$(PWD) $(PYTEST) tests

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
	@echo "  docker       - Build and start Docker containers"
	@echo "  docker-down  - Stop Docker containers"
	@echo "  migrate      - Run Alembic migrations inside container"
	@echo "  logs         - View container logs"
	@echo "  clean        - Remove venv, pyc, and __pycache__"
	@echo "  help         - Show this message"
