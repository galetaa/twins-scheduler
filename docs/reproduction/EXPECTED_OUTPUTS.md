# Expected outputs

Run `./reproduce_revision.sh` from the repository root. It delegates to
`./reproduce.sh`, whose mandatory stages include the concrete-trace and
repair-frontier runners, the complete minimum-cost synthesis study, the separate
arbitrary-order oracle, native conformance with an independent signature audit,
and three additional native repetitions plus one race-detector run. The run
writes an isolated output tree and reports its
location in `build_logs/reproduction_summary.log` within that tree. Paths below
are relative to that output root unless identified as repository documentation.

## Required checks

| Check | Required result | Canonical evidence |
| --- | --- | --- |
| Python | all active tests pass; exact count in the test log | `build_logs/python_tests.log` |
| Go | all active packages pass | `build_logs/go_tests.log` |
| Python/Go classifier | identical 384-row observations from the retained model | `results/generated/cometbft_cross_language_check.txt` |
| Independent checks | PASS | `results/generated/independent_proof_checks.json` |
| Certificate kernels | originals accepted; tampered controls rejected | `results/generated/certificate_verification.json` |
| SMT | 8 expected UNSAT; 4 expected SAT; Z3 wheel pinned to 4.13.3.0 | `results/generated/smt_summary.json` |
| Lean build | 15 jobs; exit 0 | `build_logs/lean_build.log` |
| Axiom audit | 46 declarations; only documented standard axioms; exit 0 | `build_logs/lean_axiom_audit.log` |
| Kernel-object rechecking | `leanchecker SchedulerClosure` exits 0 | `build_logs/leanchecker.log` |
| Source hygiene | 23 source files; PASS | `results/generated/formal_source_hygiene.json` |
| Frontier enumeration | PASS; zero mismatches | `results/revision/frontier_summary.json` |
| Concrete trace | 12 cases; all legality audits pass | `results/new/concrete_trace.json` and `.csv` |
| Synthesis study | 35,223 minimum-cost/infeasibility comparisons and certificate checks; no mismatches | `results/synthesis/synthesis_summary.json` |
| Independent event-order oracle | 3,253 further comparisons and certificate checks; no mismatches | `results/synthesis/order_oracle.json` |
| Synthetic scale corpus | 15 cases: 13 certified optima, 2 expected resource-limited unknowns; largest solved $k=48$ | `results/synthesis/synthesis_benchmarks.csv` |
| General transition oracle | 7,904 graph/cost/permission cases, zero mismatches | `results/transition/summary.json` |
| Coupled exporter | 128 direct total-policy runs; all counts match the corresponding audit-field quotient | `results/transition/direct_policy_checks.csv` |
| Transition abstraction | 9 cases, 32 verified iterations; model-to-model optimality/infeasibility checks | `results/transition_bridge/bridge_summary.json` |
| Independent direct/CEGAR oracle | 2,960 instances, 5,920 optimum comparisons, zero mismatches | `results/transition_bridge/random_oracle.json` |
| Structural specialization | general LTS adapter and old weighted solver agree | `results/transition_bridge/specialization_oracle.json` |
| Unchanged native consensus | 4 passing scenarios, 14 checks, 32 signed votes, 132 events; Go 1.25.0 | `results/native/native_summary.json` and `native_provenance.json` |
| Independent native signature audit | all 32 Ed25519 signatures and canonical vote metadata verified; PASS | `results/native/native_signature_audit.json` |
| Native repeatability | 3 additional normal runs and 1 race-detector run pass; semantic summaries agree | `results/native/native_repeatability.json` |
| Markdown/LaTeX | both generated source pairs agree | `build_logs/manuscript_consistency.log` |
| LIPIcs | build passes; main text at most 15 pages | `build_logs/lipics_page_budget.log` |
| PDF diagnostics | no overfull boxes or undefined references/citations; no BibTeX warnings; fonts embedded | `build_logs/lipics_warnings.log` and build checks |
| Data references | manifest hashes and byte comparisons pass | repository manifest and `build_logs/result_comparison.log` |

The PDF must satisfy the **15-page main-text limit**. Actual main-text and physical
page counts are recorded for each build in `build_logs/lipics_page_budget.log`;
counts from an earlier manuscript revision are not the acceptance criterion.
Overfull-box, undefined-reference, undefined-citation, and BibTeX-warning counts
must be zero, and all fonts must be embedded. The build uses the checksum-verified
official LIPIcs class and records actual engine versions. A documented class
fallback is not an unresolved citation, layout overflow, or build failure.

The Z3 runtime comes from the uv-locked `z3-solver==4.13.3.0` wheel. The
SAT cases are intentionally damaged obligations or negative controls; their
expected SAT results are successful checks, not proof failures.


## General transition and abstraction results

`make transition` runs the complete general-LTS study, coupled guarded protocol,
iterative abstraction, independent total-policy/subset oracle, and explicit
pivot-to-LTS specialization cross-check. All outputs in `results/transition/`
and `results/transition_bridge/`, including compressed full certificates, are
deterministic. Timings are written only to `TWINS_LOG_DIR`.

The coupled mutant has **2,516 states, 5,856 transitions, 16 unsafe states**;
the baseline has **2,372 states, 5,574 transitions, no unsafe states**. Unsafety
requires A,C disagreement. The language has one height, two rounds, 12 stages
and 32 opportunity slots, every within-stage order, and actual block catchup.
Costs 5 and 2 give optimum 2 when both fibres are allowed, 5 with only B allowed,
2 with only A allowed, 5 with B required, and 7 when both are required. Forbidding
all splits and the baseline model are infeasible in this exact environment.
The optimal guarded execution has 172 log events, 16 signed model messages,
six local certificates and 12 passing audits. Its A,C decisions are 0 and 1.

The 128 direct policy runs regenerate **17,690 reachable states and 42,750
transitions** in total from protocol guards. Those totals count repeated
per-policy explorations, not distinct global states. Every count and unsafe
classification matches the exported quotient after forgetting the same
first-arrival diagnostic field, independently of the optimizer. The direct
exploration loop shares the protocol guards and canonicalization.

The coarsest-start abstraction run has **12 iterations**, eliminates **11**
false policies, and finishes with **26 states and 60 edges**. The abstract bound
is 0 in iterations 1–4 and 2 thereafter; only the final iteration obtains a
concrete witness. Every one of the 5,856 concrete edges is checked for transition
coverage. A diagnostic-field projection gives 1,978 states / 4,628 edges and
optimum 2 immediately. Baseline infeasibility transfers from its one-group
quotient because the complete baseline graph has no unsafe state.

The independent 2,960-instance oracle includes 400 seeded LTSs, the 2,048-case
edge/cost/constraint family, and 512 Set Cover reductions. It checks direct and
abstraction-based optima separately (5,920 comparisons), every direct certificate,
and 6,857 certificates across all abstraction iterations. There are zero mismatches.
The same 2,048 and 512 families in unit tests are not additional independent
samples. The other general-LTS study has 7,904 graph/cost/permission cases and
six explicit semantic boundaries. Generator bounds, seeds and input hashes are
saved with each report.

Lean's new `TransitionRefinement.lean` proves policy completion, least trace
refinement, persistent-memory guards, strict-sublevel certificates, local
labelled simulation, bound transfer and invariant-guided quotient refinement.
Finite explicit enumeration and Python/exporter implementations remain separate
executable obligations. The whole project has 46 selected audited declarations;
source-bound command receipts are regenerated by the formal gate.

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

## Exact synthesis and certificate counts

`scripts/run_refinement_synthesis.py --study` produces the primary study in
`results/synthesis/`. It independently enumerates raw orders and admission modes
before comparing the optimizer's returned costs and certificates.

| Primary subcorpus | Declared scope | Required outcome |
| --- | --- | --- |
| Graph orders and modes | 530 directed graphs, loops allowed, $k=1,2,3$; 50,363 raw legal orders; 1,357,209 raw executions | zero oracle mismatches |
| Prescribed split boundaries | available-set and unit-quota comparisons | 103,460 checks |
| Weighted all-quota optima | $k\le2$, weights 1 through 3, declared unequal costs | 21,804 comparisons |
| Weighted three-pivot optima | deterministic heterogeneous weights/costs and five stated quota pairs per graph | 2,560 comparisons |
| Restricted keys | declared allowed/required subsets | 128 comparisons |
| Arbitrary four-event orders | all 219 labelled partial orders; 960 legal orders; 8,640 raw admission-mode executions | 10,731 weighted all-quota comparisons |
| **Total optimization certificates** | the preceding four optimization subcorpora | **35,223 compared and independently verified; zero mismatches** |

The 35,223 total is $21,804+2,560+128+10,731$. The 103,460 prescribed-set
boundary checks are a separate count. The graph/order realization corpus overlaps
the retained frontier corpus; the matching 1,357,209 execution count is an
independent recomputation, not another population of protocols. The newer
four-event study has 8,640 raw executions because it explores three admission
modes; the earlier frontier's 3,840 admission executions remain a distinct scope.

The additional `scripts/check_synthesis_order_oracle.py` record is
`results/synthesis/order_oracle.json`. With seed `20261019`, it constructs 48
arbitrary three-pivot event DAGs, weights 1 through 3, costs 0 through 7, and
allowed/required split subsets. For these inputs it enumerates **4,647** legal
event permutations and **72,117** admissible-mode executions, and checks all
quota pairs: **3,253** minimum-cost comparisons and certificate checks must pass
with no mismatches. The two optimization corpora total **38,476** compared and
verified problems, with their separate scopes retained. The seeded corpus is
not an exhaustive enumeration of all three-pivot DAGs or weight/cost vectors.

The portable examples must retain their interpretations:

- Crossed deadlines require one optimally chosen split.
- A forced one-pivot repair requires cost 1; a repair after the signature
  opportunity permits cost 0 because it cannot retract the output.
- The weighted granularity fixture requires actual attainable weights, rather
  than a continuous capacity approximation.
- In the three-key two-cycle motif, both cheap leaves together cost 2 and are
  optimal. Each leaf has zero immediate benefit alone. The specified immediate
  gain-per-cost rule instead chooses the expensive center; this is the stated
  non-submodularity and greedy control, not a comparison against all heuristics.

### Synthetic scale cases

`synthesis_benchmarks.csv` contains **15 cases** and preserves every outcome:
**13** are `OPTIMAL` with replayed witnesses and independently verified Bellman
certificates; **2** are `RESOURCE_LIMIT`, meaning unknown. The largest certified
instances have **48 pivots**. Both unknown cases exceed the configured maximum
component size of 10: a dense component on 12 vertices and a directed cycle on
24 vertices. They are not infeasibility results or observed wall-clock timeouts.

Each solved case has a compressed certificate in `results/synthesis/certificates/`.
The study also stores source observations, per-problem comparison rows, example
inputs and certificates, and a summary. The default maximum potential table has
two million cells. Single-run timing is recorded separately in
`build_logs/refinement_synthesis_timings.json`; runtime values are not deterministic
reference data or evidence of a speedup.

## Native implementation conformance

The native stage runs the unmodified consensus package at CometBFT v0.39.3 commit
`49b82838fcca442b2445f76605c101609ed04130` using Go 1.25.0. Four ordinary-operation
scenarios give the following stable semantic counts:

| Scenario | Checks | Native signed votes | Recorded events |
| --- | ---: | ---: | ---: |
| Normal commit, missing-block catch-up, immutable emitted vote | 6 | 7 | 30 |
| Mixed-quorum timeout guards | 3 | 7 | 29 |
| Lock persistence and locked prevote | 3 | 9 | 38 |
| Valid-block proposal reuse | 2 | 9 | 35 |
| **Total** | **14** | **32** | **132** |

The Go receipt has four passing subtests plus one passing parent, not five
independent scenarios. Production tracked source must be clean before and after
execution. Each delivered proposal, block part and vote came from a native
state's internal queue; each fired timeout was actually scheduled by native code.
The normal commit scenario's two observers store the same block. No client
mutation or native disagreement is part of this experiment.

`native_conformance.json` retains native states, public keys, canonical sign bytes
and signatures; `native_provenance.json` binds source/test/result hashes to the
actual Go command and successful receipt. The separate Python/OpenSSL audit uses
the uv-locked `native-audit` extra and must verify all 32 signatures, their
canonical metadata, and absence of conflicting same-slot vote records.
`native_signature_audit.json` must report PASS. It is a cryptographic/evidence
audit, not another consensus implementation.

Full reproduction reruns the base scenarios and then three additional normal
executions plus one race-detector execution. `native_repeatability.json` must
report unchanged semantic summaries, successful race-detector execution and
verified isolated output/log routing. Temporary repeated raw results stay under
the project cache; the output tree retains their passing receipts.

The native dispatcher is synchronous and uses local in-memory fixtures. It does
not run the production reactor, sockets, WAL loop or persistent signer, reproduce
the guarded model's mutation, or constitute a refinement proof. For the full
source/scope explanation see the repository's
[native conformance documentation](../../experiments/native_cometbft/README.md).

## Assurance and reproducibility interpretation

The Lean declarations retain the arbitrary one-pivot behavioral contract,
capacity and budget arithmetic, weighted interval and persistent-output machine.
`GraphRealization.lean` now proves graph reversal, finite acyclicity versus an
injective schedule, and the graph-to-order bridge including cover-edge input.
`CertificateOptimality.lean` proves the Bellman lower-bound, matching-witness
optimality and infinite-potential infeasibility principles.

The weighted four-role correspondence, maximum-acyclic-set optimization and
optimal graph-capacity attainment, Python parser/checker and SCC enumeration,
and production-client refinement remain separate paper proofs or executable
obligations. The 46-declaration axiom audit does not convert those obligations
into mechanized refinements. The repository's
[axiom report](../../formal/lean/AXIOM_REPORT.md) and
[claim ledger](../CLAIM_EVIDENCE_LEDGER.md) give the mapping; successful Lean
receipts are bound to the checked source hashes.

`scripts/verify_results.sh` compares all listed deterministic results and **every
file under `results/synthesis/`, `results/transition/` and
`results/transition_bridge/`** byte-for-byte with committed references. Synthesis
gzip headers are deterministic. Among native files, only
**`results/native/native_summary.json`** is byte-compared. Native raw timestamps,
votes, signatures, provenance, signature-audit output, repeatability receipts
and execution logs are regenerated and verified, not expected to match previous
bytes. Source manifests check exact fixture identity, including the separately
identified v0.39.3 and v0.40.0 CometBFT snapshots.

The PDF is checked for successful regeneration, source synchronization, the
15-page main-text budget, diagnostics and embedded fonts. **An identical PDF
SHA-256 across different TeX engines is not required.** Logs may contain runtime
durations, cache details and tool-version information, so their entire bytes are
not scientific result references. A run is complete only after every mandatory
stage succeeds and `build_logs/reproduction_summary.log` records PASS.

Actual physical/main/appendix page counts are recorded for the current build.
The earlier second revision had 20 physical pages; that historical count is not
a required outcome for the expanded transition-system manuscript.
