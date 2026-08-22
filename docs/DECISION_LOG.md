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

## D-010 — Repairing the supplied Lean sources

- Observation: the first genuine `lake build` failed on an obsolete
  `Std.Tactic.Omega` import, an unavailable `Set` alias, invalid filter/sublist
  proofs, an ambiguous conjunction proof term, a non-reducing derived `BEq`
  branch, and an invalid negative-control tactic.
- Decision: use the v4.33 `Std.Tactic` export; encode an observation set as its
  extensionally equivalent predicate `Observation → Prop`; use library
  `List.mem_filter`/`List.filter_sublist`; supply explicit conjunction terms;
  pattern-match the lock variant; and discharge the finite hidden-state facts
  by computation/simplification.
- Scientific effect: theorem signatures and paper-level premises were not
  weakened.  The original files remain in raw provenance and the canonical map
  records old and new hashes.  Three failed build attempts are retained beside
  the final passing log.
- Rejected: downgrade Lean; introduce `sorry`; delete failing modules; or replace
  the mature proof with the project-local kernel.

## D-011 — Paper numbering and related-work comparison

- Decision: retain only Theorems 1--3 in the paper, with one numbered lemma,
  corollary and two propositions; keep historical IDs T1/T2/T3/T6 only in the
  claim and artifact ledgers.
- Decision: expand the structural criterion into ten explicit premises.  The
  first nine separately state the requested opportunity, pivot, support,
  evidence, shared-edge, phase-label and grammar-coupling conditions; the tenth
  connects certificates to irreversible correct decisions.
- Decision: add Mallory and expose protocol-conformance and mechanization
  columns in the related-work matrix.  Unknown capabilities are recorded as
  `not reported`, not inferred to be absent.
- Rejected: present a richer scheduler API as novelty, or report bounded
  Tendermint-style refinement as production-client conformance.

## D-012 — Official LIPIcs source and generated body

- Decision: vendor the complete, unmodified official Dagstuhl author package
  `lipics-v2021` v2021.1.3 and build `main.tex` with its class checksum pinned.
- Decision: keep Markdown and the active LaTeX `body.tex` as the two manuscript
  sources and enforce their scientific statements with a consistency checker.
- Rejected: retain the stale intermediate `body_source.md`, which duplicated an
  older manuscript and still claimed that Lean was unbuilt; or relabel the A4
  review PDF as an official LIPIcs build.

## D-013 — Deterministic paper evidence

- Observation: two otherwise identical pdfTeX runs initially differed in the
  generated trailer identifier and source-path metadata.
- Decision: fix the trailer ID, omit volatile dates and suppress PTEX source
  metadata in `main.tex`; require byte identity between isolated and committed
  PDFs. The scientific content and anonymous document metadata are unchanged.
- Rejected: compare only extracted text or accept a changing PDF checksum.

## D-014 — Release self-reference boundary

- Decision: build both archives from the annotated tag in an external temporary
  staging directory. The Git ZIP contains a clean clone including `.git`; the
  source tar is `git archive` output. Archive SHA files and integrity logs are
  sidecars and therefore do not recursively appear inside the archives they
  describe.
- Rejected: create an archive inside the tree being recursively archived,
  which is nondeterministic and self-referential.

## D-015 — Container portability repairs

- Observation: clean Debian container runs exposed three host assumptions:
  the `python` alias, retired live-mirror TeX revisions, and scalable Latin
  Modern font maps; a C header set was also required by the local Z3 wrapper.
- Decision: install `python-is-python3`, `libc6-dev`, and `lmodern`; fetch the
  already checksum-pinned TeX packages from immutable official Debian snapshot
  URLs instead of the moving live mirror. A subsequent full container
  reproduction passed.
- Rejected: relax TeX revisions, disable microtype expansion, use unpinned
  `latest`, or skip SMT in the container.
