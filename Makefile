.PHONY: all dev ruff lint check_style coverage test run run_docker docker_up docker_down clean

SHELL:=/bin/bash
RUN=uv run
PYTHON=${RUN} python

all:
	@echo "make dev"
	@echo "    Create dev environment."
	@echo "make ruff"
	@echo "    Run 'ruff' to lint project."
	@echo "make lint"
	@echo "    Run lint on project."
	@echo "make check_style"
	@echo "    Check code-style"
	@echo "make style"
	@echo "    Reformat the code to match the style"
	@echo "make check"
	@echo "    Check code-style, run linters, run tests"
	@echo "make coverage"
	@echo "    Run code coverage check."
	@echo "make test"
	@echo "    Run tests on project."
	@echo "make run"
	@echo "    Run development web-server using ./manage.py runserver."
	@echo "make run_docker"
	@echo "    Run development web-server using the docker image."
	@echo "make docker_up"
	@echo "    Starts all docker-compose services, except web."
	@echo "make docker_down"
	@echo "    Stop all docker-compose services."
	@echo "make initial_migration"
	@echo "    Setting up all the tables in the database from scratch."
	@echo "make clean"
	@echo "    Remove python artifacts and virtualenv"

sync:
	uv sync

lint:
	${RUN} ruff check .

lint-fix:
	${RUN} ruff check . --fix

types: sync ruff
	${RUN} mypy .

check_style: sync
	${RUN} ruff format --check .

style: sync
	${RUN} ruff format

coverage: docker_up
	${RUN} coverage run -m pytest
	${RUN} coverage xml
	${RUN} coverage html

check: check_style lint

test: sync docker_up
	${RUN} pytest . -vv

run: sync docker_up
	${PYTHON} manage.py runserver

run_docker: sync
	docker compose --profile web up --build --attach-dependencies

docker_up:
	docker compose --profile db up --build -d

docker_down:
	docker compose --profile web down

initial_migration:
	${RUN} ./manage.py migrate --skip-checks

clean: docker_down
	uv cache clean
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name "*_cache" -exec rm -rf {} +
	rm -rf *.eggs *.egg-info dist build docs/_build .cache .mypy_cache coverage/* .pytest_cache/ .ruff_cache/ report.html
