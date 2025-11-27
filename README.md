# Mobile Coverage API

![Docker Version](https://img.shields.io/badge/docker-v26.1.1-2496ED.svg?style=for-the-badge&logo=docker)
![Python Version](https://img.shields.io/badge/python-v3.13-blue.svg?style=for-the-badge&logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![FastAPI](https://img.shields.io/badge/fastapi-v0.121.3-009688.svg?style=for-the-badge&logo=fastapi)


## Overview

A FastAPI service exposing 2G/3G/4G mobile network coverage for any address in France. It uses PostgreSQL and official antenna site data as the source of truth.

### Key Features
- Coverage lookup by address or coordinates
- REST API with OpenAPI docs
- Reproducible local setup via `uv`

## Prerequisites

- Docker 26.1.1 or higher
- Docker Compose
- [uv](https://github.com/astral-sh/uv) for local development (the project includes uv.lock and pyproject.toml)


## Quick Start

### Docker Compose (recommended)
1. Verify Docker installation:
   ```bash
   docker version && docker compose version
   ```
2. Clone the repository:
   ```bash
   git clone https://github.com/ArystanIgen/mobile-coverage-api
   cd mobile-coverage-api
   ```
3. Create your `.env` from the template:
   ```bash
   cp .env.example .env
   # Edit values as needed
   ```
4. Build and start the stack:
   ```bash
   just up-build
   ```
5. Open the service:
   - API base: http://localhost:8034
   - Swagger UI: http://localhost:8034/api/docs
   - ReDoc: http://localhost:8034/api/redoc

To see other available commands:
```bash
just
```


## Testing
You can run the test suite by executing this command:

```bash
  just test
  ```

## Linting
You can run the lints by executing this command:

```bash
  just lint
  ```
