import Std.Tactic

/-!
# Arithmetic and output component of the repair-frontier result

This module kernel-checks the quota arithmetic once an operational model has
established its maximum number `capacity` of jointly reusable pivots.  The
finite-poset/linear-extension correspondence, the graph interpretation of
`capacity`, and production-client conformance are separate proof obligations;
they are deliberately not encoded as if the arithmetic discharged them.

The primary semantics is initial-ready: a pivot whose enabling edge is closed
may still sign the second value.  An open edge permits its first signature and
admits its repair; a pivot contributes twice only if repair follows its second
signature.  Signatures already emitted cannot be withdrawn by a later repair.
-/

namespace SchedulerClosure.RepairFrontier

/-- A fixed base and one optional identity meet a certificate threshold. -/
def formsCertificate (base threshold : Nat) (signed : Bool) : Prop :=
  threshold ≤ base + (if signed then 1 else 0)

/-- Corrected single-pivot theorem over arbitrary execution and voting
functions.  Persistence is an explicit hypothesis.  The second vote when the
edge is closed is intentionally unconstrained.  `observationContract` makes the
exhaustive two-certificate observation assumption visible instead of baking
unsafety into a particular Boolean table.
-/
theorem behavioral_quorum_pivot_separation
    {State : Type}
    (run : Bool → Bool → State) (isUnsafe : State → Prop)
    (firstVote secondVote : Bool → Bool → Bool)
    (base0 base1 threshold : Nat)
    (firstNeedsPivot : base0 + 1 = threshold)
    (secondNeedsPivot : base1 + 1 = threshold)
    (firstExact : ∀ enabling repair, firstVote enabling repair = enabling)
    (persistence : secondVote true false = true)
    (timelyRepair : secondVote true true = false)
    (observationContract : ∀ enabling repair,
      isUnsafe (run enabling repair) ↔
        formsCertificate base0 threshold (firstVote enabling repair) ∧
        formsCertificate base1 threshold (secondVote enabling repair)) :
    isUnsafe (run true false) ∧
      (∀ edge : Bool, ¬ isUnsafe (run edge edge)) := by
  constructor
  · apply (observationContract true false).2
    rw [firstExact true false, persistence]
    unfold formsCertificate
    simp only [↓reduceIte]
    omega
  · intro edge hUnsafe
    have hCertificates := (observationContract edge edge).1 hUnsafe
    cases edge with
    | false =>
      have hFirst := hCertificates.1
      rw [firstExact false false] at hFirst
      simp [formsCertificate] at hFirst
      omega
    | true =>
      have hSecond := hCertificates.2
      rw [timelyRepair] at hSecond
      simp [formsCertificate] at hSecond
      omega

/-- A logical negative control for the previously unstated persistence
premise.  First-vote necessity and timely repair both hold for these functions,
but an independent disabling action (represented by the constant-false second
output) removes the fine witness as well. -/
theorem persistence_hypothesis_independent :
    let first : Bool → Bool → Bool := fun enabling _ => enabling
    let second : Bool → Bool → Bool := fun _ _ => false
    (∀ enabling repair, first enabling repair = enabling) ∧
      second true true = false ∧
      ¬ (formsCertificate 0 1 (first true false) ∧
         formsCertificate 0 1 (second true false)) := by
  simp [formsCertificate]

/-- Fine phase control can reuse all `pivots` contributors.  `need0` and `need1`
are nonnegative quorum deficits after fixed base contributions are removed. -/
def phaseUnsafe (pivots need0 need1 : Nat) : Prop :=
  need0 ≤ pivots ∧ need1 ≤ pivots

/-- Count abstraction of a coarse witness.  `opened` pivots contribute first;
`reused` of them also sign second.  The other `pivots - opened` remain initially
ready and contribute only second.  Operational realizability of any reusable
subset of size at most `capacity` is established outside this arithmetic lemma.
-/
def directedUnsafe (pivots need0 need1 capacity : Nat) : Prop :=
  ∃ opened reused : Nat,
    opened ≤ pivots ∧ reused ≤ opened ∧ reused ≤ capacity ∧
    need0 ≤ opened ∧ need1 ≤ pivots - opened + reused

/-- Exact quota boundary for initial-ready, unit-weight pivots. -/
theorem directed_unsafe_iff
    (pivots need0 need1 capacity : Nat) (_capacityBound : capacity ≤ pivots) :
    directedUnsafe pivots need0 need1 capacity ↔
      need0 ≤ pivots ∧ need1 ≤ pivots ∧ need0 + need1 ≤ pivots + capacity := by
  constructor
  · rintro ⟨opened, reused, hOpened, hReuseOpened, hReuseCapacity, hNeed0, hNeed1⟩
    omega
  · rintro ⟨hNeed0, hNeed1, hCombined⟩
    by_cases hSmall : need0 ≤ capacity
    · exact ⟨need0, need0, by omega⟩
    · exact ⟨need0, capacity, by omega⟩

def strictSeparation (pivots need0 need1 capacity : Nat) : Prop :=
  phaseUnsafe pivots need0 need1 ∧
    ¬ directedUnsafe pivots need0 need1 capacity

/-- Strict separation means the two demands exceed the ordinary capacity plus
the jointly reusable capacity, while phase-specific execution remains feasible.
-/
theorem strict_separation_iff
    (pivots need0 need1 capacity : Nat) (capacityBound : capacity ≤ pivots) :
    strictSeparation pivots need0 need1 capacity ↔
      need0 ≤ pivots ∧ need1 ≤ pivots ∧ pivots + capacity < need0 + need1 := by
  unfold strictSeparation phaseUnsafe
  rw [directed_unsafe_iff pivots need0 need1 capacity capacityBound]
  omega

/-- Making `splits` additional edges phase-specific can raise the reusable
capacity by at most `splits`, capped by the number of pivots.  The matching
construction that attains this bound is a separate finite-set argument. -/
def splitCapacity (pivots capacity splits : Nat) : Nat :=
  min pivots (capacity + splits)

theorem split_capacity_bound (pivots capacity splits : Nat) :
    splitCapacity pivots capacity splits ≤ pivots := by
  exact Nat.min_le_left pivots (capacity + splits)

/-- The exact number of additional independent phase-split edges under the
capacity assumption.  The theorem includes the existence and minimality test:
an integer budget succeeds exactly when it is at least the displayed deficit.
-/
theorem minimum_phase_splits
    (pivots need0 need1 capacity splits : Nat)
    (capacityBound : capacity ≤ pivots)
    (fineFeasible : phaseUnsafe pivots need0 need1) :
    directedUnsafe pivots need0 need1 (splitCapacity pivots capacity splits) ↔
      need0 + need1 - (pivots + capacity) ≤ splits := by
  rw [directed_unsafe_iff pivots need0 need1
    (splitCapacity pivots capacity splits)
    (split_capacity_bound pivots capacity splits)]
  rcases fineFeasible with ⟨hNeed0, hNeed1⟩
  unfold splitCapacity
  by_cases hSaturated : pivots ≤ capacity + splits
  · rw [Nat.min_eq_left hSaturated]
    omega
  · rw [Nat.min_eq_right (by omega)]
    omega

/-- Common-deadline weighted abstraction.  All late-repair pivots are opened,
with total weight `lateWeight`.  `attainable selectedWeight` records that a
subset of the forced-early pivots has exactly the selected weight.  Those opened
forced pivots contribute first; their complement contributes second. -/
def weightedDirectedUnsafe
    (totalWeight lateWeight need0 need1 : Nat)
    (attainable : Nat → Prop) : Prop :=
  ∃ selectedWeight : Nat, attainable selectedWeight ∧
    need0 ≤ lateWeight + selectedWeight ∧
    need1 ≤ totalWeight - selectedWeight

/-- Exact weighted subset interval.  Keeping the `attainable` predicate is
essential: substituting a real interval or a unit-weight inequality is unsound.
-/
theorem weighted_admission_interval
    (totalWeight lateWeight need0 need1 : Nat)
    (attainable : Nat → Prop)
    (weightBound : ∀ selectedWeight, attainable selectedWeight →
      selectedWeight ≤ totalWeight) :
    weightedDirectedUnsafe totalWeight lateWeight need0 need1 attainable ↔
      ∃ selectedWeight : Nat, attainable selectedWeight ∧
        need0 - lateWeight ≤ selectedWeight ∧
        selectedWeight + need1 ≤ totalWeight := by
  constructor
  · rintro ⟨selectedWeight, hAttainable, hFirst, hSecond⟩
    have hBound := weightBound selectedWeight hAttainable
    exact ⟨selectedWeight, hAttainable, by omega⟩
  · rintro ⟨selectedWeight, hAttainable, hLower, hUpper⟩
    exact ⟨selectedWeight, hAttainable, by omega⟩

/-- Two indivisible weight-2 pivots cannot split a first demand 1 and a second
demand 3 when neither can be reused, even though the total demands sum to 4. -/
theorem weighted_granularity_counterexample :
    phaseUnsafe 4 1 3 ∧ 1 + 3 ≤ 4 + 0 ∧
    ¬ weightedDirectedUnsafe 4 0 1 3
      (fun selectedWeight => selectedWeight = 0 ∨
        selectedWeight = 2 ∨ selectedWeight = 4) := by
  constructor
  · unfold phaseUnsafe
    decide
  constructor
  · decide
  · rintro ⟨selectedWeight, hAttainable, hFirst, hSecond⟩
    omega

/-- A minimal signed-output machine used only to validate the distinction
between the second signature and later certificate collection. -/
structure OutputState where
  enabled : Bool := false
  repaired : Bool := false
  signed0 : Bool := false
  signed1 : Bool := false
  decided0 : Bool := false
  decided1 : Bool := false
  deriving DecidableEq, Repr

inductive OutputEvent
  | enabling | firstVote | firstCertificate | repair | secondVote | secondCertificate
  deriving DecidableEq, Repr

def outputStep (s : OutputState) : OutputEvent → OutputState
  | .enabling => { s with enabled := true }
  | .firstVote => { s with signed0 := s.signed0 || s.enabled }
  | .firstCertificate => { s with decided0 := s.decided0 || s.signed0 }
  | .repair => { s with repaired := true }
  | .secondVote => { s with signed1 := s.signed1 || !s.repaired }
  | .secondCertificate => { s with decided1 := s.decided1 || s.signed1 }

def outputRun (events : List OutputEvent) : OutputState :=
  events.foldl outputStep {}

/-- Repair cannot remove the second signed output from the state recording
emitted messages, even if it prevents any new signature. -/
theorem repair_preserves_signed_output (s : OutputState) :
    (outputStep s .repair).signed1 = s.signed1 := by
  rfl

theorem late_repair_before_certificate_is_unsafe :
    (outputRun [.enabling, .firstVote, .firstCertificate,
      .secondVote, .repair, .secondCertificate]).decided0 = true ∧
    (outputRun [.enabling, .firstVote, .firstCertificate,
      .secondVote, .repair, .secondCertificate]).decided1 = true := by
  decide

theorem repair_before_second_vote_is_safe :
    (outputRun [.enabling, .firstVote, .firstCertificate,
      .repair, .secondVote, .secondCertificate]).decided1 = false := by
  decide

/-- Closing the enabling edge preserves initial readiness for the second
value.  The first certificate alone is missing in this coarse execution. -/
theorem closed_edge_still_permits_second_vote :
    (outputRun [.firstVote, .firstCertificate,
      .secondVote, .secondCertificate]).decided0 = false ∧
    (outputRun [.firstVote, .firstCertificate,
      .secondVote, .secondCertificate]).decided1 = true := by
  decide

end SchedulerClosure.RepairFrontier
