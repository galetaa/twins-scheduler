# Gate 7′ mature-prover migration report

## Decision

The Gate 6′ proof obligations were independently re-encoded in SMT-LIB 2 and
executed with **Z3 4.13.3.0**.  The migration closes the specific Gate 6′ blocker
that the only machine check was a project-local certificate kernel.

It does **not** justify the phrase “the complete BFT protocol semantics are fully
mechanized.”  The Z3 package proves the encoded theorem schemas and exact
arithmetic/Boolean obligations.  Mapping a concrete implementation to the
schema premises remains a separate refinement obligation.

## Positive obligations

| File | Logic | Expected result | Meaning |
|---|---|---|---|
| `T1_REPLAY_ERASURE.horn.smt2` | CHC/HORN | one `UNSAT` | No finite derivation reaches unequal protocol-relevant configurations when duplicates stutter and first deliveries use the same deterministic transition. |
| `T2_LOCAL_VCS.smt2` | AUFLIA | four `UNSAT` results | Transitivity, increasing insertions, forward simulation, and upward closure each discharge their local verification condition. |
| `T2_PREFIX_RELATION.horn.smt2` | CHC/HORN | one `UNSAT` | The finite-prefix relation invariant cannot be violated when the local obligations are supplied. |
| `T3_QUORUM_PIVOT.smt2` | QF_LIA | one `UNSAT` | The symbolic `n=3f+1`, `q=2f+1` branch arithmetic holds for every integer `f≥1`. |
| `T6_PREMISE_CHARACTERIZATION.smt2` | QF_LIA | one `UNSAT` | The operational seven-flag model is equivalent to `S2 ∧ D ∧ T ∧ E ∧ X ∧ (S1 ∨ Rq)`. |

The complete result, version, timings, source digests, and output digests are in
`proof_outputs/smt_proof_report.json`.

## Negative controls

Four damaged obligations are required to become satisfiable:

1. replay is allowed to change only the replay-side state;
2. an inserted action is allowed to violate the increasing relation;
3. repair no longer removes the pivot from the second branch;
4. the `Rq` disjunct is incorrectly removed from T6.

All four negative controls return `SAT`.  Therefore the proof suite is sensitive
to the premises that carry the scientific mechanism; it is not a vacuous
“always UNSAT” harness.

## Assurance decomposition

The evidence now has four independently implemented routes:

- Z3 CHC/SMT encodings for T1, T2, T3, and T6;
- the small auditable Gate 6′ certificate kernel;
- exact Go `math/big` arithmetic for 1,028 values of `f`;
- independent Go and Python fuller event loops with exact six-case conformance.

These routes reduce shared implementation risk but do not eliminate shared
specification risk.  The manuscript must expose all premises before stating the
theorems and must keep the protocol-to-schema mapping auditable.

## Trusted computing base

- Z3 4.13.3.0 and its CHC/SMT engines;
- the five positive SMT-LIB files;
- the minimal C API loader in `proofs_smt/z3cli.c`;
- the interpretation connecting paper-level terms to SMT symbols;
- the host C compiler and dynamic loader for reproduction.

## Remaining non-blocking review work

An external human proof review or a later Lean/Coq/Isabelle development would
increase assurance, especially for the mapping between the abstract repair
transition and realistic protocol executions.  It is recommended before final
submission but is no longer a Gate 7′ execution blocker because the mature SMT
migration has been run and the negative controls pass.
