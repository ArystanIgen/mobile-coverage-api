# justfile for mobile-coverage-api project
# Run with: just <command>

# List all available commands
default:
    @just --list

# Start all services in detached mode
up:
    docker-compose up -d

# Build all services
build:
    docker-compose build

# Build and start all services in detached mode
up-build:
    docker-compose up -d --build

# Stop all services
down args='':
    docker compose down {{ args }}

# Show logs for a specific service
logs service:
    docker-compose logs -f {{ service }}

# Restart a specific service
restart service:
    docker-compose restart {{ service }}

# Linting Commands
# ---------------

# Run ruff check using uv
ruff-check args='':
    uv run ruff check --no-cache . {{ args }}

# Run ruff format using uv
ruff-format:
    uv run ruff format .


# Run mypy type checking
mypy:
    uv run mypy .

# Run bandit security check
bandit:
    uv run bandit .

# Run safety check
safety:
    uv run safety check --full-report --ignore 42194

# Run all linting checks
lint: ruff-check mypy bandit safety
    @echo "All linting checks completed"

# Run linting inside Docker
docker-lint:
    docker-compose run --rm -e ENV=LINT fastapi

# Run pytest tests inside Docker
test:
    docker-compose run --rm -e ENV=TEST fastapi
