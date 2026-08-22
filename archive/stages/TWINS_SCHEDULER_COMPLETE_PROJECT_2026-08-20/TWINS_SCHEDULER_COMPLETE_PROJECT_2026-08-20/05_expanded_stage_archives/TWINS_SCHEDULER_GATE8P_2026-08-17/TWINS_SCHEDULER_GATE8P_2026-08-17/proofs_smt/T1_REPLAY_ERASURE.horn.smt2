; T1: unbounded finite-trace replay erasure under stable-key idempotence.
; Relevant configuration is abstracted as Int.  Fresh stable keys apply the
; same deterministic transition table to the replay and erased executions.
; A duplicate stable key stutters on both sides.  Every finite derivation is a
; finite trace, so Reach must preserve equality of relevant configurations.
(set-logic HORN)
(define-sort Seen () (Array Int Bool))
(define-sort Trans () (Array Int (Array Int Int)))
(declare-rel Reach (Trans Int Int Seen))
(declare-rel Bad ())
(declare-var trans Trans)
(declare-var replay_cfg Int)
(declare-var erased_cfg Int)
(declare-var key Int)
(declare-var seen Seen)

; Equal initial relevant configurations.
(rule (Reach trans replay_cfg replay_cfg ((as const Seen) false)))

; A non-first delivery is a stutter under the theorem premises.
(rule (=> (and (Reach trans replay_cfg erased_cfg seen)
               (select seen key))
          (Reach trans replay_cfg erased_cfg seen)))

; A first delivery is retained on both sides and runs the same deterministic
; relevant transition.
(rule (=> (and (Reach trans replay_cfg erased_cfg seen)
               (not (select seen key)))
          (Reach trans
                 (select (select trans replay_cfg) key)
                 (select (select trans erased_cfg) key)
                 (store seen key true))))

(rule (=> (and (Reach trans replay_cfg erased_cfg seen)
               (not (= replay_cfg erased_cfg)))
          Bad))
(query Bad :print-certificate true)
