# SchedCheck Gate 5′ — scheduler-closure boundaries for locking BFT protocols

This package closes Gate 5′ of the research program that began with a review of
Twins-style BFT fault-injection coverage. The original finite-clone claim was
rejected. The surviving topic is narrower:

> **When does erasing phase/type information from a message schedule preserve
> finite agreement observations, and when does it remove the only safety
> witness?**

## Decision

```text
Gate 5′: PASS / GO TO GATE 6′
Research status: ready for full implementation in the narrowed scope
Publication status: conditional on proof hardening and fuller event-loop replay
```

## Main results

1. **Replay erasure.** Identical replay is observationally inert when handlers
   are stable-key idempotent and quorum power is keyed by validator slot.
2. **Relational closure lifting.** A local R-monotonicity condition is sufficient
   for closure-added messages to preserve unsafety; a locking repair message
   supplies an explicit failed-premise counterexample.
3. **Parametric phase separation.** For every `f≥1`, an `n=3f+1`, `q=2f+1`
   quorum-pivot construction separates one type-uniform directed graph per view
   from phase-specific delivery.
4. **Second protocol kernel.** A Tendermint-style proposal/prevote/POLKA/
   precommit/commit model reproduces the lock, valid-round, delay, replay, and
   positive-control boundaries from Gate 4′.
5. **Implementation correspondence.** Pinned CometBFT `v0.40.0` source confirms
   the lock-before-precommit and duplicate-vote premises. Go fixtures provide
   local conformance checks; no production defect is claimed.

## Reproduce

```bash
./scripts/reproduce.sh
```

The script performs exact searches, source checks, Go/Python conformance,
controlled Go fixture tests, fast regression tests, and an independent
self-check. It requires Python 3.13+ and Go; it does not require network access
or third-party Python runtime packages.

Manual core command:

```bash
PYTHONHASHSEED=0 PYTHONPATH=src:. python scripts/run_gate5p.py
```

## Key outputs

- `docs/GATE5P_REPORT.md` — integrated Russian-language report;
- `EXECUTIVE_DECISION.md` — compact decision memo;
- `spec/protocol_class.md` — formal class, grammars, closures, and scope;
- `spec/gate5p_theorems.md` — theorem and counterexample ledger;
- `results/gate5p/gate5p_decision.json` — machine-readable verdict;
- `results/gate5p/gate5p_machine_checks.json` — all decisive checks;
- `results/gate5p/tendermint_language_matrix.csv` — second-kernel state and
  observation languages;
- `results/gate5p/cross_protocol_result_matrix.csv` — transfer across kernels;
- `results/gate5p/tendermint_witnesses.jsonl` — independently replayed witnesses;
- `results/gate5p/phase_coupled_family.json` — parametric `f=1…8` regression;
- `results/gate5p/implementation_correspondence.json` — pinned source mapping and
  controlled Go fixture;
- `gate5p/prior_art_delta.md` — restrained novelty review;
- `REPRODUCTION_VERIFICATION.md` — independent clean-copy reproduction;
- `ROADMAP_GATE6P.md` — proof-hardening and external-validity gate.

## Non-claims

The package does not claim a CometBFT vulnerability, universal incompleteness of
partition schedules, universal minimality of phase-specific scheduling,
liveness completeness, exploitability, or absolute novelty.
