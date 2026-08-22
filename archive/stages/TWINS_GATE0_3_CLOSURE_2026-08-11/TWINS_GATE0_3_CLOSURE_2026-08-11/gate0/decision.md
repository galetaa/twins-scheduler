# Gate 0 decision

## Verdict

**CLOSED — NO-GO for the proposed finite-clone cutoff/width contribution.**

## Reason

The broad Byzantine-to-equivocation part is already established by VLSM under validator assumptions. The repaired finite-`k` part is subsumed by a direct generic construction:

- persistent total clone count equals a minimum cover of incompatible deterministic local histories under exact observation;
- a reusable active-slot count collapses to one in an asynchronous safety model with replay and delayed delivery.

This exactly matches the Gate 0 no-go criterion: a direct generic theorem subsumes the residual claim.

## Surviving pivot

Only the following question survives conceptually:

> Does a concrete partition-per-view Twins scenario language refine the ideal per-message equivocation model, and what is the smallest safety-relevant trace outside that concrete language?

That is a new candidate, not an automatic continuation of the rejected one.
