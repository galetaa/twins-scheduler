# Certified transition abstraction and policy refinement

This extension transfers scheduler-refinement optimality beyond the independent-pivot schema. The generic solver accepts an arbitrary finite, control-labelled transition system. The abstraction checker verifies a relation to a more detailed transition model, and an iterative procedure repairs state abstractions that admit spurious policies.

Implementation: [transition_abstraction.py](../../src/python/twins_scheduler/transition_abstraction.py). Formal foundation: [TransitionRefinement.lean](../../formal/lean/SchedulerClosure/TransitionRefinement.lean). The general input and product semantics are specified in [TRANSITION_SYNTHESIS.md](TRANSITION_SYNTHESIS.md).

## 1. What transfers, and in which direction

Concrete and abstract models have the same fine keys, coarse-fibre map, nonnegative integer costs, allowed splits and required splits. A state map must cover every concrete state, preserve the initial state, and map every concrete unsafe state to an abstract unsafe state.

For **every concrete input transition**, the checker requires:

- An abstract transition with the same fine key and Boolean answer for a controlled transition.
- An abstract internal transition, or equal mapped endpoints, for an internal transition.

A controlled query cannot disappear as stuttering. Decorative transition labels may differ. This is a sufficient one-edge/internal-stutter simulation; the theorem can also be used with separately established richer simulation relations.

Induction gives an abstract path with the same visible query sequence for every concrete path. The same total static policy and split set realizes both. Therefore

\[
\operatorname{Opt}(A)\le\operatorname{Opt}(C).
\]

A checked abstract lower bound `L` and an independently replayed concrete unsafe witness with cost `U` establish

\[
L\le\operatorname{Opt}(C)\le U.
\]

Equality proves concrete-model optimality. Abstract infeasibility proves concrete-model infeasibility. A forward simulation by itself cannot turn an abstract witness into a concrete one. The API distinguishes `concrete-lower-bound-only`, `concrete-bounds`, `concrete-optimal`, and `concrete-infeasible`.

## 2. Concrete-policy abstraction refinement

For a concrete finite graph and a state partition `h`, construct the exact existential quotient: project every edge and declare a group unsafe if any member is unsafe. Internal self-loops are omitted; every controlled admission remains visible.

The implemented loop is:

```text
solve the current quotient and independently check its certificate
if infeasible: transfer infeasibility and finish
take the certificate's total static policy a
explore the concrete graph using only a-compatible edges
if an unsafe path exists: replay it and check equality of bounds
otherwise let R be the complete a-reachable concrete state set
split each old group into its intersection with R and its complement
repeat
```

The concrete search in one iteration tests **one total policy**, not all possible refinements. It is ordinary graph reachability and does not use the product optimizer.

The false-policy reachable set contains the initial state, is closed under every compatible edge, and excludes unsafe states. After splitting by membership in this set, each quotient group lies wholly inside or outside it. A compatible edge from an inside group has an inside concrete source, and its target is inside by closure. No inside group is unsafe. Thus the new quotient removes **all unsafe paths of that policy**.

If the old quotient had such a path, at least one group must split. Consequently there are at most `number of concrete states - number of initial groups` failed iterations. Subsequent abstract optima cannot decrease. Search-state or iteration cutoffs return `unknown`; they cannot become infeasibility certificates.

The method specializes established [counterexample-guided abstraction refinement](https://www.cs.cmu.edu/~emc/papers/Papers%20In%20Refereed%20Journals/Counterexample-guided%20abstraction%20refinement.pdf). Its specific interface is persistent scheduler policies and paid coarse-fibre distinctions. It does not claim the invention of CEGAR or finite graph search.

## 3. What the history checker verifies

`verify_abstraction_run` does not call the optimizer, quotient builder, or concrete-policy BFS. It checks each intermediate abstract certificate against the exact recorded abstract input, then independently reconstructs the projected edge and unsafe-group sets from the concrete model.

For each rejected policy, the saved state set must contain the initial state, exclude unsafety, and be closed under **every** compatible concrete edge. A safe inductive overapproximation is sufficient; exact BFS provenance is not trusted. Each next partition must strictly refine the old partition and separate the saved invariant from its complement. The final bridge is recomputed; supplied status and numeric bounds are not accepted on trust.

For the final optimality conclusion, only the final input-bound abstract certificate, all-edge simulation and concrete witness are necessary. Checking the history additionally supports the claims about eliminated policies, intermediate bounds and progress.

Tests reject missing concrete/abstract edges, hidden unsafe states, altered costs/keys, erased controlled queries, omitted invariant successors, false witness adjacency, repeated-key inconsistency and invented quotient edges. A test disables all optimization and model-construction helpers while verification still succeeds.

## 4. Stateful protocol result

The [coupled protocol model](COUPLED_PROTOCOL_MODEL.md) has two endpoint/view control fibres affecting the same local quorum. It executes guarded voting, locking, timeouts and missing-block commit behavior. Its complete declared environment contains two rounds, 12 stages and 32 once-only opportunity slots, with every within-stage permutation.

For costs `B->P=5`, `A->P=2`:

| Model / abstraction | Concrete states | Concrete transitions | Final abstract states | Iterations | Certified result |
|---|---:|---:|---:|---:|---|
| Missing lock, initially one state group | 2,516 | 5,856 | 26 | 12 | Minimum cost 2 |
| Missing lock, audit-field quotient | 2,516 | 5,856 | 1,978 | 1 | Minimum cost 2 |
| Baseline retaining the lock | 2,372 | 5,574 | 1 | 1 | Infeasible in this environment |

The coarsest-start run eliminates 11 false policies. Its abstract-state counts are `1,2,4,6,8,11,14,16,19,21,24,26`; the lower bounds are `0,0,0,0,2,2,2,2,2,2,2,2`. The bound becomes correct before the abstract policy becomes concretely realizable, which illustrates why a lower bound alone is insufficient.

The last quotient has 60 edges. The checker still validates **all 5,856 concrete edges**. The concrete witness is replayed through protocol guards and ends with unmutated observers `A=0,C=1`. The audit-field quotient removes an extra first-arrival diagnostic field; it is a projection test, not a performance result about production-state minimization.

The baseline graph contains no unsafe state, so its one-group quotient can immediately certify infeasibility. This is a simple consequence of the fully enumerated baseline model, not evidence that the algorithm proves native-client safety from one abstract state.

All complete histories, guarded replays and model hashes are saved under [results/transition_bridge](../../results/transition_bridge/). Nine illustrative runs pass, totaling 32 checked iterations and 23 eliminated policies. The separate [random_oracle.json](../../results/transition_bridge/random_oracle.json) records 2,960 instances with both direct and abstraction-based optimization checked against total-policy/subset enumeration: 5,920 optimum comparisons, 6,857 checked abstraction iterations, including final certificates and zero mismatches. This corpus includes the 2,048-case family and 512 Set Cover reductions also exercised in unit tests; those are not additional independent samples.

## 5. Commands

```bash
# All general protocol and abstraction studies, including independent oracles.
make transition

# Direct finite-LTS synthesis and independent input-bound verification.
uv run python scripts/run_transition_synthesis.py \
  --input model.json --output certificate.json.gz
uv run python scripts/run_transition_synthesis.py \
  --verify certificate.json.gz --expect-input model.json

# Iterative abstraction starting from one group.
uv run python scripts/run_transition_bridge.py \
  --input model.json --output abstraction.json.gz
uv run python scripts/run_transition_bridge.py \
  --verify abstraction.json.gz --expect-input model.json
```

An embedded hash binds a certificate to its embedded model. An external expected input is necessary when the result is being claimed for an independently specified model. Both tools accept compressed or plain JSON. Generated study data use `TWINS_OUTPUT_ROOT`; nondeterministic timings go only to `TWINS_LOG_DIR`.

## 6. Exact remaining boundary

The semantic proof does not assume finite concrete state. A code-level simulation or symbolic inductive invariant could cover an infinite implementation. The current executable checker, however, reads complete finite graphs; it does not extract such a proof from arbitrary BFT source code.

The full concrete graph is constructed before the iterative procedure. Reducing its quotient can reduce the persistent-policy product search, but it does not remove the cost of model enumeration. No measured speedup over industrial model checkers or symbolic CEGAR tools is claimed.

The policy class remains explicit: one persistent Boolean per fine key, with selected coarse fibres split into their declared fine keys. Adaptive choices, unlabelled policy-dependent behavior, uncovered client transitions, changing the bad-state predicate, or an incomplete frontier require a different theorem instance. Native unchanged-client conformance remains separate evidence and is not a universal implementation-refinement proof.
