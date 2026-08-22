# T1 — Replay erasure under stable-key idempotence

## Statement

Let a finite protocol execution contain deliveries of authenticated messages.
Each exact signed protocol action has a stable replay key. Assume:

1. after a replay key has been processed once, delivering the same key again is
   a stutter on protocol-relevant state;
2. such a duplicate emits no protocol-relevant message or callback;
3. suffix execution is congruent under equality of protocol-relevant state and
   pending relevant outputs;
4. the safety observation depends only on protocol-relevant state;
5. removing non-first replay deliveries yields an admissible execution of the
   non-replay grammar.

Then deleting every non-first occurrence of a replay key preserves the terminal
protocol-relevant state and the selected safety observation. Hence, for finite
state-based safety observations,

\[
O(L_{G_R}(P)) = O(L_{G_M}(P)).
\]

The reverse inclusion follows from `G_M ⊆ G_R`.

## Checked induction

Use the measure

\[
d(\tau)=\text{number of non-first replay-key occurrences in }\tau.
\]

### Base case

If `d(τ)=0`, replay erasure is the identity, so the terminal state and
observation are unchanged.

### Step

Assume `d(τ)>0`. Choose one non-first occurrence of replay key `κ`.
Immediately before that occurrence, `κ` has already been processed. By
stable-key idempotence, processing it changes no relevant state and emits no
relevant output. Removing it therefore leaves the same relevant configuration
for the suffix. Suffix congruence gives the same later relevant run and the same
terminal observation. The number of non-first occurrences decreases by one.
Apply the induction hypothesis.

## Boundary

T1 does not erase:

- two equivocations with different replay keys;
- duplicate processing that resets timers or invokes protocol-visible callbacks;
- handlers that count message instances rather than stable validator
  contributions;
- duplicate deliveries that alter resource or failure behavior included in the
  observation.

The constructive failure boundary is T5: if a quorum accumulator counts
instances, the trace `B,H1,H1` can cross a quorum of three with only two logical
contributors.

## Machine-readable assets

- `t1_rules.json`;
- `t1_replay_erasure_certificate.json`;
- `results/gate6p/t1_replay_erasure_proof_check.json`.
