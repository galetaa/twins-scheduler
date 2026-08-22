(set-logic QF_NIA)
(declare-const f Int)
(assert (>= f 1))
(define-fun q () Int (+ (* 2 f) 1))
(define-fun base () Int (* 2 f))
; Phase-specific: E delivered, R withheld.
(define-fun gt_c0 () Bool (>= (+ base 1) q))
(define-fun gt_c1 () Bool (>= (+ base 1) q))
(define-fun gt_unsafe () Bool (and gt_c0 gt_c1))
; Directed domain is exactly Bool: false=off, true=on.
(declare-const edge Bool)
(define-fun gd_c0 () Bool (and edge (>= (+ base 1) q)))
; If edge is on, repair is processed before C1 and disables pivot; if off, E is absent.
(define-fun gd_c1 () Bool (and edge false (>= (+ base 1) q)))
(define-fun gd_unsafe () Bool (and gd_c0 gd_c1))
(assert (not (and gt_unsafe (not gd_unsafe) (= base (- q 1)))))
(check-sat)
