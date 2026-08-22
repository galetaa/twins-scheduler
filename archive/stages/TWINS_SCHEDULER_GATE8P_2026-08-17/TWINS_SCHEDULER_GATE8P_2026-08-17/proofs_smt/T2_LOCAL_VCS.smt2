; T2 local proof obligations over an arbitrary state sort.
; Each push/pop block proves one use of a declared theorem premise by showing
; that its negation is unsatisfiable.
(set-option :produce-proofs true)
(set-logic AUFLIA)
(declare-sort S 0)
(declare-sort A 0)
(declare-fun R (S S) Bool)
(declare-fun add (S A) S)
(declare-fun step (S A) S)
(declare-fun Unsafe (S) Bool)
(declare-const x S)
(declare-const y S)
(declare-const z S)
(declare-const a A)

; VC1: transitivity supports an inserted action.
(push)
(assert (forall ((u S) (v S) (w S))
  (=> (and (R u v) (R v w)) (R u w))))
(assert (R x y))
(assert (R y z))
(assert (not (R x z)))
(check-sat)
(get-proof)
(pop)

; VC2: closure-added actions are R-increasing.
(push)
(assert (forall ((u S) (ev A)) (R u (add u ev))))
(assert (not (R x (add x a))))
(check-sat)
(get-proof)
(pop)

; VC3: original actions forward-simulate R.
(push)
(assert (forall ((u S) (v S) (ev A))
  (=> (R u v) (R (step u ev) (step v ev)))))
(assert (R x y))
(assert (not (R (step x a) (step y a))))
(check-sat)
(get-proof)
(pop)

; VC4: Unsafe is upward closed under R.
(push)
(assert (forall ((u S) (v S))
  (=> (and (R u v) (Unsafe u)) (Unsafe v))))
(assert (R x y))
(assert (Unsafe x))
(assert (not (Unsafe y)))
(check-sat)
(get-proof)
(pop)
