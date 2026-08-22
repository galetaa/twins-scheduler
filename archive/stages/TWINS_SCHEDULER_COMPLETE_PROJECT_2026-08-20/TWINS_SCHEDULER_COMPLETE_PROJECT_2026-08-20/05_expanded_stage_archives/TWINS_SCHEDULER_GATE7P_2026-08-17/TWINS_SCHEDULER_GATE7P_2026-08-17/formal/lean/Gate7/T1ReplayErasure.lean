namespace Gate7

variable {State Event : Type}

def run (step : State → Event → State) : State → List Event → State
  | state, [] => state
  | state, event :: rest => run step (step state event) rest

/-- A trace whose duplicate positions have already been marked by a stable-key pass. -/
def eraseMarked (duplicate : Event → Bool) : List Event → List Event
  | [] => []
  | event :: rest =>
      if duplicate event then eraseMarked duplicate rest
      else event :: eraseMarked duplicate rest

/-- If every marked duplicate is a protocol-relevant stutter, deleting all such
    positions preserves the final protocol-relevant state for every finite trace. -/
theorem run_eraseMarked
    (step : State → Event → State)
    (duplicate : Event → Bool)
    (hDuplicate : ∀ state event, duplicate event = true → step state event = state) :
    ∀ state trace,
      run step state (eraseMarked duplicate trace) = run step state trace := by
  intro state trace
  induction trace generalizing state with
  | nil => rfl
  | cons event rest ih =>
      by_cases h : duplicate event = true
      · simp [eraseMarked, h, run, hDuplicate state event h, ih]
      · have hf : duplicate event = false := by
          cases value : duplicate event <;> simp_all
        simp [eraseMarked, hf, run, ih]

end Gate7
