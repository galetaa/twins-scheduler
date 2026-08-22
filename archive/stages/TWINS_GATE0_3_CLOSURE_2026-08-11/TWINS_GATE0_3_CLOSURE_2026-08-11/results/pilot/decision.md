# Gate 3 Decision — BP-TWINS-FC-01-CLOSURE

## Decision

**NO-GO for the finite-clone-number research claim; PIVOT only to concrete harness conformance.**

## Completed exact bounds

- Correct replicas: 3; one faulty protocol identity.
- Values: binary and ternary diagnostic instances.
- All branch subsets enumerated.
- All reachable event states exhaustively explored for every branch subset.
- Terminal quotient independently checked against event-level BFS.
- Persistent static clone caps: [0, 1, 2, 3].
- Reusable snapshot active-slot caps: [0, 1].

## Exact results

| Instance | Model | Language | Unsafe | Missing unsafe vs AE |
|---|---:|---:|---:|---:|
| binary | AE | 125 | 24 | 0 |
| binary | static k=1 | 53 | 0 | 24 |
| binary | static k=2 | 125 | 24 | 0 |
| binary | snapshot active k=1 | 125 | 24 | 0 |
| ternary | AE | 343 | 96 | 0 |
| ternary | static k=2 | 295 | 72 | 24 |
| ternary | static k=3 | 343 | 96 | 0 |

## Decisive findings

1. `AB = AE` in this validator-only model.
2. Every finite-clone language is included in `AE`.
3. For persistent genesis clones, exact `k_min` equals the number of distinct incompatible correct-code branch histories retained by the observation. This is the minimum chain-cover width by construction.
4. For the binary protocol, static `k=2` covers every unsafe AE observation; `k=1` covers none.
5. Ternary exact observations create a strict `k=2 < k=3` hierarchy only when the observation insists on retaining a third branch. Every unsafe observation still contains a two-branch agreement-violation core.
6. Under `SnapshotDynamic(k)` interpreted as an active-slot cap with restart/replay and unbounded network delay, `k=1` equals AE for every finite observation: execute branches sequentially and delay delivery.

## Gate rule applied

Gate 3 specifies NO-GO when the result is an ordinary chain cover or trivial two-clone behavior. Both occurred. The remaining possible contribution is not a clone-number theorem but a new question about whether a concrete round-partition implementation realizes the ideal per-message scheduler semantics.
