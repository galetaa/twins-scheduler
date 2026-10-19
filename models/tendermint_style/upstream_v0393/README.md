# Verified CometBFT v0.39.3 source fixture

These files are unmodified primary-source evidence for the bounded rule-level
model. They are not a Go package and are not part of the executable test client.
The upstream Go files use local `.go.txt` names so that `go test ./...` does not
try to compile two different upstream packages as part of this repository.
Their bytes are unchanged: `SOURCE.json` records the upstream paths, immutable
URLs, original Git blob SHA-1 values, SHA-256 values and local filenames.

The official tag v0.39.3 resolves to commit
`49b82838fcca442b2445f76605c101609ed04130`. `GITHUB_RECEIPTS.json`
retains the tag and commit API responses.

Run `sha256sum -c MANIFEST.sha256` from this directory to verify the fixture.
The original Apache-2.0 license is retained in `LICENSE`.
