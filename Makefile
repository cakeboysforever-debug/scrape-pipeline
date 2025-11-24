PYTHON ?= python3
VENV ?= .venv
REQ ?= requirements.txt
KEYWORDS ?= "weight loss" "cybersecurity" "passive income"
LIMIT ?= 5
OUTPUT ?= data/latest

ACTIVATE = . $(VENV)/bin/activate &&
PIPELINE = $(ACTIVATE) PYTHONPATH=src $(PYTHON) -m scrape_pipeline.pipeline

.DEFAULT_GOAL := help
.PHONY: help install preview run clean

help:
	@echo "Usage: make <target> [LIMIT=5] [KEYWORDS=\"k1\" \"k2\"] [OUTPUT=data/latest]"
	@echo "Targets:"
	@echo "  install  - create $(VENV) and install dependencies from $(REQ)"
	@echo "  preview  - dry run with --preview and the configured LIMIT/KEYWORDS"
	@echo "  run      - execute pipeline and write outputs to OUTPUT"
	@echo "  clean    - remove $(VENV)"

# Create the virtual environment and install dependencies once.
$(VENV)/.deps-installed: $(REQ)
	$(PYTHON) -m venv $(VENV)
	$(ACTIVATE) pip install -r $(REQ)
	touch $@

install: $(VENV)/.deps-installed

preview: $(VENV)/.deps-installed
	$(PIPELINE) --preview --limit $(LIMIT) --keywords $(KEYWORDS)

run: $(VENV)/.deps-installed
	$(PIPELINE) --limit $(LIMIT) --keywords $(KEYWORDS) --output-dir $(OUTPUT)

clean:
	rm -rf $(VENV)
