VENV ?= D:/code/venvs/DataEngExam
PY := $(VENV)/Scripts/python.exe
PIP := $(PY) -m pip

.PHONY: setup run

setup:
	@if not exist "$(PY)" (py -3 -m venv "$(VENV)")
	$(PY) -m pip install --upgrade pip
	$(PY) -m pip install -r requirements.txt

run: #all etl
	$(PY) -m etl.load_data
	$(PY) -m etl.preprocess   results/raw_data.csv
	$(PY) -m etl.train_model  results/data_prepared.csv
	$(PY) -m etl.evaluate     results/model.pkl
	$(PY) -m etl.upload_results

