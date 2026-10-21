# Completed revision: editorial corrections and dependent seven-validator study

The cover now gives the definite status **not nominated (eligibility not claimed)**. The named version identifies Mikhail Alexandrovich Galeta and SUAI; the separate review version suppresses the author/affiliation and public repository URL. The student status supplied by the author does not by itself verify the venue's primarily-student-written criterion. No contact address or ORCID is fabricated.

Literal `Appendix~A`/`Table~1` rendering was fixed at the Markdown-to-LaTeX boundary, using raw LaTeX reference spans. Both compiled PDFs are checked for unresolved references, literal tildes, replacement glyphs, page budget and author leakage. The reviewer matrix is regenerated from current claim IDs and manuscript locations; the six current theorems no longer conflict with historical numbering.

The substantive new experiment (C36, Section 6.3 and Appendix G) has seven validators, quorum five and six interdependent control fibres. Its complete declared bound has 48,201 states and 55,283 transitions. The same guards couple cross-pivot prevotes, mixed-quorum timeout evidence and later-round signatures. Independent total-policy reachability, direct exact synthesis and independently checked refinement histories agree: unit-cost optimum two; heterogeneous costs (2,5,9,3,7,11) give optimum five; forbidding P1-side refinements is infeasible. Both unmutated observers disagree in the re-executed witness. The original and one-pivot-mutant models are safe within their bounds, and three dependency removals eliminate all unsafe states.

The initial guard-aware quotient falsely suggests cost zero. Nine safe-policy invariants eliminate spurious policies before the final 562-state/961-edge quotient's cost-two lower bound is matched by concrete replay. Every iteration covers every concrete input edge. The explicit accounting includes all 121,615 discovered abstract product states, peak 21,627, all 30,552 certificate states and 552,830 repeated edge-coverage checks. Direct search discovers 21,544 states and is cheaper in this instance. We therefore claim an auditable explanatory reduction and instrumentation decision, **not speed superiority**. The declared seed is heuristic and a guard-blind bounded control returns unknown.

The novelty discussion now separates conventional shortest paths, CEGAR, simulation, certifying computation and minimal revision from this work's persistent static-policy/fibre-cost/evidence contract. The practical output is a minimum set of phase predicates, an executable regression witness, and a checked reason why cheaper policies fail. Client-wide completeness and a native mutant attack remain unclaimed.

The interrupted sources were reconstructed and all new results rerun. Archived binary evidence is not substituted for a reproduction. See `SCALED_PROTOCOL.md`, current source hashes in `results/scaled/summary.json`, the full histories, and fresh run logs.

---

## Earlier general-transition revision response (retained context)

# Response on the scope of optimality

We have addressed the independent-pivot limitation in **Certified Minimum-Cost Scheduler Refinement for Stateful BFT Testing**. The main result now concerns general transition semantics; independent pivots form a structural specialization.

## General semantics and exact synthesis

The main model permits arbitrary shared protocol state and cyclic transitions. Locks, quorum accumulation, message production, block availability and timer enabledness need not decompose into independent participant contributions. Each policy-controlled step queries a fine admission key; a fixed projection groups fine keys into coarse fibres. An unsplit fibre must receive a uniform Boolean decision. Splitting permits independent fine decisions and incurs its supplied nonnegative integer cost once. Allowed and required split sets are explicit inputs.

Theorem 1 proves that a fine-key-consistent trace has the least split set consisting of its mixed coarse fibres together with required splits. Constructive policy completion proves sufficiency. Repeated fine-key answers must agree, including on cycles. Theorem 2 gives exact finite synthesis on protocol states paired with partial static policies. The objective is existential finite unsafe reachability under one total static policy. A resource cutoff yields unknown. The appendix proves NP-completeness even for acyclic graphs with two fine keys per fibre using a Set Cover reduction.

Theorem 3 separates finding a witness from certifying its optimality. A safe set of product states, closed under every legal raw-input successor below the claimed cost, excludes every cheaper counterexample. The independent checker recomputes these obligations without calling the optimizer. The checker validates the witness, total policy, permissions, cost and input identity; full safe closure certifies infeasibility. Certificates may be large. [Semantics and implementation](../research/TRANSITION_SYNTHESIS.md).

## A checked connection to a more detailed system

Theorem 4 makes the direction of abstraction explicit. A local covering simulation preserves the initial state, includes concrete bad states in abstract bad states, and covers every concrete edge. Policy queries retain the exact key and Boolean answer; only internal steps may stutter. The control and cost interfaces agree. Therefore every concrete unsafe trace is represented abstractly under the same policy, and the abstract optimum is a lower bound on the concrete optimum. A concrete replay supplies an upper bound. Equality establishes concrete optimality.

The executable bridge checks all concrete edges, not just an exhibited path. It distinguishes lower bounds, intervals, exact minima and infeasibility. Coverage is checked exhaustively for supplied finite systems; no source-level refinement of the full Go client is asserted.

Theorem 5 adds invariant-guided abstraction refinement. An abstract witness supplies a complete static policy. If concrete reachability under that policy is safe, its reachable-state set defines an invariant. Splitting every abstract block by membership in that invariant eliminates the entire spurious policy and strictly refines the partition. Without resource cutoffs the finite process terminates. The history checker validates exact quotients, certificates, invariant closure, partition progress and the final bridge. We credit established CEGAR; our specialization concerns persistent admission decisions, one-time refinement costs and independently checked policy elimination. [Bridge and refinement](../research/TRANSITION_ABSTRACTION.md).

## Evidence beyond independent pivots

The new guarded model has four validators, one Byzantine participant, two rounds, twelve stages and thirty-two once-only opportunity slots. It explores every ordering within a stage, including old-certificate repair versus quorum-enabled timeouts, and includes actual missing-block catchup. Only P's round-zero lock assignment is omitted in the mutant; valid-state and later lock updates remain. The unsafe predicate requires conflicting decisions by the unmutated observers A and C.

Five controls demonstrate dependencies absent from the old independent contract. In particular, suppressing both incoming precommits can remove round-advance readiness even after enabling prevotes arrive. Absence of repair therefore does not imply availability of the second vote. Old-round repair may also leave the node waiting for a block, and the separate block admission decision controls finalization.

The complete bounded mutant graph contains **2,516 states, 5,856 transitions and 16 unsafe states**. Refinement from the coarsest partition eliminates **11 spurious policies** in **12 iterations**, reaching **26 abstract states and 60 transitions** and proving minimum cost **2**. The concrete witness is replayed through protocol guards: **30 opportunities, 172 log events, 16 authenticated model messages, six local certificates and twelve passing audits**, ending in A=0 and C=1. Costs 5 and 2 are supplied input prices, not measured production overhead. The baseline has **2,372 states, 5,574 transitions and no unsafe state within this opportunity language**. [Recorded results](../../results/transition/summary.json), [complete refinement results](../../results/transition_bridge/bridge_summary.json).

## Validation and mechanization

The new validation layers are reported separately:

- **7,904** declared graph/cost/permission cases compare general synthesis with full policy enumeration.
- **2,960** further cases compare direct and abstraction-guided minima with an independent raw-graph oracle: **5,920** optimum comparisons and **6,857** independently checked iterations, including final certificates.
- **1,507** specialization cases compare both old and general solvers with a raw policy/event oracle: **3,014** comparisons and **1,189** successful equal-cost witness normalizations.
- All **64** policies of each protocol variant are checked using a separate exploration loop sharing the protocol guards and canonicalization. The **128** checks compare counts with the exported quotient omitting the same first-arrival diagnostic. They test export consistency, not independent consensus semantics.

All recorded comparisons have zero mismatches. The active Python suite has **119 passing tests**. The integrated Lean build has **15 jobs**, an audit of **46 declarations**, independent kernel rechecking and hygiene checks over **23 source files**. New declarations cover policy completion, least trace refinement, memory consistency, closed-sublevel certificates, labelled simulation, cost-bound transfer and invariant-based policy elimination. The Python programs, exporter and production client are not mechanically verified. [Mechanization map](../research/TRANSITION_MECHANIZATION.md).

The retained weighted four-role theorem and SCC/quota solver now appear as Theorem 6 and its detailed structural appendix. An explicit semantics adapter and normalization proof establish equal optima under their stronger behavioral contract. Existing native conformance continues to exercise unchanged CometBFT v0.39.3 using genuine Ed25519 signatures. The new guarded model uses HMAC test authentication; native mutation or native conflicting decisions are not claimed.

## Resulting scope

The revised claim is optimal refinement for a supplied protocol transition system with a control-complete static admission interface, with an explicit route to implementation-model optimality through checked coverage and a matching concrete witness. The former independent-pivot assumption is removed from the main results. Unbounded production implementations still require a justified semantic connection; general program reachability cannot be replaced by an unconditional terminating optimizer. The revision supplies the broader theorem and a dependent-state instantiation.
