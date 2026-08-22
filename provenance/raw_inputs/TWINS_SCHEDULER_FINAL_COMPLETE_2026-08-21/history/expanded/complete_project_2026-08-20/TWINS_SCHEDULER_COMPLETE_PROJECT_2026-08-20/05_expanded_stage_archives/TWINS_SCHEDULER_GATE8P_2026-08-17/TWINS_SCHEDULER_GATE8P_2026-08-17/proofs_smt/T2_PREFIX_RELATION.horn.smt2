; T2 induction skeleton: every finite merged prefix remains R-related when
; each inserted action discharges the R-increasing/transitivity VC and each
; retained original action discharges the forward-simulation VC.
(set-logic HORN)
(define-sort Rel () (Array Int (Array Int Bool)))
(declare-rel Prefix (Rel Int Int))
(declare-rel Bad ())
(declare-var r Rel)
(declare-var original Int)
(declare-var closed Int)
(declare-var original2 Int)
(declare-var closed2 Int)

; Reflexive initial relation is supplied as an explicit theorem premise.
(rule (=> (select (select r original) original)
          (Prefix r original original)))

; Inserted-action case.  The last conjunct is exactly the local consequence
; of R(original,closed), R(closed,closed2), and transitivity.
(rule (=> (and (Prefix r original closed)
               (select (select r closed) closed2)
               (select (select r original) closed2))
          (Prefix r original closed2)))

; Retained-original-action case.  The relation between successor states is
; the local forward-simulation proof obligation.
(rule (=> (and (Prefix r original closed)
               (select (select r original2) closed2))
          (Prefix r original2 closed2)))

(rule (=> (and (Prefix r original closed)
               (not (select (select r original) closed)))
          Bad))
(query Bad :print-certificate true)
