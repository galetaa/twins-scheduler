# Lean axiom report

The selected audit now contains **46 named declarations**, including four
graph/order results, three Bellman certificate results, and nineteen general
transition-refinement, closure-certificate, abstraction and CEGAR results. Their reported
dependencies below were checked with pinned Lean 4.33.0 (commit
`d8b18978322de05a8f3dba51ef03cf5461676c17`).

**Integrated validation: PASS.** The fresh build completed 15 jobs, the
46-declaration audit and independent kernel-object check exited with status 0,
and source hygiene checked 23 Lean/Coq files with no findings.

The integrated build and independent kernel-object gate runs, from the
repository root:

```text
lake build
lake env lean formal/lean/AxiomAudit.lean
lake env leanchecker SchedulerClosure
```

All three commands must exit with status 0. Their logs are
`build_logs/lean_build.log`, `build_logs/lean_axiom_audit.log`, and
`build_logs/leanchecker.log`. The separate source-hygiene gate rejects admitted
proofs, user-declared axioms and unsafe declarations. Successful command exits
and hashes of the checked sources are recorded in
`results/generated/lean_verification.json`; a retained receipt is evidence for
the current source only when those hashes match.

Every short declaration name in the table has the prefix `SchedulerClosure.`.

| Declaration | Reported axioms |
| --- | --- |
| `replay_erasure_with_outputs` | `propext` |
| `replay_erasure_state_observation` | `propext` |
| `hidden_state_counterexample` | none |
| `legal_scheduler_closure_preserves_unsafe` | none |
| `quorum_pivot_separation_criterion` | `propext`, `Classical.choice`, `Quot.sound` |
| `criterion_policy_separation` | `propext`, `Classical.choice`, `Quot.sound` |
| `parametric_family_separation` | `propext`, `Classical.choice`, `Quot.sound` |
| `bounded_tendermint_refines_quorum_pivot` | `propext`, `Classical.choice`, `Quot.sound` |
| `strictSeparation_eq_characterization` | none |
| `strictSeparation_iff_three` | none |
| `RepairFrontier.behavioral_quorum_pivot_separation` | `propext`, `Classical.choice`, `Quot.sound` |
| `RepairFrontier.directed_unsafe_iff` | `propext`, `Classical.choice`, `Quot.sound` |
| `RepairFrontier.strict_separation_iff` | `propext`, `Classical.choice`, `Quot.sound` |
| `RepairFrontier.minimum_phase_splits` | `propext`, `Classical.choice`, `Quot.sound` |
| `RepairFrontier.weighted_admission_interval` | `propext`, `Classical.choice`, `Quot.sound` |
| `RepairFrontier.weighted_granularity_counterexample` | `propext`, `Quot.sound` |
| `RepairFrontier.repair_preserves_signed_output` | none |
| `RepairFrontier.late_repair_before_certificate_is_unsafe` | none |
| `RepairFrontier.repair_before_second_vote_is_safe` | none |
| `RepairFrontier.closed_edge_still_permits_second_vote` | none |
| `GraphRealization.repair_graph_reversal_iff` | none |
| `GraphRealization.finite_acyclic_iff_schedule` | `propext`, `Classical.choice`, `Quot.sound` |
| `GraphRealization.repair_graph_iff_realizable_schedule` | `propext`, `Classical.choice`, `Quot.sound` |
| `GraphRealization.repair_graph_from_covers_iff_schedule` | `propext`, `Classical.choice`, `Quot.sound` |
| `CertificateOptimality.bellman_path_lower_bound` | `propext`, `Quot.sound` |
| `CertificateOptimality.certified_witness_is_minimum` | `propext`, `Quot.sound` |
| `CertificateOptimality.certified_infeasibility` | `propext`, `Quot.sound` |
| `TransitionRefinement.policy_realizable_iff` | `propext`, `Classical.choice`, `Quot.sound` |
| `TransitionRefinement.least_split_set` | `propext`, `Classical.choice`, `Quot.sound` |
| `TransitionRefinement.admissible_refinement_exists_iff` | `propext`, `Classical.choice`, `Quot.sound` |
| `TransitionRefinement.minimum_trace_refinement` | `propext`, `Classical.choice`, `Quot.sound` |
| `TransitionRefinement.trace_cost_mono` | `propext`, `Classical.choice`, `Quot.sound` |
| `TransitionRefinement.query_guard_iff_consistent_extension` | `propext`, `Classical.choice`, `Quot.sound` |
| `TransitionRefinement.memory_update_cost_mono` | `propext`, `Classical.choice`, `Quot.sound` |
| `TransitionRefinement.labelled_execution_simulates` | none |
| `TransitionRefinement.bad_trace_coverage` | none |
| `TransitionRefinement.sublevel_certificate_lower_bound` | `propext`, `Quot.sound` |
| `TransitionRefinement.closed_certificate_infeasible` | none |
| `TransitionRefinement.sublevel_certified_minimum` | `propext`, `Quot.sound` |
| `TransitionRefinement.abstract_lower_bound_transfers` | `propext`, `Quot.sound` |
| `TransitionRefinement.matching_concrete_witness_is_minimum` | `propext`, `Quot.sound` |
| `TransitionRefinement.abstract_infeasibility_transfers` | none |
| `TransitionRefinement.invariant_quotient_excludes_goal` | none |
| `TransitionRefinement.invariant_split_saturated` | `propext`, `Classical.choice`, `Quot.sound` |
| `TransitionRefinement.invariant_split_eliminates_policy` | `propext`, `Classical.choice`, `Quot.sound` |
| `TransitionRefinement.spurious_policy_forces_strict_split` | `propext`, `Classical.choice`, `Quot.sound` |

`propext`, `Classical.choice`, and `Quot.sound` are Lean's standard logical
axioms. Classical choice supplies decidability for arbitrary relations and
predicates in event-order existence, total policy completion, cost sums, and
invariant-membership partitions. No project-specific axiom
or bounded-enumeration oracle is introduced. The core graph-reversal theorem
has no axiom dependency at all. Neither the Bellman proofs nor the numerical
closure-certificate and simulation-transfer proofs require classical choice.
The labelled trace coverage and full-closure infeasibility proofs have no axiom
dependencies.

## What the expanded audit establishes

- `RepairFrontier` proves the arbitrary behavioral separation contract,
  arithmetic consequences of a supplied reusable-capacity bound, and explicit
  properties of a small immutable-output machine.
- `GraphRealization` proves the previously unmechanized reversal criterion and
  finite order realization. The graph is defined from actual transitive event
  precedence. No capacity formula or existence of a compatible schedule is
  assumed. The cover-edge version retains paths through every opportunity,
  including suppressed slots.
- `CertificateOptimality` proves the Bellman lower-bound rule for arbitrary
  nonnegative-cost paths with finite or infinite potentials. A feasible witness
  meeting the lower bound is optimal; an infinite initial bound excludes all
  finite-cost paths to the declared goal. The potentials need not be optimal
  dynamic-programming values.
- `TransitionRefinement` proves static-policy realization exactly when no fine
  key changes its Boolean answer and every mixed coarse fibre is split. It
  constructs the total policy and proves that required plus mixed fibres form
  the least feasible split set and attain minimum nonnegative sum cost. It
  also proves that the three-valued memory update guard is exactly consistency
  of the extended observations, and derives nondecreasing product-state cost.
- The same module proves strict-sublevel certificate soundness for arbitrary
  state relations, including loops and a nonzero required initial cost. Local
  closure below a threshold and absence of goals give a lower bound for every
  finite execution; a replayed witness attaining it is optimal. Full closure
  yields infeasibility. These results do not assume the graph is finite.
- Local labelled edge coverage, with internal stuttering only, is proved to
  preserve complete controlled traces. Local path simulation plus abstract
  cost and goal coverage transfers a checked lower bound; a matching concrete
  witness proves concrete optimality. An abstract witness alone is not claimed
  to be executable concretely.
- The invariant-guided quotient results prove that splitting blocks by a
  concrete bad-free inductive invariant eliminates every bad abstract path
  under the corresponding fixed policy. A spurious old path forces an actual
  block split. The finite upper bound on the number of refinement iterations
  is paper-level partition arithmetic.

The graph module was additionally built and independently checked as its own
`SchedulerClosure.GraphRealization` target. The certificate module was built
as `SchedulerClosure.CertificateOptimality`; direct `#print axioms` checks
produced the three dependencies reported above.

The weighted four-role correspondence, maximum-acyclic-set optimization,
SCC decomposition, executable product-graph construction and completeness,
Python parsing/search/certificate verification, and protocol-specific
behavioral conformance remain separate paper or executable obligations.
Finiteness and full enumeration are executable termination and coverage
requirements, not hypotheses of the general semantic transfer theorems. Neither native conformance tests nor the concrete mutant trace
constitute a Lean refinement proof of the production CometBFT client.

The aggregate report is assembled only after a successful command receipt
exists and matches the current Lean-source hashes. It cannot predeclare a
successful future run. Build-job counts and unrelated Python test counts are
not used as substitutes for this source-bound verification gate.
