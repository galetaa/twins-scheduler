# Gate 5′ prior-art delta

**Search cutoff:** 15 August 2026  
**Claim type:** bounded formal characterization, not an assertion of absolute
novelty.

## 1. Search question

The refresh searched for work that simultaneously:

1. models one directed communication graph per view or round;
2. compares it with one graph per message phase/type;
3. projects both execution languages onto finite agreement observations;
4. gives a property-preserving closure condition or a structural safety
   separation;
5. distinguishes replay power by idempotent logical-vote processing.

Search terms included `communication closure`, `message adversary`, `Heard-Of`,
`typed communication graph`, `phase-specific omission`, `consensus testing`,
`message filter`, `replay`, `duplicate vote`, `scheduler expressiveness`,
`trace-language inclusion`, `refinement`, and `conformance`.

## 2. Closest work map

| Source | Type | What it establishes or implements | Threat to Gate 5′ | Residual claim after comparison |
|---|---|---|---|---|
| Drăgoi et al., *Testing Consensus Implementations Using Communication Closure*, PACMPL/OOPSLA 2020, DOI 10.1145/3428278 | Peer-reviewed formal testing paper | Reduces selected asynchronous consensus executions to communication-closed/canonical executions under protocol conditions | Critical threat to any broad “normal form for schedules” claim | Gate 5′ studies a different closure: erasing phase labels to one endpoint graph and whether added messages can repair a safety witness |
| Drăgoi et al., *A Domain Specific Language for Testing Consensus Implementations* (Netrix), arXiv:2303.05893 | Research paper and tool | Message filters and monitors can drop, delay, reorder, replay, and modify protocol messages | Destroys novelty of a richer scheduler API | Capability is prior art; the residual contribution is equality/separation of safety-observation languages |
| Winter et al., *Randomized Testing of Byzantine Fault Tolerant Algorithms*, PACMPL/OOPSLA 2023, DOI 10.1145/3586053 | Peer-reviewed testing paper and artifact | Randomized message/fault exploration for BFT implementations | Destroys a “first richer Byzantine tester” claim | Gate 5′ does not claim a testing algorithm; it analyzes a closure boundary |
| Bano et al., *Twins: BFT Systems Made Robust*, OPODIS 2021, DOI 10.4230/LIPIcs.OPODIS.2021.7 | Peer-reviewed paper and engineering artifact | Clone-based equivocation with scenario-controlled delivery | Establishes the original scenario-testing mechanism | The finite-clone completeness topic was rejected; only scheduler-closure semantics remain |
| Louro Neto and Kulahcioglu Ozkan, *A Benchmark Framework for Byzantine Fault Tolerance Testing Algorithms*, FMBC 2025, DOI 10.4230/OASIcs.FMBC.2025.13 | Peer-reviewed benchmark paper | Common benchmark environment for BFT testing | Destroys novelty of a mutant catalogue or benchmark alone | Gate 5′ treats mutants as witnesses for a formal property, not as the contribution |
| Heard-Of and round-based message-adversary literature | Distributed-computing theory | Represents each round by receive sets or communication graphs | Shows that `G_D` is standard modeling vocabulary | The searched work did not supply the same phase-erasure safety projection or quorum-pivot separation |
| Meng et al., *Greybox Fuzzing of Distributed Systems*, CCS 2023, DOI 10.1145/3576915.3623097 | Peer-reviewed systems-security paper | Uses causal execution summaries to guide fault injection | Destroys novelty of causal feedback or generic scheduler exploration | Gate 5′ has no learning/coverage claim; it asks a semantic inclusion question |
| CometBFT v0.40.0 specification and source | Official engineering specification/code | Defines proposal, prevote, PoLC, persistent lock, precommit, commit, valid round, and duplicate-vote handling | Destroys novelty of the protocol rules and duplicate rejection | Provides an independent natural source mapping for the theorem premises, not a production finding |
| Nagendra, *Automated Testing of Distributed Protocol Implementations*, doctoral thesis, 2025 | Dissertation | Consolidates formal and implementation-level consensus-testing techniques | High risk of hidden nearby terminology or a secondary lemma | No identical phase-erasure closure theorem was located in the inspected public material; expert citation review remains required |

## 3. Novelty kill test

- Directed graphs, receive sets, message loss, phase labels, delay, replay, and
  message filters are all known.
- Persistent locking, valid-round evidence, and duplicate-vote rejection are
  known.
- Mutation testing and benchmark comparison are known.
- The checker implementation is not a scientific contribution by itself.
- A generic statement that “more expressive schedulers find more bugs” is not
  novel and is not retained.

The remaining scientific unit is narrower:

1. a local relational condition under which closure-added messages preserve
   unsafety;
2. an explicit counter-mechanism where added repair/terminal evidence removes
   the unique honest quorum pivot;
3. a parametric `n=3f+1`, `q=2f+1` family separating a type-uniform directed
   graph from a phase-specific graph by agreement observations;
4. a replay-erasure theorem whose exact boundary is stable-key idempotence.

## 4. Restrained novelty statement

Closest work provides schedule reductions, round communication graphs, rich
message-control DSLs, randomized Byzantine testing, and benchmark frameworks.
In the publicly available sources examined through 15 August 2026, no work was
found that simultaneously characterizes when erasing phase labels to one
directed endpoint graph preserves finite agreement observations of
certificate-driven locking protocols, constructs the quorum-pivot separation
when it does not, and isolates replay power through stable-key idempotence.

This is not evidence that no such result exists. The statement is limited by
English terminology, indexed/public sources, and possible results in
refinement, conformance, dissertations, or engineering discussions.

## 5. What may still collapse the claim

Gate 6′ must stop or pivot if expert/forward-citation review finds:

- a theorem equivalent to the quorum-pivot separation;
- a typed Heard-Of or message-adversary result that directly subsumes phase
  erasure under the same safety projection;
- a communication-closure theorem whose premises map to the two kernels without
  additional argument;
- a dissertation lemma proving the same replay/closure characterization.

## 6. Sources pinned by the artifact

- CometBFT `v0.40.0`, commit
  `0880b4d378f347ab16e54ec677ff50d803f37d62`;
- `relab/hotstuff`, commit
  `3179c6e62929294961acbfd9bf8445769716a121`;
- local SHA-256 manifests under `inputs/` and `gate2p/`.
