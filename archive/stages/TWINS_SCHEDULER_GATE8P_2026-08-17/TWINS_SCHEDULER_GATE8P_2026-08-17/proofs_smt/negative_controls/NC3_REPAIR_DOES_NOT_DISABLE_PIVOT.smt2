; Expected: sat.
; If repair fails to disable the pivot, the directed edge-present branch can
; form both certificates, so the strict G_D/G_T separation disappears.
(set-logic QF_LIA)
(declare-const f Int)
(define-fun q () Int (+ (* 2 f) 1))
(define-fun base () Int (* 2 f))
(define-fun directed_present_first () Int (+ base 1))
(define-fun directed_present_second () Int (+ base 1))
(assert (>= f 1))
(assert (= directed_present_first q))
(assert (= directed_present_second q))
(check-sat)
(get-model)
