# Certifying minimum-cost phase refinement

## Why this revision is needed

A reachability counterexample and a unit-weight phase budget do not tell an
adapter designer which feasible keys to expose at minimum cost. The first
revision also left its central graph/order argument outside the mechanized
proof and supported protocol assumptions with a guarded local model.

## Resulting behavior

The revision adds weighted cost synthesis with allowed/required keys, a complete
legal model witness, and independently checked optimality or infeasibility
certificates. The exact four-role theorem connects admission choices to weighted
quorum support. A small counterexample proves non-submodularity and an unbounded
ratio for one precisely specified immediate-benefit heuristic.

Graph reversal, finite event-order realization and the Bellman certificate
principle now have Lean proofs. Separate native conformance executes unchanged
CometBFT v0.39.3 under four ordinary-operation scenarios with actual Ed25519
votes, native timeout requests, normal commits and source-integrity checks.

The article is reorganized around this constructive result. Existing timing,
frontier, concrete-model and replay material remains with its exact scope;
the detailed trace and the unit-budget illustration are in appendices.

## Evidence

- 47 Python tests and retained Go/384-row cross-language checks pass.
- Two raw-event oracle suites give 35,223 and 3,253 weighted optimum/certificate
  comparisons, with zero mismatches; 103,460 prescribed-split boundaries pass.
- A 15-case structural study produces 13 saved, independently checked optima,
  up to 48 pivots. Two configured SCC cutoffs return unknown.
- Lean 4.33.0 completes 14 jobs, audits 27 declarations, and passes independent
  kernel rechecking; source hygiene covers 22 Lean files. SMT controls give
  eight expected UNSAT and four expected SAT results.
- Native conformance passes 14 checks on 32 signed votes and 132 events.
  Independent signature/metadata audit, three repetitions and a race-detector
  execution pass.
- The official LIPIcs build has 15 main-text and 20 physical pages, with no
  overfull boxes or unresolved references/citations and embedded fonts.

`./reproduce_revision.sh` integrates all research stages, including signature
and repeatability checks, and fails on a mandatory error. Synthesis outputs and
the native semantic summary are deterministic references; raw native signatures
and receipts retain their actual timestamps and are revalidated per run.

## Scope for review

The weighted four-role correspondence, Python checker implementation and full
client refinement are not mechanized. The solver is exponential in the largest
remaining SCC and pseudo-polynomial in quotas. Costs are synthetic inputs.
Native conformance does not execute the model's mutation or demonstrate native
disagreement. The claims concern the declared finite behavioral/order contract.
