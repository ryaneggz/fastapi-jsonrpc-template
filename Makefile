.PHONY: run

run:
	uvicorn app.main:app --reload --port 8000

test:
	python client_example.py