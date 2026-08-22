# Gate 5′ publication kill test

## Decision

**PASS WITH A NARROW CLAIM.** Gate 5′ produces a theorem-and-counterexample
package rather than a new testing framework.

Recommended paper topic:

> **Safety-Observation Closure Boundaries of Scheduler Grammars for
> Certificate-Driven Locking BFT Protocols**

Russian working title:

> **Границы сохранения safety-наблюдений при замыкании грамматик планировщика в
> certificate-driven locking BFT-протоколах**

## Contribution statement

1. Define type erasure, bounded terminal-time erasure, and replay erasure over
   phase-labelled BFT traces; prove replay erasure under stable-key idempotence
   and a relational sufficient condition for closure-preserved unsafety.
2. Construct a parametric quorum-pivot family for every `f≥1` with
   `n=3f+1,q=2f+1` that strictly separates one type-uniform directed graph per
   view from phase-specific directed delivery by agreement observations.
3. Instantiate the boundary in two bounded locking kernels, map its lock,
   valid-round, and duplicate-vote premises to pinned CometBFT v0.40.0 source,
   and release exact searches, independently replayed witnesses, closure
   counterfactuals, and Go fixtures.

## Minimum publishable unit

The minimum paper requires all of the following:

- T1 replay-erasure proof and strict non-idempotent boundary;
- T2 relational closure theorem and a failed-premise counterexample;
- T3 algebraic quorum-pivot proof, not only `f=1…8` enumeration;
- the Gate 4′ and Tendermint-style kernels;
- minimized witnesses and closure counterfactuals;
- pinned source mapping and reproducible artifact;
- a limitations section that separates model correspondence from production
  conformance.

## Publication audience

The contribution is best framed for formal methods, distributed algorithms, or
software testing of distributed systems. A blockchain-specific venue is
plausible only if the paper foregrounds consensus semantics rather than the
Twins tool name. No venue is asserted as guaranteed suitable.

## Strongest reviewer objections

### “The closure theorem is tautological.”

Required response: T2 must be presented as a local transition theorem, not the
main novelty. The nontrivial result is the explicit failure mechanism and T3’s
quorum arithmetic. Include the executable example where added repair evidence
violates the monotonicity premise and turns an unsafe trace safe.

### “The second model is merely a renaming of the first.”

Required response: provide an assumption/transition mapping showing distinct
proposal/prevote/POLKA/precommit state, valid-round evidence, and persistent
lock semantics. State honestly that both are bounded reference models. Gate 6′
should add one fuller event-loop replay or a third independently authored model.

### “These are toy mutants.”

Required response: derive each mutation from a named safety obligation—lock
persistence, value/round justification consistency, and unique signer
accounting—and map the correct obligation to official source. Do not claim the
mutations exist in production.

### “Netrix and ByzzFuzz already have richer message controls.”

Required response: concede this explicitly. Tool capability is prior art. The
claim concerns equality or strict separation of safety-observation languages,
not an API.

### “Communication closure already gives a normal form.”

Required response: compare assumptions line by line. Communication closure
normalizes timing/loss for suitable protocols; Gate 5′ studies the additional
erasure from per-phase delivery to one endpoint graph and shows how the added
messages can repair a defective trace.

### “Bounded checking cannot prove a protocol-class theorem.”

Required response: the universal `f` step comes from the algebraic construction;
the bounded checks are regression evidence and natural instantiations. Gate 6′
must mechanize or independently verify the proof.

## Claims forbidden without additional evidence

- CometBFT contains any studied defect;
- partitions are incomplete for every BFT protocol;
- phase-specific scheduling is universally minimal;
- the number of unsafe observations estimates bug probability;
- the result covers liveness or unbounded partial-synchrony executions;
- the controlled witnesses are exploitable;
- the novelty claim is absolute.

## Gate 6′ entry condition

Proceed only to proof hardening, model-to-implementation refinement, and
external-validity checks. Do not expand into a generic fuzzing DSL, a large
mutant benchmark, or experiments on a public network.
