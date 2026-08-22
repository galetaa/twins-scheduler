# Related-work capability matrix

Evidence cut-off: 22 August 2026. Entries distinguish an implemented testing capability from a theorem about property preservation; `not reported` is deliberately more conservative than inferring absence.

| Work | Endpoint partitions | Directed delivery | Phase/type-specific control | Replay | Property-preserving closure theorem | Safety-observation separation witness | Protocol-level conformance | Mechanized proof/model |
|---|---|---|---|---|---|---|---|---|
| Twins | yes | through partitions/scenarios | not reported | state-loss scenarios | no | no | executes protocol implementations | not reported |
| Communication Closure | no | lossy synchronous schedules | no | no | yes, under stated implementation conditions | no | evaluated on consensus implementations | not reported |
| Heard-Of / closed message adversaries | no | yes, as round graphs | no | no | semantic characterization, not this closure | no | no | not reported |
| Randomized BFT Testing / ByzzFuzz | no | yes | yes | yes | no | no | executes BFT implementations | not reported |
| Netrix | no | yes | yes | yes | no | no | implementation-level monitors and filters | not reported |
| ByzzBench | configurable | yes | configurable | configurable | no | no | deterministic implementation benchmark | not reported |
| Mallory | yes, as injected faults | fault-sequence control; not a phase API | no | not reported | no | no | tested deployed distributed systems | not reported |
| PERF fault-injector formalization | model dependent | model dependent | fault-type composition | model dependent | performance-model reasoning, not a safety closure theorem | no | model/deployment comparison | executable Maude formal models |
| **This work** | defined special case | yes | yes | yes, secondary result | **yes** | **yes** | bounded rule-level refinement only | **Lean kernel proof** |

This is a capability map, not a quality ranking. A richer scheduler API is established prior art and is not claimed as the scientific novelty. The contribution is the scoped property-preservation/separation result and its explicit assurance chain.
