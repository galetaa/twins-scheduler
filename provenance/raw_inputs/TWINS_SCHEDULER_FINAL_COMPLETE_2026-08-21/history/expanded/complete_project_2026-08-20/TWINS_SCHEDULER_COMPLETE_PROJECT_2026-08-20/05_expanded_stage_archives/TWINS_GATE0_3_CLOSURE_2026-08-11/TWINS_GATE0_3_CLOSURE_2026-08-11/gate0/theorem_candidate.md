# Gate 0 — Exact theorem candidate and collapse proof

## 1. Corrected semantic split

The earlier symbol `AT(k)` conflated two different resources:

1. `AT_total(k)`: at most `k` clone histories exist during the whole execution; clones may be persistent from genesis or spawned, but every distinct branch consumes one of the `k` total histories.
2. `AT_active(k)`: at most `k` physical clone slots are simultaneously active; a slot may be stopped, reset or restored and reused later.

These models are not equivalent in an asynchronous safety setting.

## 2. Assumptions

Let `P` be a deterministic authenticated message-passing protocol. Fix one faulty protocol identity and a finite dynamic state-equivocation execution `t`. Assume:

- A1. Every faulty branch executes the same deterministic correct transition function after its explicit inputs are fixed.
- A2. Every state copied by the abstract model is reachable by replaying the finite causal input history of that state.
- A3. The scheduler can deliver inputs separately to physical clones.
- A4. Messages emitted by a clone need not be delivered, and undelivered emissions are erased by the observation.
- A5. The network permits arbitrary finite delay and reordering; no deadline or fairness obligation is part of safety.
- A6. Physical clone identifiers are erased to the common protocol identity.
- A7. The observation is invariant under reordering of causally independent events.

These are the powers granted by the proposed primary formal model; weakening them defines a different harness-conformance problem.

## 3. Faulty-history poset

Let `H(t)` be the finite set of relevant faulty local actions retained by the observation, ordered by membership in one causally consistent correct local history. A chain is a subset realizable by one deterministic correct-code execution. A chain cover partitions `H(t)` into such histories. Let `cc(t)` be the minimum number of chains.

## 4. Static unfolding theorem

**Theorem G0-T1.** Under A1–A7, every finite dynamic state-equivocation trace `t` has an observationally equivalent `AT_total(cc(t))` execution using persistent genesis clones.

### Proof sketch

Choose a minimum chain cover `C1, …, Cq` of `H(t)`, where `q=cc(t)`. Preallocate one clone for every chain. Replay the common causal prefix into every clone whose chain contains that prefix. When histories diverge, continue delivering only the inputs belonging to the corresponding chain. A2 guarantees that every copied abstract state is reproduced by replay; A1 guarantees identical local outputs. Deliver to correct replicas exactly the emissions retained by `t` and suppress all other clone emissions using A3–A4. Schedule cross-branch dependencies only after their source messages have been generated. A5 permits retaining messages until this condition holds. Erase physical clone identities and independent scheduling order using A6–A7. Induction over the finite causal order yields the same observation.

## 5. Static lower bound

**Theorem G0-T2.** If the observation distinguishes every action in `H(t)`, any persistent-clone realization requires at least `cc(t)` clones.

A physical clone produces one chain because its local events lie on one deterministic history. Therefore a realization with fewer than `cc(t)` clones would give a smaller chain cover, contradicting minimality.

For a finite poset, the minimum chain decomposition equals maximum antichain width by Dilworth's theorem. Thus the proposed “faulty-history incompatibility width” is not an independent BFT construct under exact branch observation.

## 6. Active-slot collapse theorem

**Theorem G0-T3.** Under A1–A7, if a clone slot may restart from genesis or restore a reachable snapshot and previously emitted messages remain schedulable, every finite dynamic-equivocation trace has an observationally equivalent `AT_active(1)` execution.

### Proof sketch

Take any finite chain cover. Execute its chains sequentially in the one physical slot. After a chain emits its required messages, stop/reset the slot, replay the next chain and retain all emissions in the network. After all required causal sources exist, deliver messages to correct replicas in a topological order matching `t`. A5 and A7 remove any need for physical overlap.

## 7. Consequences

- For `AT_total(k)`, finite realizability is generic unfolding and `k_min` is ordinary chain cover when exact histories are preserved.
- For `AT_active(k)`, the clone hierarchy collapses to one under the original asynchronous observation model.
- Coarsening the observation may lower `k_min`, but then minimization becomes an observation-cover problem; that alone is not blockchain-specific novelty.
- A meaningful theorem requires an additional constraint not present in A1–A7: bounded real time, non-suppressible transport events, fixed per-view partitions, inability to replay state, resource-coupled signatures/nonces, or another concrete lifecycle property.

## 8. Gate decision

The Gate 0 no-go condition is met: a direct generic construction subsumes the finite-clone claim. The result does not depend on failure to find an exact paper and therefore remains valid despite incomplete access to one 2026 source and absence of a live expert review.
