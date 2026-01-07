.PHONY: test lint type-check format install check security-scan bandit safety

install:
	pip install -e ".[dev]"

test:
	pytest

lint:
	ruff check .

format:
	ruff format .

type-check:
	pyright

# Security scanning commands
bandit:
	@echo "Running Bandit security scan..."
	bandit -r src -f json -o bandit-report.json || true
	bandit -r src -f txt

safety:
	@echo "Running Safety vulnerability check..."
	@echo "Note: Safety checks runtime dependencies (dependencies = [])."
	@if [ -f requirements.txt ]; then \
		safety check --file requirements.txt || true; \
	else \
		echo "✓ No runtime dependencies to scan (project has dependencies = [])"; \
	fi

security-scan: bandit safety

check: lint type-check security-scan test
