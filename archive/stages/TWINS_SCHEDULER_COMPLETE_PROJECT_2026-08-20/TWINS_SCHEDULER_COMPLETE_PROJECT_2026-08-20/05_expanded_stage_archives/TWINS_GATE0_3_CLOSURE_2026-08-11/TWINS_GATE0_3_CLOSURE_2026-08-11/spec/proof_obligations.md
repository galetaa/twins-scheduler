# Gate 1 — Proof obligations and discharge status

| Obligation | Status | Discharge |
|---|---|---|
| PO1. Every `AT_total(k)` trace embeds in `AE`. | PASS | Allowed static branch sets are subsets of dynamic branch sets; event transitions are identical. Tested for binary and ternary bounds. |
| PO2. `AB` and `AE` use the same validator-admissible message language. | PASS FOR PILOT | Exact generated languages are equal at both completed bounds. This is not a new general VLSM proof. |
| PO3. Observation is not vacuous. | PASS | It distinguishes no message, proposal-only, and decision states and detects agreement violations. |
| PO4. Event explorer is complete for the finite quotient. | PASS | Event-level BFS equals independently generated terminal product language for every branch set. |
| PO5. Static width is well-defined. | PASS BUT NOVELTY FAIL | It is exactly the number/minimum cover of mutually incompatible deterministic value histories. |
| PO6. Snapshot active cap is meaningful. | FAIL | Reusable slot plus asynchronous delayed delivery collapses every finite trace to active `k=1`. |
| PO7. The finite-clone theorem is non-definitional. | FAIL | Static realization is one chain per history; lower bound is minimum chain cover. |
| PO8. Safety witness requires more than two branches in the binary model. | FAIL | Exact binary unsafe language is covered by static `k=2`; every unsafe observation has a two-branch core. |
| PO9. A strict hierarchy can occur. | CONDITIONAL BUT NON-SCIENTIFIC | Ternary exact observations can require three branches only because the observation retains a third branch; the safety violation itself has a two-branch subwitness. |
| PO10. Concrete production harness conforms to this ideal network. | UNKNOWN | Requires separate audit of partition-per-view scenario semantics and implementation. |
