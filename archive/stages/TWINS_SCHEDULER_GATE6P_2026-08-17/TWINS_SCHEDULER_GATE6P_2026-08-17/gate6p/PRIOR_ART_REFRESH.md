# Gate 6′ focused prior-art refresh

**Search date:** 17 August 2026  
**Question:** Is there already a theorem or systems result characterizing when
phase/type erasure from a per-phase message scheduler to one type-uniform
directed endpoint graph preserves finite BFT safety observations?

## Search dimensions

The refresh covered:

- communication closure and canonical schedules for consensus testing;
- directed dynamic networks and message-adversary graph languages;
- Twins and partition-based BFT testing;
- randomized/message-mutation BFT testing;
- message-filter DSLs with drop, delay, order, and replay;
- benchmark frameworks for BFT testing;
- combinations of “phase-specific”, “message type”, “scheduler”, “closure”,
  “safety witness”, and “quorum pivot”.

## Closest located work

1. **Testing Consensus Implementations Using Communication Closure** reduces
   relevant asynchronous executions to lossy synchronous executions under its
   hypothesis. It does not establish that erasing phase labels to one endpoint
   graph preserves agreement-violation observations, nor does it use the
   repair/pivot separation mechanism.
2. **Randomized Testing of Byzantine Fault Tolerant Algorithms (ByzzFuzz)**
   injects structured message mutations and explores BFT bugs. It demonstrates
   the utility of richer fault actions but does not characterize a minimal
   property-preserving scheduler grammar.
3. **Twins** controls prescribed message-delivery scenarios using cloned
   identities. Its practical scenario language motivates the comparison, but
   the Gate 6′ claim is not a new Twins implementation or a claim about clone
   count.
4. **Netrix** supports filters capable of dropping, delaying, reordering, and
   replaying messages. This eliminates novelty for “adding richer filters” but
   does not supply the closure theorem or phase-coupled separation.
5. **ByzzBench** provides a controlled benchmark environment for BFT testing
   algorithms. It evaluates techniques rather than proving equivalence of their
   scheduler languages under safety projection.
6. **Message-adversary/dynamic-network theory** characterizes consensus
   solvability under sequences of directed communication graphs. It supplies
   relevant formal language but asks a different question from preservation of
   a concrete safety witness when message phases are erased.

## Result of the refresh

No source located in this refresh simultaneously provides:

1. a type-erasure closure from phase-specific delivery to one type-uniform
   directed endpoint graph;
2. preservation or separation stated over finite agreement observations;
3. a repair message that destroys an unsafe witness by disabling a unique
   honest quorum pivot;
4. an explicit replay-erasure boundary under stable logical contribution keys;
5. executable validation across more than one locking model.

This is not proof of absence. The search may miss dissertations, unpublished
engineering discussions, non-English work, secondary lemmas, or publications
indexed under refinement/conformance terminology.

## Restrained novelty delta

> Closest work provides communication-closure reductions, directed
> message-adversary models, clone/partition testing, richer message filters,
> mutation-based BFT testing, and benchmark infrastructure. In the sources
> searched through 17 August 2026, no work was found that characterizes the
> safety-observation effect of phase/type erasure through the quorum-pivot
> repair mechanism studied here. The proposed contribution is restricted to
> the stated closure criterion, explicit separation family, premise boundary,
> and replay-idempotence result.
