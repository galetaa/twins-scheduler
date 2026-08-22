# Lean kernel build

Pinned environment: `leanprover/lean4:v4.33.0` from `lean-toolchain`.

Build from the repository root:

```bash
lake build
lake env lean formal/lean/AxiomAudit.lean
```

Repository CI uses the official `leanprover/lean-action@v1`, enables
`leanchecker` and `nanoda`, and rejects `sorry` through
`nanoda-allow-sorry: false`.

A source tree or CI configuration is not a successful kernel build. The
machine-readable status records `PASS` only after both commands exit zero in a
new run and their complete logs are saved.
