# Paper theorem to artifact mapping

This map follows the revised manuscript in `manuscript/markdown/manuscript.md`
and its appendices. **Theorem 3 is now the repair-frontier characterization;
Corollary 1 is the minimum phase budget for unit weights.** The old replay theorem and
seven-flag characterization are supporting Appendix B results. Historical
T1/T2/T3/T6 labels remain provenance locators.

The names below are Lean declarations, not assertions of a larger
mechanization scope. In particular, the new namespace
`SchedulerClosure.RepairFrontier` formalizes the arbitrary behavioral
contract, quota arithmetic, and a small persistent-output machine. It does
not define the repair graph, prove a linear-extension theorem, or run the
CometBFT client.

## Revised main results

| Paper item / ledger ID | Formal declaration or other evidence | Exact assurance boundary |
|---|---|---|
| Theorem 1: legal relational preservation / C1 | `SchedulerClosure.merged_trace_lifting`; `SchedulerClosure.legal_scheduler_closure_preserves_unsafe` in `ClosureLifting.lean` | Sufficient simulation/closure theorem under its relation and legal-target hypotheses. It does not make an otherwise illegal inserted trace legal. Historical obligation T2. |
| Theorem 2: behavioral quorum-pivot separation / C2 | `SchedulerClosure.RepairFrontier.behavioral_quorum_pivot_separation` | Quantifies over arbitrary state type, execution function, first/second-vote functions, and unsafe predicate. First-vote necessity, positive persistence, timely repair, one-short bases, and the observation contract are explicit hypotheses. Their realization by a legal protocol/scheduler is a separate obligation. |
| Independence of the persistence premise / C2 | `SchedulerClosure.RepairFrontier.persistence_hypothesis_independent` | A specific negative-control function satisfies first-vote necessity and timely repair but has no fine unsafe witness because it never emits the second vote. This is not a universal independence classification. |
| Lemma 1: compatible late repairs / C11 | Paper alternating-cycle proof; finite checks in `repair_frontier.py` and `frontier_summary.json` | **No Lean declaration.** The correspondence between adding `V_i < R_i` constraints and acyclicity of the induced repair graph is proved in the paper and tested over the declared finite orders. |
| Theorem 3: weighted graph-to-execution characterization / C11 | Paper proof using Lemma 1, independent behavioral contracts, and complete opportunity-order coverage | **No Lean formalization of this graph-to-execution theorem.** Its weighted subset conditions and operational realization are not established by the arithmetic declarations below. |
| Theorem 3: unit-weight quota equivalence / C11 | `SchedulerClosure.RepairFrontier.directed_unsafe_iff`; `SchedulerClosure.RepairFrontier.strict_separation_iff` | Lean proves the exact inequality for an abstract `capacity <= pivots` and the associated count abstraction. Establishing `capacity = alpha(H)` and attainable reusable sets belongs to the paper graph argument. |
| Corollary 1: minimum phase budget for unit weights / C12 | `SchedulerClosure.RepairFrontier.split_capacity_bound`; `SchedulerClosure.RepairFrontier.minimum_phase_splits` | For unit weights, Lean proves budget existence/minimality once the optimal capacity is supplied as `min(pivots, capacity + splits)`. Choosing a maximum acyclic set and attaining that graph capacity is a paper finite-set argument, not a Lean graph theorem. |
| Weighted common-frontier interval, Equation (5) / C14 | `SchedulerClosure.RepairFrontier.weighted_admission_interval`; `SchedulerClosure.RepairFrontier.weighted_granularity_counterexample` | Lean retains an arbitrary attainable-subset-weight predicate and proves the interval equivalence under its weight bound. It also checks the indivisible `(2,2)` counterexample. The scheduling reduction to a common frontier and interpretation by actual subsets are separate arguments. |
| Signature-issuance versus collector timing / C15 | `SchedulerClosure.RepairFrontier.repair_preserves_signed_output`; `SchedulerClosure.RepairFrontier.late_repair_before_certificate_is_unsafe`; `SchedulerClosure.RepairFrontier.repair_before_second_vote_is_safe`; `SchedulerClosure.RepairFrontier.closed_edge_still_permits_second_vote` | These declarations concern the explicitly defined small `OutputState/OutputEvent` machine. They prove preserved signed output and evaluate the displayed control traces. They do not prove transition correspondence with the concrete Python model or the client. |
| Section 6: complete four-validator witness / C13 | `src/python/twins_scheduler/concrete_trace.py`; `tests/unit/test_concrete_trace.py`; `results/new/concrete_trace.json` | **Executable, not a Lean transition proof.** Twelve cases and fourteen dedicated tests; actual authenticated signer sets, guarded local transitions, legal timeout evidence, explicit envelopes and block relays. The separate FIFO-compatible gossip control changes its declared message-routing skeleton. |
| Appendix A: NP-completeness of abstract coarse reachability / C16 | Paper reduction from independent set by symmetric graph orientation, with polynomial witness verification | **No Lean declaration.** The input is the variable-size independent-pivot opportunity schema. The fixed four-validator example and production-client reachability are outside this complexity claim. |

## Retained supporting results and historical declarations

| Revised location / ledger ID | Retained declaration | Interpretation after revision |
|---|---|---|
| Section 3.1: original single-pivot quorum family / C3 | `SchedulerClosure.parametric_family_separation` in `ParametricFamily.lean` | Historical T3 arithmetic and terminal Boolean classification for the original one-pivot family. It is not the revised Corollary 1 and does not formalize the new multi-pivot participant allocation. |
| Historical fixed Boolean structural model / C2, C3 | `SchedulerClosure.quorum_pivot_separation_criterion`; `SchedulerClosure.criterion_policy_separation` in `QuorumPivotCriterion.lean` | The old model defines `pivotAtSecond e r := e && !r`. Those proofs check that defined classifier. The corrected arbitrary-contract proof for current Theorem 2 is the new `RepairFrontier.behavioral_quorum_pivot_separation`, not these declarations. |
| Section 7.1: prior Tendermint-style classifier / C5 | `SchedulerClosure.bounded_baseline_safe`; `SchedulerClosure.bounded_missing_lock_phase_specific_unsafe`; `SchedulerClosure.bounded_missing_lock_directed_safe`; `SchedulerClosure.bounded_tendermint_refines_quorum_pivot` in `CometBFTInstantiation.lean` | These theorems concern `executeTendermintBounded`, which directly computes terminal flags. Despite its historical name, `bounded_tendermint_refines_quorum_pivot` proves matching unsafe/safe classifications, **not transition refinement**. The 384-row Python/Go comparison validates this old model, not the new event-level trace. |
| Appendix B.1: supporting replay-erasure proposition / C6 | `SchedulerClosure.replay_erasure_with_outputs`; `SchedulerClosure.replay_erasure_state_observation` in `ReplayErasure.lean` | State/output congruence, projected duplicate stutter, and output silence yield the finite trace statement. Historical T1; no longer paper Theorem 3. |
| Appendix B.1: hidden-state/output controls / C7 | `SchedulerClosure.hidden_state_counterexample`; `SchedulerClosure.hidden_state_breaks_output_congruence` | Specific finite counterexamples to weaker erasure assumptions. Historical T1 controls. |
| Appendix B.2: seven-flag diagnostic / C4 | `SchedulerClosure.strictSeparation_eq_characterization`; `SchedulerClosure.strictSeparation_iff_three` in `PremiseBoundary.lean` | Exact Boolean calculation with three satisfying assignments out of 128. Historical T6. It does not establish the revised graph characterization or justify repair merely before a collector. |
| Section 2: unsafe-observation typing / C8 | `SchedulerClosure.UnsafeObservationSet`; `SchedulerClosure.unsafe_observation_has_unsafe_terminal` | `Unsafe` is applied to terminal state before observation projection. |
| Section 2: original stable admission filter / C9 | `SchedulerClosure.typeClosure`; `SchedulerClosure.delivered_was_emitted`; `SchedulerClosure.delivered_preserves_order`; `SchedulerClosure.enabling_implies_closed_edge` in `SchedulerSemantics.lean` | Already-emitted envelopes, retained order, and shared-edge closure. This module does not formalize the expanded partial-order language of Theorem 3. |

## Build and audit gate

The project imports `SchedulerClosure.RepairFrontier` through
`formal/lean/SchedulerClosure.lean`; the revision's selected main declarations
are listed in `formal/lean/AxiomAudit.lean`. The intended primary toolchain is
Lean 4.33.0.

**Scientific validation gate: PASS.** The integrated project built on
Lean 4.33.0 (12 jobs), the selected 20-declaration axiom audit passed, source
hygiene passed, and `leanchecker SchedulerClosure` independently rechecked
the resulting dependency closure with exit status 0. Supporting validation
also passed: 35 Python tests, Go tests, and the existing SMT obligations
(8 positive UNSAT results and 4 negative-control SAT results using pinned
`z3-solver` 4.13.3.0).

`results/generated/lean_verification.json` records successful Lean command
exits and SHA-256 hashes of the Lean source files. The report assembler
checks that receipt against the current source hashes before producing
`results/generated/formal_verification.json`; an old retained PASS report
cannot establish a fresh build. Detailed logs are `build_logs/lean_build.log`,
`build_logs/lean_axiom_audit.log`, and `build_logs/leanchecker.log`; the axiom
interpretation is in `formal/lean/AXIOM_REPORT.md`. Exact claim boundaries
and statuses are recorded in `docs/CLAIM_EVIDENCE_LEDGER.md` and its CSV.
Typesetting and PDF inspection are separate from this scientific gate.

This successful gate does not mechanize graph reversal, graph-to-execution
correspondence, graph-capacity attainment, the complexity reduction, and
the production-client trace; they remain outside the claimed Lean formalization.
