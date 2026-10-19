import SchedulerClosure.CertificateOptimality

/-!
# Scheduler refinement for arbitrary labelled transition systems

The interface contains fine Boolean decision keys and their coarse fibres.
A static policy must repeat a fine key's decision, but may distinguish fine
keys in a fibre exactly when that fibre is split. No independence, quorum,
pivot, acyclicity or finite-state assumption is made in the semantic results.

This file proves policy completion and the least required split set, soundness
of the executable solver's strict-sublevel closure certificate, and transfer
of certified lower bounds through local stuttering simulations. Finiteness is
needed by an exhaustive implementation to terminate, not by these theorems.
The Python implementation and a production-client correspondence are separate
obligations; no transition relation is identified with a client by definition.
-/

namespace SchedulerClosure.TransitionRefinement

/-- Occurrences can be the visible projection of any finite execution. The
completion theorem also applies to an arbitrary predicate of observations. -/
abbrev Occurrences (Fine : Type u) := Fine → Bool → Prop

/-- Repeated queries of one fine key must receive the same static answer. -/
def Consistent {Fine : Type u} (observed : Occurrences Fine) : Prop :=
  ∀ f a b, observed f a → observed f b → a = b

/-- A coarse fibre is mixed when the trace has observed both Boolean answers
inside that fibre. Under consistency these must occur at different fine keys. -/
def Mixed {Fine : Type u} {Coarse : Type v}
    (fibre : Fine → Coarse) (observed : Occurrences Fine) (coarse : Coarse) : Prop :=
  ∃ f g, fibre f = coarse ∧ fibre g = coarse ∧
    observed f false ∧ observed g true

/-- Unsplit fibres retain a single admission decision shared by all fine keys. -/
def UniformOutside {Fine : Type u} {Coarse : Type v}
    (fibre : Fine → Coarse) (split : Coarse → Prop) (policy : Fine → Bool) : Prop :=
  ∀ f g, fibre f = fibre g → ¬ split (fibre f) → policy f = policy g

/-- One total static policy realizes every visible decision in the execution. -/
def Realizable {Fine : Type u} {Coarse : Type v}
    (fibre : Fine → Coarse) (split : Coarse → Prop)
    (observed : Occurrences Fine) : Prop :=
  ∃ policy : Fine → Bool, UniformOutside fibre split policy ∧
    ∀ f b, observed f b → policy f = b

/-- Complete unobserved choices by `false`. A split fibre uses each fine key's
own observations; an unsplit fibre uses the observations of its entire fibre. -/
noncomputable def completion {Fine : Type u} {Coarse : Type v}
    (fibre : Fine → Coarse) (split : Coarse → Prop)
    (observed : Occurrences Fine) (f : Fine) : Bool := by
  classical
  exact if split (fibre f) then
    if observed f true then true else false
  else
    if ∃ g, fibre g = fibre f ∧ observed g true then true else false

theorem completion_agrees {Fine : Type u} {Coarse : Type v}
    (fibre : Fine → Coarse) (split : Coarse → Prop)
    (observed : Occurrences Fine)
    (consistent : Consistent observed)
    (covered : ∀ b, Mixed fibre observed b → split b)
    {f : Fine} {value : Bool} (seen : observed f value) :
    completion fibre split observed f = value := by
  classical
  cases value with
  | false =>
    by_cases hs : split (fibre f)
    · have hn : ¬ observed f true := by
        intro h
        have contradiction := consistent f false true seen h
        cases contradiction
      simp [completion, hs, hn]
    · have hn : ¬ ∃ g, fibre g = fibre f ∧ observed g true := by
        rintro ⟨g, hg, ht⟩
        exact hs (covered (fibre f) ⟨f, g, rfl, hg, seen, ht⟩)
      simp [completion, hs, hn]
  | true =>
    by_cases hs : split (fibre f)
    · simp [completion, hs, seen]
    · have hw : ∃ g, fibre g = fibre f ∧ observed g true := ⟨f, rfl, seen⟩
      simp [completion, hs, hw]

theorem completion_uniform {Fine : Type u} {Coarse : Type v}
    (fibre : Fine → Coarse) (split : Coarse → Prop)
    (observed : Occurrences Fine) :
    UniformOutside fibre split (completion fibre split observed) := by
  classical
  intro f g hfg hs
  simp only [completion, hs, ↓reduceIte, ← hfg]

/-- Exact policy realizability. Fine-key consistency is necessary even after
all fibres are split; otherwise mixed fibres are the only coupling constraint. -/
theorem policy_realizable_iff {Fine : Type u} {Coarse : Type v}
    (fibre : Fine → Coarse) (split : Coarse → Prop)
    (observed : Occurrences Fine) :
    Realizable fibre split observed ↔
      Consistent observed ∧ ∀ b, Mixed fibre observed b → split b := by
  constructor
  · rintro ⟨policy, uniform, agrees⟩
    constructor
    · intro f a b ha hb
      exact (agrees f a ha).symm.trans (agrees f b hb)
    · intro b mixed
      classical
      by_cases hs : split b
      · exact hs
      · rcases mixed with ⟨f, g, hf, hg, hfalse, htrue⟩
        have hsame := uniform f g (hf.trans hg.symm) (by simpa only [hf] using hs)
        rw [agrees f false hfalse, agrees g true htrue] at hsame
        cases hsame
  · rintro ⟨hc, hm⟩
    exact ⟨completion fibre split observed, completion_uniform fibre split observed,
      fun _ _ h => completion_agrees fibre split observed hc hm h⟩

/-- Required fibres are paid for even when this particular trace does not mix them. -/
def Needed {Fine : Type u} {Coarse : Type v}
    (fibre : Fine → Coarse) (required : Coarse → Prop)
    (observed : Occurrences Fine) (b : Coarse) : Prop :=
  required b ∨ Mixed fibre observed b

/-- Allowed and required refinement restrictions are part of the interface. -/
def Admissible {Fine : Type u} {Coarse : Type v}
    (fibre : Fine → Coarse) (allowed required split : Coarse → Prop)
    (observed : Occurrences Fine) : Prop :=
  (∀ b, required b → split b) ∧ (∀ b, split b → allowed b) ∧
    Realizable fibre split observed

/-- The least split set is proved by inclusion, not postulated from the search. -/
theorem least_split_set {Fine : Type u} {Coarse : Type v}
    (fibre : Fine → Coarse) (required : Coarse → Prop)
    (observed : Occurrences Fine) (consistent : Consistent observed) :
    Realizable fibre (Needed fibre required observed) observed ∧
      ∀ split, (∀ b, required b → split b) → Realizable fibre split observed →
        ∀ b, Needed fibre required observed b → split b := by
  constructor
  · exact (policy_realizable_iff fibre _ observed).mpr
      ⟨consistent, fun _ h => Or.inr h⟩
  · intro split hr realizable b needed
    rcases needed with hrequired | hmixed
    · exact hr b hrequired
    · exact ((policy_realizable_iff fibre split observed).mp realizable).2 b hmixed

/-- Exact feasibility under an arbitrary allowed/required interface. -/
theorem admissible_refinement_exists_iff {Fine : Type u} {Coarse : Type v}
    (fibre : Fine → Coarse) (allowed required : Coarse → Prop)
    (observed : Occurrences Fine) :
    (∃ split, Admissible fibre allowed required split observed) ↔
      Consistent observed ∧
        ∀ b, Needed fibre required observed b → allowed b := by
  constructor
  · rintro ⟨split, hr, ha, hp⟩
    have hc := ((policy_realizable_iff fibre split observed).mp hp).1
    refine ⟨hc, ?_⟩
    intro b hb
    exact ha b ((least_split_set fibre required observed hc).2 split hr hp b hb)
  · rintro ⟨hc, ha⟩
    exact ⟨Needed fibre required observed, (fun _ h => Or.inl h), ha,
      (least_split_set fibre required observed hc).1⟩

/-- A finite key enumeration gives the interface's sum of nonnegative costs.
Applications enumerate every coarse key once. Monotonicity itself needs no
uniqueness or coverage assumption on the list. -/
noncomputable def splitCost {Coarse : Type v}
    (keys : List Coarse) (cost : Coarse → Nat) (split : Coarse → Prop) : Nat := by
  classical
  exact (keys.map (fun b => if split b then cost b else 0)).sum

theorem split_cost_mono {Coarse : Type v}
    (keys : List Coarse) (cost : Coarse → Nat) (left right : Coarse → Prop)
    (contained : ∀ b, left b → right b) :
    splitCost keys cost left ≤ splitCost keys cost right := by
  classical
  induction keys with
  | nil => simp [splitCost]
  | cons b keys ih =>
    by_cases hl : left b
    · have hr := contained b hl
      simp only [splitCost, List.map_cons, List.sum_cons, hl, hr, ↓reduceIte] at *
      omega
    · by_cases hr : right b <;>
        simp only [splitCost, List.map_cons, List.sum_cons, hl, hr, ↓reduceIte,
          Nat.zero_add] at * <;> omega

/-- For every consistent execution the mandatory/mixed union is an actual
minimum-cost admissible refinement, including indivisible and zero costs. -/
theorem minimum_trace_refinement {Fine : Type u} {Coarse : Type v}
    (fibre : Fine → Coarse) (allowed required : Coarse → Prop)
    (observed : Occurrences Fine) (keys : List Coarse) (cost : Coarse → Nat)
    (consistent : Consistent observed)
    (permitted : ∀ b, Needed fibre required observed b → allowed b) :
    Admissible fibre allowed required (Needed fibre required observed) observed ∧
      ∀ split, Admissible fibre allowed required split observed →
        splitCost keys cost (Needed fibre required observed) ≤ splitCost keys cost split := by
  have least := least_split_set fibre required observed consistent
  constructor
  · exact ⟨(fun _ h => Or.inl h), permitted, least.1⟩
  · rintro split ⟨hr, _, hp⟩
    exact split_cost_mono keys cost _ split (least.2 split hr hp)

/-- Appending observations can only add mixed fibres; this is the mathematical
reason the product state's refinement cost cannot decrease along a run. -/
theorem needed_mono {Fine : Type u} {Coarse : Type v}
    (fibre : Fine → Coarse) (required : Coarse → Prop)
    (before after : Occurrences Fine)
    (extendsObs : ∀ f b, before f b → after f b) :
    ∀ b, Needed fibre required before b → Needed fibre required after b := by
  intro b h
  rcases h with hr | ⟨f, g, hf, hg, hfalse, htrue⟩
  · exact Or.inl hr
  · exact Or.inr ⟨f, g, hf, hg, extendsObs f false hfalse, extendsObs g true htrue⟩

theorem trace_cost_mono {Fine : Type u} {Coarse : Type v}
    (fibre : Fine → Coarse) (required : Coarse → Prop)
    (before after : Occurrences Fine) (keys : List Coarse) (cost : Coarse → Nat)
    (extendsObs : ∀ f b, before f b → after f b) :
    splitCost keys cost (Needed fibre required before) ≤
      splitCost keys cost (Needed fibre required after) := by
  exact split_cost_mono keys cost _ _ (needed_mono fibre required before after extendsObs)

/-- The executable product remembers one optional Boolean answer per fine key. -/
abbrev PartialPolicy (Fine : Type u) := Fine → Option Bool

/-- A query either sets a previously unseen key or repeats its stored answer. -/
def QueryAllowed {Fine : Type u} (memory : PartialPolicy Fine)
    (key : Fine) (value : Bool) : Prop :=
  memory key = none ∨ memory key = some value

noncomputable def remember {Fine : Type u} (memory : PartialPolicy Fine)
    (key : Fine) (value : Bool) (f : Fine) : Option Bool := by
  classical
  exact if f = key then some value else memory f

/-- A legal memory update records exactly one additional observation. The
same fine-key answer persists; this lemma would fail for an overwriting update. -/
theorem remember_occurrences_iff {Fine : Type u}
    (memory : PartialPolicy Fine) (key : Fine) (value : Bool)
    (allowed : QueryAllowed memory key value) (f : Fine) (b : Bool) :
    remember memory key value f = some b ↔
      memory f = some b ∨ (f = key ∧ b = value) := by
  classical
  by_cases hf : f = key
  · subst f
    rcases allowed with unseen | same
    · simp [remember, unseen, eq_comm]
    · simp [remember, same, eq_comm]
  · simp [remember, hf]

/-- Functional memory has one answer per key by construction. -/
theorem memory_consistent {Fine : Type u} (memory : PartialPolicy Fine) :
    Consistent (fun f b => memory f = some b) := by
  intro f a b ha hb
  exact Option.some.inj (ha.symm.trans hb)

/-- The concrete three-valued memory guard is exactly the global trace
consistency condition for extending the stored observations by one query. -/
theorem query_guard_iff_consistent_extension {Fine : Type u}
    (memory : PartialPolicy Fine) (key : Fine) (value : Bool) :
    QueryAllowed memory key value ↔
      Consistent (fun f b => memory f = some b ∨ (f = key ∧ b = value)) := by
  constructor
  · intro allowed f a b ha hb
    have left := (remember_occurrences_iff memory key value allowed f a).mpr ha
    have right := (remember_occurrences_iff memory key value allowed f b).mpr hb
    exact Option.some.inj (left.symm.trans right)
  · intro consistent
    cases h : memory key with
    | none => exact Or.inl h
    | some old =>
      have equal := consistent key old value (Or.inl h) (Or.inr ⟨rfl, rfl⟩)
      exact Or.inr (by simpa only [equal] using h)

/-- Monotone refinement cost of every legal product-memory update is proved
from the occurrence representation, rather than separately assumed. -/
theorem memory_update_cost_mono {Fine : Type u} {Coarse : Type v}
    (fibre : Fine → Coarse) (required : Coarse → Prop)
    (keys : List Coarse) (cost : Coarse → Nat)
    (memory : PartialPolicy Fine) (key : Fine) (value : Bool)
    (allowed : QueryAllowed memory key value) :
    splitCost keys cost (Needed fibre required (fun f b => memory f = some b)) ≤
      splitCost keys cost
        (Needed fibre required (fun f b => remember memory key value f = some b)) := by
  apply trace_cost_mono
  intro f b seen
  exact (remember_occurrences_iff memory key value allowed f b).mpr (Or.inl seen)

/-- A finite execution records only externally controlled Boolean decisions;
internal transitions are retained in the path but contribute no decision. -/
inductive Execution {State : Type u} {Fine : Type v}
    (step : State → Option (Fine × Bool) → State → Prop) :
    State → List (Fine × Bool) → State → Prop where
  | nil (x : State) : Execution step x [] x
  | internal {x y z : State} {trace : List (Fine × Bool)} :
      step x none y → Execution step y trace z → Execution step x trace z
  | controlled {x y z : State} {key : Fine} {value : Bool}
      {trace : List (Fine × Bool)} :
      step x (some (key, value)) y → Execution step y trace z →
      Execution step x ((key, value) :: trace) z

/-- Local abstraction coverage preserves every controlled decision. Only an
internal transition may collapse to equality of abstract states. -/
def LabelSimulation {Concrete : Type u} {Abstract : Type v} {Fine : Type w}
    (concrete : Concrete → Option (Fine × Bool) → Concrete → Prop)
    (abstract : Abstract → Option (Fine × Bool) → Abstract → Prop)
    (project : Concrete → Abstract) : Prop :=
  ∀ x label y, concrete x label y →
    abstract (project x) label (project y) ∨ (label = none ∧ project x = project y)

/-- State dependencies, repeated keys, loops, and arbitrary silent work do
not affect this trace preservation argument. No path correspondence is assumed. -/
theorem labelled_execution_simulates
    {Concrete : Type u} {Abstract : Type v} {Fine : Type w}
    (concrete : Concrete → Option (Fine × Bool) → Concrete → Prop)
    (abstract : Abstract → Option (Fine × Bool) → Abstract → Prop)
    (project : Concrete → Abstract)
    (covers : LabelSimulation concrete abstract project)
    {start finish : Concrete} {trace : List (Fine × Bool)}
    (execution : Execution concrete start trace finish) :
    Execution abstract (project start) trace (project finish) := by
  induction execution with
  | nil x => exact .nil (project x)
  | @internal x y z trace edge tail ih =>
    rcases covers x none y edge with ha | ⟨_, hsame⟩
    · exact .internal ha ih
    · simpa only [hsame] using ih
  | @controlled x y z key value trace edge tail ih =>
    rcases covers x (some (key, value)) y edge with ha | ⟨impossible, _⟩
    · exact .controlled ha ih
    · cases impossible

/-- Unsafe coverage is one-way: the abstraction may contain extra bad traces,
but it must contain every concrete bad execution for lower-bound transfer. -/
theorem bad_trace_coverage
    {Concrete : Type u} {Abstract : Type v} {Fine : Type w}
    (concrete : Concrete → Option (Fine × Bool) → Concrete → Prop)
    (abstract : Abstract → Option (Fine × Bool) → Abstract → Prop)
    (project : Concrete → Abstract) (concreteBad : Concrete → Prop)
    (abstractBad : Abstract → Prop)
    (covers : LabelSimulation concrete abstract project)
    (badCovered : ∀ x, concreteBad x → abstractBad (project x))
    {start finish : Concrete} {trace : List (Fine × Bool)}
    (execution : Execution concrete start trace finish) (bad : concreteBad finish) :
    ∃ finish', Execution abstract (project start) trace finish' ∧ abstractBad finish' := by
  exact ⟨project finish,
    labelled_execution_simulates concrete abstract project covers execution,
    badCovered finish bad⟩

/-- Reflexive finite reachability with no cardinality or acyclicity restriction. -/
inductive Reachable {State : Type u} (step : State → State → Prop)
    (start : State) : State → Prop where
  | refl : Reachable step start start
  | tail {x y : State} : Reachable step start x → step x y → Reachable step start y

theorem reachable_trans {State : Type u} {step : State → State → Prop}
    {x y z : State} (first : Reachable step x y) (second : Reachable step y z) :
    Reachable step x z := by
  induction second with
  | refl => exact first
  | tail _ edge ih => exact .tail ih edge

/-- A local path simulation is lifted by induction, allowing any finite amount
of abstract stuttering work for each concrete transition. -/
theorem reachable_simulates {Concrete : Type u} {Abstract : Type v}
    (concrete : Concrete → Concrete → Prop) (abstract : Abstract → Abstract → Prop)
    (project : Concrete → Abstract)
    (covers : ∀ x y, concrete x y → Reachable abstract (project x) (project y))
    {start finish : Concrete} (path : Reachable concrete start finish) :
    Reachable abstract (project start) (project finish) := by
  induction path with
  | refl => exact .refl
  | @tail x y _ edge ih => exact reachable_trans ih (covers x y edge)

/-- A closed strict sublevel contains every reachable state below its threshold.
The certificate need not list only reachable states, nor the complete graph. -/
theorem reachable_below_in_cut {State : Type u}
    (step : State → State → Prop) (cost : State → Nat) (cut : State → Prop)
    (threshold : Nat) (start : State)
    (monotone : ∀ x y, step x y → cost x ≤ cost y)
    (initial : cost start < threshold → cut start)
    (closed : ∀ x y, cut x → step x y → cost y < threshold → cut y)
    {finish : State} (path : Reachable step start finish) :
    cost finish < threshold → cut finish := by
  induction path with
  | refl => exact initial
  | @tail x y path edge ih =>
    intro below
    have previous : cost x < threshold := by
      have hmono := monotone x y edge
      omega
    exact closed x y (ih previous) edge below

/-- Every goal has cost at least the certified threshold. This proves the
strict-sublevel checker rule, including zero thresholds and cyclic models. -/
theorem sublevel_certificate_lower_bound {State : Type u}
    (step : State → State → Prop) (cost : State → Nat)
    (goal cut : State → Prop) (threshold : Nat) (start : State)
    (monotone : ∀ x y, step x y → cost x ≤ cost y)
    (initial : cost start < threshold → cut start)
    (closed : ∀ x y, cut x → step x y → cost y < threshold → cut y)
    (safe : ∀ x, cut x → ¬ goal x)
    {finish : State} (path : Reachable step start finish) (done : goal finish) :
    threshold ≤ cost finish := by
  have inside := reachable_below_in_cut step cost cut threshold start
    monotone initial closed path
  by_cases below : cost finish < threshold
  · exact False.elim (safe finish (inside below) done)
  · omega

/-- A full closed invariant excluding all goals certifies infeasibility. -/
theorem closed_certificate_infeasible {State : Type u}
    (step : State → State → Prop) (goal cut : State → Prop) (start : State)
    (initial : cut start)
    (closed : ∀ x y, cut x → step x y → cut y)
    (safe : ∀ x, cut x → ¬ goal x) :
    ¬ ∃ finish, Reachable step start finish ∧ goal finish := by
  have contained : ∀ finish, Reachable step start finish → cut finish := by
    intro finish path
    induction path with
    | refl => exact initial
    | @tail x y _ edge ih => exact closed x y ih edge
  rintro ⟨finish, path, done⟩
  exact safe finish (contained finish path) done

/-- A replayed witness reaching the strict-sublevel lower bound is globally
minimum over all finite executions of this declared transition system. -/
theorem sublevel_certified_minimum {State : Type u}
    (step : State → State → Prop) (cost : State → Nat)
    (goal cut : State → Prop) (threshold : Nat) (start : State)
    (monotone : ∀ x y, step x y → cost x ≤ cost y)
    (initial : cost start < threshold → cut start)
    (closed : ∀ x y, cut x → step x y → cost y < threshold → cut y)
    (safe : ∀ x, cut x → ¬ goal x)
    {witness : State} (path : Reachable step start witness)
    (done : goal witness) (attains : cost witness = threshold) :
    (∃ finish, Reachable step start finish ∧ goal finish ∧ cost finish = threshold) ∧
      ∀ finish, Reachable step start finish → goal finish → threshold ≤ cost finish := by
  exact ⟨⟨witness, path, done, attains⟩,
    fun _ p g => sublevel_certificate_lower_bound step cost goal cut threshold start
      monotone initial closed safe p g⟩

/-- A checked abstract sublevel certificate bounds every concrete execution
covered by a local simulation. Abstract costs may underestimate concrete costs.
No assertion that an abstract witness is concretely realizable is required. -/
theorem abstract_lower_bound_transfers {Concrete : Type u} {Abstract : Type v}
    (concrete : Concrete → Concrete → Prop) (abstract : Abstract → Abstract → Prop)
    (project : Concrete → Abstract) (concreteCost : Concrete → Nat)
    (abstractCost : Abstract → Nat) (concreteGoal : Concrete → Prop)
    (abstractGoal cut : Abstract → Prop) (threshold : Nat) (start : Concrete)
    (covers : ∀ x y, concrete x y → Reachable abstract (project x) (project y))
    (costBound : ∀ x, abstractCost (project x) ≤ concreteCost x)
    (goals : ∀ x, concreteGoal x → abstractGoal (project x))
    (monotone : ∀ x y, abstract x y → abstractCost x ≤ abstractCost y)
    (initial : abstractCost (project start) < threshold → cut (project start))
    (closed : ∀ x y, cut x → abstract x y → abstractCost y < threshold → cut y)
    (safe : ∀ x, cut x → ¬ abstractGoal x)
    {finish : Concrete} (path : Reachable concrete start finish)
    (done : concreteGoal finish) : threshold ≤ concreteCost finish := by
  have abstractPath := reachable_simulates concrete abstract project covers path
  have lower := sublevel_certificate_lower_bound abstract abstractCost abstractGoal cut
    threshold (project start) monotone initial closed safe abstractPath (goals finish done)
  exact Nat.le_trans lower (costBound finish)

/-- A concrete witness matching the certified abstract lower bound is concrete
optimality. The statement derives its lower bound from local edge coverage and
cut conditions; it does not assume trace coverage or optimality as a premise. -/
theorem matching_concrete_witness_is_minimum
    {Concrete : Type u} {Abstract : Type v}
    (concrete : Concrete → Concrete → Prop) (abstract : Abstract → Abstract → Prop)
    (project : Concrete → Abstract) (concreteCost : Concrete → Nat)
    (abstractCost : Abstract → Nat) (concreteGoal : Concrete → Prop)
    (abstractGoal cut : Abstract → Prop) (threshold : Nat) (start : Concrete)
    (covers : ∀ x y, concrete x y → Reachable abstract (project x) (project y))
    (costBound : ∀ x, abstractCost (project x) ≤ concreteCost x)
    (goals : ∀ x, concreteGoal x → abstractGoal (project x))
    (monotone : ∀ x y, abstract x y → abstractCost x ≤ abstractCost y)
    (initial : abstractCost (project start) < threshold → cut (project start))
    (closed : ∀ x y, cut x → abstract x y → abstractCost y < threshold → cut y)
    (safe : ∀ x, cut x → ¬ abstractGoal x)
    {witness : Concrete} (path : Reachable concrete start witness)
    (done : concreteGoal witness) (attains : concreteCost witness = threshold) :
    (∃ finish, Reachable concrete start finish ∧ concreteGoal finish ∧
      concreteCost finish = threshold) ∧
      ∀ finish, Reachable concrete start finish → concreteGoal finish →
        threshold ≤ concreteCost finish := by
  exact ⟨⟨witness, path, done, attains⟩,
    fun _ p g => abstract_lower_bound_transfers concrete abstract project
      concreteCost abstractCost concreteGoal abstractGoal cut threshold start
      covers costBound goals monotone initial closed safe p g⟩

/-- Overapproximation plus an abstract closed invariant also transfers
infeasibility. Concrete and abstract numeric costs are irrelevant here. -/
theorem abstract_infeasibility_transfers {Concrete : Type u} {Abstract : Type v}
    (concrete : Concrete → Concrete → Prop) (abstract : Abstract → Abstract → Prop)
    (project : Concrete → Abstract) (concreteGoal : Concrete → Prop)
    (abstractGoal cut : Abstract → Prop) (start : Concrete)
    (covers : ∀ x y, concrete x y → Reachable abstract (project x) (project y))
    (goals : ∀ x, concreteGoal x → abstractGoal (project x))
    (initial : cut (project start))
    (closed : ∀ x y, cut x → abstract x y → cut y)
    (safe : ∀ x, cut x → ¬ abstractGoal x) :
    ¬ ∃ finish, Reachable concrete start finish ∧ concreteGoal finish := by
  rintro ⟨finish, path, done⟩
  exact closed_certificate_infeasible abstract abstractGoal cut (project start)
    initial closed safe ⟨project finish,
      reachable_simulates concrete abstract project covers path, goals finish done⟩

/-- Exact existential quotient edges. In the policy-elimination application,
`step` is the concrete relation restricted by one fixed static fine policy. -/
def QuotientStep {Concrete : Type u} {Abstract : Type v}
    (step : Concrete → Concrete → Prop) (project : Concrete → Abstract)
    (x y : Abstract) : Prop :=
  ∃ c d, project c = x ∧ project d = y ∧ step c d

def QuotientGoal {Concrete : Type u} {Abstract : Type v}
    (goal : Concrete → Prop) (project : Concrete → Abstract) (x : Abstract) : Prop :=
  ∃ c, project c = x ∧ goal c

def InvariantImage {Concrete : Type u} {Abstract : Type v}
    (invariant : Concrete → Prop) (project : Concrete → Abstract) (x : Abstract) : Prop :=
  ∃ c, project c = x ∧ invariant c

/-- Homogeneity means no abstract block mixes invariant and non-invariant states. -/
def Saturated {Concrete : Type u} {Abstract : Type v}
    (project : Concrete → Abstract) (invariant : Concrete → Prop) : Prop :=
  ∀ x y, project x = project y → invariant x → invariant y

/-- An inductive bad-free concrete invariant survives an exact existential
quotient whenever its blocks are homogeneous for that invariant. -/
theorem invariant_quotient_excludes_goal
    {Concrete : Type u} {Abstract : Type v}
    (step : Concrete → Concrete → Prop) (goal invariant : Concrete → Prop)
    (project : Concrete → Abstract) (start : Concrete)
    (initial : invariant start)
    (closed : ∀ x y, invariant x → step x y → invariant y)
    (safe : ∀ x, invariant x → ¬ goal x)
    (homogeneous : Saturated project invariant) :
    ¬ ∃ finish, Reachable (QuotientStep step project) (project start) finish ∧
      QuotientGoal goal project finish := by
  apply closed_certificate_infeasible (QuotientStep step project)
    (QuotientGoal goal project) (InvariantImage invariant project) (project start)
  · exact ⟨start, rfl, initial⟩
  · rintro x y ⟨w, hw, hR⟩ ⟨c, d, hc, hd, edge⟩
    exact ⟨d, hd, closed c d (homogeneous w c (hw.trans hc.symm) hR) edge⟩
  · rintro x ⟨w, hw, hR⟩ ⟨c, hc, bad⟩
    exact safe c (homogeneous w c (hw.trans hc.symm) hR) bad

/-- Split each old block by membership in one concrete inductive invariant. -/
noncomputable def invariantSplit {Concrete : Type u} {Abstract : Type v}
    (project : Concrete → Abstract) (invariant : Concrete → Prop)
    (x : Concrete) : Abstract × Bool := by
  classical
  exact (project x, if invariant x then true else false)

/-- The refinement is homogeneous by construction; no reachability assumption
is hidden in the partition operation. -/
theorem invariant_split_saturated {Concrete : Type u} {Abstract : Type v}
    (project : Concrete → Abstract) (invariant : Concrete → Prop) :
    Saturated (invariantSplit project invariant) invariant := by
  classical
  intro x y same hx
  have bits := congrArg Prod.snd same
  by_cases hy : invariant y
  · exact hy
  · simp only [invariantSplit, hx, hy, ↓reduceIte] at bits
    cases bits

/-- A failed abstract policy is eliminated in its entirety after splitting by
that policy's concrete reachable invariant. This is stronger than excluding
just the particular spurious path returned by the abstract optimizer. -/
theorem invariant_split_eliminates_policy
    {Concrete : Type u} {Abstract : Type v}
    (step : Concrete → Concrete → Prop) (goal invariant : Concrete → Prop)
    (project : Concrete → Abstract) (start : Concrete)
    (initial : invariant start)
    (closed : ∀ x y, invariant x → step x y → invariant y)
    (safe : ∀ x, invariant x → ¬ goal x) :
    ¬ ∃ finish,
      Reachable (QuotientStep step (invariantSplit project invariant))
        (invariantSplit project invariant start) finish ∧
      QuotientGoal goal (invariantSplit project invariant) finish := by
  exact invariant_quotient_excludes_goal step goal invariant
    (invariantSplit project invariant) start initial closed safe
    (invariant_split_saturated project invariant)

/-- If the old quotient admitted a bad path under this policy, its bad-free
concrete invariant must cut at least one old block. Thus elimination makes a
strict partition refinement, not merely a different encoding of the same blocks. -/
theorem spurious_policy_forces_strict_split
    {Concrete : Type u} {Abstract : Type v}
    (step : Concrete → Concrete → Prop) (goal invariant : Concrete → Prop)
    (project : Concrete → Abstract) (start : Concrete)
    (initial : invariant start)
    (closed : ∀ x y, invariant x → step x y → invariant y)
    (safe : ∀ x, invariant x → ¬ goal x)
    (spurious : ∃ finish, Reachable (QuotientStep step project) (project start) finish ∧
      QuotientGoal goal project finish) :
    ∃ x y, project x = project y ∧ invariant x ∧ ¬ invariant y := by
  classical
  by_cases split : ∃ x y, project x = project y ∧ invariant x ∧ ¬ invariant y
  · exact split
  · have homogeneous : Saturated project invariant := by
      intro x y same hx
      by_cases hy : invariant y
      · exact hy
      · exact False.elim (split ⟨x, y, same, hx, hy⟩)
    exact False.elim (invariant_quotient_excludes_goal step goal invariant project start
      initial closed safe homogeneous spurious)

end SchedulerClosure.TransitionRefinement
