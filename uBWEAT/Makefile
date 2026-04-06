.PHONY: install uninstall run clean help

help:
	@echo "uBWEAT - Ubuntu Weather Monitor"
	@echo ""
	@echo "Available targets:"
	@echo "  make install    - Install uBWEAT to system"
	@echo "  make uninstall  - Remove uBWEAT from system"
	@echo "  make run        - Run uBWEAT directly"
	@echo "  make clean      - Remove temporary files"
	@echo "  make help       - Show this help message"

install:
	@chmod +x install.sh
	@./install.sh

uninstall:
	@chmod +x uninstall.sh
	@./uninstall.sh

run:
	@/usr/bin/python3 ubweat.py

clean:
	@rm -rf __pycache__
	@rm -f *.pyc
	@echo "Cleaned temporary files"
