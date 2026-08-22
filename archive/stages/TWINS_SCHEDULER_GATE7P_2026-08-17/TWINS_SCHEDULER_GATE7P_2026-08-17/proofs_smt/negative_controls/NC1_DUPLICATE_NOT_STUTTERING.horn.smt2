; Expected: sat.
; Removing stable-key stuttering permits replay and erased executions to diverge.
(set-logic HORN)
(declare-rel Reach (Int Int))
(declare-rel Bad ())
(declare-var replay Int)
(declare-var erased Int)
(rule (Reach 0 0))
(rule (=> (Reach replay erased) (Reach (+ replay 1) erased)))
(rule (=> (and (Reach replay erased) (not (= replay erased))) Bad))
(query Bad)
