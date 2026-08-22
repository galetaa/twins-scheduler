# Independent audit integration ledger

This ledger maps every blocking observation in the independent audit to a concrete post-audit definition, theorem, manuscript location, executable check, and remaining assurance boundary.

| Audit observation | Implemented correction | Formal source | Manuscript location | Executed evidence | Status |
|---|---|---|---|---|---|
| T1 used an informal future-noninterference phrase | Introduced a relevant projection containing processed stable keys; added transition congruence, projected duplicate stutter, silent relevant output, and a state-based observer | `formal/lean/SchedulerClosure/T1ReplayErasure.lean`; `formal/coq/T1ReplayErasure.v`; `formal/smt_post_audit/positive/T1_*` | Section 6.1 | Independent finite check; project-local structural-induction certificate; Z3 one-step VCs | PASS at project-kernel/SMT level; Lean/Coq source unbuilt |
| Immediate projected stutter is insufficient | Added the exact `X,X,Y` hidden-state counterexample | T1 Lean/Coq source and `formal/smt_post_audit/negative_controls/T1_hidden_state_XXY_counterexample.smt2` | Section 6.2 | Independent script reports full=1, erased=0; Z3 returns SAT | PASS |
| T2 notation needed to expose the consumed-action prefix invariant | Defined inserted and retained steps, transitive relation, forward simulation, and upward-closed unsafety explicitly | `T2ClosureLifting.lean`, `T2ClosureLifting.v`, T2 SMT VCs | Section 3 | Independent finite prefix check; project-local induction; three Z3 UNSAT VCs | PASS |
| T3 did not state that E and R share a view | Envelopes carry the same sender, receiver, and view; only their phase labels differ | `T3QuorumPivot.lean`, `T3QuorumPivot.v` | Section 4.1 | Independent bounded model and project kernel | PASS |
| T3 did not force R before the second certificate opportunity | Fixed the complete order `E<C0<R<C1` | same | Section 4.1 | Independent model; project kernel; late-repair negative control is SAT | PASS |
| T3 did not define the complete directed domain | Defined `G_D` as exactly one Boolean edge bit over the shared endpoint and view | same | Sections 4.1--4.2 | Exhaustive off/on checks; other-view negative control is SAT | PASS |
| T3 stopped at conflicting certificates | Added irreversible decisions of two distinct correct replicas and defined agreement violation over those decisions | same | Section 4.1 | Independent model; project kernel | PASS |
| T6 omitted the operational equation | Included the exact `U(e,r)` equation and derived strict separation from it | `T6PremiseBoundary.lean`, `T6PremiseBoundary.v`, T6 SMT | Section 5 | Independent 128-assignment enumeration; project kernel; Z3 equivalence and exact-pattern checks | PASS |
| Author SMT/Lean/executable artifacts required separate checking | Reran inherited Gate 8 reproduction; added independent script, independent source hashes, post-audit SMT encodings, and damaged controls | `results/rechecks`, `proof_review`, `formal/smt_post_audit` | Section 8.4 | Gate 8 PASS; independent PASS; Z3 8 UNSAT / 4 SAT; project kernel PASS | PASS except mature-prover build |

## Residual assurance boundary

The post-audit result is actually checked by an independent executable model, Z3, and an executed project-local proof-certificate kernel. Parallel Lean and Coq developments contain no `sorry`, `admit`, `Admitted`, or explicit new axioms, but their compilers were unavailable and direct downloads were blocked by the execution environment. Consequently the archive does not call them kernel-built. A clean Lean or Coq build remains the only proof-assurance item not executed here.
