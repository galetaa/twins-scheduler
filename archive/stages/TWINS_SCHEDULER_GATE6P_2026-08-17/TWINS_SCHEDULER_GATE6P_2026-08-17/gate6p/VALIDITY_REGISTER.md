# Gate 6′ validity register

## Internal validity

| Threat | Current control | Residual limitation |
|---|---|---|
| Proof sketch hides a circular assumption | The theorem name cannot be assumed; every rule dependency and induction measure is explicit; tampered certificates are rejected by tests | Rule semantics remain part of the small trusted base |
| Arithmetic overflow or sample-only generalization | Exact polynomial normalization plus independent Go `math/big` checks | Protocol execution remains bounded even though arithmetic is parametric |
| Unsafe result caused by unrelated implementation bug | Mutation changes only the lock assignment; baseline and closure branches are separately checked | The fixture is deliberately small and may omit interactions present in full clients |
| Safety oracle shares implementation with protocol | Safety is computed from terminal decisions; Go and independent Python implementations agree | Both implement the same written specification and may share a specification error |
| Queue order accidentally creates the boundary | FIFO, LIFO, and 256 random orders preserve classification | This is not arbitrary asynchronous timing or liveness exploration |
| Pinned-source assumptions changed | Gate 6′ re-runs the Gate 5′ source obligations and hashes | Source mapping covers selected transitions, not full client refinement |

## Construct validity

| Construct | Operational definition | Main risk |
|---|---|---|
| Safety | Two correct replicas have different non-null decisions | Excludes other safety properties and accountability evidence |
| Phase/type erasure | All controlled message phases on one directed endpoint edge share one admission decision | Real harnesses may have additional queues, retries, or uncontrolled message kinds |
| Repair evidence | Message that decides or restores a persistent constraint before the conflicting opportunity | Some protocols repair via local timers or indirect certificates rather than one message |
| Replay idempotence | Duplicate stable replay key is a protocol-relevant stutter and adds no contribution | Logs, resource counters, callbacks, or rate limits may make duplicate delivery observable |
| Quorum pivot | Unique honest identity required by both conflicting support sets | Flexible/weighted quorums may need a generalized intersection argument |

## External validity

The mechanism appears in two exact kernels and one fuller local event loop. The
quorum arithmetic is parametric in `f`, but the executable protocol traces use
`n=4`, `f=1`, two rounds, binary values, and one Byzantine logical identity.
The work therefore supports an explicit schema and natural instantiations, not a
universal statement about all HotStuff-, Tendermint-, or PBFT-family clients.

Transfer to production requires a separate refinement argument covering the
pacemaker, message validation, networking queues, retries, persistence, and
actual certificate construction.

## Conclusion validity

The decisive results are logical language differences and exact finite-state
outcomes, not statistical estimates. No p-values or bug-discovery probabilities
are reported. Counts of schedules or observations are descriptive only.

The parameter and queue-order corpora are regression checks; they do not replace
universal protocol proofs or random-sampling inference.

## Responsible security interpretation

All mutations and adversarial schedules execute locally. The package does not
interact with mainnet, test public validators, transfer assets, or publish an
exploit against a live implementation. A future implementation-level unexpected
finding must be privately reproduced, minimized, and disclosed to maintainers
before release of sensitive details.
