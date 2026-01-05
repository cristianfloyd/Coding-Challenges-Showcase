.PHONY: test lint type-check format install check

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

check: lint type-check test
