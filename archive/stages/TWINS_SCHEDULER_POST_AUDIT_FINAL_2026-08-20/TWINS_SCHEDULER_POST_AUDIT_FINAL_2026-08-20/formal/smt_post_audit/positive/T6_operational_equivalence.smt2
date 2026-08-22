(set-logic QF_UF)
(declare-const S1 Bool)
(declare-const S2 Bool)
(declare-const Rq Bool)
(declare-const D Bool)
(declare-const T Bool)
(declare-const Ed Bool)
(declare-const X Bool)
(define-fun U ((e Bool) (r Bool)) Bool
  (and (or (not S1) e)
       (or (not S2)
           (and (or (not Rq) e)
                (not (and r D T))))))
(define-fun Strict () Bool
  (and X Ed (U true false) (not (U false false)) (not (U true true))))
(define-fun Closed () Bool
  (and S2 D T Ed X (or S1 Rq)))
(assert (xor Strict Closed))
(check-sat)
