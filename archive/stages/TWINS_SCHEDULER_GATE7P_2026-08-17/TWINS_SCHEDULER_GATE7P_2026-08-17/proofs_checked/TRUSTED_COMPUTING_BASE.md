# Trusted computing base for the Gate 6′ checked proofs

## Purpose

Gate 6′ uses a deliberately small, dependency-free proof-certificate checker for
three narrow obligations. It makes the assumptions, rule applications,
well-founded measures, and exact arithmetic visible in versioned files. It is
not presented as a replacement for Lean, Coq, Isabelle, or independent proof
review.

## Trusted components

1. CPython's execution of `src/schedcheck/gate6/proof_kernel.py`.
2. The 503-line proof kernel itself, SHA-256 recorded in
   `results/gate6p/proof_kernel_report.json`.
3. The semantic validity of the named Horn rules in `t1_rules.json` and
   `t2_rules.json`.
4. The standard well-founded induction principle over natural numbers.
5. Exact integer/rational arithmetic used by the polynomial normalizer.
6. The explicit mapping from the T3 branch fields to the protocol-schema
   premises.

The proof kernel has no runtime package dependency outside the Python standard
library. It rejects unknown rules, missing premises, malformed or circular
one-step rules, mismatched conclusions, unsupported polynomial syntax, invalid
arithmetic equalities, and malformed T3 branches.

## What is checked

- Every T1 and T2 derivation step cites a declared rule whose premises are
  already available.
- The base case and induction step are separately derived.
- The step certificate contains an explicit strictly decreasing natural-number
  measure fact.
- The theorem is not allowed to appear among premises or definitions.
- T3 polynomial identities are normalized exactly rather than tested at a
  finite sample of integers.
- Both directed branches and the phase-specific branch are checked against the
  declared quorum and base-support expressions.

## What remains trusted rather than mechanically derived

The kernel does not encode a dependent type theory. In particular, it trusts
that each named rule correctly represents the mathematical statement described
in the accompanying proof document. Consequently, the assurance is stronger
than an unchecked prose sketch and weaker than a mature proof-assistant kernel.

Before submission, the recommended final hardening is either:

- independent line-by-line proof review by a distributed-systems/formal-methods
  specialist; or
- migration of T1–T3 to a mature prover without changing their statements.

No theorem in the package is labelled as a fully mechanized Lean/Coq/Isabelle
result.
