# Independent audit integration ledger

This is the current integration status, based only on commands executed in the canonical repository. The historical audit and its former status text remain unchanged in provenance.

| Audit observation | Implemented correction | Canonical source | Manuscript | Fresh evidence | Status |
|---|---|---|---|---|---|
| Replay future noninterference was informal | Explicit projection containing processed keys; state/output congruence; duplicate stutter and silence | `formal/lean/SchedulerClosure/ReplayErasure.lean` | §7, Theorem 3 | Lean build/axioms; T1 SMT; certificate kernel | PASS |
| Projected stutter alone was insufficient | Retained `X,X,Y` hidden-bit counterexample | same; `formal/smt/negative_controls/T1_hidden_state_XXY_counterexample.smt2` | §7 | Lean theorem; SAT control; independent full=1/erased=0 | PASS |
| Closure proof blurred merged execution and legal grammar trace | Split merged-trace lemma from legal scheduler-language theorem | `formal/lean/SchedulerClosure/ClosureLifting.lean` | §3, Lemma 1 and Theorem 1 | Lean; three UNSAT VCs; independent finite enumeration | PASS |
| Quorum-pivot statement omitted shared view/phase ordering/domain | Ten explicit premises state shared sender/receiver/view, distinct phases, exact `E<C0<R<C1`, and complete Boolean edge domain | `QuorumPivotCriterion.lean`; `SchedulerSemantics.lean`; `CometBFTInstantiation.lean` | §4.1, Theorem 2 | Lean; kernel; Python/Go; SAT damaged controls | PASS |
| Certificate conflict was not connected to correct decisions | Added irreversible correct-decision transitions and agreement oracle | `CometBFTInstantiation.lean`; Python/Go event models | §§4 and 6 | Lean and cross-language terminal observations | PASS |
| Seven-premise result omitted its operational equation | Included `U(e,r)` and paper derivation before enumeration | `formal/lean/SchedulerClosure/PremiseBoundary.lean` | §5, Proposition 1 | Lean; two UNSAT VCs; all 128 assignments | PASS |
| `UnsafeObs` mixed state and observation types | Applied `Unsafe` to `last(τ)` before applying `O` | `formal/lean/SchedulerClosure/UnsafeObservations.lean` | §2.2 | Lean and independent typing check | PASS |
| Mature prover had not been compiled | Repaired source incompatibilities without changing paper statements; pinned Lean 4.33.0 | `formal/lean/`; root Lean files | §8.2 | `lake build`, axiom audit and `leanchecker` exit 0 | PASS |

Coq is retained only as a secondary archival mirror. The primary assurance claim rests on the successful Lean build; SMT and certificate kernels are supporting checks.
