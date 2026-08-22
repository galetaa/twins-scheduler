# Post-audit finalization report

## 1. Scope

This stage repairs the missing post-audit layer of the scheduler-closure project. Historical gates remain immutable for provenance. The new layer supplies revised theorem statements, executable checks, formal sources, an updated novelty review, a corrected manuscript, an A4 review PDF, and official-class LIPIcs source.

## 2. Audit correction matrix

| Theorem | Audit defect | Repair | Evidence |
|---|---|---|---|
| T1 replay erasure | Future noninterference was informal; immediate projected stutter allowed a hidden-state counterexample | Added projection congruence for every future event, projected duplicate stutter, silent relevant output, processed stable keys in the projection, and the exact `X,X,Y` counterexample | Lean/Coq source, independent checker, project kernel, 2 Z3 UNSAT VCs, SAT hidden-state control, manuscript §6 |
| T2 closure lifting | Prefix notation and retained/inserted step obligations needed clarification | Made the consumed-action prefix invariant, transitivity, insertion monotonicity, forward simulation, and upward-closed unsafety explicit | Independent 2-state prefix enumeration, project-kernel induction, 3 Z3 UNSAT VCs, manuscript §3 |
| T3 quorum-pivot separation | Same view, phase order, bounded domain, and decisions were implicit | Defined envelopes with equal endpoint and view, fixed `E<C0<R<C1`, represented all directed policies by `Bool`, and added irreversible correct decisions | Lean/Coq operational source, independent bounded model, project kernel, symbolic Z3 theorem, two SAT damaged controls, manuscript §4 |
| T6 premise boundary | Operational Boolean equation was absent from the article | Added `U(e,r)`, `Strict`, the closed form, and exact assignments | Lean/Coq source, independent 128-case enumeration, project kernel, 2 Z3 UNSAT checks, SAT damaged control, manuscript §5 |

The detailed mapping is in `proof_review/INDEPENDENT_AUDIT_INTEGRATION.md`.

## 3. Formal-assurance result

### 3.1 Independent executable checker

The checker is independent of the historical project kernels and author SMT models. It reports:

- T1 hidden-state counterexample reproduced: full projection `1`, erased projection `0`;
- T2 finite relational models: 6;
- T2 prefix/trace cases: 1,260;
- T2 counterexamples under all premises: 0;
- T3 same endpoint/view and fixed phase order: PASS;
- T3 phase-specific unsafe, directed off/on safe: PASS;
- T3 arithmetic checked for five parameters including a 400-digit integer;
- T6 assignments: 128, exact patterns: `0111111`, `1101111`, `1111111`, mismatches: 0.

### 3.2 Executed project-local proof-certificate kernel

The dependency-free kernel performs structural proof checks rather than accepting theorem labels. It reports:

- T1 finite trace checks: 504;
- T2 finite prefix checks: 972;
- T3 directed cases: 2 and parameter cases: 5;
- T6 assignments: 128;
- damaged controls rejected: 4/4.

This is an executed kernel local to the project. It is not described as a Lean, Coq, Isabelle, or externally maintained proof-assistant kernel.

### 3.3 External SMT route

Z3 4.13.3 checks twelve new post-audit files:

- 8 positive obligations return `unsat`;
- 4 deliberately damaged controls return `sat`.

These obligations are separate from the historical Gate 7 encodings.

### 3.4 Mature-prover source

Parallel Lean and Coq developments are included and contain no `sorry`, `admit`, `Admitted`, explicit new `axiom` declarations, or unsafe theorem definitions. Their toolchains were unavailable, so no mature-prover build or axiom report is claimed. Exact probe logs are preserved.

## 4. Updated prior art

The novelty review was refreshed on 20 August 2026 across academic and engineering sources covering Twins, communication closure, Heard-Of/message adversaries, VLSM, ByzzFuzz, Netrix, ByzzBench, PERF, ByzTwin-Range, `relab/hotstuff`, and CometBFT.

The remaining novelty claim is narrow:

> For a fully bounded certificate-driven locking schema, erasing phase labels to one type-uniform endpoint edge can insert repair evidence that disables a unique correct quorum pivot and thereby remove a finite agreement-violation witness; the exact premise boundary is characterized operationally, while replay erasure requires projection congruence in addition to duplicate stutter.

The project does not claim novelty for scheduler APIs, directed graphs, replay, Twins, message filtering, fault-injector composition, benchmarks, or production vulnerabilities.

## 5. Manuscript and LIPIcs conversion

The revised English manuscript incorporates every audit correction. The A4 review build has:

- 17 physical pages;
- anonymous cover on page 1;
- 14 pages of main narrative on physical pages 2--15;
- bibliography beginning on physical page 16;
- appendix beginning on physical page 17;
- 0 overfull boxes, undefined citations, or undefined references;
- embedded fonts and no encryption;
- visual inspection of cover, theorem pages, final main page, bibliography, and appendix.

A complete official-class tree is available under `manuscript/lipics`. The environment lacked `lipics-v2021.cls`, so its build attempt is preserved as a blocker. The supplied PDF must be called a review PDF, not an official LIPIcs build.

## 6. Reproducibility

`./scripts/reproduce_post_audit.sh` reruns:

1. the independent checker;
2. the project-local proof kernel;
3. every post-audit Z3 obligation and damaged control;
4. source-hygiene checks;
5. the A4 review PDF build when Pandoc and XeLaTeX are present;
6. PDF metadata and warning checks;
7. the official-class probe;
8. deterministic checksum validation when the stage manifest has been generated.

The complete all-stage archive additionally preserves the original historical ZIPs and expanded copies from Gate 0 through Gate 8.

## 7. Final status

**Scientific correction status: PASS.**

**Independent executable assurance: PASS.**

**Project-local kernel: PASS.**

**External SMT: PASS.**

**Mature Lean/Coq kernel build: NOT RUN — toolchain unavailable.**

**Review PDF: PASS.**

**Official LIPIcs-class build: NOT RUN/FAILED BEFORE COMPILATION — class unavailable.**

**Overall: CONDITIONAL PASS / SUBMISSION HOLD.**
