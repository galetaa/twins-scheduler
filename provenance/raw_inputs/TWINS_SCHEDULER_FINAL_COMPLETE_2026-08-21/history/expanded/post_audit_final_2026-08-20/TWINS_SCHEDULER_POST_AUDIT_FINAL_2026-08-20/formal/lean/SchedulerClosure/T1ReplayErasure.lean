namespace SchedulerClosure

structure RelevantState (Key Payload : Type) where
  processedKeys : List Key
  protocol : Payload

variable {State Event Rel : Type}

def run (step : State → Event → State) : State → List Event → State
  | state, [] => state
  | state, event :: rest => run step (step state event) rest

def eraseMarked (duplicate : Event → Bool) : List Event → List Event
  | [] => []
  | event :: rest =>
      if duplicate event then eraseMarked duplicate rest
      else event :: eraseMarked duplicate rest

def ProjectionCongruent
    (π : State → Rel) (step : State → Event → State) : Prop :=
  ∀ s t event, π s = π t → π (step s event) = π (step t event)

def MarkedDuplicateStutters
    (π : State → Rel) (step : State → Event → State)
    (duplicate : Event → Bool) : Prop :=
  ∀ state event, duplicate event = true → π (step state event) = π state

def MarkedDuplicateSilent
    {Output : Type}
    (emit : State → Event → List Output)
    (duplicate : Event → Bool) : Prop :=
  ∀ state event, duplicate event = true → emit state event = []

theorem run_eraseMarked_aux
    (π : State → Rel)
    (step : State → Event → State)
    (duplicate : Event → Bool)
    (hCongruent : ProjectionCongruent π step)
    (hStutter : MarkedDuplicateStutters π step duplicate) :
    ∀ trace left right,
      π left = π right →
      π (run step left (eraseMarked duplicate trace)) =
        π (run step right trace) := by
  intro trace
  induction trace with
  | nil =>
      intro left right hrel
      simpa [eraseMarked, run] using hrel
  | cons event rest ih =>
      intro left right hrel
      by_cases hdup : duplicate event = true
      · have hright : π (step right event) = π right :=
          hStutter right event hdup
        have hnext : π left = π (step right event) :=
          hrel.trans hright.symm
        simpa [eraseMarked, hdup, run] using
          ih left (step right event) hnext
      · have hkeep : duplicate event = false := by
          cases h : duplicate event <;> simp_all
        have hnext : π (step left event) = π (step right event) :=
          hCongruent left right event hrel
        simpa [eraseMarked, hkeep, run] using
          ih (step left event) (step right event) hnext

theorem replay_erasure
    (π : State → Rel)
    (step : State → Event → State)
    (duplicate : Event → Bool)
    (hCongruent : ProjectionCongruent π step)
    (hStutter : MarkedDuplicateStutters π step duplicate) :
    ∀ state trace,
      π (run step state (eraseMarked duplicate trace)) =
        π (run step state trace) := by
  intro state trace
  exact run_eraseMarked_aux π step duplicate hCongruent hStutter
    trace state state rfl

structure HiddenCounterState where
  relevant : Bool
  hidden : Bool
  deriving DecidableEq, Repr

inductive HiddenCounterEvent
  | X
  | Y
  deriving DecidableEq, Repr

def hiddenCounterStep : HiddenCounterState → HiddenCounterEvent → HiddenCounterState
  | state, .X => { state with hidden := !state.hidden }
  | state, .Y => { state with relevant := state.hidden }

def hiddenProjection (state : HiddenCounterState) : Bool := state.relevant

def hiddenInitial : HiddenCounterState :=
  { relevant := false, hidden := true }

theorem hidden_state_counterexample :
    hiddenProjection (run hiddenCounterStep hiddenInitial [.X, .X, .Y]) = true ∧
    hiddenProjection (run hiddenCounterStep hiddenInitial [.X, .Y]) = false := by
  decide

theorem hidden_state_not_congruent :
    ¬ ProjectionCongruent hiddenProjection hiddenCounterStep := by
  intro h
  let s : HiddenCounterState := { relevant := false, hidden := false }
  let t : HiddenCounterState := { relevant := false, hidden := true }
  have hrel : hiddenProjection s = hiddenProjection t := rfl
  have hbad := h s t .Y hrel
  decide at hbad

end SchedulerClosure
