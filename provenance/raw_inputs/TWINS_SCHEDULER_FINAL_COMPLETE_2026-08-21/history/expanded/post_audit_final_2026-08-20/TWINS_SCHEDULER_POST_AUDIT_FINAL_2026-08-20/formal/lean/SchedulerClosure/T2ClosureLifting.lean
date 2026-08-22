namespace SchedulerClosure

variable {State Original Inserted : Type}

inductive Merged (Original Inserted : Type)
  | original : Original → Merged Original Inserted
  | inserted : Inserted → Merged Original Inserted

def projectOriginal : List (Merged Original Inserted) → List Original
  | [] => []
  | Merged.original action :: rest => action :: projectOriginal rest
  | Merged.inserted _ :: rest => projectOriginal rest

def runOriginal (step : State → Original → State) : State → List Original → State
  | state, [] => state
  | state, action :: rest => runOriginal step (step state action) rest

def runMerged
    (step : State → Original → State)
    (add : State → Inserted → State) :
    State → List (Merged Original Inserted) → State
  | state, [] => state
  | state, Merged.original action :: rest => runMerged step add (step state action) rest
  | state, Merged.inserted action :: rest => runMerged step add (add state action) rest

theorem closure_lifting_aux
    (R : State → State → Prop)
    (step : State → Original → State)
    (add : State → Inserted → State)
    (trans : ∀ a b c, R a b → R b c → R a c)
    (increasing : ∀ state action, R state (add state action))
    (forward : ∀ action a b, R a b → R (step a action) (step b action)) :
    ∀ trace a b,
      R a b →
      R (runOriginal step a (projectOriginal trace))
        (runMerged step add b trace) := by
  intro trace
  induction trace with
  | nil =>
      intro a b hab
      simpa [projectOriginal, runOriginal, runMerged] using hab
  | cons head tail ih =>
      intro a b hab
      cases head with
      | original action =>
          have hstep := forward action a b hab
          simpa [projectOriginal, runOriginal, runMerged] using
            ih (step a action) (step b action) hstep
      | inserted action =>
          have hprefix := trans a b (add b action) hab (increasing b action)
          simpa [projectOriginal, runOriginal, runMerged] using
            ih a (add b action) hprefix

theorem closure_preserves_unsafe
    (R : State → State → Prop)
    (Unsafe : State → Prop)
    (step : State → Original → State)
    (add : State → Inserted → State)
    (initial : ∀ state, R state state)
    (trans : ∀ a b c, R a b → R b c → R a c)
    (increasing : ∀ state action, R state (add state action))
    (forward : ∀ action a b, R a b → R (step a action) (step b action))
    (upward : ∀ a b, R a b → Unsafe a → Unsafe b)
    (state : State)
    (trace : List (Merged Original Inserted))
    (unsafeOriginal : Unsafe (runOriginal step state (projectOriginal trace))) :
    Unsafe (runMerged step add state trace) := by
  apply upward _ _
  · exact closure_lifting_aux R step add trans increasing forward
      trace state state (initial state)
  · exact unsafeOriginal

end SchedulerClosure
