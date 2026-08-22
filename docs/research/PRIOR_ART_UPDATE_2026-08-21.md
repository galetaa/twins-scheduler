# Focused prior-art and novelty update

**Evidence cut-off:** 21 August 2026  
**Claim under review:** preservation of finite agreement-violation observations when a phase-specific admission policy is closed to one type-uniform directed endpoint graph.

## Search scope

The refresh covered the mechanism rather than the title alone: scheduler languages, message adversaries, communication closure, BFT testing, phase/type filters, replay, fault-injector semantics, refinement, and operational/formal links to locking consensus. Sources included peer-reviewed papers, preprints, official protocol specifications, and open engineering artifacts. Engineering capability can destroy an implementation novelty claim but is not treated as proof of a theorem.

## Closest work

| Source | Type | Established capability/result | Relation to this work | Novelty threat |
|---|---|---|---|---|
| Bano et al., *Twins* | Peer-reviewed | Same-identity replicas, round-indexed scenarios, leader equivocation, double voting, and state-loss tests | Establishes the testing lineage; does not characterize phase-erasure preservation | High to tool claims; medium to theorem |
| Drăgoi et al., *Communication Closure* | Peer-reviewed | Reduces a class of asynchronous consensus executions to lossy synchronous executions while preserving tested behavior under stated conditions | Closest result by problem; does not collapse phase labels to one endpoint bit or use the repair/pivot mechanism | Critical comparison |
| Heard-Of and closed message adversaries | Peer-reviewed theory | Round communication graphs and languages of message adversaries | Supplies established graph semantics; directed graphs are not novel | High to model claims |
| Winter et al., randomized BFT testing / ByzzFuzz | Peer-reviewed | Message mutation and randomized Byzantine testing beyond unmodified clones | Rich fault authority is known; no identical property-preserving closure theorem found | High to engineering claims |
| Netrix | Peer-reviewed/tool | Sender/receiver/type predicates, controlled drop/store/delivery/replay, and execution monitors | Rich scheduler APIs are prior art | High to API claims |
| ByzzBench | Peer-reviewed/tool | Controlled benchmark infrastructure and exact safety evaluation for BFT testing algorithms | Benchmarking and campaigns are not the contribution | Medium-high |
| Barreto et al., VLSM | Formal-methods preprint | Validator-system trace semantics and Byzantine/equivocation correspondence under explicit validity assumptions | Eliminates broad Byzantine-to-equivocation novelty; supports a narrower scheduler question | High to broad claims |
| Ni et al., functional reasoning | Formal-methods preprint with Rocq development | Safety-preserving connection between synchronous functional reasoning and asynchronous operational semantics | Important adjacent mechanized refinement work; different transformation and property boundary | Medium-high |
| Zhou et al., PERF | FM 2026 preprint | Formal fault-injector models, composition, and performance prediction | Injector specification/composition is known; this work must remain about safety observation | High to framework claims |
| Freitas et al., ByzTwin-Range | 2026 preprint | Digital-twin cyber-range for controlled Byzantine experimentation | Fresh practical threat to scenario-generation novelty, not to the stated theorem | High to engineering claims |
| CometBFT v0.39.3 specification | Official engineering source | Propose/Prevote/Precommit/Commit, PoLC, lock/relock, and commit rules | Supplies the natural bounded rule-level instantiation; does not state the scheduler theorem | Validation target |

## Novelty kill test

1. Partitions, directed graphs, phase/type filters, per-message control, and replay are all known separately.
2. A new scheduler DSL, benchmark, or mutation campaign is therefore not a scientific contribution here.
3. Communication-closure work proves a different normal form and must be treated as the closest conceptual threat.
4. The surviving claim is property-sensitive: type closure can insert already-emitted repair evidence that disables the unique correct contributor required by two conflicting quorums, thereby deleting an agreement-violation observation.
5. The paper now gives: exact scheduler semantics; a legal-target closure theorem; a structural quorum-pivot criterion; a parametric `3f+1` family; a bounded Tendermint-style instantiation; an exact diagnostic Boolean boundary; and replay erasure with state and output congruence.
6. The result remains bounded to the stated protocol schema and observation. It does not establish universal incompleteness of graph schedulers or a vulnerability in CometBFT.

## Defensible novelty delta

> Closest work supplies same-identity BFT testing, message-adversary graphs, communication-closure reductions, phase-aware testing controls, replay, benchmark infrastructure, and formal fault-injector models. In the sources reviewed through 21 August 2026, no work was found that simultaneously defines closure from per-phase admission to one type-uniform directed endpoint graph, requires the closed trace to be legal in the target language, studies finite agreement-violation observations, characterizes the repair/unique-quorum-pivot separation, instantiates the mechanism in bounded Tendermint-style locking rules, and proves replay erasure under both state and output congruence. This is a search-bounded claim, not proof of absolute novelty.

## Decision

**CONDITIONAL PASS.** The narrowed theorem package remains distinguishable. Reopen Gate 0 if a later source provides the same closure operator, property projection, legal-target condition, and repair/pivot criterion, or if the rule-level Tendermint mapping fails an independent refinement review.
