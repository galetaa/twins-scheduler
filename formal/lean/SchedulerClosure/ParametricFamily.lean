import Std.Tactic.Omega
import SchedulerClosure.QuorumPivotCriterion

namespace SchedulerClosure

def nValidators (f : Nat) : Nat := 3 * f + 1
def quorum (f : Nat) : Nat := 2 * f + 1
def branchBase (f : Nat) : Nat := 2 * f

/-- Concrete `3f+1` family as a corollary of the structural criterion. -/
theorem parametric_family_separation (f : Nat) (hf : 1 ≤ f) :
    nValidators f = 3 * f + 1 ∧
    criterionUnsafe (branchBase f) (branchBase f) (quorum f) .phaseSpecific ∧
    (∀ edge : Bool,
      ¬ criterionUnsafe (branchBase f) (branchBase f) (quorum f)
        (.directed edge)) := by
  constructor
  · rfl
  · apply criterion_policy_separation
    · simp [branchBase, quorum]
    · simp [branchBase, quorum]

end SchedulerClosure
