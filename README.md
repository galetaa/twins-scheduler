# Certified Minimum-Cost Scheduler Refinement for Stateful BFT Testing

## Completed seven-validator and editorial revision

Named author: **Mikhail Alexandrovich Galeta**, SUAI, Saint Petersburg.
The [author PDF](manuscript/pdf/final_lipics_manuscript.pdf) and
[anonymous review PDF](manuscript/pdf/review_lipics_manuscript.pdf) are built
from the same source. Both state **not nominated** for the student award;
this does not assert ineligibility. [Metadata rationale](docs/reviews/AUTHOR_METADATA.md).

The new [seven-validator study](docs/research/SCALED_PROTOCOL.md) has six coupled
control fibres, 48,201 states and 55,283 edges. Its unit-price optimum is two;
nine false-policy eliminations precede a 562-state quotient. The full work
accounting shows no speedup over direct search. Run `make scaled` or the full
`./reproduce_revision.sh`. The [reviewer matrix](docs/reviews/REVIEWER_COMPLETION_MATRIX.md)
is generated from the current claim ledger and checked for drift.


This repository contains a research manuscript, Lean proofs, executable optimizers,
independent certificate checkers and reproducible experiments for selecting the
cheapest scheduler phase distinctions that expose a finite agreement violation.

**The general optimality result now applies to arbitrary protocol transition
systems under a declared static admission interface.** It permits dependent
quorums, shared locking state, changing message availability, repeated messages,
branching and cycles. Independent pivots remain a structural specialization.

- [Current LIPIcs manuscript](manuscript/pdf/final_lipics_manuscript.pdf)
- [Russian revision report](docs/reviews/REVISION_REPORT_RU.md)
- [Response to reviewer](docs/reviews/RESPONSE_TO_REVIEWER.md)
- [General transition synthesis](docs/research/TRANSITION_SYNTHESIS.md)
- [Certified abstraction and policy refinement](docs/research/TRANSITION_ABSTRACTION.md)
- [Coupled guarded protocol model](docs/research/COUPLED_PROTOCOL_MODEL.md)
- [Claim-to-evidence ledger](docs/CLAIM_EVIDENCE_LEDGER.md)

## The general result

A fine key identifies a persistent Boolean admission decision. Fine keys are
grouped into coarse fibres, such as one transport peer/view key with several
message phases. An unsplit fibre uses one shared bit. Paying to split it permits
different bits at its fine keys. Repeated uses of the **same fine key must still
agree**, even after splitting.

For a legal execution `t`, let `Mix(t)` contain each coarse fibre on which both
admission values occur. If the trace is consistent on every fine key, its least
required refinement is exactly

\[
T_t=Q\cup\operatorname{Mix}(t),
\]

where `Q` is the required split set. It is feasible precisely when that union is
allowed. Nonnegative integer costs are counted **once per fibre**. This theorem
constructs a complete static policy for unobserved keys as well as observed ones.
It makes no independence or quorum-additivity assumption.

The exact solver explores `(protocol state, persistent partial policy)`. All
stateful behavior is retained in the protocol transition relation. A certificate
contains an unsafe path and a safe set closed under every input-derived successor
below the claimed price. A separate checker regenerates those successors and
replays the path. Missing certificate successors are rejected relative to the
complete bound input; completeness of that input remains a coverage obligation.
Full closure certifies infeasibility; resource limits return **unknown**.

The explicit product can have `|states| * 3^|fine keys|` states. The decision problem
is NP-complete even for acyclic graphs with two fine keys per fibre; the artifact
includes a checked Set Cover reduction. The method is exact, not polynomial-time.

## From an abstract optimum to concrete-model optimality

A checked state map must preserve initial states, controlled labels and unsafe
states, and cover **every concrete input transition**. Internal transitions may
stutter; a controlled admission cannot disappear. Then

\[
\operatorname{Opt}(\text{abstract})\le\operatorname{Opt}(\text{concrete}).
\]

A certified abstract lower bound plus an actual concrete witness of the same
price proves the concrete-model optimum. The abstraction need not realize every
abstract path. A spurious abstract witness supplies only a lower bound.

The implemented abstraction-refinement loop starts with a state partition,
optimizes its existential quotient, and explores the concrete graph under the
returned **total fixed policy**. A successful concrete witness closes the bound.
Otherwise its safe reachable-state invariant splits the partition and eliminates
that entire false policy. Each failed iteration strictly adds a state group.
The complete history is independently checked, including every intermediate
certificate and invariant; the checker does not invoke optimization.

### Stateful quorum experiment

The guarded model has two controlled fibres affecting the **same** local quorum,
actual signed vote sets, locks, valid blocks, timeout guards and missing-block
commit waiting. Its complete environment is one height, two rounds, 12 stages,
and 32 once-only opportunity slots, with every within-stage permutation.
Unsafety requires unmutated observers `A,C` to disagree; only replica `P` has the
explicit missing-lock model defect.

| Case | Complete concrete graph | Final quotient | Certified result |
|---|---:|---:|---|
| Missing-lock model, abstraction starts at one group | 2,516 states / 5,856 edges | 26 states / 60 edges | Cost **2**, after 11 false policies eliminated |
| Missing-lock model, audit-field projection | 2,516 / 5,856 | 1,978 / 4,628 | Cost **2**, one iteration |
| Baseline with persistent locking | 2,372 / 5,574 | 1 state | No unsafe execution in the declared environment |

Costs are `B->P=5` and `A->P=2`. The optimal witness separates `A->P`; its proposal
and enabling prevote remain admitted while the repair precommit is withheld.
With only `B->P` refinable the optimum is 5; requiring both costs 7; forbidding
all splits is infeasible. The optimized witness replays 30 opportunities and ends
with `A=0,C=1`; all 12 protocol audits pass. Its detailed execution contains
172 events, 16 signed model messages and six local certificates.

The same fixed policy has safe and unsafe orders because an attempted timeout
must actually have been enabled by a received quorum. A separate control enters
commit-wait after round change and finishes only when a genuinely emitted
`A->P` block arrives. The BLOCK phase is included in the control interface.

These are bounded rule-model results. The state-abstraction algorithm still
constructs the complete concrete graph before reducing its product search.
The audit-field projection removes a diagnostic first-arrival field; its ratio
is not a production-client compression claim.

## Run the tools

```bash
uv sync --frozen

# All general transition, protocol, abstraction and specialization studies.
make transition

# Direct synthesis for an explicit finite input model.
uv run python scripts/run_transition_synthesis.py \
  --input model.json --output certificate.json.gz
uv run python scripts/run_transition_synthesis.py \
  --verify certificate.json.gz --expect-input model.json

# Automatic abstraction refinement for the same model.
uv run python scripts/run_transition_bridge.py \
  --input model.json --output abstraction.json.gz
uv run python scripts/run_transition_bridge.py \
  --verify abstraction.json.gz --expect-input model.json
```

An embedded hash identifies the embedded problem. Use `--expect-input` to bind
verification to an independently supplied expected model. JSON input format and
Python API examples are in [the synthesis specification](docs/research/TRANSITION_SYNTHESIS.md).
Ready-to-use protocol and semantic inputs are under [results/transition](results/transition/).

## Evidence and assurance

| Evidence | Result and scope |
|---|---|
| General finite-LTS oracle | **7,904** graph/cost/permission cases, zero optimum mismatches |
| Direct plus abstraction oracle | **2,960** instances, **5,920** optimum comparisons and **6,857** certificates across all abstraction iterations, zero mismatches |
| Coupled-model export audit | **128** total-policy explorations regenerate guarded successors; all reachable state/edge counts agree with the exported quotient omitting the same first-arrival diagnostic |
| Abstraction showcase | 9 complete runs; 32 checked iterations; 23 false policies eliminated |
| Lean 4.33.0 | **46** selected audited declarations, 15 build jobs, independent kernel rechecking |
| Structural synthesis oracles | **35,223 + 3,253** optimum certificates; **103,460** prescribed-split checks; zero mismatches |
| Structural scale study | 13 certified optima among 15 cases, up to 48 pivots; two explicit component cutoffs return unknown |
| Retained guarded trace controls | 12 baseline, mutation, timing and relay executions with legality audits |
| Unchanged native CometBFT | 4 ordinary-operation scenarios, 14 checks, 32 Ed25519 votes, 132 events; independent signature audit |
| Native repeatability | Three further normal runs and one race-detector run pass |
| Retained cross-language/SMT checks | Go tests, 384-row Python/Go classifier agreement, eight expected UNSAT and four expected SAT controls |

The 2,960-case corpus includes the 2,048 graph-family and 512 Set Cover cases also
exercised by unit tests; those executions are not additional independent models.
None of the synthetic counts measure bug prevalence or the number of distinct
BFT protocols.

[TransitionRefinement.lean](formal/lean/SchedulerClosure/TransitionRefinement.lean)
proves static-policy completion, least trace refinement, exact memory query
guards, closed-set certificates, local labelled simulation, concrete bound
transfer and invariant-guided policy elimination. Its semantic theorems do not
assume finite protocol state or independent pivots.

The Python implementation and protocol exporter are separately tested, not
extracted from Lean. Applying the semantic theorem to arbitrary client code
requires a faithful control-labelled model or a proved covering simulation.
The current all-edge checker establishes a finite **model-to-model** bridge.
Native conformance executes unchanged CometBFT v0.39.3 at commit
`49b82838fcca442b2445f76605c101609ed04130` with real signing and consensus guards;
it does not reproduce the model defect or establish universal client refinement.

## Structured repair-graph specialization

For the independent-pivot behavioral contract, define a repair graph by
`i -> j` exactly when transitive opportunity precedence forces `R_i < V_j`.
Its maximum induced-acyclic cardinality `alpha(H)` gives the unit-weight boundary
and, when all splits are allowed, none required, and fine feasibility
`max(d0,d1) <= k` holds, the exact unit split budget:

\[
\text{coarse unsafe}\iff\max(d_0,d_1)\le k\ \land\ d_0+d_1\le k+\alpha(H),
\qquad t_*=\max(0,d_0+d_1-k-\alpha(H)).
\]

Weighted support, allowed/required keys and unequal costs use four-role
assignments, SCC decomposition and a two-quota dynamic program. Bellman
certificates independently check every local alternative and a concrete event
replay. The new explicit transition adapter and cross-check connect this
specialization to the general solver. See [the structural specification](docs/research/REFINEMENT_SYNTHESIS.md).

The refinement value is not submodular. For two cycles sharing a central vertex,
leaf costs 1 and central cost `M > 2`, an immediate-positive-gain-per-cost rule pays
`M` while the optimum is 2. This particular heuristic has unbounded ratio `M/2`.
The saved 30-pivot motif instance gives 1000 versus optimum 20.

```bash
uv run python scripts/run_refinement_synthesis.py \
  --input results/synthesis/examples/bow_tie_cost.input.json \
  --output .cache/bow_tie_certificate.json
uv run python scripts/run_refinement_synthesis.py \
  --verify .cache/bow_tie_certificate.json \
  --expect-input results/synthesis/examples/bow_tie_cost.input.json
```

## Full reproduction

```bash
./reproduce_revision.sh
```

Prerequisites include Python 3.11–3.13, uv 0.6.14, Go with toolchain selection,
Pandoc, Git, curl, a C compiler, pdfTeX/BibTeX, Poppler and `dpkg-deb`. The native
runner selects Go 1.25.0. Lean and the pinned TeX overlay are installed in the
project cache; empty caches require network downloads.

The mandatory pipeline stops on failure. It runs all general and structural
studies, guarded protocol checks, native/signature/repeatability checks, Lean
build/audit/rechecking and the official LIPIcs build. Individual stages are
`make test`, `make formal`, `make transition`, `make synthesis`, `make native`,
and `make paper`.

Each full reproduction uses an isolated output tree. Deterministic results,
including gzip certificates, are compared byte-for-byte. Native raw signatures
and timestamps are revalidated; their semantic summary is byte-compared. PDF
gates enforce source synchronization, at most **15 main-text pages**, no unresolved
citations/overfull boxes, and embedded fonts. Cross-engine PDF byte identity is
not promised. See [expected outputs](docs/reproduction/EXPECTED_OUTPUTS.md),
[limitations](docs/LIMITATIONS.md), [formal assurance map](formal/lean/ARTIFACT_THEOREM_MAP.md)
and [container reproduction](containers/README.md).
