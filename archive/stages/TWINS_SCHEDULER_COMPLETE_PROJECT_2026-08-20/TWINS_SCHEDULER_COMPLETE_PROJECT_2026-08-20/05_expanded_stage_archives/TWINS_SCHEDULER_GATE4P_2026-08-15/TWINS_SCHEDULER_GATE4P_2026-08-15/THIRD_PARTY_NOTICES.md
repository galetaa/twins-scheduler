# Third-party notices

The directory `inputs/hotstuff_snapshot/` contains selected source and
documentation files from `relab/hotstuff` at commit
`3179c6e62929294961acbfd9bf8445769716a121`.

Upstream project: `https://github.com/relab/hotstuff`

License: MIT. The upstream license text and copyright notice are preserved in
`inputs/hotstuff_snapshot/LICENSE`.

The copied files pin the network/scenario semantics audited by this artifact.
They are not imported into the Python checker. `conformance/go_harness/main.go`
is a clean, dependency-free executable extraction of the relevant admission and
pending-queue rules, created for differential conformance testing; it is not a
copy of the full upstream package and does not execute upstream consensus code.
