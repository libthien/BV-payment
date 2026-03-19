.PHONY: install run test clean

install:
	pip install -r requirements.txt

run:
	python app.py

dev:
	FLASK_ENV=development python app.py

test:
	pytest tests/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf venv/

lint:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	python -m pylint app.py

format:
	black .
	isort .

init:
	python -m venv venv
	.\venv\Scripts\activate && pip install -r requirements.txt

deploy:
	gunicorn -b 0.0.0.0:8000 app:app
