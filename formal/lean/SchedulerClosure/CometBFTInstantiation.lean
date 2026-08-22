import Std.Tactic
import SchedulerClosure.QuorumPivotCriterion

namespace SchedulerClosure

inductive LockVariant | baseline | missingLockUpdate
  deriving DecidableEq, Repr, BEq

inductive TendermintPolicy
  | phaseSpecific
  | directed (edge : Bool)
  deriving DecidableEq, Repr

structure TendermintBoundedState where
  height : Nat := 1
  sawPolka0 : Bool := false
  locked0 : Bool := false
  decided0AtPivot : Bool := false
  pivotPrecommit0 : Bool := false
  pivotPrecommit1 : Bool := false
  certificate0 : Bool := false
  certificate1 : Bool := false
  leftDecision0 : Bool := false
  rightDecision1 : Bool := false
  deriving DecidableEq, Repr

def EAdmitted : TendermintPolicy → Bool
  | .phaseSpecific => true
  | .directed edge => edge

def RAdmitted : TendermintPolicy → Bool
  | .phaseSpecific => false
  | .directed edge => edge

/-- Rule-level bounded execution in the fixed order `E < C0 < R < C1`.
`E` is the last PREVOTE completing a PoLC at the pivot.  `R` is the last
PRECOMMIT on the same sender/receiver/height/round edge completing a local
commit and advancing the pivot's height. -/
def executeTendermintBounded
    (f : Nat) (variant : LockVariant) (policy : TendermintPolicy) :
    TendermintBoundedState :=
  let q := 2 * f + 1
  let base := 2 * f
  let e := EAdmitted policy
  let r := RAdmitted policy
  let saw := e
  let pre0 := e
  let locked := e && match variant with
    | .baseline => true
    | .missingLockUpdate => false
  let cert0 := decide (base + (if pre0 then 1 else 0) ≥ q)
  let pivotCommitted := e && r
  let height := if pivotCommitted then 2 else 1
  let available1 := (height == 1) && !pivotCommitted && !locked
  let pre1 := available1
  let cert1 := decide (base + (if pre1 then 1 else 0) ≥ q)
  {
    height := height
    sawPolka0 := saw
    locked0 := locked
    decided0AtPivot := pivotCommitted
    pivotPrecommit0 := pre0
    pivotPrecommit1 := pre1
    certificate0 := cert0
    certificate1 := cert1
    leftDecision0 := cert0
    rightDecision1 := cert1
  }

def tendermintAgreementViolation (s : TendermintBoundedState) : Prop :=
  s.leftDecision0 = true ∧ s.rightDecision1 = true

theorem bounded_baseline_safe
    (f : Nat) (_hf : 1 ≤ f) (policy : TendermintPolicy) :
    ¬ tendermintAgreementViolation
      (executeTendermintBounded f .baseline policy) := by
  cases policy with
  | phaseSpecific =>
      simp [executeTendermintBounded, EAdmitted, RAdmitted,
        tendermintAgreementViolation]
  | directed edge =>
      cases edge <;>
        simp [executeTendermintBounded, EAdmitted, RAdmitted,
          tendermintAgreementViolation] <;> omega

theorem bounded_missing_lock_phase_specific_unsafe
    (f : Nat) (_hf : 1 ≤ f) :
    tendermintAgreementViolation
      (executeTendermintBounded f .missingLockUpdate .phaseSpecific) := by
  simp [executeTendermintBounded, EAdmitted, RAdmitted,
    tendermintAgreementViolation]

theorem bounded_missing_lock_directed_safe
    (f : Nat) (_hf : 1 ≤ f) (edge : Bool) :
    ¬ tendermintAgreementViolation
      (executeTendermintBounded f .missingLockUpdate (.directed edge)) := by
  cases edge <;>
    simp [executeTendermintBounded, EAdmitted, RAdmitted,
      tendermintAgreementViolation] <;> omega

/-- The bounded Tendermint-style mutation instantiates the abstract structural
criterion. -/
theorem bounded_tendermint_refines_quorum_pivot
    (f : Nat) (hf : 1 ≤ f) :
    tendermintAgreementViolation
      (executeTendermintBounded f .missingLockUpdate .phaseSpecific) ∧
    (∀ edge : Bool,
      ¬ tendermintAgreementViolation
        (executeTendermintBounded f .missingLockUpdate (.directed edge))) := by
  exact ⟨bounded_missing_lock_phase_specific_unsafe f hf,
    bounded_missing_lock_directed_safe f hf⟩

end SchedulerClosure
