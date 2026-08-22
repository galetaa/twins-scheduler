import Std

namespace SchedulerClosure

variable {State Action Observation : Type}

def terminal
    (step : State → Action → State)
    (initial : State) : List Action → State
  | [] => initial
  | action :: rest => terminal step (step initial action) rest

/-- `Unsafe` is deliberately a predicate on terminal protocol states. -/
def UnsafeObservationSet
    (legal : List Action → Prop)
    (step : State → Action → State)
    (initial : State)
    (Unsafe : State → Prop)
    (observe : State → Observation) : Set Observation :=
  {ω | ∃ trace,
      legal trace ∧
      Unsafe (terminal step initial trace) ∧
      observe (terminal step initial trace) = ω}

theorem unsafe_observation_has_unsafe_terminal
    (legal : List Action → Prop)
    (step : State → Action → State)
    (initial : State)
    (Unsafe : State → Prop)
    (observe : State → Observation)
    (ω : Observation)
    (h : ω ∈ UnsafeObservationSet legal step initial Unsafe observe) :
    ∃ trace, legal trace ∧ Unsafe (terminal step initial trace) := by
  rcases h with ⟨trace, hlegal, hunsafe, _⟩
  exact ⟨trace, hlegal, hunsafe⟩

end SchedulerClosure
