# Gate 8′ Prior-Art and Novelty Refresh

**Search cut-off:** 17 August 2026  
**Question:** Is there already a result that characterizes when erasing phase/type labels to one directed endpoint graph preserves finite agreement-violation observations in certificate-driven locking BFT protocols, including the quorum-pivot repair boundary and stable-key replay erasure?

## Search scope

The refresh covered academic and engineering terminology for scheduler grammars, message adversaries, communication closure, BFT testing, fault injection, replay/idempotence, locking protocols, causal schedules, refinement, and formal fault models. Sources were separated by evidentiary type: peer-reviewed theorem/system paper, preprint, protocol specification, source snapshot, and testing artifact.

## Closest sources and novelty threat

| Source | Type | Established contribution | Overlap with Gate 8′ | What remains different | Novelty threat |
|---|---|---|---|---|---|
| Bano et al., **Twins: BFT Systems Made Robust**, OPODIS 2021, DOI `10.4230/LIPIcs.OPODIS.2021.7` | Peer-reviewed systems paper | Shared-identity twins and round-varying communication scenarios for BFT testing | Clone/partition testing and injected lock-loss defects | No phase-erasure preservation theorem, quorum-pivot closure construction, or replay-erasure boundary | High for engineering novelty; medium for theorem novelty |
| Drăgoi et al., **Testing Consensus Implementations Using Communication Closure**, OOPSLA 2020, DOI `10.1145/3428278` | Peer-reviewed PL/formal paper | Property-preserving reduction of suitable asynchronous consensus executions to controlled communication-closed executions | Closure and canonical schedule reasoning | Different transformation and assumptions; does not characterize phase-label erasure through repair-disabled quorum participation | Critical adjacent theorem threat, but not a kill found |
| Winkler, Schmid, Moses, **A Characterization of Consensus Solvability for Closed Message Adversaries**, OPODIS 2019, DOI `10.4230/LIPIcs.OPODIS.2019.17` | Peer-reviewed theory paper | Per-round directed communication graphs and consensus-solvability characterization for closed message adversaries | Establishes directed graph languages as prior art | Studies solvability of adversary languages, not equality of unsafe-observation languages under phase erasure | High terminology/model threat |
| Charron-Bost and Schiper, **The Heard-Of Model**, Distributed Computing 2009, DOI `10.1007/s00446-009-0084-6` | Peer-reviewed theory paper | Round-by-round receive sets for distributed algorithms | Coarse communication abstractions | No phase-labelled closure or locking-repair separation | Medium |
| Winter et al., **Randomized Testing of Byzantine Fault Tolerant Algorithms**, OOPSLA 2023, DOI `10.1145/3586053` | Peer-reviewed testing paper | Randomized BFT fault/message exploration | Richer adversarial actions and testing | Does not prove the safety-observation closure boundary studied here | High for API/testing novelty; low-to-medium for theorem novelty |
| Drăgoi et al., **A Domain Specific Language for Testing Consensus Implementations (Netrix)**, NETYS 2024, DOI `10.1007/978-3-031-67321-4_6` | Peer-reviewed systems/formal paper | Programmer-guided message filters, monitors, reproduction, and regression testing | Phase/type/instance-selective testing power | Gate 8′ does not claim filters or a DSL; it studies when that extra power changes agreement observations | High for engineering novelty; low for theorem novelty |
| Louro Neto and Kulahcioglu Ozkan, **ByzzBench**, FMBC 2025, DOI `10.4230/OASIcs.FMBC.2025.13` | Peer-reviewed tool paper | Controlled benchmark infrastructure for BFT testing algorithms | Common execution and fault-control infrastructure | No property-preserving closure theorem or honest-pivot separation | Medium |
| Yin et al., **HotStuff**, PODC 2019, DOI `10.1145/3293611.3331591` | Peer-reviewed protocol paper | Partially synchronous chained BFT with quorum certificates | Certificate and locking vocabulary | Protocol design, not scheduler-language characterization | Low as novelty threat; high as construct-validity source |
| Dwork, Lynch, Stockmeyer, **Consensus in the Presence of Partial Synchrony**, JACM 1988, DOI `10.1145/42282.42283` | Peer-reviewed theory paper | Partial-synchrony foundations | Network/adversary assumptions | Gate 8′ is safety-only and finite; does not claim liveness | Low direct threat |
| CometBFT `v0.40.0` consensus specification and source snapshot | Engineering specification/source | Propose–Prevote–Precommit, locks, valid rounds, vote-set semantics | Natural certificate-driven locking terminology and controlled source mapping | No claim that production CometBFT instantiates the defective schema | Construct-validity evidence, not novelty kill |
| `relab/hotstuff`, commit `3179c6e62929294961acbfd9bf8445769716a121` | Engineering source | View-indexed partitions, controlled message types, pending queue semantics | Concrete coarse harness semantics | Gate 8′ theorem is protocol-independent and does not claim a bug in this implementation | High for practical motivation; no theorem kill |
| Zhou et al., **A Formal Framework for Predicting Distributed System Performance under Faults (PERF)**, FM 2026 / arXiv `2602.19088` | Accepted formal-methods paper / preprint | Formal fault injector and composed models for loss, duplication, delay, tampering, equivocation, partitions; statistical performance prediction | Modern formal fault-injection framework | Focuses performance/statistical analysis, not safety-observation preservation under phase erasure | New adjacent engineering/formal threat; no direct kill |
| Ni et al., **Functional Reasoning for Distributed Systems**, 2025 | Formal-methods research | Functional reasoning abstractions for distributed systems | General proof structuring | No inspected theorem matching the closure/separation claim | Low-to-medium |
| de Moura and Bjørner, **Z3**, TACAS 2008, DOI `10.1007/978-3-540-78800-3_24` | Solver paper | SMT solving used by the artifact | Proof tool only | No subject-matter novelty overlap | None |

## Special nearest-neighbor classification

- **Closest by problem:** communication-closure testing, because both ask whether a schedule transformation preserves a protocol property.
- **Closest by formal model:** closed message adversaries and Heard-Of, because they treat communication patterns as graph languages.
- **Closest by mechanism:** Twins/Netrix, because they expose different granularity of communication control.
- **Closest by experimental design:** ByzzBench and randomized BFT testing, because they compare fault-injection behavior in controlled executions.
- **Engineering artifact most threatening practical novelty:** Netrix; phase- and message-sensitive filtering is already implemented.
- **Adjacent 2026 result:** PERF; formal fault injectors and broad fault libraries are not new.

## Novelty kill test

1. **Same combination of problem, mechanism, property, and test?** Not found in the inspected sources.
2. **Are all elements known separately?** Yes: graph adversaries, phase-aware filters, closure proofs, locking certificates, replay, and formal fault injection.
3. **Is mere combination enough?** No. The contribution survives only because it gives a new property-level consequence: closure-added repair evidence can remove the unique honest quorum pivot and thereby erase an agreement witness.
4. **Does it change system understanding?** Narrowly: it identifies why adding valid deliveries can make a coarser scheduler less expressive for a selected safety observation.
5. **Is it only a new API or application?** It must not be presented that way. The API capability is prior art.
6. **Does novelty depend on a particular client, chain, or workload?** No; the core result is an explicit parametric schema. Client mappings are validation only.
7. **Can the contribution be stated without “first applied”?** Yes: relational closure theorem, parametric separation, exact premise boundary, and replay-erasure theorem.
8. **Could hidden engineering prior art kill the claim?** It could kill practical novelty, but practical novelty is not claimed. A hidden refinement/closure theorem with the same phase-erasure consequence would threaten the theorem claim.
9. **Minimum evidence needed to preserve novelty:** the precise closure operator, Theorem T2 with nontrivial instantiation obligation, T3 construction, T6 exact boundary, and a search-limited related-work statement.
10. **Absolute novelty?** Not established and not claimed.

## Frozen novelty delta

Closest works establish clone/partition testing, directed communication adversaries, communication-closure reductions, phase- and message-sensitive testing DSLs, mutation-based BFT testing, and benchmark infrastructure. In the sources inspected through 17 August 2026, no work was found that simultaneously defines erasure from phase-specific delivery to one type-uniform directed endpoint graph, asks preservation of finite agreement-violation observations, identifies closure-added repair evidence that disables a unique honest quorum pivot, and pairs this separation with a stable-key replay-erasure boundary. The proposed contribution is limited to those formal claims and their executable validation. This statement is bounded by the databases, terminology, languages, access, and search date and must be refreshed immediately before submission.

## Decision

**CONDITIONAL PASS.** The theorem-level novelty remains defensible in a narrow scope. Engineering novelty is intentionally disclaimed. A newly found refinement or communication-closure theorem that directly entails T3 would trigger **NO-GO or major rewrite**.
