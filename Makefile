# Author: Nick Russo
# Purpose: Provide simple "make" targets for developers
# See README for details about each target.

# Default goal runs the "test" target
.DEFAULT_GOAL := test

.PHONY: test
test: lint

.PHONY: lint
lint:
	@echo "Starting  lint"
	find . -maxdepth 1 -name "*.py" | xargs bandit
	find . -maxdepth 1 -name "*.py" | xargs black -l 85 --check
	@echo "Completed lint"