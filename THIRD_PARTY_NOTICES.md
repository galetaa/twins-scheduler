# Third-party notices

## `relab/hotstuff`

`inputs/hotstuff_snapshot/` contains selected source and documentation files
from `relab/hotstuff` commit
`3179c6e62929294961acbfd9bf8445769716a121`.

Upstream project: `https://github.com/relab/hotstuff`  
License: MIT. The upstream license text is preserved in
`inputs/hotstuff_snapshot/LICENSE`.

The snapshot pins engineering semantics audited in earlier gates and is retained
for provenance. Gate 7′ does not execute the full upstream client and does not
claim a production-client refinement proof.

## CometBFT

`inputs/cometbft_v0.40.0/` contains selected specification and implementation
fragments from CometBFT tag `v0.40.0`, commit
`0880b4d378f347ab16e54ec677ff50d803f37d62`.

Upstream project: `https://github.com/cometbft/cometbft`  
License: Apache License 2.0. The upstream license text is preserved in
`inputs/cometbft_v0.40.0/LICENSE`; source URLs, retrieval date, commit and local
hashes are recorded in `inputs/cometbft_v0.40.0/SOURCE.json` and its manifest.

The fragments are used only for source correspondence concerning lock updates,
valid-round state and duplicate-vote processing. `implementation_fixture/`
contains small independent models, not copied production consensus code. No
production vulnerability is asserted.

## System tools

CPython, Go, the host C compiler and Z3 are external runtimes and are not
bundled. Their versions are recorded under `environment/` and
`proof_outputs/smt_proof_report.json`.
