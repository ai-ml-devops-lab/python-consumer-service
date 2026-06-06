# Python Consumer Service

A production-style FastAPI service that consumes the native `portfolio-core` Python package.

## What this solves for companies

Companies often need to use optimized internal libraries from multiple applications. This repository shows a clean consumer service with:

- typed application code;
- health and scoring endpoints;
- defensive fallback if the native package is not installed;
- tests;
- Docker image build;
- CI/CD workflow.

## Local quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest -q
uvicorn consumer_service.api:app --reload
```

## Use the C++ package

After publishing or tagging `cpp-pybind-core`, install it with one of:

```bash
pip install portfolio-core
pip install 'portfolio-core @ git+https://github.com/YOUR_ORG/cpp-pybind-core.git@v0.1.0'
```

The service falls back to a pure Python implementation so that CI remains lightweight and reliable.

## Examples

Start the service locally:

```bash
uvicorn consumer_service.api:app --reload
```

Basic requests:

```bash
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/ready
curl http://127.0.0.1:8000/version

curl -X POST http://127.0.0.1:8000/score -H "Content-Type: application/json" -d '{"values":[1,2,3,4], "window":2}'
```

OpenAPI docs are available at `http://127.0.0.1:8000/docs`.

## Docker & Local Testing

### Option 1: Docker Compose (Local Development)

Fastest way to test locally with Docker:

```bash
make docker-up
```

This starts the service in a container with hot-reload on port `8010`. Test it:

```bash
curl http://127.0.0.1:8010/health
```

View logs:

```bash
make docker-logs
```

Run tests inside the container:

```bash
make docker-test
```

Stop the service:

```bash
make docker-down
```

### Option 2: Remote Container Development (VS Code)

For full IDE support **inside** the Docker container:

**Prerequisites:**
- Install [Docker Desktop](https://www.docker.com/products/docker-desktop)
- Install VS Code extension: **Dev Containers** (`ms-vscode.remote-containers`)

**Steps:**
1. Open the project folder in VS Code
2. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac), type `Dev Containers: Reopen in Container`
3. VS Code rebuilds the container and reconnects your session
4. Open the terminal in VS Code — you're now inside the container
5. Run `pytest` or `make test` directly
6. Debugging and linting work natively with Python extensions configured

**Benefits:**
- Exact environment parity (no "works on my machine" issues)
- One-click setup for team members
- All Python tooling (Pylance, Ruff, pytest, debugger) runs inside the container

### Option 3: Docker Image Build

For production-like testing:

```bash
make docker-build
docker run -p 8010:8010 python-consumer-service:local
```

Then test:

```bash
curl http://127.0.0.1:8010/
```
