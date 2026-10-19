import Std.Tactic

/-!
# Repair-graph reversal and event-order realization

This module proves the graph/event bridge without assuming a capacity formula.
`P` is the transitive strict precedence relation on *opportunities*, including
opportunities whose delivery is suppressed.  Adding `vote i < repair i` for
selected pivots is acyclic exactly when the corresponding induced repair graph
is acyclic.  Repair and vote events must be distinct across event kinds.

The result below is about mathematical event orders, not production-client
refinement.  In particular, it does not establish any BFT state-machine guards.
-/

namespace SchedulerClosure.GraphRealization

open Relation

/-- Acyclicity excludes a nonempty finite path from a vertex to itself. -/
def Acyclic {α : Type u} (r : α → α → Prop) : Prop :=
  ∀ x, ¬ TransGen r x x

/-- Reflexive closure of an already transitive relation. -/
def Before {α : Type u} (p : α → α → Prop) (x y : α) : Prop :=
  x = y ∨ p x y

theorem before_trans {α : Type u} {p : α → α → Prop}
    (pTrans : ∀ {x y z}, p x y → p y z → p x z)
    {x y z : α} (hxy : Before p x y) (hyz : Before p y z) :
    Before p x z := by
  rcases hxy with rfl | hxy
  · exact hyz
  rcases hyz with rfl | hyz
  · exact Or.inr hxy
  · exact Or.inr (pTrans hxy hyz)

theorem before_strict {α : Type u} {p : α → α → Prop}
    {x y : α} (h : Before p x y) (hne : x ≠ y) : p x y := by
  exact h.resolve_left hne

/-- The complete strict precedence relation, augmented by the requested
reversals.  It is deliberately not transitively closed by definition. -/
def Augmented {Event : Type u} {Pivot : Type v}
    (p : Event → Event → Prop) (repair vote : Pivot → Event)
    (selected : Pivot → Prop) (x y : Event) : Prop :=
  p x y ∨ ∃ i, selected i ∧ x = vote i ∧ y = repair i

/-- Induced repair graph: both endpoints belong to the reusable set. -/
def RepairGraph {Event : Type u} {Pivot : Type v}
    (p : Event → Event → Prop) (repair vote : Pivot → Event)
    (selected : Pivot → Prop) (i j : Pivot) : Prop :=
  selected i ∧ selected j ∧ p (repair i) (vote j)

theorem path_extend {α : Type u} {r : α → α → Prop}
    {x y z : α} (hxy : x = y ∨ TransGen r x y) (hyz : r y z) :
    TransGen r x z := by
  rcases hxy with rfl | hxy
  · exact .single hyz
  · exact .tail hxy hyz

/-- Every augmented path consists either solely of old precedence, or of an
old prefix, a sequence of reversal edges linked by repair-graph edges, and an
old suffix.  This is a proved normal form, not a premise of the main theorem. -/
theorem augmented_path_normal_form
    {Event : Type u} {Pivot : Type v}
    (p : Event → Event → Prop) (repair vote : Pivot → Event)
    (selected : Pivot → Prop)
    (pTrans : ∀ {x y z}, p x y → p y z → p x z)
    (disjoint : ∀ i j, repair i ≠ vote j)
    {x y : Event}
    (h : TransGen (Augmented p repair vote selected) x y) :
    p x y ∨ ∃ i j, selected i ∧ selected j ∧
      Before p x (vote i) ∧
      (i = j ∨ TransGen (RepairGraph p repair vote selected) i j) ∧
      Before p (repair j) y := by
  induction h with
  | single h =>
    rcases h with h | ⟨i, hi, rfl, rfl⟩
    · exact Or.inl h
    · exact Or.inr ⟨i, i, hi, hi, Or.inl rfl, Or.inl rfl, Or.inl rfl⟩
  | @tail y z h hyz ih =>
    rcases hyz with hyz | ⟨k, hk, hyk, rfl⟩
    · rcases ih with hxy | ⟨i, j, hi, hj, hleft, hmid, hright⟩
      · exact Or.inl (pTrans hxy hyz)
      · exact Or.inr ⟨i, j, hi, hj, hleft, hmid,
          before_trans (p := p) pTrans hright (Or.inr hyz)⟩
    · rcases ih with hxy | ⟨i, j, hi, hj, hleft, hmid, hright⟩
      · subst y
        exact Or.inr ⟨k, k, hk, hk, Or.inr hxy, Or.inl rfl, Or.inl rfl⟩
      · have hjk : p (repair j) (vote k) := by
          apply before_strict (p := p) (hne := disjoint j k)
          simpa [hyk] using hright
        exact Or.inr ⟨i, k, hi, hk, hleft,
          Or.inr (path_extend hmid ⟨hj, hk, hjk⟩), Or.inl rfl⟩

/-- A repair-graph edge is realized by old precedence followed by the
requested reversal at its target. -/
theorem graph_path_lifts
    {Event : Type u} {Pivot : Type v}
    (p : Event → Event → Prop) (repair vote : Pivot → Event)
    (selected : Pivot → Prop) {i j : Pivot}
    (h : TransGen (RepairGraph p repair vote selected) i j) :
    TransGen (Augmented p repair vote selected) (repair i) (repair j) := by
  have edgeLift : ∀ {i j}, RepairGraph p repair vote selected i j →
      TransGen (Augmented p repair vote selected) (repair i) (repair j) := by
    intro i j hij
    exact .tail (.single (Or.inl hij.2.2))
      (Or.inr ⟨j, hij.2.1, rfl, rfl⟩)
  induction h with
  | single h => exact edgeLift h
  | tail _ h ih => exact ih.trans (edgeLift h)

/-- Exact reversal criterion.  No finiteness, enumeration bound, capacity
assumption, or BFT-behavior assumption occurs in this graph theorem.  Finiteness
is needed only to turn acyclicity into a finite schedule, proved separately. -/
theorem repair_graph_reversal_iff
    {Event : Type u} {Pivot : Type v}
    (p : Event → Event → Prop) (repair vote : Pivot → Event)
    (selected : Pivot → Prop)
    (pTrans : ∀ {x y z}, p x y → p y z → p x z)
    (pIrrefl : ∀ x, ¬ p x x)
    (disjoint : ∀ i j, repair i ≠ vote j) :
    Acyclic (Augmented p repair vote selected) ↔
      Acyclic (RepairGraph p repair vote selected) := by
  constructor
  · intro hAug i hCycle
    exact hAug (repair i) (graph_path_lifts p repair vote selected hCycle)
  · intro hGraph x hCycle
    rcases augmented_path_normal_form p repair vote selected pTrans disjoint hCycle with
      hOld | ⟨i, j, hi, hj, hleft, hmid, hright⟩
    · exact pIrrefl x hOld
    · have hji : p (repair j) (vote i) :=
        before_strict (before_trans (p := p) pTrans hright hleft) (disjoint j i)
      exact hGraph i (path_extend hmid ⟨hj, hi, hji⟩)

/-- Strict cardinality monotonicity, including a witnessed additional element.
The list may contain duplicates; only coverage will be needed below. -/
theorem countP_strict_of_witness {α : Type u}
    (events : List α) (p q : α → Bool)
    (hmono : ∀ x ∈ events, p x = true → q x = true)
    (hwitness : ∃ x ∈ events, p x = false ∧ q x = true) :
    events.countP p < events.countP q := by
  induction events with
  | nil => simp at hwitness
  | cons a events ih =>
    have htail : ∀ x ∈ events, p x = true → q x = true := by
      intro x hx
      exact hmono x (by simp [hx])
    have hle := List.countP_mono_left htail
    rcases hwitness with ⟨x, hx, hpx, hqx⟩
    rcases List.mem_cons.mp hx with rfl | hx
    · simp only [List.countP_cons, hpx, hqx, Bool.false_eq_true,
        ↓reduceIte, Nat.add_zero, Nat.add_one]
      omega
    · have hlt := ih htail ⟨x, hx, hpx, hqx⟩
      have hhead := hmono a (by simp)
      cases hpa : p a <;> cases hqa : q a <;>
        simp_all <;> omega

/-- A numerical rank can be made injective by placing each rank in a block
and using an enumeration index to break ties. -/
theorem rank_block_strict {n a b i j : Nat}
    (hab : a < b) (hi : i ≤ n) :
    a * (n + 1) + i < b * (n + 1) + j := by
  have hstep := Nat.mul_le_mul_right (n + 1) (Nat.succ_le_of_lt hab)
  simp only [Nat.succ_mul] at hstep
  omega

/-- A finite schedule assigns distinct natural-number times and respects
every edge of the relation.  Idle time gaps are immaterial: increasing time
therefore induces a full linear extension of all enumerated opportunities. -/
def HasSchedule {Event : Type u} (r : Event → Event → Prop) : Prop :=
  ∃ time : Event → Nat,
    (∀ x y, time x = time y → x = y) ∧
    (∀ x y, r x y → time x < time y)

theorem schedule_path_increasing {Event : Type u}
    {r : Event → Event → Prop} (time : Event → Nat)
    (respects : ∀ x y, r x y → time x < time y)
    {x y : Event} (h : TransGen r x y) : time x < time y := by
  induction h with
  | single h => exact respects _ _ h
  | tail _ h ih => exact Nat.lt_trans ih (respects _ _ h)

/-- The finite topological-order theorem, proved directly in Std.  The
construction counts strict ancestors in a complete finite enumeration and
breaks ties by the first enumeration index.  Acyclicity is derived into strict
rank growth; existence of a linear extension is not assumed. -/
theorem finite_acyclic_iff_schedule {Event : Type u}
    (events : List Event) (covers : ∀ x, x ∈ events)
    (r : Event → Event → Prop) : Acyclic r ↔ HasSchedule r := by
  classical
  constructor
  · intro hAcyclic
    let pred : Event → Event → Bool := fun y x => decide (TransGen r x y)
    let rank : Event → Nat := fun x => events.countP (pred x)
    have rank_strict : ∀ x y, r x y → rank x < rank y := by
      intro x y hxy
      apply countP_strict_of_witness
      · intro z _ hzx
        have hpath : TransGen r z x := of_decide_eq_true hzx
        exact decide_eq_true (TransGen.tail hpath hxy)
      · refine ⟨x, covers x, ?_, ?_⟩
        · exact decide_eq_false (hAcyclic x)
        · exact decide_eq_true (TransGen.single hxy)
    let time : Event → Nat := fun x =>
      rank x * (events.length + 1) + events.idxOf x
    have block_strict : ∀ x y, rank x < rank y → time x < time y := by
      intro x y hxy
      exact rank_block_strict hxy (List.idxOf_le_length (a := x))
    refine ⟨time, ?_, ?_⟩
    · intro x y htime
      have hrank : rank x = rank y := by
        by_cases hlt : rank x < rank y
        · have := block_strict x y hlt
          omega
        by_cases hgt : rank y < rank x
        · have := block_strict y x hgt
          omega
        omega
      have hindex : events.idxOf x = events.idxOf y := by
        dsimp [time] at htime
        rw [hrank] at htime
        omega
      have hx : events[events.idxOf x]'(List.idxOf_lt_length_of_mem (covers x)) = x :=
        List.getElem_idxOf (List.idxOf_lt_length_of_mem (covers x))
      have hy : events[events.idxOf y]'(List.idxOf_lt_length_of_mem (covers y)) = y :=
        List.getElem_idxOf (List.idxOf_lt_length_of_mem (covers y))
      have hx' : events[events.idxOf y]'(List.idxOf_lt_length_of_mem (covers y)) = x := by
        simpa only [hindex] using hx
      exact hx'.symm.trans hy
    · intro x y hxy
      exact block_strict x y (rank_strict x y hxy)
  · rintro ⟨time, _, respects⟩ x hcycle
    have := schedule_path_increasing time respects hcycle
    omega

/-- Full finite bridge: an acyclic induced repair graph is equivalent to an
actual injective schedule of every original event which preserves all original
precedences and places every selected second vote before its own repair.
The event enumeration covers suppressed opportunities too. -/
theorem repair_graph_iff_realizable_schedule
    {Event : Type u} {Pivot : Type v}
    (events : List Event) (covers : ∀ x, x ∈ events)
    (p : Event → Event → Prop) (repair vote : Pivot → Event)
    (selected : Pivot → Prop)
    (pTrans : ∀ {x y z}, p x y → p y z → p x z)
    (pIrrefl : ∀ x, ¬ p x x)
    (disjoint : ∀ i j, repair i ≠ vote j) :
    Acyclic (RepairGraph p repair vote selected) ↔
      ∃ time : Event → Nat,
        (∀ x y, time x = time y → x = y) ∧
        (∀ x y, p x y → time x < time y) ∧
        (∀ i, selected i → time (vote i) < time (repair i)) := by
  rw [← repair_graph_reversal_iff p repair vote selected pTrans pIrrefl disjoint,
    finite_acyclic_iff_schedule events covers]
  constructor
  · rintro ⟨time, hinj, horder⟩
    exact ⟨time, hinj, (fun x y h => horder x y (Or.inl h)),
      (fun i hi => horder _ _ (Or.inr ⟨i, hi, rfl, rfl⟩))⟩
  · rintro ⟨time, hinj, horder, hreverse⟩
    refine ⟨time, hinj, ?_⟩
    intro x y h
    rcases h with h | ⟨i, hi, rfl, rfl⟩
    · exact horder x y h
    · exact hreverse i hi

/-- Representation-safe version for an arbitrary acyclic list of immediate
precedence edges: the graph uses their transitive closure, whereas the returned
schedule is required to respect just those original edges.  Intermediate event
opportunities remain in the domain even if their message is suppressed. -/
theorem repair_graph_from_covers_iff_schedule
    {Event : Type u} {Pivot : Type v}
    (events : List Event) (covers : ∀ x, x ∈ events)
    (edges : Event → Event → Prop) (repair vote : Pivot → Event)
    (selected : Pivot → Prop)
    (edgesAcyclic : Acyclic edges)
    (disjoint : ∀ i j, repair i ≠ vote j) :
    Acyclic (RepairGraph (TransGen edges) repair vote selected) ↔
      ∃ time : Event → Nat,
        (∀ x y, time x = time y → x = y) ∧
        (∀ x y, edges x y → time x < time y) ∧
        (∀ i, selected i → time (vote i) < time (repair i)) := by
  rw [repair_graph_iff_realizable_schedule events covers (TransGen edges)
    repair vote selected (fun hxy hyz => hxy.trans hyz) edgesAcyclic disjoint]
  constructor
  · rintro ⟨time, hinj, horder, hreverse⟩
    exact ⟨time, hinj, (fun x y h => horder x y (.single h)), hreverse⟩
  · rintro ⟨time, hinj, horder, hreverse⟩
    exact ⟨time, hinj,
      (fun _ _ h => schedule_path_increasing time horder h), hreverse⟩

end SchedulerClosure.GraphRealization
