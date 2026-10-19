# Certifying minimum-cost phase-refinement synthesis

This extension turns the repair-frontier characterization into an executable
design procedure: given an opportunity order, certificate deficits, pivot
weights, admissible refinement keys and their costs, return an optimal set of
phase distinctions, a concrete admission/event-order witness, and a separately
checkable proof that no cheaper admissible refinement works.

The fixed-set unit-weight capacity formula already occurs in the preceding
repair-frontier analysis. It is a starting point here, not a newly discovered
formula. The additions are unequal-weight/unequal-cost synthesis, required and
forbidden keys, constructive replay, explicit optimality and infeasibility
certificates, and the obstruction to a natural marginal-gain heuristic.

## 1. Model and exact scope

Let `I={0,...,k-1}` be independent pivots. Pivot `i` has positive integer weight
`w_i` and refinement cost `c_i >= 0`. Fixed base votes leave nonnegative integer
deficits `d0,d1` for two conflicting certificates. All enabling deliveries and
first-vote opportunities occur in a common prefix. The finite strict partial
order `P` constrains the remaining opportunities `R_i,V_i`, where `R_i` can
deliver a repair and `V_i` can issue the indispensable second vote.

The following conditions are inherited, rather than inferred by the tool:

1. Delivering `E_i` gives pivot `i` its first contribution. No closed key gives
   that contribution.
2. Every pivot is initially ready to issue its second vote, even if `E_i` is
   withheld. An admitted repair prevents future issuance at `V_i`.
3. Issued votes are immutable outputs: a later repair cannot retract them.
4. Contributions are independent and monotone under the prescribed modes.
   There are no hidden alternative certificate paths outside the schema.
5. Every linear extension of `P` is admitted by the declared domain. A
   suppressed envelope makes its opportunity a silent slot; it does **not**
   delete that slot or any transitive order constraint through it.
6. A coarse key either admits both `E_i,R_i` or neither. A refined key can admit
   `E_i` while withholding `R_i`. Refinement costs are additive input data.

The tool does not automatically extract these conditions from source code,
prove independence of arbitrary protocol participants, or optimize measured
CPU/network overhead. Costs can express an externally chosen instrumentation
budget, but the benchmark costs are synthetic integers. The one-pivot fixtures
are abstract inputs encoding forced repair and post-signature repair. They do
not execute a production client or establish an implementation-level result.

## 2. Prescribed keys and the weighted canonical theorem

Construct the repair graph from the **full** opportunity-order reachability:

\[
 i\to j\in H\quad\Longleftrightarrow\quad R_i\prec_P V_j.
\]

For any chosen set `J`, the joint reversals `V_i<R_i` for `i in J` admit a
linear extension exactly when `H[J]` is acyclic. This is the repair-frontier
specialization of the established alternating-cycle/reversible-pair criterion;
the graph-to-order bridge is separate from the synthesis optimization.

### Theorem S1: arbitrary weighted refinement

Let `A_allowed` and `A_required` be the available and mandatory refinement keys,
with `A_required` contained in `A_allowed`. A feasible execution exists at cost
at most `B` if and only if there is a partition

\[
 I=S\mathbin{\dot\cup}J\mathbin{\dot\cup}X\mathbin{\dot\cup}Y
\]

such that

\[
 A_{\rm required}\subseteq S\subseteq A_{\rm allowed},\qquad
 H[J]\text{ is acyclic},\qquad \sum_{i\in S}c_i\le B,
\]

and

\[
 w(S)+w(J)+w(X)\ge d_0,\qquad
 w(S)+w(J)+w(Y)\ge d_1.
\]

The four labels have the following interpretation.

| Set | Admission | Guaranteed contribution |
|---|---|---|
| `S` | Admit enabling, suppress repair, pay key cost | Both certificates |
| `J` | Admit both messages; put `V_i` before `R_i` | Both certificates |
| `X` | Admit both messages | First certificate |
| `Y` | Admit neither message | Second certificate |

`X` specifies a **guaranteed first contribution**, not a prohibition on a
second contribution. A constructed order may give some `X` pivots an additional
second vote. That can only help the lower-bound quota conditions. Similarly,
the certificates report actual replayed signer sets rather than treating this
canonical partition as an exact signer classification.

**Necessity.** Take any feasible execution. Put every actually split key in
`S`. Put each unsplit opened pivot whose second vote was issued in `J`; put
the other opened pivots in `X`, and the closed pivots in `Y`. Each `i in J`
actually has `V_i<R_i`, so `H[J]` is acyclic. The observed certificate weights
give the two quota inequalities, with precisely the paid cost of `S`. An
unused available split need not be paid; mandatory splits are retained. If
refinement is viewed as a capability rather than an actual mode, using its
canonical enabled/repair-suppressed mode weakly increases both supports under
the independent monotone contract.

**Sufficiency and construction.** Open exactly `S union J union X`, suppress
repairs exactly at `S`, and topologically sort

\[
 P\ \cup\ \{(V_i,R_i):i\in J\}.
\]

The graph-to-order criterion makes this acyclic. It preserves all original
opportunity slots, including suppressed repairs. The resulting run has at
least the guaranteed supports in the table. A repair processed after issuance
leaves that signature in the immutable output set. Thus both quotas hold.

This proof yields a synthesizable event order, not only a numeric answer.

### Corollary S2: a prescribed unit-weight set

For unit weights, let

\[
 F(S)=|S|+\alpha(H[I\setminus S]),
\]

where `alpha` is the maximum cardinality of an induced acyclic set. An
available prescribed split set `S` is sufficient exactly when

\[
 \max(d_0,d_1)\le k,\qquad d_0+d_1\le k+F(S).
\]

For sufficiency, choose a maximum acyclic `J` in the complement of `S` and
give `S union J` both contributions. Allocate
`max(0,d0-F(S))` remaining pivots to the first certificate and close the rest;
the stated inequalities leave enough second support. Necessity follows by
counting the pivots that must contribute to both certificates.

The set matters, not only its size. For edges `0->1,1->0` and isolated vertex
`2`, full quotas `(3,3)` fail with available split `{2}` (`F=2`), but succeed
with `{1}` (`F=3`). The existing cardinality formula optimizes the choice of
keys; applying it to an arbitrary preselected set is unjustified.

For positive weights and full quotas `d0=d1=W=sum(w_i)`, every pivot must
contribute to both certificates. Thus `X=Y=empty`, `J=I\S`, and minimum-cost
refinement is exactly the classical minimum-weight directed feedback vertex
set problem on `H`, with the specified available/required vertices. This is a
reduction connecting a known graph problem to refinement, not a claim that
feedback vertex set or its hardness is new.

## 3. Why a natural one-key-at-a-time heuristic fails

For unit weights, `F` is monotone and every one-key increment is either zero or
one: deleting one vertex reduces an induced acyclic maximum by at most one.
However, `F` is not submodular.

Consider the two cycles `0<->1` and `0<->2`. Then

\[
 F(\varnothing)=2,\quad F(\{1\})=F(\{2\})=2,\quad
 F(\{1,2\})=3.
\]

In particular,
`F({1})+F({2}) < F(empty)+F({1,2})`, violating submodularity.

Define a specific myopic policy: while the quota criterion fails, choose a
remaining key with the largest **positive** ratio

\[
 \frac{F(S\cup\{i\})-F(S)}{c_i};
\]

break ties by smallest vertex index, and report `STALLED` if no positive
marginal exists. Assume positive costs for this baseline. Give the center cost
`M>2`, both leaves cost `1`, and require full quotas `(3,3)`. Initially only
the center has a positive marginal, so the policy pays `M`. The optimum splits
both leaves for cost `2`. Its approximation ratio on this family is `M/2`,
which is unbounded as an input cost increases.

This statement concerns exactly the defined myopic policy. It is not an
impossibility theorem for all greedy algorithms, lookahead, approximation
algorithms, or specialized feedback-vertex-set solvers. It explains why
improving a cardinality budget or ranking keys by immediate benefit alone
cannot replace the certifying unequal-cost calculation.

## 4. Exact component algorithm

The implementation is
`src/python/twins_scheduler/refinement_synthesis.py`.

First compute `H` from the full transitive opportunity order. A self-loop
vertex cannot belong to `J`, so it can be treated as an independent singleton
with only `S,X,Y` choices. On the remaining graph, compute strongly connected
components `C_0,...,C_(m-1)`. A selected `J` is acyclic if and only if each
`H[J intersection C_j]` is acyclic. Cross-component edges cannot create a
cycle. Crucially, deleting loop vertices here removes them only from the
**reversible-choice search**; their opportunity slots have already contributed
all transitive edges to `H` and remain in the final execution.

For each component enumerate its four-state assignments, enforcing allowed
and required keys and acyclicity of its `J` part. Each valid local assignment
gives `(a,b,c)`: guaranteed first support, guaranteed second support and split
cost. Clip the supports at `d0,d1`, and retain the cheapest assignment for each
identical support pair. Clipping is exact because every residual demand stays
within those quotas. This compression does not round weights or assume that
arbitrary intermediate weight sums are attainable.

The dynamic program is over residual quotas:

\[
 L_j(x,y)=\min_{(a,b,c)\in\mathcal O_j}
 \left[c+L_{j+1}(\max(0,x-a),\max(0,y-b))\right].
\]

Its terminal values are `L_m(0,0)=0` and `L_m(x,y)=infinity` otherwise. If
`L_0(d0,d1)` is finite, follow tight transitions to recover the local labels,
then construct and replay the full augmented topological order from S1.
If the value is infinite, no canonical configuration satisfies the quotas.

The public API supports nonnegative costs, including zero, and positive
integer weights. It minimizes cost only; equal-cost outputs use deterministic
local tie breaking and need not have minimum cardinality among all equal-cost
solutions. `initially_ready=False` is rejected instead of being silently
handled by the wrong theorem.

## 5. What the certificate proves, and what must still be trusted

The portable JSON contains the problem, chosen keys, admissions, every event
opportunity, actual signer sets and weights, plus the component partition and
the entire table of Bellman lower-bound potentials. `None` represents infinity.

The checker `verify_certificate` performs two logically distinct checks.

**Upper bound.** Reconstruct the paid split keys and independently replay the
event order. Reject unknown, omitted or duplicated slots; reject precedence
violations; process repair guards and immutable issued-output sets. Verify both
certificate quotas and the claimed total cost.

**Lower bound.** Independently rebuild opportunity reachability with repeated
DFS, recover components by mutual reachability, and enumerate local assignments
with an integer encoding and a separate DFS cycle test. For every local
transition and every residual quota pair, check

\[
 L_j(x,y)\le c+L_{j+1}(\max(0,x-a),\max(0,y-b)).
\]

The checker does not compute a global minimum or invoke the optimizer. When
several assignments have identical support, their minimum cost yields the
strongest inequality, so the checker can aggregate them without losing any
obligation. It checks the full terminal row as well.

Along any feasible sequence of local configurations the inequalities telescope
to `L_0(d0,d1) <= actual cost`. A replayed witness of exactly that value proves
optimality. If the initial potential is infinity, the existence of a feasible
finite-cost path would contradict the same inequalities and terminal zero,
which certifies infeasibility. A feasible execution by itself proves only an
upper bound; a test substitutes the valid cost-10 center witness for the
cost-2 optimum and verifies that the lower-bound checker rejects the forgery.

`formal/lean/SchedulerClosure/CertificateOptimality.lean` machine-checks this
generic extended-natural Bellman path argument, the minimum-cost witness
principle, and infeasibility (`bellman_path_lower_bound`,
`certified_witness_is_minimum`, `certified_infeasibility`). This proves the
certificate principle from its edge inequalities. It does **not** verify the
Python JSON parser, the graph extraction implementation, local enumeration,
or a production-code refinement. The executable checker and its connection
to the formal state graph remain an explicit trusted boundary, challenged by
independent raw-event oracles and negative controls.

The design follows the established certifying-algorithm approach: independent
validation of each returned instance rather than an unconditional assertion
that the optimizing program is correct. The certificates here need not be
polynomial in a binary-encoded input, and checking a large component remains
exponential. The checker is independent and structurally simpler at the global
optimization layer; it is not claimed to be asymptotically faster than the
optimizer in every case.

## 6. Complexity and resource limits

Let `s` be the largest component after self-loop exclusion, `m` the number of
components including loop singletons, and `Q=(d0+1)(d1+1)`. If component `j`
has `a_j` distinct clipped support options, then
`a_j <= min(4^|C_j|,Q)`. A conservative bound for this implementation is

\[
 O\!\left(k^3+\sum_j 4^{|C_j|}k^2+Q\sum_j a_j\right)
\]

time, with `O(mQ + sum_j a_j |C_j| + k^2)` working space including the complete
certificate table. The Bellman part of the certificate has `m+1` rows of `Q`
cells; each finite cell is at most `sum_i c_i`, plus an infinity marker.
The concrete witness adds `2k` opportunity records and the input precedence.

The dependence on quotas is **pseudo-polynomial**. There is no claim of
fixed-parameter tractability in `s` alone when weights and deficits are encoded
in binary. A large single SCC can be expensive even when its optimum is
obvious to a specialized solver; the reference implementation deliberately
favors a small auditable algorithm over comprehensive graph-specific tricks.

Default limits are component size `10` and two million potential cells.
An optional wall-clock budget is supported for a standalone request.
Exhaustion raises `SynthesisLimit` and the CLI exits with `RESOURCE_LIMIT`
(exit code `2`), without fabricating an infeasibility certificate. The study's
two unsolved structural cases were stopped by the explicit component-size
limit; they were **not** timed out and were **not** proved infeasible.

## 7. Executed finite validation

`scripts/run_refinement_synthesis.py --study` produces deterministic source
observations, per-problem comparisons, portable examples and compressed
certificates. The oracle enumerates raw permutations of `R/V` events, filters
the original precedence, and executes every three-state admission assignment.
It never calls `Domain.orders`, `Domain.repair_graph`, `execute`, the capacity
formula, or the dynamic program to generate outcomes.

| Scope | Executed checks |
|---|---:|
| All directed repair graphs, loops allowed, `k=1,2,3` | 530 graphs |
| Raw legal orders in those graph-realization domains | 50,363 |
| Raw event/admission executions in those domains | 1,357,209 |
| Prescribed available sets and unit quota boundaries | 103,460 |
| Weighted all-quota optimizer/oracle comparisons, `k<=2` | 21,804 |
| Weighted three-pivot optimizer/oracle comparisons | 2,560 |
| Restricted-key comparisons | 128 |
| All labelled partial orders on two repairs and two vote opportunities | 219 |
| Raw legal orders for those arbitrary partial orders | 960 |
| Raw event/admission executions for those orders | 8,640 |
| Weighted all-quota comparisons on arbitrary partial orders | 10,731 |
| Total compared and independently verified optimization certificates | **35,223** |
| Mismatches | **0** |

The all-quota weighted sweep uses weights `1..3`; it includes unequal costs and
zero-cost keys. The three-pivot sweep uses deterministic heterogeneous
weights/costs and five stated quota pairs per graph, not every such weighting.
The arbitrary-order sweep includes `R->R`, `V->V`, `V->R` and transitively
implied dependencies; it is not limited to two-layer graph realizations.
The separately regenerated raw graph-execution count matches the existing
frontier corpus's domain size. These are alternative computations over a
declared finite corpus, not millions of independent protocols or new bugs.

The scientific record is `results/synthesis/synthesis_summary.json`,
`synthesis_oracle_cases.csv` and `synthesis_raw_observations.json.gz`.
`tests/unit/test_refinement_synthesis.py` supplies 12 further behavioral,
independent-oracle and malformed-certificate tests, including required keys,
initial-readiness rejection, immutable post-repair output and silent-slot
transitivity. The listed totals concern the main committed reproducible suite.

A separately written review oracle,
`scripts/check_synthesis_order_oracle.py`, adds 48 seeded arbitrary three-pivot
event DAGs with weights `1..3`, costs `0..7`, and allowed/required key subsets.
It directly enumerates 4,647 legal event permutations and 72,117 admissible
mode executions, then compares all quota pairs: 3,253 further minimum-cost
comparisons and certificate checks pass with zero mismatches. Its independent
record is `results/synthesis/order_oracle.json`. The two optimizer/oracle
corpora therefore contain 38,476 compared and verified problems in total;
their distinct scopes remain visible instead of merging all execution counts.

## 8. Deterministic scale study and practical interpretation

The scale corpus is synthetic and uses seed `20261019`. It covers sparse DAGs,
crossed pairs, repeated two-cycle motifs, weighted common-deadline domains,
dense strongly connected graphs, long cycles and weighted quota problems in
four-vertex cyclic blocks. It solves cases with up to 48 pivots because their
strongly coupled components are small, and explicitly retains resource-limited
large-component cases. Every solved case ships its complete compressed
certificate and a digest of the uncompressed canonical JSON.

Representative results include:

| Case | Optimal split cost | Specified myopic cost | Interpretation |
|---|---:|---:|---|
| 24 crossed pairs, 48 vertices | 75 | 75 | Cheap one-key choices suffice within each pair |
| Ten repeated two-cycle motifs, 30 vertices | 20 | 1,000 | Complementary low-cost keys defeat immediate marginal ranking |
| Weighted common deadline, 48 vertices, total weight 96, quotas `(72,77)` | 35 | Not applied | Unequal weights and incomplete quotas are solved exactly |
| Dense SCC, 10 vertices | 20 | 22 | Exact cost can improve the stated heuristic beyond the constructed trap |
| Weighted cycles, 24 vertices, total weight 75, quotas `(74,73)` | 5 | Not applied | Tight incomplete quotas require a positive refinement budget |
| Dense SCC, 12 vertices | Unknown | Not run | Explicit component-size cutoff |
| Single directed cycle, 24 vertices | Unknown | Not run | Same cutoff, even though a specialized cycle solver could do better |

The corpus contains 15 cases: 13 exact certified solutions and 2 explicit
resource-limited unknowns. All cases are in `synthesis_benchmarks.csv` and are
regenerated by the runner. An observed
single-run timing log is written to
`$TWINS_LOG_DIR/refinement_synthesis_timings.json` (default `build_logs/`).
Timing is deliberately separate from deterministic results, records one
repetition, and is not used for a speedup or statistical performance claim.
The scale result is an exactness/structure demonstration, not evidence that
all 48-pivot domains are easy or that this solver outperforms specialized
feedback-vertex-set implementations.

## 9. Reusable interface and reproduction

From the repository root, using the locked project environment:

```bash
uv run python scripts/run_refinement_synthesis.py --study

uv run python scripts/check_synthesis_order_oracle.py

uv run python scripts/run_refinement_synthesis.py \
  --input results/synthesis/examples/bow_tie_cost.input.json \
  --output /tmp/bow_tie_certificate.json

uv run python scripts/run_refinement_synthesis.py \
  --verify /tmp/bow_tie_certificate.json \
  --expect-input results/synthesis/examples/bow_tie_cost.input.json
```

Use `--expect-input` to bind certificate validation to the intended problem;
without it the checker validates the problem embedded in the certificate.
`.json.gz` input and output certificates are supported. The API is
`Problem(domain, deficit0, deficit1, costs, allowed_split, required_split)`,
`synthesize(problem)` and `verify_certificate(certificate, expected_problem)`.
Input JSON encodes positive integer `weights`, nonnegative integer `costs`,
two `deficits`, event-pair `precedence`, `allowed_split`, `required_split`, and
`initially_ready: true`. Complete executable examples are shipped for a forced
one-pivot repair, post-signature repair, crossed deadlines, the unequal-cost
two-cycle motif and weighted granularity.

The full study honors `TWINS_OUTPUT_ROOT` and `TWINS_LOG_DIR`. A per-instance
request can set `--max-component-size` and `--time-budget`. It returns the
concrete plan and proof together, so a different implementation may consume
the plan and revalidate the certificate without trusting the optimizing
program's internal decisions.

## References and attribution

- R. M. McConnell, K. Mehlhorn, S. Näher and P. Schweitzer. *Certifying
  algorithms*. Computer Science Review 5(2):119–161, 2011.
  DOI: [10.1016/j.cosrev.2010.09.009](https://doi.org/10.1016/j.cosrev.2010.09.009).
- E. Alkassar, S. Böhme, K. Mehlhorn and C. Rizkallah. *A Framework for the
  Verification of Certifying Computations*. 2013 manuscript,
  [arXiv:1301.7462](https://arxiv.org/abs/1301.7462).
  This supplies context for verified checker architectures; it is not a claim
  that the Python checker here has been verified in that framework.
- R. Tarjan. *Depth-First Search and Linear Graph Algorithms*. SIAM Journal on
  Computing 1(2):146–160, 1972.
  DOI: [10.1137/0201010](https://doi.org/10.1137/0201010).
- The existing manuscript cites the classical reversible-pair/alternating-cycle
  criterion and feedback-set hardness sources. Those established graph and
  order-theoretic ingredients are not presented as new algorithms here.
