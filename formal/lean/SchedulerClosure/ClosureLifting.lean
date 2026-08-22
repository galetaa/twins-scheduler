import Std

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
  | state, Merged.original action :: rest =>
      runMerged step add (step state action) rest
  | state, Merged.inserted action :: rest =>
      runMerged step add (add state action) rest

/-- Pure merged-trace simulation lemma. -/
theorem merged_trace_lifting
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

/-- A scheduler closure must map each legal source trace to a legal target
trace and preserve the retained source actions. -/
structure LegalSchedulerClosure
    (SourceTrace TargetTrace : Type) where
  close : SourceTrace → TargetTrace
  sourceLegal : SourceTrace → Prop
  targetLegal : TargetTrace → Prop
  legalTarget : ∀ trace, sourceLegal trace → targetLegal (close trace)

/-- Language-level corollary.  In addition to the relational premises, the
closure is required to produce an execution admitted by the target grammar. -/
theorem legal_scheduler_closure_preserves_unsafe
    (R : State → State → Prop)
    (Unsafe : State → Prop)
    (step : State → Original → State)
    (add : State → Inserted → State)
    (closure : LegalSchedulerClosure
      (List Original) (List (Merged Original Inserted)))
    (retains : ∀ trace, projectOriginal (closure.close trace) = trace)
    (initial : ∀ state, R state state)
    (trans : ∀ a b c, R a b → R b c → R a c)
    (increasing : ∀ state action, R state (add state action))
    (forward : ∀ action a b, R a b → R (step a action) (step b action))
    (upward : ∀ a b, R a b → Unsafe a → Unsafe b)
    (state : State)
    (trace : List Original)
    (hlegal : closure.sourceLegal trace)
    (hunsafe : Unsafe (runOriginal step state trace)) :
    closure.targetLegal (closure.close trace) ∧
    Unsafe (runMerged step add state (closure.close trace)) := by
  constructor
  · exact closure.legalTarget trace hlegal
  · apply upward _ _
    · have hlift := merged_trace_lifting R step add trans increasing forward
        (closure.close trace) state state (initial state)
      simpa [retains trace] using hlift
    · exact hunsafe

end SchedulerClosure
