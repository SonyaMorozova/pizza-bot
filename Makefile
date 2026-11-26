.PHONY: run test lint format typecheck check

run:
	python -m bot

test:
	python -m unittest discover -s tests -v

lint:
	ruff check .

format:
	ruff format .

typecheck:
	mypy bot

check:
	ruff format --check .
	ruff check .
	mypy bot
	python -m unittest discover -s tests -v