# Gate 6′ paper claim freeze

**Freeze date:** 17 August 2026  
**Status:** narrow claim approved for Gate 7′ artifact and manuscript build

## Frozen scientific claim

> For an explicit class of finite certificate-driven locking schemas,
> erasing message-phase distinctions to one type-uniform directed endpoint
> graph can remove agreement-violation witnesses. The mechanism is that
> closure-added repair evidence disables a unique honest quorum pivot before a
> later conflicting certificate can form. Exact replay, by contrast, is
> observationally erasable under stable-key idempotence and state-based safety
> observations.

## Contributions that may be claimed

1. **Local closure criterion.** A relational sufficient condition under which
   closure-added messages preserve unsafety, together with an explicit locking
   boundary where the condition fails.
2. **Parametric separation.** An `n=3f+1`, `q=2f+1` quorum-pivot construction
   separating type-uniform directed scheduling from phase-specific scheduling
   for every `f≥1` under stated schema premises.
3. **Premise characterization.** An exact necessary-and-sufficient Boolean
   characterization for the supplied seven-flag construction, obtained by
   exhaustive evaluation of all 128 assignments.
4. **Replay boundary.** A replay-erasure theorem under stable-key idempotence
   and a constructive failure case for instance-counting quorum logic.
5. **Executable validation.** Two exact kernels from Gate 4′/5′ plus a fuller
   two-round Go event loop, an independent Python mirror, exact conformance, and
   bounded event-order sensitivity.

## Permitted wording

- “There exists a certificate-driven locking schema for which…”
- “Under the explicit phase-coupling and pivot premises…”
- “The supplied bounded event loop reproduces…”
- “In the sources searched through 17 August 2026, we did not find…”
- “The result concerns finite agreement observations.”
- “The controlled mutation models omission of an intended lock update.”

## Wording that is not permitted

- “Partition-based testing is incomplete for all BFT protocols.”
- “Phase-specific scheduling is universally minimal.”
- “CometBFT/HotStuff/Tendermint contains the studied bug.”
- “The method finds more real bugs with higher probability.”
- “The theorem covers liveness or unbounded partial synchrony.”
- “The result proves complete conformance with a production client.”
- “This is the first work” without a refreshed venue-specific prior-art check.
- “The proofs are fully mechanized in Lean/Coq/Isabelle.”

## Claim-to-evidence map

| Claim | Primary evidence |
|---|---|
| T1 replay erasure | `proofs_checked/T1_REPLAY_ERASURE_CHECKED_PROOF.md`; `results/gate6p/t1_replay_erasure_proof_check.json` |
| T2 closure lifting | `proofs_checked/T2_RELATIONAL_CLOSURE_CHECKED_PROOF.md`; `results/gate6p/t2_closure_lifting_proof_check.json` |
| T3 parametric separation | `proofs_checked/T3_QUORUM_PIVOT_CHECKED_PROOF.md`; T3 certificate; Go big-int cross-check |
| Exact premise boundary | `results/gate6p/premise_characterization.json`; 128-row CSV |
| Fuller-loop reproduction | Go/Python event-loop outputs and conformance JSON |
| Event-order robustness | `results/gate6p/event_order_sensitivity.json` |
| Source correspondence | inherited pinned Gate 5′ source mapping and Gate 6′ recheck |

## Remaining pre-submission obligations

1. Independent human proof review or migration to a mature proof assistant.
2. Venue-specific forward/backward citation refresh immediately before
   submission.
3. Freeze a minimal artifact archive and independently reproduce it from a clean
   extraction.
4. Generate all paper figures and tables automatically from machine-readable
   results.
5. Ensure the manuscript presents the theorem before the mutation experiment
   and does not frame the contribution as a new testing DSL.
