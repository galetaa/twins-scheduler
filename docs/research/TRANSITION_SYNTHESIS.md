# Optimal refinement for general finite protocol transition systems

## What changes relative to independent pivots

The independent-pivot development remains a structured specialization. The
general optimizer in
[`transition_synthesis.py`](../../src/python/twins_scheduler/transition_synthesis.py)
instead accepts an explicit finite protocol transition system. Its transitions
may inspect and change arbitrary shared state, enable later transitions,
generate messages, preserve signed outputs, revise locks, branch
nondeterministically, and participate in cycles. None of its proofs require
independent signer contributions, additive certificate support, a repair graph,
initial readiness, or an opportunity poset.

The result is an exact minimum over every finite unsafe-reaching execution of
the declared graph under a **static Boolean scheduler policy**. A finite graph
may contain cycles, so this is not intrinsically a bounded-path-length search.
If an adapter encodes a round, message, or time bound in its state space, that
bound remains part of the model. An externally supplied graph must contain all
transitions intended by the claim; a certificate cannot prove that an exporter
faithfully extracted a client implementation.

## Model and objective

Let a finite labelled transition system be

\[
\mathcal M=(X,x_0,U,\longrightarrow),
\qquad
\longrightarrow\;\subseteq X\times
\bigl(\{\tau\}\cup(F\times\{0,1\})\bigr)\times X.
\]

Here \(X\) is the protocol state set, \(x_0\) the initial state, \(U\) the
unsafe state set, and \(F\) the finite set of fine scheduler keys. Internal
steps carry \(\tau\); an admission step carries \((f,v)\). A function
\(\pi:F\to B\) maps fine keys to coarse fibres. Each fibre \(b\) has a
nonnegative integer split cost \(c_b\). Allowed and required split sets satisfy
\(Q\subseteq D\subseteq B\).

A refinement selects \(Q\subseteq S\subseteq D\), paying
\(c(S)=\sum_{b\in S}c_b\). A **total static policy**
\(p:F\to\{0,1\}\) is compatible with \(S\) when it is constant on every
unsplit fibre:

\[
\pi(f)=\pi(g)\notin S\ \Longrightarrow\ p(f)=p(g).
\]

Under \(p\), an internal edge is available and an edge labelled \((f,v)\)
is available exactly when \(p(f)=v\). The protocol may still have multiple
available outgoing edges. The objective is existential:

\[
\operatorname{Opt}(\mathcal M)=
\min\{c(S): Q\subseteq S\subseteq D,\ p\text{ compatible with }S,
\ x_0\longrightarrow_p^* U\}.
\]

The minimum is \(+\infty\) if the set is empty. This objective does not assert
a universally winning controller, fairness, eventual termination, or a liveness
property. Multiple initial states can be represented by a fresh initial state
with internal edges to each permitted start.

### Repeated keys distinguish static policies from adaptive controllers

Splitting a coarse fibre permits different **fine keys** in that fibre to have
different values. It never permits one fine key to change its value halfway
through an execution. For example,

\[
x_0\xrightarrow{(f,1)}x_1\xrightarrow{(f,0)}u
\]

is unreachable under every static policy, even if the fibre containing \(f\)
is free to split. By contrast, replacing the second label by \((g,0)\), where
\(g\ne f\) and \(\pi(g)=\pi(f)\), yields a possible execution after paying
for that fibre. Tests explicitly separate these cases.

## Trace correspondence and exact cost

For a finite trace \(t\), let \(O_t\subseteq F\times\{0,1\}\) be its observed
admission labels. The trace is consistent when it contains at most one value
per fine key. Define its mixed coarse fibres by

\[
\operatorname{Mix}(t)=
\{b: \exists f,g,\ \pi(f)=\pi(g)=b,\ (f,0),(g,1)\in O_t\}.
\]

**Trace realization.** A trace is realizable by some total policy compatible
with a proposed split set \(S\) if and only if it is consistent and
\(\operatorname{Mix}(t)\subseteq S\).

*Proof.* A compatible policy supplies a unique value for every fine key and a
common value on every unsplit fibre, giving necessity. Conversely, copy each
observed fine-key value. On an unsplit fibre, all observations agree, so use
that value for its unobserved fine keys, or zero if none was observed. Complete
unobserved keys on split fibres arbitrarily. This constructs a total compatible
policy realizing every label in the trace. No protocol-state independence is
used. ∎

**Least refinement for a trace.** A consistent trace has an admissible
refinement precisely when \(Q\cup\operatorname{Mix}(t)\subseteq D\). Its least
split set under inclusion is

\[
S_t=Q\cup\operatorname{Mix}(t).
\]

Nonnegative costs imply that \(c(S_t)\) is minimum for that trace. Required
splits are paid even when their fine keys never occur. Optional unused splits
cannot improve this minimum. When a trace is extended consistently, its mixed
set and its cost can only grow.

These facts yield the exact characterization

\[
\operatorname{Opt}(\mathcal M)=
\min_{t:\ x_0\to^* U\atop t\text{ consistent},\ S_t\subseteq D} c(S_t).
\]

The proof applies to arbitrary state dependencies in \(\mathcal M\). The
declared static-policy interface, nonnegative split costs, and complete model
are its substantive assumptions.

## Persistent-policy product and search

A product state is \((x,a)\), where \(x\in X\) and
\(a:F\to\{\bot,0,1\}\) remembers the partial static policy. Initially all
keys are unobserved. The implementation encodes these values as integers
\(-1,0,1\).

An internal transition changes only \(x\). An admission \((f,v)\) is legal
when \(a(f)\in\{\bot,v\}\); it records \(a(f)=v\). An opposite remembered
value blocks the edge. An update that makes a forbidden fibre mixed also
blocks the edge. Protocol state and remembered policy are both retained, so
two histories reaching the same protocol state with different policy
assignments remain distinct product states.

Give a product state the cost

\[
g(x,a)=\sum_{b\in Q\cup\operatorname{Mix}(a)}c_b.
\]

The initial cost is \(c(Q)\); a product edge has incremental cost
\(g(y,a')-g(x,a)\ge0\). Every path to the same product state has the same
accumulated cost. In particular, a split is charged once when its second
distinct value is first observed; later uses and additional phases do not
charge it again.

The optimizer explores this graph in increasing cost using a heap. The first
unsafe product state supplies an optimum witness. Parent pointers produce the
input transition indices, the complete product path, a compatible total policy,
the selected split set, and its exact integer cost. If the finite graph is
exhausted without an unsafe state, the optimizer produces an infeasibility
certificate.

There are at most \(|X|3^{|F|}\) product states and
\(|\longrightarrow|3^{|F|}\) product edges. This is an exponential worst-case
bound; the implementation does not claim polynomial synthesis. It also does
not allocate a table indexed by the numeric cost bound: split costs are exact
Python integers, including values larger than floating-point integer precision.
State and wall-clock limits raise `SynthesisLimit` with result **unknown**.
They never silently truncate the graph or produce an infeasibility claim.

## Independently checkable lower-bound certificates

The checker does not trust the search frontier, reported statistics, or an
optimizer-provided edge list. It reads the original input transitions and uses
a separate implementation of the product successor relation and path replay.

### Optimality: a closed strict cost sublevel

For a claimed optimum \(K\), the certificate gives a finite set \(C\) of
product states satisfying all four conditions:

1. Every \(z\in C\) is safe and has \(g(z)<K\).
2. The initial product state belongs to \(C\) whenever \(c(Q)<K\).
3. For every \(z\in C\), the checker regenerates **every** permitted successor
   \(z'\) from the bound protocol input.
4. Whenever such a successor has \(g(z')<K\), it also belongs to \(C\).

**Closed-sublevel lower bound.** These conditions imply that every reachable
unsafe state has cost at least \(K\).

*Proof.* Suppose an unsafe execution has final cost less than \(K\). Cost
monotonicity implies that its initial state and every prefix also have cost
less than \(K\). The initial condition and successor closure inductively place
every prefix in \(C\), including the unsafe final state, contradicting safety
of \(C\). ∎

An independently replayed compatible unsafe witness costing exactly \(K\)
matches this lower bound and therefore proves optimality. With zero cost, or
when the optimum equals the required initial payment, \(C\) may be empty:
no lower-cost product state exists, and the replayed witness remains necessary.

The search outputs its settled states of cost strictly less than \(K\). The
checker need not reconstruct the search order. An arbitrary safe overapproximation
of the reachable strict sublevel also suffices if it satisfies the same closure
conditions. Omitted reachable successors cannot be hidden by omitting their
edges from a certificate, because proof edges are not a certificate field.

### Infeasibility: full successor closure

An infeasibility certificate supplies a safe set containing the initial product
state and closed under **all** legal successors, without a cost threshold. By
induction it contains every reachable product state, so no unsafe state is
reachable. The set may safely include additional unreachable states; it must
contain all reachable ones. Resource-limited partial exploration does not meet
this condition.

### Binding and trust boundary

The portable JSON contains the complete problem and its SHA-256 digest under
canonical JSON encoding. `verify_certificate(certificate, expected_problem)`
also compares this input with the caller's expected immutable model. This
external binding detects changed costs, missing input edges, altered unsafe
states, or different scheduler fibres. Without `expected_problem`, the checker
proves the claim only about the input embedded in that certificate; recomputing
a hash cannot establish that this is the model a paper or implementation meant.

The Python checker validates all integer/Boolean distinctions explicitly:
`true` is not accepted as integer index 1, nor integer 1 as an admission Boolean.
Unrecognized model fields, malformed partial assignments, omitted path states,
inconsistent repeated decisions, disallowed or unpaid splits, duplicate proof
states, and an incomplete closed set are rejected. Python checker correctness
is not itself mechanized; the Lean development proves its mathematical
certificate principles and the policy correspondence.

## Complexity: NP-complete even on an acyclic protocol graph

Consider the decision question \(\operatorname{Opt}(\mathcal M)\le K\), with
an explicit finite graph and binary-encoded nonnegative costs. It is in NP:
guess a total policy and a split set, check their coherence and cost, then run
ordinary graph reachability after filtering edges by that policy. This is
polynomial in the explicit input size. A witness path may be chosen simple in
the policy-filtered protocol graph.

For NP-hardness, reduce Set Cover. Let the universe be
\(\{e_1,\dots,e_n\}\) and the available sets
\(A_1,\dots,A_m\), with costs \(w_j\). Introduce two fine keys
\(a_j,b_j\) in coarse fibre \(j\), priced \(c_j=w_j\). Use all fibres as
allowed and none as required.

The protocol graph first follows a forced chain labelled

\[
(a_1,0),(a_2,0),\ldots,(a_m,0).
\]

Then, for each element \(e_i\), one layer has an edge labelled \((b_j,1)\)
for each \(j\) with \(e_i\in A_j\). All these edges lead to the next layer;
the final state is unsafe. Every unsafe execution selects at least one
containing set for every element. Fibre \(j\) becomes mixed exactly when its
set is selected in at least one layer, and repeated selection costs nothing
additional. Consequently its split cost is exactly the cost of the selected
cover. Conversely, any cover chooses one containing set in each layer and
yields an unsafe execution of no greater cost; an optimum cover can discard
unused positive-cost sets. The optima therefore agree.

The reduction is polynomial, the graph is acyclic, and each coarse fibre has
exactly two fine keys. Unit costs already yield the usual Set Cover decision
problem, establishing NP-completeness; weighted costs preserve the weighted
objective. This reduction identifies a classical source of hardness rather
than claiming that minimum-cost graph search itself is a new algorithmic
primitive. It also explains why the independent-pivot SCC formulation remains
valuable as a structural specialization.

[`transition_examples.py`](../../src/python/twins_scheduler/transition_examples.py)
implements this reduction as `set_cover_problem(universe_size, sets, costs)`.
Tests independently enumerate covers for all 512 ordered three-set families
over a three-element universe and compare the reduced optima, including
infeasible families. Empty universes, uncovered elements, and a cost exceeding
\(2^{128}\) are additional controls.

## The independent-pivot optimizer is an optimum-preserving specialization

[`transition_pivot_adapter.py`](../../src/python/twins_scheduler/transition_pivot_adapter.py)
makes the connection executable. Given an initially-ready independent-pivot
`Problem`, `build_pivot_model` exports a complete finite transition system.
Its state records the processed enabling prefix, first-signature set, completed
repair/vote opportunity slots, repair flags, and immutable second-signature
set. Fine keys \(2i\) and \(2i+1\) represent \(E_i\) and \(R_i\), both mapped
to coarse fibre \(i\). Vote issuance \(V_i\) is an internal transition.

The prefix resolves every \(E_i\). Thereafter, every still-unprocessed event
whose input predecessors have completed is a possible next opportunity. This
uses the supplied order edges directly, so cover relations and their
transitive consequences are preserved. An admitted repair sets its flag; a
suppressed repair still completes its opportunity slot. Issuance adds a second
signature exactly when the pivot is not repaired. Later repair cannot delete
it. The unsafe goal requires all opportunities to complete and both weighted
certificate deficits to be met.

The exporter includes all four Boolean pairs for \((E_i,R_i)\), including
\((0,1)\). Thus equivalence with the older three-pattern normalized model is a
proved dominance property rather than an input restriction that silently
removes extra fine policies.

**Specialization theorem.** For the declared initially-ready independent-pivot
contract, arbitrary positive weights, nonnegative split costs, quota deficits,
and allowed/required split sets, the exported general LTS and the weighted
four-role optimization have the same optimum, including infeasibility.

*Proof.* Any normalized independent-pivot execution embeds directly: process
its enabling prefix and its complete legal opportunity order, using its
\((0,0)\), \((1,1)\), or split \((1,0)\) pairs. The signer sets, split cost,
and goal agree, establishing that the general optimum is no larger.

Conversely, take a general unsafe execution under a selected split set \(S\).
Keep its complete opportunity order. For each \(i\in S\), replace its pair
by \((E_i,R_i)=(1,0)\); every unsplit pair is already uniform and remains
unchanged. This preserves the allowed/required conditions and pays no greater
cost. Each changed pivot now contributes a first signature and never has its
second issuance disabled by repair. Independent contributions imply that
neither signer set shrinks. Opportunity slots and every precedence constraint
remain unchanged, including slots whose repair value changed to suppressed.
The normalized execution still meets both quotas and lies in the independent
contract, giving the reverse inequality. Required but previously uniform
split fibres are normalized in the same way. ∎

This proof uses pivot independence only for the **specialization bridge**;
the general LTS certificate and abstraction-refinement proofs do not use it.
The adapter calls no repair-graph extraction, acyclic-capacity formula,
four-role optimizer, or event-order enumerator. Its state limit raises
`AdapterLimit`, a subclass of `SynthesisLimit`, before returning an incomplete
model. This is a model-to-model theorem, not a client-code extraction theorem.

The reproducible
[`check_transition_specialization.py`](../../scripts/check_transition_specialization.py)
compares both solvers with an additional raw oracle that enumerates every
legal event permutation, all four per-pivot Boolean patterns, and every
allowed/required split subset. Its
[`specialization_oracle.json`](../../results/transition_bridge/specialization_oracle.json)
records 1,507 queries: all 18 directed graphs on one or two pivots including
self-loops, all quota pairs through total weight plus one under two weight
profiles, 144 permission controls, and all 219 labelled four-event posets at
three weighted quota pairs. There are 3,014 optimum comparisons, 3,014 checked
certificates, and zero mismatches. The raw oracle covers 221 order domains,
963 legal orders, and 15,372 Boolean-policy/order executions. All 1,189 feasible
general witnesses also normalize to accepted independent-model executions at
the same cost. The largest export has 199 states and 398 transitions.

Eight additional unit tests check every raw order and every Boolean pattern
for the unrestricted two-pivot domain, normalization of reversed mixed pairs,
required splits, persistent signatures after repair, suppressed intermediate
slots, weighted quotas, and resource limits. A monkeypatch test disables every
specialized solver/order/capacity helper while export and general certificate
verification still succeed.

```bash
uv run python scripts/check_transition_specialization.py
```

## Executable interface

```python
from twins_scheduler.transition_synthesis import (
    Problem, Transition, synthesize, verify_certificate,
)

problem = Problem(
    states=("start", "enabled", "unsafe"),
    initial=0,
    unsafe=frozenset({2}),
    transitions=(
        Transition(0, 1, key=0, value=True, label="enable"),
        Transition(1, 2, key=1, value=False, label="withhold repair"),
    ),
    key_fibres=(0, 0),
    costs=(5,),
)
certificate = synthesize(problem, max_product_states=100_000)
assert certificate["minimum_cost"] == 5
assert verify_certificate(certificate, problem)["status"] == "PASS"
```

`Transition(source, target)` denotes an internal edge. Transition `label`
strings and state names are descriptive; the semantics use state indices and
the typed `(key, value)` pair. A fibre may contain more than two fine keys,
and fine keys need not be contiguous within a fibre. Coarse fibres without
used fine keys remain meaningful when their split is required.

`Problem.to_dict()` and `Problem.from_dict()` provide the portable input
format. `Problem.digest()` returns its canonical SHA-256. `replay_trace`
computes a canonical compatible total policy for any legal input-edge path.
`product_successors` exposes the product semantics for adapters, but the
certificate checker deliberately does not call it.

An optimal certificate has `status="optimal"`, integer `minimum_cost`, a
`witness`, and a `proof` of kind `closed-strict-sublevel`. Its witness contains
input `transitions` indices, every `product_states` entry, a total Boolean
`policy`, the `split` indices, exact `cost`, and the unsafe `terminal` index.
An infeasible certificate has `minimum_cost=null`, `witness=null`, and proof
kind `closed-reachable-set`. The verifier reports its own checked state and
transition counts; optimizer statistics are informative and untrusted.

## Validation and proof correspondence

[`test_transition_synthesis.py`](../../tests/unit/test_transition_synthesis.py)
currently has 33 passing test cases. Its independent oracle enumerates total
Boolean policies and allowed split subsets, then computes ordinary protocol
graph reachability. It agrees with synthesis and certificate verification on
2,048 graph/cost/constraint instances from an exhaustive eight-edge-family
sweep. This oracle does not use partial assignments, product exploration,
Dijkstra, repair graphs, or certificate code. The 512 Set Cover comparisons
check an additional reduction-specific property.

The standalone
[`check_transition_oracle.py`](../../scripts/check_transition_oracle.py)
records both families together with 400 seeded arbitrary finite transition
systems. Its deterministic
[`random_oracle.json`](../../results/transition_bridge/random_oracle.json)
contains the exact generator settings, canonical input/outcome hashes, and
these checked totals:

| Measure | Count |
|---|---:|
| Generated model instances | 2,960 |
| Direct and abstraction-based optimum comparisons | 5,920 |
| Direct certificate checks | 2,960 |
| Complete abstraction-run checks | 2,960 |
| All abstract iterations checked, including final certificates | 6,857 |
| False policies eliminated and checked | 3,897 |
| Enumerated policy/split pairs after allowed/required filtering | 291,804 |
| Pairs satisfying complete-policy fibre uniformity | 132,626 |
| Independent Set Cover subset checks | 4,096 |
| Optimum, certificate, or reduction mismatches | 0 |

The 2,960 instances comprise the 2,048 edge-family cases, 512 Set Cover
reductions, and 400 random graphs; the unit-test sweeps are not counted again
as additional independent instances. The largest observed number of abstraction
iterations is seven, within the per-model state-count termination bound. The
report is byte-identical under a fresh output root and excludes runtime
measurements. Its seeded graphs are a finite audit, not an exhaustive
enumeration of arbitrary transition systems.

```bash
uv run python scripts/check_transition_oracle.py
```

Behavioral controls exercise merged states reached with different policies,
four phases in one fibre, immutable repeated-key choices, initially unsafe
states, required but unobserved splits, cycles, nondeterministic successors,
zero costs, and empty fine-key interfaces. Malicious-certificate controls
replace an optimum witness with a valid expensive one, forge infeasibility,
remove initial or successor states, alter input edges, and corrupt types or
policies. A monkeypatch control disables every optimizer transition helper
while the independent verifier still checks the certificate successfully.

[`TransitionRefinement.lean`](../../formal/lean/SchedulerClosure/TransitionRefinement.lean)
mechanizes the general policy and certificate arguments, including:

- `policy_realizable_iff`, `least_split_set`,
  `admissible_refinement_exists_iff`, and `minimum_trace_refinement`;
- `trace_cost_mono`, `query_guard_iff_consistent_extension`, and
  `memory_update_cost_mono`;
- `sublevel_certificate_lower_bound`, `closed_certificate_infeasible`, and
  `sublevel_certified_minimum`;
- labelled execution simulation and the transfer of an abstract lower bound,
  matching concrete witness, or abstract infeasibility to a concrete model.

The accompanying model-to-model abstraction checker preserves the full static
scheduler interface and checks every concrete input transition. Exactness for
a concrete model follows when a certified abstract lower bound matches a
replayed concrete unsafe witness. A spurious abstract unsafe path alone is
only a lower bound. Connecting the finite concrete model to production client
code requires its own extraction/refinement argument; neither explicit-graph
certification nor a successful conformance trace supplies that argument
automatically.
