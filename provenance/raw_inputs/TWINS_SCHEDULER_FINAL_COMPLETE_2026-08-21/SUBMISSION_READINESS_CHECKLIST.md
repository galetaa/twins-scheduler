# Submission-readiness checklist

## Scientific and formal revision

- [x] Natural protocol selected: CometBFT/Tendermint-style locking.
- [x] Explicit rule-level map for pivot, enabling evidence, repair evidence, certificate opportunities, and shared edge.
- [x] Exact bounded domain and fixed phase order specified.
- [x] Structural quorum-pivot criterion proved at paper and certificate levels.
- [x] Parametric `3f+1`, quorum-`2f+1` family stated as a corollary.
- [x] `UnsafeObs` typing repaired.
- [x] Directed and phase-specific scheduler relations formalized.
- [x] Closure defined without message synthesis and with stable once-only delivery.
- [x] Legal target-language condition added to the closure theorem.
- [x] Replay theorem strengthened with output congruence.
- [x] Hidden `X,X,Y` state/output counterexample retained.
- [x] Seven-premise operational equation and paper derivation included.
- [x] Internal artifact theorem IDs removed from the main paper.
- [x] Related-work comparison matrix and 21 August 2026 refresh included.

## Executable evidence

- [x] Independent final checker passes.
- [x] Python bounded protocol model passes.
- [x] Independent Go bounded protocol model passes.
- [x] Python/Go outputs match.
- [x] Focused pytest passes.
- [x] Project-local kernel 1.1.0 passes.
- [x] Five damaged kernel controls are rejected.
- [x] Eight positive Z3 obligations are `UNSAT`.
- [x] Four damaged Z3 controls are `SAT`.
- [x] One-command reproduction is provided.

## Submission blockers

- [ ] Pinned Lean project compiled by `lake build` or parallel Coq project compiled by `coqc`.
- [ ] Mature-prover axiom/assumption report reviewed.
- [ ] Official `lipics-v2021.cls` source compiled successfully.
- [ ] Author names, affiliations, ORCID data, funding, and student-paper eligibility supplied.
- [ ] Literature search refreshed on the actual submission date.
- [ ] AI-use disclosure adapted to the final venue policy and approved by the authors.
