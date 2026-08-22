; Expected: sat.
; If a closure-added action is not R-increasing, an unsafe original state can
; be mapped to a safe closed state.  Here R is integer <= and Unsafe(x) is x>=1.
(set-logic QF_LIA)
(declare-const original Int)
(declare-const closed Int)
(assert (= original 1))
(assert (= closed 0))
(assert (>= original 1))
(assert (not (>= closed 1)))
(assert (not (<= original closed)))
(check-sat)
(get-model)
