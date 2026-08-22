# Replay-erasure theorem for logical-key-idempotent vote processing

## Setting

Let a finite delivery trace be `τ = m1 … mk`. Every signed protocol action has a
stable logical key

\[
\kappa(m)=(height,round,phase,value,validator).
\]

Two byte-identical retransmissions of the same vote have the same key. A genuine
equivocation for another value has a different key and is not erased.

A handler is **logical-key idempotent** when, after key `κ(m)` has been processed,
processing another message with the same key:

1. leaves all protocol-relevant state unchanged;
2. emits no protocol-relevant message;
3. adds no voting power or signer contribution;
4. leaves every state-based safety observation unchanged.

Let `dedup(τ)` retain the first occurrence of every logical key.

## Theorem T1

For every initial state `s0` and every finite trace `τ`, if all handlers are
logical-key idempotent, then

\[
\delta^*(s_0,\tau)=\delta^*(s_0,\operatorname{dedup}(\tau))
\]

on protocol-relevant state. Consequently, quorum status and every state-based
safety observation are identical before and after replay erasure.

## Proof

Induct on the length of `τ`.

- The empty trace is immediate.
- Write `τ = ρ·m` and assume the claim for `ρ`.
  - If `κ(m)` does not occur in `ρ`, then `m` is retained by `dedup`; both runs
    process the same logical action after states equal by induction.
  - If `κ(m)` already occurs in `ρ`, then `m` is removed by `dedup`. By
    logical-key idempotence, processing it in the original run is a stuttering
    step on protocol-relevant state. Therefore both final states remain equal.

The quorum and observation claims follow because they are functions of the
protocol-relevant state. ∎

## Strict boundary

If a handler counts message instances instead of stable logical keys, replay
erasure need not preserve quorum. With quorum three, the trace

```text
H1, H1, H1
```

has one logical signer but three message instances. Unique-key processing does
not reach quorum; instance counting does. This is a constructive strict
separation between per-message delivery and delivery with replay for the
controlled non-idempotent mutation.

## Executable evidence

- `results/gate5p/replay_idempotence_checks.json` exhaustively checks all 364
  sequences over three validators up to length five.
- `results/gate5p/comet_vote_conformance.json` compares the Python model with a
  dependency-free Go fixture on 728 cases: 364 unique-key and 364
  instance-counting cases.
- `results/gate5p/implementation_correspondence.json` maps the premise to pinned
  CometBFT v0.40.0 source, where exact duplicate votes return without adding a
  contribution and voting power is associated with the validator slot.

## Scope

The theorem concerns exact replay of the same logical signed action. It does not
erase equivocations, altered payloads, signatures under different domains, or
protocol messages whose repeated processing intentionally changes state.
