# Final completion report

## 1. Scope of this completion pass

This pass implements the remaining recommendations from the independent review of the post-audit manuscript. It does not invent a new topic. It strengthens the existing phase-erasure result and connects it to a natural protocol rule vocabulary while preserving the bounded, falsifiable scope.

## 2. Reviewer-requested scientific changes

### 2.1 Natural Tendermint/CometBFT instantiation

A new bounded transition system is pinned to the published CometBFT `v0.39.3` consensus rules. The mapping is explicit at the rule level: PoLC-completing prevote, persistent lock update, precommit quorum, and commit/height advancement. The shared scheduler edge is fixed by sender, receiver, height, and round; only the phase differs.

The baseline and the single controlled mutation `MISSING_LOCK_UPDATE` are evaluated under three policies. For every checked `f`:

- the baseline is safe under phase-specific, directed-edge-off, and directed-edge-on policies;
- the mutation is unsafe only when the phase-specific policy admits the enabling prevote and rejects the repair precommit;
- both type-uniform directed choices are safe.

The executable evidence is intentionally bounded and is presented as a refinement of published rules, not production conformance.

### 2.2 Structural separation theorem

The paper now separates three levels:

1. a general relational sufficient condition for unsafety preservation by legal closure;
2. a structural quorum-pivot separation criterion for any bounded system satisfying explicit enabling, repair, timing, necessity, and scheduler-coupling premises;
3. a `3f+1`, quorum-`2f+1` family as a corollary.

The diagnostic seven-flag characterization is no longer positioned as the central theorem.

### 2.3 Replay theorem

The replay theorem now has two congruence premises:

- equal relevant projections induce equal next relevant projections;
- equal relevant projections induce equal protocol-relevant output for every retained event.

Marked duplicates must be projected stutters and produce an empty relevant output. The theorem consequently preserves both final projection and the entire relevant output trace. The `X,X,Y` hidden-state counterexample remains as the necessity boundary.

### 2.4 Exact definitions

The final manuscript and formal source include:

- `Unsafe` as a predicate on terminal protocol state;
- `UnsafeObs` as observations of unsafe terminal states;
- directed and phase-sensitive admission relations;
- existential type closure;
- stable-filter delivery with no synthesis, inherited order, and once-only delivery;
- an explicit requirement that closure creates a legal target-language execution;
- the exact `P_f,B_f` bounded domain;
- the operational Boolean equation and a paper derivation of its closed form.

### 2.5 Paper presentation

The main text uses ordinary theorem numbering only. Internal artifact identifiers are moved to `formal/lean/ARTIFACT_THEOREM_MAP.md`. Contributions are reordered around the quorum-pivot mechanism, repeated disclaimers are consolidated, replay is secondary, and a compact related-work capability table is included.

## 3. Independent and executable evidence

### 3.1 Independent checker

`proof_review/final_independent_checks.py` imports none of the project models, SMT encodings, certificate kernel, or prover sources. It reports:

- exact scheduler closure with no synthesis, stable order, and once-only delivery;
- typed unsafe-observation construction;
- 84 valid legal-closure finite models with no counterexample;
- the structural criterion for 64 quorum sizes;
- 768 bounded CometBFT bridge cases for `f=1..128`;
- the replay hidden-state counterexample and positive state/output congruence cases.

### 3.2 Dual protocol instantiations

The Python and Go implementations independently generate 384 rows each for `f=1..64`, two variants, and three scheduler policies. The terminal rows are identical.

### 3.3 Project-local kernel

Kernel version 1.1.0 checks:

- 96 finite replay models and 12,096 finite traces;
- 32 closure models and 8,256 merged prefixes;
- both directed-domain cases and five arithmetic parameters;
- all 128 seven-premise assignments;
- five damaged controls, all rejected.

This route is an executed small trusted checker, not a substitute for an externally maintained proof assistant.

### 3.4 SMT

Z3 4.13.3.0 returns `UNSAT` for eight positive obligations and `SAT` for four deliberately weakened controls.

### 3.5 Mature prover source

The Lean development is pinned to Lean `v4.33.0`, contains a `lakefile.toml`, an axiom-audit entry point, and a GitHub Actions workflow using `leanprover/lean-action@v1` with no-sorry checks. A parallel Coq source tree is retained. Source hygiene passes, but neither compiler existed in the verified environment, and no mature-kernel build is claimed.

## 4. Prior art and novelty

The search was refreshed through 21 August 2026 across academic papers, specifications, open code, and recent testing/formalization work. The comparison matrix distinguishes scheduler controls from property-preserving closure and from an explicit safety separation witness.

The surviving claim is limited to the combined result:

> legal relational closure conditions, a structural repair-disables-pivot separation criterion, its parametric family and bounded Tendermint-style instantiation, and an output-aware replay-erasure boundary.

Directed graphs, phase filters, replay, Twins, fault-injection APIs, benchmark infrastructure, and a new mutation campaign are not claimed as novel.

## 5. Manuscript and typesetting

The final manuscript is about 4,800 words and contains:

- exact scheduler semantics;
- typed observations;
- three central theorems with paper proofs;
- the bounded CometBFT/Tendermint bridge;
- evidence and assurance boundaries;
- a related-work capability matrix;
- consolidated limitations and an AI-use disclosure draft.

The A4 review PDF builds without blocking LaTeX warnings and is rendered for visual inspection. The official-class source tree uses `lipics-v2021`, `plainurl`, PDF figures, anonymous metadata, and a separate cover. The class file itself was unavailable locally, so an official-class PDF is not claimed.

## 6. Reproducibility

`./reproduce.sh` is the single entry point. It regenerates all decisive machine-readable results and the review PDF. Missing external proof or class toolchains are printed as `NOT_RUN`, never converted into `PASS`. Setting `STRICT_MATURE_PROVER=1` makes a missing Lean toolchain fatal.

## 7. Final verdict

| Dimension | Verdict |
|---|---|
| Scientific mechanism | PASS |
| Structural theorem | PASS |
| Parametric family and exact bounded domain | PASS |
| Natural protocol rule-level bridge | PASS, bounded |
| Replay correction | PASS |
| Independent executable evidence | PASS |
| Prior-art refresh | CONDITIONAL PASS |
| Mature Lean/Coq kernel build | NOT RUN |
| Review PDF | PASS |
| Official LIPIcs-class PDF | NOT RUN |
| Overall | **CONDITIONAL PASS / COMPLETE SCIENTIFIC REVISION / SUBMISSION HOLD** |
