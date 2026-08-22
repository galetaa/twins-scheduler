# Reproduction contract

## Minimum local commands

From the stage root:

```bash
./scripts/reproduce_post_audit.sh
```

Expected decisive results:

```text
independent_proof_checks=PASS
project_local_proof_kernel=PASS
post_audit_smt=PASS (8 UNSAT, 4 SAT controls)
formal_source_hygiene=PASS
review_pdf_build=PASS, when pandoc and xelatex are installed
review_pdf_pages=17
blocking_latex_warnings=0
```

## External optional checks

A mature proof-assistant build requires either the pinned Lean toolchain from `formal/lean/lean-toolchain` or a compatible Coq installation. Those checks were not executable in the verified environment and must not be inferred from source presence.

The official typesetting check requires the official `lipics-v2021.cls` and `plainurl.bst`. Run the command documented in `manuscript/lipics/BUILD_INSTRUCTIONS.md`.

## Determinism

The independent checker, project kernel, SMT outcomes, generated review TeX, and source hashes are deterministic. The PDF may contain TeX metadata that makes a byte-for-byte comparison environment-dependent; correctness is checked by page count, extracted content, warning status, font embedding, and visual inspection.
