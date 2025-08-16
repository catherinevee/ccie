FILE: /ccie/ccie/Makefile
----------------------------------------
# Makefile for CCIE Network Configuration Project

# Variables
PYTHON=python3
PIP=pip
VENV=venv

# Targets
.PHONY: all install clean deploy validate test

all: install

install: 
	$(PIP) install -r requirements.txt

clean:
	rm -rf $(VENV)

deploy:
	$(PYTHON) scripts/deploy/deploy.py

validate:
	$(PYTHON) scripts/deploy/validate.py

test:
	$(PYTHON) -m unittest discover -s tests/unit
	$(PYTHON) -m unittest discover -s tests/integration
----------------------------------------