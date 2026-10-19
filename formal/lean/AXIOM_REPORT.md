# Lean axiom report

The selected audit now contains **27 named declarations**, including four
graph/order results and three minimum-cost certificate results. Their reported
dependencies below were checked with pinned Lean 4.33.0 (commit
`d8b18978322de05a8f3dba51ef03cf5461676c17`).

**Integrated validation: PASS.** The fresh build completed 14 jobs, the
27-declaration audit and independent kernel-object check exited with status 0,
and source hygiene checked 22 Lean/Coq files with no findings.

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

`propext`, `Classical.choice`, and `Quot.sound` are Lean's standard logical
axioms. Classical choice supplies decidability of the arbitrary finite
relations used by the event-order existence proof. No project-specific axiom
or bounded-enumeration oracle is introduced. The core graph-reversal theorem
has no axiom dependency at all; the generic Bellman proofs do not require
classical choice.

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

The graph module was additionally built and independently checked as its own
`SchedulerClosure.GraphRealization` target. The certificate module was built
as `SchedulerClosure.CertificateOptimality`; direct `#print axioms` checks
produced the three dependencies reported above.

The weighted four-role correspondence, maximum-acyclic-set optimization,
SCC decomposition and exhaustive enumeration implemented in Python, and
protocol-specific behavioral conformance remain separate paper or executable
obligations. Neither native conformance tests nor the concrete mutant trace
constitute a Lean refinement proof of the production CometBFT client.

The aggregate report is assembled only after a successful command receipt
exists and matches the current Lean-source hashes. It cannot predeclare a
successful future run. Build-job counts and unrelated Python test counts are
not used as substitutes for this source-bound verification gate.
