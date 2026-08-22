# Contributing

Keep active code independent of `archive/stages/` and never edit
`provenance/raw_inputs/`. Each change must leave its corresponding target
passing.

To add a proof obligation, add the Lean statement and proof, include it in
`AxiomAudit.lean`, add an independent executable or SMT control where useful,
and update both claim ledgers. Negative controls must remain negative.

To add a model or regression witness, place reusable semantics under `models/`
or `src/`, a focused test under the matching `tests/` category, and a stable
reference result only when scientifically relevant. Python and Go terminal
observations must use the shared canonical JSON schema.

Manuscript changes must be synchronized between `manuscript/markdown/` and
`manuscript/lipics/`, then checked with `make paper`. Do not change a theorem
statement independently of Lean or expand its scope beyond the ledger.

Run `make test formal paper verify` before committing; use `make reproduce`
before a release. Update provenance and third-party records for copied content.
