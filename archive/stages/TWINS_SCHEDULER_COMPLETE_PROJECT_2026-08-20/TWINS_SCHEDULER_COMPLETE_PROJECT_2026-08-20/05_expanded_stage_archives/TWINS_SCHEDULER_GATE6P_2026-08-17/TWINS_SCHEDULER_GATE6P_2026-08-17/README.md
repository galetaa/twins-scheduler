# SchedCheck Gate 6′ — proof-hardened scheduler-closure boundaries for locking BFT protocols

This package closes Gate 6′ of a research program on the safety-observation
expressiveness of BFT testing scheduler grammars.

## Decision

```text
Gate 6′: PASS / GO TO GATE 7′
Research status: ready for reproducible paper/artifact build in the narrow scope
Submission status: not yet submission-ready
```

## Frozen question

> When does erasing message phase/type information to one type-uniform directed
> endpoint graph preserve finite agreement observations, and when can the
> closure-added messages destroy the only unsafe witness?

## Gate 6′ results

1. **T1 replay erasure** and **T2 relational closure lifting** are represented by
   checked induction certificates with explicit premises and a small trusted
   proof script.
2. **T3 quorum-pivot separation** is checked by exact polynomial normalization,
   explicit branch obligations, and an independent Go `math/big` program.
3. The complete seven-premise abstraction is characterized by all 128 Boolean
   assignments.
4. A fuller two-round Go event loop implements proposal, prevote, POLKA,
   precommit, COMMIT, persistent locks, decisions, and stable logical vote keys.
5. An independent Python implementation agrees on all six terminal cases.
6. FIFO, LIFO, and 256 seeded queue orders preserve the safety boundary.

## Reproduce

Requirements:

- CPython 3.13 or later;
- Go 1.23 or later;
- `pytest` for the regression suite;
- no network access;
- no third-party Python runtime dependency.

One command:

```bash
./scripts/reproduce_gate6p.sh
```

Manual core sequence:

```bash
export PYTHONHASHSEED=0
export PYTHONPATH=src:.
python scripts/run_gate6p.py
pytest -q tests/test_gate6p_*.py
python scripts/selfcheck_gate6p.py
```

## Key files

- `docs/GATE6P_REPORT.md` — integrated Gate 6′ report;
- `EXECUTIVE_DECISION.md` — compact decision memo;
- `gate6p/PAPER_CLAIM_FREEZE.md` — allowed and prohibited claims;
- `gate6p/VALIDITY_REGISTER.md` — validity threats and controls;
- `gate6p/PRIOR_ART_REFRESH.md` — focused novelty refresh;
- `proofs_checked/` — human-readable proofs, rule files, and certificates;
- `spec/full_event_loop.md` — fuller event-loop semantics;
- `implementation_fixture/full_event_loop/` — independent Go fixture;
- `implementation_fixture/proof_crosscheck/` — Go big-integer T3 checker;
- `src/schedcheck/gate6/event_loop.py` — independent Python event loop;
- `src/schedcheck/gate6/necessity.py` — ablation and exact premise boundary;
- `src/schedcheck/gate6/proof_kernel.py` — small checked-proof kernel;
- `results/gate6p/gate6p_decision.json` — machine-readable verdict;
- `results/gate6p/gate6p_theorem_ledger.json` — theorem status;
- `results/gate6p/full_event_loop_matrix.csv` — six decisive cases;
- `results/gate6p/premise_truth_table.csv` — all 128 assignments;
- `ROADMAP_GATE7P.md` — next gate.

## Assurance boundary

The proof kernel checks dependencies, measures, arithmetic, and branches, but it
is not a mature proof assistant. The package therefore requires independent
proof review or mature-prover migration before submission.

## Non-claims

No production-client vulnerability, universal scheduler minimality, liveness
result, unbounded completeness, bug-prevalence estimate, or absolute novelty is
claimed.
