# Roadmap — Gate 8′: manuscript and submission-readiness review

## Gate objective

Turn the frozen Gate 7′ claim and generated evidence into a complete paper while
preventing scope inflation. Gate 8′ is complete only when every scientific
sentence is mapped to evidence or explicitly labeled as interpretation,
limitation, or future work.

## WP8.1 Full manuscript construction — 4–7 focused person-days

Write the complete paper from `manuscript/PAPER_SKELETON.md`. Keep the order:
problem and observation language, closure theorem, separation construction,
exact premise boundary, replay theorem, executable validation, related work,
validity, reproducibility.

**Acceptance:** no section depends on an unstated theorem or result file.

## WP8.2 Claim-to-evidence audit — 1–2 days

For every abstract, introduction, contribution, and conclusion sentence, record
its evidence path in `manuscript/EVIDENCE_INDEX.md`. Check all quantities against
machine-readable files and retain all prohibited claims from Table 7.

**Acceptance:** every load-bearing claim has a proof, exact result, source, or
explicit inference label.

## WP8.3 Proof assurance closure — 2–5 days

Complete independent human proof review or successfully build a kernel-checked
Lean/Coq/Isabelle development. Resolve every objection and rerun the artifact if
a statement or premise changes.

**Acceptance:** no blocking proof objection remains; exact tool output and hashes
are archived.

## WP8.4 Related-work and novelty refresh — 2–4 days

Refresh communication closure, message adversaries, BFT testing frameworks,
refinement/conformance, and mutation/fuzzing literature as of the submission
date. Search specifications, dissertations, repositories, and issue discussions
for the same phase-erasure/pivot result.

**Acceptance:** the novelty statement remains narrow, dated, source-bounded, and
survives a reviewer-style kill test.

## WP8.5 Venue adaptation and artifact appendix — 2–3 days

Select a plausible audience only after the completed contribution is visible.
Adapt terminology, page budget, proof placement, artifact appendix, and
responsible-disclosure language without changing the claim.

**Acceptance:** manuscript and artifact satisfy the chosen venue's current
format and evaluation requirements; no venue suitability is treated as a
guarantee of acceptance.

## Gate decision rules

**PASS / submission-ready:** complete manuscript, no unresolved proof objection,
current novelty audit, all figures/tables generated, artifact cleanly
reproduced, and claim-to-evidence audit passes.

**PIVOT:** proof review narrows T2 or T3 but leaves a nontrivial, independently
validated separation result.

**NO-GO:** the theorem encoding is materially wrong, a newly found source already
contains the same mechanism and result, or the paper requires a broader claim
than the artifact supports.

## Critical path

`proof assurance closure → full manuscript → claim audit → novelty refresh →
venue adaptation → submission-readiness decision`.
