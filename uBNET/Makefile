.PHONY: install uninstall run test lint clean help

PYTHON := /usr/bin/python3
APP := ubnet.py

help:
	@echo "uBNET - Ubuntu Network Monitor"
	@echo ""
	@echo "Available targets:"
	@echo "  make install    - Install uBNET to ~/.local"
	@echo "  make uninstall  - Remove uBNET from ~/.local"
	@echo "  make run        - Run uBNET directly"
	@echo "  make test       - Run syntax check"
	@echo "  make lint       - Run linter (requires pylint)"
	@echo "  make clean      - Remove Python cache files"
	@echo "  make help       - Show this help message"

install:
	@./install.sh

uninstall:
	@./uninstall.sh

run:
	@$(PYTHON) $(APP)

test:
	@$(PYTHON) -m py_compile $(APP) && echo "Syntax OK"

lint:
	@pylint $(APP) --disable=C0114,C0115,C0116 || true

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@echo "Cleaned up cache files"
