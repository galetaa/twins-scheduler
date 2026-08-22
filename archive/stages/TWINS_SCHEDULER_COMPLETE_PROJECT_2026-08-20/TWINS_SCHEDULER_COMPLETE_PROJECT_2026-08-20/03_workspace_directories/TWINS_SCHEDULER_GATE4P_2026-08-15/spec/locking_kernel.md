# Gate 4′ locking-kernel specification

## Status and purpose

This specification defines the smallest natural, certificate-driven locking
protocol used to test whether scheduler-grammar differences survive beyond the
diagnostic machines of Gate 0′–3′. It is a bounded research kernel inspired by
leader-based BFT locking protocols. It is **not** claimed to be the HotStuff
protocol, an implementation of relab/hotstuff, or a production vulnerability.

## Participants and identities

Logical identities are

```text
B, H1, H2, H3
```

with `n = 4`, `f = 1`, and quorum size `q = 3`. `B` is represented by physical
processes `T0` and `T1`, which share one logical Byzantine identity. `H1`, `H2`,
and `H3` execute the selected protocol variant. A quorum always contains the
leader's one logical vote plus enough honest signer identities. `T0` and `T1`
never count as two signers.

## Values, views, and persistent state

The value domain is `{0, 1}`. The bounded experiments use two conflicting views:

```text
view 1: leader T0 proposes 0
view 2: leader T1 proposes 1
```

Each honest replica stores

```text
(locked_value, locked_view, decision)
```

where `decision` is irrevocable. The safety observation is

```text
O(s) = (decision(H1), decision(H2), decision(H3)).
```

Agreement is violated exactly when at least two non-empty components of `O(s)`
contain different values.

## View stages

Every view has five barriers. Messages inside one barrier commute after receipt
multisets are canonicalized; quorum formation occurs only at the barrier.

1. `PROPOSAL`: the active twin sends a value and optional justification.
2. `PREVOTE`: accepting honest replicas send one vote to the leader.
3. `PRECOMMIT_QC` or `TIMEOUT_QC`: the leader disseminates evidence.
4. `PRECOMMIT`: ready honest replicas send one precommit to the leader.
5. `COMMIT_QC` or `FORGED_COMMIT_QC`: the leader disseminates terminal evidence.

A correct proposal is accepted when it does not conflict with an irrevocable
decision and either agrees with the local lock or carries a strictly newer,
value-matching justification. A correct replica locks before sending a
precommit after a valid `PRECOMMIT_QC`. A valid `COMMIT_QC` requires three
logical signers and causes an undecided receiver to decide.

## Scheduler grammars

### `G_P_PARTITION`

One symmetric connected set around the active leader is selected per view. All
controlled message types use the same reachability relation.

### `G_D_DIRECTED_VIEW`

One outbound mask and one inbound mask around the active leader are selected per
view. The masks are reused for every message type in that direction.

### `G_D1_DIRECTED_DELAY1`

`G_D_DIRECTED_VIEW` plus a bounded temporal operation: selected admitted
`COMMIT_QC` messages may be held and delivered after all normal stages of the
next view. A certificate held in the final bounded view remains pending. This is
a diagnostic temporal extension, not a claim that the current relab/hotstuff
scenario language exposes the same control directly.

### `G_T_TYPE_SPECIFIC`

A separate endpoint mask is selected for each message kind. This permits, for
example, admitting `PRECOMMIT_QC` to a replica while suppressing `COMMIT_QC` on
the same physical edge.

### `G_M_PER_MESSAGE`

Every emitted message instance is independently delivered or omitted. Within a
stage, the canonical order is sufficient because the declared transition
operations commute.

### `G_R_PER_MESSAGE_REPLAY1`

`G_M_PER_MESSAGE` plus multiplicity `0`, `1`, or `2` for every `PREVOTE` and
`PRECOMMIT` instance. Other message types are delivered at most once.

The standard embedding checked by the artifact is

```text
G_P ⊆ G_D ⊆ G_T ⊆ G_M ⊆ G_R.
```

`G_D ⊆ G_D1` is checked separately. `G_D1` and `G_T` are intentionally not
ordered: one adds bounded time, the other phase/type discrimination.

## Protocol variants

- `BASELINE`: all guards and identity de-duplication enabled.
- `MISSING_LOCK_UPDATE`: a valid precommit certificate enables a precommit but
  does not update the lock.
- `WRONG_QC_GUARD`: the proposal guard ignores the certified value and uses a
  non-strict view comparison.
- `TIMEOUT_AS_PRECOMMIT`: a timeout certificate enables a value-specific
  precommit without a lock.
- `DUPLICATE_VOTE_COUNTING`: receipt instances, not logical signers, determine
  quorum size.
- `RECEIVER_VALIDATION_OMISSION`: `H3` accepts a forged commit certificate. This
  is a positive control that should be visible even under partitions.

## Exact search and reduction rules

The explorer enumerates all policies in the finite grammar and all reachable
protocol states, deduplicating equal symbolic states. It retains the
lexicographically deterministic witness with the smallest number of delivered
messages. Receipt tuples are sorted, preserving multiplicity, so permutations
inside a stage are exactly state-equivalent. `tests/test_locking_gate4p.py`
checks the stage commutativity assumption on a complete baseline view.

Every serialized unsafe witness is checked twice:

1. by replay through the executable kernel;
2. by `locking/oracle.py`, which parses the trace into an independently
   implemented mutable state machine and does not call the explorer's transition
   functions.

## Scope boundaries

The result is bounded to two views, one Byzantine logical identity, three honest
replicas, binary values, deterministic processing, star-shaped leader traffic,
and agreement observations. It excludes liveness, probabilistic leader
selection, cryptographic forgery, arbitrary payload mutation, unbounded replay,
real-time deadlines, and a proof for all HotStuff/Tendermint protocols.
