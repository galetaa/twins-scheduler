# Third-party notices

## LIPIcs author package

`vendor/lipics/` is the complete, unmodified LIPIcs author package v2021.1.3
downloaded from Dagstuhl Publishing. The package is licensed under LPPL 1.3c;
its `LICENSE.md` is preserved. The original official ZIP is retained at
`provenance/source_archives/lipics-v2021.1.3-authors.zip`.

Official source: `https://submission.dagstuhl.de/styles/download-tag/lipics/v2021.1.3/authors/zip`
Package SHA-256: `b9a4a6d6b44444cc4b9463c8d402e8f41b87e411a344b4af2508cd5bed6c19ef`
Class SHA-256: `ecae53dfd29c7b22d02a9065327c104760fb726a028b146d556732021a5977f0`

## `relab/hotstuff` historical material

Historical snapshots contain selected source and documentation files
from `relab/hotstuff` commit
`3179c6e62929294961acbfd9bf8445769716a121`.

Upstream project: `https://github.com/relab/hotstuff`  
License: MIT. The upstream license text is preserved with the historical
snapshot.

The snapshot pins engineering semantics audited in earlier gates and is retained
for provenance. Gate 7′ does not execute the full upstream client and does not
claim a production-client refinement proof.

## CometBFT source-correspondence fragments

`models/tendermint_style/upstream_fragments/` contains selected specification and implementation
fragments from CometBFT tag `v0.40.0`, commit
`0880b4d378f347ab16e54ec677ff50d803f37d62`.

Upstream project: `https://github.com/cometbft/cometbft`  
License: Apache License 2.0. The upstream license text, source register and
checksum manifest are preserved in that directory.

The fragments are used only for source correspondence concerning lock updates,
valid-round state and duplicate-vote processing. `implementation_fixture/`
contains small independent models, not copied production consensus code. No
production vulnerability is asserted.

## External system tools

CPython, uv, Go, Lean/elan, TeX Live, the host C compiler and Z3 are external
runtimes and are not bundled. Their pinned acquisition data and executed
versions are recorded in `containers/TOOLCHAIN_SOURCES.md` and build logs.
