namespace SchedulerClosure

structure Premises where
  S1 : Bool
  S2 : Bool
  Rq : Bool
  D : Bool
  T : Bool
  Ed : Bool
  X : Bool
  deriving DecidableEq, Repr

/-- U(e,r) = (not S1 or e) and
    [not S2 or ((not Rq or e) and not (r and D and T))]. -/
def unsafeOutcome (p : Premises) (e r : Bool) : Bool :=
  ((!p.S1) || e) &&
  ((!p.S2) || (((!p.Rq) || e) && (!(r && p.D && p.T))))

def strictSeparation (p : Premises) : Bool :=
  p.X && p.Ed && unsafeOutcome p true false &&
  !(unsafeOutcome p false false) && !(unsafeOutcome p true true)

def characterization (p : Premises) : Bool :=
  p.S2 && p.D && p.T && p.Ed && p.X && (p.S1 || p.Rq)

theorem strictSeparation_eq_characterization (p : Premises) :
    strictSeparation p = characterization p := by
  rcases p with ⟨S1, S2, Rq, D, T, Ed, X⟩
  cases S1 <;> cases S2 <;> cases Rq <;> cases D <;>
    cases T <;> cases Ed <;> cases X <;> decide

def p0111111 : Premises :=
  { S1 := false, S2 := true, Rq := true, D := true, T := true, Ed := true, X := true }
def p1101111 : Premises :=
  { S1 := true, S2 := true, Rq := false, D := true, T := true, Ed := true, X := true }
def p1111111 : Premises :=
  { S1 := true, S2 := true, Rq := true, D := true, T := true, Ed := true, X := true }

theorem strictSeparation_iff_three (p : Premises) :
    strictSeparation p = true ↔
      p = p0111111 ∨ p = p1101111 ∨ p = p1111111 := by
  rcases p with ⟨S1, S2, Rq, D, T, Ed, X⟩
  cases S1 <;> cases S2 <;> cases Rq <;> cases D <;>
    cases T <;> cases Ed <;> cases X <;> decide

end SchedulerClosure
