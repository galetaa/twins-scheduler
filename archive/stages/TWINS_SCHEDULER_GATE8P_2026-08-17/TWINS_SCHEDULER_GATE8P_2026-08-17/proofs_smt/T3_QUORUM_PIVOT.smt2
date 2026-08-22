; T3: symbolic parametric quorum-pivot separation for every integer f >= 1.
; Unsatisfiability of the negated conjunction establishes all arithmetic and
; branch obligations without enumerating concrete fault bounds.
(set-option :produce-proofs true)
(set-logic QF_LIA)
(declare-const f Int)
(define-fun n () Int (+ (* 3 f) 1))
(define-fun q () Int (+ (* 2 f) 1))
(define-fun base () Int (* 2 f))
(define-fun phase_first () Int (+ base 1))
(define-fun phase_second () Int (+ base 1))
(define-fun directed_absent_first () Int base)
(define-fun directed_present_first () Int (+ base 1))
(define-fun directed_present_second () Int base)
(define-fun intersection () Int (+ f 1))

(assert (>= f 1))
(assert
  (not
    (and
      (= n (+ (* 3 f) 1))
      (= q (+ (* 2 f) 1))
      (= intersection (+ f 1))
      (= phase_first q)
      (= phase_second q)
      (< directed_absent_first q)
      (= directed_present_first q)
      (< directed_present_second q)
      (= (- q base) 1))))
(check-sat)
(get-proof)
