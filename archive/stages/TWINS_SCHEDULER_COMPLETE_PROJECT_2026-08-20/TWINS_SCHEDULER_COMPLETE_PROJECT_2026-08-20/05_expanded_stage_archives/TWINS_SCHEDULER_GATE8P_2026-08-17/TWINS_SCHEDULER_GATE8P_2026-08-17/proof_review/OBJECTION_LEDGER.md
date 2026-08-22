# Proof-objection ledger

| ID | Potential objection | Resolution at Gate 7′ | Residual limitation | Blocking? |
|---|---|---|---|---|
| O1 | T1 may silently equate replay with equivocation. | Stable replay key, stuttering duplicate transition, and no protocol-relevant output are explicit premises. A damaged non-stuttering model is `SAT`. | Different signed contents, timers, callbacks, counters, and resource effects are outside T1. | No |
| O2 | T2 may assume the desired preservation result through `R`. | Increasing insertions, forward simulation, transitivity, and upward closure are separate local VCs; the prefix invariant is a separate CHC query. | Each protocol instance must still exhibit a meaningful preorder `R`; repair messages can fail this obligation. | No for the conditional theorem |
| O3 | T3 may be only a sample over small `f`. | QF_LIA proves the symbolic arithmetic for every integer `f≥1`; Go `math/big` independently checks 1,028 values, including a 400-digit value. | Executable traces remain bounded to a small two-round fixture. | No |
| O4 | T3 may claim universal scheduler incompleteness. | The statement is frozen as an existential separation family for an explicit schema. | Transfer to another protocol requires a schema-instantiation argument. | No |
| O5 | T6 may be inferred from only one-at-a-time ablations. | Z3 proves symbolic equivalence and the executable checker evaluates all 128 assignments. | The characterization is exact only for the seven-flag model. | No |
| O6 | The unsafe result may be caused by queue order. | FIFO, LIFO, and 256 seeded orders preserve all six classifications and terminal signatures. | This is bounded event-order sensitivity, not an unbounded asynchronous result. | No |
| O7 | Go and Python may share the same code. | The implementations are independent and communicate only through serialized terminal observations. | Both follow the same written specification and can share a specification error. | No |
| O8 | The work may be a new testing DSL rather than a scientific result. | The theorem, closure boundary, and separation construction precede the implementation in the manuscript skeleton; richer filters are explicitly treated as prior art. | Reviewer framing must remain disciplined during Gate 8′. | No |
