# Prior-art update and novelty decision — 20 August 2026

## Search question

The search was re-run after the independent proof audit.  It targeted not merely
"Twins" or BFT testing, but the exact residual claim: preservation of finite
agreement-violation observations when a scheduler erases message phase/type and
collapses per-phase admission to one directed endpoint edge in one view; the
countermechanism is closure-added repair evidence disabling a unique correct
quorum pivot.  A second query targeted replay erasure under stable-key
idempotence and projection congruence.

The search covered scholarly papers, preprints, protocol specifications, source
repositories, and current engineering frameworks.  Absence below is bounded by
publicly accessible sources, terms, languages, and the search date; it is not a
proof that no prior art exists.

## Closest scholarly and engineering sources

| Source | Type | What it already establishes | Relation to the revised claim | Novelty threat |
|---|---|---|---|---|
| Bano et al., **Twins: BFT Systems Made Robust**, OPODIS 2021, DOI 10.4230/LIPIcs.OPODIS.2021.7 | Peer-reviewed systems paper | Same-identity replicas, partitions that vary by round/view, deterministic Byzantine scenarios | Establishes the testing lineage and destroys novelty for clone/partition testing itself; does not characterize safety-observation preservation under phase erasure | High to broad claims; low-to-medium to the narrowed theorem |
| Dragoi et al., **Testing Consensus Implementations Using Communication Closure**, TOPLAS 2021, DOI 10.1145/3428278 | Peer-reviewed formal/systems paper | Communication-closure reduction and model-based testing of Paxos-style implementations | Closest work on property-preserving schedule normalization.  It makes any broad “new normal form” claim untenable, but it does not give the same phase-erasure/repair-pivot separation | Very high |
| Charron-Bost and Schiper, **The Heard-Of Model**, Distributed Computing 2009 | Peer-reviewed distributed-computing theory | Round receive sets and communication abstractions | Directed/round communication languages are known; graph grammars are not the contribution | High to scheduler-language novelty |
| Rincon Galeana et al., **Characterizing Asynchronous Message-Passing Models Through Rounds**, OPODIS 2019, DOI 10.4230/LIPIcs.OPODIS.2019.17 | Peer-reviewed theory | Message adversaries, delivered collections, and round-model characterizations | Closest neighboring theory for communication languages; no matching finite agreement-observation phase-erasure result found | Medium-high |
| Barreto et al., **Validating Labelled State and Message Production Systems**, arXiv:2202.12662 | Formal-methods preprint | Validator-system traces and equivalence between Byzantine and equivocation models under explicit validity assumptions | Eliminates the former broad Byzantine-to-equivocation novelty; motivates the narrower scheduler-closure question | High |
| Ganesan et al., **Systematic Testing of Distributed Systems with Netrix**, arXiv:2303.05893 | Systems-testing paper/preprint | Message-level filters, monitors, controlled delivery/drop/replay for consensus testing | Richer scheduler APIs and per-message control are already engineering prior art | High to implementation claims |
| Jepsen et al., **ByzzBench: Benchmarking Fault-Tolerant Distributed Systems**, FMBC 2025, DOI 10.4230/OASIcs.FMBC.2025.13 | Peer-reviewed benchmark paper | Deterministic simulation, fault-injection benchmark, exact safety checking | New harness/benchmark/campaign is not a scientific novelty; does not supply the revised closure theorem | Medium-high |
| Buchman et al., **ByzzFuzz: Automated Byzantine Fault Injection**, technical paper/artifact | Engineering/research artifact | Message mutation and randomized Byzantine behaviors beyond unmodified Twins | Demonstrates that correct-code clones do not cover arbitrary mutation faults; rules out broad completeness claims | Medium-high |
| Wang et al., **PERF: A Framework for Specifying and Reasoning About Fault Injectors**, arXiv:2602.19088 | 2026 preprint | Formal specification and composition/reasoning for fault injectors | Further destroys novelty for injector taxonomies or composition; no identical phase-erasure observation theorem found | High to framework claims; medium to narrowed result |
| Gorbunov, Konnov, and Yurchenko, **Improving the Validation of BFT Consensus Protocols with Enhanced Fault Injection and Scenario Generation**, arXiv:2604.18049 | 2026 preprint | ByzTwin-Range, broader scenario generation and fault injection for Twins-style validation | Closest fresh engineering threat; the revised contribution must remain a theorem/characterization, not scenario-generation machinery | High to engineering novelty |
| relab/hotstuff `twins` implementation and documentation, commit family inspected in earlier gates | Open-source implementation | One view contains leader and partitions; admission is controlled by shared partition membership and selected runtime message types | Concrete instantiation of a coarser scheduler and source of conformance obligations; implementation novelty is absent | High to practical novelty |
| CometBFT consensus specification | Official protocol specification | Proposal/prevote/precommit, POLKA/PoLC, locking and valid-round behavior | Supplies a natural locking vocabulary and validation target; does not itself claim the scheduler theorem | Medium |

## Closest source by dimension

- **Problem:** communication closure and property-preserving testing (Dragoi et al.).
- **Mechanism:** Twins/ByzTwin-Range partition and phase-controlled scenarios.
- **Formal model:** Heard-Of/message-adversary and VLSM trace semantics.
- **Experimental design:** Netrix and ByzzBench controlled message scheduling.
- **Engineering novelty threat:** ByzTwin-Range and Netrix.
- **Neighboring result most likely to have been missed:** general fault-injector
  reasoning in PERF.

## Novelty kill test

1. The same broad combination of “BFT testing + richer scheduler + replay” is
   already known.  It is not claimable.
2. All individual language ingredients—partitions, directed round graphs,
   per-type filters, per-message delivery, and replay—are known.
3. The paper therefore cannot claim a new scheduler hierarchy merely because
   the implementation enumerates it.
4. The surviving result is the *property-sensitive boundary*: phase erasure can
   insert repair evidence that removes the unique correct quorum pivot, thereby
   deleting a finite agreement-violation witness.
5. The corrected replay result survives only as a semantic boundary under
   stable keys, projected duplicate stutter, output silence, state-based
   observation, and projection congruence.
6. The contribution is meaningful only if the transition system, phase order,
   same-view condition, bounded directed domain, and decisions are all part of
   the theorem.  The post-audit revision now makes them explicit.
7. No novelty is attributed to a particular client, network, programming
   language, dataset, workload, mutation campaign, or API.

## Defensible novelty delta

> Closest work establishes communication abstractions, schedule-normalization
> results, same-identity BFT testing, message-level testing controls, fault-
> injector frameworks, and expanded scenario generation.  In the sources
> reviewed through 20 August 2026, no result was found that simultaneously
> defines the same-view phase-erasure closure, projects executions to finite
> agreement violations, identifies closure-added repair evidence as disabling a
> unique correct quorum pivot, gives the exact seven-premise operational
> boundary, and pairs it with replay erasure under projection congruence.  The
> claim is limited to the explicit finite schema and corrected T1/T2/T3/T6
> statements; absolute novelty is not asserted.

## Decision

**CONDITIONAL PASS.**  The narrowed theorem package remains a plausible
publication contribution.  The decision would revert to `NO-GO` if a pre-
submission search finds an existing theorem with the same property projection,
closure operator, repair/pivot mechanism, and exact boundary, or if a reviewer
shows that the result is an immediate corollary of a communication-closure
framework under assumptions already stated there.

## Stable identifiers and official sources

- Twins: https://doi.org/10.4230/LIPIcs.OPODIS.2021.7
- Communication closure: https://doi.org/10.1145/3428278
- Heard-Of: https://doi.org/10.1007/s00446-009-0082-6
- Round/message-adversary characterization: https://doi.org/10.4230/LIPIcs.OPODIS.2019.17
- VLSM: https://arxiv.org/abs/2202.12662
- Netrix: https://arxiv.org/abs/2303.05893
- ByzzBench: https://doi.org/10.4230/OASIcs.FMBC.2025.13
- PERF: https://arxiv.org/abs/2602.19088
- ByzTwin-Range: https://arxiv.org/abs/2604.18049
- relab/hotstuff: https://github.com/relab/hotstuff
- CometBFT consensus specification: https://docs.cometbft.com/main/spec/consensus/consensus
