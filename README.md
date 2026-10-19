# Certifying Minimum-Cost Phase Refinements for BFT Testing

This repository contains the manuscript, mathematical proofs, executable
synthesis procedure, independent certificate checker, and reproducible
experiments for **minimum-cost phase control in an explicit BFT-testing
schema**.

The procedure chooses which admission keys must distinguish voting phases,
constructs a legal model witness, and supplies evidence that no cheaper choice
works. Unequal vote weights, nonnegative control costs, unavailable keys and
already-required keys are supported. The input contract must be supplied and
justified for the protocol under test.

- [Current LIPIcs manuscript](manuscript/pdf/final_lipics_manuscript.pdf)
- [Russian revision report](docs/reviews/REVISION_REPORT_RU.md)
- [Response to reviewer](docs/reviews/RESPONSE_TO_REVIEWER.md)
- [Synthesis specification and proofs](docs/research/REFINEMENT_SYNTHESIS.md)
- [Claim-to-evidence ledger](docs/CLAIM_EVIDENCE_LEDGER.md)

## Central result

A repair message can prevent a prospective conflicting signature; it cannot
withdraw one already issued and available to its collector. For each pivot
$i$, let $R_i$ be its repair opportunity and $V_i$ its second-vote opportunity.
Build the repair graph from transitive precedence in the **complete** event
order, including suppressed slots:

$$
i\to j\iff R_i\prec V_j.
$$

The graph describes which contributors can remain jointly reusable. A chosen
split set $S$ admits a witness exactly when the pivot identities have a
partition $I=S\mathbin{\dot\cup}J\mathbin{\dot\cup}X\mathbin{\dot\cup}Y$ with

$$
H[J]\text{ acyclic},\qquad
w(S\cup J\cup X)\ge d_0,\qquad
w(S\cup J\cup Y)\ge d_1.
$$

Here $d_0,d_1$ are certificate deficits. Split keys $S$ and unsplit reusable
keys $J$ contribute to both branches. Open keys $X$ guarantee first support;
closed, initially ready keys $Y$ provide second support. Additional second
votes from $X$ are harmless. Costs are minimized over allowed and required
split choices.

The algorithm enumerates local choices in strongly connected components and
uses a two-quota dynamic program. It then constructs the complete event order.
A separate checker verifies every local Bellman lower-bound inequality and
replays the witness. Matching its cost to the lower bound proves optimality;
an infinite lower bound proves infeasibility. A resource limit returns
**unknown**, not infeasible. Verification remains exponential in the largest
remaining SCC and pseudo-polynomial in integer quota values.

The earlier unit-weight capacity and minimum-cardinality results are retained:

$$
\text{coarse witness}\iff
\max(d_0,d_1)\le k\ \land\ d_0+d_1\le k+\alpha(H),
\qquad
t_* = \max(0,d_0+d_1-k-\alpha(H)).
$$

Here $\alpha(H)$ is the maximum induced-acyclic cardinality. The prescribed-set
formula $|S|+\alpha(H[I\setminus S])$ already belonged to the first revision.
The second revision adds weighted cost synthesis, key restrictions, constructive
certificates, graph/order mechanization, and native conformance evidence.

### A reason to optimize combinations

For two directed cycles $0\leftrightarrow1$ and $0\leftrightarrow2$, unit vote
weights and full quotas, splitting either leaf alone has zero immediate benefit.
Splitting both leaves works. With costs $(M,1,1)$ and $M>2$, a rule that maximizes
immediate capacity gain per cost chooses the center for $M$, although the
optimum is 2. The ratio $M/2$ is unbounded. This proves non-submodularity and
failure of that specific myopic rule; it is not a claim about all heuristics.

## Use the certifying synthesizer

```bash
uv sync --frozen
uv run python scripts/run_refinement_synthesis.py \
  --input results/synthesis/examples/bow_tie_cost.input.json \
  --output .cache/bow_tie_certificate.json
uv run python scripts/run_refinement_synthesis.py \
  --verify .cache/bow_tie_certificate.json \
  --expect-input results/synthesis/examples/bow_tie_cost.input.json
```

The example's certified optimum is 2. [Five input fixtures](results/synthesis/examples/)
cover the cost counterexample, crossed deadlines, indivisible weights, and
one-pivot signature timing. These fixtures are abstract model inputs.

## Evidence obtained

| Evidence | Result and scope |
| --- | --- |
| Active Python tests | **47 pass**: 35 retained and 12 synthesis tests |
| Main independent synthesis oracle | **35,223** weighted optimum/certificate comparisons; **103,460** prescribed-split checks; zero mismatches |
| Separate arbitrary-order oracle | **3,253** optimum/certificate comparisons on 48 six-event DAGs; zero mismatches |
| Structural synthesis study | **13 certified optima** among 15 synthetic cases, up to **48 pivots**; 2 explicit SCC-size cutoffs return unknown |
| Retained frontier validation | 530 repair graphs, all 219 labelled four-event partial orders, 44 common-deadline and 258 weighted domains |
| Guarded protocol model | 12 baseline/mutant/timing/relay cases with complete legality audits |
| Unchanged native CometBFT | **4 scenarios, 14 checks, 32 native Ed25519 votes, 132 events**; independent signature audit passes |
| Native repeated execution | 3 additional normal runs preserve semantic outcomes; 1 race-detector run passes |
| Lean 4.33.0 | **14 build jobs, 27 audited declarations, 22 source files**; independent kernel rechecking passes |
| Retained supporting checks | Go tests and 384-row Python/Go classifier comparison; 8 expected UNSAT and 4 expected SAT SMT controls |

The two synthesis oracles obtain outcomes from raw permutations and admissions,
without deriving their observations from the repair graph or capacity formula.
The graph-based oracle's 1,357,209 executions belong to one declared schema;
they are not independent protocol instances or a bug-prevalence measurement.
Complete [synthesis results](results/synthesis/) include all 13 scale proofs.

### Formal and implementation scope

[GraphRealization.lean](formal/lean/SchedulerClosure/GraphRealization.lean)
proves the graph-reversal equivalence and constructs an injective event schedule
from finite acyclicity, including input given as cover edges.
[CertificateOptimality.lean](formal/lean/SchedulerClosure/CertificateOptimality.lean)
proves the Bellman lower-bound, minimum-witness and infeasibility rules for
arbitrary nonnegative-cost paths. Neither module assumes an optimal capacity
or an optimally computed potential table.

The full weighted behavioral correspondence and Python checker implementation
are not mechanized. The concrete model has no Lean transition refinement of
CometBFT. [Native conformance](experiments/native_cometbft/) separately executes
unchanged CometBFT v0.39.3 at commit
`49b82838fcca442b2445f76605c101609ed04130`, with pinned Go 1.25.0, native signing,
locking, proposer priority, actual timeout guards and ordinary commits. It
uses synchronous dispatch, test keys and in-memory fixtures. It does not
reproduce the model's mutation or exercise a production network.

## Reproduce all reported checks

Prerequisites are Python 3.11–3.13, uv 0.6.14, Go 1.24 or later with toolchain
selection, Pandoc, Git, curl, a C compiler, pdfTeX/BibTeX, Poppler commands and
`dpkg-deb`. The native runner selects Go 1.25.0. Lean and the pinned TeX overlay
are installed into the project cache; the Python lock pins Z3 and the independent
native signature-audit dependencies. Empty caches require network downloads.

```bash
./reproduce_revision.sh
```

The mandatory pipeline runs the retained checks, both frontier/model runners,
the new synthesis study and separate oracle, unchanged native conformance,
independent signature audit, three additional normal runs and one race-detector
run, the Lean build/audit/rechecking, and the official LIPIcs build. It stops on
failure. Individual stages are available through `make test`, `make formal`,
`make synthesis`, `make native`, and `make paper`.

Each reproduction uses an isolated output tree. Deterministic data, including
synthesis certificates and the native semantic summary, are compared against
committed references. Native wall-clock timestamps, signatures and raw receipts
are revalidated for that execution. PDF gates check source synchronization,
main text at most **15 pages**, warnings and font embedding; they do not require
identical PDF bytes across TeX engines. See [expected outputs](docs/reproduction/EXPECTED_OUTPUTS.md)
and [container reproduction](containers/README.md).

## Repository guide

- [Manuscript](manuscript/): Markdown, official LIPIcs source, figures and PDF.
- [Synthesis](src/python/twins_scheduler/refinement_synthesis.py),
  [frontier model](src/python/twins_scheduler/repair_frontier.py), and
  [guarded trace](src/python/twins_scheduler/concrete_trace.py).
- [Synthesis results](results/synthesis/), [native evidence](results/native/),
  [frontier tables](results/revision/), and [model traces](results/new/).
- [Formal proof map](formal/lean/ARTIFACT_THEOREM_MAP.md) and
  [axiom report](formal/lean/AXIOM_REPORT.md).
- [Source fixtures](models/tendermint_style/) preserve exact v0.39.3 bytes
  and separately identified historical v0.40.0 material.
- [Limitations](docs/LIMITATIONS.md),
  [literature audit](docs/research/LITERATURE_AND_PROVENANCE_AUDIT.md), and
  [provenance](provenance/PROVENANCE.md).

Original code and documentation use the MIT license. Third-party materials
retain the terms in [third-party notices](THIRD_PARTY_NOTICES.md).
