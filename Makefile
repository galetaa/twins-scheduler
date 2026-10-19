SHELL := /bin/bash

.PHONY: bootstrap test formal paper revision reproduce verify release

bootstrap:
	./scripts/bootstrap.sh

test:
	./scripts/test_all.sh

formal:
	./scripts/build_formal.sh

paper:
	./scripts/build_paper.sh

reproduce:
	./reproduce.sh

revision:
	uv run python scripts/run_repair_frontier.py
	uv run python scripts/run_concrete_trace.py

verify:
	./scripts/verify_provenance.sh
	./scripts/verify_results.sh

release:
	./scripts/package_release.sh
