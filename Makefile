.PHONY: setup pipeline train eval serve test drift

setup:
	pip install -U pip
	pip install -r requirements.txt
	pre-commit install

pipeline:
	dvc repro

train:
	dvc repro train
	echo "Done: train"

eval:
	dvc repro evaluate
	@type metrics.json 2>nul || cat metrics.json

serve:
	uvicorn service.app:app --host 0.0.0.0 --port 8000

drift:
	python monitoring/drift_report.py

test:
	pytest -q