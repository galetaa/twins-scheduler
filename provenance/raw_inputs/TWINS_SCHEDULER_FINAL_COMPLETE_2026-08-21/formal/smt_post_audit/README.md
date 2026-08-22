# Post-audit SMT obligations

These files re-encode the corrected paper obligations independently of the historical Gate 7 encodings.

Expected outcomes:

- every file in `positive/` is `unsat`;
- every file in `negative_controls/` is `sat`.

The positive T1 files are the one-step obligations used by the structural replay-erasure induction; the full finite induction is checked by the independent script and project-local proof kernel. T2 is split into its inserted-action, retained-action, and upward-unsafety verification conditions. T3 encodes the complete bounded Boolean directed-policy domain and exact quorum arithmetic. T6 encodes the operational equation and exact three-pattern boundary.

Z3 is an external mature SMT solver, but these results are not described as a Lean/Coq kernel proof.
