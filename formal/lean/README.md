# Lean 4 primary formalization

The repository root pins `leanprover/lean4:v4.33.0` in `lean-toolchain` and
defines the `SchedulerClosure` library in the root `lakefile.toml`.  These
sources cover replay erasure, legal closure lifting, the structural quorum
pivot criterion and corollary, exact scheduler semantics, typed unsafe
observations, the bounded Tendermint-style instantiation, and the seven-flag
diagnostic boundary.

From the repository root:

```bash
lake build
lake env lean formal/lean/AxiomAudit.lean
```

`#print axioms` output is recorded only from the second command.  The
project-local certificate kernel and SMT files are supporting checks, not a
replacement for this mature-prover build.
