# Mechanized scheduler refinement beyond independent pivots

`formal/lean/SchedulerClosure/TransitionRefinement.lean` adds a general semantic
layer over arbitrary labelled transition systems. The independent-pivot graph
and four-role optimizer remain a specialized tractable structure. None of the
new semantic results assumes independent participants, fixed vote support,
quorums, repair frontiers, acyclic execution graphs, or a bounded number of
protocol transitions.

This document uses result titles and Lean declaration names so that changes in
manuscript numbering do not alter the mapping. The proof module is imported by
`formal/lean/SchedulerClosure.lean`; nineteen of its declarations join the
selected axiom audit. The complete selected audit has 46 declarations.

## 1. The scheduler interface

A fine key identifies one persistent Boolean scheduling choice. The function
`fibre : Fine → Coarse` specifies which fine keys share a decision before a
coarse fibre is split. Outside a selected set `split`, `UniformOutside` requires
all fine keys in a fibre to have the same decision. Inside it, different fine
keys may differ; repeated occurrences of the same fine key must still agree.

The semantics separates arbitrary protocol state from this particular control
interface. Protocol transitions may be internal or may record a fine-key
Boolean decision. An execution can contain state-dependent enabling, changes
to several participants, repeated keys, feedback, and loops. There is no rule
that identifies independent contributions to a quorum.

For a predicate of observed decisions `observed`, `Consistent observed` means
that a fine key never occurs with both answers. `Mixed fibre observed b` means
that some fine key in fibre `b` occurs with `false` and some fine key in that
fibre occurs with `true`. Under consistency these witnesses must be distinct
fine keys.

### Exact policy completion

`policy_realizable_iff` proves

\[
\operatorname{Realizable}(S,O)
\quad\Longleftrightarrow\quad
\operatorname{Consistent}(O)\;\land\;
\operatorname{Mixed}(O)\subseteq S.
\]

The reverse implication constructs a total policy. A split fibre uses a fine
key's own observed answer. An unsplit fibre uses the fibre's observed answer.
Unobserved choices can be set to false. Consistency prevents a repeated fine
key from being overwritten, and absence of an unsplit mixed fibre prevents a
conflict between distinct fine keys. This construction is the substantive
sufficiency argument; a realizable policy is not a premise of that direction.

For required fibres `Q`, `least_split_set` proves that
`Needed = Q ∪ Mixed(O)` realizes a consistent trace and is contained in every
realizing split set containing `Q`. `admissible_refinement_exists_iff` adds an
allowed set `D`: some admissible refinement exists exactly when the trace is
consistent and `Needed ⊆ D`.

`minimum_trace_refinement` proves that `Needed` attains the minimum sum of
nonnegative integer costs among all admissible refinements for this trace.
The sum is over an explicit finite enumeration of coarse keys. A client of the
definition enumerates each key once and covers its interface; the monotonicity
proof itself remains valid even for lists with repetitions. Zero-cost fibres
are permitted. Multiple minimum split sets can exist.

These results apply to arbitrary observation predicates; finiteness is not
needed for Boolean policy completion. The cost sum has a finite interface
presentation. The executable solver uses finite visible traces represented by
persistent partial assignments.

## 2. Persistent memory and cost

`PartialPolicy Fine` is `Fine → Option Bool`. `none` is unseen; `some false`
and `some true` are the two observed choices. A query is legal exactly when
the key is unseen or the query repeats its stored answer.

`remember_occurrences_iff` proves that a legal update represents exactly the
union of the previous observations and the new query. It neither deletes an
old observation nor silently replaces its Boolean value.

`query_guard_iff_consistent_extension` proves that the executable update guard
is equivalent to consistency of that union. `trace_cost_mono` proves that
extending observations can only add mixed fibres, and
`memory_update_cost_mono` applies the result to the partial-memory update. It
therefore justifies the nondecreasing state cost used by the reachability
certificate. Required fibres are included before the first transition.

The Python encoding uses `-1`, `0`, and `1`; the Lean encoding uses `Option
Bool`. The structural memory fact is proved. Parsing the concrete tuple,
constructing the complete product graph, and the correspondence of Python
functions to these definitions are separately tested, not kernel-verified.

## 3. Closed strict-sublevel certificates

`Reachable step start finish` denotes a finite path in an arbitrary relation.
Let `cost` be nondecreasing on its edges and let `K` be a claimed lower bound.
A cut `C` has three local obligations:

1. The initial state belongs to `C` if its cost is below `K`.
2. Every successor of a state in `C` also belongs to `C` whenever that
   successor's cost is below `K`.
3. No state in `C` is a goal.

`reachable_below_in_cut` proves by induction that every reachable state below
`K` belongs to `C`. The key step uses monotonicity to show that its predecessor
also lies below `K`. `sublevel_certificate_lower_bound` then excludes every
reachable goal of cost less than `K`.

`sublevel_certified_minimum` adds an actual path to a goal of cost `K`. The path
supplies feasibility and the cut supplies the lower bound, so the witness is
minimum among all finite goal-reaching executions of the declared relation.
The statement includes `K = 0`, nonzero mandatory initial cost, arbitrary
zero-cost transitions, and cycles. A cut need not contain only reachable
states, and need not enumerate states at or above the threshold.

`closed_certificate_infeasible` proves the analogous full-closure rule with no
cost threshold: a closed set containing the initial state and excluding every
goal excludes all finite goal-reaching executions. A finite search that runs
out of a configured resource budget has not supplied this proof and must
report unknown.

The mathematical certificate rule does not need a finite graph. The executable
producer and checker require finite enumerations for termination and must
account for every relevant successor. The Lean theorem does not itself
establish completeness of a Python successor generator.

## 4. The exact direction of implementation transfer

`LabelSimulation` checks local transitions. Every concrete controlled edge
must map to an abstract edge with the identical fine key and Boolean value.
A concrete internal edge may map to an abstract internal edge or to equality
of abstract states. `labelled_execution_simulates` derives complete visible
trace preservation by induction. With concrete bad states included in
abstract bad states, `bad_trace_coverage` follows. Neither theorem assumes
whole-path coverage as a hypothesis.

This is the direction needed for lower bounds: every concrete bad trace must
be covered by the abstract model. The model can have extra traces and can
therefore underestimate the required refinement cost. The same fine decisions
have the same consistency and mixed-fibre set under an unchanged interface.
A state projection that discards a controlled decision does not meet these
label-preserving hypotheses.

A more general `reachable_simulates` allows each concrete edge to be simulated
by any finite abstract path. `abstract_lower_bound_transfers` combines those
local path obligations with a checked abstract sublevel cut, inclusion of
concrete goals, and abstract cost no greater than concrete cost. It proves the
concrete lower bound directly from those local conditions.

`matching_concrete_witness_is_minimum` adds a concrete goal-reaching witness
whose cost equals the certified abstract lower bound. It concludes an actual
concrete minimum. It does not require every abstract witness to lift and does
not require the abstraction to be exact. `abstract_infeasibility_transfers`
likewise transfers a full closed invariant through the covering simulation.

An executed witness alone gives an upper bound. Abstract trace coverage alone
gives a lower bound. Their equality yields optimality. Ordinary client
conformance tests do not establish the quantified local coverage conditions.
A production-client claim requires a proved or exhaustively checked account
of the relevant client transitions and its declared scheduler interface.

## 5. Invariant-guided elimination of a spurious policy

For one fixed fine policy, take `step` to be its compatible concrete relation.
A concrete search that establishes no bad state produces its reachable set
`R`: it contains the initial state, is closed under these edges, and excludes
bad states. The proof only requires an inductive invariant with these three
properties; it need not be the least reachable set.

`QuotientStep` is the exact existential quotient of this fixed-policy relation.
An abstract block is bad when it contains a concrete bad state.
`invariant_quotient_excludes_goal` proves that the quotient retains a bad-free
invariant whenever no block mixes states inside and outside `R`.

`invariantSplit` refines each old block by the Boolean membership value of
`R`. `invariant_split_saturated` proves the new blocks are homogeneous.
`invariant_split_eliminates_policy` proves that the new quotient has no bad
path under this policy. Consequently the entire false policy is eliminated,
including other spurious traces the earlier optimizer did not return.

`spurious_policy_forces_strict_split` proves that if the previous quotient had
a bad path, some old block necessarily contains a state inside `R` and another
outside `R`. Therefore the new partition is strictly finer. For a finite
concrete state set, the resulting upper bound of the number of states minus
the number of initial blocks on strict refinements is a paper finite-partition
argument; the Lean file does not prove that cardinality arithmetic or verify
the CEGAR implementation.

## 6. Executed verification and limits

The expanded integrated build completed 15 jobs. The selected 46-declaration
axiom audit and `leanchecker SchedulerClosure` both exited with status zero.
Source hygiene checked 23 Lean/Coq files with no findings. Exact axiom
dependencies are listed in `formal/lean/AXIOM_REPORT.md`.

Policy completion and arbitrary membership predicates use Lean's standard
classical axioms. The labelled execution simulation, bad-trace coverage,
full-closure infeasibility and invariant-preserving quotient theorem have no
axiom dependencies. The numerical cut and lower-bound transfer proofs use
`propext` and `Quot.sound`, and do not require classical choice. No project
axiom or admitted proof is introduced.

The expanded mechanization proves scheduler-interface semantics, local
certificate rules and generic transfer/refinement principles. It does not
prove that a supplied production BFT implementation realizes a supplied model,
that every paper optimizer is the Lean function, or that finite-state model
bounds cover arbitrary messages, heights, storage, network behavior or faults.
The general semantics no longer depends on the independent-pivot contract;
its remaining boundary is the explicitly chosen control interface and the
transition-system coverage evidence supplied for each implementation.
