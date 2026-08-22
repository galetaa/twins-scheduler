# Gate 5′ formal result ledger

## T1. Replay-erasure theorem

### Statement

Let `P` be deterministic. Assume duplicate delivery is stable-key idempotent,
quorum contribution is keyed by validator slot rather than message instance,
and `O` ignores non-protocol telemetry. Every finite `G_R` execution has a
`G_M` execution obtained by deleting repeated replay keys with the same
protocol-relevant terminal state and safety observation:

\[
O(L_{G_R}(P))=O(L_{G_M}(P)).
\]

The reverse inclusion follows from `G_M⊆G_R`.

### Proof

Choose one non-first occurrence of a replay key. By stable-key idempotence, its
transition is a stutter on protocol-relevant state and emits no new relevant
message. Deleting it leaves every later transition enabled with the same result.
Induct on the finite number of duplicate occurrences.

### Boundary

The theorem does not erase equivocations or any message with a distinct replay
key. It fails if duplicate handling changes callbacks, timers, emitted messages,
quorum weight, or any state used by later protocol transitions.

### Executable evidence

- `results/gate5p/replay_idempotence_checks.json`: all 364 sequences through
  length five satisfy erasure in the idempotent model.
- The minimal one-replay strict counterexample for instance counting is
  `B,H1,H1`: three instances but two contribution identities.
- `results/gate5p/comet_vote_conformance.json`: 728 Go/Python transition cases.
- `results/gate5p/implementation_correspondence.json`: controlled Go fixture and
  pinned-source checks.

## T2. Relational closure-lifting theorem

### Statement

Let `τ` be an unsafe finite trace. Insert closure-added messages while retaining
the order of original transitions. If the insertion is R-monotone as defined in
`protocol_class.md`, then the closed trace is also unsafe.

If, additionally, related states have the same observation, closure preserves
the complete terminal observation rather than only unsafety.

### Proof

Induct over the sequence obtained by interleaving original and closure-added
messages. An added message moves upward in `R`. Forward simulation preserves the
relation across each original transition. Hence the final original state is
related to the final closed state. Upward closure of `Unsafe` gives the first
claim; observation preservation gives the corollary.

### Mechanistic boundary

Locking protocols can violate the premise. A repair or terminal message may
remove the unique pivot’s ability to support a later conflicting quorum. It is
therefore not R-increasing for a relation that preserves future safety-relevant
actions. In the supplied finite counterexample, the original trace is unsafe and
its closure is safe.

### Executable evidence

`results/gate5p/closure_theorem_checks.json` verifies the local premises on an
additive system and records the explicit locking-fragility counterexample.

## T3. Parametric quorum-pivot separation

### Statement

For every `f≥1`, there exists a deterministic two-round certificate-driven
protocol instance with `n=3f+1` and `q=2f+1`, satisfying the quorum-pivot
template, such that

\[
UnsafeObs(G_D)=\varnothing,
\qquad
UnsafeObs(G_T)\neq\varnothing.
\]

Consequently, type-uniform directed scheduling and phase-specific directed
scheduling are strictly separated by safety observations on this protocol
family.

### Construction and proof

Use

\[
Q_0=B\cup A\cup\{p\},\qquad Q_1=B\cup C\cup\{p\},
\]

with `|B|=|A|=|C|=f`. Each fixed base support has size `2f`, one below quorum.

Under `G_T`, deliver enabling evidence `e` to `p`, omit the later repair message
`r`, and let the controlled defective transition leave `p` eligible for both
rounds. Both supports reach `2f+1`, yielding conflicting certificates.

Under `G_D`, the shared edge is absent or present for both phases. If absent,
`Q0` has only `2f` supporters. If present, `r` disables `p` before the second
round, so `Q1` has only `2f` supporters. Neither case reaches both quorums.

The proof is algebraic for every positive `f`. The executable family check for
`f=1,…,8` is a regression check, not the basis of the universal arithmetic
step.

### Natural instantiations

The same zero/nonzero separation class occurs in two executable kernels for:

1. omitted persistent lock update;
2. defective value/round justification guard.

This gives four natural instances total. Every selected witness is independently
replayed and becomes safe under type erasure.

### Executable evidence

- `results/gate5p/phase_coupled_family.json`;
- `results/gate5p/phase_coupled_finite_model.json`;
- `results/gate5p/cross_protocol_result_matrix.csv`;
- `results/gate5p/tendermint_witnesses.jsonl`.

## T4. Bounded terminal-delay corollary

When `r` is terminal/repair evidence and deferring it through the conflicting
round changes no other required transition, `G_D1` reproduces the phase-specific
witness: `e` is delivered now and `r` after the second quorum opportunity.
Immediate-delivery closure `C_time` removes the violation.

This is conditional and does not order `G_D1` and `G_T` generally. A defect that
requires discrimination between two non-terminal inbound phases can remain
inexpressible in `G_D1`.

## T5. Non-idempotent replay separation

If a quorum accumulator counts message instances rather than unique validator
contributions, a one-replay trace can cross quorum without crossing it after
replay erasure. In the `n=4,q=3` witness, `B,H1,H1` reaches three instances but
only two validator contributions. Both exact kernels expose agreement violations
only in `G_R` for the controlled mutation.

## Machine-readable status

The authoritative status is in:

- `results/gate5p/gate5p_theorem_ledger.json`;
- `results/gate5p/gate5p_machine_checks.json`;
- `results/gate5p/gate5p_decision.json`.

## What is not proved

The results do not prove:

- that every natural BFT defect requires phase-specific scheduling;
- that partitions are universally incomplete;
- that `G_T` is a universally minimal grammar;
- that CometBFT contains any studied defect;
- that the results extend to liveness or unbounded executions;
- that a bounded exact search establishes production prevalence or probability.
