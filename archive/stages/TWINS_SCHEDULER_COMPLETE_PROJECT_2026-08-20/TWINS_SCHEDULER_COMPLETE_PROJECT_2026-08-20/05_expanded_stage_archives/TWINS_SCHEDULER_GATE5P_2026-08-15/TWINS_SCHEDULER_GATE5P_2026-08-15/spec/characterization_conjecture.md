# Candidate characterization for Gate 5′

## Problem after Gate 4′

The empirical question is no longer whether richer schedulers create more raw
traces. Gate 4′ establishes that natural locking mistakes can be hidden or
revealed by specific scheduler capabilities while the correct baseline remains
safe. Gate 5′ must replace this finite observation with a protocol-class result.

## Type-uniform closure

For a per-type schedule `σ`, define `C_type(σ)` by erasing message kinds and
allowing every kind on an endpoint/direction used by any kind in the same view.
A safety witness is **type-closure fragile** when it is unsafe under `σ` but safe
under `C_type(σ)`.

The three phase-sensitive Gate 4′ witnesses are type-closure fragile. The extra
messages admitted by `C_type` establish a lock, deliver terminal evidence, or
prevent the conflicting branch from obtaining the required quorum.

## Temporal erasure

For a schedule that defers terminal evidence by one view, define `C_time(σ)` by
delivering that evidence immediately. The lock-omission and QC-guard witnesses
are time-closure fragile: immediate terminal evidence decides a would-be voter
before the conflicting view. The timeout-classification mutant is not exposed
by terminal delay alone because its required distinction is between two inbound
quorum-forming phases.

## Replay erasure

For a replay schedule `σ`, define `C_dup(σ)` by retaining one instance of each
signed vote. The duplicate-counting witness disappears under `C_dup` because no
quorum certificate is then causally producible.

## Candidate claims

### C5.1 — closure-preservation sufficiency

For a protocol implementation whose transition relation is safety-monotone under
all additional messages introduced by a closure `C`, every unsafe execution of
the richer scheduler has an unsafe execution in the weaker grammar.

This statement needs a non-circular definition of safety-monotonicity and may be
false for general locking protocols.

### C5.2 — phase-coupled separation

If an implementation defect permits a replica to perform a safety-relevant
outbound action after evidence `e` without retaining the state constraint that
`e` should establish, and a later repair/terminal message on the same edge would
remove that replica from a conflicting quorum, then a type-uniform view graph can
be strictly weaker than a phase-specific scheduler.

### C5.3 — bounded terminal-delay simulation

For defects where only terminal evidence repairs the unsafe branch, one-view
late delivery can simulate the necessary type-specific omission. This fails when
the distinguishing omission is needed between two inbound quorum-forming phases.

### C5.4 — replay/idempotence boundary

Bounded replay adds no safety observations when vote processing is idempotent by
logical signer identity. It can strictly enlarge the unsafe language when a
quorum counter is non-idempotent over message instances.

## Required proof obligations

1. Define the protocol class without naming the five mutants.
2. Define closure-induced additional messages and safety-monotonicity on traces.
3. Prove a sufficient theorem or construct a natural counterexample to C5.1.
4. State and prove a separation lemma for C5.2 on a parametric two-view kernel.
5. Prove the idempotence result for C5.4.
6. Instantiate the definitions on a second locking protocol model.
7. Show that at least one implementation-level mutation maps to the abstract
   preconditions without changing the scheduler semantics.
8. Re-run novelty search in communication-adversary, conformance, refinement,
   fault-injection, and distributed-testing literature.

## Decision rule

Gate 5′ is a GO only if at least one claim becomes a theorem or a reusable
separation condition independent of the current mutant names. Merely finding
more examples, adding a DSL, or increasing state-space coverage is a NO-GO for
the scientific theme.
