.PHONY: install uninstall run clean help

help:
	@echo "uBTIME - Ubuntu World Clock"
	@echo ""
	@echo "Available targets:"
	@echo "  make install    - Install uBTIME to system"
	@echo "  make uninstall  - Remove uBTIME from system"
	@echo "  make run        - Run uBTIME directly"
	@echo "  make clean      - Remove temporary files"
	@echo "  make help       - Show this help message"

install:
	@chmod +x install.sh
	@./install.sh

uninstall:
	@chmod +x uninstall.sh
	@./uninstall.sh

run:
	@/usr/bin/python3 ubtime.py

clean:
	@rm -rf __pycache__
	@rm -f *.pyc
	@echo "Cleaned temporary files"
