.PHONY: test lint check build

test:
	python -m pytest

lint:
	python scripts/clean_code_lint.py
	ruff check src experiments tests

check: test lint

build:
	python -m build
