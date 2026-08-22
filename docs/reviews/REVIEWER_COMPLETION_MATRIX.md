# Reviewer completion matrix

Statuses below refer to the canonical repository and fresh logs, not inherited gate reports.

| Requirement | Correction | Source / proof | Manuscript | Status |
|---|---|---|---|---|
| Natural protocol bridge | Explicit pivot, `E`, `R`, `C0`, `C1`, shared edge, distinct phases, baseline/mutation and correct decisions | `CometBFTInstantiation.lean`; `bounded.py`; Go mirror; cross-language log | §6, Proposition 2 | PASS |
| Structural quorum-pivot criterion | Ten separately stated structural and decision premises; family is a corollary | `QuorumPivotCriterion.lean`; `ParametricFamily.lean` | §4, Theorem 2 / Corollary 1 | PASS |
| Replay projection and outputs | Both congruences, stable-key projection, duplicate stutter/silence, output trace | `ReplayErasure.lean`; T1 SMT/certificates | §7, Theorem 3 | PASS |
| Relational closure legality | Merged-trace lemma separated from scheduler-language corollary | `ClosureLifting.lean`; T2 SMT | §3 | PASS |
| `UnsafeObs` typing | State predicate is applied to terminal state before observation | `UnsafeObservations.lean` | §2.2 | PASS |
| Scheduler semantics | Exact `A_D`, `A_T`, type closure and stable emitted-envelope filter | `SchedulerSemantics.lean`; independent checker | §§2.3--2.4 | PASS |
| Explicit `(P_f,B_f)` | Fixed finite values/phases/messages/edges/order/observation/decision semantics | family and bounded model sources | §4.2 | PASS |
| Seven-premise algebra | Paper Boolean derivation precedes exhaustive cross-check | `PremiseBoundary.lean`; T6 SMT | §5, Proposition 1 | PASS |
| External theorem numbering | Only Theorems 1--3 in paper; internal IDs confined to ledgers | claim ledger and artifact map | entire manuscript | PASS |
| Related-work matrix | Adds required systems, conformance and mechanization columns; novelty is property-level | `docs/research/RELATED_WORK_CAPABILITY_MATRIX.*` | §9 | PASS |
| Mature-prover assurance | Lean library, axiom audit and `leanchecker` built on pinned toolchain | `formal/lean/AXIOM_REPORT.md`; logs | §8.2 | PASS |

See `docs/CLAIM_EVIDENCE_LEDGER.md` for exact claim boundaries and prohibited extensions.
