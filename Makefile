
.PHONY: setup run api test fmt docker-build docker-run unit

PY=python

setup:
	$(PY) -m venv .venv && . .venv/bin/activate && pip install -U pip && pip install -r requirements.txt

run:
	$(PY) -m uvicorn src.app.main:app --host 0.0.0.0 --port 8000 --reload

api: run

test:
	pytest -q

docker-build:
	docker build -t modr:latest .

docker-run:
	docker run --rm -p 8000:8000 modr:latest

unit:
	$(PY) -m pytest tests/test_smoke.py -q
