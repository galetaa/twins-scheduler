# A complete four-validator Tendermint-style witness

## Result and evidence level

The new executable trace produces conflicting decisions at **two unmutated
validators**, `A = 0` and `C = 1`, when the pivot `P` omits a single persistent
lock assignment in round 0 and the scheduler admits `B -> P: PREVOTE(0,0)` but withholds
`B -> P: PRECOMMIT(0,0)`. Every quorum consists of three distinct, actually
emitted, authenticated vote records. There are no network messages named
`POLKA` or `COMMIT`, no preloaded quorum bases, and no synthetic pivot votes.

The trace also identifies a sharper boundary than “repair before the second
decision.” If the coarse edge is on and its round-0 repair precommit arrives
**after P has signed its round-1 precommit but before C's second decision**,
then `A = 0, P = 0, C = 1`. Repair cannot retract the vote already in the
network buffer. The relevant cutoff is the pivot's last indispensable vote
emission, not the observer's later certificate delivery.

This is an executable witness in a declared, small transition system derived
from CometBFT's published rules. It is neither execution of the production
client nor a formal refinement proof for that client. It replaces an
arithmetic-only explanation of this particular trace with guarded local
states, actual vote sets, legal timeouts, and a complete network history.

## Reproduction

From the repository root:

```sh
python scripts/run_concrete_trace.py
uv run --frozen pytest -q tests/unit/test_concrete_trace.py
```

The runner uses only the Python standard library and creates:

- `results/new/concrete_trace.json`: twelve complete traces, states after every
  event, all signed records, all emitted envelopes and their final buffer
  status, local certificates, checkpoints, and independent audit results;
- `results/new/concrete_trace.csv`: the twelve terminal classifications.

The implementation is `src/python/twins_scheduler/concrete_trace.py`. It
imports neither `bounded.py` nor `event_loop.py`. The dedicated test module
has 14 tests, including damaged-authentication, absent-envelope,
unjustified-timeout, absent-PoLC, duplicate-vote, duplicate-delivery, and
incorrect-certificate-timing controls, plus a FIFO-compatible gossip relay
control that retains the late-repair conflict.

## Exact source pin and rule correspondence

The source pin for this new witness is **CometBFT v0.39.3**, commit
`49b82838fcca442b2445f76605c101609ed04130`. The verified exact files are under
`models/tendermint_style/upstream_v0393/`; `SOURCE.json`, `GITHUB_RECEIPTS.json`,
and `MANIFEST.sha256` retain their provenance and integrity information.

The previously supplied `upstream_fragments/` directory is **v0.40.0**,
commit `0880b4d378f347ab16e54ec677ff50d803f37d62`, despite the older mapping
document's v0.39.3 title. It must not be cited as an exact v0.39.3 snapshot.

| Rule exercised by the witness | Official pinned source | Concrete implementation |
|---|---|---|
| A designated proposer reuses its valid block if present | [`defaultDecideProposal`](https://github.com/cometbft/cometbft/blob/49b82838fcca442b2445f76605c101609ed04130/consensus/state.go#L1246) | `propose`; `valid_value` and `valid_round` survive round advancement |
| A locked validator prevotes its lock; an unlocked one can prevote the received valid proposal | [`defaultDoPrevote`](https://github.com/cometbft/cometbft/blob/49b82838fcca442b2445f76605c101609ed04130/consensus/state.go#L1387) | `_enter_prevote` |
| A current-round PoLC updates the valid block separately from the persistent lock assignment | [`addVote`, prevote case](https://github.com/cometbft/cometbft/blob/49b82838fcca442b2445f76605c101609ed04130/consensus/state.go#L2312) | `_after_vote`; this update is retained in the mutant |
| A known-block PoLC causes lock/relock before precommit | [`enterPrecommit`, lock assignments](https://github.com/cometbft/cometbft/blob/49b82838fcca442b2445f76605c101609ed04130/consensus/state.go#L1572) | `_enter_precommit`; only P's round-0 assignment is omitted in the mutant |
| A mixed prevote quorum can enable timeout and a nil precommit | [`enterPrevoteWait` and `enterPrecommit`](https://github.com/cometbft/cometbft/blob/49b82838fcca442b2445f76605c101609ed04130/consensus/state.go#L1448) | `_after_vote`, `timeout`, `_enter_precommit` |
| Advancing after a precommit timeout requires any three distinct precommits | [`enterPrecommitWait`](https://github.com/cometbft/cometbft/blob/49b82838fcca442b2445f76605c101609ed04130/consensus/state.go#L1606) | `ARM_TIMEOUT`, `timeout`, `_enter_next_round` |
| Three matching precommits enter Commit and prevent further signing at that height | [`addVote`, precommit case](https://github.com/cometbft/cometbft/blob/49b82838fcca442b2445f76605c101609ed04130/consensus/state.go#L2386) | `_after_vote`, `_start_commit` |
| A commit quorum does not supply missing block data; decision waits for the matching block | [`enterCommit` and `tryFinalizeCommit`](https://github.com/cometbft/cometbft/blob/49b82838fcca442b2445f76605c101609ed04130/consensus/state.go#L1638) | `_start_commit`, `_finalize_commit`, explicit `send_block` relay |

The official [consensus specification](https://github.com/cometbft/cometbft/blob/49b82838fcca442b2445f76605c101609ed04130/spec/consensus/consensus.md)
supplies the step, timeout, PoLC, gossip, and commit terminology. Source
correspondence documents the exercised guards; it does not assert that every
branch of these production functions is implemented by the model.

## Participants, authentication, and bounded environment

There are four equally weighted identities, threshold `q = 3`, one fixed
height `H = 1`, and two conflicting but application-valid blocks denoted by
`0` and `1`. The proposer prefix is fixed to `B` in round 0 and `C` in round
1. The model checks designated-proposer signatures; it does not simulate
the weighted proposer-priority algorithm.

| Identity | Role | Actual signed votes in the fine mutant trace |
|---|---|---|
| B | The sole Byzantine identity; authenticated vote production is adversarial | `PV(0,0), PC(0,0), PV(1,1), PC(1,1)` |
| A | Unmutated validator and first deciding observer | `PV(0,0), PC(0,0)` |
| P | Pivot; unmutated in baseline, missing only its round-0 persistent lock assignment in mutant | `PV(0,0), PC(0,0), PV(1,1), PC(1,1)` |
| C | Unmutated validator and round-1 proposer/deciding observer | `PV(0,nil), PC(0,nil), PV(1,1), PC(1,1)` |

Here `PV(r,v)` means a height-1 prevote for value `v` in round `r`, and `PC`
means precommit. Correct identities sign once per `(height, round, type)`.
No same-round equivocation by B is needed; its cross-round support is
adversarially chosen. B's round-0 precommit may be emitted before it sees a
PoLC because B is explicitly Byzantine. Every A, P, and C vote is generated
by the modeled rules, with the one declared P mutation. In particular, P's
round-1 lock assignment executes normally. The witness therefore needs only
one omitted logical lock-state update at one validator in the first round; a
permanent removal of all later lock assignments is unnecessary.

Authentication uses deterministic **test-only HMAC tags**, not production
Ed25519 keys. The scheduler cannot choose signers or construct signed
records; delivery resolves an existing authenticated envelope. Quorum
accounting uses signer identity, so a relayed duplicate does not contribute
another vote. This models authenticated-message semantics, not cryptographic
security or compatibility with CometBFT's wire format.

Only `(transport sender B, receiver P, H=1, round=0)` is controlled by the
tested admission policy. Its two emitted envelopes are exactly `E = PV(0,0)`
and `R = PC(0,0)`. B's signed round-0 proposal initially goes to A. A then
gossips **that same signed proposal and block** to P. Transport sender A and
proposal signer B are separately represented. This prevents a hidden change
to proposal admission when the controlled B-to-P edge is turned off.

All other deliveries, fixed finite withholding choices, and timeout
opportunities are fixed by `run_trace`. Votes that a changed execution does
not generate are recorded as unavailable delivery opportunities. They are
never injected to keep a table artificially constant. Undelivered emitted
envelopes remain explicitly buffered. The finite execution makes no fairness
or liveness claim about those pending messages.

There is no hidden phase-specific admission on another edge. The fixed
non-self active directed edges are shown below; all self-deliveries are
admitted. All other edges are off. The audit independently checks that the
actual complete traces have uniform delivery outcomes on every other
sender/receiver/height/round combination.

| Round | Fixed active directed edges | Variable edge |
|---|---|---|
| 0 | `B→A, A→P, A→C, P→A, P→C, C→P` | `B→P`: E/R admission |
| 1 | `B→P, B→C, C→P, P→C` | None |

## Complete fine mutant execution

Initially A, P, and C are at `(H=1,r=0,Propose)` with no lock, valid block,
received votes, or decision. A signed vote is multicast into explicit
recipient envelopes. Its local self-envelope is emitted and then delivered
once. The following table lists all externally scheduled steps of the fine
mutant run; the JSON expands each into signatures, transmissions,
acceptances, guards, and local transitions.

| Step | Delivery or local event | Consequence justified by local evidence |
|---|---|---|
| 1 | B signs proposal `(r0, block0, validRound=-1)` and sends it to A | A accepts the complete block and signs `A:PV(0,0)` |
| 2 | A relays the same B-signed proposal and block to P | P accepts it and signs `P:PV(0,0)` |
| 3 | C's propose timeout expires without a proposal | C signs `C:PV(0,nil)` |
| 4 | B signs and emits `B:PV(0,0)` and `B:PC(0,0)` | Both E and R now exist in the buffer before E is attempted |
| 5 | Deliver `P:PV(0,0)` and `B:PV(0,0)` to A | With self-vote A, its PoLC is `{A,P,B}:0`; A sets valid/locked block `0@0`, then signs `A:PC(0,0)` |
| 6 | Deliver `A:PV(0,0)` and E=`B:PV(0,0)` to P | With self-vote P, its PoLC is `{A,P,B}:0`; P sets valid block `0@0`, omits the persistent lock assignment, and signs `P:PC(0,0)` |
| 7 | Deliver `C:PV(0,nil)` to P; deliver `P:PV(0,0)` and `A:PV(0,0)` to C | C has the mixed prevote set `{A:0,P:0,C:nil}` and no value-0 PoLC |
| 8 | C's quorum-enabled prevote timeout expires | C lawfully signs `C:PC(0,nil)` and remains without a valid block or lock |
| 9 | Deliver `A:PC(0,0)` to P and C; deliver `P:PC(0,0)` to A and C | P has `{A:0,P:0}`; C has the mixed set `{A:0,P:0,C:nil}` and arms a precommit timeout |
| 10 | Deliver `B:PC(0,0)` to A | A's local precommit set `{A,P,B}:0` reaches 3; A decides 0 and advances to height 2 |
| 11 | Deliver `C:PC(0,nil)` to P | P now has `{A:0,P:0,C:nil}` and arms a precommit timeout, while still having only two precommits for 0 |
| 12 | Attempt R=`B:PC(0,0)` to P | The phase-specific grammar drops R; P has not committed |
| 13 | P and C's quorum-enabled precommit timeouts expire | Both legally enter round 1. P keeps `valid=0@0`, `locked=none`; C keeps `valid=none`, `locked=none` |
| 14 | C signs proposal `(r1, block1, validRound=-1)`, receives it locally, and sends it to P | C and the unlocked P each sign `PV(1,1)` |
| 15 | B signs and emits `PV(1,1)` and `PC(1,1)` | B's second-round support is available without fabricating any honest vote |
| 16 | Deliver `C:PV(1,1)` and `B:PV(1,1)` to P | P obtains `{P,C,B}:1`, updates valid/locked block normally to `1@1`, and signs `P:PC(1,1)` |
| 17 | Deliver `P:PV(1,1)` and `B:PV(1,1)` to C | C obtains `{P,C,B}:1`, sets valid/locked block `1@1`, and signs `C:PC(1,1)` |
| 18 | Deliver `P:PC(1,1)` and `B:PC(1,1)` to C | With self-precommit C, the local set `{P,C,B}:1` reaches 3; C decides 1 |
| 19 | Deliver `C:PC(1,1)` and `B:PC(1,1)` to P | With its own precommit, P also decides 1 |

The only timeout opportunity omitted from the table is a disabled P prevote
timeout opportunity: after E it has already entered Precommit. It is logged
as `NO_ENABLED_TIMEOUT`. Fixed late prevote-timeout opportunities in round
1 are likewise disabled once a non-nil PoLC has produced a precommit.

### Local-state checkpoints

`v@r` denotes a persistent value and its round; a dash denotes no value.
The finalization rule clears the old height's lock/valid fields, so the
decision column carries the irreversible historical result.

| Checkpoint | A | P | C |
|---|---|---|---|
| After E | `H1/r0`, lock `0@0`, valid `0@0`, precommitted 0 | `H1/r0`, lock `—`, valid `0@0`, precommitted 0 | `H1/r0`, lock `—`, valid `—`, prevoted nil |
| After first decision | `H2`, decided 0 | `H1/r0`, lock `—`, valid `0@0`, uncommitted | `H1/r0`, lock `—`, valid `—`, precommitted nil |
| After round advancement | `H2`, decided 0 | `H1/r1`, lock `—`, valid `0@0`, Propose | `H1/r1`, lock `—`, valid `—`, Propose |
| After P's round-1 precommit | `H2`, decided 0 | `H1/r1`, lock `1@1`, valid `1@1`, precommitted 1 | `H1/r1`, lock `—`, valid `—`, prevoted 1 |
| Terminal | `H2`, decided 0 | `H2`, decided 1 | `H2`, decided 1 |

The first commit certificate is the actual signed set `{A,P,B}` in round 0;
the second is `{P,C,B}` in round 1. Their unmutated deciding observers are
A and C. P is non-Byzantine **relative to the explicitly mutated program**;
it is not a validator satisfying the original Tendermint locking rules.
There is consequently no contradiction of the unmutated protocol's safety
theorem and no claim of a deployed-client vulnerability.

## Why the baseline and coarse schedules differ

The complete canonical matrix, reproduced by the runner, is:

| Program | Admission on B-to-P round-0 edge | A decision | P decision | C decision | Agreement violation |
|---|---|---:|---:|---:|---|
| Baseline | Fine: E admitted, R withheld | 0 | — | — | No |
| Baseline | Coarse off: E and R withheld | — | 1 | 1 | No |
| Baseline | Coarse on: E and R admitted | 0 | 0 | — | No |
| Missing lock at P | Fine: E admitted, R withheld | 0 | 1 | 1 | **Yes** |
| Missing lock at P | Coarse off: E and R withheld | — | 1 | 1 | No |
| Missing lock at P | Coarse on: E and R admitted | 0 | 0 | — | No |

With the fine baseline, P retains its round-0 lock and prevotes 0 when C
proposes 1. P and C receive only a mixed round-1 prevote set, so their
quorum-enabled timeouts produce nil precommits. Neither supplies a second
value-1 commit certificate.

With the coarse edge off, P still receives the B-signed proposal through A
and prevotes 0. It lacks B's PoLC-completing prevote, receives C's nil
prevote, times out on the mixed set `{A:0,P:0,C:nil}`, and precommits nil.
A has `{A:0,B:0,P:nil}`, so A does not decide 0. P and C can legally advance
using `{A:0,P:nil,C:nil}`. Both are unlocked, and the round-1 value-1
certificate forms. A's absent first decision is essential to the safe
classification; “safe” does not mean no node decides.

With the coarse edge on in the fixed order, E causes P's round-0 precommit.
R then completes P's actual round-0 set `{A,P,B}:0`. P enters Commit and
advances height before it can vote in round 1. C's round-1 value-1 prevotes
come only from C and B, so there is no value-1 PoLC or commit quorum.

These differences arise from protocol guards and generated messages. The
execution does not force absent P votes or pretend that a precommit quorum
can be assembled without them.

## Repair timing: the vote emission frontier

Four additional cases leave the coarse edge **on** and change only when its
already-emitted R is delivered. Two use the baseline and two use the mutant.
Two further cases use a separately declared gossip route to make the late
precommit control compatible with FIFO order on every admitted peer vote
channel.

| R processing position | Baseline decisions | P-mutant decisions | What it establishes |
|---|---|---|---|
| Before round-1 entry (canonical) | `A=0,P=0` | `A=0,P=0` | The original fixed-order coarse domain is safe |
| After P signs `PV(1,1)` in mutant, before its precommit opportunity | `A=0,P=0` | `A=0,P=0` | P's prevote alone can let C lock 1, but cannot supply the missing third value-1 precommit |
| After P's round-1 precommit opportunity, direct round-1 B-to-P prevote delivery | `A=0,P=0` | **`A=0,P=0,C=1`** | Buffered support survives repair; this direct-delivery control permits non-FIFO overtaking |
| After P's round-1 precommit opportunity, B's round-1 prevote relayed through C | `A=0,P=0` | **`A=0,P=0,C=1`** | Same conflict with FIFO-compatible admitted vote-envelope order in a separate gossip skeleton |

In the last mutant case the exact causal order is:

1. A decides 0.
2. P lawfully signs `PV(1,1)` and then, on its local `{B,C,P}` PoLC,
   `PC(1,1)` under the missing-lock mutation.
3. R completes P's old-round commit quorum. P enters Commit for 0 and stops
   signing at height 1.
4. P's current proposal block and its new round-1 lock are both 1. The model
   therefore clears the mismatching proposal block and waits; it does not invent block
   0 from the precommit. A sends its known block 0, and P finalizes 0.
5. The already-emitted `P:PV(1,1)` and `P:PC(1,1)` remain deliverable to C.
   C receives its full prevote and precommit quorums and decides 1.

Thus `R < C's decision 1` is insufficient for safety once the bound permits
this alternative order. A theorem formulated in terms of “repair makes P
unavailable at C1” must also rule out an already-issued indispensable
contribution or explicitly put repair before its irreversible emission.
This is an execution-level failure of the broader premise, not a failure of
the two-policy separation in its original strictly fixed domain.

The aggregate block relay is compatible with the source's
[`addProposalBlockPart`](https://github.com/cometbft/cometbft/blob/49b82838fcca442b2445f76605c101609ed04130/consensus/state.go#L1997)
behavior: block parts can be reused across rounds, so the old block's round
does not prevent its acquisition while P commits at the same height.

### Transport ordering and the FIFO-compatible control

The direct late-precommit case allows `B:PV(1,1)` to reach P before the
earlier-emitted R=`B:PC(0,0)`. That is a valid order for an arbitrary
interception/reordering scheduler, but it does **not** preserve FIFO for
those two vote messages on the same directed peer connection. It must not
be described as a direct FIFO wire replay. The runner diagnoses this
inversion explicitly in `vote_channel_order.violations`.

The added control keeps the same fixed active graphs but changes the fixed
gossip skeleton. Its round-1 sequence is:

1. C's own prevote 1 is delivered to P.
2. B's signed prevote 1 is delivered to C. C has only its own and B's
   prevotes at this point, so it has not yet signed a precommit 1.
3. C forwards the **same B-signed prevote** to P. P now has three distinct
   signers `{P,C,B}`, obtains its PoLC, normally locks 1, and emits precommit
   1 in the mutant execution.
4. R is delivered on B-to-P, followed by the old block data needed for P's
   commit 0. The original direct copy of B's round-1 prevote is delivered
   after R and is stale at P; it does not provide the PoLC-completing copy.
5. P's already-emitted prevote and precommit 1 reach C, which decides 1.

The signed B contribution is counted once even though it has two transport
routes. The C-to-P relay follows C's own earlier prevote on that connection;
the direct B-to-P vote follows R on its connection. The checker examines
**all pairs of admitted vote envelopes on each directed peer edge across
rounds**, including not-yet-delivered earlier messages. Both relay controls
pass this FIFO check, as do the six canonical traces. Both direct
late-precommit controls are correctly identified as non-FIFO.

The FIFO check excludes proposal/block traffic and messages rejected by the
fixed graph or phase admission filter before transmission. This is a
compatibility result for the ordering of the finite vote trace, not an
execution or performance claim for CometBFT networking. The relay control
also changes one declared message-forwarding opportunity; it is not
evidence that the original fixed skeleton can be arbitrarily reordered
while preserving the original separation theorem.

## Hidden assumptions resolved and remaining limits

The trace resolves four concrete omissions in the earlier rule-level
explanation. First, P and C have lawful mixed-vote quorums that enable round
advancement. A timeout alone cannot supply this guard. Second, P retains
`ValidBlock=0` despite the mutation; choosing P as the next proposer would
make it propose 0. The dedicated negative control verifies this, and the
witness instead uses C. Third, proposal transport and proposer signature
are distinct, so only the intended E/R channel is changed. Fourth, repair
enters Commit using actual precommits and can require real block data; it
does not directly set a lock or erase network messages.

The model remains finite and intentionally restricted. It assumes two valid
complete blocks, equal voting power, the fixed proposer prefix, and the
explicitly shown delivery/timeout opportunities. It does not implement
ABCI, block validation internals, vote extensions, weighted quorums,
validator-set changes, full gossip selection, future-round catch-up,
disk/WAL recovery, wall-clock bounds, or later heights. An attempted
future-round quorum transition, late old-round proposal-POL completion,
or precommit-majority auto-entry before the local precommit step raises an
error rather than silently pretending to implement that path. Detailed
vote bookkeeping while awaiting a commit block is also outside the subset.
None of these omitted branches occurs in the twelve reported executions.

The twelve cases are concrete witnesses and controls, not exhaustive execution
exploration and not an estimate of production bug prevalence. The old
Python/Go agreement checks remain checks of their original models; they do
not constitute an independent Go implementation of this new trace. The
new audit checks authenticate all records, verify prior emission and
once-only delivery, check actual distinct-signer certificates and their
prior local receipt, inspect vote/lock guards at signing, verify timeout
evidence, and justify every decision by a local precommit certificate.
