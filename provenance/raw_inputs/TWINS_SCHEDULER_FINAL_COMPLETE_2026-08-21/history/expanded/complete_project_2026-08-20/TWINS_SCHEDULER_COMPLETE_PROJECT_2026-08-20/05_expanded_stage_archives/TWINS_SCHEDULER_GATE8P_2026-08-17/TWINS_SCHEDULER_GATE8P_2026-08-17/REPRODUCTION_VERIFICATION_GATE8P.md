# Gate 8′ Reproduction Verification

**Date:** 17 August 2026  
**Command:** `./scripts/reproduce_gate8p.sh`

## Verified environment

- Python 3.13.5
- go version go1.23.2 linux/amd64
- pandoc 3.1.11.1
- XeTeX 3.141592653-2.6-0.999996 (TeX Live 2025/dev/Debian)
- pdfinfo version 25.06.0
- Z3 4.13.3.0 through the included minimal C loader

## Full-route result

The full Gate 8′ runner completed successfully in approximately 26 seconds on the verification host with a maximum resident set of about 220 MiB.

Verified stages:

1. Gate 7 core evidence: 17 tests passed; five positive SMT/CHC files produced eight expected UNSAT outcomes; four damaged controls produced SAT; inherited core and full-payload manifests passed.
2. Nested Gate 5 exact kernels: reproduction passed; the Tendermint-style second kernel produced 15 serialized witnesses; 728 Go/Python vote-processing cases passed; the parametric family passed for f=1…8.
3. Gate 8 claim audit: 30 claims loaded, all had evidence routes, and `submission_ready=false` was enforced.
4. Manuscript build: Markdown and bibliography regenerated LaTeX; XeLaTeX produced a 17-page A4 PDF; required theorem, nonclaim, and AI-disclosure text was found; no overfull boxes or LaTeX errors were accepted.
5. Gate 8 manifest: every non-transient payload file except the PDF passed SHA-256 verification. The PDF is semantically rebuilt but excluded from byte-level regeneration because dvipdfmx emits a fresh trailer identifier; the outer ZIP hash protects the delivered PDF.

## Clean-copy criterion

A final verification consists of extracting the distributed ZIP into an empty directory and running the same command without modifying the payload. Success requires the terminal line:

`GATE 8' REPRODUCTION PASS`

## Assurance limitation retained

The Lean scaffold was not kernel-checked. `lean`, `lake`, and `elan` were unavailable in the verified environment, and the recorded `lake build` attempt exited with status 127. This remains a submission blocker rather than being silently treated as a passed proof route.
