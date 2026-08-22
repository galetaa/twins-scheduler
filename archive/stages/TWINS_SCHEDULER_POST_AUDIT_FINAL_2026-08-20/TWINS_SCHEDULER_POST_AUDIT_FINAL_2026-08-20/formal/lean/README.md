# Lean 4 post-audit development

Target: `leanprover/lean4:v4.32.2`.

The source closes the audit gaps in T1, T3 and T6 and restates T2.  It is a
parallel mature-prover migration target.  In the current offline container the
Lean executable is unavailable, so this directory is not the evidence used to
claim an executed kernel check.  The executed evidence is in
`../project_kernel/`; its trusted base and limitations are stated explicitly.

Intended commands in a Lean-enabled environment:

```bash
lake build
lake env lean AxiomAudit.lean
```
