SHELL := /bin/bash

.PHONY: bootstrap test formal paper revision synthesis native reproduce verify release

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
	$(MAKE) synthesis

synthesis:
	uv run python scripts/run_refinement_synthesis.py --study
	uv run python scripts/check_synthesis_order_oracle.py

native:
	./scripts/run_native_conformance.sh
	uv run --extra native-audit python experiments/native_cometbft/audit_evidence.py
	python3 experiments/native_cometbft/check_repeatability.py

verify:
	./scripts/verify_provenance.sh
	./scripts/verify_results.sh

release:
	./scripts/package_release.sh
