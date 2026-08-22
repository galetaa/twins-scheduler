# Reviewer completion matrix

| # | Requested change | Implementation | Evidence | Status |
|---:|---|---|---|---|
| 1 | Connect the central theorem to one natural BFT protocol | Bounded rule-level CometBFT/Tendermint locking instantiation with explicit `p,E,R,C0,C1`, lock/commit predicates, same edge, exact phase order, and independent Python/Go models | `protocol_instantiation/`, `src/cometbft_bounded.py`, `go/cometbft_refinement/`, manuscript §6 | **PASS — bounded rule-level refinement** |
| 2 | Add an intermediate structural theorem | New quorum-pivot separation criterion; parametric `3f+1` family is a corollary | manuscript §4.1–4.2; `QuorumPivotCriterion.lean`; `ParametricFamily.lean` | **PASS** |
| 3 | Fix replay output-trace gap | Added output congruence and duplicate-output silence; theorem preserves projection and output trace | manuscript §7; `ReplayErasure.lean`; kernel 1.1.0; SMT | **PASS** |
| 4 | Repair `UnsafeObs` typing | `Unsafe` is applied to terminal state; observation is taken afterwards | manuscript §2.2; `UnsafeObservations.lean` | **PASS** |
| 5 | Formalize scheduler semantics | Defined `A_D`, `A_T`, type closure, emitted envelopes, stable filter, no synthesis, stable order, once-only delivery, and controlled-edge scope | manuscript §2.3–2.4; `SchedulerSemantics.lean`; independent checker | **PASS** |
| 6 | State theorem over `P_f,B_f` | Exact protocol family and bounded domain now appear in theorem/corollary statement | manuscript §4.2 | **PASS** |
| 7 | Require a legal target closure trace | Split merged-trace lemma from legal scheduler-language corollary | manuscript §3; `ClosureLifting.lean` | **PASS** |
| 8 | Show the Boolean simplification on paper | Added values of `U(1,0)`, `U(0,0)`, `U(1,1)` and stepwise conjunction simplification | manuscript §5 | **PASS** |
| 9 | Remove internal T1/T2/T3/T6 names | Main manuscript uses Theorems 1–3 only; internal mapping moved to artifact file | manuscript; `formal/lean/ARTIFACT_THEOREM_MAP.md` | **PASS** |
| 10 | Actually compile Lean or Coq | Pinned Lean project, no-sorry CI, axiom audit, strict reproduction hook prepared; local compiler unavailable and outbound retrieval blocked | `formal/lean/`, `.github/workflows/lean.yml`, `results/final/external_tool_status.json` | **NOT RUN — external toolchain blocker** |
| 11 | Do not add more random executions | No expanded random campaign; effort moved to proofs and protocol refinement | final design | **PASS** |
| 12 | Keep seven flags diagnostic | Repositioned as a diagnostic exact abstraction, not universal characterization | manuscript §5 | **PASS** |
| 13 | Keep replay secondary | Replay moved after main phase-erasure and protocol-instantiation story | manuscript §7 | **PASS** |
| 14 | Reduce repeated disclaimers | Consolidated scope and limitations; removed audit-response repetition | manuscript §§1.2, 10 | **PASS** |
| 15 | Clean assurance language | Distinguishes executed evidence, project-local kernel, source-only mature prover, and review PDF | manuscript §8; final reports | **PASS** |
| 16 | Sharpen related work with a matrix | Added scheduler/property/separation capability matrix | manuscript §9; `prior_art/RELATED_WORK_MATRIX_2026-08-21.*` | **PASS** |
| 17 | Reorder contributions | Quorum-pivot mechanism first; closure theorem second; family/diagnostic third; replay secondary | manuscript §1.1 | **PASS** |
| 18 | One-command artifact | `./reproduce.sh` executes all available evidence and probes external checks | `reproduce.sh`; `REPRODUCTION.md` | **PASS** |

## Completion interpretation

Seventeen requested changes are implemented and executable where they do not depend on an unavailable external compiler. Item 10 is source-complete and CI-ready but was not executed locally. It remains a submission blocker and is not represented as completed merely because the files exist.
