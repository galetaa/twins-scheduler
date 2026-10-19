# Third-party notices

## LIPIcs author package

`vendor/lipics/` is the complete, unmodified LIPIcs author package v2021.1.3
downloaded from Dagstuhl Publishing. The package is licensed under LPPL 1.3c;
its `LICENSE.md` is preserved. The original official ZIP is retained at
`provenance/source_archives/lipics-v2021.1.3-authors.zip`.

Official source:
[Dagstuhl author package](https://submission.dagstuhl.de/styles/download-tag/lipics/v2021.1.3/authors/zip).

- Package SHA-256: `b9a4a6d6b44444cc4b9463c8d402e8f41b87e411a344b4af2508cd5bed6c19ef`.
- Class SHA-256: `ecae53dfd29c7b22d02a9065327c104760fb726a028b146d556732021a5977f0`.

## `relab/hotstuff` historical material

Historical snapshots contain selected source and documentation files
from `relab/hotstuff` commit
`3179c6e62929294961acbfd9bf8445769716a121`.

Upstream project: [relab/hotstuff](https://github.com/relab/hotstuff).

License: MIT. The upstream license text is preserved with the historical
snapshot.

The snapshot pins engineering semantics audited in earlier gates and is retained
for provenance. Gate 7′ does not execute the full upstream client and does not
claim a production-client refinement proof.

## CometBFT source fixtures

Upstream project: [CometBFT](https://github.com/cometbft/cometbft).

License: Apache License 2.0. Each retained source fixture includes the upstream
license text in its own `LICENSE` file.

### v0.39.3 fixture used by the revision

[upstream_v0393](models/tendermint_style/upstream_v0393/) contains the selected,
unmodified consensus specification, `consensus/state.go`, `types/vote_set.go`,
and license from tag `v0.39.3`, immutable commit
`49b82838fcca442b2445f76605c101609ed04130`.

The fixture's `SOURCE.json` records upstream paths, immutable URLs, original Git
blob identifiers, local filenames, sizes, and SHA-256 hashes. Its
`GITHUB_RECEIPTS.json` preserves the tag and commit lookup evidence;
`MANIFEST.sha256` verifies the saved files. The Go files use `.go.txt` local
suffixes so the repository's Go test command does not compile the source fixture
as a client package. Their bytes, including copyright and license notices,
are preserved.

These files provide primary-source correspondence for the new bounded trace.
They are not executed as a production CometBFT client, and their integrity checks
do not establish transition refinement or a production vulnerability.

### Separately retained v0.40.0 fixture

[upstream_fragments](models/tendermint_style/upstream_fragments/) retains the
earlier specification and implementation material from tag `v0.40.0`, commit
`0880b4d378f347ab16e54ec677ff50d803f37d62`. Its source register, Apache-2.0
license text, and checksum manifest remain with that snapshot. It has not been
relabeled as v0.39.3 or substituted for the revision's source pin.

The independently authored executable models elsewhere in this repository are
separate from these upstream evidence files. The
[source mapping](models/tendermint_style/COMETBFT_V0393_MAPPING.md) identifies
which exercised rules are compared with the revision's pinned sources.

## External system tools

CPython, uv, Go, Lean/elan, Pandoc, TeX Live, Poppler, the host C compiler, and
Z3 are external build or execution tools. Their runtime distributions are not
vendored as original repository code. Downloaded packages retain their upstream
license terms.

The Python dependency lock pins `z3-solver==4.13.3.0`; its wheel supplies the
Z3 runtime used by the SMT checks. Pandoc generates LaTeX from the Markdown
manuscript. Acquisition pins where supplied, together with executed tool
versions, are documented in
[toolchain sources](containers/TOOLCHAIN_SOURCES.md), `pyproject.toml`, `uv.lock`,
and the build logs. A source or package checksum identifies the acquired bytes;
it is not a proof of protocol behavior.
