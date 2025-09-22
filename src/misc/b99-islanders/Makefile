.DEFAULT_GOAL := run

.PHONY: bootstrap
bootstrap:
	pipenv install

.PHONY: run
run: bootstrap
	pipenv run mypy --ignore-missing-imports main.py
	pipenv run python main.py
