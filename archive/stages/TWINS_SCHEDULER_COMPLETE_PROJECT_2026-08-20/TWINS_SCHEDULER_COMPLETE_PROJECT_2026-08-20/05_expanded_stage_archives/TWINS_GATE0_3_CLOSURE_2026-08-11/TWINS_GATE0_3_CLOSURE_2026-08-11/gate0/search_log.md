# Gate 0 — Search log

**Search date:** 11 August 2026  
**Scope:** literature and engineering prior art relevant to finite-clone Twins expressiveness, state equivocation, refinement, dynamic process creation, chain cover and concrete harness semantics.

## Sources fully or substantially checked

- Bano et al., *Twins: BFT Systems Made Robust*, OPODIS 2021, DOI `10.4230/LIPIcs.OPODIS.2021.7`, arXiv `2004.10617`.
- Zamfir et al., *Validating Labelled State Transition and Message Production Systems*, arXiv `2202.12662v4`, including the state-equivocation definitions and Byzantine/equivocation trace theorems.
- Winter et al., *Randomized Testing of Byzantine Fault Tolerant Algorithms*, PACMPL/OOPSLA 2023, DOI `10.1145/3586053`.
- Louro Neto and Kulahcioglu Ozkan, *A Benchmark Framework for Byzantine Fault Tolerance Testing Algorithms*, FMBC 2025, DOI `10.4230/OASIcs.FMBC.2025.13`.
- Drăgoi et al., *Testing Consensus Implementations Using Communication Closure*, PACMPL/OOPSLA 2020, DOI `10.1145/3428278`.
- Marić et al., *Cutoff Bounds for Consensus Algorithms*, CAV 2017, DOI `10.1007/978-3-319-63390-9_12`.
- Konnov et al., *A Short Counterexample Property...*, POPL 2017, DOI `10.1145/3009837.3009860`.
- Abadi and Lamport, *The Existence of Refinement Mappings*, TCS 1991, DOI `10.1016/0304-3975(91)90224-P`.
- Lynch and Tuttle, *An Introduction to Input/Output Automata*, CWI Quarterly 1989.
- Attie, *Dynamic Input/Output Automata*, JCSS 2016 / MIT technical report, covering dynamic creation and destruction of automata.
- Winskel, *Event Structures*, 1987, for causal/conflict histories.
- Cáceres et al., *Minimum Chain Cover in Almost Linear Time*, ICALP 2023, for the explicit width/minimum-chain-cover identity on DAGs.
- Liang et al., *Node-Centric Systematic Testing for Distributed Systems*, ACM TOSEM 2026, DOI `10.1145/3831368`.
- `asonnino/twins-simulator` and `relab/hotstuff` official repository documentation.

## Search families

- `Twins BFT completeness coverage theorem clone adversary`
- `full disclosure Twins Byzantine causal past`
- `state equivocation finite copies clone cutoff`
- `dynamic state equivocation bounded replicas`
- `correct-code clones arbitrary Byzantine trace inclusion`
- `I/O automata dynamic process creation refinement copies`
- `event structure unfolding histories chain cover replicas`
- `minimum chain cover causal histories testing`
- `round partition Twins scenario expressiveness`
- `node-centric equivalence distributed testing clones`

## Saturation finding

No publication was found that states the exact finite-clone theorem proposed in the previous report. That absence no longer supports novelty because the selected semantics themselves yield the generic static-unfolding and active-slot-collapse theorems in `theorem_candidate.md`.

## S20 limitation

The official ACM metadata and abstract for *Node-Centric Systematic Testing for Distributed Systems* were available, but an open full text was not found. The abstract concerns node-centric transition equivalence and bug-preserving state-space reduction, not shared protocol identities, clone lifecycle or a finite-clone cutoff. Because Gate 0 ends in no-go by independent derivation, this access gap cannot rescue the rejected claim.

## Expert-review limitation

No live subject-matter expert was contacted in this run. The prior Gate 0 plan requested an expert terminology review. This remains an external validation action for any future pivot, but it is not needed to justify the present no-go: the collapse follows from explicit assumptions and an executable exact pilot.
