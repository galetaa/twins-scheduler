# Submission-Level Proof Assurance Blocker

**Gate 8′ status:** blocking for submission, non-blocking for manuscript review.

## Evidence already completed

- Project-local induction certificates for T1, T2, and T3, checked by a small dependency-free kernel.
- Five positive SMT/CHC encodings with eight expected `UNSAT` outcomes.
- Four damaged encodings with expected `SAT` outcomes.
- Exact Go `math/big` arithmetic for 1,028 T3 cases.
- Exhaustive 128-assignment T6 check.
- Independent Go/Python operational validation and event-order sensitivity.
- Explicit trusted-computing-base statement in `proofs_checked/TRUSTED_COMPUTING_BASE.md`.

These routes substantially reduce ordinary implementation error. They do **not** eliminate the possibility that the same paper-level statement was translated incorrectly into the certificate kernel, SMT formulas, and executable model.

## Lean status

The artifact contains a Lean scaffold pinned to `v4.33.0`. The official Lean release record dates Lean 4.33.0 to 10 August 2026. In the current execution environment, `lean`, `lake`, and `elan` were not installed. The attempted `lake build` therefore exited with status 127. The exact record is `formal/lean/BUILD_ATTEMPT_2026-08-17.md`.

The correct interpretation is:

> The Lean development was not kernel-checked in this environment. Its presence is not evidence that it compiles, nor evidence that it fails logically.

## Two acceptable closure routes

### Route A — mature proof-assistant build

1. Install the pinned Lean 4.33.0 toolchain through the official distribution.
2. From `formal/lean/`, run `lake build` in a clean environment.
3. Record `lean --version`, `lake --version`, operating system, and complete build output.
4. Reject any unapproved `sorry`, `axiom`, `admit`, `unsafe` theorem shortcut, or imported inconsistent axiom.
5. Add theorem-to-paper mapping for T1, T2, T3, and T6.
6. Add negative compilation or theorem controls where technically meaningful.
7. Archive source hashes and build logs in the submission artifact.
8. Re-run the full Gate 8 reproduction and update the claim ledger.

Acceptance criterion: the pinned kernel accepts all claimed theorems from a clean checkout, with no unreviewed axioms or placeholders, and an independent reader confirms the theorem statements match the manuscript.

### Route B — independent specialist review

1. A named researcher with distributed-algorithms/formal-methods competence reviews every definition, theorem, proof, and model mapping.
2. The reviewer records objections and resolutions in a dated ledger.
3. At least one counterexample search is performed against each theorem’s omitted-premise boundary.
4. The reviewer explicitly confirms that T3 is existential, T2 is conditional, and T6 is model-specific.
5. The final manuscript incorporates all corrections and links each theorem to reviewed evidence.

Acceptance criterion: no unresolved major objection and a signed or attributable review record suitable for the authors’ internal archive.

## Submission decision

Until Route A or Route B is completed, the correct label is:

**MANUSCRIPT COMPLETE — SUBMISSION HOLD.**

This blocker does not assert that the theorem is wrong. It records that current assurance is not yet strong enough for an external publication claim framed around formal results.
