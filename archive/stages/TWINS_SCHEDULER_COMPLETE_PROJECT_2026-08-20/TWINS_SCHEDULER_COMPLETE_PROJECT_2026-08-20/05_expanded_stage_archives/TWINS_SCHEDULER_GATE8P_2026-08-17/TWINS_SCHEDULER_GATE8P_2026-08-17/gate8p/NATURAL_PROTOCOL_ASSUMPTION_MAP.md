# Natural-Protocol Assumption Map

**Date:** 17 August 2026  
**Purpose:** distinguish protocol-motivated premises from claims actually established for a deployed implementation.

## Sources fixed in the artifact

- CometBFT consensus specification and source at release `v0.40.0`, commit `0880b4d378f347ab16e54ec677ff50d803f37d62`, under `inputs/cometbft_v0.40.0/`.
- `relab/hotstuff` Twins harness semantics at commit `3179c6e62929294961acbfd9bf8445769716a121`, recorded in `gate2p/source_manifest.csv` and prior Gate reports.
- The abstract protocol class in `spec/protocol_class.md` and fuller event loop in `spec/full_event_loop.md`.

## Mapping table

| Abstract premise | CometBFT / locking analogue | HotStuff / certificate analogue | Evidence status | Consequence |
|---|---|---|---|---|
| Certificate-driven phases | Proposal, prevote, precommit, PoLC/commit evidence | Proposal/vote/QC phases | **PASS as terminology** | The schema is naturally motivated by real BFT phase structure. |
| Persistent safety-relevant lock | `lockedValue` / `lockedRound` constrain later votes | locked/high-QC state constrains later proposals/votes | **PASS at specification level** | Receiving evidence can remove future conflicting support. |
| Distinct enabling and repair/terminal labels | PoLC/valid-round evidence versus later precommit/commit evidence | enabling QC versus later locking/commit QC | **CONDITIONAL** | Candidate labels exist, but the exact E/R transition pair must be proved per instantiation. |
| E and R share one sender-to-receiver endpoint edge | A leader or relay may send different phase messages to the same validator | A proposer/replica may deliver several phase messages to the same peer | **POSSIBLE, NOT ESTABLISHED AS REQUIRED EXECUTION** | Same-edge coupling is not assumed to hold for every natural execution. |
| Repair R disables the pivot before the second quorum opportunity | Lock/commit processing may reject or prevent later conflicting support | A higher lock/commit state may prevent later conflicting voting | **CONDITIONAL / IMPLEMENTATION-SPECIFIC** | This is the central refinement obligation; it is not inferred merely from the word “lock.” |
| Unique honest pivot between two q=2f+1 quorums | Two minimal quorums can intersect in f Byzantine identities plus one correct identity | Same standard quorum arithmetic | **PASS as combinatorial construction** | Establishes possibility in the schema, not reachability in a production protocol. |
| No alternative honest contributor replaces the pivot | Fixed support sets A and C in the construction | No direct production analogue without a complete execution argument | **SCHEMA-ONLY** | Required for T3; external validity must not silently assume it. |
| Controlled defective transition leaves pivot eligible after E | `MISSING_LOCK_UPDATE` / wrong guard mutation in the model | analogous controlled lock-update omission | **PASS only for injected model mutation** | This is not evidence of a CometBFT or HotStuff bug. |
| G_T can separate E and R | Phase/type-specific filters can express this schedule | Netrix-like filtering can express this control | **PASS as scheduler capability** | The capability itself is prior art, not a contribution. |
| G_D couples all controlled phases on one endpoint edge | Definition of the type-uniform directed grammar | Approximation of a view-level graph with phase erasure | **PASS by formal definition** | A concrete harness must be shown to implement this grammar before the theorem is applied. |
| Finite two-opportunity witness | Two rounds/views in the bounded kernel | Two-view certificate pattern | **PASS for bounded validation** | Does not establish unbounded partial-synchrony or liveness results. |
| Stable-key idempotent duplicate processing | Vote sets keyed by validator/round/type should avoid double weight | signer-set based QC processing should avoid duplicate weight | **CONDITIONAL per implementation** | Replay erasure applies only after checking all five idempotence obligations. |

## Refinement obligations before naming a production protocol instance

1. Define the concrete message labels corresponding to E and R.
2. Prove that both traverse the same abstract scheduler edge.
3. Prove the processing order that makes R disable the pivot before the second opportunity.
4. Prove the absence of a replacement contribution.
5. Show that the controlled defective transition is a meaningful implementation obligation, not an artefact of the kernel.
6. Map concrete decisions/certificates to the paper’s agreement observation.
7. Re-run the witness in a fuller client event loop or provide a formal refinement proof.

## Decision

**CONDITIONAL PASS for construct validity; FAIL for a production-vulnerability claim.** The current paper may state that CometBFT- and HotStuff-style designs motivate the certificate, phase, and lock vocabulary. It may not state that either production protocol realizes the T3 counterexample or contains the controlled mutation.
