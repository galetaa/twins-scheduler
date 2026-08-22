# SchedCheck Gate 4′: natural locking scheduler separations

This package closes Gate 4′ of a research program on safety-preserving
expressiveness of Twins-style scheduler grammars.

## Result

A bounded certificate-driven locking kernel with `n=4`, `f=1` was checked under:

```text
G_P_PARTITION
G_D_DIRECTED_VIEW
G_D1_DIRECTED_DELAY1
G_T_TYPE_SPECIFIC
G_M_PER_MESSAGE
G_R_PER_MESSAGE_REPLAY1
```

The correct baseline is safe in every checked grammar. Three natural locking
mutants are invisible to a type-uniform directed graph but visible to
phase/type-specific scheduling. One-view delayed commit evidence exposes two of
those mutants; timeout-certificate confusion still requires inbound phase
separation. A duplicate-signer-counting mutant requires replay. A validation
omission is visible already under partitions and serves as a positive control.

**Decision:** `PASS / CONDITIONAL GO TO GATE 5′`. The overall research status
remains `ТРЕБУЕТ СУЖЕНИЯ` until a protocol-class theorem and a second natural
protocol instantiation exist.

## Reproduce

```bash
./scripts/reproduce_gate4p.sh
```

Manual commands:

```bash
PYTHONPATH=src:. PYTHONHASHSEED=0 python scripts/run_conformance.py
PYTHONPATH=src:. PYTHONHASHSEED=0 python scripts/run_gate4p.py
PYTHONPATH=src:. PYTHONHASHSEED=0 pytest -q
PYTHONPATH=src:. PYTHONHASHSEED=0 python scripts/selfcheck_gate4p.py
```

Python runtime dependencies: none. Executable source conformance requires Go.

## Key outputs

- `docs/GATE4P_REPORT.md` — integrated report;
- `spec/locking_kernel.md` — exact model;
- `spec/characterization_conjecture.md` — Gate 5′ proof obligations;
- `results/gate4p/language_matrix.csv` — all state/observation counts;
- `results/gate4p/separations.csv` — strict scheduler separations;
- `results/gate4p/witnesses.jsonl` — minimal witnesses;
- `results/gate4p/closure_counterfactuals.json` — mechanism tests;
- `results/gate4p/theorem_checks.json` — machine-readable claims;
- `results/gate4p/conformance_summary.json` — Go/Python conformance;
- `gate4p/source_verification.md` — pinned-source mapping;
- `ROADMAP_GATE5P.md` — next gate.

## Non-claims

The package does not claim a HotStuff vulnerability, a defect in
`relab/hotstuff`, universal incompleteness of partitions, or novelty of richer
fault-injection APIs. The bounded result is evidence for a formal
characterization question, not a production security finding.
