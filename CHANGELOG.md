# Changelog

## Unreleased — general transition and checked-abstraction revision, 2026-10-19

- Removed independent-pivot assumptions from the main optimality formulation.
  Arbitrary protocol state and cyclic transitions are represented by a labelled
  transition system with persistent static admission decisions. The exact trace
  refinement is the union of required and mixed coarse fibres.
- Added exact product-state synthesis and independent closed-sublevel certificate
  checking, including infeasibility, repeated fine keys, zero prices, and
  allowed/required splits. Resource limits return unknown. Proved NP-completeness
  for the explicit finite budget problem, already on acyclic input graphs.
- Added all-edge covering simulation, transfer of abstract lower bounds and
  matching concrete witnesses, and invariant-guided refinement that eliminates
  a whole false policy. Every quotient, invariant, certificate and strict
  partition refinement can be independently checked.
- Added the coupled guarded model with 12 stages and 32 opportunity slots.
  Repair, block arrival and quorum-enabled timeouts share actual protocol state.
  The complete mutant has 2,516 states and 5,856 transitions. Refinement eliminates
  11 policies and proves optimum 2 on 26 abstract states; the witness passes all
  12 guarded replay audits and gives conflicting unmutated observer decisions.
- Added separate 7,904-case and 2,960-case oracle studies, with zero mismatches.
  The latter checks both optimizers and all 6,857 abstraction iterations. The
  128-policy protocol audit compares guarded exploration with the corresponding
  exported diagnostic-field quotient, using shared protocol rules.
- Connected the old structural solver to the general semantics by an explicit
  event-state adapter, equal-optimum proof and 1,507-case raw-oracle study.
  All 3,014 optimum comparisons and 1,189 witness normalizations pass.
- Added general Lean policy, memory, certificate, simulation and invariant
  proofs. The integrated gate now has 15 build jobs, 46 audited declarations
  and 23 hygiene-checked source files, with independent kernel rechecking.
- Expanded the active Python suite to 119 passing tests and integrated the
  transition studies into reproduction and CI. Reorganized the article around
  six main theorems; the PDF has 12 main-text and 24 physical pages. Updated
  literature positioning, claim/evidence links and both reviewer reports.

## Second revision — certifying synthesis, 2026-10-19 (d502ce0)

- Reframed the manuscript around minimum-cost phase refinement, with an exact
  weighted four-role characterization, unequal nonnegative costs, and
  allowed/required keys. The earlier prescribed-set capacity formula is retained
  as a starting lemma, not re-labelled as a new discovery.
- Added component-wise synthesis, quota dynamic programming, complete legal
  model witnesses and independently checked optimality/infeasibility certificates.
  Explicit resource limits return unknown. Verification and optimization retain
  their exponential local and pseudo-polynomial quota dependence.
- Proved non-submodularity and an unbounded approximation ratio for the specified
  immediate-gain-per-cost heuristic; repeated two-cycle motifs give optimum 20
  versus heuristic cost 1000.
- Added two independent raw-event oracle suites: 35,223 and 3,253 optimum and
  certificate comparisons, with zero mismatches; 103,460 prescribed-set checks.
  Saved all 13 solved certificates in a 15-case structural study up to 48 pivots.
- Mechanized the full graph/event-order equivalence, finite schedule construction
  and cover-edge bridge, plus the Bellman lower-bound and infeasibility principle.
  The integrated Lean build passes 14 jobs, a 27-declaration axiom audit and
  independent kernel rechecking; source hygiene covers 22 Lean files.
- Added unchanged native CometBFT conformance: four scenarios, fourteen checks,
  thirty-two native Ed25519 votes, actual quorum/timeouts and normal commits.
  An independent signature/metadata audit, three repeated runs and one
  race-detector run pass. This does not reproduce the local model's mutation.
- Added twelve synthesis tests, bringing the active Python suite to 47 passing
  tests; integrated all new evidence stages into one-command reproduction and
  a dedicated GitHub Actions workflow. Native raw timestamps are retained and
  audited, while deterministic summaries/certificates are byte-compared.
- Updated the manuscript, evidence ledger, formal maps, reviewer response and
  Russian research report; added current primary-source positioning against
  adaptive distributed-system testing and established certifying algorithms.

## First reviewer revision — 2026-10-19 (8007cef)

- Corrected the one-pivot separation theorem with explicit persistence,
  first-vote necessity, observation coverage, and repair before the second
  signature. Added an arbitrary-contract Lean theorem and a missing-persistence
  counterexample.
- Added the exact repair-frontier characterization for independent initially
  ready pivots over finite opportunity partial orders. Derived the unit-weight
  minimum phase budget, the weighted attainable-subset condition, and the
  declared schema's decision-complexity result. Credited the classical
  reversible-set and graph arguments used in the proofs.
- Added an independent guarded-event evaluator and finite checks covering
  530 repair graphs, 219 labelled four-event partial orders, 44 common-deadline
  domains, and 258 weighted domains. The graph suite executes 1,357,209
  policy/split runs and checks 13,074 reachability boundaries and 13,074 minimum
  budgets without a mismatch.
- Added 12 concrete four-validator executions, 14 dedicated tests, and 8
  frontier tests, bringing the active Python total to 35. The new trace records
  actual signed envelopes, local certificates, nil votes, legal timeouts, and
  late-repair controls, including a separately declared relay case that passes
  the admitted-vote FIFO audit.
- Pinned the new source fixture to CometBFT v0.39.3 commit
  `49b82838fcca442b2445f76605c101609ed04130`, preserving source bytes, Git blob
  identities, SHA-256 manifests, and the Apache-2.0 license. Retained the older
  v0.40.0 fixture with its original version identity.
- Integrated the new Lean module: 12 build jobs, 20 audited declarations, and
  successful kernel-object rechecking. Documented that graph correspondence
  and the concrete protocol transition model remain outside the mechanized
  proof. Retained the old Python/Go results as terminal-classification evidence.
- Pinned the SMT runtime through the uv-locked `z3-solver==4.13.3.0` wheel;
  all 8 expected UNSAT and 4 expected SAT controls pass.
- Added the `./reproduce_revision.sh` alias for the expanded `./reproduce.sh`
  pipeline and Pandoc-based Markdown/LaTeX synchronization. Deterministic data
  use byte comparisons; PDF checks cover successful build, page budget,
  diagnostics, and embedded fonts instead of requiring identical bytes across
  TeX engines. The revised PDF has 17 physical pages and 13 main-text pages.
- Added a Russian revision report, an English response to reviewer points
  7.1–7.4, and an updated claim-to-evidence account. No production-client
  vulnerability, full transition refinement, or acceptance guarantee is claimed.

## 1.0.0-reproducible — 2026-08-22

- Consolidated immutable historical inputs into a canonical active tree.
- Repaired and built the primary Lean 4.33 formalization with an axiom audit.
- Added cross-language bounded-model checks, SMT, and certificate controls.
- Revised the scientific statements, evidence ledger, and related-work matrix.
- Added an official LIPIcs v2021.1.3 build and final PDF.
- Added isolated one-command reproduction, CI, manifests, and release packaging.
