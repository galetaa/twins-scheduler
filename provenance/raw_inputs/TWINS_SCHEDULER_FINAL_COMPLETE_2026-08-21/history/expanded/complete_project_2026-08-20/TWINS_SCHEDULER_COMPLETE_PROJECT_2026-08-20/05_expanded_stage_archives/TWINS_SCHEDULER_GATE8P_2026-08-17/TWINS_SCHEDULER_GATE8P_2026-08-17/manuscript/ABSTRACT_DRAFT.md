# Abstract draft

Fault-injection frameworks for Byzantine fault-tolerant protocols expose
different amounts of control over message delivery: some choose a partition or
directed communication graph for an entire view, while others distinguish
message phases, individual instances, or replay.  A richer scheduler trivially
generates more executions, but it is unclear when that additional authority
changes the set of *safety-relevant observations* rather than merely producing
redundant traces.

We study closure from phase-specific delivery to one type-uniform directed
endpoint graph for finite certificate-driven locking schemas.  First, we give a
relational sufficient condition under which closure-added messages preserve an
unsafe observation.  We then identify its locking boundary: repair evidence
added by type erasure can disable the unique honest participant shared by two
conflicting quorums.  For every `f≥1`, with `n=3f+1` and `q=2f+1`, we construct an
explicit schema in which phase-specific delivery forms both conflicting
certificates, whereas both directed-edge choices remain safe.  We derive an
exact seven-premise characterization of this construction and separately prove
that exact replay is observationally erasable under stable-key idempotence.

The results are independently re-encoded as Z3 CHC/SMT obligations, cross-checked
with exact Go big-integer arithmetic, and reproduced in two bounded locking
kernels plus a fuller two-round Go event loop and an independent Python mirror.
The work establishes an explicit safety-observation boundary; it does not claim
universal incompleteness of graph-based schedulers, a production-client
vulnerability, or a liveness result.
