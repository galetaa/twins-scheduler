# Expected outputs

Run `./reproduce_revision.sh` from the repository root. It delegates to
`./reproduce.sh`, whose mandatory stages include the new concrete-trace and
repair-frontier runners. The run writes an isolated output tree and reports its
location in `build_logs/reproduction_summary.log` within that tree. Paths below
are relative to that output root unless identified as repository documentation.

## Required checks

| Check | Required result | Canonical evidence |
| --- | --- | --- |
| Python | 35 tests pass: 13 retained, 8 frontier, 14 concrete | `build_logs/python_tests.log` |
| Go | all active packages pass | `build_logs/go_tests.log` |
| Python/Go classifier | identical 384-row observations from the retained model | `results/generated/cometbft_cross_language_check.txt` |
| Independent checks | PASS | `results/generated/independent_proof_checks.json` |
| Certificate kernels | originals accepted; tampered controls rejected | `results/generated/certificate_verification.json` |
| SMT | 8 expected UNSAT; 4 expected SAT; Z3 wheel pinned to 4.13.3.0 | `results/generated/smt_summary.json` |
| Lean build | 12 jobs; exit 0 | `build_logs/lean_build.log` |
| Axiom audit | 20 declarations; only documented standard axioms; exit 0 | `build_logs/lean_axiom_audit.log` |
| Kernel-object rechecking | `leanchecker SchedulerClosure` exits 0 | `build_logs/leanchecker.log` |
| Source hygiene | PASS | `results/generated/formal_source_hygiene.json` |
| Frontier enumeration | PASS; zero mismatches | `results/revision/frontier_summary.json` |
| Concrete trace | 12 cases; all legality audits pass | `results/new/concrete_trace.json` and `.csv` |
| Markdown/LaTeX | both generated source pairs agree | `build_logs/manuscript_consistency.log` |
| LIPIcs | build passes; main text at most 15 pages | `build_logs/lipics_page_budget.log` |
| PDF diagnostics | no overfull boxes or undefined references/citations; no BibTeX warnings; fonts embedded | `build_logs/lipics_warnings.log` and build checks |
| Data references | manifest hashes and byte comparisons pass | repository manifest and `build_logs/result_comparison.log` |

The current verified PDF has **17 physical pages**: one cover page, 13 main-text
pages, one reference page, and two appendix pages. Its overfull-box,
undefined-reference, undefined-citation, and BibTeX-warning counts are zero;
all fonts are embedded. The build uses the checksum-verified official LIPIcs
class and records actual engine versions. A documented class fallback is not
an unresolved citation, layout overflow, or build failure.

The Z3 runtime comes from the uv-locked `z3-solver==4.13.3.0` wheel. The
SAT cases are intentionally damaged obligations or negative controls; their
expected SAT results are successful checks, not proof failures.

## Exact frontier counts

The canonical summary is `results/revision/frontier_summary.json`. Its counts
must agree with the following finite scopes; `mismatch_count` is zero.

| Sweep | Domains and orders | Executions | Comparisons |
| --- | --- | --- | --- |
| General graphs | 530 directed graphs with loops for $k=1,2,3$; 50,363 linear extensions | 1,357,209 policy/split executions | 13,074 boundary; 13,074 minimum budget; 4,164 joint lateness |
| Four-event orders | All 219 labelled partial orders on two repairs and two vote opportunities; 960 linear extensions | 3,840 admission executions | 3,504 boundary; 876 joint lateness |
| Common deadline | 44 domains for $k=1,\ldots,8$; all forced-repair counts | 174,250 executions at barrier representatives | 2,636 boundary |
| Weighted common deadline | 258 domains, up to three pivots with weights in $\{1,2,3\}$ | 1,884 admissions at extremal late orders | 15,700 boundary |

The general graph suite varies both admission and split choices and checks all
deficit pairs from zero through $k+1$. The four-event suite supplies cover edges
to test extraction of **transitive** repair precedence, including paths through
suppressed slots. Full order enumeration applies to those two suites. Common
and weighted sweeps use the stated representatives and must not be described as
all event permutations.

The supporting case tables are `frontier_graph_cases.csv`,
`frontier_common_cases.csv`, and `frontier_weighted_cases.csv` in
`results/revision/`. Three explicit controls must retain their outcomes:

- Crossed deadlines: each repair can be late separately, but the two cannot be
  late together; $\alpha(H)=1$, and one split suffices for deficits $2,2$.
- Repair after the second signature and before its collector: the signed output
  persists, so the supplied execution remains unsafe.
- Weights $2,2$, deficits $1,3$, and no late repair: coarse unsafety is false,
  although the incorrect continuous total-capacity test would accept it.

## Concrete execution counts

The 12 traces comprise six canonical policy cases, four direct timing controls,
and two separate relay controls. Six execute the baseline and six the mutant.
All six baseline traces remain safe in this matrix. The mutant fine-policy trace
and late-precommit controls expose disagreement at the unmutated observers.

The canonical cases and relay controls pass the scoped FIFO audit for admitted
vote envelopes. The direct late-precommit control is diagnosed as non-FIFO;
that diagnosis is an expected result. The full interpretation and exact
environmental choices are in the repository's
[concrete-trace explanation](../research/CONCRETE_TRACE.md).

## Assurance and reproducibility interpretation

The new Lean declarations check an arbitrary one-pivot behavioral contract,
capacity and budget arithmetic, a weighted interval retaining attainable
weights, and a small persistent-output machine. Graph reversal, graph-to-execution
correspondence, and optimal graph-capacity attainment remain paper proofs with
finite cross-checks. The 20-declaration axiom audit does not turn those separate
arguments or the concrete protocol model into mechanized refinements. The
repository's [axiom report](../../formal/lean/AXIOM_REPORT.md) and
[claim ledger](../CLAIM_EVIDENCE_LEDGER.md) give the mapping.

Deterministic result files listed by the verification script are compared
byte-for-byte with committed references. Source manifests check exact fixture
identity, including both separately identified CometBFT snapshots. The PDF is
checked for successful regeneration, source synchronization, the page budget,
diagnostics, and embedded fonts. **An identical PDF SHA-256 across different
TeX engines is not required.** Logs may contain runtime durations, cache details,
and tool-version information, so their entire bytes are not scientific result
references. A run is complete only after every mandatory stage succeeds and the
reproduction summary records PASS.
