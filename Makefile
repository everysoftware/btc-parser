run:
	python -m uvicorn src.main:app --reload

beat:
	celery -A src.celery.app beat -l info

worker:
	celery -A src.celery.app worker -l info -P solo