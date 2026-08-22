# Executive decision — post-audit finalization

## Decision

**CONDITIONAL PASS / COMPLETE POST-AUDIT REVISION / SUBMISSION HOLD.**

Every mathematical correction requested by the independent proof audit is implemented in the formal sources, manuscript, independent checker, external SMT obligations, and executed project-local proof-certificate kernel:

- T1 now uses an explicit relevant-state projection, transition congruence, projected duplicate stutter, silent relevant output, and includes the `X,X,Y` hidden-state counterexample;
- T2 exposes the prefix simulation invariant and all four preservation premises;
- T3 now defines a complete bounded transition system: `E` and `R` share sender, receiver, and view, the phase order is `E<C0<R<C1`, the directed domain is exactly one Boolean edge bit, and unsafety is defined by conflicting decisions of distinct correct replicas;
- T6 includes the operational `U(e,r)` equation, the strict-separation predicate, the closed form, and the exact three assignments.

## Executed evidence

- independent checker: **PASS**;
- project-local proof-certificate kernel: **PASS**;
- damaged project-kernel controls rejected: **4/4**;
- post-audit Z3 obligations: **8 UNSAT positive obligations, 4 SAT negative controls**;
- inherited Gate 8 reproduction: **PASS**;
- revised review PDF: **PASS**, 17 physical A4 pages;
- main narrative after cover: physical pages 2--15, **14 pages**;
- bibliography begins on physical page 16;
- appendix begins on physical page 17;
- blocking LaTeX warnings in the review build: **0**;
- visual PDF inspection: **PASS**.

## Remaining external blockers

The archive contains parallel Lean and Coq developments with source-hygiene checks, but the execution environment did not contain Lean/Lake/Elan or Coq/Coqchk and direct downloads were blocked. These sources are therefore **not claimed as mature-prover kernel-built**.

The archive also contains a complete `lipics-v2021` source tree, but the official class was unavailable locally. The supplied PDF is an A4 review build, **not an official LIPIcs-class PDF**.

Submission should remain on hold until:

```text
Lean or Coq clean kernel build: PASS
axiom/assumption audit in that prover: PASS
official lipics-v2021 build: PASS
```

The scientific result survives the audit; the remaining conditions concern external proof and typesetting infrastructure, not unresolved conceptual design.
