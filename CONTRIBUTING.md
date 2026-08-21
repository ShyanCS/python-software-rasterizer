# Contributing

Thank you for your interest in contributing to `python-software-rasterizer`!

## Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/ShyanCS/python-software-rasterizer.git
   cd python-software-rasterizer
   ```

2. **Create a virtual environment and install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## Before Opening a Pull Request

Please make sure all of the following pass locally:

```bash
# Lint
ruff check src/renderer tests

# Formatting
black --check src/renderer tests

# Tests with coverage
pytest --cov=src/renderer --cov-report=term-missing --cov-fail-under=70 tests/
```

## Commit Guidelines

- Keep commits small and focused on a single logical change.
- Use a descriptive commit message in the imperative mood (e.g., `Add texture sampling tests`).
- Each new feature or bug fix should include a matching test.

## Project Structure

```
src/renderer/     # Core renderer source code
tests/            # Pytest unit and integration tests
.github/          # CI workflows and Dependabot config
Dockerfile        # Container build
docker-compose.yml
```
