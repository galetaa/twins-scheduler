# Gate 5′ Tendermint-style locking kernel

## Purpose

This is the independent natural protocol instantiation required by Gate 5′. It
is not a full CometBFT model. It preserves the protocol mechanisms relevant to
the claims: proposal valid-round evidence, prevotes, a +2/3 prevote certificate
(POLKA/PoLC), persistent locking, precommits, terminal commit evidence, and
logical-signer vote counting.

## Participants and thresholds

- validators: one Byzantine logical identity represented by two controlled
  branches and three correct replicas `H1,H2,H3`;
- `n=4`, `f=1`, quorum `q=3`;
- values: `0` and `1`;
- two bounded views/rounds.

## Local state

Each correct replica contains at least:

- current round;
- proposed value and proposal valid round;
- `LockedValue` and `LockedRound`;
- `ValidValue` and `ValidRound`;
- processed logical vote keys;
- prevote/precommit support;
- irreversible decision.

## Stage order

```text
PROPOSAL -> PREVOTE -> POLKA -> PRECOMMIT -> COMMIT
```

Handlers are deterministic. The scheduler controls only delivery, bounded delay,
and bounded replay according to the selected grammar.

## Correct baseline

- a valid POLKA establishes or updates the persistent lock before precommit;
- a proposal justified by a prior valid round must be consistent with the
  receiver-side guard;
- exact repeated logical votes add no signer or voting power;
- terminal evidence can decide but does not erase a prior conflicting decision.

## Controlled mutations

1. `TM_MISSING_LOCK_UPDATE`: process enabling POLKA but omit the persistent lock
   update.
2. `TM_WRONG_VALID_ROUND_GUARD`: accept a mismatched value/valid-round
   justification.
3. `TM_DUPLICATE_VOTE_COUNTING`: count message instances rather than stable
   logical signer keys.
4. `TM_RECEIVER_VALIDATION_OMISSION`: positive control that omits receiver-side
   certificate validation and is detectable even under partitions.

These are semantic perturbations of proof obligations, not claims about defects
in CometBFT.

## Checked scheduler grammars

- `G_P_PARTITION`;
- `G_D_DIRECTED_VIEW`;
- `G_D1_DIRECTED_DELAY1`;
- `G_T_TYPE_SPECIFIC`;
- `G_M_PER_MESSAGE`;
- `G_R_PER_MESSAGE_REPLAY1`.

## Safety property

An observation is unsafe exactly when two correct replicas have distinct,
non-null decisions.

## Exact-search results

| Mutation | Partition | Directed | Delay-1 | Phase-specific | Per-message | Replay-1 |
|---|---:|---:|---:|---:|---:|---:|
| Lock update omitted | 0 | 0 | 12 | 9 | 9 | 9 |
| Valid-round guard wrong | 0 | 0 | 12 | 9 | 9 | 9 |
| Duplicate instances counted | 0 | 0 | 0 | 0 | 0 | 12 |
| Validation omission control | 1 | 1 | 3 | 3 | 3 | 3 |

Cells are counts of distinct agreement-violating decision observations. The
correct baseline has zero unsafe observations for every case and grammar.

## Validation

Every serialized unsafe witness is replayed by the main kernel and by a
separately coded mutable-state oracle. Selected witnesses are then closed by:

- type erasure;
- immediate terminal delivery;
- logical-vote deduplication.

Each closure removes the corresponding violation, confirming the proposed
mechanism rather than only the language-size difference.

## Source correspondence

Pinned CometBFT v0.40.0 sources are used only to verify that the model's natural
premises exist in an open implementation/specification:

- the protocol uses propose/prevote/precommit rounds and PoLC/polka locking;
- lock assignment precedes the local precommit action in the checked source
  path;
- proposals carry a valid round;
- exact duplicate votes return without adding another contribution;
- voting power is accumulated by validator slot.

The artifact does not claim complete implementation equivalence.
