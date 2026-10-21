# Seven-validator dependency study

Run `make scaled`, or `PYTHONPATH=src/python python scripts/run_scaled_study.py`. It uses `TWINS_OUTPUT_ROOT` and `TWINS_LOG_DIR` and fails nonzero on a mismatch.

## Scientific question

Can a minimum-cost policy be certified when several admission controls influence multiple local quorum guards and their subsequent emissions? This is not an independent-pivot arithmetic sweep. The compact finite explorer and the dictionary/envelope replay implement local rules separately; neither preloads the two conflicting certificates.

## Declared environment

Seven identities A, P0, P1, C, D, B0, B1; quorum five; one height; two rounds. B0/B1 are Byzantine. The original, one-pivot-mutant, and two-pivot-mutant programs are separate variants. Only the round-zero lock assignment is omitted at selected pivots. A and C remain unmutated and must decide different values for unsafety.

Six controlled fibres are A/B0/B1 to P0 and A/B0/B1 to P1 (height 1, round 0); each has PREVOTE and PRECOMMIT keys. All other admissions follow fixed environment batches. There are sixteen stages and twenty-three one-shot slots. All permutations inside a stage are enumerated, but not reorderings across stages or within a fixed batch. Missing envelopes and disabled timers give conditional no-ops. This does not claim completeness for a production network.

`STAGES` and `run_batch` in the source are the executable bound. Both engines share these environment declarations, not their vote/lock/timer guards. The dictionary engine uses real model HMAC message authentication, distinct received signers, and immutable emitted messages. Its default four-validator behavior is retained unchanged.

## Results and interpretation

The mutant has 48,201 states and 55,283 edges, with 36 unsafe states. Exhaustive ordinary graph reachability over all 4,096 total assignments finds 36 unsafe policies; equality of these two counts is incidental. Every unsafe policy needs a split towards both P0 and P1. Direct synthesis and the certified abstraction procedure both return cost 2 at unit prices. With prices (2,5,9,3,7,11), the optimum is 5. Both select A-to-P0 and A-to-P1. Restricting refinements to P0 is infeasible.

The guard-aware initial partition (449 states) retains stage/remaining slots, the unsafe bit, and each pivot's count of received round-zero value-zero prevotes and emitted precommit. It was selected after exploratory coarse-seed behavior. Its initial cost-zero path is false. Nine safe-policy invariants are required before the final 562-state/961-edge quotient gives a cost-two bound met by a concrete replay. Every iteration checks coverage of all 55,283 edges. Every saved abstract certificate and policy elimination is checked separately.

Direct search discovers 21,544 product states. The ten refinement searches discover 121,615 cumulatively, with peak 21,627. Its final certificate contains 7,130 product states versus 7,103 for direct synthesis. Across ten rounds it checks 30,552 certificate product states and 552,830 input-edge coverage obligations. The full concrete graph is materialized first. The smaller final quotient is an explanatory/certifying artifact, **not evidence of a runtime or total-memory speedup**. Wall-clock observations are separate, noncanonical logs.

The original and one-mutated-pivot variants have no unsafe state (48,071 and 48,141 states, respectively). Three ablations remove cross-pivot prevotes, nil timeout support, or P1's round-one prevote; each removes all violations. A fixed policy has unsafe and safe runs depending on whether the support precommits precede the one-shot timeout attempts. Thus repair suppression is not equivalent to readiness. The witness replay checks 23 successive states, 26 authenticated messages and 418 events, with 11 guard/evidence audits. Eighteen additional safe/mixed replays challenge agreement between the engines.

A 32-group guard-blind seed runs under eight-refinement/10,000-product-state limits and returns unknown. A three-state export cap also returns unknown. Neither is treated as safety or a lower bound that has not been checked.

## Provenance and repeatability

The interrupted revision left models/certificates/PDFs but not their new source. This revision reconstructs source and recomputes outputs. The mutant numbered source/target/key/value relation and unsafe IDs match the preserved graph exactly. The reconstruction retains distinct baseline and one-mutant states and declares a new weighted price case; old byte hashes are not claimed. `summary.json` binds both operational implementations by current SHA-256. All deterministic gzip headers use mtime zero. The manifest is rebuilt only after fresh studies and the reproduction run compares all scaled files byte-for-byte.

## Where the method adds value

A harness designer gets a smallest sufficient set of phase predicates, an explicit static policy, a re-executed regression schedule, and a checkable reason why cheaper settings fail. A false abstract optimum is rejected rather than used as instrumentation advice. A forbidden-interface query produces a bounded infeasibility diagnosis. These benefits do not require falsely claiming that refinement is faster here. The theorem-to-evidence link is C36 in the claim ledger; production-client transition coverage remains an external obligation.
