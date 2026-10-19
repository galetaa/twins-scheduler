# Paper theorem to artifact mapping

This map follows the revised manuscript in `manuscript/markdown/manuscript.md`
and its appendices. **Theorem 3 is the repair-frontier characterization;
Corollary 1 is the minimum phase budget for unit weights; Theorem 4 is the
weighted refinement characterization; Theorem 5 is certificate soundness.**
The old replay theorem and seven-flag characterization are supporting
Appendix B results. Historical T1/T2/T3/T6 labels remain provenance locators.

The names below are Lean declarations, not assertions of a larger
mechanization scope. `SchedulerClosure.RepairFrontier` formalizes the arbitrary
behavioral contract, quota arithmetic and a small persistent-output machine.
`SchedulerClosure.GraphRealization` now supplies the full graph-reversal and
finite event-order existence proofs. `SchedulerClosure.CertificateOptimality`
proves the generic lower-bound certificate principle. None of these modules
runs or refines the production CometBFT client.

## Revised main results

| Paper item / ledger ID | Formal declaration or other evidence | Exact assurance boundary |
|---|---|---|
| Theorem 1: legal relational preservation / C1 | `SchedulerClosure.merged_trace_lifting`; `SchedulerClosure.legal_scheduler_closure_preserves_unsafe` in `ClosureLifting.lean` | Sufficient simulation/closure theorem under its relation and legal-target hypotheses. It does not make an otherwise illegal inserted trace legal. Historical obligation T2. |
| Theorem 2: behavioral quorum-pivot separation / C2 | `SchedulerClosure.RepairFrontier.behavioral_quorum_pivot_separation` | Quantifies over arbitrary state type, execution function, first/second-vote functions, and unsafe predicate. First-vote necessity, positive persistence, timely repair, one-short bases, and the observation contract are explicit hypotheses. Their realization by a legal protocol/scheduler is a separate obligation. |
| Independence of the persistence premise / C2 | `SchedulerClosure.RepairFrontier.persistence_hypothesis_independent` | A specific negative-control function satisfies first-vote necessity and timely repair but has no fine unsafe witness because it never emits the second vote. This is not a universal independence classification. |
| Lemma 1: compatible late repairs / C11 | `SchedulerClosure.GraphRealization.repair_graph_reversal_iff`; `SchedulerClosure.GraphRealization.finite_acyclic_iff_schedule`; `SchedulerClosure.GraphRealization.repair_graph_iff_realizable_schedule`; `SchedulerClosure.GraphRealization.repair_graph_from_covers_iff_schedule` | **The graph/order bridge is now mechanized.** For any transitive irreflexive precedence relation with disjoint repair/vote event kinds, adding the selected `V_i < R_i` requests is acyclic exactly when the induced repair graph is acyclic. A complete finite enumeration yields injective times respecting every original edge and every request. The cover-edge theorem derives transitive reachability without deleting suppressed opportunities. No capacity or schedule-existence premise is assumed. |
| Theorem 3: weighted graph-to-execution characterization / C11 | The four `GraphRealization` results above; paper proof connecting them to independent behavioral contracts, certificate weights and complete opportunity-order coverage | Event-order realizability is machine-checked. The correspondence from an event order to the weighted certificate-support inequalities and unsafe observations is a paper argument under explicit behavioral assumptions. There is no Lean refinement of the Python interpreter or the client. |
| Theorem 3: unit-weight quota equivalence / C11 | `SchedulerClosure.RepairFrontier.directed_unsafe_iff`; `SchedulerClosure.RepairFrontier.strict_separation_iff` | Lean proves the exact inequality for an abstract `capacity <= pivots` and the associated count abstraction. The graph module proves realization of each acyclic reusable set; maximizing its cardinality and combining that maximum with the participant-allocation argument remain paper finite-set reasoning. |
| Corollary 1: minimum phase budget for unit weights / C12 | `SchedulerClosure.RepairFrontier.split_capacity_bound`; `SchedulerClosure.RepairFrontier.minimum_phase_splits` | For unit weights, Lean proves budget existence/minimality once the optimal capacity is supplied as `min(pivots, capacity + splits)`. Choosing a maximum acyclic set and attaining that graph capacity is a paper finite-set argument, not a Lean graph theorem. |
| Weighted common-frontier interval, Equation (5) / C14 | `SchedulerClosure.RepairFrontier.weighted_admission_interval`; `SchedulerClosure.RepairFrontier.weighted_granularity_counterexample` | Lean retains an arbitrary attainable-subset-weight predicate and proves the interval equivalence under its weight bound. It also checks the indivisible `(2,2)` counterexample. The scheduling reduction to a common frontier and interpretation by actual subsets are separate arguments. |
| Signature-issuance versus collector timing / C15 | `SchedulerClosure.RepairFrontier.repair_preserves_signed_output`; `SchedulerClosure.RepairFrontier.late_repair_before_certificate_is_unsafe`; `SchedulerClosure.RepairFrontier.repair_before_second_vote_is_safe`; `SchedulerClosure.RepairFrontier.closed_edge_still_permits_second_vote` | These declarations concern the explicitly defined small `OutputState/OutputEvent` machine. They prove preserved signed output and evaluate the displayed control traces. They do not prove transition correspondence with the concrete Python model or the client. |
| Theorem 4: weighted refinement characterization | `src/python/twins_scheduler/refinement_synthesis.py`; `docs/research/REFINEMENT_SYNTHESIS.md`; paper proof using mechanized Lemma 1 | **The four-role support correspondence remains a paper proof.** Split keys, unsplit jointly reusable keys, first-contributing keys and closed second-contributing keys partition the pivots. A first-contributing role guarantees first support but may acquire additional second support in the constructed order. Allowed/required keys, positive vote weights and nonnegative control costs are explicit. The input-to-schedule theorem is conditional on the independent-pivot contract. |
| Theorem 5: certificate soundness | `SchedulerClosure.CertificateOptimality.bellman_path_lower_bound`; `SchedulerClosure.CertificateOptimality.certified_witness_is_minimum`; `SchedulerClosure.CertificateOptimality.certified_infeasibility` | **The Bellman certificate principle is mechanized.** Every actual transition must satisfy its finite/infinite lower-bound inequality and every goal must have zero potential. Those hypotheses imply a lower bound for every terminating path, optimality of an attaining witness, and infeasibility for an infinite root. Optimal dynamic-programming values are not a premise. The Python parser, graph extraction, component decomposition and completeness of local enumeration are not thereby verified. |
| Non-submodular split capacity and unbounded myopic ratio | Paper three-key construction; `tests/unit/test_refinement_synthesis.py`; reproducible synthesis study | **Paper proof and executable controls, not a Lean theorem.** The specified maximum-immediate-gain-per-cost rule pays `M` on two cycles sharing a center while splitting the two leaves costs 2. The ratio `M/2` is unbounded. This is not a lower bound against every greedy, lookahead or approximation algorithm. |
| Concrete protocol evidence: complete four-validator witness / C13 | `src/python/twins_scheduler/concrete_trace.py`; `tests/unit/test_concrete_trace.py`; `results/new/concrete_trace.json` | **Executable, not a Lean transition proof.** Twelve cases and fourteen dedicated tests; actual authenticated model signer sets, guarded local transitions, legal timeout evidence, explicit envelopes and block relays. The separate FIFO-compatible gossip control changes its declared message-routing skeleton. |
| Concrete protocol evidence: unchanged native implementation | `experiments/native_cometbft/native_conformance_test.go.txt`; `results/native/native_summary.json`; `results/native/native_signature_audit.json`; `results/native/native_repeatability.json` | **Targeted ordinary-operation tests of actual pinned CometBFT code.** Four scenarios, fourteen checks, native Ed25519 votes, normal commits, scheduled timeouts, lock persistence and valid-block reuse. Synchronous in-process dispatch and upstream test keys/storage; no native mutant disagreement, production reactor or Lean refinement is claimed. |
| Appendix A: NP-completeness of abstract coarse reachability / C16 | Paper reduction from independent set by symmetric graph orientation, with polynomial witness verification | **No Lean declaration.** The input is the variable-size independent-pivot opportunity schema. The fixed four-validator example and production-client reachability are outside this complexity claim. |

## Retained supporting results and historical declarations

| Revised location / ledger ID | Retained declaration | Interpretation after revision |
|---|---|---|
| Section 3.1: original single-pivot quorum family / C3 | `SchedulerClosure.parametric_family_separation` in `ParametricFamily.lean` | Historical T3 arithmetic and terminal Boolean classification for the original one-pivot family. It is not the revised Corollary 1 and does not formalize the new multi-pivot participant allocation. |
| Historical fixed Boolean structural model / C2, C3 | `SchedulerClosure.quorum_pivot_separation_criterion`; `SchedulerClosure.criterion_policy_separation` in `QuorumPivotCriterion.lean` | The old model defines `pivotAtSecond e r := e && !r`. Those proofs check that defined classifier. The corrected arbitrary-contract proof for current Theorem 2 is the new `RepairFrontier.behavioral_quorum_pivot_separation`, not these declarations. |
| Validation and assurance: prior Tendermint-style classifier / C5 | `SchedulerClosure.bounded_baseline_safe`; `SchedulerClosure.bounded_missing_lock_phase_specific_unsafe`; `SchedulerClosure.bounded_missing_lock_directed_safe`; `SchedulerClosure.bounded_tendermint_refines_quorum_pivot` in `CometBFTInstantiation.lean` | These theorems concern `executeTendermintBounded`, which directly computes terminal flags. Despite its historical name, `bounded_tendermint_refines_quorum_pivot` proves matching unsafe/safe classifications, **not transition refinement**. The 384-row Python/Go comparison validates this old model, not the new event-level trace. |
| Appendix B.1: supporting replay-erasure proposition / C6 | `SchedulerClosure.replay_erasure_with_outputs`; `SchedulerClosure.replay_erasure_state_observation` in `ReplayErasure.lean` | State/output congruence, projected duplicate stutter, and output silence yield the finite trace statement. Historical T1; no longer paper Theorem 3. |
| Appendix B.1: hidden-state/output controls / C7 | `SchedulerClosure.hidden_state_counterexample`; `SchedulerClosure.hidden_state_breaks_output_congruence` | Specific finite counterexamples to weaker erasure assumptions. Historical T1 controls. |
| Appendix B.2: seven-flag diagnostic / C4 | `SchedulerClosure.strictSeparation_eq_characterization`; `SchedulerClosure.strictSeparation_iff_three` in `PremiseBoundary.lean` | Exact Boolean calculation with three satisfying assignments out of 128. Historical T6. It does not establish the revised graph characterization or justify repair merely before a collector. |
| Section 2: unsafe-observation typing / C8 | `SchedulerClosure.UnsafeObservationSet`; `SchedulerClosure.unsafe_observation_has_unsafe_terminal` | `Unsafe` is applied to terminal state before observation projection. |
| Section 2: original stable admission filter / C9 | `SchedulerClosure.typeClosure`; `SchedulerClosure.delivered_was_emitted`; `SchedulerClosure.delivered_preserves_order`; `SchedulerClosure.enabling_implies_closed_edge` in `SchedulerSemantics.lean` | Already-emitted envelopes, retained order, and shared-edge closure. This module does not formalize the expanded partial-order language of Theorem 3. |

## Build and audit gate

The project imports `SchedulerClosure.RepairFrontier`,
`SchedulerClosure.GraphRealization` and
`SchedulerClosure.CertificateOptimality` through
`formal/lean/SchedulerClosure.lean`. The selected **27 declarations** are listed
in `formal/lean/AxiomAudit.lean`; the primary toolchain is pinned Lean 4.33.0.
This selected count is not the total number of proved declarations, nor a
claim that every paper result is mechanized.

The scientific gate requires `lake build`, the selected axiom audit, source
hygiene, and `leanchecker SchedulerClosure` to succeed. The graph module also
passed an independent module-level `leanchecker` invocation. Dependencies of
the four graph/order and three Bellman declarations were checked directly;
the exact results appear in `formal/lean/AXIOM_REPORT.md`.

**Integrated validation: PASS.** The fresh Lean build completed 14 jobs; the
selected 27-declaration audit and independent kernel-object check exited with
status 0. Source hygiene checked 22 Lean/Coq files without findings. These
counts describe this executed gate, not additional protocol instances.

`results/generated/lean_verification.json` records successful Lean command
exits and SHA-256 hashes of the Lean source files. The report assembler
checks that receipt against the current source hashes before producing
`results/generated/formal_verification.json`; an old retained PASS report
cannot establish a fresh build. Detailed logs are `build_logs/lean_build.log`,
`build_logs/lean_axiom_audit.log`, and `build_logs/leanchecker.log`; the axiom
interpretation is in `formal/lean/AXIOM_REPORT.md`. Exact claim boundaries
and statuses are recorded in `docs/CLAIM_EVIDENCE_LEDGER.md` and its CSV.
Typesetting and PDF inspection are separate from this scientific gate.

The expanded gate now includes graph reversal, finite linear-extension
existence and the abstract certificate principle. It does **not** mechanize
the weighted four-role correspondence, graph-capacity maximization, completeness
of the executable checker, the complexity reduction, or protocol/client
refinement. These boundaries distinguish an actual checked bridge from a
claim that the entire synthesis and consensus stack has been verified.
