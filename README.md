# Twins Scheduler Closure

## Research question and bounded claim

Can erasing a protocol phase from a fault-injection scheduler change the
agreement violations that a bounded test can observe? This artifact proves and
executes a strict safety-observation separation between a phase-specific
grammar and its type-uniform directed-edge abstraction. The witness uses one
honest quorum pivot in a finite certificate-driven locking model.

The natural-protocol bridge is a bounded rule-level Tendermint/CometBFT-style
refinement. It is neither a production CometBFT vulnerability claim nor a
production event-loop conformance result. No liveness, unbounded completeness,
bug prevalence, or universal minimality claim is made.

## Repository map

- `src/` and `tests/`: canonical Python and Go models and checks.
- `formal/lean/`: primary kernel-checked formalization; `formal/smt/` and
  `formal/project_kernel/` are independent supporting evidence.
- `models/` and `experiments/`: finite semantics and executable witnesses.
- `manuscript/`: synchronized Markdown, official LIPIcs source, figures and PDF.
- `results/reference/` and `results/generated/`: fixed reference evidence.
- `provenance/raw_inputs/` and `archive/stages/`: immutable acquisitions and
  non-active historical snapshots.
- `docs/CLAIM_EVIDENCE_LEDGER.md`: claim-to-proof/test mapping.

## Quick start

Prerequisites are Python 3.11, uv 0.6.14, Go 1.24, Git, curl, a C compiler,
base pdfTeX/BibTeX/Poppler commands, and `dpkg-deb`. Lean and
the pinned TeX overlay are installed beneath `.cache/`; host installations are
not modified.

```bash
./reproduce.sh
```

The same interface is available as `make bootstrap`, `make test`, `make
formal`, `make paper`, `make verify`, `make reproduce`, and `make release`.
See `containers/README.md` when local prerequisites are unavailable.

## Expected outputs and assurance

A passing reproduction creates an isolated output tree beneath `.cache/` and
checks it byte-for-byte against the committed reference results. Key outputs
are `results/generated/formal_verification.json`, cross-language observations,
SMT outcomes, Lean logs, and `manuscript/pdf/final_lipics_manuscript.pdf`.
Exact expectations are listed in `docs/reproduction/EXPECTED_OUTPUTS.md`.

Lean 4.33.0 plus `lake build`, `#print axioms`, source hygiene, and
`leanchecker` provide the primary mature-prover evidence. Z3 obligations, a
small certificate kernel, tampered controls, direct Python/Go enumeration, and
an independent checker provide supporting diversity; they do not replace Lean.

## Manuscript, provenance, and limitations

Run `make paper` to build with the checksum-pinned official
`lipics-v2021.cls` v3.1.3. The PDF is anonymous and the build enforces the
OPODIS 2026 15-page main-text limit. Acquisition hashes, archive lineage, and
canonical choices are documented in `provenance/PROVENANCE.md`,
`provenance/CANONICAL_FILE_MAP.csv`, and `docs/DECISION_LOG.md`. Scientific and
engineering limits are stated in `docs/LIMITATIONS.md`.

## Citation and license

Citation metadata is in `CITATION.cff`. Canonical original code and
documentation are MIT licensed; vendored and historical materials retain
their own terms as recorded in `THIRD_PARTY_NOTICES.md`.
