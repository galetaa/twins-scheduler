# Lean kernel build

Pinned environment: `leanprover/lean4:v4.33.0` from `lean-toolchain`.

Local build:

```bash
cd formal/lean
lake build
lake env lean AxiomAudit.lean
```

Repository CI uses the official `leanprover/lean-action@v1`, enables
`leanchecker` and `nanoda`, and rejects `sorry` through
`nanoda-allow-sorry: false`.

A source tree or CI configuration is not a successful kernel build. The
machine-readable status records `PASS` only after the commands above have
actually exited successfully. In the supplied execution environment the Lean
binary was unavailable, so the local mature-prover status remains `NOT_RUN`.
