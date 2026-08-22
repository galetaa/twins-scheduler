# Bounded rule-level instantiation to CometBFT/Tendermint locking

## Status and source pin

This document instantiates the abstract quorum-pivot mechanism in a bounded
transition system derived from the published CometBFT consensus rules.  It is
**not** a claim of a bug in CometBFT and **not** a full refinement proof from the
production Go implementation.  The protocol source is pinned to:

- repository: `cometbft/cometbft`;
- release tag: `v0.39.3`;
- release commit prefix reported by GitHub: `49b8283`;
- specification: `spec/consensus/consensus.md` at tag `v0.39.3`;
- evidence cut-off: 21 August 2026.

The official specification defines rounds with `Propose`, `Prevote`,
`Precommit`, and `Commit`; a +2/3 set of prevotes for one block is a PoLC; a
validator that has a PoLC in the current round locks (or relocks) and
precommits that block; and +2/3 precommits for a block lead to `Commit`.

## Abstract-to-protocol correspondence

| Abstract object | Bounded Tendermint-style interpretation |
|---|---|
| height/view | one fixed height `H=1`; scheduler coupling is within round `r0=0` |
| pivot `p` | one correct validator whose contribution is required by both conflicting `2f+1` precommit sets |
| Byzantine base `B` | `f` Byzantine validators contributing to both branches |
| honest base `A` | `f` correct validators contributing only to value `0` at round `0` |
| honest base `C` | `f` correct validators contributing only to value `1` at round `1` |
| enabling envelope `E` | the last `PREVOTE(0,H,0)` from fixed sender `b0` to `p`, completing `p`'s local +2/3 PoLC for value `0` |
| mutation | `MISSING_LOCK_UPDATE`: after the PoLC, `p` emits `PRECOMMIT(0,H,0)` but omits the persistent update `lockedValue:=0, lockedRound:=0` |
| first certificate opportunity `C0` | a correct observer obtains the `2f+1` precommits of `B union A union {p}` and decides value `0` |
| repair envelope `R` | the last `PRECOMMIT(0,H,0)` from the same `b0` to `p`, completing `p`'s local +2/3 precommit set and causing `p` to enter `Commit(H)`/advance height |
| second certificate opportunity `C1` | at later round `1` of the same height, a correct observer can obtain the `2f+1` precommits of `B union C union {p}` for value `1` only if `p` is still available |
| enabled | `p` saw the round-0 PoLC and emitted a round-0 precommit |
| disabled | before `C1`, `p` either retained lock `0` or committed height `H`; in either case it cannot supply the conflicting round-1 contribution in the bounded schema |
| shared edge | `E` and `R` have the same sender `b0`, receiver `p`, height `H`, and round `0`, but distinct phases `PREVOTE` and `PRECOMMIT` |
| phase-specific grammar `G_T` | admits `E` and rejects `R` |
| type-uniform directed grammar `G_D` | one Boolean admission bit for `(H,0,b0,p)`, therefore it rejects both envelopes or admits both |

## Fixed bounded domain

The bounded domain `B_f` fixes all of the following:

1. `n=3f+1`, `q=2f+1`, `f>=1`;
2. one height and two rounds;
3. values `0` and `1`;
4. the phase order `E < C0 < R < C1`;
5. every message production, every other edge, and every other delivery;
6. one controlled edge `(H,0,b0,p)`;
7. once-only delivery of already emitted controlled envelopes;
8. no late delivery of `R` after `C1`;
9. correct decisions are emitted exactly when the corresponding local precommit set reaches `q`.

Thus the directed grammar has exactly two executions in this domain: edge off
and edge on.  The phase-specific witness is the additional policy that admits
`E` and rejects `R`.

## Refinement statement

Let `P_f^lock` be the bounded Tendermint-style transition system above and
`P_f^miss` the same system with only the persistent lock assignment removed.
The executable model establishes for `f=1..64`, independently in Python and
Go:

- `P_f^lock` is safe under all three canonical policies;
- `P_f^miss` has an agreement violation under `G_T(E=1,R=0)`;
- `P_f^miss` is safe under both `G_D` policies;
- the Python and Go terminal observations coincide for all 384 cases.

The algebraic proof is parameterized by every `f>=1`; the finite executable
range is a cross-check, not the basis of the universal claim.

## Why this is a natural instantiation, and its limit

The mapping uses the protocol's actual semantic roles—PoLC, lock update,
precommit quorum, and commit—rather than renaming arbitrary terminal events.
It also makes the scheduler coupling concrete through two distinct vote types
on the same sender/receiver/height/round edge.

The mapping remains a **bounded rule-level refinement**.  It does not model
all proposal validation, gossip, timeouts, evidence, weighted voting power,
vote extensions, WAL/recovery, or the production event loop.  No claim is made
that the mutation exists in release `v0.39.3`.
