# Gate 7′ proof assurance report

## Assurance verdict

**Sufficient for Gate 8′ manuscript construction; insufficient for final
submission without an additional independent review route.**

The Gate 6′ blocker was dependence on a project-local proof checker. Gate 7′
adds a mature, independently implemented SMT/CHC route using Z3 4.13.3.0 and
falsifying controls. This materially reduces implementation risk, but does not
eliminate specification or abstraction risk.

## Discharged obligations

### T1 — replay erasure

A constrained Horn-clause encoding checks that finite-prefix equality cannot be
violated when first deliveries use the same deterministic transition and
subsequent deliveries with the same stable key are protocol-relevant stutters.
The damaged non-stuttering control is satisfiable.

### T2 — relational closure lifting

Four first-order verification conditions check transitivity, increasing
insertions, forward simulation, and upward closure. A separate Horn query checks
the finite-prefix invariant skeleton. The generic induction composition is also
checked by the small explicit certificate kernel. A damaged insertion that is
not increasing is satisfiable.

### T3 — quorum-pivot separation

Quantifier-free linear integer arithmetic checks the symbolic identities and
both directed branches for every integer `f≥1`, with `n=3f+1` and `q=2f+1`.
Independent Go `math/big` code checks 1,028 values, including a 400-digit value.
A damaged model in which repair does not disable the pivot is satisfiable.

### T6 — exact premise boundary

The operational seven-flag construction and the Boolean formula

```text
S2 ∧ D ∧ T ∧ E ∧ X ∧ (S1 ∨ Rq)
```

are symbolically equivalent in Z3. The dependency-free checker independently
evaluates all 128 assignments and finds exactly three strict patterns:
`0111111`, `1101111`, and `1111111`. Dropping the `Rq` disjunct yields a
satisfiable counterexample.

## Solver results

- five positive SMT/CHC source files;
- eight positive `UNSAT` results in total;
- four negative-control files;
- four expected `SAT` results;
- zero `unknown`, parsing errors, or unexpected results.

The complete source/output digests are in
`proof_outputs/smt_proof_report.json`.

## Independent executable routes

The proof package is complemented by:

1. a small auditable certificate checker;
2. exact Go big-integer arithmetic;
3. a fuller Go event loop;
4. an independently written Python event-loop mirror;
5. FIFO, LIFO, and 256 seeded random queue-order checks.

These routes do not share implementation code, but they do share a written
specification and can therefore share a modeling error.

## Trusted computing base

- Z3 4.13.3.0;
- five positive SMT-LIB files and four negative controls;
- the statement-to-symbol interpretation;
- the minimal Z3 C-API loader;
- the host C compiler and dynamic loader;
- the project-local T2 induction certificate checker;
- the abstract protocol/schema specification.

## Lean 4 scaffold

`formal/lean/` pins Lean 4.33.0 and contains proposed direct statements of
T1–T3. Lean, Elan, and Lake were not installed in the verified environment, so
these files were not kernel-checked. They are excluded from the evidence used
for the Gate 7′ PASS decision.

## Remaining submission blocker

Complete either:

- independent line-by-line review by a formal-methods/distributed-systems
  specialist, with an objection ledger and signed-off corrections; or
- a successful kernel-checked development in Lean, Coq, or Isabelle, including
  recorded toolchain hashes and build output.

A mature-solver `UNSAT` result is strong evidence for the encoded obligations;
it is not a substitute for reviewing whether the encoding exactly matches every
paper-level premise.
