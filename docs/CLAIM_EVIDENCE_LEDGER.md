# Claim-to-evidence ledger

This ledger maps the current manuscript's six main theorems. Historical
T1/T2/T3/T6 identifiers name retained artifact obligations and do not denote
the current main-paper theorem numbers. C1-C22 retain the earlier scientific
evidence with updated manuscript locations; C23-C35 identify the general
transition-system extension and its additional checks.

## Current theorem map

| Main theorem | Manuscript location | Statement | Ledger claims |
|---|---|---|---|
| Theorem 1 | Section 3.1 | Exact trace refinement and least required/mixed split set | C23 |
| Theorem 2 | Section 3.2 | Minimum-cost synthesis in a complete finite LTS | C24 |
| Theorem 3 | Section 3.3 | Strict-sublevel and full-closure certificate soundness | C25 |
| Theorem 4 | Section 4.1 | Abstract lower-bound transfer and matching concrete witness | C26 |
| Theorem 5 | Section 4.2 | Whole-policy elimination and finite abstraction progress | C27 |
| Theorem 6 | Section 5 | Weighted independent-pivot refinement characterization | C18, C33 |

The retained structural proofs are now in Appendix E: Proposition E1 is legal
relational preservation (C1), Proposition E2 is behavioral one-pivot separation
(C2), Lemma E1 is graph/order realization and Proposition E3 is the frontier
characterization (C11), Corollary E1 is the unit-weight phase budget (C12), and
Proposition E4 is the structural Bellman certificate principle (C19). Supporting
replay/diagnostic results remain in Appendix B, the original guarded trace in
Appendix C, parametric families in Appendix D, and the budget illustration in
Appendix F. Appendix A distinguishes general finite-LTS complexity (C28) from
the retained independent-pivot reduction (C16).

## Evidence interpretation

The general semantic results remove pivot independence from policy completion,
closed-set certificates, labelled simulation and whole-policy elimination.
Their hypotheses still require a complete declared control interface and the
stated transition, cost and observation correspondence. The executable
optimizer/checkers consume complete finite graphs. Their correctness, the
protocol exporter, and correspondence with arbitrary production-client code
are not kernel-verified.

The integrated Lean 4.33.0 gate completes **15 build jobs**, audits **46 selected
named declarations** and rechecks the compiled object with
`leanchecker SchedulerClosure`; source hygiene covers **23 Lean/Coq files**.
These are different units. The source-bound receipt records successful exits
and hashes of the checked Lean sources. Nineteen selected declarations belong
to the new general transition-refinement module; the earlier graph/order and
Bellman results remain integrated. The finite CEGAR iteration-count bound and
weighted four-role correspondence retain paper-level proof obligations.
Supporting SMT retains **8 expected UNSAT** and **4 expected SAT** cases.

Native conformance executes unchanged CometBFT code for four ordinary-operation
scenarios (C22). The disagreement witnesses and complete protocol graphs are
instances of the separately bounded guarded model (C13, C29-C30). Matching a
native trace does not discharge the new theorem's universal local-simulation
premises. The earlier 384-row Python/Go agreement checks its historical terminal
classifier (C5), not a transition refinement or an independent implementation
of the coupled model.

## Experimental counting units

| Evidence family | Reported unit and result | Interpretation |
|---|---|---|
| Retained structural optimum oracles | 35,223 and 3,253 optimum/certificate comparisons; zero mismatches | Parameterized independent-pivot instances, not distinct protocols |
| Structural scale study | 13 certified optima and 2 configured unknowns | Fifteen synthetic inputs; no runtime ranking |
| General direct-synthesis study | 7,904 configurations = 7,776 exhaustive-family + 128 seeded inputs | C31; six semantic examples and coupled controls are recorded separately |
| Independent direct/CEGAR oracle | 2,960 instances, 5,920 method comparisons, 6,857 checked iterations | C32; two methods reuse each input, and iterations are internal to those runs |
| Pivot/general specialization | 1,507 queries, 3,014 method comparisons, 1,189 normalized witnesses | C33; graph/poset families overlap retained structural studies |
| Guarded exporter audit | 128 direct explorations = 64 policies for each of two program variants | C30; per-policy state/edge totals repeat common states |
| Saved semantic/protocol CEGAR runs | 9 runs, 32 iterations, 23 eliminated policies | C34; reuses six semantic examples and the coupled models |

The 512 Set Cover reductions and 2,048 edge-family configurations in C32 also
appear in unit tests. They are not additional disjoint corpora. The 512
reductions are likewise the finite evidence cited for C28. The two coupled
abstraction starts in C34 use the same mutant input. No global deduplication
across studies is claimed, so these counters must not be summed into a count
of unique protocols or unique inputs. Executable checks support the represented
finite models; they do not replace general proofs or verify their Python
implementations.

The CSV and Markdown below contain the same 35 claims. Artifact links point
to the complete underlying inputs, proofs, observations or reports; a PASS
status validates only the scope stated in its row.

## Claims

### C1: Appendix E.1, Proposition E1 (legal relational preservation)

**Claim.** Legal relational closure preserves terminal unsafety under the insertion, retained-action simulation, and upward-closure hypotheses, with independent target-trace legality.

**Evidence kind.** Supporting sufficient relational theorem

**Historical reference.** T2

**Lean coverage.** SchedulerClosure.merged_trace_lifting; SchedulerClosure.legal_scheduler_closure_preserves_unsafe

**Executable evidence.** Existing independent finite legal-target check; target legality checked separately

**Supporting SMT.** Existing T2 insertion/retained/upward verification conditions

**Scope.** Finite merged traces under the stated relation and legal coarse-language membership; theorem is sufficient, not necessary.

**Unsupported extension.** Arbitrary message insertion; necessity; automatic legality after repair suppresses a later emission; novelty as a general simulation principle.

**Artifact paths.** [formal/lean/SchedulerClosure/ClosureLifting.lean](../formal/lean/SchedulerClosure/ClosureLifting.lean); [results/generated/independent_proof_checks.json](../results/generated/independent_proof_checks.json)

**Recorded status.** PASS_RETAINED

### C2: Appendix E.2, Proposition E2 (behavioral quorum-pivot separation)

**Claim.** The explicit behavioral quorum-pivot contract yields a fine unsafe run and safe runs for both coarse edge bits; persistence, first-vote necessity, timely repair before second-vote issuance, and observation coverage are hypotheses.

**Evidence kind.** Corrected arbitrary-contract separation theorem

**Historical reference.** T3 (historical Boolean precursor only)

**Lean coverage.** SchedulerClosure.RepairFrontier.behavioral_quorum_pivot_separation; SchedulerClosure.RepairFrontier.persistence_hypothesis_independent

**Executable evidence.** Concrete canonical runs and persistence/late-output controls provide examples, not a proof that every protocol meets the contract

**Supporting SMT.** No new SMT encoding of the arbitrary behavioral contract; old T3 checks only its prior fixed Boolean schema

**Scope.** Lean quantifies over arbitrary run, vote, and unsafe functions satisfying the contract; legal scheduler realization and discharge of the behavioral assumptions remain external obligations.

**Unsupported extension.** Inferring persistence from absence of repair; using repair merely before a collector; calling the old hard-coded pivotAtSecond table a proof of the corrected arbitrary-contract theorem.

**Artifact paths.** [formal/lean/SchedulerClosure/RepairFrontier.lean](../formal/lean/SchedulerClosure/RepairFrontier.lean); [src/python/twins_scheduler/concrete_trace.py](../src/python/twins_scheduler/concrete_trace.py)

**Recorded status.** LEAN_CONTRACT_PASS

### C3: Appendix D (parametric certificate families); Appendix E.2

**Claim.** For f>=1 the original n=3f+1, q=2f+1 family has one-short bases; the paper also allocates k required pivots for 1<=k<=f under the behavioral contract.

**Evidence kind.** Conditional certificate-family construction

**Historical reference.** T3

**Lean coverage.** SchedulerClosure.parametric_family_separation (old single-pivot Boolean family only)

**Executable evidence.** Existing exact quorum arithmetic, Go big.Int checks, and Python large-f checks; multi-pivot participant allocation is a paper argument

**Supporting SMT.** Existing T3 arithmetic verification conditions for the original family

**Scope.** Unweighted certificate arithmetic and explicitly supplied behavior; old Lean declaration does not formalize the new k-pivot participant allocation or its protocol realization.

**Unsupported extension.** Calling this Corollary E1 or main Theorem 3; weighted-stake or arbitrary locking-protocol refinement; claiming k>1 Tendermint transition traces from the n=4 witness.

**Artifact paths.** [formal/lean/SchedulerClosure/ParametricFamily.lean](../formal/lean/SchedulerClosure/ParametricFamily.lean); [manuscript/markdown/appendices.md](../manuscript/markdown/appendices.md)

**Recorded status.** PASS_RETAINED_SCOPE_NARROWED

### C4: Appendix B.2 (earlier seven-flag diagnostic)

**Claim.** Within the retained Boolean machine, strict separation is S2 and D and T and Ed and X and (S1 or Rq), with exactly three of 128 satisfying assignments.

**Evidence kind.** Supplementary finite Boolean characterization

**Historical reference.** T6

**Lean coverage.** SchedulerClosure.strictSeparation_eq_characterization; SchedulerClosure.strictSeparation_iff_three

**Executable evidence.** Existing exhaustive 128-assignment cross-check

**Supporting SMT.** Existing T6 operational equivalence and three-assignment verification conditions

**Scope.** This seven-flag abstraction; the revised interpretation of T concerns the second-vote opportunity, not a later collector. The old atomic opportunity combined these events.

**Unsupported extension.** Calling this the revised central theorem; treating it as a universal locking-protocol criterion; importing its atomic timing into the explicit signed-output model.

**Artifact paths.** [formal/lean/SchedulerClosure/PremiseBoundary.lean](../formal/lean/SchedulerClosure/PremiseBoundary.lean); [manuscript/markdown/appendices.md](../manuscript/markdown/appendices.md)

**Recorded status.** PASS_RETAINED

### C5: Section 7.1 (retained earlier terminal-classifier evidence)

**Claim.** The earlier bounded Boolean Tendermint-style model has the reported six terminal classifications, and Python and Go agree on 384 rows per implementation for f=1..64.

**Evidence kind.** Retained terminal-classification and arithmetic evidence

**Historical reference.** Historical natural-protocol bridge

**Lean coverage.** SchedulerClosure.bounded_baseline_safe; SchedulerClosure.bounded_missing_lock_phase_specific_unsafe; SchedulerClosure.bounded_missing_lock_directed_safe; SchedulerClosure.bounded_tendermint_refines_quorum_pivot

**Executable evidence.** Existing 384-row Python/Go comparison; old independent f=1..128 sweep (768 classifier cases)

**Supporting SMT.** No SMT transition refinement of the production client

**Scope.** Definitions compute terminal flags from admission/lock formulas. The declaration containing refines proves terminal classification only. Legacy artifact filenames and report field names are retained for provenance.

**Unsupported extension.** Transition refinement; source-to-source production conformance; independent Go verification of the new concrete trace; interpreting increasing f as validation of many protocols.

**Artifact paths.** [formal/lean/SchedulerClosure/CometBFTInstantiation.lean](../formal/lean/SchedulerClosure/CometBFTInstantiation.lean); [results/generated/cometbft_refinement_results.json](../results/generated/cometbft_refinement_results.json); [results/generated/cometbft_refinement_results_go.json](../results/generated/cometbft_refinement_results_go.json)

**Recorded status.** PRIOR_CLASSIFICATION_PASS

### C6: Appendix B.1 (supporting replay-erasure proposition)

**Claim.** Under state/output congruence, projected duplicate stutter, and silent duplicate output, erasure preserves terminal relevant state and the complete relevant output trace.

**Evidence kind.** Supplementary replay-erasure theorem

**Historical reference.** T1

**Lean coverage.** SchedulerClosure.replay_erasure_with_outputs; SchedulerClosure.replay_erasure_state_observation

**Executable evidence.** Existing T1 certificate and independent replay checks

**Supporting SMT.** Existing T1 projection and duplicate-stutter verification conditions

**Scope.** Finite traces, the declared relevant projection and output function, and observations factoring through that projection.

**Unsupported extension.** Calling replay the current main Theorem 3; erasure under immediate projected silence alone; novelty as general congruence reasoning.

**Artifact paths.** [formal/lean/SchedulerClosure/ReplayErasure.lean](../formal/lean/SchedulerClosure/ReplayErasure.lean); [manuscript/markdown/appendices.md](../manuscript/markdown/appendices.md)

**Recorded status.** PASS_RETAINED

### C7: Appendix B.1 (hidden-state replay negative control)

**Claim.** The supplied X,X,Y machine shows that an immediately silent duplicate can change a later relevant observation or output through hidden state.

**Evidence kind.** Finite counterexample

**Historical reference.** T1

**Lean coverage.** SchedulerClosure.hidden_state_counterexample; SchedulerClosure.hidden_state_breaks_output_congruence

**Executable evidence.** Existing independent replay check: full observation 1, erased observation 0

**Supporting SMT.** Existing T1 hidden-state XXY satisfiable negative control

**Scope.** The supplied hidden-state/output machine demonstrates necessity of the appropriate congruence conditions.

**Unsupported extension.** Claiming every duplicate is harmful or that all replay erasures fail.

**Artifact paths.** [formal/lean/SchedulerClosure/ReplayErasure.lean](../formal/lean/SchedulerClosure/ReplayErasure.lean); [formal/smt/negative_controls/T1_hidden_state_XXY_counterexample.smt2](../formal/smt/negative_controls/T1_hidden_state_XXY_counterexample.smt2)

**Recorded status.** PASS_RETAINED

### C8: Section 2 (unsafe protocol states); Appendix E.1-E.2 (UnsafeObs)

**Claim.** Unsafe is a state predicate on the terminal execution state, and the observation function is applied separately when forming UnsafeObs.

**Evidence kind.** Typed semantic definition

**Lean coverage.** SchedulerClosure.UnsafeObservationSet; SchedulerClosure.unsafe_observation_has_unsafe_terminal

**Executable evidence.** Existing independent unsafe-observation typing check

**Scope.** Designated observer decisions and the stated observation domain; separation concerns emptiness, not equality of every unsafe observation.

**Unsupported extension.** Applying Unsafe directly to an observation or claiming all unsafe observation values are preserved by the negative results.

**Artifact paths.** [formal/lean/SchedulerClosure/UnsafeObservations.lean](../formal/lean/SchedulerClosure/UnsafeObservations.lean)

**Recorded status.** PASS_RETAINED

### C9: Section 2 (declared admission interface); Appendix E.3.1 (complete opportunity language)

**Claim.** The original fixed-order closure is a stable filter of already-emitted controlled envelopes, with no synthesis, replay, or retained-order change; later partial-order languages are separately specified.

**Evidence kind.** Scheduler semantics for the original fixed-order filter

**Lean coverage.** SchedulerClosure.typeClosure; SchedulerClosure.delivered_was_emitted; SchedulerClosure.delivered_preserves_order; SchedulerClosure.enabling_implies_closed_edge

**Executable evidence.** Existing scheduler checks; new concrete no-synthesis and once-only audits; separate frontier order checks in C11

**Scope.** The old Lean scheduler module covers a stable fixed-order filter, not the general LTS interface or all linear extensions of the independent-pivot order schema. Suppressed opportunity slots retain their precedence constraints in that schema. The new general semantics are separately mapped in C23-C27.

**Unsupported extension.** Reading FIFO, within-view delay, order coverage, or automatic message production into a directed admission graph.

**Artifact paths.** [formal/lean/SchedulerClosure/SchedulerSemantics.lean](../formal/lean/SchedulerClosure/SchedulerSemantics.lean); [src/python/twins_scheduler/concrete_trace.py](../src/python/twins_scheduler/concrete_trace.py); [src/python/twins_scheduler/repair_frontier.py](../src/python/twins_scheduler/repair_frontier.py)

**Recorded status.** PASS_RETAINED_SCOPE_NARROWED

### C10: Section 7.1 (mechanized and executable obligations)

**Claim.** The integrated Lean 4.33.0 project builds in 15 jobs, audits 46 selected declarations, and passes independent kernel-object rechecking; source hygiene checks 23 Lean/Coq files. The source-bound receipt matches the current checked Lean files.

**Evidence kind.** Revision assurance gate

**Historical reference.** Expanded assurance gate; prior revision audited 27 declarations in 14 jobs with 22 hygiene files

**Lean coverage.** formal/lean/AxiomAudit.lean; retained RepairFrontier, GraphRealization and CertificateOptimality results; nineteen selected TransitionRefinement results detailed in C35.

**Executable evidence.** lake build: 15 jobs; selected axiom audit: 46 declarations; leanchecker exit 0; source hygiene: 23 Lean/Coq files PASS. Retained SMT obligations are 8 expected UNSAT and 4 expected SAT; Python/Go aggregate execution is recorded separately in its logs.

**Supporting SMT.** Supporting SMT checks: 8 positive UNSAT and 4 negative-control SAT, pinned z3-solver 4.13.3.0; these do not replace Lean kernel checking

**Scope.** Counts denote build jobs, selected audited declarations and source-hygiene files, respectively; none is a count of independently verified protocols. The successful receipt records SHA-256 hashes and the report assembler rejects missing, unsuccessful or stale receipts. The earlier 27-declaration/14-job gate remains historical evidence. Coq remains secondary.

**Unsupported extension.** Calling the full weighted four-role theorem, executable product/CEGAR implementation, Python checker or production CometBFT refinement kernel-checked; calling 23 hygiene files 23 Lean proof modules; conflating SMT/custom certificates with the Lean kernel gate.

**Artifact paths.** [formal/lean/AXIOM_REPORT.md](../formal/lean/AXIOM_REPORT.md); [results/generated/lean_verification.json](../results/generated/lean_verification.json); [results/generated/formal_verification.json](../results/generated/formal_verification.json); [build_logs/lean_build.log](../build_logs/lean_build.log); [build_logs/lean_axiom_audit.log](../build_logs/lean_axiom_audit.log); [build_logs/leanchecker.log](../build_logs/leanchecker.log); [build_logs/python_tests.log](../build_logs/python_tests.log); [build_logs/go_tests.log](../build_logs/go_tests.log); [results/generated/smt_summary.json](../results/generated/smt_summary.json)

**Recorded status.** EXPANDED_SOURCE_BOUND_LEAN_GATE_PASS

### C11: Appendix E.3, Lemma E1 and Proposition E3; Section 5 (structural specialization)

**Claim.** Joint lateness of J is realizable iff the repair graph H[J] is acyclic. Under the independent initial-ready pivot and complete-order contracts, coarse unsafety has the weighted subset characterization and, for unit weights, max(d0,d1)<=k and d0+d1<=k+alpha(H).

**Evidence kind.** Mechanized graph/event-order equivalence with paper behavioral and capacity correspondence

**Historical reference.** New repair frontier

**Lean coverage.** GraphRealization.repair_graph_reversal_iff; finite_acyclic_iff_schedule; repair_graph_iff_realizable_schedule; repair_graph_from_covers_iff_schedule; RepairFrontier.directed_unsafe_iff and strict_separation_iff (arithmetic)

**Executable evidence.** 530 directed graphs including loops for k=1..3; 50,363 legal orders; 1,357,209 executions; 13,074 boundary and 4,164 joint-lateness checks; additionally all 219 labelled four-event partial orders via cover edges

**Supporting SMT.** No new SMT proof of the graph-to-execution correspondence

**Scope.** The full graph/order lemma is proved for a strict partial order and distinct repair/vote event kinds; finite event coverage supplies a schedule. The behavioral contribution law, collector coverage and capacity optimization remain separate paper obligations. No capacity formula or alpha(H) premise is assumed by the graph module.

**Unsupported extension.** Extending the initially-ready independent-pivot contract to interdependent protocol behavior or incomplete scheduler order languages without a conformance argument; identifying graph mechanization with full client refinement.

**Artifact paths.** [src/python/twins_scheduler/repair_frontier.py](../src/python/twins_scheduler/repair_frontier.py); [scripts/run_repair_frontier.py](../scripts/run_repair_frontier.py); [results/revision/frontier_summary.json](../results/revision/frontier_summary.json); [formal/lean/SchedulerClosure/RepairFrontier.lean](../formal/lean/SchedulerClosure/RepairFrontier.lean); [formal/lean/SchedulerClosure/GraphRealization.lean](../formal/lean/SchedulerClosure/GraphRealization.lean)

**Recorded status.** GRAPH_ORDER_LEAN_PAPER_BEHAVIOR_FINITE_PASS

### C12: Section 5 (unit-cost special case); Appendix E.4.2, Corollary E1; Appendix F (illustration)

**Claim.** With unit vote weights, unit split costs, no required splits, all keys allowed and fine feasibility, the exact minimum number of optimally chosen split keys is max(0,d0+d1-k-alpha(H)); an at-most-t budget yields optimal capacity min(k,alpha(H)+t).

**Evidence kind.** Paper optimal-set construction plus mechanized quota arithmetic

**Historical reference.** New phase budget

**Lean coverage.** SchedulerClosure.RepairFrontier.split_capacity_bound; SchedulerClosure.RepairFrontier.minimum_phase_splits

**Executable evidence.** 13,074 exhaustive minimum-budget comparisons across the 530 graph domains

**Scope.** Lean proves the budget equivalence assuming the split-capacity expression. The maximum-acyclic-set choice and its graph attainment are paper arguments. Split-key choice is existential.

**Unsupported extension.** Every arbitrary choice of that many exceptions suffices; weighted budget follows from the unit formula; Lean proves the graph optimization itself.

**Artifact paths.** [formal/lean/SchedulerClosure/RepairFrontier.lean](../formal/lean/SchedulerClosure/RepairFrontier.lean); [results/revision/frontier_graph_cases.csv](../results/revision/frontier_graph_cases.csv); [results/revision/frontier_summary.json](../results/revision/frontier_summary.json)

**Recorded status.** PAPER_OPTIMIZATION_FINITE_PASS_LEAN_ARITHMETIC_PASS

### C13: Section 6.1 (retained timing controls); Appendix C (original guarded trace)

**Claim.** Twelve guarded n=4 traces reproduce the canonical baseline/mutant matrix, distinguish repair before and after indispensable precommit issuance, and retain A=0,C=1 in a separate FIFO-compatible gossip control; only P's round-0 logical lock update is omitted.

**Evidence kind.** Authenticated event-level bounded witness and controls

**Historical reference.** New concrete trace

**Lean coverage.** None for the concrete transition model or client; the small abstract output component is separately identified in C15

**Executable evidence.** 12 trace legality audits; 14 dedicated unit tests; 6 canonical cases, 4 direct timing controls, 2 relay controls; all 6 canonical and both relay controls pass admitted-vote FIFO checks

**Scope.** Equal weights, H=1, rounds 0/1, proposer prefix B/C, fixed other type-uniform edges and declared block/relay opportunities; deterministic test-only authentication. Unsupported transition branches are explicit. A and C are unmutated.

**Unsupported extension.** Production CometBFT execution or vulnerability; full refinement; an independent Go mirror; direct late-precommit timing without its non-FIFO qualification; silently treating the relay skeleton as the original bound.

**Artifact paths.** [src/python/twins_scheduler/concrete_trace.py](../src/python/twins_scheduler/concrete_trace.py); [scripts/run_concrete_trace.py](../scripts/run_concrete_trace.py); [tests/unit/test_concrete_trace.py](../tests/unit/test_concrete_trace.py); [results/new/concrete_trace.json](../results/new/concrete_trace.json); [results/new/concrete_trace.csv](../results/new/concrete_trace.csv); [docs/research/CONCRETE_TRACE.md](../docs/research/CONCRETE_TRACE.md)

**Recorded status.** BOUNDED_12_CASES_14_TESTS_PASS

### C14: Appendix E.4.3 (weighted common-frontier interval); Section 5 (indivisible support)

**Claim.** A weighted coarse witness exists iff an attainable forced-early subset weight x satisfies max(0,d0-WL)<=x and x+d1<=W; indivisible weights prevent replacing attainable sums by a continuous total-capacity inequality.

**Evidence kind.** Weighted admission interval under a common-frontier contract

**Historical reference.** New weighted boundary

**Lean coverage.** SchedulerClosure.RepairFrontier.weighted_admission_interval; SchedulerClosure.RepairFrontier.weighted_granularity_counterexample

**Executable evidence.** 258 weighted domains, weights in {1,2,3}, up to 3 pivots; 15,700 boundary checks using extremal late order and all admissions; explicit weights (2,2), deficits (1,3) control

**Scope.** The attainable-subset predicate is retained in Lean. Common-frontier scheduling reduction and subset interpretation are separate paper arguments; the sweep is not all order permutations.

**Unsupported extension.** Continuous-weight substitution; arbitrary weighted graph scheduling discharged by the interval lemma; weighted or dynamic-validator CometBFT refinement.

**Artifact paths.** [formal/lean/SchedulerClosure/RepairFrontier.lean](../formal/lean/SchedulerClosure/RepairFrontier.lean); [results/revision/frontier_weighted_cases.csv](../results/revision/frontier_weighted_cases.csv); [results/revision/frontier_summary.json](../results/revision/frontier_summary.json)

**Recorded status.** WEIGHTED_INTERVAL_LEAN_FINITE_PASS

### C15: Section 6.1 (signature-time repair boundary); Appendix E.2 (persistence obligation)

**Claim.** Repair can prevent a prospective second signature but cannot erase an already recorded signed output; the supplied output-machine trace and concrete executions demonstrate repair before a collector can be too late.

**Evidence kind.** Small output-machine theorem and concrete timing counterexample

**Historical reference.** New persistent-output boundary

**Lean coverage.** SchedulerClosure.RepairFrontier.repair_preserves_signed_output; SchedulerClosure.RepairFrontier.late_repair_before_certificate_is_unsafe; SchedulerClosure.RepairFrontier.repair_before_second_vote_is_safe; SchedulerClosure.RepairFrontier.closed_edge_still_permits_second_vote

**Executable evidence.** Frontier immutable-output control; concrete direct and FIFO-compatible relay late-repair cases; direct transport inversion is explicitly diagnosed

**Scope.** The Lean output machine is deliberately small; signed/enqueued support persists under its transitions. The concrete protocol trace independently instantiates the issue inside its declared bound.

**Unsupported extension.** Treating the toy output machine as a production transition proof; requiring every late repair to cause disagreement; using only the second decision as the repair deadline.

**Artifact paths.** [formal/lean/SchedulerClosure/RepairFrontier.lean](../formal/lean/SchedulerClosure/RepairFrontier.lean); [results/revision/frontier_summary.json](../results/revision/frontier_summary.json); [results/new/concrete_trace.json](../results/new/concrete_trace.json)

**Recorded status.** ABSTRACT_OUTPUT_LEAN_CONCRETE_PASS

### C16: Appendix A.2 (independent-pivot complexity); Appendix E.4.3

**Claim.** Coarse unsafe reachability is NP-complete when the finite unit-weight independent-pivot opportunity schema and k are inputs, via the classical symmetric-orientation/independent-set construction.

**Evidence kind.** Paper complexity proof using a classical reduction

**Historical reference.** New complexity appendix

**Lean coverage.** None

**Executable evidence.** No finite enumeration is offered as proof of the complexity result; the paper supplies the reduction and polynomial certificate verification

**Supporting SMT.** None

**Scope.** The explicit abstract opportunity schema with complete-order coverage; graph size varies. Classical graph hardness is credited rather than claimed as new.

**Unsupported extension.** A hardness result for the fixed n=4 trace or a production client; every constructed opportunity order is protocol-realizable; kernel checking of the reduction.

**Artifact paths.** [manuscript/markdown/appendices.md](../manuscript/markdown/appendices.md)

**Recorded status.** PAPER_PROOF_ONLY

### C17: Section 6.1 (guarded-model source pin); Section 6.3 (native source identity)

**Claim.** The new trace cites exact CometBFT v0.39.3 commit 49b82838fcca442b2445f76605c101609ed04130; the older upstream_fragments snapshot is correctly retained as v0.40.0.

**Evidence kind.** Primary-source integrity and attribution

**Historical reference.** New exact source provenance

**Lean coverage.** None

**Executable evidence.** Exact GitHub tag/commit receipts, Git blob identifiers and SHA-256 manifests; documented inspection of the exercised guards

**Supporting SMT.** None

**Scope.** Source verification proves identity of the evidence files; it does not prove execution equivalence. v0.39.3 state path is consensus/state.go, while local source fixtures have .go.txt suffixes.

**Unsupported extension.** Calling the old v0.40.0 fixture v0.39.3; equating source-fragment matches or immutable hashes with client conformance.

**Artifact paths.** [models/tendermint_style/upstream_v0393/SOURCE.json](../models/tendermint_style/upstream_v0393/SOURCE.json); [models/tendermint_style/upstream_v0393/GITHUB_RECEIPTS.json](../models/tendermint_style/upstream_v0393/GITHUB_RECEIPTS.json); [models/tendermint_style/upstream_v0393/MANIFEST.sha256](../models/tendermint_style/upstream_v0393/MANIFEST.sha256); [docs/research/LITERATURE_AND_PROVENANCE_AUDIT.md](../docs/research/LITERATURE_AND_PROVENANCE_AUDIT.md)

**Recorded status.** SOURCE_IDENTITY_VERIFIED

### C18: Section 5, Theorem 6 (weighted refinement characterization); Appendix E.5 (construction)

**Claim.** Positive integer vote weights, nonnegative split costs and allowed/required keys admit exactly the four-role partition T,J,X,Y with H[J] acyclic and both guaranteed support quotas met. Minimizing split cost yields a legal independent-pivot model witness of minimum control cost.

**Evidence kind.** Paper characterization plus exact constructive algorithm

**Historical reference.** Second revision: weighted synthesis

**Lean coverage.** GraphRealization realizes selected reversals; the full weighted four-role correspondence is not mechanized.

**Executable evidence.** 35,223 raw-event optimum comparisons and independent certificate checks; separate 3,253-case arbitrary-order oracle; 12 dedicated tests.

**Scope.** Initially-ready independent pivots, first signatures exactly when the corresponding enabling admissions are true, actual enabling/repair availability on first-certificate-feasible executions, and full opportunity-order coverage. X guarantees first support but may supply a bonus second vote. Costs are supplied inputs; all slots survive suppression. Exponential in largest loop-free SCC and pseudo-polynomial in quotas. Its explicit general-LTS specialization bridge is separately checked in C33.

**Unsupported extension.** A formula newly discovered for prescribed unit-cost S; automatic contract extraction; polynomial-time optimization or verification on all inputs; treating resource limits as infeasibility.

**Artifact paths.** [src/python/twins_scheduler/refinement_synthesis.py](../src/python/twins_scheduler/refinement_synthesis.py); [scripts/run_refinement_synthesis.py](../scripts/run_refinement_synthesis.py); [scripts/check_synthesis_order_oracle.py](../scripts/check_synthesis_order_oracle.py); [results/synthesis/synthesis_summary.json](../results/synthesis/synthesis_summary.json); [results/synthesis/order_oracle.json](../results/synthesis/order_oracle.json)

**Recorded status.** PAPER_EXACT_SYNTHESIS_ORACLES_PASS

### C19: Appendix E.5, Proposition E4 (Bellman certificate soundness); Section 5

**Claim.** Local Bellman lower-bound inequalities and terminal conditions bound the cost of every feasible represented path. A replayed witness attaining the finite root bound is optimal; an infinite root bound certifies infeasibility.

**Evidence kind.** Mechanized general certificate principle with independent executable checker

**Historical reference.** Second revision: certificates

**Lean coverage.** CertificateOptimality.bellman_path_lower_bound; certified_witness_is_minimum; certified_infeasibility

**Executable evidence.** All 38,476 certificates in the two oracle suites checked independently; 13 full scale certificates retained; suboptimal witness, input substitution, terminal-table corruption and lost-slot controls rejected.

**Scope.** Lean covers arbitrary nonnegative-cost paths and extended-natural potentials, without assuming optimal potentials. Python parsing, graph reconstruction, local enumeration completeness and model replay remain implemented obligations.

**Unsupported extension.** A Lean-verified Python program; trusting only chosen transitions for an optimum; a short polynomial certificate for every instance; a solver resource limit as mathematical infeasibility.

**Artifact paths.** [formal/lean/SchedulerClosure/CertificateOptimality.lean](../formal/lean/SchedulerClosure/CertificateOptimality.lean); [src/python/twins_scheduler/refinement_synthesis.py](../src/python/twins_scheduler/refinement_synthesis.py); [tests/unit/test_refinement_synthesis.py](../tests/unit/test_refinement_synthesis.py); [results/synthesis/certificates/](../results/synthesis/certificates/)

**Recorded status.** BELLMAN_LEAN_CHECKER_CONTROLS_PASS

### C20: Section 5 (non-submodularity and the specified myopic rule)

**Claim.** The unit-weight fixed-split capacity F is not submodular. In the three-key two-cycle family with costs M,1,1 and M>2, the specified immediate-gain-per-cost rule pays M while the optimum is 2, so its approximation ratio is unbounded.

**Evidence kind.** Explicit mathematical counterexample with executable controls

**Historical reference.** Second revision: myopic lower bound

**Lean coverage.** Not mechanized.

**Executable evidence.** M=3,10,100,1000 controls match the proof; ten repeated motifs at k=30 produce certified optimum 20 and myopic cost 1000.

**Scope.** Unit vote weights and full quotas; one completely specified greedy rule. Tie-breaking does not affect the family because only the center has positive initial marginal gain.

**Unsupported extension.** Impossibility for every greedy or heuristic method; representative measured performance against external solvers.

**Artifact paths.** [manuscript/markdown/manuscript.md](../manuscript/markdown/manuscript.md); [results/synthesis/synthesis_summary.json](../results/synthesis/synthesis_summary.json); [results/synthesis/synthesis_benchmarks.csv](../results/synthesis/synthesis_benchmarks.csv)

**Recorded status.** PAPER_COUNTEREXAMPLE_EXECUTED_PASS

### C21: Sections 5 and 6.3 (structural synthesis scale cases)

**Claim.** Of 15 deterministic synthetic domains, 13 have independently certified optima, with largest solved k=48; two exceed the configured largest-component limit 10 and return unknown.

**Evidence kind.** Declared finite structural experiment

**Historical reference.** Second revision: structural scaling

**Lean coverage.** General certificate principle only.

**Executable evidence.** All 13 full certificates saved; weighted 24-pivot W=75 case changes optimum from 0 to 5 as quotas tighten from (60,68) to (74,73).

**Scope.** Synthetic weights/costs and seeded graph families; configured size cutoffs, not observed timeouts. Timing observations are separate and nondeterministic.

**Unsupported extension.** A runtime benchmark victory, production scale guarantee, or infeasibility of the two resource-limited cases.

**Artifact paths.** [results/synthesis/synthesis_benchmarks.csv](../results/synthesis/synthesis_benchmarks.csv); [results/synthesis/certificates/](../results/synthesis/certificates/); [docs/research/REFINEMENT_SYNTHESIS.md](../docs/research/REFINEMENT_SYNTHESIS.md)

**Recorded status.** 13_OPTIMAL_2_UNKNOWN

### C22: Section 6.3 (unchanged native conformance); Section 7.3 (scope)

**Claim.** Four ordinary-operation scenarios execute unchanged CometBFT v0.39.3 at the pinned commit, pass 14 checks, record 32 native Ed25519 votes and 132 events, and preserve the specified semantic outcomes over three repeats plus one race-detector run.

**Evidence kind.** Execution of unchanged native consensus code and independent cryptographic audit

**Historical reference.** Second revision: native conformance

**Lean coverage.** No protocol transition refinement is mechanized.

**Executable evidence.** Native emitted proposals, votes, actual scheduled timeout guards, lock/valid state, proposer priority, missing-block catch-up, in-memory BlockStore and local ABCI. Separate cryptography/OpenSSL audit validates all 32 canonical signed votes. Source and evidence hashes checked.

**Scope.** Four equal-weight validators per finite ordinary scenario; synchronous State dispatch, upstream MockPV test keys and in-memory fixtures. No reactor, sockets, WAL receive loop or persistent signer. Raw native timestamps vary across runs.

**Unsupported extension.** A native mutant disagreement, deployed-client vulnerability, exhaustive safety proof, model-to-client refinement or disk durability guarantee.

**Artifact paths.** [experiments/native_cometbft/](../experiments/native_cometbft/); [results/native/native_summary.json](../results/native/native_summary.json); [results/native/native_provenance.json](../results/native/native_provenance.json); [results/native/native_signature_audit.json](../results/native/native_signature_audit.json); [results/native/native_repeatability.json](../results/native/native_repeatability.json)

**Recorded status.** NATIVE_BASELINE_14_CHECKS_32_SIGNATURES_PASS

### C23: Sections 2 and 3.1, Theorem 1 (exact trace refinement)

**Claim.** A finite labelled path is realizable by a static fine-key policy under split set T exactly when repeated fine-key answers are consistent and every mixed coarse fibre is split. With required Q and allowed D, Q union Mixed is the least feasible split set and attains minimum nonnegative sum cost whenever it is allowed.

**Evidence kind.** Mechanized policy-completion and least-trace-refinement theorem

**Historical reference.** Third revision: general static-policy semantics

**Lean coverage.** TransitionRefinement.policy_realizable_iff; least_split_set; admissible_refinement_exists_iff; minimum_trace_refinement

**Executable evidence.** Total-policy completion, required unused splits, more than two phases, repeated-key contradictions and zero-cost cases in test_transition_synthesis.py; the independent model corpora are counted separately in C31-C33.

**Scope.** All dependence on the selected static policy must be represented by labelled queries. Internal protocol-state dependencies, nondeterminism and finite traces through cyclic or infinite-state relations are permitted. Costs are nonnegative; splitting distinguishes fine keys, not successive answers to the same key.

**Unsupported extension.** Adaptive history-dependent policies; an unlabelled guard secretly consulting the selected policy; negative split costs; claiming an arbitrary implementation has been proved to satisfy the interface.

**Artifact paths.** [formal/lean/SchedulerClosure/TransitionRefinement.lean](../formal/lean/SchedulerClosure/TransitionRefinement.lean); [src/python/twins_scheduler/transition_synthesis.py](../src/python/twins_scheduler/transition_synthesis.py); [tests/unit/test_transition_synthesis.py](../tests/unit/test_transition_synthesis.py); [docs/research/TRANSITION_SYNTHESIS.md](../docs/research/TRANSITION_SYNTHESIS.md)

**Recorded status.** LEAN_TRACE_POLICY_CORRESPONDENCE_PASS

### C24: Section 3.2, Theorem 2 (general minimum-cost synthesis)

**Claim.** For a complete finite explicit transition system, the minimum required/mixed-fibre cost among reachable unsafe states in the product of protocol state and persistent three-valued fine-key memory equals the minimum admissible static refinement cost. Exhaustive absence of unsafe product states proves infeasibility; resource exhaustion returns unknown.

**Evidence kind.** Paper product-reachability equivalence and exact executable search, supported by mechanized memory lemmas

**Historical reference.** Third revision: general finite-state synthesis

**Lean coverage.** TransitionRefinement.query_guard_iff_consistent_extension; remember_occurrences_iff; memory_update_cost_mono; trace_cost_mono. These prove semantic ingredients, not the complete Python product constructor or search implementation.

**Executable evidence.** Priority-queue search supports shared-state dependencies, repeated labels, zero-cost/internal cycles and nondeterministic successors; raw total-policy reachability comparisons in C31 and C32; state/time-limit and merged-state memory controls.

**Scope.** Complete finite supplied graph and finite control alphabet, with at most |S|*3^|F| product states. All finite unsafe-reaching paths of that graph are covered, without an intrinsic path-length bound; bounds encoded by an exporter remain part of its model. Objective is existential safety reachability.

**Unsupported extension.** Reintroducing an independent-pivot prerequisite; polynomial-time search; a universal winning-controller or liveness objective; completeness for omitted implementation transitions or arbitrary unbounded code.

**Artifact paths.** [src/python/twins_scheduler/transition_synthesis.py](../src/python/twins_scheduler/transition_synthesis.py); [tests/unit/test_transition_synthesis.py](../tests/unit/test_transition_synthesis.py); [formal/lean/SchedulerClosure/TransitionRefinement.lean](../formal/lean/SchedulerClosure/TransitionRefinement.lean); [docs/research/TRANSITION_SYNTHESIS.md](../docs/research/TRANSITION_SYNTHESIS.md)

**Recorded status.** PAPER_PRODUCT_EQUIVALENCE_EXECUTABLE_ORACLES_PASS

### C25: Section 3.3, Theorem 3 (closed-set certificate soundness)

**Claim.** A safe strict-cost-sublevel set containing the initial product state when below the bound and closed under every legal input-derived successor below that bound proves a lower bound. A replayed unsafe witness attaining it proves optimality. Safe full successor closure containing the initial state proves infeasibility.

**Evidence kind.** Mechanized certificate principle and separate executable checker

**Historical reference.** Third revision: complete closed-set certificates

**Lean coverage.** TransitionRefinement.sublevel_certificate_lower_bound; sublevel_certified_minimum; closed_certificate_infeasible

**Executable evidence.** Checker independently regenerates successors from the bound input and replays the path; it rejects missing initial/successor states, substituted expensive witnesses, changed expected inputs, malformed integer/Boolean fields and inconsistent repeated answers. Tests disable every optimizer transition/replay helper while verification still succeeds.

**Scope.** Closure and monotone-cost proof principles do not need finite protocol state; the executable checker consumes an explicit finite model and proof set. A safe inductive overapproximation may contain unreachable states. The expected external input, not the self-contained digest alone, binds the claim to the intended model.

**Unsupported extension.** A kernel-verified Python verifier; trusting only listed/chosen proof edges; incomplete exploration as infeasibility; polynomial-size certificates for every input; treating a recomputed self-contained hash as external model authenticity.

**Artifact paths.** [formal/lean/SchedulerClosure/TransitionRefinement.lean](../formal/lean/SchedulerClosure/TransitionRefinement.lean); [src/python/twins_scheduler/transition_synthesis.py](../src/python/twins_scheduler/transition_synthesis.py); [tests/unit/test_transition_synthesis.py](../tests/unit/test_transition_synthesis.py); [results/transition/certificates/](../results/transition/certificates/); [results/transition_bridge/certificates/](../results/transition_bridge/certificates/)

**Recorded status.** LEAN_CUT_SOUNDNESS_INDEPENDENT_CHECKER_PASS

### C26: Section 4.1, Theorem 4 (implementation-model optimality transfer)

**Claim.** Label-preserving coverage of every concrete transition, initial-state coverage, unsafe-state inclusion and the same control/cost interface imply Opt(abstract)<=Opt(concrete). A certified abstract lower bound and actual admissible concrete witness give a cost interval; equality proves the concrete-model optimum. Abstract infeasibility transfers.

**Evidence kind.** Mechanized semantic transfer and executable finite all-edge simulation checker

**Historical reference.** Third revision: all-edge model transfer

**Lean coverage.** TransitionRefinement.labelled_execution_simulates; bad_trace_coverage; abstract_lower_bound_transfers; matching_concrete_witness_is_minimum; abstract_infeasibility_transfers

**Executable evidence.** verify_simulation checks all concrete input edges and the complete scheduler interface; verify_optimality_bridge verifies the abstract certificate and independently replays the concrete witness. Missing-edge, erased-visible-admission, hidden-unsafe-state and mismatched-input controls reject invalid bridges.

**Scope.** The executable checker establishes correspondence between supplied finite models using an internal one-edge match or stutter and exact controlled labels. The semantic theorem can cover infinite concrete systems only when its local simulation obligations are supplied for all relevant transitions. A spurious abstract path gives no concrete upper bound.

**Unsupported extension.** Production-client refinement from a few matching traces; inferring a concrete witness from forward overapproximation alone; hiding a policy query as an internal stutter; equating a labelled finite model with verified native-client extraction.

**Artifact paths.** [formal/lean/SchedulerClosure/TransitionRefinement.lean](../formal/lean/SchedulerClosure/TransitionRefinement.lean); [src/python/twins_scheduler/transition_abstraction.py](../src/python/twins_scheduler/transition_abstraction.py); [tests/unit/test_transition_abstraction.py](../tests/unit/test_transition_abstraction.py); [docs/research/TRANSITION_MECHANIZATION.md](../docs/research/TRANSITION_MECHANIZATION.md); [results/transition_bridge/](../results/transition_bridge/)

**Recorded status.** LEAN_TRANSFER_FINITE_ALL_EDGE_BRIDGE_PASS

### C27: Section 4.2, Theorem 5 (policy elimination and finite progress)

**Claim.** Splitting every existential-quotient block by membership in a safe policy-inductive concrete set eliminates all unsafe quotient paths of that fixed policy. A spurious old policy forces a strict block split. A finite concrete graph permits at most |S_C|-|initial nonempty blocks| failed refinements before an exact result, unless a resource limit intervenes.

**Evidence kind.** Mechanized invariant/policy elimination, paper cardinality bound, and checked executable history

**Historical reference.** Third revision: whole-policy abstraction refinement

**Lean coverage.** TransitionRefinement.invariant_quotient_excludes_goal; invariant_split_saturated; invariant_split_eliminates_policy; spurious_policy_forces_strict_split. The numerical finite-iteration bound is a paper argument.

**Executable evidence.** Every saved iteration checks the complete abstract certificate, safe policy invariant, exact existential quotient shape and strict partition refinement. Histories and eliminated-policy counts are recorded in C32 and C34; a configured zero-refinement limit produces unknown.

**Scope.** Exact existential quotient edges and bad groups come from the supplied complete concrete graph. A safe inductive superset of concrete policy reachability also suffices. The implementation constructs that graph first; it does not automatically infer symbolic invariants from arbitrary code. This instantiates established CEGAR methodology.

**Unsupported extension.** Only one path is excluded while claiming whole-policy elimination; applying elimination to an arbitrary overapproximation with invented edges; a mechanized iteration-count proof or verified Python implementation; invention of general CEGAR; avoidance of initial concrete-state enumeration.

**Artifact paths.** [formal/lean/SchedulerClosure/TransitionRefinement.lean](../formal/lean/SchedulerClosure/TransitionRefinement.lean); [src/python/twins_scheduler/transition_abstraction.py](../src/python/twins_scheduler/transition_abstraction.py); [tests/unit/test_transition_abstraction.py](../tests/unit/test_transition_abstraction.py); [results/transition_bridge/random_oracle.json](../results/transition_bridge/random_oracle.json); [results/transition_bridge/bridge_summary.json](../results/transition_bridge/bridge_summary.json)

**Recorded status.** LEAN_POLICY_ELIMINATION_PAPER_PROGRESS_CHECKED_HISTORY_PASS

### C28: Section 3.2 and Appendix A.1 (finite complexity and unbounded-program boundary)

**Claim.** Cost-bounded static refinement reachability for an explicit finite LTS is NP-complete even with an acyclic graph and exactly two fine keys per coarse fibre, by a cost-preserving Set Cover reduction and polynomial policy/reachability verification. A terminating complete solver for arbitrary unrestricted programs would decide halting even with no controlled keys.

**Evidence kind.** Paper complexity and undecidability reductions to classical problems

**Historical reference.** Third revision: general complexity boundary

**Lean coverage.** Not mechanized.

**Executable evidence.** All 512 ordered three-set families on three universe elements are independently checked against the Set Cover exporter. These are the same 512 cases included in C32, not an additional corpus. No finite check is presented as proof of NP-hardness or undecidability.

**Scope.** Finite decision inputs use binary-encoded nonnegative costs. The halting boundary concerns arbitrary computationally unrestricted programs, not a specific bounded BFT instance. General simulation/invariant theorems can still establish claims about particular infinite systems with proved premises.

**Unsupported extension.** NP-completeness of the fixed n=4 example; unconditional exponential lower bounds; impossibility of all unbounded-program proofs; kernel checking of the reduction; novelty as the invention of minimum-label or specification-revision optimization.

**Artifact paths.** [manuscript/markdown/appendices.md](../manuscript/markdown/appendices.md); [src/python/twins_scheduler/transition_examples.py](../src/python/twins_scheduler/transition_examples.py); [tests/unit/test_transition_synthesis.py](../tests/unit/test_transition_synthesis.py); [scripts/check_transition_oracle.py](../scripts/check_transition_oracle.py); [results/transition_bridge/random_oracle.json](../results/transition_bridge/random_oracle.json)

**Recorded status.** PAPER_REDUCTIONS_EXHAUSTIVE_SMALL_REDUCTION_CHECKS_PASS

### C29: Section 6.1 and Section 6.2 protocol table

**Claim.** The complete declared two-round coupled mutant model has 2,516 states, 5,856 transitions and 16 A/C-disagreement states; its minimum split cost is 2 under costs (5,2), selecting A->P. The corresponding baseline has 2,372 states, 5,574 transitions and no unsafe state. Both controlled fibres affect P shared quorum/state, violating the independent-pivot contribution and initial-readiness assumptions.

**Evidence kind.** Executable guarded protocol model with exact general-LTS certificates

**Historical reference.** Third revision: coupled guarded protocol model

**Lean coverage.** No mechanized proof of this protocol exporter or its correspondence to CometBFT. C23-C27 supply the general mathematical principles.

**Executable evidence.** Seven permission/cost model configurations independently certified; mutant coarse-only infeasible, B->P-only optimum 5, A->P-only optimum 2, required B->P optimum 5, both required optimum 7. The minimum guarded replay yields A=0,C=1 and passes all 12 audits.

**Scope.** n=4 with quorum 3, one explicitly Byzantine B and only P round-0 lock assignment mutated; unmutated A/C define unsafety. Height 1, two rounds, 12 ordered groups and 32 once-only slots, all within-group permutations, atomic bootstrap/proposal/block sequences and declared fixed admissions. Test-only HMAC, actual emitted/received distinct-signer certificates and synthetic control costs.

**Unsupported extension.** Independent pivots secretly assumed by this instance; all schedules of a production BFT client; native mutant execution or deployed vulnerability; suppression automatically implies second-vote readiness; test HMAC is production Ed25519; input costs measure runtime.

**Artifact paths.** [src/python/twins_scheduler/coupled_protocol.py](../src/python/twins_scheduler/coupled_protocol.py); [src/python/twins_scheduler/concrete_trace.py](../src/python/twins_scheduler/concrete_trace.py); [scripts/run_transition_study.py](../scripts/run_transition_study.py); [tests/unit/test_coupled_protocol.py](../tests/unit/test_coupled_protocol.py); [results/transition/summary.json](../results/transition/summary.json); [results/transition/model_cases.csv](../results/transition/model_cases.csv); [results/transition/certificates/](../results/transition/certificates/); [results/transition/coupled_protocol_witness.json.gz](../results/transition/coupled_protocol_witness.json.gz); [docs/research/COUPLED_PROTOCOL_MODEL.md](../docs/research/COUPLED_PROTOCOL_MODEL.md)

**Recorded status.** COUPLED_FINITE_MODEL_EXACT_OPTIMUM_GUARDED_REPLAY_PASS

### C30: Section 6.2 (direct protocol exploration and state-dependent controls)

**Claim.** All 64 total six-key policies in both baseline and mutant are explored directly through guarded protocol code: 128 comparisons agree with exported audit-quotient unsafety and complete reachable state/edge counts after forgetting the same first-arrival diagnostic field. Five saved protocol controls exhibit safe/unsafe orders under one policy, actual block-dependent commit completion, and loss of round advancement when both peer precommits are suppressed.

**Evidence kind.** Fresh protocol-successor exploration versus graph interpretation, plus full guarded controls

**Historical reference.** Third revision: exporter and dependency controls

**Lean coverage.** No protocol-specific transition correspondence to native client code is mechanized.

**Executable evidence.** 128 direct policy checks generate 17,690 states and 42,750 transitions summed over those explorations, with zero mismatches. The optimized witness replays 30 opportunity slots, 172 log events, 16 signed messages and six local certificates, checking every semantic successor and all 12 guard/admission audits.

**Scope.** Direct and exported exploration share the underlying guarded protocol rules; the comparison separately challenges graph construction, not an independently implemented consensus specification. Both count comparisons forget the same non-guard first-arrival diagnostic field. State/edge counts are summed per policy, not unique combined-model states. Atomic environment slots and all bounded assumptions of C29 remain in force.

**Unsupported extension.** 128 distinct protocols; complete state counts for unrestricted client code; an independent implementation of every consensus rule; 16 messages means 16 signers in a certificate; a safe timed opportunity can be reused later without changing the bound.

**Artifact paths.** [src/python/twins_scheduler/coupled_protocol.py](../src/python/twins_scheduler/coupled_protocol.py); [scripts/run_transition_study.py](../scripts/run_transition_study.py); [tests/unit/test_coupled_protocol.py](../tests/unit/test_coupled_protocol.py); [results/transition/direct_policy_checks.csv](../results/transition/direct_policy_checks.csv); [results/transition/coupled_order_controls.json.gz](../results/transition/coupled_order_controls.json.gz); [results/transition/coupled_protocol_witness.json.gz](../results/transition/coupled_protocol_witness.json.gz); [results/transition/summary.json](../results/transition/summary.json)

**Recorded status.** 128_DIRECT_EXPORT_COMPARISONS_FIVE_GUARDED_CONTROLS_PASS

### C31: Section 6.2 (7,904 graph/cost/permission configurations)

**Claim.** The direct product optimizer and its independent certificate checker agree with complete total-policy/split-subset graph reachability on 7,904 configurations: 1,296 graphs times six cost/permission profiles, plus 128 seeded random cases. No optimum or certificate mismatch is observed.

**Evidence kind.** Finite exhaustive-family and seeded executable oracle study

**Historical reference.** Third revision: general direct-synthesis oracle

**Lean coverage.** General semantic/certificate principles only; finite enumeration is not a proof of Python correctness.

**Executable evidence.** 7,776 exhaustive configurations plus 128 random configurations; 35,368 total-policy enumerations and 40,008 compatible policy/split pairs; 7,904 independent certificate checks and zero mismatches. Six semantic example models and the seven coupled configurations are separately recorded, not added to the 7,904 count.

**Scope.** The exhaustive family has three states and four fixed directed positions, each with six absent/internal/Boolean-label choices. It is not every directed three-state graph. Random seed 20261019 generates 128 systems with 4-8 states and 3-6 fine keys. Counts are configurations/enumerations, not distinct protocols or globally unique policies.

**Unsupported extension.** Exhaustive coverage of arbitrary finite transition systems; a proof that the implementation has no bugs; adding repeated semantic examples or other study counters as disjoint new protocols; a runtime ranking.

**Artifact paths.** [scripts/run_transition_study.py](../scripts/run_transition_study.py); [src/python/twins_scheduler/coupled_protocol.py](../src/python/twins_scheduler/coupled_protocol.py); [results/transition/oracle_cases.csv](../results/transition/oracle_cases.csv); [results/transition/summary.json](../results/transition/summary.json); [results/transition/semantic_examples.json](../results/transition/semantic_examples.json)

**Recorded status.** 7904_CONFIGURATION_ORACLE_CERTIFICATES_PASS

### C32: Section 6.2 (2,960-instance standalone oracle)

**Claim.** An independently coded raw total-policy/split-subset reachability oracle agrees with both direct synthesis and iterative abstraction on 2,960 instances: 400 seeded systems, 2,048 exhaustive edge/cost/constraint configurations and 512 Set Cover reductions. It checks 5,920 optimum comparisons and all 6,857 saved abstract iterations, with zero mismatches.

**Evidence kind.** Reproducible three-family cross-algorithm and certificate-history audit

**Historical reference.** Third revision: independent direct-and-CEGAR audit

**Lean coverage.** General semantic, certificate and invariant-elimination principles; the audited programs themselves are not mechanized.

**Executable evidence.** 2,960 direct certificates and 2,960 full abstraction-run checks; all 6,857 abstract certificates comprise 2,960 final and 3,897 rejected iterations, with each eliminated-policy step checked. 291,804 policy/split pairs after permission filtering, of which 132,626 satisfy fibre coherence; 4,096 independent cover-subset checks. Exact input/outcome hashes and all generator settings are recorded; no runtimes enter deterministic output.

**Scope.** The 5,920 comparisons are two methods on the same 2,960 instances. The 6,857 iterations and 3,897 policy eliminations are events within those runs, not extra independent model instances. The 2,048 and 512 families also appear in unit tests; the 512 reductions are the evidence in C28. Cross-study inputs are not deduplicated into a global unique-protocol corpus.

**Unsupported extension.** Adding all these counters as distinct test cases or protocols; counting the same Set Cover/unit-test instances twice; exhaustive arbitrary-LTS coverage; general performance superiority from this audit.

**Artifact paths.** [scripts/check_transition_oracle.py](../scripts/check_transition_oracle.py); [src/python/twins_scheduler/transition_examples.py](../src/python/twins_scheduler/transition_examples.py); [results/transition_bridge/random_oracle.json](../results/transition_bridge/random_oracle.json); [tests/unit/test_transition_synthesis.py](../tests/unit/test_transition_synthesis.py); [tests/unit/test_transition_abstraction.py](../tests/unit/test_transition_abstraction.py)

**Recorded status.** 2960_INSTANCES_5920_COMPARISONS_6857_ITERATIONS_PASS

### C33: Section 5 (explicit pivot-to-general-LTS adapter); Theorem 6 and Appendix E.3-E.5

**Claim.** For the stated initially-ready independent-pivot contract, the explicit enabling/repair/immutable-signature LTS and the weighted four-role problem have equal optima. Every general unsafe witness normalizes selected splits to E=1,R=0 without deleting event slots or increasing cost. A 1,507-query study confirms both solvers against a raw four-pattern admission/order oracle.

**Evidence kind.** Paper specialization proof, independent exporter, and cross-solver/raw-oracle checks

**Historical reference.** Third revision: executable structural specialization

**Lean coverage.** Graph/order and memory/certificate components are mechanized; the exporter, full specialization normalization and weighted four-role optimization are not kernel-checked.

**Executable evidence.** 1,507 queries produce 3,014 optimum comparisons and 3,014 certificate checks with zero mismatches. The raw oracle covers 221 order domains, 963 legal orders and 15,372 Boolean-policy/order executions. All 1,189 feasible general witnesses normalize at equal cost. All 18 graphs with k<=2 including loops and all 219 labelled four-event posets are represented; maximum export is 199 states and 398 transitions.

**Scope.** Positive integer weights; nonnegative costs; allowed/required sets; initial readiness, first signatures exactly when the corresponding enabling admissions are true, enabling/repair availability on first-certificate-feasible executions, independent contribution laws and complete opportunity coverage. Includes reversed E=0,R=1 fine policies before normalization. The 1,507 count comprises 706 all-quota graph queries, 144 permission controls and 657 poset/quota queries; reused graph/poset families are not additional unique protocols.

**Unsupported extension.** Automatic extraction of this contract from arbitrary code; omitting suppressed slots or transitive constraints; equality of all traces rather than optimum/unsafe feasibility; calling the raw exporter or normalization Lean-verified; adding 3,014 comparisons as 3,014 distinct input models.

**Artifact paths.** [src/python/twins_scheduler/transition_pivot_adapter.py](../src/python/twins_scheduler/transition_pivot_adapter.py); [tests/unit/test_transition_pivot_adapter.py](../tests/unit/test_transition_pivot_adapter.py); [scripts/check_transition_specialization.py](../scripts/check_transition_specialization.py); [results/transition_bridge/specialization_oracle.json](../results/transition_bridge/specialization_oracle.json); [docs/research/TRANSITION_SYNTHESIS.md](../docs/research/TRANSITION_SYNTHESIS.md)

**Recorded status.** 1507_SPECIALIZATION_QUERIES_1189_NORMALIZATIONS_PASS

### C34: Section 6.2 (general synthesis and protocol abstraction table)

**Claim.** Nine saved abstraction runs pass all-edge simulation, certificate checks for all 32 iterations (nine final and 23 rejected), and 23 policy-elimination checks. Starting from one block, the 2,516-state coupled mutant reaches a 26-state, 60-edge abstraction in 12 iterations; its certified cost-2 lower bound matches the guarded concrete witness and proves the bounded concrete optimum.

**Evidence kind.** Complete saved CEGAR histories with model-to-model optimality transfer

**Historical reference.** Third revision: checked protocol abstraction runs

**Lean coverage.** The principles in C26-C27; finite instance construction and all Python checks remain executable obligations.

**Executable evidence.** Complete input/certificate history for all nine runs; 11 false policies eliminated in the coarsest-start coupled mutant run. The supplied audit-field quotient certifies the same optimum in one iteration at 1,978 states/4,628 edges; the 2,372-state baseline is certified infeasible from one abstract state. Both concrete mutant replays pass 12 guard audits.

**Scope.** The nine runs reuse six semantic examples plus two different abstraction starts for the same coupled mutant and one baseline. They are not nine independent protocols and are separate from the 6,857-iteration standalone audit. The audit-field quotient deliberately forgets a non-guard history field; its compression is not a competitive benchmark. The complete concrete graph was built before CEGAR.

**Unsupported extension.** 26 states model every execution of CometBFT; avoiding concrete graph construction; measured superiority to other synthesis/model-checking tools; counting two abstraction starts as two distinct mutant protocols; a model-to-production-client refinement.

**Artifact paths.** [scripts/run_transition_bridge.py](../scripts/run_transition_bridge.py); [src/python/twins_scheduler/transition_abstraction.py](../src/python/twins_scheduler/transition_abstraction.py); [results/transition_bridge/bridge_summary.json](../results/transition_bridge/bridge_summary.json); [results/transition_bridge/certificates/](../results/transition_bridge/certificates/); [results/transition_bridge/replays/](../results/transition_bridge/replays/)

**Recorded status.** NINE_CHECKED_BRIDGES_32_ITERATIONS_COUPLED_OPTIMUM_PASS

### C35: Section 7.1; semantic components of Theorems 1-5

**Claim.** Nineteen selected TransitionRefinement declarations mechanize static-policy completion and least required/mixed cost, persistent-memory consistency and monotonicity, strict/full-closure certificates, labelled simulation and cost-bound transfer, and invariant-guided whole-policy elimination with strict splitting. Together with retained results, the integrated audit has 46 declarations, a 15-job build and hygiene checks on 23 Lean/Coq files.

**Evidence kind.** Kernel-checked semantic results with explicit nonmechanized implementation boundary

**Historical reference.** Third revision: expanded mechanized semantic scope

**Lean coverage.** TransitionRefinement declarations selected in AxiomAudit.lean; full mapping in ARTIFACT_THEOREM_MAP.md and TRANSITION_MECHANIZATION.md; all reported standard axiom dependencies in AXIOM_REPORT.md.

**Executable evidence.** Source-bound successful lake build, selected #print axioms audit and independent leanchecker SchedulerClosure exits are recorded in results/generated/lean_verification.json; checked source hashes match. Source hygiene reports no admitted proofs, user-declared axioms or unsafe declarations in its 23-file scope.

**Scope.** General semantic proofs need neither finite protocol state nor pivot independence when their stated premises hold. The finite iteration-count bound, full weighted partition correspondence, executable product construction, Python search/checker/exporter and production-client correspondence remain paper or executable obligations. This is the same integrated gate counted in C10, not an additional build or corpus.

**Unsupported extension.** 46 separately verified protocols; all paper arguments are fully mechanized; kernel verification of Python or native code; a proved production implementation relation; counting standard Lean axioms as newly introduced user assumptions or omitting their recorded dependencies.

**Artifact paths.** [formal/lean/SchedulerClosure/TransitionRefinement.lean](../formal/lean/SchedulerClosure/TransitionRefinement.lean); [formal/lean/AxiomAudit.lean](../formal/lean/AxiomAudit.lean); [formal/lean/AXIOM_REPORT.md](../formal/lean/AXIOM_REPORT.md); [formal/lean/ARTIFACT_THEOREM_MAP.md](../formal/lean/ARTIFACT_THEOREM_MAP.md); [docs/research/TRANSITION_MECHANIZATION.md](../docs/research/TRANSITION_MECHANIZATION.md); [results/generated/lean_verification.json](../results/generated/lean_verification.json); [build_logs/lean_build.log](../build_logs/lean_build.log); [build_logs/lean_axiom_audit.log](../build_logs/lean_axiom_audit.log); [build_logs/leanchecker.log](../build_logs/leanchecker.log); [build_logs/formal_verification.log](../build_logs/formal_verification.log)

**Recorded status.** LEAN_POLICY_MEMORY_CUT_TRANSFER_INVARIANT_SCOPE_PASS
