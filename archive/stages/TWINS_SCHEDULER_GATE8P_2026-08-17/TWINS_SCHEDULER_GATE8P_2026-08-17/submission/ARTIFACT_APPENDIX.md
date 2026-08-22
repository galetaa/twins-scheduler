# Artifact Appendix and Evaluation Map

## Artifact purpose

The artifact substantiates four formal results (T1, T2, T3, T6), the fuller event-loop validation, the cross-kernel bounded evidence, sensitivity checks, generated figures/tables, and the sentence-level claim audit. It is designed for offline reproduction on a Linux-compatible host.

## Entry points

| Goal | Command or path | Expected result |
|---|---|---|
| Full Gate 8 reproduction | `./scripts/reproduce_gate8p.sh` | Gate 7 evidence, legacy exact kernels, claim audit, and manuscript PDF validate |
| Core Gate 7 evidence only | `./scripts/reproduce_gate7p.sh` | 17 tests; positive/negative SMT outcomes; manifests pass |
| Legacy exact kernels | nested archive under `legacy_evidence/` | Gate 5 reproduction passes and regenerates cross-protocol results |
| Read theorem ledger | `results/gate7p/gate7p_theorem_ledger.json` | T1/T2/T3/T6 statements and scopes |
| Inspect claim traceability | `manuscript/CLAIM_EVIDENCE_AUDIT.md` | each load-bearing claim mapped to evidence |
| Inspect proof limits | `gate8p/PROOF_ASSURANCE_BLOCKER.md` | exact trusted-base and submission blocker |
| Read paper | `manuscript/FULL_MANUSCRIPT.md` or PDF | complete anonymous manuscript draft |

## Decisive result mapping

- **T1 replay erasure:** `proofs_smt/T1_REPLAY_ERASURE.horn.smt2`, `proof_outputs/T1_REPLAY_ERASURE_horn.out`, `results/gate7p/t1_replay_erasure_proof_check.json`.
- **T2 closure lifting:** `proofs_smt/T2_LOCAL_VCS.smt2`, `proofs_smt/T2_PREFIX_RELATION.horn.smt2`, corresponding outputs, and checked certificate.
- **T3 quorum pivot:** `proofs_smt/T3_QUORUM_PIVOT.smt2`, `results/gate7p/t3_bigint_crosscheck.json`, fuller event loop, and checked certificate.
- **T6 premise boundary:** `proofs_smt/T6_PREMISE_CHARACTERIZATION.smt2`, `results/gate7p/premise_truth_table.csv`, and symbolic result JSON.
- **Negative controls:** `proofs_smt/negative_controls/` and `proof_outputs/NC*`.
- **Operational validation:** `results/gate7p/full_event_loop_*` and `implementation_fixture/full_event_loop/`.
- **Cross-kernel evidence:** `legacy_evidence/TWINS_SCHEDULER_GATE5P_2026-08-15.zip`.

## Expected resource envelope

The Gate 7 core route previously completed in seconds on the recorded host. The nested Gate 5 exact-kernel route takes tens of seconds and is the longest default stage. No GPU, mainnet access, archive node, cloud service, private key, or external dataset is required. The reproduction scripts should make no network calls.

## Artifact-evaluation criteria

The package is structured to support consistency, reproducibility, completeness, documentation, and reuse. A final public artifact should be deposited in a persistent repository with a DOI, and a container should be added if required by the selected venue. The current local archive has deterministic hashes but no public DOI.

## Known limitation

The Lean directory is a migration scaffold. It did not build in the current environment because Lean/Lake were unavailable and must not be counted as a kernel-checked proof. See `formal/lean/BUILD_ATTEMPT_2026-08-17.md`.
