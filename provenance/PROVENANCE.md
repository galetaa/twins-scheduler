# Provenance

## Acquisition boundary

The workspace contained one supplied directory,
`TWINS_SCHEDULER_FINAL_COMPLETE_2026-08-21`.  It was discovered on
2026-08-22 in `/home/galetka/Documents/Programming/twins-scheduler`.  The
entire directory was copied byte-for-byte below `provenance/raw_inputs/`
before any canonical source was edited.  The supplied tree remains untouched.

`RAW_INPUTS_MANIFEST.csv` inventories all 1,567 supplied files with size,
SHA-256, source mtime, role, material type, successor and conflict fields.
`RAW_INPUTS_SHA256SUMS` verifies the immutable copy.  The import verification
is in `build_logs/provenance_import.log`.

## Archive lineage

The newest complete-project archive is
`TWINS_SCHEDULER_COMPLETE_PROJECT_2026-08-20.zip` (SHA-256
`4bc0818c89d3b9f2e2ded63ba35ea43162332f3b7df2e6854f7c5eabd56290a5`).
The newest post-audit layer is
`TWINS_SCHEDULER_POST_AUDIT_FINAL_2026-08-20.zip` (SHA-256
`732584aa8e4dec44931e4adc454a4645aa92ce37dc0a9b5b2530fa77a6f87cd6`).
The supplied 2026-08-21 directory adds a broader Lean development, a Go
bridge, revised manuscript, bounded protocol instantiation, updated related
work and final-but-still-conditional reports.  Its own reports explicitly say
that mature-prover and official LIPIcs builds had not been run.

All ten supplied ZIP files are copied to `provenance/source_archives/`.
Their expanded snapshots in `archive/stages/` were produced directly from
those ZIP files after rejecting unsafe absolute or parent-traversal entries.
No active build is permitted to read `archive/stages/`.

## Canonical selection

The active starting point is the non-history portion of the supplied
2026-08-21 snapshot because content comparison shows that it strictly adds the
audit-response sources absent from the 2026-08-20 post-audit ZIP.  File dates
alone were not used.  The selected Markdown manuscript is
`FULL_MANUSCRIPT_FINAL_2026-08-21.md` (SHA-256
`6086987ac088b29b7f810e9908b35fc268b6b33e14da5c2a8361f685df5d0ba7`).
The selected historical review PDF is
`TWINS_SCHEDULER_FINAL_MANUSCRIPT_2026-08-21.pdf` (SHA-256
`a5a32cd0e5afa60b0f2c981ebbd2b17975baad506eb2a0f71a6dcba962a5d4a9`).
It is not treated as an official LIPIcs build.

The inventory contains 665 unique hashes and 902 duplicate instances across
436 exact-duplicate groups.  Eighteen manuscript records belong to logical
version families with different content; all are retained in raw provenance
and the rejected active candidates are recorded in `docs/DECISION_LOG.md`.

## Integrity caveat

One supplied checksum sidecar contains an absolute `/mnt/data/...` filename.
The expected digest is valid, but the path is not portable.  Import
verification therefore compares the first digest field with the adjacent ZIP
basename.  The sidecar itself is preserved unchanged.

