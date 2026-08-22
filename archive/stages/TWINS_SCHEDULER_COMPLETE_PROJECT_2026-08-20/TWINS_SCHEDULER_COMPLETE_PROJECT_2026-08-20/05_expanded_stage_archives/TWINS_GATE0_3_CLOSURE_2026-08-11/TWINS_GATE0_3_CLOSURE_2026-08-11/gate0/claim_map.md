# Gate 0 — Claim and novelty map

**Decision date:** 11 August 2026  
**Status:** CLOSED — **NO-GO** for the finite-clone-number theorem; **PIVOT CANDIDATE** for concrete harness conformance.

## Classification

| Claim | Classification | Evidence or derivation | Consequence |
|---|---|---|---|
| C1. Shared-identity correct-code copies reproduce important equivocation, double-voting and state-loss attacks. | KNOWN | Twins, OPODIS 2021, DOI `10.4230/LIPIcs.OPODIS.2021.7`. | Not a novelty claim. |
| C2. Arbitrary Byzantine behavior is generally equivalent to correct-code clones. | KILLED AS STATED | VLSM proves Byzantine/equivocation trace equivalence only for validators and its validity model; ByzzFuzz exhibits mutation behaviors outside unmodified correct-code Twins. | Core model must be validator-only accepted-message behavior. |
| C3. Dynamic state equivocation is an adequate abstract baseline for honest-validator observations. | KNOWN, CONDITIONAL | VLSM, arXiv `2202.12662v4`, Theorems 6.1, 7.1 and limited variants. | The broad abstract theorem is not new. |
| C4. Every finite dynamic-equivocation trace can be realized by finitely many persistent genesis clones. | DERIVABLE, GENERIC | Static-unfolding construction in `theorem_candidate.md`: one clone per chain in a finite cover of local faulty histories. | Finite realizability is not a new BFT theorem under the selected scheduler powers. |
| C5. A fixed persistent cap `k` is more restrictive than unbounded dynamic equivocation. | KNOWN/DEFINITIONAL | A persistent clone executes one causally consistent local history; `k` clones cover at most `k` incompatible histories. | Only the minimization problem remains. |
| C6. Minimum clone count is a protocol-specific scientific quantity. | KILLED IN CURRENT MODEL | Under exact history-preserving observation, `k_min` is the minimum chain cover, equal to poset width by Dilworth. | The proposed quantity is generic combinatorics unless extra concrete constraints are added. |
| C7. A cap on simultaneously active snapshot clones yields a meaningful hierarchy. | KILLED | With restart/replay, unbounded message delay and interleaving-insensitive observation, one active slot sequentially replays every finite branch. | `SnapshotDynamic(k)` was ill-posed: active count collapses to `k=1`. |
| C8. A causal-width characterization is novel. | KILLED | It is precisely a chain-cover/antichain-width characterization under the model's own compatibility relation. | Renaming it does not create novelty. |
| C9. Lifecycle and scheduler restrictions may create completeness boundaries. | CONDITIONAL, SURVIVES AS PIVOT | Concrete implementations use round/view partition scenarios rather than the ideal unrestricted per-message semantics; exact conformance remains unproved. | This is a different research question requiring a new Gate 0. |
| C10. The finite-clone result collapses to ordinary chain cover. | CONFIRMED | Formal construction plus exact pilot. | Triggers Gate 3 NO-GO rule. |
| C11. Two persistent clones suffice for all bounded binary safety witnesses in the pilot. | CONFIRMED ONLY FOR PILOT | Exact event-state exploration: `UnsafeAE = UnsafeAT_static(2)`; `UnsafeAT_static(1)=∅`. | Cannot be generalized without a protocol-class proof. |
| C12. A concrete Twins harness conforms to ideal `AT(k)` semantics. | UNKNOWN, POTENTIALLY NEW | Twins simulator and `relab/hotstuff` use generated per-view network partitions. No refinement proof was found. | Only defensible pivot left by Gates 0–3. |

## Novelty delta after Gate 0

The finite-clone-number contribution does **not** survive. The only residual candidate is:

> Characterize the trace-language gap between ideal per-message state-equivocation semantics and a concrete round/view-partition Twins harness, including the smallest safety witness that requires a delivery relation not representable by the harness scenario language.

This residual is not approved automatically. It needs a new prior-art search covering scenario-language expressiveness, partition schedules, conformance testing, communication closure and implementation refinement.
