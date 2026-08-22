import Std

namespace SchedulerClosure

variable {State Event Rel Output : Type}

def eraseMarked (duplicate : Event → Bool) : List Event → List Event
  | [] => []
  | event :: rest =>
      if duplicate event then eraseMarked duplicate rest
      else event :: eraseMarked duplicate rest

structure RunResult (State Output : Type) where
  state : State
  output : List Output

def runWithOutput
    (step : State → Event → State)
    (emit : State → Event → List Output) :
    State → List Event → RunResult State Output
  | state, [] => ⟨state, []⟩
  | state, event :: rest =>
      let tail := runWithOutput step emit (step state event) rest
      ⟨tail.state, emit state event ++ tail.output⟩

def ProjectionCongruent
    (π : State → Rel) (step : State → Event → State) : Prop :=
  ∀ s t event, π s = π t → π (step s event) = π (step t event)

/-- Future output noninterference: equal relevant projections produce equal
protocol-relevant output on every retained event. -/
def OutputCongruent
    (π : State → Rel) (emit : State → Event → List Output) : Prop :=
  ∀ s t event, π s = π t → emit s event = emit t event

def MarkedDuplicateStutters
    (π : State → Rel) (step : State → Event → State)
    (duplicate : Event → Bool) : Prop :=
  ∀ state event, duplicate event = true → π (step state event) = π state

def MarkedDuplicateSilent
    (emit : State → Event → List Output)
    (duplicate : Event → Bool) : Prop :=
  ∀ state event, duplicate event = true → emit state event = []

theorem eraseMarked_preserves_projection_and_output_aux
    (π : State → Rel)
    (step : State → Event → State)
    (emit : State → Event → List Output)
    (duplicate : Event → Bool)
    (hStep : ProjectionCongruent π step)
    (hOutput : OutputCongruent π emit)
    (hStutter : MarkedDuplicateStutters π step duplicate)
    (hSilent : MarkedDuplicateSilent emit duplicate) :
    ∀ trace left right,
      π left = π right →
      let erased := runWithOutput step emit left (eraseMarked duplicate trace)
      let original := runWithOutput step emit right trace
      π erased.state = π original.state ∧ erased.output = original.output := by
  intro trace
  induction trace with
  | nil =>
      intro left right hrel
      simpa [eraseMarked, runWithOutput] using And.intro hrel rfl
  | cons event rest ih =>
      intro left right hrel
      by_cases hdup : duplicate event = true
      · have hright : π (step right event) = π right :=
          hStutter right event hdup
        have hnext : π left = π (step right event) :=
          hrel.trans hright.symm
        have htail := ih left (step right event) hnext
        have hempty : emit right event = [] := hSilent right event hdup
        simpa [eraseMarked, hdup, runWithOutput, hempty] using htail
      · have hkeep : duplicate event = false := by
          cases h : duplicate event <;> simp_all
        have hstate : π (step left event) = π (step right event) :=
          hStep left right event hrel
        have hout : emit left event = emit right event :=
          hOutput left right event hrel
        have htail := ih (step left event) (step right event) hstate
        simpa [eraseMarked, hkeep, runWithOutput, hout] using
          And.intro htail.1 (congrArg (fun xs => emit right event ++ xs) htail.2)

theorem replay_erasure_with_outputs
    (π : State → Rel)
    (step : State → Event → State)
    (emit : State → Event → List Output)
    (duplicate : Event → Bool)
    (hStep : ProjectionCongruent π step)
    (hOutput : OutputCongruent π emit)
    (hStutter : MarkedDuplicateStutters π step duplicate)
    (hSilent : MarkedDuplicateSilent emit duplicate)
    (state : State)
    (trace : List Event) :
    let erased := runWithOutput step emit state (eraseMarked duplicate trace)
    let original := runWithOutput step emit state trace
    π erased.state = π original.state ∧ erased.output = original.output := by
  exact eraseMarked_preserves_projection_and_output_aux
    π step emit duplicate hStep hOutput hStutter hSilent trace state state rfl

/-- State-only observations factor through the final relevant projection. -/
theorem replay_erasure_state_observation
    {Observation : Type}
    (π : State → Rel)
    (observe : Rel → Observation)
    (step : State → Event → State)
    (emit : State → Event → List Output)
    (duplicate : Event → Bool)
    (hStep : ProjectionCongruent π step)
    (hOutput : OutputCongruent π emit)
    (hStutter : MarkedDuplicateStutters π step duplicate)
    (hSilent : MarkedDuplicateSilent emit duplicate)
    (state : State)
    (trace : List Event) :
    observe (π (runWithOutput step emit state (eraseMarked duplicate trace)).state) =
      observe (π (runWithOutput step emit state trace).state) := by
  exact congrArg observe
    (replay_erasure_with_outputs π step emit duplicate hStep hOutput
      hStutter hSilent state trace).1

structure HiddenCounterState where
  relevant : Bool
  hidden : Bool
  deriving DecidableEq, Repr

inductive HiddenCounterEvent | X | Y deriving DecidableEq, Repr

def hiddenCounterStep : HiddenCounterState → HiddenCounterEvent → HiddenCounterState
  | state, .X => { state with hidden := !state.hidden }
  | state, .Y => { state with relevant := state.hidden }

def hiddenCounterEmit : HiddenCounterState → HiddenCounterEvent → List Bool
  | state, .X => []
  | state, .Y => [state.hidden]

def hiddenProjection (state : HiddenCounterState) : Bool := state.relevant

def hiddenInitial : HiddenCounterState :=
  { relevant := false, hidden := true }

theorem hidden_state_counterexample :
    hiddenProjection
      (runWithOutput hiddenCounterStep hiddenCounterEmit hiddenInitial
        [.X, .X, .Y]).state = true ∧
    hiddenProjection
      (runWithOutput hiddenCounterStep hiddenCounterEmit hiddenInitial
        [.X, .Y]).state = false := by
  decide

theorem hidden_state_breaks_output_congruence :
    ¬ OutputCongruent hiddenProjection hiddenCounterEmit := by
  intro h
  let s : HiddenCounterState := { relevant := false, hidden := false }
  let t : HiddenCounterState := { relevant := false, hidden := true }
  have hrel : hiddenProjection s = hiddenProjection t := rfl
  have hbad := h s t .Y hrel
  decide at hbad

end SchedulerClosure
