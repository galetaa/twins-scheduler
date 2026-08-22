# Independent reproduction verification — Gate 4′

**Date:** 15 August 2026  
**Artifact:** `TWINS_SCHEDULER_GATE4P_2026-08-15.zip`  
**Artifact SHA-256:** `f4ffe60c1218b28d49e2709d630ab92d1c57e3c3aa49deb2369c3b7d924afa34`

## Clean-room procedure

The ZIP archive was extracted into a new directory that did not contain a Python virtual environment, caches, generated result files, or build outputs. The following environment was used:

```text
CPython 3.13.5
Go 1.23.2 linux/amd64
PYTHONHASHSEED=0
```

The artifact's pinned manifest was checked with `sha256sum -c`; every listed file passed.

## Re-executed checks

1. Go/Python network-semantics conformance: **PASS**, 134/134 cases.
2. Exact Gate 4′ enumeration: **PASS / CONDITIONAL GO TO GATE 5′**.
3. Full test suite without fast-reproduction skips: **38 passed**.
4. Machine-readable self-check: **PASS**.
5. Baseline safety, grammar inclusions, natural phase separations, delay boundary, replay boundary, positive control, counterfactual closures, and independent witness oracle: all **true**.

## Determinism check

The following regenerated files were byte-identical to the packaged originals:

```text
baseline_checks.json
closure_counterfactuals.json
conformance_summary.json
gate4p_decision.json
language_matrix.csv
separations.csv
theorem_checks.json
witnesses.jsonl
```

## Scope of this verification

This verifies the packaged finite-state checker, the declared bounded state spaces, serialized witnesses, counterfactual mechanism tests, and the Go/Python abstraction of pinned network admission and pending-queue behavior. It does not establish a protocol-class theorem, execute the complete `relab/hotstuff` consensus loop, or demonstrate a production vulnerability.
