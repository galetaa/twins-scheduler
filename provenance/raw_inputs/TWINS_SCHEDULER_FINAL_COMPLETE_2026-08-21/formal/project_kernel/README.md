# Purpose-built proof-certificate kernel

This dependency-free checker validates a narrow certificate language for the
four theorem packages. Version 1.1 adds the reviewer-requested output trace
condition to replay erasure: finite models must satisfy both projection
congruence and output congruence, the marked duplicate is a projected stutter,
and its relevant output is empty. The hidden `X,X,Y` machine separates both
final relevant state and future output when congruence is absent.

Run:

```bash
python proof_kernel.py certificate.json --negative-controls \
  --json-output ../../results/final/project_kernel_result_final.json
```

This is an executed project-local checker, not a replacement for a Lean/Coq
kernel. Five damaged controls must be rejected.
