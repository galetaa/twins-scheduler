# Gate 8′ Final Clean-Copy Reproduction Verification

**Date:** 17 August 2026

The final distribution archive was extracted into a new empty directory and reproduced with:

```bash
./scripts/reproduce_gate8p.sh
```

## Result

```text
Gate 7 core evidence: PASS
Gate 5 nested exact kernels: PASS
Gate 8 claim audit: PASS, 30 claims
Manuscript build: PASS, 17 A4 pages
Gate 8 manifest: PASS
GATE 8' REPRODUCTION PASS
elapsed=26.08 seconds
maximum resident set=220136 KiB
```

The final ZIP SHA-256 is:

```text
90432335c34251e6bde79e6224fe1610ab0f2d06aaca34b20bdd29b90c926c69
```

The PDF was regenerated and semantically validated. It is excluded from the inner byte-for-byte manifest because dvipdfmx emits a fresh trailer identifier; the final ZIP checksum protects the distributed PDF. The Markdown, generated LaTeX, proof/model sources, result files, manifests, and decision documents are covered by the inner Gate 8 manifest.

The Lean scaffold remains unbuilt because Lean/Lake were unavailable. The clean-copy run therefore confirms the solver/certificate/executable routes, not a mature proof-assistant kernel route.
