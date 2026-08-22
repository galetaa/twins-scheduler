# Related-work capability matrix

Evidence cut-off: 21 August 2026.

| Work | Endpoint partitions | Directed | Phase/type | Per instance | Replay | Property-preserving closure | Safety separation witness |
|---|---:|---:|---:|---:|---:|---:|---:|
| Twins | yes | via partitions | no | no | state-loss scenarios | no | no |
| Communication Closure | no | lossy synchronous | no | no | no | yes | no |
| Heard-Of / closed message adversaries | no | yes | no | no | no | semantic model | no |
| Randomized BFT Testing / ByzzFuzz | no | yes | yes | yes | yes | no | no |
| Netrix | no | yes | yes | yes | yes | no | no |
| ByzzBench | configurable | yes | configurable | configurable | configurable | no | no |
| PERF | no | model dependent | fault-type composition | model dependent | model dependent | performance-model reasoning | no |
| ByzTwin-Range | scenario dependent | model dependent | model dependent | model dependent | model dependent | no | no |
| **This work** | defined special case | yes | yes | formalized | yes | **yes** | **yes** |

The table is a capability map, not a quality ranking. A `yes` under a control column does not imply property-preserving completeness, and absence of a mark does not imply that a tool cannot be extended.
