# uBCPU Makefile

.PHONY: install uninstall run clean help

help:
	@echo "uBCPU - Ubuntu CPU Monitor"
	@echo ""
	@echo "Usage:"
	@echo "  make install    - Install uBCPU to ~/.local"
	@echo "  make uninstall  - Remove uBCPU"
	@echo "  make run        - Run uBCPU directly"
	@echo "  make clean      - Remove generated files"
	@echo "  make help       - Show this help message"

install:
	@./install.sh

uninstall:
	@./uninstall.sh

run:
	@python3 ubcpu.py

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "Cleaned generated files."
