# Mechanized repair graph–event order bridge

## What is newly proved

`formal/lean/SchedulerClosure/GraphRealization.lean` closes the graph/order gap
left explicit in the first repair-frontier revision. Its principal result is
an equivalence between an acyclic induced repair graph and an actual finite
schedule of **all** event opportunities, with every selected vote preceding
its own repair. The capacity formula is not a hypothesis of this proof.

This formalizes the classical reversal/alternating-cycle argument used in the
paper. It is an assurance improvement, not a claim that the underlying
combinatorial criterion is new.

## Precise objects and assumptions

- `Event` and `Pivot` are arbitrary types; no bounded `Fin 3` encoding occurs.
- `p : Event → Event → Prop` is the **transitive strict precedence relation**.
- `repair vote : Pivot → Event` identify the repair and second-signature slots.
- `selected : Pivot → Prop` identifies the intended jointly reusable pivots.
- Event kinds are disjoint: `∀ i j, repair i ≠ vote j`.
- For the finite realization theorem, a list `events` covers every event.
  The list need not be duplicate-free; the resulting time assignment is
  nevertheless injective.

The augmented event relation is

```text
Augmented p repair vote selected x y :=
  p x y ∨ ∃ i, selected i ∧ x = vote i ∧ y = repair i.
```

The induced repair graph is

```text
RepairGraph p repair vote selected i j :=
  selected i ∧ selected j ∧ p (repair i) (vote j).
```

`Acyclic r` means that no vertex has a **nonempty** `Relation.TransGen r`
path to itself. Self-loops are therefore excluded, as required for forced-early
repairs. Reflexive closure is used only for prefixes and suffixes of the
intermediate normal-form argument, not for graph acyclicity.

## Auditable theorem statements

### `repair_graph_reversal_iff`

Given transitivity and irreflexivity of `p` and disjoint repair/vote kinds,

```text
Acyclic (Augmented p repair vote selected)
  ↔ Acyclic (RepairGraph p repair vote selected).
```

This theorem does not require finiteness. It has no capacity, graph-optimum,
schedule-existence or state-machine-behavior assumption.

The proof first derives a normal form for an arbitrary augmented path: an old
precedence prefix, a chain of reversals joined by induced repair-graph paths,
and an old precedence suffix. If an augmented cycle exists, its suffix and
prefix close a repair-graph cycle. Conversely, each repair-graph edge lifts
to old event precedence followed by the target's requested reversal; a graph
cycle thus lifts to an augmented event cycle.

### `finite_acyclic_iff_schedule`

For any relation `r` on an explicitly covered finite event domain,

```text
Acyclic r ↔
  ∃ time : Event → Nat,
    (∀ x y, time x = time y → x = y) ∧
    (∀ x y, r x y → time x < time y).
```

The existence of a topological order is proved, not assumed. A vertex's rank
is the number of its strict ancestors in the covering list. For every edge,
the predecessor's ancestor set is included in the successor's, and the
predecessor itself witnesses a strict increase. An enumeration index breaks
rank ties inside blocks of size `events.length + 1`.

The resulting timestamps may have gaps. Since they are injective, increasing
time is a full linear extension, with one distinct position per opportunity.
The proof uses classical decidability of reachability and equality. It is an
existence proof for arbitrary finite relations, not a refinement proof of the
Python topological-sort implementation.

### `repair_graph_iff_realizable_schedule`

Combining the first two results establishes

```text
Acyclic (RepairGraph p repair vote selected) ↔
  ∃ time : Event → Nat,
    (∀ x y, time x = time y → x = y) ∧
    (∀ x y, p x y → time x < time y) ∧
    (∀ i, selected i → time (vote i) < time (repair i)).
```

This is the full graph-to-event-order bridge used by the repair-frontier
argument. It is stronger than independently testing small finite instances.

### `repair_graph_from_covers_iff_schedule`

An implementation can provide any acyclic relation `edges` of immediate
precedence constraints. The repair graph is built using `TransGen edges`,
while the returned schedule need only be checked against the original edges.
The same exact equivalence follows.

This version addresses an important representation issue: an intermediate
opportunity cannot be deleted merely because its message is suppressed.
Every event remains covered, and paths through suppressed slots still affect
the repair graph's transitive reachability.

## What this does and does not close

The previous scope statement “graph interpretation and finite linear-extension
correspondence are outside the Lean proof” can now be replaced by a reference
to these four declarations. The graph interpretation is established over
unbounded domains, and the finite scheduling step is proved for every finite
enumeration.

The following are separate obligations and must not be described as proved
by this module:

1. BFT state-machine guards, observation coverage and independence of pivot
   contributions.
2. Refinement of the Python event interpreter or a production CometBFT client.
3. Maximum-cardinality or maximum-weight optimization over induced acyclic
   sets, its quota arithmetic and the chosen optimization implementation.
4. Sound extraction of a certificate schema from arbitrary production code.

The module supplies the nontrivial order-realizability premise those arguments
need. It does not substitute a graph property for a missing behavioral premise.

## Executed checks

The following commands completed successfully with the repository's pinned
Lean `v4.33.0` toolchain:

```bash
lake build SchedulerClosure.GraphRealization
lake env leanchecker SchedulerClosure.GraphRealization
```

An independent `#print axioms` invocation gave:

| Declaration | Reported axiom dependencies |
|---|---|
| `repair_graph_reversal_iff` | None |
| `finite_acyclic_iff_schedule` | `propext`, `Classical.choice`, `Quot.sound` |
| `repair_graph_iff_realizable_schedule` | `propext`, `Classical.choice`, `Quot.sound` |
| `repair_graph_from_covers_iff_schedule` | `propext`, `Classical.choice`, `Quot.sound` |

These are Lean's standard logical principles, with no user-defined axiom,
admitted proof, native-decision shortcut or bounded-enumeration oracle.

For integration, import `SchedulerClosure.GraphRealization` from the main
library and include the four declarations above in the central axiom audit.
