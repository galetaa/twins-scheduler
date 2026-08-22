# Gate 2 clean reproduction record

**Date:** 11 August 2026  
**Result:** PASS

A clean copy of the package was created without `.venv`, `__pycache__` or `.pyc` files. Running `./gate2/reproduce.sh`:

1. created a new uv virtual environment with CPython 3.13.5;
2. passed all nine unit/regression tests;
3. regenerated the exact pilot outputs;
4. verified every reviewed deterministic file against `results/pilot/manifest.sha256`;
5. produced byte-identical `language_summary.csv`, `k_min.csv`, `state_space.json`, `theorem_checks.json` and `unmatched_traces.jsonl` relative to the reviewed run.

The clean reproduction used no network service, external solver, blockchain node, RPC endpoint or dataset.
