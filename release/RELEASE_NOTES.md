# Release notes — v1.0.0-reproducible

This release closes the supplied scheduler-closure research artifact with a
fresh Lean 4.33 kernel build and axiom audit, independent supporting checks,
an official deterministic LIPIcs v2021.1.3 PDF, immutable provenance, and a
clean-clone one-command reproduction.

The Git ZIP is a clean clone of the annotated release tag and includes its
`.git` directory. The source tarball contains the same tracked release tree but
omits `.git`. Outer archives and their own SHA sidecars cannot recursively
contain themselves; they are distributed beside the archives.

Scientific scope remains bounded and rule-level. See `docs/LIMITATIONS.md` and
the claim ledger before citing or extending a claim.
