# Lean axiom report

Status: **PASS** on Lean 4.33.0 (commit
`d8b18978322de05a8f3dba51ef03cf5461676c17`).

Commands executed from the repository root:

```text
lake build
lake env lean formal/lean/AxiomAudit.lean
lake env leanchecker SchedulerClosure
```

All three commands exited with status 0.  Complete logs are
`build_logs/lean_build.log`, `build_logs/lean_axiom_audit.log`, and
`build_logs/leanchecker.log`.  Source hygiene checked 20 Lean/Coq source files
and found no `sorry`, `admit`/`Admitted`, user `axiom`/`Axiom`, or unsafe
declaration.

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

`propext`, `Classical.choice`, and `Quot.sound` are Lean's standard logical
axioms used by library proof automation.  No project-specific axiom is
declared.  `leanchecker` independently rechecked the produced
`SchedulerClosure.olean` dependency closure with exit status 0.


## Repair-frontier revision

The integrated 2026-10-19 run built 12 jobs and audited the 20 declarations
above. `results/generated/lean_verification.json` records successful build,
axiom-audit and leanchecker exits and the SHA-256 of the audited Lean sources.
The aggregate report is assembled only after this receipt exists and matches
the current sources. The supporting checker is not allowed to predeclare a
successful future Lean run.

The new theorem is over an arbitrary behavioral contract. Its realization
premises are assumptions to discharge for a concrete execution domain. The
capacity and split-budget statements are arithmetic consequences of their
capacity contracts. The graph reversal lemma, graph-to-execution proof and
optimal graph capacity are proved in the paper and checked on finite instances;
they are not mechanized by this Lean module. The concrete message executor is
not a Lean refinement proof of the production CometBFT client.
