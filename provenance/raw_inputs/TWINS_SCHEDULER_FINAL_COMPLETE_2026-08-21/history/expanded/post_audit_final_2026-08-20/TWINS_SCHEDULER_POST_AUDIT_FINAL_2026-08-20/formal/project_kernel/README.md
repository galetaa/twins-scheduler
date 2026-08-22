# Executed project-local proof kernel

`proof_kernel.py` is a small, purpose-built certificate checker independent of
the experiment code.  It checks the corrected proof structure for T1 and T2,
exhaustively validates their two-state finite instances, evaluates the complete
bounded T3 transition system, checks arbitrary-precision quorum arithmetic, and
exhausts all 128 T6 assignments.  Four damaged certificates must be rejected.

Run:

```bash
python3 proof_kernel.py certificate.json \
  --negative-controls --json-output kernel_result.json
```

## Assurance boundary

This is an **actually executed kernel check**, but the kernel is project-local,
not a mature external prover.  Its trusted computing base is `proof_kernel.py`,
CPython's Boolean/integer/JSON semantics, and the mapping from the paper's
symbols to `certificate.json`.  The Lean and Coq directories are parallel
mature-prover migrations; they were not compiled in the offline runtime and are
not used to claim a Lean/Coq kernel proof.
