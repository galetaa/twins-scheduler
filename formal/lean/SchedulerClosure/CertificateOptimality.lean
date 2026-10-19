import Std.Tactic

/-!
# Soundness of minimum-cost certificates

The executable refinement checker uses cost-to-go Bellman lower bounds, with
`none` denoting infinity. This module proves the underlying certificate rule
for arbitrary nonnegative-cost transition systems, including infeasibility.
It does not assume that a supplied table was computed by dynamic programming.
The Python parser, SCC enumeration and protocol/model correspondence are not
thereby mechanically verified; they must establish the hypotheses below.
-/

namespace SchedulerClosure.CertificateOptimality

/-- A finite execution with its actual accumulated cost. -/
inductive CostedPath {Node : Type u} (step : Node → Node → Nat → Prop) :
    Node → Node → Nat → Prop where
  | nil (x : Node) : CostedPath step x x 0
  | cons {x y z : Node} {c d : Nat} :
      step x y c → CostedPath step y z d → CostedPath step x z (c + d)

/-- `left ≤ cost + right` over naturals extended with infinity. -/
def EdgeBound (left right : Option Nat) (cost : Nat) : Prop :=
  match left, right with
  | none, none => True
  | none, some _ => False
  | some _, none => True
  | some a, some b => a ≤ cost + b

/-- A finite-cost execution must exceed a finite lower bound; an infinite
lower bound rules out every finite-cost execution. -/
def BoundsCost (bound : Option Nat) (cost : Nat) : Prop :=
  match bound with
  | none => False
  | some lower => lower ≤ cost

/-- Local certificate inequalities propagate a lower bound across one edge. -/
theorem edge_bound_compose {left right : Option Nat} {c d : Nat}
    (hedge : EdgeBound left right c) (htail : BoundsCost right d) :
    BoundsCost left (c + d) := by
  cases left with
  | none =>
    cases right with
    | none => exact htail
    | some b => exact hedge
  | some a =>
    cases right with
    | none => exact False.elim htail
    | some b =>
      change a ≤ c + b at hedge
      change b ≤ d at htail
      change a ≤ c + d
      omega

/-- A checked Bellman potential bounds every terminating path, independently
of the optimizer which produced the potential and independently of acyclicity. -/
theorem bellman_path_lower_bound
    {Node : Type u} (step : Node → Node → Nat → Prop)
    (goal : Node → Prop) (potential : Node → Option Nat)
    (edges : ∀ x y c, step x y c →
      EdgeBound (potential x) (potential y) c)
    (terminals : ∀ x, goal x → potential x = some 0)
    {start finish : Node} {cost : Nat}
    (path : CostedPath step start finish cost) (done : goal finish) :
    BoundsCost (potential start) cost := by
  induction path with
  | nil x =>
    rw [terminals x done]
    exact Nat.le_refl 0
  | @cons x y z c d hstep hpath ih =>
    exact edge_bound_compose (edges x y c hstep) (ih done)

/-- A replayed feasible witness meeting its certified lower bound is optimal
among all terminating executions of the declared transition system. -/
theorem certified_witness_is_minimum
    {Node : Type u} (step : Node → Node → Nat → Prop)
    (goal : Node → Prop) (potential : Node → Option Nat)
    (edges : ∀ x y c, step x y c →
      EdgeBound (potential x) (potential y) c)
    (terminals : ∀ x, goal x → potential x = some 0)
    {start witnessFinish : Node} {claimed : Nat}
    (root : potential start = some claimed)
    (witness : CostedPath step start witnessFinish claimed)
    (witnessDone : goal witnessFinish) :
    (∃ finish, CostedPath step start finish claimed ∧ goal finish) ∧
      ∀ finish cost, CostedPath step start finish cost → goal finish → claimed ≤ cost := by
  constructor
  · exact ⟨witnessFinish, witness, witnessDone⟩
  · intro finish cost path done
    have bound := bellman_path_lower_bound step goal potential edges terminals path done
    simpa only [root, BoundsCost] using bound

/-- Infinity at the start is a valid infeasibility certificate when every
local inequality and every terminal condition have been checked. -/
theorem certified_infeasibility
    {Node : Type u} (step : Node → Node → Nat → Prop)
    (goal : Node → Prop) (potential : Node → Option Nat)
    (edges : ∀ x y c, step x y c →
      EdgeBound (potential x) (potential y) c)
    (terminals : ∀ x, goal x → potential x = some 0)
    {start : Node} (root : potential start = none) :
    ¬ ∃ finish cost, CostedPath step start finish cost ∧ goal finish := by
  rintro ⟨finish, cost, path, done⟩
  have bound := bellman_path_lower_bound step goal potential edges terminals path done
  rw [root] at bound
  exact bound

end SchedulerClosure.CertificateOptimality
