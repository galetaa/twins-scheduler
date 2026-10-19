# Claim-to-evidence ledger

This ledger maps the current manuscript's five main theorems: legal relational
preservation (1), behavioral one-pivot separation (2), repair-frontier
characterization (3), weighted minimum-cost refinement (4), and certificate
soundness (5). Lemma 1 is the graph/order equivalence; Corollary 1 is the
unit-weight minimum phase budget. Historical T1/T2/T3/T6 names identify retained
artifact obligations, not current paper numbering.

## Evidence interpretation

The full graph/event-order lemma and the general Bellman certificate principle
are now mechanized. The independent-pivot behavioral contract, weighted
four-role correspondence, completeness of Python parsing/enumeration/replay,
and full production-client refinement remain separate obligations. Native
conformance executes unchanged code for four normal-operation scenarios; the
mutant disagreement belongs to the guarded local model.

The integrated scientific gate passes **47 Python tests**, Go checks,
**8 expected UNSAT and 4 expected SAT SMT obligations**, a **14-job Lean build**,
an audit of **27 named declarations**, source hygiene on **22 Lean files**, and
independent `leanchecker SchedulerClosure` rechecking. The receipt in
`results/generated/lean_verification.json` binds successful commands to exact
source hashes. Typesetting and full data reproduction have their separate logs.

The synthesis experiments contain two independently implemented raw-event
oracle suites: **35,223** and **3,253** optimum/certificate comparisons, with
zero mismatches. All **13** solved scale cases retain full independently checked
certificates; the other **2** cases return a configured resource-limit result.
The old 384-row Python/Go comparison remains evidence about the old terminal
classifier. It is not an independent implementation of the new concrete model.

A successful command validates only the scope recorded below. In particular,
a general Lean certificate theorem is not a verified Python checker, and a
normal-operation native test is not a mutant disagreement experiment.

## Claims

### C1: Section 2.1, Theorem 1

**Claim.** Legal relational closure preserves terminal unsafety under the insertion, retained-action simulation, and upward-closure hypotheses, with independent target-trace legality.

**Evidence kind.** Supporting sufficient relational theorem

**Lean coverage.** SchedulerClosure.merged_trace_lifting; SchedulerClosure.legal_scheduler_closure_preserves_unsafe

**Executable evidence.** Existing independent finite legal-target check; target legality checked separately

**Supporting SMT.** Existing T2 insertion/retained/upward verification conditions

**Scope.** Finite merged traces under the stated relation and legal coarse-language membership; theorem is sufficient, not necessary.

**Unsupported extension.** Arbitrary message insertion; necessity; automatic legality after repair suppresses a later emission; novelty as a general simulation principle.

**Artifact paths.** formal/lean/SchedulerClosure/ClosureLifting.lean; results/generated/independent_proof_checks.json

**Recorded status.** PASS_RETAINED

### C2: Section 3, Theorem 2

**Claim.** The explicit behavioral quorum-pivot contract yields a fine unsafe run and safe runs for both coarse edge bits; persistence, first-vote necessity, timely repair before second-vote issuance, and observation coverage are hypotheses.

**Evidence kind.** Corrected arbitrary-contract separation theorem

**Lean coverage.** SchedulerClosure.RepairFrontier.behavioral_quorum_pivot_separation; SchedulerClosure.RepairFrontier.persistence_hypothesis_independent

**Executable evidence.** Concrete canonical runs and persistence/late-output controls provide examples, not a proof that every protocol meets the contract

**Supporting SMT.** No new SMT encoding of the arbitrary behavioral contract; old T3 checks only its prior fixed Boolean schema

**Scope.** Lean quantifies over arbitrary run, vote, and unsafe functions satisfying the contract; legal scheduler realization and discharge of the behavioral assumptions remain external obligations.

**Unsupported extension.** Inferring persistence from absence of repair; using repair merely before a collector; calling the old hard-coded pivotAtSecond table a proof of the corrected arbitrary-contract theorem.

**Artifact paths.** formal/lean/SchedulerClosure/RepairFrontier.lean; src/python/twins_scheduler/concrete_trace.py

**Recorded status.** LEAN_CONTRACT_PASS

### C3: Appendix D, parametric certificate families

**Claim.** For f>=1 the original n=3f+1, q=2f+1 family has one-short bases; the paper also allocates k required pivots for 1<=k<=f under the behavioral contract.

**Evidence kind.** Conditional certificate-family construction

**Lean coverage.** SchedulerClosure.parametric_family_separation (old single-pivot Boolean family only)

**Executable evidence.** Existing exact quorum arithmetic, Go big.Int checks, and Python large-f checks; multi-pivot participant allocation is a paper argument

**Supporting SMT.** Existing T3 arithmetic verification conditions for the original family

**Scope.** Unweighted certificate arithmetic and explicitly supplied behavior; old Lean declaration does not formalize the new k-pivot participant allocation or its protocol realization.

**Unsupported extension.** Labeling this the revised Corollary 1; weighted-stake or arbitrary locking-protocol refinement; claiming k>1 Tendermint transition traces from the n=4 witness.

**Artifact paths.** formal/lean/SchedulerClosure/ParametricFamily.lean; manuscript/markdown/manuscript.md

**Recorded status.** PASS_RETAINED_SCOPE_NARROWED

### C4: Appendix B.2, earlier seven-flag diagnostic

**Claim.** Within the retained Boolean machine, strict separation is S2 and D and T and Ed and X and (S1 or Rq), with exactly three of 128 satisfying assignments.

**Evidence kind.** Supplementary finite Boolean characterization

**Lean coverage.** SchedulerClosure.strictSeparation_eq_characterization; SchedulerClosure.strictSeparation_iff_three

**Executable evidence.** Existing exhaustive 128-assignment cross-check

**Supporting SMT.** Existing T6 operational equivalence and three-assignment verification conditions

**Scope.** This seven-flag abstraction; the revised interpretation of T concerns the second-vote opportunity, not a later collector. The old atomic opportunity combined these events.

**Unsupported extension.** Calling this the revised central theorem; treating it as a universal locking-protocol criterion; importing its atomic timing into the explicit signed-output model.

**Artifact paths.** formal/lean/SchedulerClosure/PremiseBoundary.lean; manuscript/markdown/appendices.md

**Recorded status.** PASS_RETAINED

### C5: Validation and assurance, retained prior algebraic evidence

**Claim.** The earlier bounded Boolean Tendermint-style model has the reported six terminal classifications, and Python and Go agree on 384 rows per implementation for f=1..64.

**Evidence kind.** Retained terminal-classification and arithmetic evidence

**Lean coverage.** SchedulerClosure.bounded_baseline_safe; SchedulerClosure.bounded_missing_lock_phase_specific_unsafe; SchedulerClosure.bounded_missing_lock_directed_safe; SchedulerClosure.bounded_tendermint_refines_quorum_pivot

**Executable evidence.** Existing 384-row Python/Go comparison; old independent f=1..128 sweep (768 classifier cases)

**Supporting SMT.** No SMT transition refinement of the production client

**Scope.** Definitions compute terminal flags from admission/lock formulas. The declaration containing refines proves terminal classification only. Legacy artifact filenames and report field names are retained for provenance.

**Unsupported extension.** Transition refinement; source-to-source production conformance; independent Go verification of the new concrete trace; interpreting increasing f as validation of many protocols.

**Artifact paths.** formal/lean/SchedulerClosure/CometBFTInstantiation.lean; results/generated/cometbft_refinement_results.json; results/generated/cometbft_refinement_results_go.json

**Recorded status.** PRIOR_CLASSIFICATION_PASS

### C6: Appendix B.1, supporting replay-erasure proposition

**Claim.** Under state/output congruence, projected duplicate stutter, and silent duplicate output, erasure preserves terminal relevant state and the complete relevant output trace.

**Evidence kind.** Supplementary replay-erasure theorem

**Lean coverage.** SchedulerClosure.replay_erasure_with_outputs; SchedulerClosure.replay_erasure_state_observation

**Executable evidence.** Existing T1 certificate and independent replay checks

**Supporting SMT.** Existing T1 projection and duplicate-stutter verification conditions

**Scope.** Finite traces, the declared relevant projection and output function, and observations factoring through that projection.

**Unsupported extension.** Labeling replay the revised Theorem 3; erasure under immediate projected silence alone; novelty as general congruence reasoning.

**Artifact paths.** formal/lean/SchedulerClosure/ReplayErasure.lean; manuscript/markdown/appendices.md

**Recorded status.** PASS_RETAINED

### C7: Appendix B.1, replay negative control

**Claim.** The supplied X,X,Y machine shows that an immediately silent duplicate can change a later relevant observation or output through hidden state.

**Evidence kind.** Finite counterexample

**Lean coverage.** SchedulerClosure.hidden_state_counterexample; SchedulerClosure.hidden_state_breaks_output_congruence

**Executable evidence.** Existing independent replay check: full observation 1, erased observation 0

**Supporting SMT.** Existing T1 hidden-state XXY satisfiable negative control

**Scope.** The supplied hidden-state/output machine demonstrates necessity of the appropriate congruence conditions.

**Unsupported extension.** Claiming every duplicate is harmful or that all replay erasures fail.

**Artifact paths.** formal/lean/SchedulerClosure/ReplayErasure.lean; formal/smt/negative_controls/T1_hidden_state_XXY_counterexample.smt2

**Recorded status.** PASS_RETAINED

### C8: Section 2, executions and unsafe observations

**Claim.** Unsafe is a state predicate on the terminal execution state, and the observation function is applied separately when forming UnsafeObs.

**Evidence kind.** Typed semantic definition

**Lean coverage.** SchedulerClosure.UnsafeObservationSet; SchedulerClosure.unsafe_observation_has_unsafe_terminal

**Executable evidence.** Existing independent unsafe-observation typing check

**Scope.** Designated observer decisions and the stated observation domain; separation concerns emptiness, not equality of every unsafe observation.

**Unsupported extension.** Applying Unsafe directly to an observation or claiming all unsafe observation values are preserved by the negative results.

**Artifact paths.** formal/lean/SchedulerClosure/UnsafeObservations.lean

**Recorded status.** PASS_RETAINED

### C9: Section 2, admission and order semantics

**Claim.** The original fixed-order closure is a stable filter of already-emitted controlled envelopes, with no synthesis, replay, or retained-order change; later partial-order languages are separately specified.

**Evidence kind.** Scheduler semantics for the original fixed-order filter

**Lean coverage.** SchedulerClosure.typeClosure; SchedulerClosure.delivered_was_emitted; SchedulerClosure.delivered_preserves_order; SchedulerClosure.enabling_implies_closed_edge

**Executable evidence.** Existing scheduler checks; new concrete no-synthesis and once-only audits; separate frontier order checks in C11

**Scope.** The old Lean scheduler module covers the stable filter, not all linear extensions of the new graph schema. Suppressed opportunity slots retain their precedence constraints in that schema.

**Unsupported extension.** Reading FIFO, within-view delay, order coverage, or automatic message production into a directed admission graph.

**Artifact paths.** formal/lean/SchedulerClosure/SchedulerSemantics.lean; src/python/twins_scheduler/concrete_trace.py; src/python/twins_scheduler/repair_frontier.py

**Recorded status.** PASS_RETAINED_SCOPE_NARROWED

### C10: Validation and assurance, what Lean checks

**Claim.** The integrated Lean 4.33.0 project builds, audits 27 declarations, and passes independent kernel-object rechecking. Graph/event-order realization and Bellman certificate soundness are mechanized; weighted behavior, the Python checker and production-client refinement are not.

**Evidence kind.** Revision assurance gate

**Lean coverage.** formal/lean/AxiomAudit.lean; RepairFrontier, GraphRealization and CertificateOptimality declarations in ARTIFACT_THEOREM_MAP.md

**Executable evidence.** lake build: 14 jobs; axiom audit: 27 declarations; leanchecker exit 0; source hygiene: 22 files PASS; Python: 47 tests PASS; Go: PASS

**Supporting SMT.** Supporting SMT checks: 8 positive UNSAT and 4 negative-control SAT, pinned z3-solver 4.13.3.0; these do not replace Lean kernel checking

**Scope.** The successful command receipt records SHA-256 hashes of the checked formal/lean source files. The report assembler rejects missing, unsuccessful, or source-stale receipts. This gate validates the named formal declarations and executable scopes; it does not extend them. Coq remains secondary.

**Unsupported extension.** Calling the weighted four-role theorem, Python checker implementation or production CometBFT refinement kernel-checked; conflating SMT/custom certificates with a mature prover.

**Artifact paths.** formal/lean/AXIOM_REPORT.md; results/generated/lean_verification.json; results/generated/formal_verification.json; build_logs/lean_build.log; build_logs/lean_axiom_audit.log; build_logs/leanchecker.log; build_logs/python_tests.log; build_logs/go_tests.log; results/generated/smt_summary.json

**Recorded status.** SCIENTIFIC_REVISION_GATE_PASS

### C11: Section 4, Lemma 1 and Theorem 3

**Claim.** Joint lateness of J is realizable iff the repair graph H[J] is acyclic. Under the independent initial-ready pivot and complete-order contracts, coarse unsafety has the weighted subset characterization and, for unit weights, max(d0,d1)<=k and d0+d1<=k+alpha(H).

**Evidence kind.** Mechanized graph/event-order equivalence with paper behavioral and capacity correspondence

**Lean coverage.** GraphRealization.repair_graph_reversal_iff; finite_acyclic_iff_schedule; repair_graph_iff_realizable_schedule; repair_graph_from_covers_iff_schedule; RepairFrontier.directed_unsafe_iff and strict_separation_iff (arithmetic)

**Executable evidence.** 530 directed graphs including loops for k=1..3; 50,363 legal orders; 1,357,209 executions; 13,074 boundary and 4,164 joint-lateness checks; additionally all 219 labelled four-event partial orders via cover edges

**Supporting SMT.** No new SMT proof of the graph-to-execution correspondence

**Scope.** The full graph/order lemma is proved for a strict partial order and distinct repair/vote event kinds; finite event coverage supplies a schedule. The behavioral contribution law, collector coverage and capacity optimization remain separate paper obligations. No capacity formula or alpha(H) premise is assumed by the graph module.

**Unsupported extension.** Extending the initially-ready independent-pivot contract to interdependent protocol behavior or incomplete scheduler order languages without a conformance argument; identifying graph mechanization with full client refinement.

**Artifact paths.** src/python/twins_scheduler/repair_frontier.py; scripts/run_repair_frontier.py; results/revision/frontier_summary.json; formal/lean/SchedulerClosure/RepairFrontier.lean; formal/lean/SchedulerClosure/GraphRealization.lean

**Recorded status.** GRAPH_ORDER_LEAN_PAPER_BEHAVIOR_FINITE_PASS

### C12: Section 5.2, Corollary 1

**Claim.** With unit weights and fine feasibility, the exact minimum number of optimally chosen split keys is max(0,d0+d1-k-alpha(H)); an at-most-t budget yields optimal capacity min(k,alpha(H)+t).

**Evidence kind.** Paper optimal-set construction plus mechanized quota arithmetic

**Lean coverage.** SchedulerClosure.RepairFrontier.split_capacity_bound; SchedulerClosure.RepairFrontier.minimum_phase_splits

**Executable evidence.** 13,074 exhaustive minimum-budget comparisons across the 530 graph domains

**Scope.** Lean proves the budget equivalence assuming the split-capacity expression. The maximum-acyclic-set choice and its graph attainment are paper arguments. Split-key choice is existential.

**Unsupported extension.** Every arbitrary choice of that many exceptions suffices; weighted budget follows from the unit formula; Lean proves the graph optimization itself.

**Artifact paths.** formal/lean/SchedulerClosure/RepairFrontier.lean; results/revision/frontier_graph_cases.csv; results/revision/frontier_summary.json

**Recorded status.** PAPER_OPTIMIZATION_FINITE_PASS_LEAN_ARITHMETIC_PASS

### C13: Concrete protocol evidence and Appendix C, guarded model witness

**Claim.** Twelve guarded n=4 traces reproduce the canonical baseline/mutant matrix, distinguish repair before and after indispensable precommit issuance, and retain A=0,C=1 in a separate FIFO-compatible gossip control; only P's round-0 logical lock update is omitted.

**Evidence kind.** Authenticated event-level bounded witness and controls

**Lean coverage.** None for the concrete transition model or client; the small abstract output component is separately identified in C15

**Executable evidence.** 12 trace legality audits; 14 dedicated unit tests; 6 canonical cases, 4 direct timing controls, 2 relay controls; all 6 canonical and both relay controls pass admitted-vote FIFO checks

**Scope.** Equal weights, H=1, rounds 0/1, proposer prefix B/C, fixed other type-uniform edges and declared block/relay opportunities; deterministic test-only authentication. Unsupported transition branches are explicit. A and C are unmutated.

**Unsupported extension.** Production CometBFT execution or vulnerability; full refinement; an independent Go mirror; direct late-precommit timing without its non-FIFO qualification; silently treating the relay skeleton as the original bound.

**Artifact paths.** src/python/twins_scheduler/concrete_trace.py; scripts/run_concrete_trace.py; tests/unit/test_concrete_trace.py; results/new/concrete_trace.json; results/new/concrete_trace.csv; docs/research/CONCRETE_TRACE.md

**Recorded status.** BOUNDED_12_CASES_14_TESTS_PASS

### C14: Section 5.3, weighted common-frontier interval

**Claim.** A weighted coarse witness exists iff an attainable forced-early subset weight x satisfies max(0,d0-WL)<=x and x+d1<=W; indivisible weights prevent replacing attainable sums by a continuous total-capacity inequality.

**Evidence kind.** Weighted admission interval under a common-frontier contract

**Lean coverage.** SchedulerClosure.RepairFrontier.weighted_admission_interval; SchedulerClosure.RepairFrontier.weighted_granularity_counterexample

**Executable evidence.** 258 weighted domains, weights in {1,2,3}, up to 3 pivots; 15,700 boundary checks using extremal late order and all admissions; explicit weights (2,2), deficits (1,3) control

**Scope.** The attainable-subset predicate is retained in Lean. Common-frontier scheduling reduction and subset interpretation are separate paper arguments; the sweep is not all order permutations.

**Unsupported extension.** Continuous-weight substitution; arbitrary weighted graph scheduling discharged by the interval lemma; weighted or dynamic-validator CometBFT refinement.

**Artifact paths.** formal/lean/SchedulerClosure/RepairFrontier.lean; results/revision/frontier_weighted_cases.csv; results/revision/frontier_summary.json

**Recorded status.** WEIGHTED_INTERVAL_LEAN_FINITE_PASS

### C15: One-pivot timing correction and concrete late-repair controls

**Claim.** Repair can prevent a prospective second signature but cannot erase an already recorded signed output; the supplied output-machine trace and concrete executions demonstrate repair before a collector can be too late.

**Evidence kind.** Small output-machine theorem and concrete timing counterexample

**Lean coverage.** SchedulerClosure.RepairFrontier.repair_preserves_signed_output; SchedulerClosure.RepairFrontier.late_repair_before_certificate_is_unsafe; SchedulerClosure.RepairFrontier.repair_before_second_vote_is_safe; SchedulerClosure.RepairFrontier.closed_edge_still_permits_second_vote

**Executable evidence.** Frontier immutable-output control; concrete direct and FIFO-compatible relay late-repair cases; direct transport inversion is explicitly diagnosed

**Scope.** The Lean output machine is deliberately small; signed/enqueued support persists under its transitions. The concrete protocol trace independently instantiates the issue inside its declared bound.

**Unsupported extension.** Treating the toy output machine as a production transition proof; requiring every late repair to cause disagreement; using only the second decision as the repair deadline.

**Artifact paths.** formal/lean/SchedulerClosure/RepairFrontier.lean; results/revision/frontier_summary.json; results/new/concrete_trace.json

**Recorded status.** ABSTRACT_OUTPUT_LEAN_CONCRETE_PASS

### C16: Appendix A

**Claim.** Coarse unsafe reachability is NP-complete when the finite unit-weight independent-pivot opportunity schema and k are inputs, via the classical symmetric-orientation/independent-set construction.

**Evidence kind.** Paper complexity proof using a classical reduction

**Lean coverage.** None

**Executable evidence.** No finite enumeration is offered as proof of the complexity result; the paper supplies the reduction and polynomial certificate verification

**Supporting SMT.** None

**Scope.** The explicit abstract opportunity schema with complete-order coverage; graph size varies. Classical graph hardness is credited rather than claimed as new.

**Unsupported extension.** A hardness result for the fixed n=4 trace or a production client; every constructed opportunity order is protocol-realizable; kernel checking of the reduction.

**Artifact paths.** manuscript/markdown/appendices.md

**Recorded status.** PAPER_PROOF_ONLY

### C17: Concrete protocol evidence and limitations, source pin

**Claim.** The new trace cites exact CometBFT v0.39.3 commit 49b82838fcca442b2445f76605c101609ed04130; the older upstream_fragments snapshot is correctly retained as v0.40.0.

**Evidence kind.** Primary-source integrity and attribution

**Lean coverage.** None

**Executable evidence.** Exact GitHub tag/commit receipts, Git blob identifiers and SHA-256 manifests; documented inspection of the exercised guards

**Supporting SMT.** None

**Scope.** Source verification proves identity of the evidence files; it does not prove execution equivalence. v0.39.3 state path is consensus/state.go, while local source fixtures have .go.txt suffixes.

**Unsupported extension.** Calling the old v0.40.0 fixture v0.39.3; equating source-fragment matches or immutable hashes with client conformance.

**Artifact paths.** models/tendermint_style/upstream_v0393/SOURCE.json; models/tendermint_style/upstream_v0393/GITHUB_RECEIPTS.json; models/tendermint_style/upstream_v0393/MANIFEST.sha256; docs/research/LITERATURE_AND_PROVENANCE_AUDIT.md

**Recorded status.** SOURCE_IDENTITY_VERIFIED

### C18: Theorem 4, certifying minimum-cost phase refinement

**Claim.** Positive integer vote weights, nonnegative split costs and allowed/required keys admit exactly the four-role partition S,J,X,Y with H[J] acyclic and both guaranteed support quotas met. Minimizing split cost yields a legal model witness of minimum control cost.

**Evidence kind.** Paper characterization plus exact constructive algorithm

**Lean coverage.** GraphRealization realizes selected reversals; the full weighted four-role correspondence is not mechanized.

**Executable evidence.** 35,223 raw-event optimum comparisons and independent certificate checks; separate 3,253-case arbitrary-order oracle; 12 dedicated tests.

**Scope.** Initially-ready independent pivots and full opportunity order. X guarantees first support but may supply a bonus second vote. Costs are declared inputs; all original slots survive suppression. Exponential in largest loop-free SCC and pseudo-polynomial in quotas.

**Unsupported extension.** A formula newly discovered for prescribed unit-cost S; automatic contract extraction; polynomial-time optimization or verification on all inputs; treating resource limits as infeasibility.

**Artifact paths.** src/python/twins_scheduler/refinement_synthesis.py; scripts/run_refinement_synthesis.py; scripts/check_synthesis_order_oracle.py; results/synthesis/synthesis_summary.json; results/synthesis/order_oracle.json

**Recorded status.** PAPER_EXACT_SYNTHESIS_ORACLES_PASS

### C19: Theorem 5, certificate soundness

**Claim.** Local Bellman lower-bound inequalities and terminal conditions bound the cost of every feasible represented path. A replayed witness attaining the finite root bound is optimal; an infinite root bound certifies infeasibility.

**Evidence kind.** Mechanized general certificate principle with independent executable checker

**Lean coverage.** CertificateOptimality.bellman_path_lower_bound; certified_witness_is_minimum; certified_infeasibility

**Executable evidence.** All 38,476 certificates in the two oracle suites checked independently; 13 full scale certificates retained; suboptimal witness, input substitution, terminal-table corruption and lost-slot controls rejected.

**Scope.** Lean covers arbitrary nonnegative-cost paths and extended-natural potentials, without assuming optimal potentials. Python parsing, graph reconstruction, local enumeration completeness and model replay remain implemented obligations.

**Unsupported extension.** A Lean-verified Python program; trusting only chosen transitions for an optimum; a short polynomial certificate for every instance; a solver resource limit as mathematical infeasibility.

**Artifact paths.** formal/lean/SchedulerClosure/CertificateOptimality.lean; src/python/twins_scheduler/refinement_synthesis.py; tests/unit/test_refinement_synthesis.py; results/synthesis/certificates/

**Recorded status.** BELLMAN_LEAN_CHECKER_CONTROLS_PASS

### C20: Why immediate benefit is an unreliable guide

**Claim.** The unit-weight fixed-split capacity F is not submodular. In the three-key two-cycle family with costs M,1,1 and M>2, the specified immediate-gain-per-cost rule pays M while the optimum is 2, so its approximation ratio is unbounded.

**Evidence kind.** Explicit mathematical counterexample with executable controls

**Lean coverage.** Not mechanized.

**Executable evidence.** M=3,10,100,1000 controls match the proof; ten repeated motifs at k=30 produce certified optimum 20 and myopic cost 1000.

**Scope.** Unit vote weights and full quotas; one completely specified greedy rule. Tie-breaking does not affect the family because only the center has positive initial marginal gain.

**Unsupported extension.** Impossibility for every greedy or heuristic method; representative measured performance against external solvers.

**Artifact paths.** manuscript/markdown/manuscript.md; results/synthesis/synthesis_summary.json; results/synthesis/synthesis_benchmarks.csv

**Recorded status.** PAPER_COUNTEREXAMPLE_EXECUTED_PASS

### C21: Validation and assurance, synthesis cases

**Claim.** Of 15 deterministic synthetic domains, 13 have independently certified optima, with largest solved k=48; two exceed the configured largest-component limit 10 and return unknown.

**Evidence kind.** Declared finite structural experiment

**Lean coverage.** General certificate principle only.

**Executable evidence.** All 13 full certificates saved; weighted 24-pivot W=75 case changes optimum from 0 to 5 as quotas tighten from (60,68) to (74,73).

**Scope.** Synthetic weights/costs and seeded graph families; configured size cutoffs, not observed timeouts. Timing observations are separate and nondeterministic.

**Unsupported extension.** A runtime benchmark victory, production scale guarantee, or infeasibility of the two resource-limited cases.

**Artifact paths.** results/synthesis/synthesis_benchmarks.csv; results/synthesis/certificates/; docs/research/REFINEMENT_SYNTHESIS.md

**Recorded status.** 13_OPTIMAL_2_UNKNOWN

### C22: Concrete protocol evidence, targeted tests of unchanged implementation code

**Claim.** Four ordinary-operation scenarios execute unchanged CometBFT v0.39.3 at the pinned commit, pass 14 checks, record 32 native Ed25519 votes and 132 events, and preserve the specified semantic outcomes over three repeats plus one race-detector run.

**Evidence kind.** Execution of unchanged native consensus code and independent cryptographic audit

**Lean coverage.** No protocol transition refinement is mechanized.

**Executable evidence.** Native emitted proposals, votes, actual scheduled timeout guards, lock/valid state, proposer priority, missing-block catch-up, in-memory BlockStore and local ABCI. Separate cryptography/OpenSSL audit validates all 32 canonical signed votes. Source and evidence hashes checked.

**Scope.** Four equal-weight validators per finite ordinary scenario; synchronous State dispatch, upstream MockPV test keys and in-memory fixtures. No reactor, sockets, WAL receive loop or persistent signer. Raw native timestamps vary across runs.

**Unsupported extension.** A native mutant disagreement, deployed-client vulnerability, exhaustive safety proof, model-to-client refinement or disk durability guarantee.

**Artifact paths.** experiments/native_cometbft/; results/native/native_summary.json; results/native/native_provenance.json; results/native/native_signature_audit.json; results/native/native_repeatability.json

**Recorded status.** NATIVE_BASELINE_14_CHECKS_32_SIGNATURES_PASS
