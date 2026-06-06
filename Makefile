.PHONY: install test serve docker-build docker-up docker-down docker-logs docker-test

install:
	python -m pip install --upgrade pip
	pip install -e '.[dev]'

test:
	ruff check .
	mypy src
	pytest -q --cov=src --cov-report=term-missing

serve:
	uvicorn consumer_service.api:app --host 0.0.0.0 --port 8010

docker-build:
	docker build -t python-consumer-service:local .

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f consumer-service

docker-test:
	docker-compose exec consumer-service pytest -q

docker-shell:
	docker-compose exec consumer-service /bin/bash
