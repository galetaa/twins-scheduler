SHELL := /bin/bash

.PHONY: bootstrap test formal paper revision synthesis transition scaled native reproduce verify release

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
	$(MAKE) transition
	$(MAKE) scaled

synthesis:
	uv run python scripts/run_refinement_synthesis.py --study
	uv run python scripts/check_synthesis_order_oracle.py

transition:
	uv run python scripts/run_transition_study.py
	uv run python scripts/run_transition_bridge.py --study
	uv run python scripts/check_transition_oracle.py
	uv run python scripts/check_transition_specialization.py

scaled:
	uv run python scripts/run_scaled_study.py

native:
	./scripts/run_native_conformance.sh
	uv run --extra native-audit python experiments/native_cometbft/audit_evidence.py
	python3 experiments/native_cometbft/check_repeatability.py

verify:
	./scripts/verify_provenance.sh
	./scripts/verify_results.sh

release:
	./scripts/package_release.sh
