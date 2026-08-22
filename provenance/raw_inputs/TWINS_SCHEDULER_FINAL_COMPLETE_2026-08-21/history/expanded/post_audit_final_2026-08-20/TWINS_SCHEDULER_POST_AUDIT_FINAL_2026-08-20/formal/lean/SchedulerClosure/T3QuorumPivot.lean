import Std.Tactic.Omega

namespace SchedulerClosure

inductive Value | zero | one deriving DecidableEq, Repr
inductive MessagePhase | enabling | repair deriving DecidableEq, Repr

structure Envelope where
  sender : Nat
  receiver : Nat
  view : Nat
  phase : MessagePhase
  deriving DecidableEq, Repr

def enablingEnvelope : Envelope :=
  { sender := 0, receiver := 1, view := 0, phase := .enabling }
def repairEnvelope : Envelope :=
  { sender := 0, receiver := 1, view := 0, phase := .repair }

theorem enabling_repair_same_endpoint_and_view :
    enablingEnvelope.sender = repairEnvelope.sender ∧
    enablingEnvelope.receiver = repairEnvelope.receiver ∧
    enablingEnvelope.view = repairEnvelope.view := by decide

inductive Phase | deliverE | certificate0 | deliverR | certificate1
  deriving DecidableEq, Repr

def phaseIndex : Phase → Nat
  | .deliverE => 0 | .certificate0 => 1 | .deliverR => 2 | .certificate1 => 3

theorem explicit_phase_order :
    phaseIndex .deliverE < phaseIndex .certificate0 ∧
    phaseIndex .certificate0 < phaseIndex .deliverR ∧
    phaseIndex .deliverR < phaseIndex .certificate1 := by decide

inductive Policy | phaseSpecific | directed (edge : Bool)
  deriving DecidableEq, Repr

theorem directed_domain_exhaustive (edge : Bool) :
    edge = false ∨ edge = true := by cases edge <;> simp

structure OperationalState where
  pivotEnabled : Bool := false
  pivotDisabled : Bool := false
  certificate0 : Bool := false
  certificate1 : Bool := false
  leftDecision : Option Value := none
  rightDecision : Option Value := none
  deriving DecidableEq, Repr

def delivered : Policy → MessagePhase → Bool
  | .phaseSpecific, .enabling => true
  | .phaseSpecific, .repair => false
  | .directed edge, _ => edge

def transition (policy : Policy) (state : OperationalState) : Phase → OperationalState
  | .deliverE => if delivered policy .enabling then { state with pivotEnabled := true } else state
  | .certificate0 => if state.pivotEnabled then
      { state with certificate0 := true, leftDecision := some .zero } else state
  | .deliverR => if delivered policy .repair then { state with pivotDisabled := true } else state
  | .certificate1 => if state.pivotEnabled && !state.pivotDisabled then
      { state with certificate1 := true, rightDecision := some .one } else state

def execute (policy : Policy) : OperationalState :=
  let s0 : OperationalState := {}
  let s1 := transition policy s0 .deliverE
  let s2 := transition policy s1 .certificate0
  let s3 := transition policy s2 .deliverR
  transition policy s3 .certificate1

def AgreementViolation (state : OperationalState) : Prop :=
  state.leftDecision = some .zero ∧ state.rightDecision = some .one

theorem phase_specific_agreement_violation :
    AgreementViolation (execute .phaseSpecific) := by decide

theorem directed_edge_off_safe :
    ¬ AgreementViolation (execute (.directed false)) := by decide

theorem directed_edge_on_safe :
    ¬ AgreementViolation (execute (.directed true)) := by decide

theorem directed_unsafe_observations_empty (edge : Bool) :
    ¬ AgreementViolation (execute (.directed edge)) := by
  cases edge
  · exact directed_edge_off_safe
  · exact directed_edge_on_safe

theorem phase_specific_strictly_separates :
    AgreementViolation (execute .phaseSpecific) ∧
    (∀ edge : Bool, ¬ AgreementViolation (execute (.directed edge))) := by
  exact ⟨phase_specific_agreement_violation, directed_unsafe_observations_empty⟩

def quorum (f : Nat) : Nat := 2 * f + 1
def baseSupport (f : Nat) : Nat := 2 * f

theorem pivot_completes_quorum (f : Nat) : baseSupport f + 1 = quorum f := by
  simp [baseSupport, quorum]

theorem without_pivot_short (f : Nat) :
    baseSupport f < quorum f ∧ quorum f - baseSupport f = 1 := by omega

theorem parametric_quorum_pivot_separation (f : Nat) (hf : 1 ≤ f) :
    baseSupport f + 1 = quorum f ∧
    baseSupport f < quorum f ∧
    AgreementViolation (execute .phaseSpecific) ∧
    (∀ edge : Bool, ¬ AgreementViolation (execute (.directed edge))) := by
  exact ⟨pivot_completes_quorum f, (without_pivot_short f).1,
    phase_specific_agreement_violation, directed_unsafe_observations_empty⟩

end SchedulerClosure
