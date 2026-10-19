# Unmodified CometBFT implementation conformance

This experiment executes the **actual, unmodified CometBFT v0.39.3
consensus state machine** at commit
[`49b82838fcca442b2445f76605c101609ed04130`](https://github.com/cometbft/cometbft/tree/49b82838fcca442b2445f76605c101609ed04130).
It validates implementation assumptions used by the paper's smaller models.

The experiment contains four ordinary-operation scenarios, fourteen explicit
checks, thirty-two votes emitted and signed by native state machines, and 132
recorded scheduling/state events. Each scenario instantiates four unchanged
validators with equal voting power. All tests pass. **No production code is
patched, no protocol fault is injected, and no conflicting commit is attempted.**

The existing Python mutant trace remains a distinct experiment in its declared
transition system. These native checks do not upgrade it into a production-client
fault witness or a refinement proof.

## Reproduce

From the repository root, with Python 3, Git, and a Go installation supporting
toolchain selection:

```sh
./scripts/run_native_conformance.sh
```

The runner selects the pinned **Go 1.25.0** toolchain (downloaded by Go if needed),
clones the exact public source into `.cache/native_cometbft`, verifies
the commit and clean tracked source, copies one added `_test.go` file into its
`consensus` package, and executes:

```sh
go test ./consensus -run '^TestNativeConformance$' -count=1 -timeout=120s -json
```

The added test file is then removed. The `.go.txt` suffix in this repository
prevents the main project's unrelated Go module from trying to compile it.
`TWINS_OUTPUT_ROOT` redirects the default result directory to
`$TWINS_OUTPUT_ROOT/results/native`; `TWINS_LOG_DIR` receives the test receipts
and a compact command summary. Build and source caches remain in this project's
`.cache` directory.

Use an existing clean checkout or an explicit toolchain as follows:

```sh
./scripts/run_native_conformance.sh --source-dir /path/to/pinned/cometbft --go /path/to/go
```

An additional run of the same scenarios with Go's race detector is available:

```sh
./scripts/run_native_conformance.sh --race --output-dir results/native_race
```

The committed repeatability receipt can be regenerated with:

```sh
python3 experiments/native_cometbft/check_repeatability.py
```

It compares three additional normal executions and one race-detector execution
with the semantic reference, and checks `TWINS_OUTPUT_ROOT` / `TWINS_LOG_DIR`
routing. Temporary per-run evidence stays in `.cache/native_repeatability`;
`results/native/native_repeatability.json` retains the passing Go receipts.

Initial compilation downloads the dependencies declared in the unchanged
upstream `go.mod`/`go.sum`. Native execution, the independent signature audit,
and repeatability checks are mandatory stages of `./reproduce_revision.sh`;
`make native` runs just these stages. They remain separate from the lightweight
model tests in `make test`. No sockets,
external peers, or application networks are started by the harness.

## What actually runs

`native_conformance_test.go.txt` uses the upstream test constructor
`newStateWithConfig`. It creates actual `consensus.State`, `VoteSet`,
`BlockExecutor`, in-memory `BlockStore`, local ABCI application, and Ed25519
signing objects. The state machine's `defaultDecideProposal`, `defaultDoPrevote`,
`enterPrecommit`, `tryAddVote`, `enterCommit`, and `finalizeCommit` are the
unaltered upstream functions.

The test controls dispatch into `State.handleMsg` and `State.handleTimeout`.
Every proposal, block part, and honest vote delivered by the test was previously
emitted into a native state's internal message queue. The harness does not
construct a quorum by signing votes on behalf of validators. It verifies each
emitted vote using the production `Vote.Verify` routine and records its canonical
sign bytes and Ed25519 signature.

The ticker records **only timeout requests made by the native implementation**.
The scripted dispatcher can fire such a recorded request; it cannot invent a
quorum-wait timeout to force progress. Tests check both sides of the two-vote /
three-vote boundary before firing the resulting native timeout.

### Scenarios and observations

| Scenario | Native observations | Checks / emitted votes / recorded events |
|---|---|---:|
| Normal commit, missing-block catch-up, and vote immutability | Retransmission does not add voting power. A real three-prevote PoLC updates both lock and valid fields. Three native precommits cause block validation, block-store write, and application execution. The emitted precommit bytes and signature remain valid after its signer advances height. A fourth node with the certificate but no block stays in Commit until genuine Merkle-checked block parts arrive, then commits the same block. | 6 / 7 / 30 |
| Mixed-quorum timeout guards | Missing-proposal timeout emits nil. Two distinct prevotes do not schedule prevote-wait; three mixed prevotes do. Its timeout emits a native nil precommit. Two precommits do not schedule advancement; three nil precommits do, and the scheduled timeout advances one round. | 3 / 7 / 29 |
| Lock persistence and locked prevote | A legal mixed-precommit timeout preserves lock and valid block. The actual next proposer supplies a different valid block; the locked recipient's unchanged prevote rule emits a vote for its previous lock. No node commits in this scenario. | 3 / 9 / 38 |
| Valid-block proposal reuse | A validator that retained a valid block becomes the actual next-round proposer. It reuses that block and includes the retained POL round; its existing authentic PoLC makes the proposal complete and the native prevote matches the reused block. | 2 / 9 / 35 |

The proposer sequence is obtained from the **actual weighted proposer-priority
implementation**, with four equal weights and deterministic public keys; it is
not manually assigned after initialization. In the normal-commit scenario both
deciding observers store the same block. The other scenarios produce no commit.

## Evidence and integrity

The runner writes:

- `results/native/native_conformance.json`: complete per-event native states,
  public keys, vote sign bytes, signatures, checks, and terminal states;
- `results/native/native_summary.json`: the semantic result counts and scope;
- `results/native/native_provenance.json`: exact commit/tree, SHA-256 hashes of
  the exercised source files, test/runner hashes, Go version, actual command,
  exit code, passing Go test records, and result hashes;
- `results/native/native_test_events.jsonl`: the actual `go test -json` receipt;
- `results/native/native_test_stderr.txt`: captured test stderr.

An independent signature audit uses Python `cryptography` / OpenSSL, rather than
CometBFT's Ed25519 implementation:

```sh
uv run --extra native-audit python experiments/native_cometbft/audit_evidence.py
```

It verifies all 32 signatures and parses their canonical protobuf sign bytes to
check type, height, round, block hash, chain ID, nanosecond timestamp, and signer
address against the recorded metadata. It also verifies the test/runner/result
receipts and absence of conflicting same-slot vote records. Its output is
`results/native/native_signature_audit.json`. This is an independent
cryptographic/evidence audit, not a second consensus implementation.

There are four passing subtests and one passing parent test; this is not reported
as five independent scenarios. The runner verifies source integrity both before
and after execution, refuses other untracked Go files, and removes the added test
without modifying tracked production files.

The fixed keys, genesis, schedule, and assertions make the semantic outcomes
deterministic. Native wall-clock proposal/vote timestamps are deliberately left
untouched, so signatures, raw test receipts, and raw-evidence hashes can differ
between successful reruns. The semantic summary can be compared directly.

## Assurance boundary

This is implementation-level evidence for the exercised guards, with several
constraints:

1. Consensus dispatch runs synchronously in process. The reactor, peer network,
   WAL receive loop, and production timer goroutines are not exercised.
2. The native block store and ABCI application use the upstream in-memory test
   fixture. A successful store write does not claim disk durability or crash
   recovery.
3. Ed25519 signatures are real, but the private signer is upstream `MockPV` with
   deterministic **test-only keys**, not `FilePV` persistence. The harness checks
   that the normal schedules emit no conflicting same-slot vote.
4. The four scripts are finite normal-operation checks. They do not establish
   protocol safety for all schedules, reproduce the model's mutation, prove
   graph/frontier theorems, or demonstrate a deployed-client vulnerability.
5. Output immutability is observed across normal local height advancement. The
   general irreversible-output assumption and the model's repair timing theorem
   retain their separately stated proof and model evidence.

These boundaries make the bridge useful: it replaces source-reading-only support
for specific assumptions with successful execution of the precise implementation
whose rules the abstraction cites, while preserving the distinction between
model claims and production-code evidence.
