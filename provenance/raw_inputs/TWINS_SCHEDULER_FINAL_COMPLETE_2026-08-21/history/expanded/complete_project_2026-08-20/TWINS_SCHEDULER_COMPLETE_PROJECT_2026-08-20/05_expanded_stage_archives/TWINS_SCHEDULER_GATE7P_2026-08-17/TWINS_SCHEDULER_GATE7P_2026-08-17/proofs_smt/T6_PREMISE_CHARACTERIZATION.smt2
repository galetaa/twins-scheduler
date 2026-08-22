; T6: symbolic equivalence between the operational seven-flag construction
; and the closed Boolean characterization.  The model mirrors
; schedcheck.gate6.necessity.evaluate_separation exactly.
(set-option :produce-proofs true)
(set-logic QF_LIA)
(declare-const f Int)
(declare-const S1 Bool)
(declare-const S2 Bool)
(declare-const Rq Bool)
(declare-const D Bool)
(declare-const T Bool)
(declare-const Eshare Bool)
(declare-const X Bool)

(define-fun q () Int (+ (* 2 f) 1))
(define-fun first_base () Int (ite S1 (- q 1) q))
(define-fun second_base () Int (ite S2 (- q 1) q))

; Safety outcome for one delivery policy (deliverE, deliverR).
(define-fun unsafe ((deliverE Bool) (deliverR Bool)) Bool
  (let ((firstCert (>= (+ first_base (ite deliverE 1 0)) q)))
    (let ((pivotEnabled (or deliverE (not Rq))))
      (let ((repaired (and deliverR D T firstCert)))
        (let ((secondPivot (and pivotEnabled (not repaired))))
          (and firstCert
               (>= (+ second_base (ite secondPivot 1 0)) q)))))))

; If X holds, G_T can select E without R.  Otherwise it collapses to the two
; endpoint-uniform choices available on a shared edge.
(define-fun typedUnsafe () Bool
  (ite X
       (unsafe true false)
       (or (unsafe false false) (unsafe true true))))

; If E and R share one endpoint edge, G_D has only off/off and on/on.  If they
; use different endpoint edges, G_D can select all four combinations.
(define-fun directedUnsafe () Bool
  (ite Eshare
       (or (unsafe false false) (unsafe true true))
       (or (unsafe false false)
           (unsafe false true)
           (unsafe true false)
           (unsafe true true))))

(define-fun actualStrict () Bool
  (and typedUnsafe (not directedUnsafe)))
(define-fun predictedStrict () Bool
  (and S2 D T Eshare X (or S1 Rq)))

(assert (>= f 1))
(assert (not (= actualStrict predictedStrict)))
(check-sat)
(get-proof)
