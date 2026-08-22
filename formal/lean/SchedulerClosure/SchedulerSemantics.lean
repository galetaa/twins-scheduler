import Std

namespace SchedulerClosure

/-- A controlled protocol envelope.  `view` may be a protocol view or the
height/round pair encoded by the instantiation. -/
structure ControlledEnvelope (Node View Label Payload : Type) where
  sender : Node
  receiver : Node
  view : View
  label : Label
  payload : Payload

/-- One type-uniform directed admission relation. -/
abbrev DirectedAdmission (Node View : Type) := View → Node → Node → Prop

/-- A phase/type-sensitive admission relation. -/
abbrev TypedAdmission (Node View Label : Type) :=
  View → Label → Node → Node → Prop

/-- Type erasure existentially closes all labels on one directed endpoint
edge.  It does not mention payloads and therefore cannot create an envelope. -/
def typeClosure
    {Node View Label : Type}
    (A : TypedAdmission Node View Label) : DirectedAdmission Node View :=
  fun view sender receiver => ∃ label, A view label sender receiver

def admittedTyped
    {Node View Label Payload : Type}
    (A : TypedAdmission Node View Label)
    (e : ControlledEnvelope Node View Label Payload) : Prop :=
  A e.view e.label e.sender e.receiver

def admittedDirected
    {Node View Label Payload : Type}
    (A : DirectedAdmission Node View)
    (e : ControlledEnvelope Node View Label Payload) : Prop :=
  A e.view e.sender e.receiver

/-- Delivery is a stable filter of the already emitted envelope list.  Thus
order is inherited from emission order, every occurrence is delivered at most
once, and no non-emitted envelope is synthesized. -/
def deliver
    {Envelope : Type}
    (admitted : Envelope → Prop)
    [DecidablePred admitted]
    (emitted : List Envelope) : List Envelope :=
  emitted.filter admitted

theorem delivered_was_emitted
    {Envelope : Type}
    (admitted : Envelope → Prop)
    [DecidablePred admitted]
    (emitted : List Envelope)
    (e : Envelope)
    (h : e ∈ deliver admitted emitted) :
    e ∈ emitted := by
  induction emitted with
  | nil => simp [deliver] at h
  | cons head tail ih =>
      by_cases hadmit : admitted head
      · simp [deliver, hadmit] at h ⊢
        exact h.elim (fun heq => Or.inl heq) (fun htail => Or.inr (ih htail))
      · simp [deliver, hadmit] at h ⊢
        exact Or.inr (ih h)

theorem delivered_preserves_order
    {Envelope : Type}
    (admitted : Envelope → Prop)
    [DecidablePred admitted]
    (emitted : List Envelope) :
    deliver admitted emitted <+ emitted := by
  induction emitted with
  | nil => simp [deliver]
  | cons head tail ih =>
      by_cases hadmit : admitted head
      · change head :: deliver admitted tail <+ head :: tail
        exact List.Sublist.cons_cons head ih
      · change deliver admitted tail <+ head :: tail
        exact List.sublist_cons_of_sublist head ih

/-- A shared-edge pair records the exact coupling used by type erasure: the
sender, receiver, and view coincide, while labels are distinct. -/
structure SharedEdgePair
    (Node View Label Payload : Type) where
  enabling : ControlledEnvelope Node View Label Payload
  repair : ControlledEnvelope Node View Label Payload
  sameSender : enabling.sender = repair.sender
  sameReceiver : enabling.receiver = repair.receiver
  sameView : enabling.view = repair.view
  differentLabel : enabling.label ≠ repair.label

/-- If the typed policy admits the enabling label, its type closure admits the
shared directed edge. -/
theorem enabling_implies_closed_edge
    {Node View Label Payload : Type}
    (A : TypedAdmission Node View Label)
    (pair : SharedEdgePair Node View Label Payload)
    (h : admittedTyped A pair.enabling) :
    admittedDirected (typeClosure A) pair.enabling := by
  exact ⟨pair.enabling.label, h⟩

end SchedulerClosure
