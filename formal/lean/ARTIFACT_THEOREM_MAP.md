# Paper result to artifact mapping

This map uses result titles and declaration names instead of manuscript
numbers. The revised central results concern static trace conflicts, general
transition-system synthesis, closed-sublevel certificates, abstraction
transfer, and the independent-pivot specialization. Supporting graph,
behavioral, replay and arithmetic results retain their historical declaration
names. Historical T1/T2/T3/T6 file labels are provenance locators.

The names below are Lean declarations, not assertions of a larger
mechanization scope. `TransitionRefinement` proves policy realizability,
minimum trace split cost, the memory-update bridge, closure certificates,
local simulation transfer, and invariant-guided quotient refinement for
arbitrary state relations. `GraphRealization` proves the repair graph/order
bridge. `CertificateOptimality` proves the Bellman principle used by the
specialized optimizer. None of these modules is a refinement proof of the
production CometBFT client.

## General transition-system results

All short declarations in this table have the prefix
`SchedulerClosure.TransitionRefinement.`.

| Paper item | Formal declaration or other evidence | Exact assurance boundary |
|---|---|---|
| Static trace conflict characterization | `policy_realizable_iff`; `completion_agrees`; `completion_uniform` | **Exact semantic correspondence is mechanized.** A total static policy exists precisely when a fine key never changes its Boolean value and every coarse fibre observed with both values is split. The proof constructs a completion of unobserved choices. There are no pivot, independence, quorum, finite-state or acyclicity assumptions. |
| Least refinement for a fixed trace | `least_split_set`; `admissible_refinement_exists_iff`; `minimum_trace_refinement` | **Least set and cost minimality are mechanized.** Required fibres union mixed fibres is contained in every realizing permitted refinement and itself realizes a consistent trace when allowed. Its nonnegative integer cost is minimum over all realizing split sets. The cost sum uses an explicit finite interface enumeration; applications cover each key once. |
| General product-memory semantics | `remember_occurrences_iff`; `query_guard_iff_consistent_extension`; `memory_update_cost_mono` | **The incremental representation bridge is mechanized.** A key can be set only while unseen or repeated with its stored answer. The legal update represents exactly the previous observations plus the new query, and its required/mixed cost cannot decrease. Lean uses `Option Bool`; the Python tuple encoding, complete product construction and search are separately implemented and tested. |
| General finite transition-system synthesis | The preceding policy, least-cost and memory declarations; paper finite-product reachability argument; executable general solver and independent policy-enumeration controls | **The semantic core is mechanized; the solver program is not.** Exhausting a finite protocol-state/partial-policy product covers every finite bad execution for its declared interface. Protocol transitions may be cyclic and arbitrarily interdependent. Finiteness ensures exhaustive-search termination; it is not a hypothesis of the semantic theorems. A finite adapter's state/horizon bounds remain part of that adapter's claim. |
| Closed strict-sublevel certificate | `reachable_below_in_cut`; `sublevel_certificate_lower_bound`; `sublevel_certified_minimum` | **The certificate principle is mechanized.** Monotone state costs, inclusion of the initial state when below the claimed threshold, successor closure strictly below it, and absence of goals imply the lower bound. A replayed path attaining the threshold proves an actual minimum. Zero costs, nonzero required initial cost and cycles are included. Checking every successor of each listed state remains an executable coverage obligation. |
| General infeasibility certificate | `closed_certificate_infeasible` | **Full-closure soundness is mechanized.** A closed set containing the initial state and excluding goals rules out every finite goal-reaching execution. A resource cutoff is not this certificate. |
| Local labelled abstraction coverage | `labelled_execution_simulates`; `bad_trace_coverage` | **Whole-trace coverage is derived from local edges.** Controlled edges preserve their fine key and Boolean value. Only internal edges may collapse to abstract stuttering. Inclusion of concrete bad states yields inclusion of concrete bad traces. No whole-path coverage or production correspondence is assumed under another name. |
| Abstract lower bound and concrete optimality sandwich | `reachable_simulates`; `abstract_lower_bound_transfers`; `matching_concrete_witness_is_minimum` | **The generic transfer theorem is mechanized.** Every concrete edge must have a finite abstract simulation path, abstract state cost must not exceed concrete state cost, concrete goals must map to abstract goals, and the abstract cut must satisfy its local conditions. These hypotheses imply the concrete lower bound. A concrete witness attaining it proves a concrete minimum even if some abstract witnesses are spurious. |
| Transfer of abstract infeasibility | `abstract_infeasibility_transfers` | **The generic infeasibility transfer is mechanized.** A local covering simulation and bad-state coverage transfer an abstract full-closure invariant. Ordinary conformance tests alone do not establish those universal coverage obligations. |
| Policy-level CEGAR elimination | `invariant_quotient_excludes_goal`; `invariant_split_saturated`; `invariant_split_eliminates_policy` | **Elimination of the entire spurious policy is mechanized.** For one fixed policy, an inductive concrete bad-free invariant survives its exact existential quotient when blocks are homogeneous. Splitting every block by invariant membership enforces homogeneity, excluding all abstract bad traces under that policy. The checker must establish that the computed concrete invariant is closed under all policy-compatible edges. |
| Strict CEGAR progress | `spurious_policy_forces_strict_split`; paper finite-partition argument | **An actual block split is mechanized.** A bad path in the old quotient combined with a concrete bad-free invariant forces an old block to mix invariant and non-invariant states. The upper bound on the number of strict refinements for a finite state set remains paper cardinality reasoning. The CEGAR program and its output parser are not extracted Lean code. |

## Independent-pivot specialization and retained semantic results

Every short declaration in this section has the prefix `SchedulerClosure.`.

| Paper item / ledger ID | Formal declaration or other evidence | Exact assurance boundary |
|---|---|---|
| Legal relational preservation / C1 | `merged_trace_lifting`; `legal_scheduler_closure_preserves_unsafe` in `ClosureLifting.lean` | Sufficient simulation/closure theorem under its relation and legal-target hypotheses. It does not make an illegal inserted trace legal. Historical obligation T2. |
| Behavioral quorum-pivot separation / C2 | `RepairFrontier.behavioral_quorum_pivot_separation` | Arbitrary state type, execution function, vote functions and unsafe predicate, subject to explicit first-vote necessity, positive persistence, timely repair, one-short bases and observation assumptions. Realization by a legal protocol/scheduler is a separate obligation. |
| Independence of the persistence premise / C2 | `RepairFrontier.persistence_hypothesis_independent` | A specific negative-control function satisfies first-vote necessity and timely repair but has no fine unsafe witness because it never emits the second vote. This is not a universal independence classification. |
| Compatible late repairs and full event-order realization / C11 | `GraphRealization.repair_graph_reversal_iff`; `GraphRealization.finite_acyclic_iff_schedule`; `GraphRealization.repair_graph_iff_realizable_schedule`; `GraphRealization.repair_graph_from_covers_iff_schedule` | **The graph/order bridge is mechanized.** For transitive irreflexive precedence with disjoint repair/vote event kinds, adding selected vote-before-repair requests is acyclic exactly when the induced repair graph is acyclic. Complete finite enumeration supplies injective times respecting every original edge and request. Cover paths retain suppressed opportunities. No capacity or schedule-existence premise is assumed. |
| Weighted repair-frontier characterization / C11 | The four `GraphRealization` results; paper connection to independent behavioral contracts, certificate weights and full opportunity-order coverage | Event-order realizability is machine-checked. Its correspondence to certificate supports and unsafe observations is a paper argument under the independent-pivot behavioral assumptions. These special-case assumptions are not inherited by the new general transition-system framework. |
| Unit-weight quota equivalence / C11 | `RepairFrontier.directed_unsafe_iff`; `RepairFrontier.strict_separation_iff` | Exact inequality for an abstract reusable capacity and the count abstraction. The graph module realizes each acyclic reusable set; maximizing its cardinality and participant allocation remain paper finite-set reasoning. |
| Minimum phase budget for unit weights / C12 | `RepairFrontier.split_capacity_bound`; `RepairFrontier.minimum_phase_splits` | Budget existence and minimality for the supplied optimal capacity expression. Choosing a maximum acyclic set and attaining that capacity are paper arguments. This arithmetic result is not a general implementation-level minimum. |
| Weighted common-frontier interval / C14 | `RepairFrontier.weighted_admission_interval`; `RepairFrontier.weighted_granularity_counterexample` | Interval equivalence under an arbitrary attainable-subset-weight predicate and the indivisible `(2,2)` counterexample. Scheduling reduction to a common frontier and interpretation by actual subsets are separate arguments. |
| Signature-issuance versus collector timing / C15 | `RepairFrontier.repair_preserves_signed_output`; `RepairFrontier.late_repair_before_certificate_is_unsafe`; `RepairFrontier.repair_before_second_vote_is_safe`; `RepairFrontier.closed_edge_still_permits_second_vote` | Properties of the explicit small `OutputState/OutputEvent` machine, including immutable signed output and displayed control traces. They do not establish transition correspondence with the concrete Python model or the native client. |
| Weighted four-role refinement specialization | Paper proof and `src/python/twins_scheduler/refinement_synthesis.py`, using mechanized graph realization | **The four-role support correspondence remains a paper proof.** Allowed/required keys, positive vote weights and nonnegative control costs are explicit. An open first-contributing role can also obtain extra second support. This specialized input-to-schedule result remains conditional on the independent-pivot contract. |
| Bellman certificate for the specialized optimizer | `CertificateOptimality.bellman_path_lower_bound`; `CertificateOptimality.certified_witness_is_minimum`; `CertificateOptimality.certified_infeasibility` | **The Bellman principle is mechanized.** Local finite/infinite potential inequalities and zero potential at goals prove a lower bound, minimum of an attaining witness and infeasibility at an infinite root. Optimal dynamic-programming values are not a premise. Parser, graph extraction, component decomposition and enumeration are not thereby verified. |
| Non-submodular split capacity and unbounded myopic ratio | Paper three-key construction; specialized synthesis tests and study | Paper proof and executable controls. The specified immediate-gain-per-cost rule pays `M` where splitting two leaves costs 2. The ratio `M/2` is unbounded. This is not a statement against every greedy, lookahead or approximation method. |
| Complexity of the variable-size independent-pivot specialization / C16 | Paper reduction from independent set by symmetric orientation, with polynomial witness verification | No Lean complexity declaration. The general transition model has its own state/interface presentation and search-size bounds; the fixed four-validator example and unbounded production-client reachability are outside this old complexity claim. |

## Executable protocol evidence and historical supporting declarations

| Item / ledger ID | Declaration or artifact | Assurance boundary |
|---|---|---|
| Concrete guarded four-validator witness / C13 | `src/python/twins_scheduler/concrete_trace.py`; concrete trace tests; `results/new/concrete_trace.json` | Executable evidence with model authentication, guarded transitions, legal timeout evidence, envelopes and block relays. The FIFO-compatible gossip control changes its declared routing skeleton. It is not a Lean refinement of the concrete model or a production client. |
| Unchanged native implementation conformance | Native harness, `results/native/native_summary.json`, signature audit and repeatability data | Ordinary-operation tests of pinned CometBFT code: native votes, commits, timeouts, lock persistence and valid-block reuse. Synchronous in-process dispatch with upstream test keys/storage; no native mutant disagreement or production-reactor coverage is claimed. |
| Original single-pivot quorum family / C3 | `parametric_family_separation` in `ParametricFamily.lean` | Historical T3 arithmetic and terminal Boolean classification, retained as a supporting result. |
| Historical fixed Boolean model / C2, C3 | `quorum_pivot_separation_criterion`; `criterion_policy_separation` | Proofs about the old directly defined `e && !r` classifier. The arbitrary behavioral theorem is the separate `RepairFrontier` declaration. |
| Historical Tendermint-style classifier / C5 | `bounded_baseline_safe`; `bounded_missing_lock_phase_specific_unsafe`; `bounded_missing_lock_directed_safe`; `bounded_tendermint_refines_quorum_pivot` in `CometBFTInstantiation.lean` | Despite its historical name, the last theorem proves matching terminal classifications, not transition refinement. The 384-row Python/Go comparison validates this old classifier. |
| Replay erasure / C6 | `replay_erasure_with_outputs`; `replay_erasure_state_observation` | State/output congruence, projected duplicate stuttering and output silence yield a finite-trace statement. Historical T1. |
| Hidden-state/output controls / C7 | `hidden_state_counterexample`; `hidden_state_breaks_output_congruence` | Specific finite counterexamples to weaker replay-erasure hypotheses. |
| Seven-flag diagnostic / C4 | `strictSeparation_eq_characterization`; `strictSeparation_iff_three` | Exact Boolean calculation with three satisfying assignments out of 128. Historical T6; no repair-frontier or collector-timing conclusion is inferred from it. |
| Unsafe-observation typing / C8 | `UnsafeObservationSet`; `unsafe_observation_has_unsafe_terminal` | `Unsafe` applies to terminal state before observation projection. |
| Original stable admission filter / C9 | `typeClosure`; `delivered_was_emitted`; `delivered_preserves_order`; `enabling_implies_closed_edge` | Already-emitted envelopes, retained order and shared-edge closure. This older module does not define the new general product relation. |

## Build and audit gate

`formal/lean/SchedulerClosure.lean` imports the new `TransitionRefinement`
module alongside the retained `RepairFrontier`, `GraphRealization` and
`CertificateOptimality` modules. The selected **46 declarations** are listed
in `formal/lean/AxiomAudit.lean`. This is a selected audit count, not the total
number of declarations or a claim of whole-stack verification.

**Integrated validation: PASS.** With pinned Lean 4.33.0, the build completed
15 jobs, the 46-declaration axiom audit and independent
`leanchecker SchedulerClosure` exited with status zero, and source hygiene
checked 23 Lean/Coq files without findings. The exact axiom dependencies are
listed in `formal/lean/AXIOM_REPORT.md`.

The reproducibility pipeline records successful command exits and current
Lean-source SHA-256 hashes in `results/generated/lean_verification.json`.
`assemble_formal_report.py` requires that receipt to match the current source;
a retained report cannot certify newly edited files. Detailed logs are
`build_logs/lean_build.log`, `build_logs/lean_axiom_audit.log` and
`build_logs/leanchecker.log`. Publication rebuilds this source-bound receipt
through the full gate after the proof sources are frozen.

The new semantic and certificate results no longer depend on independent
pivots. Their application to an implementation still requires an explicit
control interface, truthful transition/goal coverage and the stated cost
mapping. The executable coverage checker can discharge finite local model
obligations; the Lean module proves why those obligations suffice. Neither
component establishes coverage of an unbounded production client without
additional implementation evidence.
