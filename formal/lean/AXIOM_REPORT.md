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
`build_logs/leanchecker.log`.  Source hygiene checked 19 Lean/Coq source files
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

`propext`, `Classical.choice`, and `Quot.sound` are Lean's standard logical
axioms used by library proof automation.  No project-specific axiom is
declared.  `leanchecker` independently rechecked the produced
`SchedulerClosure.olean` dependency closure with exit status 0.

