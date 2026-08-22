import Std.Tactic

namespace SchedulerClosure

/-- Certificate formation from a base support and an optional pivot. -/
def certificate (base q : Nat) (pivot : Bool) : Prop :=
  base + (if pivot then 1 else 0) ≥ q

/-- In the bounded mechanism, `e` enables the pivot; repair `r` processed
before the second opportunity disables it. -/
def pivotAtSecond (e r : Bool) : Bool := e && !r

def twoConflictingCertificates
    (base0 base1 q : Nat) (e r : Bool) : Prop :=
  certificate base0 q e ∧ certificate base1 q (pivotAtSecond e r)

/-- Structural quorum-pivot separation criterion.  The scheduler side of the
premise is that a phase-specific policy realizes `(e,r)=(true,false)`, whereas
one type-uniform edge realizes only `(false,false)` or `(true,true)`. -/
theorem quorum_pivot_separation_criterion
    (base0 base1 q : Nat)
    (firstNeedsPivot : base0 + 1 = q)
    (secondNeedsPivot : base1 + 1 = q) :
    twoConflictingCertificates base0 base1 q true false ∧
    ¬ twoConflictingCertificates base0 base1 q false false ∧
    ¬ twoConflictingCertificates base0 base1 q true true := by
  unfold twoConflictingCertificates certificate pivotAtSecond
  simp
  omega

/-- Operational policy domain used by the criterion. -/
inductive CoupledPolicy
  | phaseSpecific
  | directed (edge : Bool)
  deriving DecidableEq, Repr

def enablingAdmission : CoupledPolicy → Bool
  | .phaseSpecific => true
  | .directed edge => edge

def repairAdmission : CoupledPolicy → Bool
  | .phaseSpecific => false
  | .directed edge => edge

def criterionUnsafe (base0 base1 q : Nat) (policy : CoupledPolicy) : Prop :=
  twoConflictingCertificates base0 base1 q
    (enablingAdmission policy) (repairAdmission policy)

theorem criterion_policy_separation
    (base0 base1 q : Nat)
    (firstNeedsPivot : base0 + 1 = q)
    (secondNeedsPivot : base1 + 1 = q) :
    criterionUnsafe base0 base1 q .phaseSpecific ∧
    (∀ edge : Bool, ¬ criterionUnsafe base0 base1 q (.directed edge)) := by
  have h := quorum_pivot_separation_criterion
    base0 base1 q firstNeedsPivot secondNeedsPivot
  constructor
  · simpa [criterionUnsafe, enablingAdmission, repairAdmission] using h.1
  · intro edge
    cases edge
    · simpa [criterionUnsafe, enablingAdmission, repairAdmission] using h.2.1
    · simpa [criterionUnsafe, enablingAdmission, repairAdmission] using h.2.2

end SchedulerClosure
