SHELL:=/usr/bin/env bash

.PHONY: format
format:
	black .
	isort .
	pycln .

.PHONY: lint
lint:
	mypy .

.PHONY: style
style: format lint

.PHONY: unit
unit:
	pytest

.PHONY: test
test: style unit
