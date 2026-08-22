# Gate 5′ source register

**Search cut-off:** 15 August 2026.

## Academic prior art

| Source | Type | Relevance | Stable identifier |
|---|---|---|---|
| Bano et al., *Twins: BFT Systems Made Robust* | Peer-reviewed OPODIS paper | Clone-based BFT testing and partition scenarios; prior art for the original method | DOI `10.4230/LIPIcs.OPODIS.2021.7`; https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.OPODIS.2021.7 |
| Drăgoi et al., *Testing Consensus Implementations Using Communication Closure* | Peer-reviewed PACMPL/OOPSLA paper | Canonical schedule reduction and the closest threat to closure claims | DOI `10.1145/3428278`; https://dl.acm.org/doi/10.1145/3428278 |
| Winkler, Schmid, Moses, *A Characterization of Consensus Solvability for Closed Message Adversaries* | Peer-reviewed OPODIS paper | Directed communication graph per round and message-adversary language | DOI `10.4230/LIPIcs.OPODIS.2019.17`; https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.OPODIS.2019.17 |
| Winter et al., *Randomized Testing of Byzantine Fault Tolerant Algorithms* | Peer-reviewed PACMPL/OOPSLA paper | Message mutations and randomized BFT testing; prevents claiming richer faults as new | DOI `10.1145/3586053`; https://dl.acm.org/doi/10.1145/3586053 |
| Drăgoi et al., *A Domain Specific Language for Testing Distributed Systems* / Netrix | Peer-reviewed/formal testing work | Filters, monitors, drop, delay, ordering, and replay are prior art | DOI `10.1007/978-3-031-67321-4_6`; preprint https://arxiv.org/abs/2303.05893 |
| Louro Neto and Kulahcioglu Ozkan, *A Benchmark Framework for Byzantine Fault Tolerance Testing Algorithms* | Peer-reviewed FMBC tool paper | ByzzBench and cross-tester benchmarking; prevents claiming a benchmark framework as contribution | DOI `10.4230/OASIcs.FMBC.2025.13`; https://drops.dagstuhl.de/entities/document/10.4230/OASIcs.FMBC.2025.13 |

## Engineering and protocol sources

| Source | Type | Version | Use in artifact |
|---|---|---|---|
| CometBFT release | Official release | `v0.40.0`, commit `0880b4d378f347ab16e54ec677ff50d803f37d62` | Pinned source semantics for rounds, locks, valid round, and duplicate votes |
| `types/vote_set.go` | Official source code | Same commit | Duplicate vote stuttering and validator-index voting-power accounting |
| `internal/consensus/state.go` | Official source code | Same commit | Lock update before precommit and valid-round state |
| `spec/consensus/consensus.md` | Official specification | Same commit | Propose/Prevote/Precommit round and PoLC lock vocabulary |
| `relab/hotstuff` Twins files | Official open-source repository snapshot | commit pinned in Gate 4′ | First-kernel network-admission and partition semantics |

All downloaded source files are stored locally with SHA-256 manifests. White
papers, source code, documentation, and tool papers are not treated as
peer-reviewed proofs, but they can eliminate practical or engineering novelty.
