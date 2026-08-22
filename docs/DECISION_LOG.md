# Decision log

## D-001 — Acquisition unit

- Decision: preserve the complete supplied 2026-08-21 directory beneath
  `provenance/raw_inputs/`, not only files whose names contain `input`.
- Reason: the acquisition boundary is a directory and reports/generated
  evidence are part of the requested provenance.
- Rejected: copying only the ten ZIP files.  That would lose loose audit,
  manuscript and finalization records.

## D-002 — Historical expansion

- Decision: expand each immutable ZIP afresh into a separate
  `archive/stages/<archive-name>/` directory.
- Reason: this gives a direct archive-to-snapshot lineage and avoids trusting
  the pre-expanded copies embedded in the supplied complete package.
- Rejected: promote the supplied `history/expanded` tree to active source.

## D-003 — Canonical source layer

- Decision: use the active non-history files from the supplied 2026-08-21
  final-complete snapshot as the consolidation base, then verify and repair
  them in the new repository.
- Reason: a recursive content diff shows additions after the 2026-08-20
  post-audit ZIP: structural Lean modules, the bounded Tendermint-style bridge,
  Go comparison, revised paper, related-work matrix and final check scripts.
- Rejected: the complete-project archive lacks the post-audit changes; the
  post-audit archive lacks the 2026-08-21 additions.

## D-004 — Manuscript versions

- Decision: start from `FULL_MANUSCRIPT_FINAL_2026-08-21.md`; retain the
  2026-08-21 A4 PDF only as a historical review PDF until a real official-class
  build succeeds.
- Rejected: the 2026-08-20 revised/submission text and the Gate 8 manuscript
  are superseded; the A4 review PDF cannot be relabelled as LIPIcs.

## D-005 — Primary mature prover

- Decision: Lean is primary; Coq is retained as secondary/archival unless it
  can be built without creating two independently maintained canonical proofs.
- Reason: the 2026-08-21 Lean tree covers all named audit obligations and the
  task explicitly prefers Lean.
- Rejected: treating the project-local certificate kernel or SMT as a mature
  prover.

## D-006 — Supplied status reports

- Decision: all supplied PASS/NOT_RUN records are historical evidence only.
  New canonical status is derived exclusively from commands run in this
  repository and complete logs under `build_logs/`.
- Rejected: copying `GATE_STATUS.csv` values into the release status.

## D-007 — Git text conversion in immutable material

- Observation: after the first import commit, a blob-level audit found that
  the user's global `core.autocrlf=input` had normalized CRLF in some loose CSV
  provenance files.  The original workspace, raw-input worktree copies and ZIP
  archives were unchanged.
- Decision: add repository attributes with `-text` for `raw_inputs`,
  `source_archives` and `archive/stages`, then re-index those paths from the
  unchanged copies.  Verify every indexed raw-input blob against
  `RAW_INPUTS_SHA256SUMS`.
- Rejected: rewrite the first commit, which would obscure the actual sequence
  of work; or accept normalization, which would violate byte preservation.

## D-008 — Go module boundary

- Observation: a root `go test ./...` initially traversed Go fragments inside
  immutable historical snapshots and attempted to resolve their unrelated
  upstream dependencies.
- Decision: keep one active root Go module and add non-active fence modules at
  `archive/go.mod` and `provenance/go.mod`.  These files sit above, not inside,
  immutable snapshots.  Copied source-correspondence fragments under `models/`
  use `.go.txt`, retaining their bytes while excluding them from compilation.
- Rejected: modify historical snapshots; depend on `archive/stages`; or hide
  failures by changing the documented command away from `go test ./...`.

## D-009 — Root `go.sum`

- Decision: omit `go.sum` while the active Go module has no third-party module
  dependencies; `go mod tidy` intentionally produces no sum file.
- Rejected: create a synthetic or invalid checksum entry only to satisfy a
  cosmetic tree template.
