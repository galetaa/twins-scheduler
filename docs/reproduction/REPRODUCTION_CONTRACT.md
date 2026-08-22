# Reproduction contract

`./reproduce.sh` is successful only when every mandatory command exits zero.
It activates pinned dependencies in repository-local caches, writes fresh
results beneath a unique `.cache/reproduction.*` directory, and never reads
`archive/stages/`. It runs Python, Go, cross-language, independent proof,
certificate, SMT, Lean, axiom, leanchecker, manuscript, page-budget,
provenance, and byte-comparison checks.

Automation may set `TWINS_REPRODUCTION_RUN_ROOT` to an explicit empty output
directory for artifact extraction. Without it, the script creates a unique
repository-local ignored directory.

Failure is fail-closed: `set -euo pipefail` propagates the first mandatory
error. Network access is needed only when a pinned Lean or TeX dependency is
not cached. Python, uv, Go, Git, curl, a C compiler, base TeX, Poppler, and
dpkg-deb are environment prerequisites. The pinned container provides them
when the host does not.

Committed `results/generated/` files and the final PDF are references, not a
substitute for execution. A run is accepted only after fresh output matches
those references and provenance hashes pass.
