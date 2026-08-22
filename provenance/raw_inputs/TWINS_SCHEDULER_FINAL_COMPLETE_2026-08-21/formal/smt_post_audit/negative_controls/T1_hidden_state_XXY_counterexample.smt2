(set-logic ALL)
; State is represented by relevant bit r and hidden bit h.
; X toggles h. Y copies h into r.
(define-fun X_r ((r Bool) (h Bool)) Bool r)
(define-fun X_h ((r Bool) (h Bool)) Bool (not h))
(define-fun Y_r ((r Bool) (h Bool)) Bool h)
(define-fun Y_h ((r Bool) (h Bool)) Bool h)
; Initial state (r=false,h=true).
(define-fun r0 () Bool false)
(define-fun h0 () Bool true)
; Full X,X,Y.
(define-fun r1 () Bool (X_r r0 h0))
(define-fun h1 () Bool (X_h r0 h0))
(define-fun r2 () Bool (X_r r1 h1))
(define-fun h2 () Bool (X_h r1 h1))
(define-fun rFull () Bool (Y_r r2 h2))
; Erased X,Y.
(define-fun rErase () Bool (Y_r r1 h1))
; The second X is immediately projection-stuttering, but terminal projections differ.
(assert (= r2 r1))
(assert (not (= rFull rErase)))
(check-sat)
(get-value (rFull rErase r1 r2 h1 h2))
