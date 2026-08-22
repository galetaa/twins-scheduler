(set-logic QF_UF)
; Damaged U omits the repair/timing term, so the claimed closed form no longer follows.
(declare-const S1 Bool)
(declare-const S2 Bool)
(declare-const Rq Bool)
(declare-const D Bool)
(declare-const T Bool)
(declare-const Ed Bool)
(declare-const X Bool)
(define-fun Ubad ((e Bool) (r Bool)) Bool
  (and (or (not S1) e)
       (or (not S2) (or (not Rq) e))))
(define-fun StrictBad () Bool
  (and X Ed (Ubad true false) (not (Ubad false false)) (not (Ubad true true))))
(define-fun Closed () Bool (and S2 D T Ed X (or S1 Rq)))
(assert (xor StrictBad Closed))
(check-sat)
(get-model)
