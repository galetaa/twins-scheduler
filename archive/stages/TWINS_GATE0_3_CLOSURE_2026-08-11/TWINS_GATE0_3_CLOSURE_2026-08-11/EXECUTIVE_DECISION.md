# Executive decision: Gate 0–3

**Date:** 11 August 2026  
**Original candidate:** finite-clone completeness boundaries of Twins-based BFT safety testing.  
**Decision:** **REJECT THE ORIGINAL CANDIDATE.**

## Gate outcomes

- **Gate 0:** CLOSED — NO-GO. The broad Byzantine/equivocation result is prior art; the residual finite-clone result collapses constructively.
- **Gate 1:** CLOSED — NO-GO. After disambiguating total persistent histories from simultaneous reusable slots, the theorem is either a minimum chain-cover identity or a one-slot collapse.
- **Gate 2:** CLOSED — PASS for the exact pilot. The package reproduces offline in a clean environment.
- **Gate 3:** CLOSED — NO-GO. Exact enumeration hits the predeclared chain-cover/trivial-two-branch stop rule.

## Decisive result

For persistent clones, one clone realizes one causally consistent correct-code history. Therefore the minimum clone count for an exact finite observation is the minimum chain cover of required histories, equal to poset width under the selected compatibility relation.

For reusable active slots with deterministic replay and unbounded finite message delay, one slot can generate all finite branches sequentially and release retained messages later. Thus an active-slot hierarchy collapses to `k=1`.

## Exact pilot

- Binary: `AE=125` observations, `24` unsafe; static `k=1` covers no unsafe observation, static `k=2` covers all; reusable active `k=1` covers all.
- Ternary: `AE=343`, `96` unsafe; static `k=2` covers `72` unsafe and static `k=3` covers all, but every unsafe observation has a two-branch violation core.
- Nine tests pass; event-level BFS equals an independently implemented closed-form quotient.

## Consequence

Do not proceed to the original Gate 4. The only defensible follow-on is a new Gate 0 for a different question: whether a concrete view-partition Twins scenario language is complete for safety witnesses relative to ideal per-message equivocation semantics.
