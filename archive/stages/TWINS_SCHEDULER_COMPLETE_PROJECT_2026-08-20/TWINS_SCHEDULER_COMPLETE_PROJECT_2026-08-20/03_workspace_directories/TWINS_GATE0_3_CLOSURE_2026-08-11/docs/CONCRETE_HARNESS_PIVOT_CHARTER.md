# Conditional pivot charter: concrete Twins harness conformance

**Status:** NEW CANDIDATE — **NOT READY FOR IMPLEMENTATION**.  
**Relationship to the closed candidate:** this is not a repaired finite-clone theorem. It is a distinct conformance/separation problem that must restart at Gate 0.

## Working title

**Russian:** Выразительность сценарного языка Twins с разбиениями по view относительно идеальной помодельной state-equivocation семантики.  
**English:** Expressiveness of View-Partition Twins Scenario Languages Relative to Ideal Per-Message State Equivocation.

## Problem

The rejected model granted an ideal scheduler clone-specific delivery, suppression of all undelivered emissions, arbitrary finite delay, replayable histories and an observation that erased physical scheduling. Under those powers, clone-count results collapse.

A concrete harness can be materially weaker. The inspected `relab/hotstuff` documentation describes a scenario by the number of replicas/twins plus a leader and network partition assignment for each view. A partition controls which messages are sent or dropped. This syntax may fail to encode delivery relations that vary by message type, sender/receiver pair or causal point inside one view.

## Research question

For a fixed deterministic view-based BFT protocol and bounded number of views, which ideal per-message equivocation traces are representable by a concrete sequence of view-level partitions and leader choices? Is there a smallest safety-relevant ideal trace outside the scenario language, or does the concrete language preserve every safety witness for a stated protocol class?

## Candidate formal objects

- `L_ideal(P,b)`: bounded observations under ideal per-message state equivocation.
- `L_part(P,b,p)`: bounded observations under at most `p` view-partition scenarios using the concrete scenario grammar.
- `encode : Scenario -> DeliveryRelation`.
- Soundness obligation: `L_part ⊆ L_ideal`.
- Completeness obligation for property `φ`: every `φ`-violating observation in `L_ideal` has a witness in `L_part`.
- Separation witness: a minimized `τ ∈ L_ideal \ L_part` that is safety-relevant and not merely a different internal schedule.

## Distinguishing test

Implement the same protocol transition system twice:

1. an ideal scheduler chooses delivery independently for each emitted message;
2. a scenario scheduler chooses one partition relation for each view and applies the concrete send/drop rules.

Compare canonical safety-observation languages under identical protocol, bounds and validity rules. A separation result is meaningful only if the unmatched ideal trace cannot be transformed to a partition trace while preserving the safety witness.

## Gate 0 kill questions

1. Is this already a direct instance of communication closure, trace refinement or scenario-language conformance?
2. Does the concrete implementation in fact allow finer per-message control than its generator documentation suggests?
3. Is the scenario language merely a user-interface restriction while the executor can encode arbitrary filters?
4. Does every agreement violation admit a partition-normal-form witness even when arbitrary safe traces do not?
5. Is the result independent of one implementation and useful beyond `relab/hotstuff`?

## Minimum pilot after a new Gate 0 GO

- acquire one concrete harness at an exact commit;
- extract and test its actual executor semantics, not only documentation;
- formalize a two-view or three-view locking protocol;
- enumerate `L_ideal` and `L_part` exactly;
- minimize the first unmatched safety witness;
- test whether the witness disappears under communication-closure normalization;
- classify outcome as completeness theorem, safety-only normal form, separation, or no difference.

## Go / no-go

**GO:** a safety-relevant separation or a nontrivial safety-preserving normal-form theorem remains after refinement/communication-closure prior-art review.

**NO-GO:** the executor already supports arbitrary per-message filters, the result is a direct standard refinement check with no new consequence, or all differences are observationally irrelevant.

## Immediate prohibition

Do not integrate a production client or build a large scenario generator before this new Gate 0 establishes a defensible claim.
