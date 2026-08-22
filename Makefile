SHELL := /bin/bash

.PHONY: bootstrap test formal paper reproduce verify release

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

verify:
	./scripts/verify_provenance.sh
	./scripts/verify_results.sh

release:
	./scripts/package_release.sh
