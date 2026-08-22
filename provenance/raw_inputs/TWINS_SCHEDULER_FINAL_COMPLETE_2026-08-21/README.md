# Scheduler-closure research project: final complete revision

**Artifact date:** 21 August 2026  
**Paper:** *Phase Erasure Can Hide Agreement-Violation Witnesses in Certificate-Driven Locking BFT Protocols*

This directory is the final revision layer of the research project. It closes the scientific and presentation issues in the independent review, adds a bounded rule-level instantiation to the published CometBFT/Tendermint locking rules, and preserves all evidence needed to reproduce the available checks.

## One-command reproduction

From this directory:

```bash
./reproduce.sh
```

The command executes:

1. an independent checker that does not import the project models;
2. the Python bounded CometBFT/Tendermint instantiation;
3. an independently written Go instantiation and cross-language comparison;
4. focused pytest checks;
5. the project-local proof-certificate kernel with five damaged controls;
6. twelve Z3 obligations and controls;
7. source-hygiene checks for the Lean and Coq developments;
8. the A4 review-PDF build;
9. Lean, Coq, and official LIPIcs builds when their external toolchains are installed.

A successful run in the verified environment ends with:

```text
T1 replay erasure with output congruence   PASS
T2 legal relational closure               PASS
structural quorum-pivot criterion          PASS
parametric P_f/B_f family                  PASS
diagnostic seven-premise boundary          PASS
bounded CometBFT rule-level refinement     PASS
negative controls                          PASS
final reproduction                         PASS_WITH_EXPLICIT_EXTERNAL_BLOCKERS
```

The final line records two environment-dependent checks that were not executable here: a mature Lean/Coq kernel build and an official `lipics-v2021.cls` build. Their source trees and CI/build instructions are included, but their presence is not represented as a successful build.

## Main deliverables

- `manuscript/FULL_MANUSCRIPT_FINAL_2026-08-21.md` — final paper source;
- `manuscript/TWINS_SCHEDULER_FINAL_MANUSCRIPT_2026-08-21.pdf` — rendered and visually checked A4 review PDF;
- `manuscript/lipics/` — official-class LIPIcs source tree;
- `formal/lean/` — pinned Lean 4 development and axiom-audit entry point;
- `formal/coq/` — parallel Coq source retained from the post-audit stage;
- `protocol_instantiation/COMETBFT_V0393_MAPPING.md` — bounded rule-level refinement map;
- `src/cometbft_bounded.py` and `go/cometbft_refinement/` — independent executable instantiations;
- `proof_review/final_independent_checks.py` — independent finite checker;
- `prior_art/PRIOR_ART_UPDATE_2026-08-21.md` — refreshed prior-art and novelty review;
- `REVIEWER_COMPLETION_MATRIX.md` — item-by-item closure of the review;
- `results/final/` — decisive machine-readable results and reproduction log.

## Scientific status

The scientific revision is complete in the deliberately bounded scope:

> For an explicit finite class of certificate-driven locking schemas, erasing phase labels to one type-uniform directed edge can remove an agreement-violation witness because closure-added repair evidence disables a unique correct quorum pivot. Exact replay preserves relevant state and output traces only under state and output congruence, projected duplicate stutter, and duplicate-output silence.

The CometBFT/Tendermint bridge is a **bounded rule-level refinement of the published rules**, not production-client conformance and not a claim of a vulnerability.

## Submission status

**CONDITIONAL PASS / COMPLETE SCIENTIFIC REVISION / SUBMISSION HOLD.**

Before submission, execute one mature-prover build with an axiom report and compile the supplied official-class LIPIcs source with the current Dagstuhl package. Author metadata and a final same-day literature refresh also remain author-side submission tasks.

## Historical completeness

The final distribution also contains `history/`:

- `history/original_inputs/` preserves the brief, first-pass analysis, independent topic audit, initial specification, and reviewer recommendations;
- `history/stage_archives/` preserves every original ZIP package from the initial specification through Gate 8′ and the first post-audit revision;
- `history/expanded/complete_project_2026-08-20/` is the exact expanded earlier all-stage archive;
- `history/expanded/post_audit_final_2026-08-20/` is the exact expanded first post-audit layer.

The files at the archive root are authoritative when a historical claim, theorem statement, implementation, or status conflicts with a later revision.
