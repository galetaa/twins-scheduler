# Third-party notices

## `relab/hotstuff`

The directory `inputs/hotstuff_snapshot/` contains selected source and
documentation files from `relab/hotstuff` at commit
`3179c6e62929294961acbfd9bf8445769716a121`.

Upstream project: `https://github.com/relab/hotstuff`

License: MIT. The upstream license text and copyright notice are preserved in
`inputs/hotstuff_snapshot/LICENSE`.

The copied files pin the network/scenario semantics audited in Gate 4′. They
are not imported into the Python checker. `conformance/go_harness/main.go` is a
clean, dependency-free executable extraction of the relevant admission and
pending-queue rules; it is not a copy of the full upstream package and does not
execute upstream consensus code.

## CometBFT

The directory `inputs/cometbft_v0.40.0/` contains selected source,
specification, metadata, and license files from CometBFT tag `v0.40.0`, commit
`0880b4d378f347ab16e54ec677ff50d803f37d62`.

Upstream project: `https://github.com/cometbft/cometbft`

License: Apache License 2.0. The upstream license text is preserved in
`inputs/cometbft_v0.40.0/LICENSE`; exact source URLs, retrieval date, commit,
and local hashes are recorded in `inputs/cometbft_v0.40.0/SOURCE.json` and
`MANIFEST.sha256`.

The selected files are used only to map abstract obligations concerning
prevote/precommit locking, valid-round state, and duplicate-vote processing to
a pinned implementation and specification. The Go fixtures under
`conformance/comet_vote_fixture/` and `implementation_fixture/go_harness/` are
small independent correspondence models. They do not assert full-client
conformance and do not report a production vulnerability.
