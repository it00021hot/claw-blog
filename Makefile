.PHONY: fetch
fetch:
	@echo "Running article fetcher..."
	PYTHONPATH=. python scripts/main.py

.PHONY: fetch-dry-run
fetch-dry-run:
	@echo "Running article fetcher (dry run)..."
	PYTHONPATH=. python scripts/main.py --dry-run

.PHONY: fetch-verbose
fetch-verbose:
	@echo "Running article fetcher (verbose)..."
	PYTHONPATH=. python scripts/main.py --verbose
