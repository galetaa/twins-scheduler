# Gate 8′ — Manuscript and Submission-Readiness Report

**Date:** 17 August 2026  
**Topic:** Safety-observation closure boundaries of scheduler grammars for certificate-driven locking BFT protocols  
**Paper title:** *Phase Erasure Can Hide Agreement-Violation Witnesses in Certificate-Driven Locking BFT Protocols*

# 1. Executive decision

**Status: CONDITIONAL PASS / MANUSCRIPT COMPLETE / SUBMISSION HOLD.**

Gate 8′ has closed the manuscript-construction gap. A complete anonymous English paper, working PDF, related-work refresh, sentence-level evidence ledger, venue plan, reviewer-objection matrix, AI disclosure, and artifact appendix now exist. No additional conceptual protocol design is required before external review.

Submission is not authorized yet. The decisive blocker is independent proof assurance: the current routes are solver-checked and independently executable, but no mature proof-assistant kernel build or external human proof review has been completed. Three secondary pre-submission tasks remain: refresh prior art on the actual submission date, review the natural-protocol assumption map with a specialist, and compile under the official LIPIcs A4 class.

# 2. Frozen contribution package

## 2.1 T2 — relational closure lifting

If closure-added actions are increasing under a preorder, retained actions forward-simulate that preorder, and `Unsafe` is upward-closed, then inserting closure-required actions preserves finite unsafety. This is a conditional theorem; a protocol instantiation must supply a non-vacuous preorder.

## 2.2 T3 — parametric quorum-pivot separation

For every `f≥1`, with `n=3f+1` and `q=2f+1`, the supplied schema has a unique honest pivot shared by two conflicting quorums. Phase-specific delivery can admit enabling evidence `E` and omit repair evidence `R`; type-uniform directed delivery must admit both or neither. Edge-off leaves the first branch at `q−1`; edge-on lets repair disable the pivot, leaving the second branch at `q−1`.

## 2.3 T6 — exact premise boundary

For the seven-flag abstraction, strict separation holds exactly under:

```text
S2 ∧ D ∧ T ∧ E_d ∧ X ∧ (S1 ∨ R_q)
```

The only strict bit patterns are `0111111`, `1101111`, and `1111111`.

## 2.4 T1 — replay erasure

Exact replay adds no state-based safety-observation power when duplicate processing is a stable-key stutter that emits no relevant output, adds no voting power, and cannot affect later protocol behavior. Counting message instances provides the complementary controlled counterexample.

# 3. Manuscript package

The manuscript contains:

- explicit definitions for protocol state, safety observation, scheduler grammars, and closure operators;
- theorem statements and proof ideas for T1/T2/T3/T6;
- executable validation and negative controls;
- a prior-art section that disclaims API/DSL novelty;
- internal, construct, external, conclusion, and proof-assurance limitations;
- responsible-security nonclaims;
- one-command artifact instructions;
- an AI-use disclosure draft.

The Markdown source has approximately 6,683 prose words. The working PDF has 17 physical A4 pages: one cover page, 15 numbered manuscript pages, and reference continuation. It is a review template, not the official LIPIcs layout.

# 4. Claim-to-evidence audit

Thirty load-bearing claims were audited. Every central theorem, executable result, prior-art assertion, limitation, and nonclaim has a named evidence path. The ledger distinguishes `PASS`, conditional theorem status, search-limited novelty, and proof-assurance limitations.

The audit found no unsupported central empirical number. It did identify the same publication blocker as Gate 7′: T1–T3 are not yet kernel-checked in a mature proof assistant and have not been independently reviewed by a human specialist.

# 5. Prior art and novelty

The refresh covers Twins, communication closure, closed message adversaries, Heard-Of, randomized BFT testing, Netrix, ByzzBench, HotStuff, partial synchrony, CometBFT and relab harness sources, and the 2026 PERF formal fault-injection framework.

The prior art destroys any claim to a new scheduler API, directed graph model, replay mechanism, or formal fault injector. The defensible novelty delta is narrower: a property-preserving closure question for phase erasure, a repair-disabled honest-pivot separation, an exact premise boundary, and a stable-key replay boundary.

No inspected source through 17 August 2026 was found to combine all four. This is a search-limited statement, not proof of absolute novelty.

# 6. Natural protocol relevance

CometBFT- and HotStuff-style protocols motivate phase-labelled certificates, persistent locks, and later evidence that can restrict future support. Standard quorum arithmetic permits two minimal quorums whose only correct intersection identity is a pivot.

What is not established is equally important: the artifact does not prove that one production protocol exposes the exact `E/R` same-edge pattern, repair timing, absence of replacement contributors, and controlled defective transition required by T3. The production mapping is therefore conditional. No vulnerability is alleged.

# 7. Proof assurance

Completed assurance routes:

- project-local checked induction certificates;
- independent SMT/CHC encodings;
- eight positive `UNSAT` outcomes;
- four damaged `SAT` controls;
- exact Go big-integer arithmetic for 1,028 cases;
- 128 exact premise assignments;
- independent Go/Python event-loop correspondence;
- 1,548 event-order sensitivity runs;
- two bounded exact-kernel routes in the nested Gate 5 archive.

Unclosed assurance route:

- Lean 4.33.0 scaffold exists, but `lean`, `lake`, and `elan` were unavailable; `lake build` was not executed successfully.

The final acceptable routes are a clean kernel-checked development with statement mapping or an independent, attributable human proof review with an objection ledger.

# 8. Venue readiness

OPODIS 2026 is the primary current candidate, not a guaranteed fit. Its scope matches the theory/practice combination. The call requires anonymous English A4 LIPIcs submissions, a separate cover, no more than 15 pages excluding cover/references/appendices, and disclosure of substantial AI use. The working manuscript is organized around those constraints, but official LIPIcs compilation remains mandatory.

# 9. Artifact readiness

The Gate 7 core route remains offline and deterministic. Gate 8 adds:

- the complete manuscript and PDF;
- the sentence-level claim ledger;
- the venue and novelty documents;
- the proof blocker record;
- the nested reproducible Gate 5 exact-kernel archive;
- a Gate 8 validator and one-command runner;
- a complete Gate 8 checksum manifest.

The local archive is evaluation-ready in structure but has no public DOI or venue-specific container yet.

# 10. Safety and responsible use

All schedules and mutations execute locally. The package makes no network contact with public validators, transfers no assets, accesses no private keys, and performs no denial of service. The paper disclaims production vulnerabilities and withholds exploit framing. An unexpected client-level issue discovered later must be privately reproduced, minimized, and responsibly disclosed before sensitive details are made public.

# 11. Gate status

| Work package | Status | Blocking action |
|---|---|---|
| WP8.1 Complete connected manuscript | PASS | none |
| WP8.2 Sentence-level claim audit | PASS | none |
| WP8.3 Submission-level proof assurance | **FAIL / BLOCKING** | independent review or kernel-checked development |
| WP8.4 Prior-art refresh | CONDITIONAL PASS | repeat immediately before submission |
| WP8.5 Natural protocol mapping | CONDITIONAL PASS | specialist construct-validity review |
| WP8.6 Venue/artifact adaptation | PASS WITH FORMAT RECHECK | official LIPIcs conversion |
| WP8.7 Final submission decision | **SUBMISSION HOLD** | all blockers above must close |

# 12. Final verdict

**Gate 8′ is complete as a manuscript-construction stage. The research package is ready for external proof review, not for submission.**

The next irreversible step is proof assurance, not feature development.
