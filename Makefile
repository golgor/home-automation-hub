.PHONY: all dev ruff lint check_style coverage test run run_docker docker_up docker_down clean

SHELL:=/bin/bash
RUN=rye run
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

dev:
	rye sync

lint:
	rye lint

lint-fix:
	rye lint --fix

types: dev ruff
	${RUN} mypy .

check_style: dev
	rye fmt --check

style: dev
	rye fmt

coverage: docker_up
	${RUN} coverage run -m pytest
	${RUN} coverage xml
	${RUN} coverage html

check: check_style lint

test: dev docker_up
	${RUN} pytest . -vv

run: dev docker_up
	${PYTHON} manage.py runserver

run_docker: dev
	docker compose --profile web up --build --attach-dependencies

docker_up:
	docker compose --profile db up --build -d

docker_down:
	docker compose --profile web down

initial_migration:
	${RUN} ./manage.py migrate --skip-checks

clean: docker_down
	poetry env remove --all
	find -type d | grep __pycache__ | xargs rm -rf
	find -type d | grep .*_cache | xargs rm -rf
	rm -rf *.eggs *.egg-info dist build docs/_build .cache .mypy_cache coverage/* .pytest_cache/ .ruff_cache/ report.html
