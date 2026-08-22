# Twins Gate 0–3 closure package

This package executes the blocking Gate 0–3 review for the finite-clone Twins candidate. It contains the three input reports, literature/claim audit, corrected formal model, exact bounded pilot, tests, machine-readable results, and the final no-go decision.

## Reproduce against the reviewed baseline

```bash
./gate2/reproduce.sh
```

Equivalent explicit commands:

```bash
uv run python -m unittest discover -s tests -v
PYTHONHASHSEED=0 uv run python scripts/run_pilot.py --config configs/pilot.toml
sha256sum -c results/pilot/manifest.sha256
```

The normal pilot run does **not** replace the expected manifest. After an intentional reviewed change, regenerate it with:

```bash
PYTHONHASHSEED=0 uv run python scripts/run_pilot.py \
  --config configs/pilot.toml --update-manifest
```

## Decisions

- Integrated report: `docs/GATE0_3_CLOSURE_REPORT.md`
- Gate table: `GATE_STATUS.csv`
- Gate 3 decision: `results/pilot/decision.md`
- Conditional next candidate: `docs/CONCRETE_HARNESS_PIVOT_CHARTER.md`

The executable pilot is standard-library-only and does not contact a blockchain network, RPC endpoint, or external dataset.
